from os.path import join, basename
from os import listdir

from keras.models import load_model

from joblib import load as joblib_load
from pickle import load as pickle_load
from numpy import array, append

from PyQt5.QtGui import (
    QBrush,
    QColor,
    QIcon,
    QPainter, 
    QPixmap,
)
from PyQt5.QtCore import (
    QCoreApplication,
    QDir,
    QPoint,
    Qt,
    QUrl,
)
from PyQt5.QtMultimedia import (
    QMediaPlayer,
    QMediaContent
)

from PyQt5.QtWidgets import (
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

from src.core.Prediction import Prediction
from src.interface.OptionsWindow import OptionsWindow
from src.tools.Coverart import loadCoverart

class PredictionWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.folderName = QDir.homePath()
        self.seconds = 3
        
        self.data_dir = 'Emotions'
        self.model_dir = 'model[3]_0.93_best.h5'
        self.segments = 4
        
        self.WIDTH = 640
        self.HEIGHT = 200

        self.pixmap_temp = [0, 0]

        self.windowHeader = 'Music Classification Tool'
        
        self.setWindowTitle("Emotions are Real")
        QMainWindow.__init__(self, None, Qt.WindowStaysOnTopHint)
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setWindowIcon(QIcon('./img/icons/window-icon.png'))
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowOpacity(1)
        self.resize(self.WIDTH, self.HEIGHT)
        
        self.mediaPlayer = QMediaPlayer()
        
        self.updateOptions(self.data_dir, self.model_dir, self.segments)
        self.setupUi()

            
    # @pyqtSignal(str, str, int)
    def updateOptions(self, data_dir, model_dr, segments):
        self.data_dir = join('data', data_dir)
        self.segments = segments
        # print(data_dir, model_dr, segments)
        self.model = load_model(join(self.data_dir, model_dr))

        self.scaler = joblib_load(join(self.data_dir, "scaler.pkl"))  # load from disk
        with open(join(self.data_dir, "labels.pkl"), "rb") as a_file:
            self.labels = pickle_load(a_file)
            
    def setupUi(self):
        self.setupUiElements()
        self.setupUiStructure()
        self.setupUiEvents()

    def setupUiStructure(self):
        controlLayout = QHBoxLayout()
        controlLayout.setContentsMargins(0, 0, 0, 0)
        controlLayout.addWidget(self.playButton)
        controlLayout.addWidget(self.positionSlider)

        trackLayout = QHBoxLayout()
        trackLayout.addWidget(self.trackCover, alignment=Qt.AlignLeft)
        trackLayout.addItem(self.hSpacer)
        trackLayout.addWidget(self.trackLabel, alignment=Qt.AlignLeft)

        playerContainer = QWidget(objectName = "playerContainer")
        playerLayout = QVBoxLayout(playerContainer)
        # playerLayout.addItem(self.vSpacer)
        playerLayout.addLayout(trackLayout)
        # playerLayout.addItem(self.vSpacer)
        playerLayout.addLayout(controlLayout)

        labelLayout = QVBoxLayout()
        labelLayout.addLayout(self.labelList)

        observerLayout = QHBoxLayout()
        observerLayout.addItem(self.vSpacer)
        observerLayout.addWidget(playerContainer)
        observerLayout.addItem(self.hSpacer)
        observerLayout.addLayout(labelLayout)
        observerLayout.addItem(self.vSpacer)

        toolbarContainer = QWidget(objectName = "toolbarContainer")
        toolbarLayout = QHBoxLayout(toolbarContainer)
        toolbarLayout.addWidget(self.windowLabel)
        toolbarLayout.addItem(self.expandingHSpacer)
        toolbarLayout.addWidget(self.openButton, alignment= Qt.AlignRight | Qt.AlignTop)
        toolbarLayout.addWidget(self.optionsButton, alignment= Qt.AlignRight | Qt.AlignTop)
        toolbarLayout.addWidget(self.exitButton, alignment= Qt.AlignRight | Qt.AlignTop)

        layoutContainer = QWidget(objectName = "window")
        layout = QVBoxLayout(layoutContainer)
        layout.addWidget(toolbarContainer)
        layout.addItem(self.vSpacer)
        layout.addLayout(observerLayout)
        layout.addWidget(self.infoLabel)
        
        layoutLayout = QHBoxLayout()
        layoutLayout.addWidget(layoutContainer)
        self.centralWidget.setLayout(layoutLayout)

    def setupUiElements(self):
        self.expandingVSpacer = QSpacerItem(1, 1, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.expandingHSpacer = QSpacerItem(1, 1, QSizePolicy.Expanding, QSizePolicy.Minimum)
        
        self.hSpacer = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Maximum)
        self.vSpacer = QSpacerItem(10, 20, QSizePolicy.Maximum, QSizePolicy.Minimum)

        self.playButton = QPushButton(objectName="playButton")
        self.playButton.setEnabled(False)
        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        
        self.positionSlider = QSlider(Qt.Horizontal, objectName="positionSlider")
        self.positionSlider.setRange(0, 0)
        
        self.labelList = QVBoxLayout(objectName="labelList")
        self.labelList.setObjectName(u"gridLayout")
        self.setupLabelButtons()
        
        self.trackCover = QLabel(objectName="trackCover")
        
        self.trackLabel = QLabel("", objectName="trackLabel")
        self.trackLabel.setWordWrap(True)
        self.trackLabel.setFixedWidth(self.WIDTH * 0.6)
        self.trackLabel.setFixedHeight(self.HEIGHT * 0.7)

        # size = 28
        self.openButton = QPushButton(objectName="toolbarButton")
        self.openButton.setIcon(QIcon('./img/icons/album-folder.png'))
        
        self.optionsButton = QPushButton(objectName="toolbarButton")
        self.optionsButton.setIcon(QIcon('./img/icons/settings.png'))
        
        self.exitButton = QPushButton(objectName="toolbarButton")
        self.exitButton.setIcon(QIcon('./img/icons/close.png'))
        
        self.windowLabel = QLabel(self.windowHeader, objectName="windowLabel")
        
        self.infoLabel = QLabel('Emotion Classification', alignment=Qt.AlignRight, objectName='infoLabel')
    
    def setupUiEvents(self):
        self.playButton.clicked.connect(self.toggleAudio)
        self.positionSlider.sliderMoved.connect(self.setSliderPosition)
        self.exitButton.clicked.connect(self.quitUi)
        self.optionsButton.clicked.connect(self.openOptionsWindow)
        self.openButton.clicked.connect(self.loadLibaryFolder)
        self.mediaPlayer.error.connect(self.loadNextFile)
        
        self.mediaPlayer.stateChanged.connect(self.mediaStateChanged)
        self.mediaPlayer.positionChanged.connect(self.positionChanged)
        self.mediaPlayer.durationChanged.connect(self.durationChanged)

    def quitUi(self, _):
        self.stopThread()
        QCoreApplication.quit()

    def openOptionsWindow(self):
        self.options = OptionsWindow(self.data_dir, self.model_dir, self.segments)
        self.options.saved.connect(self.updateOptions)
        self.options.show()
        
    def updateUi(self, data):
        self.updateLabelButtons(data)
        
    def clearLayout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def updateTrackCover(self):
        pixmap = QPixmap('./img/coverart.jpg')
        pixmap_temp = [int(pixmap.width()), int(pixmap.height())]
        
        if(self.pixmap_temp == pixmap_temp):
            pixmap = QPixmap('./img/default_coverart.jpg')
            self.pixmap_temp = pixmap_temp
            
        if pixmap.isNull():
            return
        
        pixmap = pixmap.scaled(100, 100)
        radius = 20

        # create empty pixmap of same size as original 
        rounded = QPixmap(pixmap.size())
        rounded.fill(QColor("transparent"))
        
        # # draw rounded rect on new pixmap using original pixmap as brush
        painter = QPainter(rounded)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QBrush(pixmap))
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(pixmap.rect(), radius, radius)
        painter.end()
        
        self.trackCover.setPixmap(rounded)
        
    def updateLabelButtons(self, results):
        self.winner = ''
        self.winner_sus = 0
        for button_pos, (index, result) in enumerate(results):
            self.labelButtons[button_pos].setText(f'{self.labels[index]}: {int((result*100))}%')
            self.labelButtons[button_pos].setEnabled(True)
            if(result > self.winner_sus):
                self.winner_sus = result
                self.winner = self.labels[index]
        # print(f'Winner: {self.winner} | {int(self.winner_sus*100)}%')

        self.labelList.update()
        self.openButton.setEnabled(True)

    def setupLabelButtons(self):
        self.labelButtons = array([])
        for index in range(len(self.labels)):
            self.labelButtons = append(self.labelButtons, QPushButton(self.labels[index], objectName='labelButtons'))
            self.labelButtons[index].setEnabled(False)
            self.labelButtons[index].setFixedWidth(100)
            self.labelList.addWidget(self.labelButtons[index], alignment=Qt.AlignLeft)
            self.labelButtons[index].clicked.connect(self.loadNextFile)

    def refreshLabelButton(self):
        self.clearLayout(self.labelList)
        self.setupLabelButtons()

    def loadNextFile(self, _ = None):
        self.playButton.setEnabled(False)
        self.refreshLabelButton()

        # sending_button = self.sender()
        # actual_genre = sending_button.text().split(':')[0]
        if(len(self.files) <= 0):
            self.openButton.setEnabled(True)
            return False
            
        self.fileName = join(self.folderName, self.files[0])
        loadCoverart(self.fileName)

        self.files.pop(0)

        self.trackLabel.setText(basename(self.fileName))
        self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(self.fileName)))
        self.playButton.setEnabled(True)
        self.toggleAudio()
        
        self.stopThread()
        self.thread = Prediction(file=self.fileName, options=self)
        self.thread.result_value.connect(self.updateUi)
        self.thread.start()

        self.updateTrackCover()

    def stopThread(self):
        if (type(self.thread) == Prediction) and self.thread.isRunning:
            self.thread.stop()
            self.thread.quit()

    def loadLibaryFolder(self, folderName = None):
        if type(folderName) is not str:
            folderName = QFileDialog.getExistingDirectory(self, "Select Libary Folder", self.folderName)
        if folderName != '':
            self.openButton.setEnabled(False)
        
            self.folderName = folderName
            self.files = listdir(folderName)
            self.refreshLabelButton()
            self.loadNextFile()

    def toggleAudio(self):
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

    def setSliderPosition(self, position):
        self.mediaPlayer.setPosition(position)

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        if hasattr(self, 'oldPos'):
            delta = QPoint(event.globalPos() - self.oldPos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()