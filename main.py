import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import pyqtSignal, QTimer, QObject, QThread

from front.front import Ventana
from back.back import Back

# TODO
app = QApplication([])
ventana = Ventana()
back = Back()
ventana.main.compiler.senal_cambiar_typ.connect(back.cambiar_ruta_typ)
ventana.main.compiler.compilar_uno.clicked.connect(back.compilar_typ)
back.senal_mensaje.connect(ventana.mostrar_mensaje)
back.senal_cambiar_label_error.connect(ventana.main.compiler.cambiar_label_errores)
ventana.main.convert.senal_cambiar_tex.connect(back.cambiar_ruta_tex)
ventana.main.convert.transformar.clicked.connect(back.transformar_a_typ)
back.senal_cambiar_label_convertir.connect(ventana.main.convert.cambiar_resultados)

sys.exit(app.exec())
