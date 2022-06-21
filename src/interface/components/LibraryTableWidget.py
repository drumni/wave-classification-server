from ctypes import ArgumentError
from posixpath import basename
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QLabel, QListWidget, QPushButton, QLineEdit, QScrollArea, QSizePolicy, QVBoxLayout, QWidget, QHBoxLayout
from numpy.lib.function_base import append
from src.interface.components.LibraryTableItemWidget import LibraryTableItemWidget

class LibraryTableWidget(QWidget):
    def __init__(self, library=None):
        super().__init__()
        self.selections = ['Files', 'Folders', 'Labels']
        self.selection = 'Folders'
        self.data = []
        self.library = library
        
        self.libaryTable = QWidget(objectName = "primaryContainer")
        self.libaryTableScroll = QScrollArea(self.libaryTable)
        self.libaryTableScroll.setWidgetResizable(True)
        # expand horizontal
        self.libaryTableScroll.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        self.libaryTableVbox = QVBoxLayout(self.libaryTableScroll)
        # expand horizontal
        self.libaryTableVbox.addWidget(QLabel('Library'))
        
        self.selectionButtons = QWidget()
        self.selectionButtonsLayout = QHBoxLayout(self.selectionButtons)
        
        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.addWidget(self.libaryTable)
        self.mainLayout.addWidget(self.selectionButtons)
        
        self.updateSelection()
              
    def updateSelection(self):
        selection = self.sender()
        selection = self.selection if selection is None else selection.text()
        # get origin element that calls switchSelection
        if selection == 'Files':
            self.selection = 'Files'
            self.data = self.library.files
        elif selection == 'Folders':
            self.selection = 'Folders'
            self.data = self.library.folders
        elif selection == 'Labels':
            self.selection = 'Labels'
            self.data = self.library.labels
        else:
            return
      
        self.updateElements()
      
    def updateElements(self):
        self.updateButtons()
        self.updateItems()
        
        # selection buttons for table view "files", "folder", "labels", "segmets"

    def updateButtons(self):
        self.clearLayout(self.selectionButtonsLayout)
        self.selectionButtons = []
        
        # spacer horizontalSpacer
        self.selectionButtonsLayout.addStretch()
        
        ###############################
        for selection in self.selections:
          self.selectionButtons = append(self.selectionButtons, QPushButton(selection, clicked=self.updateSelection))
          self.selectionButtonsLayout.addWidget(self.selectionButtons[-1])
            
    def updateItems(self):
        self.clearLayout(self.libaryTableVbox)
        # add horizontal expand
        
        self.itemContainers = []

        ###############################
        header_item = LibraryTableItemWidget(self.data[0], selection=self.selection)
        self.libaryTableVbox.addWidget(header_item.getHeaderWidget())
        ###############################
        for index, item in enumerate(self.data):
            item = LibraryTableItemWidget(item, selection=self.selection)
            self.itemContainers = append(self.itemContainers, item)
            self.libaryTableVbox.addWidget(self.itemContainers[index])
            
        ###############################
        
        
    def clearLayout(self, layout):
      if layout is not None:
          while layout.count():
              child = layout.takeAt(0)
              if child.widget():
                  child.widget().deleteLater()
              if child.layout():
                  self.clearLayout(child.layout())
        

