"""
Created on 20 de ene. de 2016

@author: IHC
"""

# Standard libs:
import time
import threading
import traceback
from _socket import timeout
from urllib.request import URLError
from datetime import timedelta
from http.client import HTTPException

# QGIS / PyQt libs:
from qgis.utils import iface
from PyQt5.QtCore import pyqtSlot, QTime, pyqtSignal
from qgis.core import QgsMessageLog, Qgis
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem, QDockWidget
from PyQt5.Qt import Qt

# Our libs:
from .AnimationController2 import Controller
from . import AnimationWCSManager, AnimationWMSManager, Animation_menu

class AnimationFrame(QDockWidget):
    """Animation widget UI manager.

    It basically redirects all inputs to AnimationController.Controller,
    which behaves as a controller/presenter.

    This interface must be given the MapObject to work with
    """
    lock = threading.RLock()
    errorSignal = pyqtSignal(str) #We will delegate any error reporting to the class which uses this widget.
    
    def __init__(self, parent = None):
        super(AnimationFrame, self).__init__(parent)
        self.parent = parent
        self.animationUI = Animation_menu.Ui_dockAnimationWidget()
        self.animationUI.setupUi(self)

        if iface and not iface.mainWindow().restoreDockWidget(self):
            iface.mainWindow().addDockWidget(Qt.RightDockWidgetArea, self)

        self.mapObject = None
        self.addLayerMenu = None

        self.animationUI.progressBar.hide()
        self.animationUI.labelInfo.setText("")
        self.animationUI.animationSlider.sliderMoved.connect(self.onUserMovesSlider)
        #We disable controller to avoid accidental inputs
        self.animationUI.labelInfo.setEnabled(True)
        #self.animationUI.animationSlider.setEnabled(False)
        #self.animationUI.playButton.setEnabled(False)
        self.animationUI.cancelButton.hide()

        self.animationUI.addWCSButton.clicked.connect(self._onAddWCSLayerButtonClicked)
        self.animationUI.addWMSButton.clicked.connect(self._onAddWMSLayerButtonClicked)
        self.animationUI.addOtherButton.clicked.connect(self._onAddOtherLayerButtonClicked)
        self.animationUI.removeButton.clicked.connect(self._removeLayerFromAnimation)
        self.animationUI.cancelButton.clicked.connect(self._onCancelRequested)
        self.animationUI.playButton.clicked.connect(self.play)
        self.animationUI.buttonLoad.clicked.connect(self.prepareAnimation)
        self.layerInfoList = []
        self.animationUI.frameRateSpinbox.valueChanged.connect(self._newFrameRateSelected)
        #self.animationUI.timeFrameVariation.timeChanged.connect(self._timeVariationChanged)
        #self.animationUI.daysFrameVariation.valueChanged.connect(self._timeVariationChanged)

        #self.animationUI.timeTolerance.timeChanged.connect(self._toleranceChanged)
        #self.animationUI.daysTolerance.valueChanged.connect(self._toleranceChanged)

        self.initController()
        self.animationUI.timeFrameVariation.setTime(QTime(1, 0, 0))
        self._timeVariationChanged(QTime(1, 0, 0))

        iface.addDockWidget( Qt.LeftDockWidgetArea, self )

    def initController(self):
        """Initializes a new controller to handle all the animation functions."""

        self.controller = Controller(self.parent)
        self.controller.animationGenerationStepDone.connect(self._updateProgressBar)
        self.controller.newFrameShown.connect(self._updateSeekBar)
        self.controller.animatorReady.connect(self._onAnimationReady)
        self.controller.externalAnimationLoaded.connect(self._addLayerToAnimation)
        self.controller.errorSignal.connect(self._onError)
        self.controller.statusSignal.connect(self._updateInfoText)
        self.controller.animationPlaybackEnd.connect(self._onAnimationPlaybackFinish)

    @pyqtSlot()
    def _removeLayerFromAnimation(self):
        """Removes one of the layers to be animated from the animation handler."""

        selectedIndex = self.animationUI.tableLayerList.currentRow()
        if selectedIndex >= 0:
            self.layerInfoList.remove(self.layerInfoList[selectedIndex])
            self._updateTable()

    @pyqtSlot()
    def _onCancelRequested(self):
        if self.controller:
            self.controller.cancelLoad()

    @pyqtSlot(str)
    def _onError(self, errorMessage):
        self.errorSignal.emit(errorMessage)

    @pyqtSlot(str)
    def _updateInfoText(self, message):
        self.animationUI.labelInfo.setText(message)

    def _resetUIPlaybackController(self):
        self.animationUI.animationSlider.setMinimum(0)
        self.animationUI.animationSlider.setMaximum(0)

    @pyqtSlot()
    def _onAddWCSLayerButtonClicked(self):
        if self.mapObject and self.mapObject.getWCS():
            self.addLayerMenu = AnimationWCSManager.AnimationWCSLayerManager(self.mapObject)
            self.addLayerMenu.animationLayerCreated.connect(self._addLayerToAnimation)
            self.addLayerMenu.show()
        else:
            self.onError("A map must first be selected\nin THREDDS Explorer catalog view.")

    @pyqtSlot()
    def _onAddWMSLayerButtonClicked(self):
        if self.mapObject:
            try:
                self.addLayerMenu = AnimationWMSManager.AnimationWMSLayerManager(self.mapObject)
                self.addLayerMenu.animationLayerCreated.connect(self._addLayerToAnimation)
                self.addLayerMenu.show()
            except (HTTPException, URLError, timeout):
                #self.onError("Connection error: Server or resource unreachable.")
                #QgsMessageLog.logMessage(traceback.format_exc(), "THREDDS Explorer", QgsMessageLog.CRITICAL )
                iface.messageBar().pushMessage("THREDDS Explorer", "Connection error: Server or resource unreachable.", level=Qgis.Critical)
        else:
            self.onError("A map must first be selected\nin THREDDS Explorer catalog view.")

    @pyqtSlot()
    def _onAddOtherLayerButtonClicked(self):
        if self.controller is None:
            self.initController()
        self.controller.addExternalTimeLayer()

    @pyqtSlot(object)
    def _addLayerToAnimation(self, animationLayer):
        """Will create an AnimationLayer object with the required information,
        and append it to our self.layerList internal list.
        """
        al = animationLayer
        if self.addLayerMenu:
            self.addLayerMenu.close()
            self.addLayerMenu = None

        self.layerInfoList.append(animationLayer)
        self._updateTable()

    @pyqtSlot(int)
    def onUserMovesSlider(self, newValue):
        if self.controller is not None:
            self.controller.setCurrentFrame(newValue)
            time.sleep(0.1) #Dirty hack to avoid an extreme number of value updates per second.

    def _updateTable(self):
        """Updates the visual reference of which layers and maps are queued for animation. """

        table = self.animationUI.tableLayerList
        table.setRowCount(len(self.layerInfoList))
        table.setColumnCount(3)
        table.setHorizontalHeaderLabels("Map;Layer;times".split(";"))
        table.horizontalHeader().setStretchLastSection(True)
        for (i, item) in enumerate(self.layerInfoList):
            #If there is no MapObject in this element it probably
            #is because it is an external layer. We will only use
            #the AnimationLayer built-in name then.
            try:
                table.setItem(i,0, QTableWidgetItem(item.getMapObject().getName()))
            except AttributeError:
                table.setItem(i,0, QTableWidgetItem(item.getLayerName()))

            table.setItem(i,1, QTableWidgetItem(item.getLayerName()))
            table.setItem(i,2, QTableWidgetItem(str(item.getTimes())))

    @pyqtSlot()
    def _updateProgressBar(self):
        self.animationUI.progressBar.setValue(self.animationUI.progressBar.value()+1)

    @pyqtSlot(tuple)
    def _updateSeekBar(self, infoTuple):
        """Update the seek bar.

        :param infoTuple: information about the frame number and frame descriptive text
        :type  infoTuple: tuple: (frameNumber, infoText)
        """
        self._updateInfoText(infoTuple[1])
        self.animationUI.animationSlider.setValue(infoTuple[0])

    @pyqtSlot(int)
    def _newFrameRateSelected(self, frameRateMilliseconds):
        self.controller.setFrameRate(frameRateMilliseconds)
        self.animationUI.animationSlider.setMaximum(self.controller.getNumberOfFrames())

    @pyqtSlot(object)
    def _timeVariationChanged(self, value):
        vhours = self.animationUI.timeFrameVariation.time().hour() \
                + (self.animationUI.daysFrameVariation.value() * 24)
        vminutes = self.animationUI.timeFrameVariation.time().minute()
        vseconds = self.animationUI.timeFrameVariation.time().second()
        delta = timedelta(hours = vhours,\
                          minutes= vminutes,\
                          seconds= vseconds)

        self.controller.setTimeDeltaPerFrame(delta)
        self.animationUI.animationSlider.setMaximum(self.controller.getNumberOfFrames())

    @pyqtSlot(object)
    def _toleranceChanged(self):
        vhours = self.animationUI.timeTolerance.time().hour() \
                + (self.animationUI.daysTolerance.value() * 24)
        vminutes = self.animationUI.timeTolerance.time().minute()
        vseconds = self.animationUI.timeTolerance.time().second()
        tolerance = timedelta(hours = vhours,\
                          minutes= vminutes,\
                          seconds= vseconds)

        self.controller.setTimeDeviationTolerance(tolerance)

    def setAnimationInformation(self, mapObject):
        """Method used to store the Map object which holds the
        required information we may need to generate an
        AnimationLayer for it later.

        :param mapObject:
        :type  mapObject: threddsMapperGeneric.Map
        """
        self.mapObject = mapObject
        # We will pause the animation, if running, when our data is updated:
        if self.controller and self.controller.isPlaying():
            self.play()

        if not self.mapObject.getWCS():
            self.animationUI.addWCSButton.setEnabled(False)

        if not self.mapObject.getWMS():
            self.animationUI.addWButton.setEnabled(False)

    def prepareAnimation(self):
        """Puts the UI in "load mode", showing or hiding certain controls.
        It will relay the request to its controller and provide it
        with some default values.
        """
        if self.controller.isPlaying():
            self.controller.pause()

        self._resetUIPlaybackController()
        try:
            self.animationUI.progressBar.show()
            self.animationUI.cancelButton.show()
            self.animationUI.progressBar.setMinimum(0)
            self.animationUI.progressBar.setValue(0)
            self.controller.setUpAnimation(self.layerInfoList)
            self.animationUI.progressBar.setMaximum(self.controller.getMaxProgressValue())
            self.controller.setFrameRate(self.animationUI.frameRateSpinbox.value())
        except AttributeError as e:
            #self.onError(str(e))
            #QgsMessageLog.logMessage(traceback.format_exc(), "THREDDS Explorer", QgsMessageLog.CRITICAL )
            iface.messageBar().pushMessage("THREDDS Explorer", "Invalid data provided.", level=Qgis.Critical)

    def play(self):
        self.animationUI.labelInfo.show()
        # Sanity check to avoid QGIS crashes if the user attempts to create
        # a new animation while an old one is playing:
        if self.controller is not None:
            self.controller.togglePlay()

    @pyqtSlot()
    def _onAnimationReady(self):
        """Sets up the interface so the user can now
        interact with the animation playback components.
        """
        self.animationUI.progressBar.hide()
        self.animationUI.animationSlider.setMaximum(self.controller.getNumberOfFrames())
        self.animationUI.cancelButton.hide()
        self.controller.setCurrentFrame(0) #We show the user the first frame.

    @pyqtSlot()
    def _onAnimationPlaybackFinish(self):
        if self.animationUI.loopCheckbox.isChecked():
            self.play()

    def onError(self, messageString):
        box = QMessageBox()
        box.setText(messageString)
        box.setIcon(QMessageBox.Critical)
        box.exec_()

    def onSaveAnimation(self):
        """TODO: Implement"""
        pass

    def onLoadAnimation(self):
        """TODO: Implement"""
        pass
