from os import path
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QMainWindow, QWidget, QFileDialog)
from PyQt5.QtWidgets import (QHBoxLayout, QVBoxLayout, QTabWidget)
from PyQt5.QtWidgets import (QPushButton, QLabel)


class TransformarWidget(QWidget):
    senal_cambiar_tex = pyqtSignal(str)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.abrir = QPushButton('&Abrir archivo .tex', self)
        self.abrir.resize(self.abrir.sizeHint())
        self.abrir.clicked.connect(self.obtener_tex)

        self.archivo = QLabel("Archivo .tex: ", self)

        self.transformar = QPushButton('&Convertir a .typ', self)
        self.transformar.resize(self.transformar.sizeHint())

        self.resultados = QLabel("", self)

        ui = QVBoxLayout()
        ui.addStretch(1)
        ui.addWidget(self.abrir)
        ui.addWidget(self.archivo)
        ui.addWidget(self.transformar)
        ui.addWidget(self.resultados)
        ui.addStretch(1)
        lay_bacan = QHBoxLayout()
        lay_bacan.addStretch(1)
        lay_bacan.addLayout(ui)
        lay_bacan.addStretch(1)
        self.setLayout(lay_bacan)

    def obtener_tex(self):
        archivo = QFileDialog.getOpenFileName(self, "abrir archivo", "", "tex (*.tex)")
        self.archivo.setText(f"Archivo .tex: {str(archivo[0])}")
        self.senal_cambiar_tex.emit(str(archivo[0]))

    def cambiar_resultados(self, ruta):
        texto = f"""Se acaban de escribir los siguientes archivos en la ruta
        {path.dirname(ruta)}

        - theorems.typ
        - {path.basename(ruta)}

        Recuerda personalizar los teoremas en `theorems.typ`.

        También comprueba posibles errores en la conversión"""
        self.resultados.setText(texto)


class CompileWidget(QWidget):
    senal_cambiar_typ = pyqtSignal(str)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.abrir = QPushButton('&Abrir .typ', self)
        self.abrir.resize(self.abrir.sizeHint())
        self.abrir.clicked.connect(self.obtener_typ)

        self.compilar_uno = QPushButton('&Compilar una vez', self)
        self.compilar_uno.resize(self.compilar_uno.sizeHint())

        self.compilar_watch = QPushButton('&Compilar al guardar el documento[no implementado]', self)
        self.compilar_watch.resize(self.compilar_watch.sizeHint())

        self.errores = QLabel(self)
        self.mi_label = QLabel("Archivo .typ:", self)

        ui = QVBoxLayout()
        ui.addStretch(1)
        ui.addWidget(self.abrir)
        ui.addWidget(self.mi_label)
        ui.addWidget(self.compilar_uno)
        ui.addWidget(self.compilar_watch)
        ui.addWidget(self.errores)
        ui.addStretch(1)
        lay_bacan = QHBoxLayout()
        lay_bacan.addStretch(1)
        lay_bacan.addLayout(ui)
        lay_bacan.addStretch(1)
        #  self.setLayout(mi_layout)
        self.setLayout(lay_bacan)

    def obtener_typ(self):
        archivo = QFileDialog.getOpenFileName(self, "abrir archivo", "", "typst (*.typ)")
        self.mi_label.setText(f"Archivo typ: {str(archivo[0])}")
        self.senal_cambiar_typ.emit(str(archivo[0]))

    def cambiar_label_errores(self, text):
        self.errores.setText(text)


class MainWidget(QWidget):
    senal_cambiar_typ = pyqtSignal(str)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tabs = QTabWidget()
        self.compiler = CompileWidget(self)
        self.convert = TransformarWidget(self)
        self.tabs.addTab(self.compiler, "Compilar Typst")
        self.tabs.addTab(self.convert, "Transformar .tex a .typ")
        lay = QVBoxLayout()
        lay.addWidget(self.tabs)
        self.setLayout(lay)


class Ventana(QMainWindow):

    senal_cambio_carpeta = pyqtSignal(str)
    senal_iniciar_partida = pyqtSignal(QMainWindow, list, str)
    senal_almacenar_teclas = pyqtSignal(QWidget, str)
    senal_activar_pausar = pyqtSignal(QPushButton)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("omg")
        self.setGeometry(200, 200, 700, 700)
        self.main = MainWidget(self)
        self.setCentralWidget(self.main)
        self.show()

        # self.menu_bar = self.menuBar()

        tool_bar = self.addToolBar("Toolbar")

        self.statusBar().showMessage("")

    def mostrar_mensaje(self, txt):
        self.statusBar().showMessage(txt)
