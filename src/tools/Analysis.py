from librosa import (
    get_samplerate,
    get_duration
)
from src.tools.Segment import Segment
from src.core.Base import Base

from warnings import filterwarnings
filterwarnings('ignore')

class Analysis:
    def __init__(self,
                 audio_path,
                 options: Base,
                 _bar = None,
                 _ui_bar = None):
        
        self.audio_path = audio_path
        
        self.bar = _bar
        self.ui_bar = _ui_bar
        
        self.segments = []
        
        self.segment_count = options.segments
        self.segment_duration = options.seconds
        self.rate = 22050

    def loadFeatures(self):
        sr = get_samplerate(path=self.audio_path)
        self.length = get_duration(filename=self.audio_path, sr=sr) / 60 # self.duration = len(self.audio_data) / SAMPLE_RATE / 60
        self.offset_per_segment = self.segment_duration / self.segment_count # self.frames = SAMPLE_RATE * self.duration # self.samples_per_second = self.frames / segment_count

        if(self.length * 60 < self.segment_duration * self.segment_count):
            return False
        
        for i in range(self.segment_count):
            segment = Segment()
            segment.loadAudio(self.audio_path, self.offset_per_segment * i, self.segment_duration, target_sr=self.rate)
            segment.loadFeatures()
            self.segments.append(segment)
            
            if(self.bar):
                self.bar.update(1)
                
            if(self.ui_bar):
                self.ui_bar.emit(1)
        
        return [segment.features for segment in self.segments]

