import os
import json
from typing import List

from tqdm import tqdm

from src.utility import loadDir
from src.analysis import Analysis
from src.database import Database

# [Human Error Code 42]: Code should be readable without comments
            
class LibraryAnalysier:
    acceppted_audio_formats = ['wav', 'mp3'] 
    data_dir = 'data'
    
    tracks = 2 # more track better model performance
    segments = 10 # more segments better model performance
                # too many segments (segments * seconds < track_duration)
    seconds = 3 # just use 3 or either 30 seconds
    rate = 22050 # dont change this
    seed = 42 # DONT change this
    
    sub_dir = os.path.join(data_dir, f'{tracks}x{segments}x{seconds}')

    def save(self):
        with open(os.path.join(self.sub_dir, 'config.json'), 'w', encoding='utf-8') as f:
            json.dump(self.__dict__, f, ensure_ascii=False, indent=4)
    
    def __init__(self, library='', include = None, exclude = None):
        self.include = [] if include is None else include
        self.exclude = [] if exclude is None else exclude
        self.labels = [e for e in os.listdir(library) if e not in self.exclude and e in self.include]
        print(f"Initialized library: {', '.join(self.labels)}")
        self.loadStructureFromLibrary(library)
        
    # TODO load exsisting Data
    def loadStructureFromFile(self, path):
        print('Import is not included yet!')
        # with open(path, 'r') as f:
        #     _options = dict(json.load(f))
        # self.__init__(options = _options)
        return
        
    def loadStructureFromLibrary(self, path):
        self.library = path
        self.database = Database(self.sub_dir)
        
        for index_dir, dir in enumerate(self.labels):
            if(self.loadFolder(dir, index_dir)):
                return True
            else:
                continue
        
    def loadFolder(self, dir, i):
        files, genre = loadDir(os.path.join(self.library, dir))
        self.database.updateLabel(genre)
        if(len(files) == 0):
            print(f' -> {i + 1}.\t{genre}: empty.')
            return False
        
        if(len(files) < self.tracks):
            print( f' -> {i + 1}.\t{genre}: missing {self.tracks - len(files)}')
            return False

        if(self.database.count('label', genre) / self.segments >= self.tracks):
            print(f' -> {i + 1}.\t{genre}: satisfied with {self.database.count("label", genre)} rows.')
            return False

        __bar = tqdm(total=(self.tracks) * self.segments, 
                    desc=f' -> {i + 1}.\t{genre}:',
                    bar_format="{desc}\t{bar:20} {n_fmt}/{total_fmt} [{elapsed} -> {remaining}]",
                    initial=self.database.count('label', genre))

        for file_path in files:
            if(self.database.count('label', genre) / self.segments >= self.tracks):
                break
            
            if(self.loadFile(file_path, __bar)):
                return True
            else:
                continue
        
        __bar.close()
    
    def loadFile(self, file_path, __bar):
        if (os.path.splitext(file_path)[-1] in self.acceppted_audio_formats):
            return False

        if(self.database.alreadyExsist(file_path)):
            return False

        alyis = Analysis(audio_path=file_path, options=self, _bar = __bar)
        if(alyis.failed):
            return False
        
        self.database.push(alyis.calculate(), file_path)
        self.database.save()
        return True