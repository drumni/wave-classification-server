from numpy import float64
import pandas as pd
import os
import re

def normalizeName(filename: str) -> str:
    filewords = re.findall(
        r'\w+', os.path.basename(filename).replace('_', ''))
    return ''.join([x.capitalize() for x in filewords])

class Database:
    def __init__(self, path: str, label = ''):
        if not os.path.exists(path):
            os.makedirs(path)
        self.path = os.path.join(path, 'db.csv')
        self.label = label
        self.load()
    
    def updateLabel(self, label):
        self.label = label
        if not self.exsist:
            self.load()
            
    def load(self):
        if os.path.exists(self.path):
            self.exsist = True
            self.df = pd.read_csv(self.path, index_col=[0])
        else:
            self.exsist = False
            self.df = pd.DataFrame()
    
    def push(self, obj, filename):
        filename = normalizeName(filename)
        for index, dict in enumerate(obj):
            dict['filename'] = f'{filename}.{index}'
            dict['label'] = self.label
        _df = pd.DataFrame(obj, dtype=float64)
        
        _df = _df[ ['filename'] + [ col for col in _df.columns if col != 'filename' ] ]
        self.df = self.df.append(_df, ignore_index=True)
        self.exsist = True      
              
    def alreadyExsist(self, filename):
        if(self.exsist == False):
            return False
        return len(self.df.loc[self.df['filename'] == normalizeName(filename)+'.0']) > 0
    
    def count(self, key: str, value: str) -> int:
        if(key not in self.df.columns):
            return 0
        return len(self.df.loc[self.df[key].str.contains(value)])
        
    def save(self):
        self.df.to_csv(self.path)
        