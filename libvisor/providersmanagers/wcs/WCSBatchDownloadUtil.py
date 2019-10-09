'''
Created on 28 de mar. de 2016

@author: IHC
'''
from PyQt5.QtCore import pyqtSignal
from .WCSParser import WCSparser
from datetime import datetime
from ..DownloadWorkerThread import DownloadWorkerThread


class WCSDownloadWorkerThread(DownloadWorkerThread):
    """
    Handles the download of multiple WCS objects.
    
    Through calling asynchronously its run() method, it can be
    run on the background and signals will notify of any progress
    update, success or failure for the operation.
    """
    # Custom signal which must return as first parameter, 
    # a dictionary with time:layer as second, 
    # the third is a reference to itself.
    WCSProcessdone = pyqtSignal(dict, DownloadWorkerThread) 
    WCSFrameStartsDownload = pyqtSignal()
    WCSFrameFinishedDownload = pyqtSignal()
    WCSMapDownloadFail = pyqtSignal(int, str)

    def __init__(self, capabilitiesURL, times, layerName,
                 boundingBox, parent = None, jobName = None):
        """
        :param capabilitiesURL:     The URL to the capabilities.xml file for this map.
        :type  capabilitiesURL:     str
        
        :param times:     List of times to request maps from.
        :type  times:     [str]
        
        :param layerName: Name of the layer we must request.
        :type  layerName: str
        
        :param boundingBox: Bounding box extent to be requested
        :type  boundingBox: BoundingBox
        
        :param jobName: Identifier string for this work thread (optional)
        :type  jobName: str
        """
        super(WCSDownloadWorkerThread, self).__init__(parent)
        
        if jobName is None:
            jobName = layerName+"_"+str(len(times))
            
        DownloadWorkerThread.setJobName(self, jobName)
        
        self.failedDownloads = 0
        self.capabilitiesURL = capabilitiesURL
        self.times = times
        self.layerName = layerName
        self.boundingBox = boundingBox
        self.cancel = False
        self.inTimeFormat = "%Y-%m-%dT%H:%M:%SZ"
        self.outTimeFormat = "%Y-%m-%d %H:%M:%S"
        self.selfReference = self #Self reference is not accurate from method run() due to some strange issues
                                    #when being called asynchronously.
        
    def requestCancellation(self):
        self.cancel = True
        
    def getLayerDict(self):
        return super(WCSDownloadWorkerThread, self).getLayerDict()    
        
    def getJobName(self):
        """
        Returns an automatically generated, human-readable
        name for this batch work.
        """
        return super(WCSDownloadWorkerThread, self).getJobName()
        
    def run(self):
        parser = WCSparser(self.capabilitiesURL)
        for moment in self.times:
            if self.cancel == True:
                return
            
            self.WCSFrameStartsDownload.emit()
            mapDownloadURL = parser.generateURLForGeoTIFF(self.layerName, moment, self.boundingBox)
            layer = parser.generateLayerFromGeoTIFFURL(mapDownloadURL, moment+"_"+self.layerName)
            if layer is not None and layer.isValid() == True:
                #outputFormattedTime = (datetime.strptime(moment, self.inTimeFormat))\
                #                            .strftime(self.outTimeFormat)
                (self.getLayerDict())[datetime.strptime(moment, self.inTimeFormat)] = (layer)
            else:
                #If the layer couldn't be properly retrieved, we will reduce by one
                #the number of layers we expect to group.
                self.failedDownloads = self.failedDownloads + 1
            
            self.WCSFrameFinishedDownload.emit()
        if self.failedDownloads > 0:
            self.WCSMapDownloadFail.emit(self.failedDownloads, self.layerName)
                
        self.WCSProcessdone.emit(self.getLayerDict(), self.selfReference)