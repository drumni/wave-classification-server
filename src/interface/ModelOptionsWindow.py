from os.path import join
from os import listdir

from PySide2.QtGui import (
    QIcon,
)
from PySide2.QtCore import (
    QPoint,
    Qt,
    Signal,
)
from src.interface.TemplateWindow import TemplateWindow
from PySide2.QtWidgets import (
    QComboBox,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSizePolicy,
    QSlider, 
    QSpacerItem,
    QVBoxLayout,
    QWidget,
)

from src.core.Options import Options

class ModelOptionsWindow(TemplateWindow):
    def __init__(self, options: Options):
        self.options = options
        
        self.WIDTH = 80*5
        self.HEIGHT = 20*5
        
        # super().__init__(__file__)
        

      
    ####################################################################
    #   ______               __      __                                #
    #  /      \             /  |    /  |                               #
    # /$$$$$$  |  ______   _$$ |_   $$/   ______   _______    _______  #
    # $$ |  $$ | /      \ / $$   |  /  | /      \ /       \  /       | #
    # $$ |  $$ |/$$$$$$  |$$$$$$/   $$ |/$$$$$$  |$$$$$$$  |/$$$$$$$/  #
    # $$ |  $$ |$$ |  $$ |  $$ | __ $$ |$$ |  $$ |$$ |  $$ |$$      \  #
    # $$ \__$$ |$$ |__$$ |  $$ |/  |$$ |$$ \__$$ |$$ |  $$ | $$$$$$  | #
    # $$    $$/ $$    $$/   $$  $$/ $$ |$$    $$/ $$ |  $$ |/     $$/  #
    #  $$$$$$/  $$$$$$$/     $$$$/  $$/  $$$$$$/  $$/   $$/ $$$$$$$/   #
    #           $$ |                                                   #
    #           $$ |                                                   #
    #           $$/                                                    #
    #                                                                  #
    ####################################################################
    
    # def updateOptions(self, data_dir, model_dir, segments, autoTolarance, autoMove, autoNext):
    #     self.autoMove = autoMove
    #     self.autoNext = autoNext
    #     self.autoTolarance = autoTolarance
    #     self.segments = segments
        
    #     if data_dir:
    #         self.data_dir = path_join(self.storage_location, data_dir)
            
    #     try:
    #         console.debug("Load Model")
    #         self.model = load_model(path_join(self.data_dir, model_dir))
    #     except (OSError, TypeError):
    #         console.error(f'Model {model_dir} not found in {self.data_dir}')
    #         self.model = None
    
    #     try:
    #         console.debug("Load Scaler")
    #         self.scaler = joblib_load(path_join(self.data_dir, "scaler.pkl"))
    #     except (FileNotFoundError, TypeError):
    #         console.error(f'Scaler not found in {self.data_dir}')
    #         self.scaler = None

    #     try: 
    #         console.debug("Load Labels")
    #         with open(path_join(self.data_dir, "labels.pkl"), "rb") as a_file:
    #             self.labels = pickle_load(a_file)
    #     except (FileNotFoundError, TypeError):
    #         console.error(f'Labels not found in {self.data_dir}')
    #         self.labels = []
            
    #     self.refreshLabelButton()
    #     console.debug("Updated options")
            
    # def openOptionsWindow(self):
    #     if not self.options and hasattr(self.options, 'isVisible') and self.options.isVisible():
    #         self.options.quitUi()
    #         return 0
    #     self.options.show()
    #     console.debug("Opened options window")
    
    