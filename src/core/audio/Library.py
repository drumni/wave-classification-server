from os.path import join
from os import listdir

from pandas import read_csv, DataFrame
from src.core.Options import Options

from src.core.audio.File import File

# A Collection Of Folders that contain audio files. The folders are searched for audio files and the files are added to a list. 
# Each folder is assigned a label. The list of folders and labels is saved in a csv file.
class Library:
    def __init__(self, path: str, options: Options):
      # options for the audio library
      self.options = options
      
      # the location of the audio library file
      self.path = path
      
      # a list of all the folders paths in the library with their labels
      self.folders = []
      
      # a list of all the file paths in the library with their labels
      self.files = []
      
      # a list of all the labels in the library
      self.labels = []
      
      # a dataframe of the library
      self.dataframe = None
      
    def addFile(self, file: File):
        if file.label not in self.labels:
            self.labels.append(file.label)
        if file is not None:
            self.files.append(file)
        
    def addLabel(self, label):
        if label not in self.labels:
          self.labels.append(label)
        
    def addFolder(self, path, label):
        self.folders.append({'path': path, 'label': label})
        
        # add labels to the list of labels
        self.addLabel(label)
        
        # read all files in folder and add them to the list of files
        for file in listdir(path):
          file = File(join(path, file), label, self.options)
          self.addFile(file)
          
    def addLibrary(self, library):
        for folder in library['folders']:
            self.addFolder(folder['path'], folder['label'])
            
    def createDataFrame(self):
        # load headers from headersTemplateFile
          
        # create a dataframe with the files and labels
        self.dataframe = DataFrame(self.getSegments())
        
        if self.options.headersTemplateFile is not None:
          headers = read_csv(self.options.headersTemplateFile).columns
          self.dataframe = self.dataframe[headers]

    def loadLibrary(self):
        # read the library file
        library = read_csv(self.path)
        
        # add the library to the list of folders and files
        self.addLibrary(library)
        
        # create a dataframe of the library
        self.createDataFrame()
        
    def saveLibrary(self):
        # create a dataframe of the library
        self.createDataFrame()
        
        # save the library file
        self.dataframe.to_csv(self.path, index=False)
        
    def getSegments(self):
        segments = []
        for file in self.files:
            segments.extend(segment.getFeatures() for segment in file.segments)
        return segments
        
    def getFile(self, path):
        return next((file for file in self.files if file.path == path), None)
      
    def getFileByLabel(self, label):
        return next((file for file in self.files if file.label == label), None)
      
    def getFolder(self, path):
        return next((folder for folder in self.folders if folder['path'] == path), None)
      
    def getFolderByLabel(self, label):
        return next((folder for folder in self.folders if folder['label'] == label), None)
      
    def getLabel(self, label):
        return next((label for label in self.labels if label == label), None)