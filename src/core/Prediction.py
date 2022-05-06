from src.core.Base import Base
from src.tools.Analysis import Analysis

from keras.models import load_model
import joblib
import pickle

import pandas as pd
import os
import numpy as np



class Prediction(Base):
    def load(self):
        self.model = load_model(os.path.join(self.data_dir, "model.h5"))
        self.scaler = joblib.load(os.path.join(self.data_dir, "scaler.pkl"))  # load from disk
        with open(os.path.join(self.data_dir, "labels.pkl"), "rb") as a_file:
            self.labels = pickle.load(a_file)

    def loadLabel(self, file):
        result = self.loadFile(file, None)
        inside_df = pd.DataFrame(result, dtype=np.float64)
        inside_df = pd.DataFrame(self.scaler.transform(inside_df), columns=inside_df.columns)
        inside_df.reset_index(drop=True)
        return self.model.predict(inside_df)
    
    def loadFile(self, file_path, progress_bar):
        alyis = Analysis(audio_path=file_path, options=self, _bar = progress_bar)
        if(alyis.failed == True):
            return False
        return alyis.loadFeatures()
