
# 4typst

Este es un programita para convertir archivos `.tex` a formato `.typ`.

![](compilar.png)
![](transformar)

El programa hace una conversión usando [pandoc](https://pandoc.org). Se usa el filtro `filtro.lua` para que los ambientes de teoremas queden en formato `#thm[...]`.

El archivo `theorems.typ` es código de [sahasatvik](https://github.com/sahasatvik/typst-theorems).

# Dependencias

- `python`
- Tener `pyqt5` instalado
    - Basta con escribir el comando `pip install pyqt5` en una consola
- Tener la [última versión de pandoc](https://pandoc.org/installing.html) instalada.
    - En Windows basta con usar el instalador que aparece en la página
    - En Linux basta con descargar [la última versión de la página de github](https://github.com/jgm/pandoc/releases) y dejar el binario `pandoc` en la carpeta `$HOME/.local/bin`
- Opcional. Tener `typst` instalado para usar la pestaña `Compilar typst`.
    - En Linux se puede descargar desde la [página de github](https://github.com/typst/typst/releases) y mover el binario `typst` a la carpeta `$HOME/.local/bin`.
    - En Windows no sé. De todas formas, se puede instalar [typst para VSCode(ium)](https://marketplace.visualstudio.com/items?itemName=nvarner.typst-lsp) y tener un editor local integrado.
