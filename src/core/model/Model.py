# import uuid4
from uuid import uuid4

class Model:
    def __init__(self, name, model_path):
        self.model_path = model_path
        # define unique id for the model
        self.id = str(uuid4())