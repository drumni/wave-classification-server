from src.tools.Console import Console
console = Console()
console.setOwner(__file__)

from PySide2.QtWidgets import QHBoxLayout, QLabel, QWidget

class LibraryTableItemWidget(QWidget): # LibraryTableItemWidget
  def __init__(self, item=None, selection=None):
    super().__init__()
    self.selection = selection
    
    self.headers = []
    self.values = {}
    self.labels = []
    
    for key in item.keys():
      self.headers.append(key)
      self.values[key] = self.convToString(item[key])
      
    self.updateLayout()
    
  def updateLayout(self):
    self.labels = []
    
    layout = QHBoxLayout(self)
    for key in self.values.keys():
      item =  QLabel(self.values[key])
      self.labels.append(item)
      console.debug(f'{key}: {self.values[key]}')
      layout.addWidget(QWidget(item))
    return layout
  
  def getHeaderWidget(self):
    headerWidget = QWidget()
    layout = QHBoxLayout(headerWidget)
    for header in self.headers:
      item = QLabel(header)
      self.labels.append(item)
      layout.addWidget(QWidget(item))
    return headerWidget
  
  def convToString(self, item):
    return str(item)
    