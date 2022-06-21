from sys import exit
from src.interface.ModelListWindow import ModelListWindow
from PySide2.QtWidgets import QApplication
from src.tools.ColorTheme import ColorTheme

if __name__ == "__main__":
    app = QApplication()
    app.setApplicationName(__file__)
    color_theme = ColorTheme()
    app.setStyleSheet(color_theme.loadData())
    window = ModelListWindow()
    window.show()
    exit(app.exec_())