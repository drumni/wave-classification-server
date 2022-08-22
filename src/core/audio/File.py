import logging
from src.core.audio.Segment import Segment

from src.core.Options import Options
logger = logging.getLogger(__file__)

from librosa import get_duration

class File:
  def __init__(self, path: str, label: str, options: Options):
    self.path = path
    self.label = label
    self.options = options
    self.length = get_duration(filename=self.path, sr=self.options.sample_rate) / 60
    self.segments = []
    
    self.loadSegments()
    
  def loadSegments(self):
    # create self.options.segments segments of the audio file with loop in brackets
    self.segments = [Segment(self.options, self.path, self.label) for _ in range(self.options.segments)]
    
    for index in range(len(self.segments)):
      self.segments[index].load(index)
  
  def onAnalysed(self, path, label, index):
    pass