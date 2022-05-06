import os
import json
import json
import json
            


class Config:
    def __init__(self, filename = '', options = None):
        if len(filename) == 0:
            if options is None:
                raise ValueError("You need to add one of these arguments: 'filename' or 'options'.")
                
            self.excluded_labels = [] if (options.excluded_labels is not None) else options.excluded_labels
            self.tracks = 100
            self.segments = 10 
            self.seconds = 3 
            self.rate = 22050
            self.data_dir = 'data'
            
            if (options.list is not None):
                self.lib_dir = options.lib_dir
            else:
                raise ValueError("You need to define your Audio Libary 'lib_dir' in your configuration.")
            
            self.labels = [e for e in os.listdir(self.lib_dir) if e not in self.excluded_labels]
            self.sub_dir = os.path.join(self.data_dir, f'{self.tracks}x{self.segments}x{self.seconds}-{len(self.labels)}')
            self.seed = options.seed
        else:
            with open(filename, 'r') as f:
                options = json.load(f)
            return Config(options = options)
        

    def save(self):
        import json
        with open(os.path.join(self.data_dir, 'config.json'), 'w', encoding='utf-8') as f:
            json.dump(self.__dict__, f, ensure_ascii=False, indent=4)

