'''
Created on 27 de ene. de 2016

@author: IHC
'''
from PyQt4.QtGui import QWidget
from PyQt4.QtCore import pyqtSignal, pyqtSlot, SIGNAL
from THREDDSExplorer.libvisor.providersmanagers.wcs.WCSParser import WCSparser
from THREDDSExplorer.libvisor.animation import Animation_add_wcs_layer
from THREDDSExplorer.libvisor.animation.AnimationLayer import AnimationLayer
from urllib2 import HTTPError, URLError
from _socket import timeout


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
        self.connect(self.dialog.layerSelector, SIGNAL("currentIndexChanged(const QString&)"), self._onSelectedCoverageChanged)
        self.connect(self.dialog.beginTimeSelector, SIGNAL("currentIndexChanged(int)"), self._onSelectedBeginTime)
        
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
        self.dialog.beginTimeSelector.clear()
        try:
            self.dialog.beginTimeSelector.addItems(self.dataList[str(QStringItem)])
        except KeyError:
            pass
        self._onSelectedBeginTime(0)
      
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
        
        
        returnObject = AnimationLayer(self.mapObject,
                                      self.dialog.layerSelector.currentText(),
                                      allAvailableTimes[selectedBeginTimeIndex:selectedFinishTimeIndex+1],
                                      "WCS")
        self.animationLayerCreated.emit(returnObject)
    
    