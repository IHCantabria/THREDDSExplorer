'''
Created on 27 de ene. de 2016

@author: IHC
'''
from PyQt5.QtWidgets import QMessageBox, QWidget
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from ..providersmanagers.wcs.WCSParser import WCSparser
from . import Animation_add_wcs_layer
from .AnimationLayer import AnimationLayer
from urllib.request import HTTPError, URLError
from _socket import timeout
from ..providersmanagers.BoundingBoxInfo import BoundingBox


class AnimationWCSLayerManager(QWidget):
    '''
    Manager which will allow an user to load a new layer
    information object (AnimationLayer) through WCS services.
    
    This is an useful example on how we could implement
    an AnimationLayer generator to be loaded through
    AnimationOtherLayerManager, using its own UI and data
    provider method.
    '''
    animationLayerCreated = pyqtSignal(object) #Should return instance of AnimationLayer


    def __init__(self, mapObject):
        '''
        Constructor
        '''
        QWidget.__init__(self)
        self.dialog = Animation_add_wcs_layer.Ui_AddLayerDialog()
        self.dialog.setupUi(self)
        
        self.mapObject = mapObject
        self.loadLayerList()
        #self.connect(self.dialog.layerSelector, SIGNAL("currentIndexChanged(const QString&)"), self._onSelectedCoverageChanged)
        #self.connect(self.dialog.beginTimeSelector, SIGNAL("currentIndexChanged(int)"), self._onSelectedBeginTime)
        self.dialog.layerSelector.currentIndexChanged[str].connect(self._onSelectedCoverageChanged)
        self.dialog.beginTimeSelector.currentIndexChanged[int].connect(self._onSelectedBeginTime)
        
        self.dialog.buttonAddLayer.clicked.connect(self._onAcceptClicked)
        
        
    def loadLayerList(self):
        self.dialog.buttonAddLayer.setEnabled(False) #We disable the accept button while no layer can be created
        parser = WCSparser(self.mapObject.getWCS().getCapabilitiesURL())
        try:
            self.coverages = parser.getAvailableCoverages()
        except (HTTPError, timeout, URLError):
            self.coverages = None
            self.dialog.layerSelector.clear()
            self.dialog.layerSelector.addItems(["No layers available."])
            self.dialog.beginTimeSelector.clear()
            self.dialog.beginTimeSelector.addItem("No times available")
            self.dialog.finishTimeSelector.clear()
            self.dialog.finishTimeSelector.addItem("No times available")
            return
        #A map will be created in the form layerName : timesAvailable
        self.dataList = {}
        
        if self.coverages is not None:
            for layer in self.coverages:
                self.dataList[layer.getName()] = layer.getTiempos()

        self.dialog.layerSelector.clear()
        self.dialog.layerSelector.addItems(self.dataList.keys())
        self.dialog.layerSelector.setCurrentIndex(0)
        #We force a first update on the available times...
        self._onSelectedCoverageChanged(self.dialog.layerSelector.currentText())
        
    @pyqtSlot(str)
    def _onSelectedCoverageChanged(self, QStringItem):
        self.selectedCover = [x for x in self.coverages if x.getName() == QStringItem][0]
        bbox = self.selectedCover.getBoundingBoxInfo();
        self.dialog.beginTimeSelector.clear()
        try:
            self.dialog.beginTimeSelector.addItems(self.dataList[str(QStringItem)])
        except KeyError:
            pass
        self._onSelectedBeginTime(0)
        self.repopulateBBOX(bbox)
      
    @pyqtSlot(int)
    def _onSelectedBeginTime(self, position):
        #Only times which are after the one picked in the "begin at.."
        #will be able to be selected in the "finish at.." box.
        self.dialog.finishTimeSelector.clear()
        try:
            self.dialog.finishTimeSelector.addItems(
                        (self.dataList[self.dialog.layerSelector.currentText()])[position:] )
        except KeyError:
            pass
        self.dialog.buttonAddLayer.setEnabled(True)
        
    @pyqtSlot()
    def _onAcceptClicked(self):
        selectedLayer = self.dialog.layerSelector.currentText()
        allAvailableTimes = self.dataList[str(selectedLayer)]
        selectedBeginTimeIndex = allAvailableTimes.index(self.dialog.beginTimeSelector.currentText())
        selectedFinishTimeIndex = allAvailableTimes.index(self.dialog.finishTimeSelector.currentText())
        try:
            north = float(self.dialog.northBound.text())
            south = float(self.dialog.southBound.text())
            east = float(self.dialog.eastBound.text())
            west = float(self.dialog.westBound.text())
        except ValueError:
            box = QMessageBox()
            box.setText("Bounding box values were not valid."
            +"\nCheck only decimal numbers are used\n(example: 12.44)")
            box.setIcon(QMessageBox.Critical)
            box.exec_()
            return
                        
        requestedBBOX = BoundingBox()
        requestedBBOX.setCRS(self.selectedCover.getBoundingBoxInfo().getCRS())
        requestedBBOX.setSouth(south)
        requestedBBOX.setNorth(north)
        requestedBBOX.setEast(east)
        requestedBBOX.setWest(west)
        
        returnObject = AnimationLayer(self.mapObject,
                                      self.dialog.layerSelector.currentText(),
                                      allAvailableTimes[selectedBeginTimeIndex:selectedFinishTimeIndex+1],
                                      "WCS",
                                      boundingBox = requestedBBOX)
        self.animationLayerCreated.emit(returnObject)
        
    def repopulateBBOX(self, bboxInfoObject):
        """
        :param bboxInfoObject: The object with crs and bbox information
        :type  bboxInfoObject BoundingBoxInfo.BoundingBox
        """
        self.dialog.northBound.setText(bboxInfoObject.getNorth())
        self.dialog.southBound.setText(bboxInfoObject.getSouth())
        self.dialog.eastBound.setText(bboxInfoObject.getEast())
        self.dialog.westBound.setText(bboxInfoObject.getWest())
        self.dialog.labelCRS.setText("CRS: "+bboxInfoObject.getCRS())
    
    