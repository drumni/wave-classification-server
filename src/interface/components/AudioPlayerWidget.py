# A PySide2 Widget for displaying the currently playing Audio file and be able to play, stop and change the time and volume of the audio file.

from PySide2.QtCore import Qt
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QHBoxLayout, QLabel, QPushButton, QSlider, QStyle, QVBoxLayout, QWidget, QSizePolicy, QSpacerItem


from PySide2.QtMultimedia import (
    QMediaPlayer,
    QMediaContent
)

class AudioPlayerWidget(QWidget):
    def __init__(self):
        super(AudioPlayerWidget, self).__init__()
        
        self.maxVolume = 0.1
        self.volume = 0
        self.autoNext = False
        
        
        
        # Start Media Player and set the volume to 0.1
        self.mediaPlayer = QMediaPlayer()
        
        self.initUI()
        
    
    def initUI(self):
        # A Q Spacer item that is used to space out the widgets in the layout.
        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        
        self.audioPlayButton = QPushButton(objectName="playButton")
        self.audioPlayButton.setEnabled(False)
        self.audioPlayButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        
        self.audioReloadButton = QPushButton(objectName="reloadButton")
        self.audioReloadButton.setEnabled(False)
        self.audioReloadButton.setIcon(QIcon('./img/reload.png'))
        
        self.audioNextButton = QPushButton(objectName="nextButton")
        self.audioNextButton.setEnabled(False)
        self.audioNextButton.setIcon(QIcon('./img/next.png'))
        
        self.audioPositionSlider = QSlider(Qt.Horizontal, objectName="positionSlider")
        self.audioPositionSlider.setRange(0, 0)
        
        self.audioVolumeSlider = QSlider(Qt.Vertical, objectName="volumeSlider")
        self.audioVolumeSlider.setRange(0, self.maxVolume)
        self.audioVolumeSlider.setValue(self.volume)
        
        self.audioCoverImage = QLabel(objectName="coverImage")
        
        self.audioLabelText = QLabel("", objectName="labelText")
        self.audioLabelText.setWordWrap(True)
        
        self.controlLayout = QHBoxLayout()
        self.controlLayout.setContentsMargins(0, 0, 0, 0)
        self.controlLayout.addWidget(self.audioPlayButton)
        self.controlLayout.addWidget(self.audioReloadButton)
        self.controlLayout.addWidget(self.audioNextButton)
        self.controlLayout.addWidget(self.audioPositionSlider)

        self.trackLayout = QHBoxLayout()
        self.trackLayout.addWidget(self.audioCoverImage, alignment=Qt.AlignLeft)
        self.trackLayout.addItem(self.horizontalSpacer)
        self.trackLayout.addWidget(self.audioLabelText, alignment=Qt.AlignLeft)
        self.trackLayout.addWidget(self.audioVolumeSlider)

        self.audioPlayerContainer = QWidget(objectName = "playerContainer")
        self.audioPlayerLayout = QVBoxLayout(self.audioPlayerContainer)
        self.audioPlayerLayout.addLayout(self.trackLayout)
        self.audioPlayerLayout.addLayout(self.controlLayout)
        
        self.layoutLayout = QHBoxLayout()
        self.layoutLayout.addWidget(self.audioPlayerContainer)
        self.setLayout(self.layoutLayout)
        
        
        self.audioPlayButton.clicked.connect(self.toggleMediaState)
        # self.audioReloadButton.clicked.connect(self.loadCurrentFile)
        # self.audioNextButton.clicked.connect(self.loadNextFile)
        self.audioPositionSlider.sliderMoved.connect(self.mediaSliderChanged)
        self.audioVolumeSlider.sliderMoved.connect(self.mediaVolumeChanged)
        # self.mediaPlayer.error.connect(self.loadNextFile)
        
        self.mediaPlayer.stateChanged.connect(self.mediaStateChanged)
        self.mediaPlayer.positionChanged.connect(self.positionChanged)
        self.mediaPlayer.durationChanged.connect(self.durationChanged)
        
        
    # def updateTrackCover(self):
    #     pixmap = QPixmap('./img/coverart.jpg')
    #     pixmap_temp = [int(pixmap.width()), int(pixmap.height())]
        
    #     if(self.pixmap_temp == pixmap_temp):
    #         pixmap = QPixmap('./img/default_coverart.jpg')
    #         self.pixmap_temp = pixmap_temp
    #         console.debug("Updated coverart")
            
    #     if pixmap.isNull():
    #         return
        
    #     pixmap = pixmap.scaled(100, 100)
    #     radius = 20

    #     # create empty pixmap of same size as original 
    #     rounded = QPixmap(pixmap.size())
    #     rounded.fill(QColor("transparent"))
        
    #     # # draw rounded rect on new pixmap using original pixmap as brush
    #     painter = QPainter(rounded)
    #     painter.setRenderHint(QPainter.Antialiasing)
    #     painter.setBrush(QBrush(pixmap))
    #     painter.setPen(Qt.NoPen)
    #     painter.drawRoundedRect(pixmap.rect(), radius, radius)
    #     painter.end()
        
    #     self.trackCover.setPixmap(rounded)
    #     console.debug("Created new Pixmap")


    ###############################################################################################################
    #  __       __                  __  __                  _______   __                                          #
    # /  \     /  |                /  |/  |                /       \ /  |                                         #
    # $$  \   /$$ |  ______    ____$$ |$$/   ______        $$$$$$$  |$$ |  ______   __    __   ______    ______   #
    # $$$  \ /$$$ | /      \  /    $$ |/  | /      \       $$ |__$$ |$$ | /      \ /  |  /  | /      \  /      \  #
    # $$$$  /$$$$ |/$$$$$$  |/$$$$$$$ |$$ | $$$$$$  |      $$    $$/ $$ | $$$$$$  |$$ |  $$ |/$$$$$$  |/$$$$$$  | #
    # $$ $$ $$/$$ |$$    $$ |$$ |  $$ |$$ | /    $$ |      $$$$$$$/  $$ | /    $$ |$$ |  $$ |$$    $$ |$$ |  $$/  #
    # $$ |$$$/ $$ |$$$$$$$$/ $$ \__$$ |$$ |/$$$$$$$ |      $$ |      $$ |/$$$$$$$ |$$ \__$$ |$$$$$$$$/ $$ |       #
    # $$ | $/  $$ |$$       |$$    $$ |$$ |$$    $$ |      $$ |      $$ |$$    $$ |$$    $$ |$$       |$$ |       #
    # $$/      $$/  $$$$$$$/  $$$$$$$/ $$/  $$$$$$$/       $$/       $$/  $$$$$$$/  $$$$$$$ | $$$$$$$/ $$/        #
    #                                                                              /  \__$$ |                     #
    #                                                                              $$    $$/                      #
    #                                                                               $$$$$$/                       #
    #                                                                                                             #
    ###############################################################################################################

    def toggleMediaState(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()

    def mediaStateChanged(self, state):
        if self.mediaPlayer.state() == QMediaPlayer.EndOfMedia and self.autoNext:
            self.loadNextFile()

        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.audioPlayButton.setIcon(
                    self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.audioPlayButton.setIcon(
                    self.style().standardIcon(QStyle.SP_MediaPlay))

    def positionChanged(self, position):
        self.audioPositionSlider.setValue(position)

    def durationChanged(self, duration):
        self.audioPositionSlider.setRange(0, duration)

    def mediaSliderChanged(self, position):
        self.mediaPlayer.setPosition(position)
        
    def mediaVolumeChanged(self, value):
        self.mediaPlayer.setVolume(value)
        