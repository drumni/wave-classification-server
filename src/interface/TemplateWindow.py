from src.tools.Console import Console
console = Console()

from os.path import join as join, exists, expanduser
from os import makedirs
from PySide2.QtGui import QIcon
from PySide2.QtCore import QCoreApplication, QPoint, Qt
from PySide2.QtWidgets import QHBoxLayout,  QLabel,  QMainWindow,  QPushButton,  QSizePolicy, QSpacerItem, QVBoxLayout,QWidget

class TemplateWindow(QWidget):
    def __init__(self, 
                title = 'Template', 
                icon_path = './imgwindow-icon.png',
                WindowWidth = 800,
                WindowHeight = 600,
                localLayout = None):
        self.windowHeader = title.split('Window')[0].split('\\')[-1]
        console.setOwner(self.windowHeader)
        super().__init__()
        
        self.minimizeSpacer = QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Minimum)
        
        self.expandingVSpacer = QSpacerItem(1, 1, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.expandingHSpacer = QSpacerItem(1, 1, QSizePolicy.Expanding, QSizePolicy.Minimum)
        
        self.hSpacer = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Maximum)
        self.vSpacer = QSpacerItem(10, 20, QSizePolicy.Maximum, QSizePolicy.Minimum)
        
        console.debug("Loaded Console!")
        self.setupStorage()

        self.WIDTH = WindowWidth
        self.HEIGHT = WindowHeight

        self.setWindowTitle(title)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setWindowIcon(QIcon(icon_path))
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowOpacity(1)
        
        self.resize(self.WIDTH, self.HEIGHT)
        self.setupUi(mainContainer = localLayout())
    
    def setupStorage(self):
        self.storage_location = join(expanduser('~/Documents'), 'SoundModels')
        if not exists(self.storage_location):
            makedirs(self.storage_location)
            console.info(f'created folder {self.storage_location}') 
            
    ##############################################################################################################################################################
    #  __       __  __                  __                                __       __                                                                    __      #
    # /  |  _  /  |/  |                /  |                              /  \     /  |                                                                  /  |     #
    # $$ | / \ $$ |$$/  _______    ____$$ |  ______   __   __   __       $$  \   /$$ |  ______   __     __  ______   _____  ____    ______   _______   _$$ |_    #
    # $$ |/$  \$$ |/  |/       \  /    $$ | /      \ /  | /  | /  |      $$$  \ /$$$ | /      \ /  \   /  |/      \ /     \/    \  /      \ /       \ / $$   |   #
    # $$ /$$$  $$ |$$ |$$$$$$$  |/$$$$$$$ |/$$$$$$  |$$ | $$ | $$ |      $$$$  /$$$$ |/$$$$$$  |$$  \ /$$//$$$$$$  |$$$$$$ $$$$  |/$$$$$$  |$$$$$$$  |$$$$$$/    #
    # $$ $$/$$ $$ |$$ |$$ |  $$ |$$ |  $$ |$$ |  $$ |$$ | $$ | $$ |      $$ $$ $$/$$ |$$ |  $$ | $$  /$$/ $$    $$ |$$ | $$ | $$ |$$    $$ |$$ |  $$ |  $$ | __  #
    # $$$$/  $$$$ |$$ |$$ |  $$ |$$ \__$$ |$$ \__$$ |$$ \_$$ \_$$ |      $$ |$$$/ $$ |$$ \__$$ |  $$ $$/  $$$$$$$$/ $$ | $$ | $$ |$$$$$$$$/ $$ |  $$ |  $$ |/  | #
    # $$$/    $$$ |$$ |$$ |  $$ |$$    $$ |$$    $$/ $$   $$   $$/       $$ | $/  $$ |$$    $$/    $$$/   $$       |$$ | $$ | $$ |$$       |$$ |  $$ |  $$  $$/  #
    # $$/      $$/ $$/ $$/   $$/  $$$$$$$/  $$$$$$/   $$$$$/$$$$/        $$/      $$/  $$$$$$/      $/     $$$$$$$/ $$/  $$/  $$/  $$$$$$$/ $$/   $$/    $$$$/   #
    #                                                                                                                                                            #
    ##############################################################################################################################################################

    def mousePressEvent(self, event):
        self.moveWindow = event.pos().y() < 69
        if (event.button() == Qt.LeftButton):
            self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        if not self.moveWindow:
            return
        if hasattr(self, 'oldPos'):
            delta = QPoint(event.globalPos() - self.oldPos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()
        
        
    ##############################################################################
    #   ______               __                                __    __  ______  #
    #  /      \             /  |                              /  |  /  |/      | #
    # /$$$$$$  |  ______   _$$ |_    __    __   ______        $$ |  $$ |$$$$$$/  #
    # $$ \__$$/  /      \ / $$   |  /  |  /  | /      \       $$ |  $$ |  $$ |   #
    # $$      \ /$$$$$$  |$$$$$$/   $$ |  $$ |/$$$$$$  |      $$ |  $$ |  $$ |   #
    #  $$$$$$  |$$    $$ |  $$ | __ $$ |  $$ |$$ |  $$ |      $$ |  $$ |  $$ |   #
    # /  \__$$ |$$$$$$$$/   $$ |/  |$$ \__$$ |$$ |__$$ |      $$ \__$$ | _$$ |_  #
    # $$    $$/ $$       |  $$  $$/ $$    $$/ $$    $$/       $$    $$/ / $$   | #
    #  $$$$$$/   $$$$$$$/    $$$$/   $$$$$$/  $$$$$$$/         $$$$$$/  $$$$$$/  #
    #                                         $$ |                               #
    #                                         $$ |                               #
    #                                         $$/                                #
    #                                                                            #
    ##############################################################################

    def quitUi(self):
        self.stopThread()
        self.close()

    def stopThread(self):
        pass

    def setupUi(self, mainContainer):
        if not mainContainer:
            mainContainer = QWidget(objectName = "mainContainer")
        
        self.mainContainer = mainContainer
        
        self.setupUiElements()
        console.debug('Loaded Elements')
        self.setupUiStructure()
        console.debug('Loaded Structure')
        self.setupUiEvents()
        console.debug('Loaded Events')

    def setupUiElements(self):
        self.exitButton = QPushButton(objectName="toolbarButton")
        self.exitButton.setIcon(QIcon('./img/close.png'))
        
        self.windowLabel = QLabel(self.windowHeader, objectName="windowLabel")
        self.infoLabel = QLabel('42', alignment=Qt.AlignRight, objectName='infoLabel')

    def setupUiStructure(self):
        toolbarContainer = QWidget(objectName = "toolbarContainer")
        toolbarLayout = QHBoxLayout(toolbarContainer)
        toolbarLayout.addWidget(self.windowLabel)
        toolbarLayout.addItem(self.minimizeSpacer)
        toolbarLayout.addWidget(self.exitButton, alignment= Qt.AlignRight | Qt.AlignTop)

        footprintLayout = QHBoxLayout()
        footprintLayout.addWidget(self.infoLabel)

        layoutContainer = QWidget(objectName = "windowContainer")
        layout = QVBoxLayout(layoutContainer)
        layout.addWidget(toolbarContainer)
        # layout.addItem(self.vSpacer)
        layout.addWidget(self.mainContainer)
        # layout.addItem(self.vSpacer)
        layout.addLayout(footprintLayout)
        
        self.layoutLayout = QHBoxLayout()
        self.layoutLayout.addWidget(layoutContainer)
        self.setLayout(self.layoutLayout)
    
    def setupUiEvents(self):
        console.link(outputTypes='INFO', method=self.infoLabel)
        self.exitButton.clicked.connect(self.quitUi)
