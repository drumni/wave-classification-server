from pandas import DataFrame
from pandas import read_csv
from tqdm.std import tqdm
import os

class Base:
    data_dir = 'data'
    
    tracks = 2
    segments = 3
    seconds = 30
    rate = 22050
    
    SAVE_ENABLED = True
    
    def __init__(self):
        self.df = DataFrame(columns=['filename'])
        self.library = {}
        self.database = {}
        # pass
    
    def normalizeDataFrame(self):  # sourcery skip: avoid-builtin-shadow
        min = self.df.label.value_counts().min()
        self.df = self.df.groupby('label').head(min).reset_index()
        self.SAVE_ENABLED = False
    
    def saveDataFrame(self):
        col = self.df.pop("filename")
        self.df.insert(0, col.name, col)
        if(self.SAVE_ENABLED == False):
            self.df.to_csv(os.path.join(self.data_dir, 'db.min.csv'))
        else:
            self.df.to_csv(os.path.join(self.data_dir, 'db.csv'))
    
    def loadDataFrame(self):
        expectedColumns = self.database[list(self.database.keys())[0]][0][0].keys()
        self.df = DataFrame(columns=expectedColumns)
        self.loadDataFrameFile()
        self.updateDataFrame()
        self.saveDataFrame()
        
    def loadDataFrameFile(self):
        if os.path.exists(os.path.join(self.data_dir, 'db.csv')):
            self.df = read_csv(os.path.join(self.data_dir, 'db.csv'), index_col=[0])      
    
    def updateDataFrame(self):
        for label in list(self.database.keys()):
            for file in self.database[label]:
                for segment in file:
                    if(len(self.df.loc[self.df['filename'] == segment['filename']]) == 0):
                        segment.update({
                            "label": label
                        })
                        self.df = self.df.append(segment, ignore_index=True)
    
    def getCountInsideDataFrame(self, col: str, value: str):
        try:
            return len(self.df.loc[self.df[col] == value])
        except Exception:
            return 0
    
    def validateFile(self, file_path, filename):
        acceppted_audio_formats = ['wav', 'mp3'] 
        if (os.path.splitext(file_path)[-1] in acceppted_audio_formats):
            return False
        
        if(self.getCountInsideDataFrame('filename', self.getFilename(filename, 0)) > 0):
            return False
        
        return True
    
    def validateFolder(self, label):
        files = len(self.library[label])
        if(files == 0):
            print(f' -> {label}: library empty.')
            return False
        
        if(len(self.library[label]) < self.tracks):
            print(f' -> {label}: library missing {self.tracks - len(self.library[label])} files.')
            # return False

        if(self.getCountInsideDataFrame("label", label) / self.segments >= self.tracks):
            print(f' -> {label}: dataframe satisfied with {self.getCountInsideDataFrame("label", label)} rows.')
            return False
    
        return True
    
    def loadProgressBar(self, label, init = 0) -> tqdm:
        return tqdm(total=self.segments * len(self.library[label]), desc=label, bar_format="{desc}\t{bar:20} {n_fmt}/{total_fmt} [{elapsed} -> {remaining}]", initial=init)

    def getFilename(self, filename, i = ''):
        words = os.path.splitext(filename)
        return ''.join([words[0], str(i), words[-1]])  
