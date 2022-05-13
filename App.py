import sys
import os

from src.interface.PredictionWindow import PredictionWindow
from src.interface.SplashScreen import SplashScreen
from src.tools.Animation import opacity

from PyQt5.QtCore import (
    Qt,
)

from PyQt5.QtWidgets import (
    QApplication,
)

from src.tools.ColorTheme import ColorTheme

# logging.basicConfig(format="%(message)s", level=logging.INFO)
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("emotions are Real")
    
    color_theme = ColorTheme()
    app.setStyleSheet(color_theme.loadData())
    
    window = PredictionWindow()
    window.setWindowOpacity(0)
        
    splash = SplashScreen('./img/load.gif', Qt.WindowStaysOnTopHint)
    window.setWindowOpacity(0)
    
    splash.show()
    opacity(splash, 0, 1, 0.001)
    opacity(splash, 1, 0, 0.001)
    
    window.show()
    opacity(window, 0, 1, 0.001)
    
    window.loadLibaryFolder('D:\\Musik\\Genres\\Electronic\\DnB\\liquid')
    splash.finish(window)
    sys.exit(app.exec())