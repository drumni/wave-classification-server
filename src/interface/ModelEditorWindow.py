from src.interface.components.LibraryTableWidget import LibraryTableWidget
from src.service.AudioLibaryService import AudioLibaryService
from src.interface.TemplateWindow import TemplateWindow

from PySide2.QtWidgets import QLabel, QPushButton, QLineEdit, QVBoxLayout, QWidget, QHBoxLayout
# pyside2 -
class ModelEditorWindow(TemplateWindow):
    def __init__(self):
        self.service = AudioLibaryService()
        
        super().__init__(title="Model Editor", localLayout=self.setupLocalLayout, WindowHeight=100, WindowWidth=500)

        # create AudioLibaryService thread
        
        
    def setupLocalLayout(self):
        mainContainer = QWidget(objectName = "mainContainer")
        mainLayout = QVBoxLayout(mainContainer)
        
        # create pyside2 Name input field for the name
        modelNameInputField = QLineEdit()
        mainLayout.addWidget(modelNameInputField)
        
        # table of data self.selection from AudioLibaryService
        
        libraryTableWidget = LibraryTableWidget(library=self.service.library)
        mainLayout.addWidget(libraryTableWidget)
        
        # add folder button that open dictionary path selection dialog and add the selected path to the model
        
        return mainContainer
      