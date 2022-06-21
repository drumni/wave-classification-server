from PySide2.QtCore import QThread
from service.Prediction import Prediction
from tools.Console import Console
console = Console()

class AudioAnalyser(QThread):
    def __init__(self):
        self.audio_analyser = None
        self.thread = Prediction()
        
    ######################################################################################################################
    #   ______                       __                                       ______                   __  __            #
    #  /      \                     /  |                                     /      \                 /  |/  |           #
    # /$$$$$$  | _______    ______  $$ | __    __   _______   ______        /$$$$$$  | __    __   ____$$ |$$/   ______   #
    # $$ |__$$ |/       \  /      \ $$ |/  |  /  | /       | /      \       $$ |__$$ |/  |  /  | /    $$ |/  | /      \  #
    # $$    $$ |$$$$$$$  | $$$$$$  |$$ |$$ |  $$ |/$$$$$$$/ /$$$$$$  |      $$    $$ |$$ |  $$ |/$$$$$$$ |$$ |/$$$$$$  | #
    # $$$$$$$$ |$$ |  $$ | /    $$ |$$ |$$ |  $$ |$$      \ $$    $$ |      $$$$$$$$ |$$ |  $$ |$$ |  $$ |$$ |$$ |  $$ | #
    # $$ |  $$ |$$ |  $$ |/$$$$$$$ |$$ |$$ \__$$ | $$$$$$  |$$$$$$$$/       $$ |  $$ |$$ \__$$ |$$ \__$$ |$$ |$$ \__$$ | #
    # $$ |  $$ |$$ |  $$ |$$    $$ |$$ |$$    $$ |/     $$/ $$       |      $$ |  $$ |$$    $$/ $$    $$ |$$ |$$    $$/  #
    # $$/   $$/ $$/   $$/  $$$$$$$/ $$/  $$$$$$$ |$$$$$$$/   $$$$$$$/       $$/   $$/  $$$$$$/   $$$$$$$/ $$/  $$$$$$/   #
    #                                   /  \__$$ |                                                                       #
    #                                   $$    $$/                                                                        #
    #                                    $$$$$$/                                                                         #
    #                                                                                                                    #
    ######################################################################################################################

    # def loadCurrentFile(self, _ = None):
    #     self.progressLabelValue = 0
    #     console.debug("Load next file")
    #     self.progressLabel.setText('load...')
    #     self.playButton.setEnabled(False)
    #     self.refreshLabelButton()

    #     # sending_button = self.sender()
    #     # actual_genre = sending_button.text().split(':')[0]
    #     if(len(self.files) <= 0):
    #         console.info(f'no files found in {self.audio_dir}') 
    #         self.openButton.setEnabled(True)
    #         return False

    #     self.updateMedia()

    # def loadNextFile(self, _ = None):
    #     console.debug("Load next file")
    #     self.progressLabel.setText('load...')

    #     self.reloadButton.setEnabled(True)
    #     self.nextButton.setEnabled(True)
    #     self.playButton.setEnabled(False)
    #     self.refreshLabelButton()


    #     # sending_button = self.sender()
    #     # actual_genre = sending_button.text().split(':')[0]
    #     if(len(self.files) <= 0):
    #         console.info("No files found!")
    #         self.openButton.setEnabled(True)
    #         return False

    #     self.fileName = path_join(self.audio_dir, self.files[0])

    #     console.debug("Load coverart")
    #     loadCoverart(self.fileName)

    #     self.files.pop(0)

    #     self.startThread()
    #     self.updateMedia()
        
    # def updateMedia(self):
    #     self.trackLabel.setText(basename(self.fileName))
    #     self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(self.fileName)))
    #     self.playButton.setEnabled(True)
    #     self.toggleAudio()
    #     console.info("Loaded Next File")
    #     self.updateTrackCover()
        

    def startThread(self):
        self.stopThread()
        
        self.thread = Prediction(file=self.fileName, options=self)
        self.thread.result_value.connect(self.updateUi)
        self.thread.change_value.connect(self.updateProgressLabel)
        self.thread.start()
        console.debug("Started Thread")

      # def stopThread(self):
      #   if (type(self.thread) == Prediction) and self.thread.isRunning:
      #       self.thread.stop()
      #       self.thread.quit()
      #       console.debug("Stoped Thread")