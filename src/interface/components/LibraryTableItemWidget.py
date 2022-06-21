from PySide2.QtWidgets import QHBoxLayout, QLabel, QWidget

class LibraryTableItemWidget(QWidget): # LibraryTableItemWidget
  def __init__(self, item=None, selection=None):
    super().__init__()
    self.selection = selection
    
    self.__item = item
    self.headers = []
    self.values = []
    
    if self.selection == 'Labels':
        self.label = self.__item
        self.headers = ['label']
    else:
      if self.selection == 'Files':
        self.__item = self.__item.__dict__

      # get all keys in item
      for key in self.__item.keys():
        self.headers.append(key)
        self.values.append(self.__item[key])
        self.__item[key] = QLabel(str(self.__item[key]))
      
    self.updateLayout()
    print(self.headers)
    
  def updateLayout(self):
    layout = QHBoxLayout(self)
    for i, value in enumerate(self.values):
      print(value)
      layout.addWidget(QLabel(self.values[i]))
    return layout
  
  def getHeaderWidget(self):
    headerWidget = QWidget()
    layout = QHBoxLayout(headerWidget)
    for header in self.headers:
      layout.addWidget(QLabel(header))
    return headerWidget