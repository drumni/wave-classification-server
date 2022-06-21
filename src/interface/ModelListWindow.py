from src.interface.ModelEditorWindow import ModelEditorWindow
from src.interface.ModelPredictWindow import ModelPredictWindow
from src.interface.components import ModelInfoWidget, ModelListWidget
from src.interface.TemplateWindow import TemplateWindow
from src.tools.Console import Console
from PySide2.QtWidgets import QHBoxLayout,  QLabel, QListWidget,  QMainWindow,  QPushButton,  QSizePolicy, QSpacerItem, QVBoxLayout,QWidget

class ModelListWindow(TemplateWindow):
    def __init__(self):
        self.models = ['Foo', 'Bar', 'Baz', 'Bar']
        self.model_selection = None
        super().__init__(title="Model Overview", localLayout=self.setupLocalLayout, WindowHeight=100, WindowWidth=500)
        
        
    def setupLocalLayout(self):
        mainContainer = QWidget(objectName = 'mainContainer')
        
        modelInfoContainer = QWidget()
        modelInfo = QHBoxLayout(modelInfoContainer)
        modelInfoWidget = ModelInfoWidget(model=self.getSelectedModel(), onOpen=self.openModelPredicateDialog)
        modelInfo.addWidget(modelInfoWidget)
        
        newModelWidget = QPushButton("New Model", clicked=self.openModelCreationDialog)
        
        modelListContainer = QWidget()
        modelList = QVBoxLayout(modelListContainer)
        modelList.addWidget(newModelWidget)
        for model in self.models:
            modelList.addWidget(ModelListWidget(model=model, onClick=modelInfoWidget.update))
        
        mainLayout = QHBoxLayout(mainContainer)
        mainLayout.addWidget(modelListContainer)
        mainLayout.addWidget(modelInfoContainer)
        
        return mainContainer
    
    def getSelectedModel(self):
        if self.model_selection is not None:
            return self.models[self.model_selection]
        else:
            return None
    
    def openModelCreationDialog(self):
        print("Creating new model")
        self.creator = ModelEditorWindow()
        self.creator.show()
    
    def openModelPredicateDialog(self, model=None):
        self.prediction = ModelPredictWindow()
        # self.prediction.setSelectModel(model)
        self.prediction.show()
