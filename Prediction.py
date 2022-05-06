from Classification import Classification

from keras.models import load_model
import joblib
import pickle
from tqdm.std import tqdm

import pandas as pd
import os
import numpy as np

class Prediction(Classification):
    def load(self):
        self.model = load_model(os.path.join(self.data_dir, "model.h5"))
        self.scaler = joblib.load(os.path.join(self.data_dir, "scaler.pkl"))  # load from disk
        with open(os.path.join(self.data_dir, "labels.pkl"), "rb") as a_file:
            self.labels = pickle.load(a_file)
    
    def predictFolder(self, directory):
        self.load()
        self.predict_dir = directory
        files = os.listdir(self.predict_dir)

        for file in files:
            if(os.path.splitext(file)[-1] not in ['.wav', '.mp3']):
                print('not supported')
                continue
            g = self.loadLabel(file)
            a, a_val, b, b_val = self.loadGuess(g)
            if a == 'other':
                print(' > no genre found')
            if b != 'other':    
                print(f' > ({a}: {round(np.max(a_val)*100, 2)}% or {b}: {round(np.max(b_val)*100, 2)}%)')
            else:
                print(f' > ({a}: {round(np.max(a_val)*100, 2)}%)')
    
    
    def loadProgressBar(self, label):
        return tqdm(total=self.segments, desc=label, bar_format="{desc}\t{bar:20} {n_fmt}/{total_fmt} [{elapsed} -> {remaining}]")
    
            
    def loadGuess(self, q):
        a = 'other'
        a_val = 0
        b = 'other'
        b_val = 0
        
        temp = 0
        for i, r in enumerate(q):
            _max = np.max(r)
            temp += _max
            g = np.mean(r) * (1 - (np.var(r)))
            
            if((_max < 0.80)):
                continue
            if(g > a_val):
                b = a
                b_val = a_val
                a_val = g
                a = self.labels[i]
            elif(g > b_val):
                b = self.labels[i]
                b_val = g
        
        return a, a_val, b, b_val

    def loadLabel(self, file):
        result = self.loadFile(file, None)
        inside_df = pd.DataFrame(result, dtype=np.float64)
        # inside_df.drop(['length'], axis=1, inplace=True)
        inside_df = pd.DataFrame(self.scaler.transform(inside_df), columns=inside_df.columns)
        inside_df.reset_index(drop=True)
        return self.model.predict(inside_df)
