import librosa
from src.segment import AudioSegment
# from DONT.Config import Config

import warnings
warnings.filterwarnings('ignore')


class Analysis:
    def __init__(self,
                 audio_path,
                 options,
                 _bar = None):
        
        self.audio_path = audio_path
        self.bar = _bar
        
        self.segments = []
        
        self.tracks = options.tracks
        self.segment_count = options.segments
        self.segment_duration = options.seconds
        self.rate = options.rate
        self.failed = False

    def calculate(self):
        sr = librosa.get_samplerate(path=self.audio_path)
        self.length = librosa.get_duration(filename=self.audio_path, sr=sr) / 60 # self.duration = len(self.audio_data) / SAMPLE_RATE / 60
        self.offset_per_segment = self.segment_duration / self.segment_count # self.frames = SAMPLE_RATE * self.duration # self.samples_per_second = self.frames / segment_count

        self.addFeatures()

        return [segment.features for segment in self.segments]

    def addFeatures(self):
        for i in range(self.segment_count):
            offset = self.offset_per_segment

            segment = AudioSegment()
            segment.load(self.audio_path,  offset * i, self.segment_duration, target_sr=self.rate)
                        
            segment.addFeatures()
            
            self.segments.append(segment)
            if(self.bar):
                self.bar.update(1)

