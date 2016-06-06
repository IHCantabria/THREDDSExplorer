# -*- coding:utf8 -*-

from THREDDSExplorer.libvisor.providersmanagers.wcs import WCSParser as WCS
import THREDDSExplorer.libvisor.providersmanagers.wms.WMSParser as WMS
import THREDDSExplorer.libvisor.ThreddsMapperGeneric as TFR
import threading
import tempfile
import urllib2
from httplib import HTTPException
from THREDDSExplorer.libvisor.persistence.ServerDataPersistenceManager import ServerStorageManager
from PyQt4.QtCore import pyqtSlot, pyqtSignal, QObject
from urllib2 import URLError
from _socket import timeout
from THREDDSExplorer.libvisor.providersmanagers.wcs.WCSBatchDownloadUtil import WCSDownloadWorkerThread
from THREDDSExplorer.libvisor.providersmanagers.wms.WMSBatchDownloadUtil import WMSDownloadWorkerThread
from THREDDSExplorer.libvisor.providersmanagers.DownloadWorkerThread import DownloadWorkerThread


class VisorController(QObject):
    """
    Links UI and data from Visor_WMS project.

    This controller connects the main UI with the ServerManager
    controller (See: libvisor.persistence.ServerDataPersistenceManager.py),
    with the animation controller (See: libvisor.animation),
    the ThreddsMapperGeneric component, and the providersmanagers.

    Through its methods the UI can request maps to be downloaded
    as a single entity or in batches, and send the selected MapObject
    to any listeners to its mapInfoRetrieved signal (currently the
    main UI, and the AnimatorFrame animation interface).
    """

    threddsServerMapObjectRetrieved = pyqtSignal(list, str) #Emitted when we have a new list of available base catalogs/datasets from thredds server.
    threddsDataSetUpdated = pyqtSignal(TFR.DataSet) #Emitted when a dataSet/catalog is mapped.
    mapImageRetrieved = pyqtSignal(tuple) #Emitted when a new map layer is available for use.
    mapInfoRetrieved = pyqtSignal(object) #Emitted when a new MapInfo object is selected through this controller
    batchDownloadFinished = pyqtSignal(list, str) #Emitted when a list of layers is downloaded
    standardMessage = pyqtSignal(str)
    errorMessage = pyqtSignal(str)

    def __init__(self):
        super(VisorController, self).__init__()
        self.InfoService = None
        self.serverDataService = None
        self.temporaryDirectoryPath = tempfile.gettempdir()

    def showServerManager(self, parent = None):
        """
        Shows the QDialog assigned to the persistent data
        manager, which currently (only) holds the server
        information.
        """
        self.serverDataService = ServerStorageManager(parent)
        self.serverDataService.serverSelected.connect(self._loadServerDatasets)
        self.serverDataService.show()


    ###                                   ###
    ###Dataset handling related operations###
    ###                                   ###

    def _loadServerDatasets(self, threddsServerInfoObj, depth=0):
        """
        This will be called when a new Thredds Server hast to be
        mapped, and will delegate that operation to a ThreddsMapperGeneric
        object.

        :param     threddsServerInfoObj: Object which contains the URL (and other details)
                                         to the main catalog of the thredds service we want
                                         to map.
        :type    threddsServerInfoObj:   ThreddsServerInfo.ThreddsServerInfoObject

        :param    depth:    The depth of mapping done to the server.
                            If left at -1, a full map will be done.
                            If not, a max of depth steps will be done
                            per dataset found.
        :type     depth:    int
        """
        try:
            serverName = threddsServerInfoObj.getName()
            self.standardMessage.emit("Loading datasets from "+serverName)
            self.InfoService = TFR.ThreddsCatalogInfo(threddsServerInfoObj.getURL(), serverName)
            self.InfoService.threddsServerMapObjectRetrieved.connect(self._onNewDataSetListRetrieved)
            self.asyncQueryDataset(depth)
            self.serverDataService.hide()
        except (HTTPException, URLError, ValueError, timeout):
            self.errorMessage.emit("Error fetching datasets: Server unreachable")


    def asyncQueryDataset(self, depth=0):
        """
        Will request an asynchronous update of the underlying
        data map for the thredds server.

        This process will not generate any return data, but
        that data will (should) be returned through a custom
        QT signal which expects a list of DataSet objects.
        """
        try:
            threading.Thread(target = self._fetchDatasetList, args=(depth,)).start()
        except (HTTPException, URLError, ValueError, timeout):
            self.errorMessage.emit("Error fetching datasets: Server unreachable or corrupt data found.")


    def _fetchDatasetList(self, depth):
        try:
            self.InfoService.fetchAvailableDatasets(depth)
        except (HTTPException, URLError, ValueError, timeout):
            self.errorMessage.emit("Error fetching datasets: URL not found")


    @pyqtSlot(list, str)
    def _onNewDataSetListRetrieved(self, dataSetList, serverName):
        """
        Redirects any signal received about a new available
        datasetlist to any listener registered to our own
        signals.
        """
        self.threddsServerMapObjectRetrieved.emit(dataSetList, serverName)



    def getSingleDataset(self, datasetName):
        """
        finds the main dataset object with the specified
        name.

        This method will not perform recursive lookups.

        :param datasetName: Name of the dataset to retrieve the information from.
        :type datasetName:  str

        :returns:   The requested DataSet tree data, including sub-datasets and
                    available layers..
        :rtype:     threddsFetcherRecursos.DataSet
        """
        returnItem = None
        for dataSet in self.InfoService.getAvailableDatasets():
            if dataSet.getName() == datasetName:
                returnItem = dataSet
                break
        return returnItem

    def mapDataSet(self, dataSetObject, depth=-1):
        """
        Request to map to depth-levels the provided
        dataSet.

        :param projectDataSet:  The DataSet the requested map belongs to.
        :type projectDataSet:   threddsFetcherRecursos.DataSet

        :param depth:           The depth the tree will have.
        :type  depth:           int
        """
        try:
            self.InfoService.fillDataSet(dataSetObject, depth)
            self.threddsDataSetUpdated.emit(dataSetObject)
        except (HTTPException, URLError, ValueError, timeout):
            self.errorMessage.emit("Error fetching datasets: Server unreachable")

    def getMapObject(self, mapName, parentSetName, projectDataSet):
        """
        Will take the requested map name (mapName), the map parent sub set
        name (parentSetName) and the project DataSet object (DataSet) as
        parameters to return a Map object as created by the threddsFetcherRecursos
        class.

        To avoid problems with duplicated names for maps in different sub-sets
        of data within the same project, the parent Set name is required for
        this operation. This way, if we have a "daily" and "Hourly" sub-sets
        of data with the same map (coast_20150210.nc) we will not always retrieve
        the first one found, but the proper one from the project selected.


        :param mapName:         The map we want the data from.
        :type mapName:          threddsFetcherRecursos.Map

        :param parentSetName:   The name of the subDataset the map belongs
                                to.
        :type parentSetName:    threddsFetcherRecursos.Map

        :param projectDataSet:  The DataSet the requested map belongs to.
        :type projectDataSet:   threddsFetcherRecursos.DataSet

        :returns:   Object with all the required information
                    to perform a WMS request for this object.
        :rtype:     threddsFetcherRecursos.Map

        """
        #If the map may belong to the base set...
        if parentSetName is None or parentSetName == projectDataSet.getName():
            mapInfoList = projectDataSet.searchMapsByName(mapName,exactMatch = True)
        #If it doesn't seem to belong to the base set...
        else:
            chosenSet = projectDataSet.searchSubsetsByName(parentSetName, exactMatch = True)
            if(len(chosenSet)>1):
                self.errorMessage.emit("- Set integrity error. Multiple results found for this item.")
                return
            elif(len(chosenSet)==0):
                self.errorMessage.emit("- Set integrity error. No results found for this item.")
                return
            else:
                parentSet = chosenSet[0]
                mapInfoList = parentSet.searchMapsByName(mapName,exactMatch = True)

        if(len(mapInfoList)>1):
                self.errorMessage.emit("Map list integrity error. Multiple results found for this item.")
                return None
        elif(len(mapInfoList)==0):
            #self.errorMessage.emit("Map list integrity error. No results found for this item.")
            return None
        else:
            try:
                #print("emitting from controller... "+str(mapInfoList.values()[0]))
                self.mapInfoRetrieved.emit(mapInfoList.values()[0])
            except IndexError:
                return None




    ###                                ###
    ###WMS retrieval related operations###
    ###                                ###

    def getWMSMapInfo(self, mapObject):
        """
        Retrieves the WMSInfo object available for this map.

        :param mapObject: The map we want the data from.
        :type mapObject:  threddsFetcherRecursos.Map

        :returns:   Object with all the required information
                    to perform a WMS request for this object.
        :rtype:     WmsLayerInfo.WMSMapInfo
        """
        try:
            wmsCatalog = mapObject.getWMS()
            if wmsCatalog is not None:
                WMSreader = WMS.WMSparser(wmsCatalog)
                return WMSreader.getMapInfo()
            else:
                return None
        except (HTTPException,urllib2.URLError, timeout):
            return None


    def _retrieveWMSMapImage(self, threddsMapObject,layerName,styleName,timeRequested):
        """
        Async call to retrieve the image from server.
        Potentially long-running operation to be done
        off the main thread.

        Will post result through the mapImageRetrieved
        signal to any registered listeners.
        """
        #print("_retrieveWMSMapImage"+layerName+"--"+timeRequested+"++"+str(threddsMapObject))
        if threddsMapObject is not None and threddsMapObject.getWMS() is not None:
            self.standardMessage.emit("Downloading '"+layerName+"' [WMS], please wait...")
            lectorWMS = WMS.WMSparser(threddsMapObject.getWMS())
            lectorWMS.createMapLayer(layerName,styleName,timeRequested)
            resultImage = (lectorWMS.getLastCreatedMapLayer(),layerName,"WMS")
            self.mapImageRetrieved.emit(resultImage)

    def asyncFetchWMSImageFile(self, threddsMapObject, layerName, styleName, timeRangeRequested):
        """
        Will perform an async request for the layer to the WMS server,
        and return it to the calling object through the WMSprocessdone
        signal.

        :param threddsMapObject: The map we want the image from.
        :type threddsMapObject:  threddsFetcherRecursos.Map

        :param  coverageName:    name of the coverage to retrieve
        :type coverageName:      str

        :param timeRangeRequested:  time dimension of the maps to be retrieved
        :type timeRangeRequested:   [str]

        :returns: QGIS Raster Layer object through the WMSprocessdone signal.
        :rtype: QgsRasterLayer
        """
        if timeRangeRequested is None or len(timeRangeRequested) ==0:
            threading.Thread(target = self._retrieveWMSMapImage,
             args=(threddsMapObject,layerName,styleName,"")).start()
        elif len(timeRangeRequested) == 1:
            threading.Thread(target = self._retrieveWMSMapImage,
             args=(threddsMapObject,layerName,styleName,timeRangeRequested[0])).start()
        else:
            self.standardMessage.emit("Downloading maps, please wait...")
            wmsBatchWorkerThread = WMSDownloadWorkerThread(
                threddsMapObject.getWMS(),
                timeRangeRequested,
                layerName,
                styleName,
                jobName = threddsMapObject.getName()+"_"+layerName+"_"+styleName)
            thread = threading.Thread(target = wmsBatchWorkerThread.run)
            wmsBatchWorkerThread.WMSprocessdone.connect(self.BatchWorkerThreadDone)
            thread.start()




    ###                                ###
    ###WCS retrieval related operations###
    ###                                ###

    def asyncFetchWCSImageFile(self, threddsMapObject, coverageName, timeRangeRequested):
        """
        Will perform an async request for the layer to the WCS server,
        and return it to the calling object through the WCSProcessdone
        signal.

        :param threddsMapObject: The map we want the image from.
        :type threddsMapObject: threddsFetcherRecursos.Map

        :param  coverageName:  name of the coverage to retrieve
        :type coverageName:    str

        :param timeRangeRequested:  time dimension of the maps to be retrieved
        :type timeRangeRequested:   [str]

        :returns: QGIS Raster Layer object through WCSProcessdone QtSignal.
        :rtype: QgsRasterLayer
        """
        #print("A time!")
        if timeRangeRequested is None or len(timeRangeRequested) ==0:
            #print("0 time!")
            threading.Thread(target = self._retrieveWCSMapImage,
             args=(threddsMapObject,coverageName,"")).start()
        elif len(timeRangeRequested) == 1:
            #print("1 time!")
            threading.Thread(target = self._retrieveWCSMapImage,
             args=(threddsMapObject,coverageName,timeRangeRequested[0])).start()
        else:
            self.standardMessage.emit("Downloading maps, please wait...")
            wcsBatchWorkerThread = WCSDownloadWorkerThread(
                       threddsMapObject.getWCS().getCapabilitiesURL(),
                       timeRangeRequested,
                       coverageName,
                       jobName = threddsMapObject.getName()+"_"+coverageName)
            thread = threading.Thread(target = wcsBatchWorkerThread.run)
            wcsBatchWorkerThread.WCSProcessdone.connect(self.BatchWorkerThreadDone)
            thread.start()


    def _retrieveWCSMapImage(self, threddsMapObject, coverageName, timeRequested):
        """
        Async call to retrieve the image from server.
        Potentially long-running operation to be done
        off the main thread.

        Will post result through the mapImageRetrieved signal
        so it can be processed in main thread.
        """
        #print("_retrieveWCSMapImage"+coverageName+"--"+timeRequested+"++"+str(threddsMapObject))
        if threddsMapObject is not None and threddsMapObject.getWCS() is not None:
            self.standardMessage.emit("Downloading '"+coverageName+"' [WCS], please wait...")
            lectorWCS = WCS.WCSparser(threddsMapObject.getWCS().getCapabilitiesURL())
            resultImage = (lectorWCS.generateLayer(coverageName, timeRequested),coverageName, "WCS")
            self.mapImageRetrieved.emit(resultImage)



    def getWCSCoverages(self, mapObject):
        """
        Retrieves the list of WCS coverages available in this map.

        :param mapObject: The map we want the image from.
        :type mapObject:  threddsFetcherRecursos.Map

        :returns:   All the WCS Coverages available for this map in
                    the THREDDS server.
        :rtype:     list of WCSParser.WCScoverage
        """
        try:
            wcsData = mapObject.getWCS()
            if wcsData is not None:
                wcsCatalog = wcsData.getCapabilitiesURL()
                WCSreader = WCS.WCSparser(wcsCatalog)
                return WCSreader.getAvailableCoverages()
            else:
                return None
        except (HTTPException,urllib2.URLError, timeout):
            return None




    @pyqtSlot(dict, WMSDownloadWorkerThread)
    def BatchWorkerThreadDone(self, layerDictionary, workerObject):
        """
        :param layerDictionary: List of layers and times they represent.
        :type  layerDictionary: dict {time:layer}
        """
        try:
            self.batchDownloadFinished.emit(layerDictionary.values(), workerObject.getJobName())
        except KeyError:
            #Might happen if a thread is cancelled in the last frame download,
            #as it'll already have been queued for removal from the threadsInUse dict
            pass
