from PyQt5.QtCore import QCoreApplication, QDir, QPoint, Qt, QUrl
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtWidgets import  QMainWindow, QApplication, QFileDialog, QHBoxLayout, QLabel, QMessageBox, QPushButton, QSizePolicy, QSlider, QSpacerItem, QStyle, QVBoxLayout, QWidget

from Prediction import Prediction

import sys
import os
import numpy as np

class PredictionManager(QMainWindow):
    def loadButtons(self):
        self.labelButtons = np.array([])
        for index in range(6):
            self.labelButtons = np.append(self.labelButtons, QPushButton("Select Libary Folder"))
            self.labelList.addWidget(self.labelButtons[index])
    
    def __init__(self, parent=None):
        super().__init__()
        
        self.pred = Prediction()
        self.pred.load()
        
        # Window size
        self.WIDTH = 640
        self.HEIGHT = 200
        self.resize(self.WIDTH, self.HEIGHT)

        # Initial
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowOpacity(1)
        self.setWindowTitle("PyQt5 Video Player")
        
        self.labelList = QVBoxLayout()
        self.labelList.setObjectName(u"gridLayout")
        self.loadButtons()

        self.mediaPlayer = QMediaPlayer()

        # play / pause button
        self.playButton = QPushButton()
        self.playButton.setEnabled(False)
        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playButton.clicked.connect(self.play)
 
        # time slider
        self.positionSlider = QSlider(Qt.Horizontal)
        self.positionSlider.setRange(0, 0)
        self.positionSlider.sliderMoved.connect(self.setPosition)
 
        # error output
        self.error = QLabel()
        self.error.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)

        # load button
        self.openButton = QPushButton("Select Libary Folder")
        self.openButton.setToolTip("Open Libary")
        self.openButton.setStatusTip("Open Libary")
        self.openButton.setFixedHeight(24)
        
 
        wid = QWidget(self)
        self.setCentralWidget(wid)

        controlLayout = QHBoxLayout()
        controlLayout.setContentsMargins(0, 0, 0, 0)
        controlLayout.addWidget(self.playButton)
        controlLayout.addWidget(self.positionSlider)
    
        closeButton = QPushButton('X')
        closeButton.clicked.connect(self.closeEvent)
        closeButton.setFixedWidth(20)
        closeButton.setFixedHeight(20)
        
        infoLabel = QLabel('Robin Seerig - Emotion Classification', alignment=Qt.AlignCenter)
        infoLabel.setStyleSheet('margin-top: 60px')

        self.leftSpacer = QSpacerItem(500, 8, QSizePolicy.Maximum, QSizePolicy.Minimum)

        self.mainLayout = QVBoxLayout()
        self.mainLayout.addItem(self.leftSpacer)
        self.mainLayout.addWidget(closeButton, alignment=Qt.AlignRight)
        self.mainLayout.addLayout(controlLayout)
        self.mainLayout.addWidget(self.error)
        self.mainLayout.addWidget(self.openButton)

        self.labelSelectLayout = QVBoxLayout()
        self.labelSelectLayout.addLayout(self.labelList)

        self.observerLayout = QHBoxLayout()
        self.observerLayout.addLayout(self.mainLayout)
        self.observerLayout.addLayout(self.labelSelectLayout)

        layout = QVBoxLayout()
        layout.addLayout(self.observerLayout)
        layout.addWidget(infoLabel)
        wid.setLayout(layout)
 
        self.openButton.clicked.connect(self.openFile)
        self.mediaPlayer.stateChanged.connect(self.mediaStateChanged)
        self.mediaPlayer.positionChanged.connect(self.positionChanged)
        self.mediaPlayer.durationChanged.connect(self.durationChanged)
        self.mediaPlayer.error.connect(self.handleError)
        for x in self.labelButtons:
            x.clicked.connect(self.next)
 
    def closeEvent(self, event):
        QCoreApplication.quit()
 
    def mousePressEvent(self, event):
        if(event.localPos().y() < 30):
            self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        if(event.localPos().y() < 30):
            if hasattr(self, 'oldPos'):
                delta = QPoint(event.globalPos() - self.oldPos)
                self.move(self.x() + delta.x(), self.y() + delta.y())
            self.oldPos = event.globalPos()
 
    def openFile(self):
        folderName = QFileDialog.getExistingDirectory(self, "Select Libary Folder", QDir.homePath()) 
        
        if folderName != '':
            self.predictFolder(folderName)

    def predictFolder(self, folderName):
        self.openButton.setEnabled(False)
        self.folderName = folderName
        self.openButton.setEnabled(False)
        self.pred.files = os.listdir(folderName)
        self.predictFile(0)
        self.playButton.setEnabled(True)
        
        
    def predictFile(self, i):
        fileName = os.path.join(self.folderName, self.pred.files[i])
        self.pred.files.pop(i)
        
        
        # Load Audio
        self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(fileName)))
        self.playButton.setEnabled(True)

        # Load Analysis
        q = self.pred.loadLabel(fileName)
        results = self.loadBetterGuess(q.T)
        for index, result in enumerate(results):
            self.labelButtons[index].setText(f'{result[0]}: {result[1]}')
        self.labelList.update()
        self.openButton.setEnabled(True)
        
    def next(self, event):
        self.playButton.setEnabled(False)
        self.predictFile(0)
        self.playButton.setEnabled(True)

    
    def loadBetterGuess(self, q):
        r = np.empty((0,2))
        for i, d in enumerate(q):
            print(f'{self.pred.labels[i]}, {d}')
            g = np.mean(d)
            data = np.array([ str(self.pred.labels[i]), g])
            r = np.append(r, np.array([data]), axis=0)
        return r
         
    def exitCall(self):
        sys.exit(app.exec_())
 
    def play(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()
 
    def mediaStateChanged(self, state):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.playButton.setIcon(
                    self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.playButton.setIcon(
                    self.style().standardIcon(QStyle.SP_MediaPlay))
 
    def positionChanged(self, position):
        self.positionSlider.setValue(position)
 
    def durationChanged(self, duration):
        self.positionSlider.setRange(0, duration)
 
    def setPosition(self, position):
        self.mediaPlayer.setPosition(position)
 
    def handleError(self):
        self.playButton.setEnabled(False)
        self.error.setText(f"Error: {self.mediaPlayer.errorString()}")

if __name__ == "__main__":
    app = QApplication(sys.argv)

    with open('style.css', 'r') as file:
        data = file.read().replace('\n', ' ')
        app.setStyleSheet(data)

    pred_manager = PredictionManager()
    pred_manager.show()
    
    pred_manager.predictFolder('D:/Musik/Unknow')
    
    sys.exit(app.exec_())

 