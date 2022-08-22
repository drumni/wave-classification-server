from src.tools.Console import Console
console = Console()
console.setOwner(__file__)

from ctypes import ArgumentError
from posixpath import basename
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QLabel, QListWidget, QPushButton, QLineEdit, QScrollArea, QScrollBar, QSizePolicy, QVBoxLayout, QWidget, QHBoxLayout
from numpy.lib.function_base import append
from src.interface.components.LibraryTableItemWidget import LibraryTableItemWidget


class LibraryTableWidget(QWidget):
    def __init__(self, library=None):
        super().__init__()
        self.selections = ['Labels', 'Folders', 'Files', 'Segments']
        self.selection = 'Folders'
        self.data = []
        self.library = library
        
        self.setupLocalLayout()
        self.updateSelection()
        console.debug(f'Loaded Table: {self}')
        
            
    def setupLocalLayout(self):
        
        # self.libaryTable = QWidget()
        
        self.scrollBar = QScrollBar()
        self.scrollBar.setOrientation(Qt.Vertical)
        self.scrollBar.setSingleStep(1)
        self.scrollBar.setMaximum(100)

        # self.libaryTableScroll = QScrollArea()
        # self.libaryTableScroll.set(self.libaryTable)
        
        self.libaryTableVbox = QVBoxLayout()
        # self.libaryTableVbox.setParent(self.libaryTableVbox)
        
        self.selectionButtons = QWidget()
        self.selectionButtonsLayout = QHBoxLayout(self.selectionButtons)
        # self.mainLayout.addWidget(self.libaryTable)
      
        self.mainLayout = QVBoxLayout()
        
        self.mainLayout.addWidget(self.scrollBar)
        
        self.setLayout(self.mainLayout)
        
            
    def updateSelection(self):
        selection = self.sender()
        selection = self.selection if selection is None else selection.text()
        
        # get origin element that calls switchSelection
        self.data = self.library.getData(selection)
        if self.data is not None:
            self.selection = selection
            console.debug(f'Selection: {self.selection}')
        else:
            self.data = []

        # self.updateButtons()
        # self.updateItems()

    def updateButtons(self):
        self.clearLayout(self.selectionButtonsLayout)
        self.selectionButtons = []
        
        # spacer horizontalSpacer
        # self.selectionButtonsLayout.addStretch()
        
        ###############################
        for selection in self.selections:
          self.selectionButtons = append(self.selectionButtons, QPushButton(selection, clicked=self.updateSelection))
          self.selectionButtonsLayout.addWidget(self.selectionButtons[-1])
            
    def updateItems(self):
        console.debug(f'Updating {len(self.data)} Items')
        self.clearLayout(self.libaryTableVbox)
        
        self.itemContainers = []

        self.header_item = LibraryTableItemWidget(self.data[0], selection=self.selection).getHeaderWidget()
        self.libaryTableVbox.addWidget(self.header_item)
        
        for itemWidget in self.data:

            item = LibraryTableItemWidget(itemWidget, selection=self.selection)
            self.itemContainers = append(self.itemContainers, item)
            self.libaryTableVbox.addWidget(self.itemContainers[-1])

    def clearLayout(self, layout):
      if layout is not None:
          while layout.count():
              child = layout.takeAt(0)
              if child.widget():
                  child.widget().deleteLater()
              if child.layout():
                  self.clearLayout(child.layout())
        
