class Options:
  def __init__(self, onSegmentAnalysed = None, headersTemplateFile = None):
    
    # a callback function for each segment analysis step
    self.onSegmentAnalysed = onSegmentAnalysed
    self.headersTemplateFile = headersTemplateFile
    self.segments = 2
    self.segment_duration = 3
    self.sample_rate = 22050
    
    self.storage_location = None
    self.data_dir = None
    self.model_dir = None
    self.autoTolarance = False
    self.autoMove = False
    self.autoNext = False
    self.features = {
      'filename': 0, 
      'length': 0, 
      'tempo': 0, 
      'mfcc_perc': 2, 
      'mfcc_harmony': 2, 
      'chroma_stft': 2, 
      'mfcc_delta': 1, 
      'mfcc_delta_delta': 1, 
      'rms': 1, 
      'tonnetz': 1, 
      'spectral_contrast': 1, 
      'zero_crossing_rate': 1, 
      'label': 0
    }