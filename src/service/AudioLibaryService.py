from PySide2.QtCore import QThread
from src.core.Options import Options

# import audio.Library
from src.core.audio.Library import Library

# A Service for the Audio Library Window that handles the creation of the audio database. 
class AudioLibaryService(QThread):
    def __init__(self):
        super().__init__()
        
        self.options = Options(onSegmentAnalysed=self.onSegmentAnalysed, headersTemplateFile='./data/template.csv')

        # create a new audio library and load the folder 'C:\\Users\\robin\\Music\\PioneerDJ\\Demo Tracks' with the label 'Demo Tracks'
        self.library = Library('./data/library.csv', options = self.options)
        # self.library.loadFolder('./data/Demo Tracks', 'Demo Tracks')
        self.library.addFolder('C:\\Users\\robin\\Music\\PioneerDJ\\Demo Tracks', 'Demo')
        
    def run(self):
        print('run')
        
    def onSegmentAnalysed(self, path, label, index):
        print(f'{path} {label} {index}')