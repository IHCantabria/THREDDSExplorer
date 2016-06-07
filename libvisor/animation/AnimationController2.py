'''
Created on 28 de ene. de 2016

@author: IHC
'''
from PyQt4.QtCore import QObject, QTimer, pyqtSignal, pyqtSlot, Qt
import threading
from qgis.core import QgsRasterLayer, QgsMapLayerRegistry, QgsProject, QgsRectangle, QgsLayerTreeLayer
from qgis.utils import iface
import time
from THREDDSExplorer.libvisor.animation.Animation2 import AnimationData
from THREDDSExplorer.libvisor.animation.AnimationLayer import AnimationLayer
from THREDDSExplorer.libvisor.animation import AnimationOtherLayerManager
from datetime import timedelta
from THREDDSExplorer.libvisor.providersmanagers.wcs.WCSBatchDownloadUtil import WCSDownloadWorkerThread
from THREDDSExplorer.libvisor.providersmanagers.wms.WMSBatchDownloadUtil import WMSDownloadWorkerThread
from THREDDSExplorer.libvisor.utilities.LayerLegendGroupifier import LayerGroupifier
from qgis.core import QgsMessageLog
import traceback


class Controller(QObject):
    '''
    Manages all operations required to handle animation operations.

    a) Load time-aware data from any of several supported providers.
    b) Create a single or multiple layer animation.
    c) Play, stop, find frames.

    After creating this object, whatever is calling it should
    provide it with a number of AnimationLayer objects through
    its setUpAnimation() method, which accepts a list of them.
    It will then read each layer's getAnimationData() and
    getAnimationLegendGroups() methods, and if no data is defined
    in -both- of them, it'll attempt to find a controller suitable
    to download and generate that information, to create a fully
    interpretable AnimationLayer object. This controller can, at
    this point, handle WMS/WCS data download, and load any proper
    AnimationLayer object.

    After performing the AnimationLayer load (either by downloading
    required data or not because it had all the data already prepared),
    updateTimeRange() will be called to update the oldest and newest
    time which will be played. This allows us to handle the animation
    as a time series instead of a simple frame-by-frame based animation.

    Through the method setTimeDeltaPerFrame() we can tell the animator
    how much map time will pass between frame updates, and
    setTimeDeviationTolerance() will define how much deviation from
    that exact time we allow when looking for the map to draw in
    QGIS interface.

    Several signals provide for status updates while preparing or
    playing back the animation.

    '''
    animationPlaybackEnd = pyqtSignal()
    animatorReady = pyqtSignal()
    externalAnimationLoaded = pyqtSignal(object)#Must be an AnimationLayer like object
    animationGenerationStepDone = pyqtSignal()
    newFrameShown = pyqtSignal(tuple) #Emitted when a new 'time frame' is shown, with the time tag as parameter
    #Self-signal so the group creation will be run on main thread
    #even after being requested by async ops.
    createLayerGroupsOnMainThread = pyqtSignal(AnimationLayer, str)
    maxDownloadThreads = 3
    lock = threading.RLock()
    groupAssignmentLock = threading.RLock()
    errorSignal = pyqtSignal(str)
    statusSignal = pyqtSignal(str)


    def __init__(self, parent = None):
        '''
        Constructor
        '''
        #TODO: Remove debug
        #import sys
        #sys.stdout = open(r'F:\PROYECTOS_IH\_UNVERSIONED\visorlog.txt', 'w')

        super(Controller, self).__init__(parent)
        self.paused = True

        self.playbackSpeed = 500
        self.timer = QTimer()
        self.timer.timeout.connect(self.onNextFrameRequested)
        self.createLayerGroupsOnMainThread.connect(self.createLayerGroup)
        iface.mapCanvas().setParallelRenderingEnabled(True)
        self.timeDeviationTolerance = None
        self.timeDeltaPerFrame = None
        self.initialize()

    def initialize(self):
        self.animationBeginTime = None
        self.animationEndTime = None

        self.threadsInUse = {} #Dictionary which contains all the 'worker objects' and their assocciated threads.
                                #in {workerObject : threadObject} form so we can cancel and so stuff with both.
        self.framesShown = []
        self.animationElements = []
        self.animationGroups = [] #QGIS UI layer groups
        self.nextFrame = None #next time to be requested
        self.paused = True
        self.maxProgress = 0
        self.layersToBeGrouped = 0
        self.errors = False
        self.maxAnimationGroupsToBeCreated = 0
        self.layersAddedToGroups = 0



    #
    # Methods to assist in playback
    #
    def play(self):
        if self.animationGroups is not None and len(self.animationGroups) != 0:
            self.timer.start(self.playbackSpeed)
            self.paused = False

    def pause(self):
        self.paused = True
        self.timer.stop()

    def togglePlay(self):
        if self.paused:
            self.play()
        else:
            self.pause()

    def getNumberOfFrames(self):
        try:
            timeRangeInDelta = abs(self.animationEndTime - self.animationBeginTime)
            return int( (timeRangeInDelta.total_seconds()/self.timeDeltaPerFrame.total_seconds()))
        except (AttributeError, ZeroDivisionError, TypeError):
            QgsMessageLog.logMessage(traceback.format_exc(), "THREDDS Explorer", QgsMessageLog.CRITICAL )
            return 0


    def onNextFrameRequested(self):
        if self.nextFrame is None or self.nextFrame < self.animationBeginTime:
            self.nextFrame = self.animationBeginTime
        elif self.nextFrame > self.animationEndTime:
            #print("====END====")
            #print(self.nextFrame)
            #print(self.animationEndTime)
            #print("====END====")
            self.pause()
            self.nextFrame = self.animationBeginTime
            self.animationPlaybackEnd.emit()
            return


        self.framesShown = []
        for animation in self.animationElements:
            try:
                layer = animation.getFrameByTime(self.nextFrame,
                                                  self.timeDeviationTolerance)
                try:
                    iface.legendInterface().setLayerVisible(layer, True)
                except RuntimeError:
                    #Will happen if the animator attempts to set as visible
                    #a no longer existing layer (i.e. if the user removes
                    #that layer or group from the legend interface).
                    self.pause()
                    self.errorSignal.emit("A layer for this animation was not found.\nWas it removed?"\
                                          " Please, click\nagain on prepare animation to fix this issue.")
                    QgsMessageLog.logMessage(traceback.format_exc(), "THREDDS Explorer", QgsMessageLog.CRITICAL )
                self.framesShown.append(layer)
            except KeyError:
                QgsMessageLog.logMessage(traceback.format_exc(), "THREDDS Explorer", QgsMessageLog.CRITICAL )
                #print("MAP NOT FOUND ANIMATIONCONTROLLER"+str(self.nextFrame))
                continue

        #print("MAP SEARCH FINISHED")
        try:
            nextFrameToBeDisplayedIndex = \
                abs((self.animationBeginTime - self.nextFrame).total_seconds())/self.timeDeltaPerFrame.total_seconds()
        except TypeError:
            #Will happen if this animation is reset while running.
            self.pause()
            return

        #print("next frame to show int: "+str(nextFrameToBeDisplayedIndex))
        self.newFrameShown.emit((nextFrameToBeDisplayedIndex, str(self.nextFrame)))
        self.nextFrame = self.nextFrame + self.timeDeltaPerFrame

    def setCurrentFrame(self, intFramePosition):
        """
        Sets the animation in the specified frame.
        """
        timeDelta = timedelta(seconds=intFramePosition * self.timeDeltaPerFrame.total_seconds())
        self.nextFrame = self.animationBeginTime + timeDelta
        if self.paused:
            #If the animation is paused, we will manually
            #trigger a new layer draw.
            self.onNextFrameRequested()

    def setFrameRate(self, millisecondsPerFrame):
        self.playbackSpeed = millisecondsPerFrame
        if not self.paused:
            #If the animation is running, we will stop and restart it
            #so it uses our new framerate.
            self.pause()
            self.play()

    def setTimeDeviationTolerance(self, timedeltaMaxDeviation):
        """
        Sets the maximum allowed variation between the expected
        time to be shown to the user and the actual one stored.

        This means, if we are playing at 15 min / second, and
        we have a tolerance of 5 minutes, when the animation
        controller requests the map for 15:00, the closest
        map available for that time will be shown within the
        set tolerance. This might be a map "set" between
        14:55 and 15:05.

        :param timedeltaMaxDeviation: Max time deviation or None for exact
                                      match.
        :type  timedeltaMaxDeviation: datetime.timedelta
        """
        self.timeDeviationTolerance = timedeltaMaxDeviation
        #print("Tolerance = "+str(self.timeDeviationTolerance))

    def setTimeDeltaPerFrame(self, timeDelta):
        self.timeDeltaPerFrame = timeDelta

    def isPlaying(self):
        return not self.paused


    #
    # Methods to create the animation elements and manage them
    #
    def setUpAnimation(self, animationLayerList):

        if animationLayerList is None or len(animationLayerList) == 0:
            raise AttributeError("Invalid data provided.")

        self.initialize()

        self.animationLayerObjectList = animationLayerList

        wcsLayers = []
        wmsLayers = []
        otherLayers = []
        for animationLayer in animationLayerList:
            #If the layer has both animationData and legendGroups ready,
            #it is ready to be used, no matter its origin, which should
            #be through a controller which generates an AnimationLayer.
            if animationLayer.getAnimationData() is not None \
                and animationLayer.getAnimationLegendGroups() is not None:
                otherLayers.append(animationLayer)

            #Other supported layers missing those attributes should be handled
            #separately.
            #TODO: Refactor this WMS/WCS layer fabrication through an external
            #controller, as TESEO one, sort of...
            elif animationLayer.getService() == "WMS":
                wmsLayers.append(animationLayer)
            elif animationLayer.getService() == "WCS":
                wcsLayers.append(animationLayer)

        #The max amount of steps which will be reported to progress
        #bars or such things will be one operation per WCS animationLayer
        #retrieval attempt (begin, end), and four per WMS animationLayer
        #retrieval attempt (two per range check, one to begin
        #retrieving the animationLayer itself, one when it finishes)
        self.maxProgress = 2*sum([len(x.getTimes()) for x in wcsLayers]) \
                         + 3*sum([len(x.getTimes()) for x in wmsLayers])

        for animationLayer in otherLayers:
            if animationLayer.getAnimationLegendGroups() is not None:
                self.animationGroups.append(animationLayer.getAnimationLegendGroups())
                self.animationElements.append(animationLayer.getAnimationData())
                self.updateTimeRange(animationLayer.getAnimationData().frameData.keys())

        self.maxAnimationGroupsToBeCreated = len(wmsLayers) + len(wcsLayers) + len(otherLayers)
        if len(wmsLayers) > 0:
            threading.Thread(target = self.createMultipleWMSAnimationElements, args=(wmsLayers,)).start()
        if len(wcsLayers) > 0:
            threading.Thread(target = self.createMultipleWCSAnimationElements, args=(wcsLayers,)).start()

        #If no layers must be downloaded, it's over and ready.
        if len(wmsLayers) == 0 and len(wcsLayers) == 0:
            #print("READY WITHOUT LAYERS")
            self.animatorCreated()
            return

        self.statusSignal.emit("Downloading layers...")


    def cancelLoad(self):
        try:
            for item in self.threadsInUse.keys():
                item.requestCancellation()
                #print("ITEM ALIVE: "+str((self.threadsInUse[item]).isAlive()))
                self.threadsInUse.pop(item)
            self.statusSignal.emit("Operation cancelled.")
        except AttributeError:
            pass


    def animatorCreated(self):
        #print("ANIMATOR CREATED --------------")
        self.animatorReady.emit()

        if self.errors == True :
            self.errorSignal.emit("An error occured during the download.\nThe animation may have gaps.")

    def getMaxProgressValue(self):
        """
        This will report the maximum number of operations/steps
        which will be done by this controller when attempting
        to prepare an animation.
        """
        return self.maxProgress



    def createMultipleWCSAnimationElements(self, animationLayerList):
        """
        :param     animationLayerList:    List of AnimationLayer to be created and managed
                                          by this controller.
        :type      animationLayerList:    [AnimationLayer]

        """
        for item in animationLayerList:
            worker = WCSDownloadWorkerThread(item.getMapObject().getWCS().getCapabilitiesURL(),
                                 item.getTimes(),
                                 item.getLayerName(),
                                 parent = self)

            baseLayerDictionary = worker.getLayerDict()
            animData = AnimationData(item.getLayerName(), baseLayerDictionary)
            item.setAnimationData(animData)

            worker.WCSFrameStartsDownload.connect(self.animationGenerationStepDone.emit, Qt.DirectConnection)
            worker.WCSFrameFinishedDownload.connect(self.animationGenerationStepDone.emit, Qt.DirectConnection)
            worker.WCSProcessdone.connect(self.BatchWorkerThreadDone)
            worker.WCSMapDownloadFail.connect(self.WorkerThreadDownloadError)
            thread = threading.Thread(target = worker.run)
            self.threadsInUse[worker] = thread
            thread.start()

    def createMultipleWMSAnimationElements(self, animationLayerList):
        """
        :param     animationLayerList:    List of AnimationLayer to be created and managed
                                          by this controller.
        :type      animationLayerList:    [AnimationLayer]

        """
        for item in animationLayerList:
            worker = WMSDownloadWorkerThread(
                                 item.getMapObject().getWMS(),
                                 item.getTimes(),
                                 item.getLayerName(),
                                 item.getStyle(),
                                 parent = self)
            baseLayerDictionary = worker.getLayerDict()
            animData = AnimationData(item.getLayerName()+"_"+item.getStyle(), baseLayerDictionary)
            item.setAnimationData(animData)
            worker.WMSFrameStartsDownload.connect(self.animationGenerationStepDone.emit, Qt.DirectConnection)
            worker.WMSFrameFinishedDownload.connect(self.animationGenerationStepDone.emit, Qt.DirectConnection)
            worker.WMSSingleValueRangeProcessed.connect(self.animationGenerationStepDone.emit, Qt.DirectConnection)
            worker.WMSprocessdone.connect(self.BatchWorkerThreadDone)
            worker.WMSMapDownloadFail.connect(self.WorkerThreadDownloadError)
            thread = threading.Thread(target = worker.run)
            self.threadsInUse[worker] = thread
            thread.start()


    @pyqtSlot(dict, QObject)
    def BatchWorkerThreadDone(self, layerDict, workerObject):
        """
        :param animationLayerObject: The previously provided AnimationLayer object
                                     for this animated map in createMultipleWMS/WCSAnimationElements.
        :type  animationLayerObject: AnimationLayer

        :param layerDict: The dictionary holding the layers in the form timestamp : layer
                          It is already held inside animationLayerObject, but the signal
                          is emitted with a reference to it in case the AnimationLayer
                          object was not provided to the batch downloader (i.e. in the static
                          viewer case).
        :type  layerDict: dict

        :param workerObject: The thread object
        :type  workerObject: QObject
        """
        try:
            self.threadsInUse.pop(workerObject) #We have to keep our list clean.
            #We find what animationLayer object this dictionary
            #is from

            animationLayerObject = \
             ([x for x in self.animationLayerObjectList if x.getAnimationData().frameData == layerDict])[0]

            self.initializeAnimator(animationLayerObject)
            groupName = animationLayerObject.getMapObject().getName()+"-"+animationLayerObject.getLayerName()
            threading.Thread(target = self.addPendingLayerGroupRequest,
                             args = (animationLayerObject,
                                     groupName)).start()
        except KeyError:
            #Might happen if a thread is cancelled in the last frame download,
            #as it'll already have been queued for removal from the threadsInUse dict
            pass

    @pyqtSlot(int, str)
    def WorkerThreadDownloadError(self, numberOfFailedDownloads, layerName):
        self.errorSignal.emit("Warning: "+str(numberOfFailedDownloads)+" frames failed to be downloaded from layer \n"
                              +layerName+". The resulting animation\nmay have gaps.")


    def initializeAnimator(self, animationLayerObject):
        animationData = animationLayerObject.getAnimationData()
        self.animationElements.append(animationData)
        self.updateTimeRange(animationData.frameData.keys()) #We update the list of times covered by our frames


    def addExternalTimeLayer(self):
        self.addLayerMenu = AnimationOtherLayerManager.AnimationOtherLayerManager(self)
        self.addLayerMenu.animationLayerCreated.connect(self.addNewExternalAnimatedLayer)
        self.addLayerMenu.show()

    @pyqtSlot(object)
    def addNewExternalAnimatedLayer(self, animationLayer):
        self.externalAnimationLoaded.emit(animationLayer)


    def updateTimeRange(self, newElements):
        """
        Will append the given list of times to the current ones available
        for animation, remove any duplicates, and sort them.
        """
        orderedElements = sorted(newElements)
        if newElements == None or len(newElements) == 0:
            return

        if self.animationBeginTime is None \
        or self.animationBeginTime > orderedElements[0]:
            self.animationBeginTime = orderedElements[0]

        if self.animationEndTime is None \
        or self.animationEndTime < orderedElements[len(orderedElements)-1]:
            self.animationEndTime = orderedElements[len(orderedElements)-1]



    @pyqtSlot(AnimationLayer,str)
    def addPendingLayerGroupRequest(self, animationLayerObject, groupName):
        while len(self.threadsInUse.keys()) > 0:
            time.sleep(0.5)
        self.createLayerGroupsOnMainThread.emit(animationLayerObject, groupName)


    def createLayerGroup(self, animationLayerObject, groupName):
        layerList = animationLayerObject.getAnimationData().frameData.values()
        groupifier = LayerGroupifier(layerList, groupName)
        groupifier.statusSignal.connect(self.statusSignal)
        groupifier.groupifyComplete.connect(self._newLegendGroupReady)
        #We assign the generated group reference to this animationLayer object
        animationLayerObject.setAnimationLegendGroups(groupifier.getGeneratedGroup())
        groupifier.groupify()

    def _newLegendGroupReady(self, qgsGroupObject):
        self.animationGroups.append(qgsGroupObject)
        if len(self.animationGroups) == self.maxAnimationGroupsToBeCreated:
            self.animatorCreated()
