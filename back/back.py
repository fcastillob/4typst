import subprocess
import re
from os import path
from PyQt5.QtCore import pyqtSignal, QObject


class Back(QObject):
    senal_cambiar_label_error = pyqtSignal(str)
    senal_mensaje = pyqtSignal(str)
    senal_cambiar_label_convertir = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.ruta_typ = ""
        self.ruta_tex = ""
        # mostrar pdf al compilar
        self.mostrar_pdf = False

    def cambiar_ruta_typ(self, texto):
        # Actualiza self.ruta_typ luego de seleccionar el archivo
        self.ruta_typ = texto

    def cambiar_ruta_tex(self, texto):
        # Actualiza self.ruta_tex luego de seleccionar el archivo
        self.ruta_tex = texto

    def compilar_typ(self):
        if self.ruta_typ == "":
            self.senal_mensaje.emit("No hay un archivo seleccionado")
        else:
            res = subprocess.getoutput(f"typst compile {self.ruta_typ}")
            if res == "":
                self.senal_mensaje.emit("Compilado con éxito")
                self.senal_cambiar_label_error.emit("")
                if self.mostrar_pdf:
                    subprocess.run(["xdg-open", self.ruta_typ[:-4]+".pdf"])
            else:
                self.senal_cambiar_label_error.emit(res.encode("utf-8", errors="ignore").decode("utf-8"))

    def transformar_a_typ(self):
        if self.ruta_tex == "":
            self.senal_mensaje.emit("no hay ruta .tex")
            return
        thm = self.obtener_teoremas()
        self.modificar_filtro(thm)

        ruta_tex_aux = self.ruta_tex.replace(" ", "\ ")
        ruta_typ = ruta_tex_aux[:-3] + "typ"
        print(ruta_tex_aux)
        print(ruta_typ)
        res = subprocess.getoutput(f"pandoc -L filtro_tmp.lua -f latex -t typst -s {ruta_tex_aux} > {ruta_typ}")
        print(res)
        # se lee de nuevo para no tomar en cuenta errores de pandoc
        info_archivo = "#import \"theorems.typ\": *\n\n"
        ruta_typ = self.ruta_tex[:-3] + "typ"
        print(ruta_typ)
        with open(ruta_typ, "r") as file:
            for line in file:
                if "sectionnumbering: none" in line:
                    info_archivo += "  sectionnumbering: \"1.\",\n"
                else:
                    info_archivo += line
        info_archivo = info_archivo.replace("#strong[].", "")
        info_archivo = info_archivo.replace(", width: \\textwidth", "")
        with open(ruta_typ, "w") as file:
            file.write(info_archivo)

        self.copiar_archivo_teoremas_typ(thm)

        self.senal_cambiar_label_convertir.emit(ruta_typ)
        print("Éxito")

    def copiar_archivo_teoremas_typ(self, teoremas: list[tuple]):
        ruta_para_theorems = path.join(path.dirname(self.ruta_tex), "theorems.typ")
        print(ruta_para_theorems)
        info_raw = ""
        with open("theorems.typ", "r") as file:
            for line in file:
                info_raw += line
        info_raw += "\n\n"
        for tupla in teoremas:
            info_raw += f"#let {tupla[0]} = thmbox(\"thm\", \"{tupla[1]}\", fill: rgb(\"eeffee\"))\n\n"
        with open(ruta_para_theorems, "w") as file:
            file.write(info_raw)

        print(info_raw)

    def obtener_teoremas(self) -> list[tuple]:
        teoremas = set()
        with open(self.ruta_tex, "r") as file:
            for line in file:
                if "newtheorem{" in line.strip():
                    teoremas.add(line.strip())
        keys_display = []
        print(teoremas)
        for line in teoremas:
            key = re.findall("newtheorem{(.*)}{", line)[0]
            display = re.findall("}{(.*)}$", line)[0]
            keys_display.append((key, display))
        return keys_display

    def modificar_filtro(self, teoremas: list[tuple]):
        thm_mode_str = "thm_mode = {\n"
        for tupla in teoremas:
            thm_mode_str += f"\t\"{tupla[0]}\",\n"
        thm_mode_str += "}\n"

        texto_raw = ""
        with open("filtro.lua", "r") as file:
            for line in file:
                texto_raw += line

        with open("filtro_tmp.lua", "w") as file:
            file.write(thm_mode_str + texto_raw)

        return thm_mode_str + texto_raw
