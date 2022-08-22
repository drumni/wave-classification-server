from src.tools.Console import Console
console = Console()
console.setOwner(__file__)


from PySide2.QtCore import Qt
from PySide2.QtWidgets import QPushButton, QVBoxLayout
from PySide2.QtWidgets import QWidget
from numpy import array
from numpy.lib.function_base import append

class ClassificationLabelButtonsWidget(QWidget):
    def __init__(self):
        self.labelList = QVBoxLayout(objectName="labelList")
        self.labelList.setObjectName(u"gridLayout")
        self.setupLabelButtons()
        
             
    ##########################################################################################################################
    #  __                  __                  __        _______               __      __                                    #
    # /  |                /  |                /  |      /       \             /  |    /  |                                   #
    # $$ |        ______  $$ |____    ______  $$ |      $$$$$$$  | __    __  _$$ |_  _$$ |_     ______   _______    _______  #
    # $$ |       /      \ $$      \  /      \ $$ |      $$ |__$$ |/  |  /  |/ $$   |/ $$   |   /      \ /       \  /       | #
    # $$ |       $$$$$$  |$$$$$$$  |/$$$$$$  |$$ |      $$    $$< $$ |  $$ |$$$$$$/ $$$$$$/   /$$$$$$  |$$$$$$$  |/$$$$$$$/  #
    # $$ |       /    $$ |$$ |  $$ |$$    $$ |$$ |      $$$$$$$  |$$ |  $$ |  $$ | __ $$ | __ $$ |  $$ |$$ |  $$ |$$      \  #
    # $$ |_____ /$$$$$$$ |$$ |__$$ |$$$$$$$$/ $$ |      $$ |__$$ |$$ \__$$ |  $$ |/  |$$ |/  |$$ \__$$ |$$ |  $$ | $$$$$$  | #
    # $$       |$$    $$ |$$    $$/ $$       |$$ |      $$    $$/ $$    $$/   $$  $$/ $$  $$/ $$    $$/ $$ |  $$ |/     $$/  #
    # $$$$$$$$/  $$$$$$$/ $$$$$$$/   $$$$$$$/ $$/       $$$$$$$/   $$$$$$/     $$$$/   $$$$/   $$$$$$/  $$/   $$/ $$$$$$$/   #
    #                                                                                                                        #
    ##########################################################################################################################
    
    # def manuallySelectLabel(self):
    #     self.winner_man = self.sender().text().split(":")[0]
    #     self.updateFile(self.fileName, self.winner_man)
        
    #     self.labelList.update()
    #     self.openButton.setEnabled(True)
    #     self.loadNextFile();
        
    def setupLabelButtons(self):
        try:
            self.labelButtons = array([])
            for index in range(len(self.labels)):
                self.labelButtons = append(self.labelButtons, QPushButton(self.labels[index], objectName='labelButtons'))
                self.labelButtons[index].setEnabled(False)
                self.labelButtons[index].setFixedWidth(100)
                self.labelList.addWidget(self.labelButtons[index], alignment=Qt.AlignLeft)
                self.labelButtons[index].clicked.connect(self.manuallySelectLabel)
        except AttributeError:
            console.debug('ok')
            # Console.debug('42 is loaded')

    # def refreshLabelButton(self):
    #     if hasattr(self, 'labelList'):
    #         self.clearLayout(self.labelList)
    #     self.setupLabelButtons()
        
    # def clearLayout(self, layout):
    #     while layout.count():
    #         child = layout.takeAt(0)
    #         if child.widget():
    #             child.widget().deleteLater()