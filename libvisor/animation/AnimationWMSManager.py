"""
Created on 27 de ene. de 2016

@author: IHC
"""
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from ..providersmanagers.wms.WMSParser import WMSparser
from . import Animation_add_wms_layer
from .AnimationLayer import AnimationLayer
from urllib.request import HTTPError, URLError
from _socket import timeout


class AnimationWMSLayerManager(QWidget):
    """Manager which will allow an user to load a new layer
    information object (AnimationLayer) through WCS services.

    This is an useful example on how we could implement
    an AnimationLayer generator to be loaded through
    AnimationOtherLayerManager, using its own UI and data
    provider method.
    """

    animationLayerCreated = pyqtSignal(
        object
    )  # Should return instance of AnimationLayer

    def __init__(self, mapObject):
        """Constructor."""

        QWidget.__init__(self)
        self.dialog = Animation_add_wms_layer.Ui_AddLayerDialog()
        self.dialog.setupUi(self)

        self.mapObject = mapObject
        self.loadLayerList()
        # self.connect(self.dialog.layerSelector, SIGNAL("currentIndexChanged(const QString&)"), self._onSelectedLayerChanged)
        # self.connect(self.dialog.graphicSelector, SIGNAL("currentIndexChanged(const QString&)"), self._onWMSGraphicSelectorSelectorItemChanged)
        # self.connect(self.dialog.beginTimeSelector, SIGNAL("currentIndexChanged(int)"), self._onSelectedBeginTime)
        self.dialog.layerSelector.currentIndexChanged[str].connect(
            self._onSelectedLayerChanged
        )
        self.dialog.graphicSelector.currentIndexChanged[str].connect(
            self._onWMSGraphicSelectorSelectorItemChanged
        )
        self.dialog.beginTimeSelector.currentIndexChanged[int].connect(
            self._onSelectedBeginTime
        )

        self.dialog.buttonAddLayer.clicked.connect(self._onAcceptClicked)

    def loadLayerList(self):
        self.dialog.buttonAddLayer.setEnabled(
            False
        )  # we disable the accept button while no layer can be created
        parser = WMSparser(self.mapObject.getWMS())
        self.dialog.layerSelector.clear()
        try:
            self.mapInfo = parser.getMapInfo()
        except (HTTPError, timeout, URLError):
            self.mapInfo = None
            self.dialog.layerSelector.addItem("No layers available.")
            self.dialog.beginTimeSelector.clear()
            self.dialog.beginTimeSelector.addItem("No times available")
            self.dialog.finishTimeSelector.clear()
            self.dialog.finishTimeSelector.addItem("No times available")
            self.dialog.graphicSelector.clear()
            self.dialog.graphicSelector.addItem("No styles available.")

            return

        if self.mapInfo:
            self.dialog.layerSelector.addItems(
                [x.getName() for x in self.mapInfo.getLayers()]
            )

        self.dialog.layerSelector.setCurrentIndex(0)

        # We force a first update on the available times:
        self._onSelectedLayerChanged(self.dialog.layerSelector.currentText())

    @pyqtSlot(str)
    def _onSelectedLayerChanged(self, QStringItem):
        self.dialog.graphicSelector.clear()
        self.dialog.paletteSelector.clear()
        self.dialog.beginTimeSelector.clear()
        for layer in self.mapInfo.getLayers():
            if layer.getName() == str(QStringItem):
                self.selectedLayer = layer
                self.wmsAvailableStyles = layer.getStyles()
                self.dialog.graphicSelector.addItems(
                    list(
                        {(x.getName().split(r"/"))[0] for x in self.wmsAvailableStyles}
                    )
                )
                self._onWMSGraphicSelectorSelectorItemChanged(
                    self.dialog.graphicSelector.currentText()
                )
                self.dialog.graphicSelector.setCurrentIndex(0)
                self.dialog.beginTimeSelector.addItems(self.selectedLayer.getTimes())
                self._onSelectedBeginTime(0)

    @pyqtSlot(str)
    def _onWMSGraphicSelectorSelectorItemChanged(self, qstringitem):
        self.dialog.paletteSelector.clear()
        self.dialog.paletteSelector.addItems(
            list(
                {
                    (x.getName().split(r"/"))[1]
                    for x in self.wmsAvailableStyles
                    if str(qstringitem) in x.getName()
                }
            )
        )

    @pyqtSlot(int)
    def _onSelectedBeginTime(self, position):
        # Only times which are after the one picked in the "begin at.."
        # will be able to be selected in the "finish at.." box.
        self.dialog.finishTimeSelector.clear()
        try:
            self.dialog.finishTimeSelector.addItems(
                self.selectedLayer.getTimes()[position:]
            )
        except KeyError:
            pass
        self.dialog.buttonAddLayer.setEnabled(True)

    @pyqtSlot()
    def _onAcceptClicked(self):
        selectedLayer = self.dialog.layerSelector.currentText()

        # Get bounding box, if possible. Default is None.
        bbox = None
        if self.mapInfo:
            for layer in self.mapInfo.getLayers():
                if layer.getName() == selectedLayer:
                    bbox = layer.getBoundingBoxInfo()

        allAvailableTimes = self.selectedLayer.getTimes()
        selectedBeginTimeIndex = allAvailableTimes.index(
            self.dialog.beginTimeSelector.currentText()
        )
        selectedFinishTimeIndex = allAvailableTimes.index(
            self.dialog.finishTimeSelector.currentText()
        )

        returnObject = AnimationLayer(
            mapObject=self.mapObject,
            layerName=selectedLayer,
            times=allAvailableTimes[
                selectedBeginTimeIndex : selectedFinishTimeIndex + 1
            ],
            service="WMS",
            boundingBox=bbox,
            selectedStyle=self.dialog.graphicSelector.currentText(),
        )

        self.animationLayerCreated.emit(returnObject)
