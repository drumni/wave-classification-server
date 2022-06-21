from src.core.Options import Options

import librosa

import warnings
warnings.filterwarnings('ignore')

from numpy import (
    array,
    var,
    mean,
    float64
)

# from numpy.random import seed

class Features:
    def __init__(self, options: Options, name: str, label: str):
        self.name = name
        self.label = label
        self.options = options
        self.features = {}
        self.results = {}

    def add(self, name ,function, state=None):
        result = function() if type(function) == type(self.add) else function

        if state is None:
            state = len(array(result).shape)
        self.results[name] = result
        if state == 0:
            self.features[name] = result
        elif state == 1:
            self.features[f'{name}_var'] = var(result, dtype=float64)
            self.features[f'{name}_mean'] = mean(result, dtype=float64)
        elif state == 2:
            for i, value in enumerate(result):
                self.features[f'{name}{i+1}_var'] = var(value, dtype=float64)
                self.features[f'{name}{i+1}_mean'] = mean(value, dtype=float64)
        else:
            raise ValueError(f'Invalid state {state}')

    def load(self, audio_data, index: int):
        self.index = index
        self.audio_data = audio_data
        
        # call each feature function from self.options.features
        for feature in self.options.features:
            self.add(feature, getattr(self, feature), self.options.features[feature])

    def label(self):
      return self.label

    def filename(self):
      fn = self.name.split('.')
      fn = f'{fn[0]}.{self.index}.{fn[1]}'
      return fn

    tonnetz_ = None
    def tonnetz(self):
        if self.tonnetz_ is not None:
            return self.tonnetz_
        self.tonnetz_ = librosa.feature.tonnetz(y=self.harmonic())
        return self.tonnetz_

    harmonic_ = None
    def harmonic(self):
        if self.harmonic_ is not None:
            return self.harmonic_
        self.harmonic_ = librosa.effects.harmonic(y=self.harmony())
        return self.harmonic_

    mfcc_ = None
    def mfcc(self):
        if self.mfcc_ is not None:
            return self.mfcc_
        self.mfcc_ = librosa.feature.mfcc(y=self.audio_data, sr=self.options.sample_rate)
        return self.mfcc_

    mfcc_delta_ = None
    def mfcc_delta(self):
        if self.mfcc_delta_ is not None:
            return self.mfcc_delta_
        self.mfcc_delta_ = librosa.feature.delta(self.mfcc(), order = 1)
        return self.mfcc_delta_
    
    mfcc_delta_delta_ = None
    def mfcc_delta_delta(self):
        if self.mfcc_delta_delta_ is not None:
            return self.mfcc_delta_delta_
        self.mfcc_delta_delta_ = librosa.feature.delta(self.mfcc(), order = 2)
        return self.mfcc_delta_delta_

    mfcc_harmony_ = None
    def mfcc_harmony(self):
        if self.mfcc_harmony_ is not None:
            return self.mfcc_harmony_
        self.mfcc_harmony_ = librosa.feature.mfcc(y=self.harmony(), sr=self.options.sample_rate, n_mfcc=40)[-20:][::3]
        return self.mfcc_harmony_
    
    mfcc_perc_ = None
    def mfcc_perc(self):
        if self.mfcc_perc_ is not None:
            return self.mfcc_perc_
        self.mfcc_perc_ = librosa.feature.mfcc(y=self.perc(), sr=self.options.sample_rate, n_mfcc=40, lifter=2 * 40)[::3]
        return self.mfcc_perc_

    stft_ = None
    def stft(self):
        if self.stft_ is not None:
            return self.stft_
        self.stft_ = librosa.core.stft(self.audio_data)
        return self.stft_

    chroma_stft_ = None
    def chroma_stft(self):
        if self.chroma_stft_ is not None:
            return self.chroma_stft_
        self.chroma_stft_ = librosa.feature.chroma_stft(S=self.stft(), sr=self.options.sample_rate)
        return self.chroma_stft_

    spectral_centroid_ = None
    def spectral_centroid(self):
        if self.spectral_centroid_ is not None:
            return self.spectral_centroid_
        self.spectral_centroid_ = librosa.feature.spectral_centroid(self.audio_data)
        return self.spectral_centroid_

    spectral_bandwidth_ = None
    def spectral_bandwidth(self):
        if self.spectral_bandwidth_ is not None:
            return self.spectral_bandwidth_
        self.spectral_bandwidth_ = librosa.feature.spectral_bandwidth(self.audio_data)
        return self.spectral_bandwidth_

    spectral_rolloff_ = None
    def spectral_rolloff(self):
        if self.spectral_rolloff_ is not None:
            return self.spectral_rolloff_
        self.spectral_rolloff_ = librosa.feature.spectral_rolloff(self.audio_data)
        return self.spectral_rolloff_

    spectral_contrast_ = None
    def spectral_contrast(self):
        if self.spectral_contrast_ is not None:
            return self.spectral_contrast_
        self.spectral_contrast_ = librosa.feature.spectral_contrast(y = self.audio_data)
        return self.spectral_contrast_

    zero_crossing_rate_ = None
    def zero_crossing_rate(self):
        if self.zero_crossing_rate_ is not None:
            return self.zero_crossing_rate_
        self.zero_crossing_rate_ = librosa.feature.zero_crossing_rate(self.audio_data)
        return self.zero_crossing_rate_

    rms_ = None
    def rms(self):
        if self.rms_ is not None:
            return self.rms_
        self.rms_ = librosa.feature.rms(self.audio_data)
        return self.rms_

    harmony_ = None
    def harmony(self):
        if self.harmony_ is not None:
            return self.harmony_
        self.hpss()
        return self.harmony_

    perc_ = None
    def perc(self):
        if self.perc_ is not None:
            return self.perc_
        self.hpss()
        return self.perc_

    def hpss(self):
        self.harmony_, self.perc_ = librosa.effects.hpss(y = self.audio_data)

    tempo_ = None
    def tempo(self):
        if self.tempo_ is not None:
            return self.tempo_
        _tempo = librosa.beat.tempo(self.audio_data)[0]
        _tempo = round(_tempo % 180)
        self.tempo_ = _tempo
        return self.tempo_

    length_ = None
    def length(self):
        if self.length_ is not None:
            return self.length_
        self.length_ = len(self.audio_data)
        return self.length_ 
      
    def getFeatures(self):
      if self.features is not None:
        return self.features