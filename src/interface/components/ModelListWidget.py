
from PySide2.QtWidgets import QWidget, QPushButton, QHBoxLayout

class ModelListWidget(QWidget):
    def __init__(self, model=None, onClick=None):
        super(ModelListWidget, self).__init__()
        self.model = model
        self.onClick = onClick
        
        self.initUI()
    
    def initUI(self):
        modelContainer = QWidget(objectName = "secondaryContainer")
        layout = QHBoxLayout(modelContainer)
        layout.addWidget(QPushButton(self.model, clicked = self.updateModelInfoWidget))
        
        layoutLayout = QHBoxLayout()
        layoutLayout.addWidget(modelContainer)
        self.setLayout(layoutLayout)
        
    def updateModelInfoWidget(self):
        self.onClick(self.model)