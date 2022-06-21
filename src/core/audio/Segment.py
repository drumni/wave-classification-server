from src.core.audio.Features import Features
from src.core.Options import Options
from librosa import load, resample
from os.path import basename

class Segment:
    def __init__(self, options: Options, path: str, label: str):
        self.path = path
        self.options = options
        self.label = label
        
        self.freatures = Features(self.options, basename(self.path), self.label)
        
    def load(self, index: int):
        offset_per_segment = self.options.segment_duration / self.options.segments

        # TODO add random offset by seed
        audio_data, rate = load(self.path, offset=offset_per_segment * index, duration=self.options.segment_duration, sr=self.options.sample_rate)
        # self.audio_data, _ = librosa.effects.trim(self.audio_data) 
        # # TODO check effects!
        
        if rate != self.options.sample_rate:
          audio_data = resample(self.audio_data, rate, self.options.sample_rate)
          
        self.freatures.load(audio_data, index)
        self.options.onSegmentAnalysed(self.path, self.label, index)
        
    def getFeatures(self):
        return self.freatures.getFeatures()