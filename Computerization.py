from Base import Base

import pickle
import joblib

import os
# import IPython
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('whitegrid')
# %matplotlib inline

import tensorflow as tf
print("TF version:-", tf.__version__)
import keras as k


import warnings
warnings.filterwarnings('ignore')
import sklearn.model_selection as skms
import sklearn.preprocessing as skp

seed = 42
tf.random.set_seed(seed)
np.random.seed(seed) 

class Computerization(Base):
    def preperation(self):
        self.df.drop(['length'], axis=1, inplace=True)
        self.encodeGenreLabel()
        self.df.label = [self.label_index[l] for l in self.df.label]
        self.splitSets()
        
    def splitSets(self):
        self.df = self.df.sample(frac=1, random_state=seed).reset_index(drop=True) 
    
                # remove irrelevant columns
        self.df.drop(['filename'], axis=1, inplace=True)
        df_y = self.df.pop('label')
        df_X = self.df
        
        # split into train dev and test
        self.X_train, self.X_dev, self.y_train, self.y_dev = skms.train_test_split(df_X, df_y, train_size=0.8, random_state=seed, stratify=df_y)

        self.scaler = skp.StandardScaler()
        self.X_train = pd.DataFrame(self.scaler.fit_transform(self.X_train), columns=self.X_train.columns)
        self.X_dev = pd.DataFrame(self.scaler.transform(self.X_dev), columns=self.X_dev.columns)

    def trainModel(self, model, epochs, optimizer):
        # [32, 64] - CPU
        # [128, 256] - GPU for more boost
        batch_size = 32
        
        # Stop training when a monitored metric has stopped improving.
        callback = tf.keras.callbacks.EarlyStopping(monitor='loss', patience=3)
        
        model.compile(optimizer=optimizer,
                    loss='sparse_categorical_crossentropy',
                    metrics='accuracy'
        )
        return model.fit(self.X_train, self.y_train, validation_data=(self.X_dev, self.y_dev), epochs=epochs, 
                        batch_size=batch_size, callbacks=[callback])


        

    def buildModel(self):
        self.model = k.models.Sequential([
            k.layers.Dense(512, activation='relu', input_shape=(self.X_train.shape[1],)),
            k.layers.Dropout(0.2),
            
            k.layers.Dense(256, activation='relu'),
            k.layers.Dropout(0.2),

            k.layers.Dense(128, activation='relu'),
            k.layers.Dropout(0.2),

            k.layers.Dense(64, activation='relu'),
            k.layers.Dropout(0.2),

            k.layers.Dense(len(self.label_index.keys()), activation='softmax'),
        ])
        print(self.model.summary())
        self.history = self.trainModel(model=self.model, epochs=100, optimizer='adam')

    def generateHistory(self):
        print("Max. Validation Accuracy",max(self.history.history["val_accuracy"]))
        pd.DataFrame(self.history.history).plot(figsize=(12,6))
        plt.show()
        plt.savefig(os.path.join(self.data_dir, "History.png"))
          
    def encodeGenreLabel(self):
        self.label_index = {}
        self.index_label = {}
        for i, x in enumerate(self.df.label.unique()):
            self.label_index[x] = i
            self.index_label[i] = x
        
    def save(self):
        self.model.save( os.path.join(self.data_dir, "model.h5"))

        joblib.dump(self.scaler , os.path.join(self.data_dir, "scaler.pkl"))     # save to disk

        with open(os.path.join(self.data_dir, "labels.pkl"), "wb") as a_file:
            pickle.dump(self.index_label, a_file)
            
