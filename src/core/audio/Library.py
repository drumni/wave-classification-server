from ctypes import ArgumentError
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
        self.addLabel(file.label)
        if file is not None:
            self.files.append(file)
        
    def addLabel(self, label):
        if {'label': label} not in self.labels:
          self.labels.append({'label': label})
        
    def addFolder(self, path, label):
        if {'label': label} not in self.labels:
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
        
    def getData(self, selection):
        data = []

        if selection == 'Files':
            data.extend(iter(self.files))
        elif selection == 'Folders':
            data.extend(iter(self.folders))
        elif selection == 'Labels':
            data.extend(iter(self.labels))
        elif selection == 'Segments':
            for file in self.files:
                data.extend(iter(file.segments))
        else:
            data = None
            raise ArgumentError(f'selection {selection} not found')

        for i in range(len(data)):
            if isinstance(data[i], object) and type(data[i]) is not dict:
                data[i] = data[i].__dict__
                
        return data