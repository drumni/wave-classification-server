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

class OptionsWindow(QWidget):
    saved = Signal(str, str, int, bool)
    isOpen = False
    
    def __init__(self, data_dir, model_dir, segments, autoMove):
        super().__init__()
        isOpen = True
        
        self.data_dir = data_dir
        self.model_dir = model_dir
        self.segments = segments
        self.autoMove = autoMove
        
        self.WIDTH = 80*5
        self.HEIGHT = 20*5
        
        self.windowHeader = 'Options'
        self.setWindowTitle("Emotions are Real | Options")
        # QMainWindow.__init__(self, None, Qt.WindowStaysOnTopHint)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setWindowIcon(QIcon('./img/icons/window-icon.png'))
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowOpacity(1)
        self.resize(self.WIDTH, self.HEIGHT)
        self.setupUi()
    
    def saveOptions(self):
        # print(f'Segments: {self.segments}')
        # print(f'Model: {self.model_dir}')
        # print(f'Data: {self.data_dir}')
        self.saved.emit(self.data_dir, self.model_dir, self.segments)
        # print("Save options")
    
    def updateModelDir(self, dir):
        self.model_dir = dir
        
    def updateDataDir(self, dir):
        self.data_dir = dir
        self.modelSelectorComboBox.clear()
        self.setupModelComBox()
                
    def updateSegments(self, segments):
        # print(segments)
        self.segments = segments
        self.segmentSliderLabel.setText(str(self.segments))
            
    def setupUi(self):
        self.setupUiElements()
        self.setupUiStructure()
        self.setupUiEvents()
    
    def setupUiElements(self):
        self.expandingVSpacer = QSpacerItem(1, 1, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.expandingHSpacer = QSpacerItem(1, 1, QSizePolicy.Expanding, QSizePolicy.Minimum)
        
        self.hSpacer = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Maximum)
        self.vSpacer = QSpacerItem(10, 20, QSizePolicy.Maximum, QSizePolicy.Minimum)
        
        self.exitButton = QPushButton(objectName="toolbarButton", clicked =self.quitUi)
        self.exitButton.setIcon(QIcon('./img/icons/close.png'))
        
        self.saveButton = QPushButton(objectName="toolbarButton", clicked =self.saveOptions)
        self.saveButton.setIcon(QIcon('./img/icons/save.png'))
        
        self.datasetSelectorComboBox = QComboBox(objectName="selector")
        self.setupDataComBox()
        
        self.modelSelectorComboBox = QComboBox(objectName="selector")
        self.setupModelComBox()

        self.windowLabel = QLabel(self.windowHeader, objectName="windowLabel")
        
        self.segmentSlider = QSlider(Qt.Horizontal, minimum=1, maximum=50, objectName="positionSlider")
        self.segmentSliderLabel = QLabel(str(self.segments), objectName="trackLabel")
        self.segmentSlider.setValue(self.segments)

        self.autoMoveButton = QPushButton(objectName="labelButtons", clicked=self.updateAutoMove)
        self.autoMoveButton.setText('Move files automatic:' + ('On' if self.autoMove else 'Off'))

    def updateAutoMove(self):
        self.autoMove = not self.autoMove
        self.autoMoveButton.setText('Move files automatic: ' + ('On' if self.autoMove else 'Off'))

    def setupDataComBox(self):
        trained = listdir('data')
        for i, train in enumerate(trained):
            if(i == 0):
                self.data_dir = train
            self.datasetSelectorComboBox.addItem(train)
            
        index = self.datasetSelectorComboBox.findText(self.data_dir, Qt.MatchFixedString)
        if index >= 0:
            self.datasetSelectorComboBox.setCurrentIndex(index)

    def setupModelComBox(self):
        models = listdir(join('data', self.data_dir))
        for model in models:
            if '.h5' in model:
                self.modelSelectorComboBox.addItem(model)

        # print(self.model_dir)
        index = self.modelSelectorComboBox.findText(self.model_dir, Qt.MatchFixedString)
        if index >= 0:
            self.modelSelectorComboBox.setCurrentIndex(index)
    
    def setupUiEvents(self):
        self.datasetSelectorComboBox.currentTextChanged.connect(self.updateDataDir)
        self.modelSelectorComboBox.currentTextChanged.connect(self.updateModelDir)
        self.segmentSlider.valueChanged.connect(self.updateSegments)

    def setupUiStructure(self):
        sliderLayout = QHBoxLayout()
        sliderLayout.addWidget(self.segmentSliderLabel)
        sliderLayout.addWidget(self.segmentSlider)
        
        optionsContainer = QWidget(objectName = "playerContainer")
        optionsLayout = QVBoxLayout(optionsContainer)
        optionsLayout.addWidget(self.datasetSelectorComboBox)
        optionsLayout.addWidget(self.modelSelectorComboBox)
        optionsLayout.addLayout(sliderLayout)
        optionsLayout.addWidget(self.autoMoveButton)
        optionsLayout.addItem(self.expandingVSpacer)
        
        toolbarContainer = QWidget(objectName = "toolbarContainer")
        toolbarLayout = QHBoxLayout(toolbarContainer)
        toolbarLayout.addWidget(self.windowLabel)
        toolbarLayout.addItem(self.expandingHSpacer)
        toolbarLayout.addWidget(self.saveButton, alignment= Qt.AlignRight | Qt.AlignTop)
        toolbarLayout.addWidget(self.exitButton, alignment= Qt.AlignRight | Qt.AlignTop)

        layoutContainer = QWidget(objectName = "window")
        layout = QVBoxLayout(layoutContainer)
        layout.addWidget(toolbarContainer)
        layout.addWidget(optionsContainer)
        
        layoutLayout = QHBoxLayout()
        layoutLayout.addWidget(layoutContainer)
        self.setLayout(layoutLayout)

    def quitUi(self):
        self.close()
        isOpen = False
                
    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        if hasattr(self, 'oldPos'):
            delta = QPoint(event.globalPos() - self.oldPos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()