import librosa
import numpy as np

np.random.seed(42)


class AudioSegment:
    def __init__(self):
        self.features = {}
        self.results = {}

    def load(self, path, offset, length, target_sr):
        # TODO add  random offset by seed
        self.audio_data, self.rate = librosa.load(
            path, offset=offset, duration=length, sr=target_sr)
        # self.audio_data, _ = librosa.effects.trim(self.audio_data) # TODO check effects!

    def calculate(self, name ,function, state=None):
        result = function() if type(function) == type(self.calculate) else function
        
        if state != None:
            state = len(np.array(result).shape)

        self.results[name] = result

        if state == -1:
            valueValue = np.mean(result)
            self.features[f'{name}_var'] = np.var(value)
            self.features[f'{name}_mean'] = np.mean(value)
        elif state == 0:
            self.features[name] = result
        elif state == 1:
            self.features[f'{name}_var'] = np.var(result)
            self.features[f'{name}_mean'] = np.mean(result)
        elif state == 2:
            for i, value in enumerate(result):
                self.features[f'{name}{i+1}_var'] = np.var(value)
                self.features[f'{name}{i+1}_mean'] = np.mean(value)
        elif state == 3:
            for i, value in enumerate(result):
                valueValue = np.mean(value)
                self.features[f'{name}{i+1}_var'] = np.var(valueValue)
                self.features[f'{name}{i+1}_mean'] = np.mean(valueValue)

    def addFeatures(self):
        # self.calculate('harmonic', self.harmonic) just harmonic audio sample
        # self.calculate('chroma_custom', self.chroma_custom, 2)
        # self.calculate('melspectrogram', self.melspectrogram) not good
        self.calculate('rms', self.rms, 1) # TODO more prozessing
        self.calculate('length', self.length, 0)
        
        self.calculate('tonnetz', self.tonnetz, 1)
        self.calculate('mfcc', self.mfcc, 2)
        self.calculate('chroma', self.chroma, 2)
        self.calculate('chroma_stft', self.chroma_stft, 2) 
        self.calculate('spectral_centroid', self.spectral_centroid, 1)
        self.calculate('spectral_contrast', self.spectral_contrast, -1)
        self.calculate('spectral_bandwidth', self.spectral_bandwidth, 1)
        self.calculate('spectral_rolloff', self.spectral_rolloff, 1)
        self.calculate('zero_crossing_rate', self.zero_crossing_rate, 1)
        # self.calculate('zero_crossing_rate_perc', self.zero_crossing_rate_perc, 1)
        self.calculate('harmony', self.harmony, 1)
        self.calculate('tempo', self.tempo, 0)
        # self.calculate('chroma_harmony', self.chroma_harmony, 2)

    tonnetz_ = None
    def tonnetz(self):
        if self.tonnetz_ is not None:
            return self.tonnetz_
        self.tonnetz_ = librosa.feature.tonnetz(y=self.harmonic(), sr=self.rate, chroma=self.chroma_custom())
        return self.tonnetz_

    harmonic_ = None
    def harmonic(self):
        if self.harmonic_ is not None:
            return self.harmonic_
        self.harmonic_ = librosa.effects.harmonic(y=self.audio_data)
        return self.harmonic_

    mfcc_ = None
    def mfcc(self):
        if self.mfcc_ is not None:
            return self.mfcc_
        self.mfcc_ = librosa.feature.mfcc(y=self.audio_data, sr=self.rate)
        return self.mfcc_

    melspectrogram_ = None
    def melspectrogram(self):
        if self.melspectrogram_ is not None:
            return self.melspectrogram_
        self.melspectrogram_ = librosa.feature.melspectrogram(self.audio_data)
        self.melspectrogram_ = librosa.amplitude_to_db(self.melspectrogram_, ref=np.max)
        return self.melspectrogram_

    stft_ = None
    def stft(self):
        if self.stft_ is not None:
            return self.stft_
        self.stft_ = librosa.stft(self.audio_data)
        return self.stft_

    chroma_stft_ = None
    def chroma_stft(self):
        if self.chroma_stft_ is not None:
            return self.chroma_stft_
        self.chroma_stft_ = librosa.feature.chroma_stft(S=self.stft(), sr=self.rate)
        return self.chroma_stft_
    
    chroma_ = None
    def chroma(self):
        if self.chroma_ is not None:
            return self.chroma_
        self.chroma_ = librosa.feature.chroma_stft(self.audio_data, sr=self.rate)
        return self.chroma_

    chroma_harmony_ = None
    def chroma_harmony(self):
        if self.chroma_harmony_ is not None:
            return self.chroma_harmony_
        self.chroma_harmony_ = librosa.feature.chroma_stft(self.harmony(), sr=self.rate)
        return self.chroma_harmony_

    chroma_custom_ = None
    def chroma_custom(self):
        if self.chroma_custom_ is not None:
            return self.chroma_custom_
        self.chroma_custom_ = self.chroma_stft()
        return self.chroma_custom_

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

    def zero_crossing_rate_perc(self):
        self.zero_crossing_rate_perc_ = librosa.feature.zero_crossing_rate(self.perceptr())
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

    perceptr_ = None
    def perceptr(self):
        if self.perceptr_ is not None:
            return self.perceptr_
        self.hpss()
        return self.perceptr_

    def hpss(self):
        self.harmony_, self.perceptr_ = librosa.effects.hpss(y = self.audio_data)

    tempo_ = None
    def tempo(self):
        if self.tempo_ is not None:
            return self.tempo_
        _tempo = librosa.beat.tempo(self.perceptr())[0]
        if(_tempo > 170):
            _tempo /= 2
        self.tempo_ = _tempo
        return self.tempo_

    length_ = None
    def length(self):
        if self.length_ is not None:
            return self.length_
        self.length_ = len(self.audio_data)
        return self.length_ 
