from PySide2.QtWidgets import QWidget, QLabel, QPushButton, QHBoxLayout

class ModelInfoWidget(QWidget):
    def __init__(self, model='42', onOpen=None):
        super(ModelInfoWidget, self).__init__()
        self.model = model
        self.onOpen = onOpen
        
        self.initUI()
    
    def initUI(self):
        modelContainer = QWidget(objectName = "secondaryContainer")
        layout = QHBoxLayout(modelContainer)
        self.modelLabel = QLabel(self.getModelName())
        self.modelLoader = QPushButton('Load', clicked=self.openModel)
        self.modelLoader.setDisabled(True)
        layout.addWidget(self.modelLabel)
        layout.addWidget(self.modelLoader)

        layoutLayout = QHBoxLayout()
        layoutLayout.addWidget(modelContainer)
        self.setLayout(layoutLayout)
        
    def update(self, model):
        self.model = model
        if modelName := self.getModelName():
            self.modelLoader.setDisabled(False)
        else:
            self.modelLoader.setDisabled(True)
            
        self.modelLabel.setText(self.getModelName())
        
    def getModelName(self):
        return 'Unknwown' if self.model is None else self.model
    
    def openModel(self):
        self.onOpen(self.model)