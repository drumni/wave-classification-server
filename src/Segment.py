import librosa
import numpy as np

class AudioSegment: 
    def __init__(self):
        self.features = {}
        
    def load(self, path, offset, length, target_sr):
        audio_data, sr = librosa.load(path, offset=offset, duration=length, sr=target_sr)
        audio_data, _ = librosa.effects.trim(audio_data)
        self.audio_data = audio_data

    def calculate(self, name, function):
        result, state = function()
        # state = len(np.array(result).shape)

        if state == 0:
            self.features[name] = result
        elif state == 1:
            self.features[f'{name}_var'] = np.var(result)
            self.features[f'{name}_mean'] = np.mean(result)
        elif state == 2:
            for i, value in enumerate(result):
                self.features[f'{name}{i+1}_var'] = np.var(value)
                self.features[f'{name}{i+1}_mean'] = np.mean(value)
    
    def mfcc(self):
        return librosa.feature.mfcc(self.audio_data), 2
    
    def melspectrogram(self):
        melspectrogram = librosa.feature.melspectrogram(self.audio_data)
        return librosa.amplitude_to_db(melspectrogram, ref=np.max), 1
    
    def chroma_stft(self):
        return np.mean(librosa.feature.chroma_stft(self.audio_data), axis=1), 1
    
    def spectral_centroid(self):
        return librosa.feature.spectral_centroid(self.audio_data), 1
    
    def spectral_bandwidth(self):
        return librosa.feature.spectral_bandwidth(self.audio_data), 1
    
    def rolloff(self):
        return librosa.feature.spectral_rolloff(self.audio_data), 1
    
    def zero_crossing_rate(self):
        return librosa.feature.zero_crossing_rate(self.audio_data), 1
    
    def rms(self):
        return librosa.feature.rms(self.audio_data), 1
    
    def harmony(self):
        harmony, _ = librosa.effects.hpss(self.audio_data)
        return harmony, 1
    
    def perceptr(self):
        _, perceptr = librosa.effects.hpss(self.audio_data)
        return perceptr, 1
    
    def tempo(self):
        _tempo = librosa.beat.tempo(self.audio_data)[0]
        if(_tempo > 170):
            _tempo /= 2
        return _tempo, 0
    
    def length(self):
        return len(self.audio_data), 0

