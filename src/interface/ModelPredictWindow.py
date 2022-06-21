from src.interface.components import AudioPlayerWidget, ClassificationLabelButtonsWidget
from src.tools.Console import Console
console = Console()
console.setOwner("ModelPredictWindow")

from os.path import join as path_join, basename, join, exists, dirname, expanduser
from os import listdir, makedirs
from shutil import move
# from keras.models import load_model
from pickle import load as pickle_load
from joblib import load as joblib_load
from numpy import array, append
from PySide2.QtGui import (
    QBrush,
    QColor,
    QIcon,
    QPainter, 
    QPixmap,
)
from PySide2.QtCore import (
    QCoreApplication,
    QDir,
    QPoint,
    Qt,
    QUrl,
)
from PySide2.QtWidgets import (
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QSizePolicy,
    QSlider,
    QSpacerItem,
    QStyle,
    QVBoxLayout,
    QWidget,
)

from src.interface.ModelOptionsWindow import ModelOptionsWindow
from src.interface.TemplateWindow import TemplateWindow
from src.core.Options import Options

class ModelPredictWindow(TemplateWindow):
    def setupLocalLayout(self):
        mainContainer = QWidget(objectName = "mainContainer")
        audioPlayerWidget = AudioPlayerWidget()
        mainLayout = QHBoxLayout(mainContainer)
        mainLayout.addItem(self.vSpacer)
        mainLayout.addWidget(audioPlayerWidget)
        mainLayout.addItem(self.hSpacer)
        mainLayout.addItem(self.vSpacer)
        
        return mainContainer
    
    def __init__(self):
        options = Options()
        self.options = ModelOptionsWindow(options)

        super().__init__(title="Prediction", localLayout=self.setupLocalLayout, WindowHeight=100, WindowWidth=500)
    
    def updateUi(self, data):
        self.progressLabel.setText('done!')
        self.progressLabelValue = 0
        self.updateLabelButtons(data)
        console.debug("Updated UI")

    def updateProgressLabel(self, value):
        self.progressLabelValue += value;
        self.progressLabel.setText(f'{self.progressLabelValue}/{self.segments}')
        console.debug(f"Loaded Segment {self.progressLabelValue}/{self.segments}")
        
    def updateLabelButtons(self, results):
        self.winner = ''
        self.winner_sus = 0
        for button_pos, (index, result) in enumerate(results):
            self.labelButtons[button_pos].setText(f'{self.labels[index]}: {int((result*100))}%')
            self.labelButtons[button_pos].setEnabled(True)
            if(result > self.winner_sus):
                self.winner_sus = result
                self.winner = self.labels[index]
        self.openButton.setEnabled(True)
                
        if(self.autoTolarance > self.winner_sus * 100):
            self.labelList.update()
            console.info('Manuel action required to continue')
            self.progressLabel.setText('done!')
            return False
                
        if(self.autoMove):
            self.updateFile(self.fileName, self.winner)
        
        if(self.autoNext):
            self.loadNextFile();

    def updateFile(self, path, label):
        folder_dir = join(dirname(path), '#classified')
        if not exists(folder_dir):
            makedirs(folder_dir)
            console.info(f'Created folder {folder_dir}') 
        label_dir = join(folder_dir, label)
        if not exists(label_dir):
            makedirs(label_dir)
            console.info(f'Created folder {label_dir}') 

        path = join(label_dir, basename(path))
        try:
            move(path, path)
            split = '\\'
            console.info(f'{basename(path)} moved to {label_dir.split(split)[-1]}') 
        except FileNotFoundError:
            console.error(f'could not save {basename(path)}')
        
        console.debug(f'Updated File {label}: {basename(path)}')
    