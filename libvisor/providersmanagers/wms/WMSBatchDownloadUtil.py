'''
Created on 28 de mar. de 2016

@author: IHC
'''
from PyQt4.QtCore import pyqtSignal, Qt
from THREDDSExplorer.libvisor.providersmanagers.wms.WMSParser import WMSparser
from datetime import datetime
from THREDDSExplorer.libvisor.animation.Animation2 import AnimationData
from THREDDSExplorer.libvisor.animation.AnimationLayer import AnimationLayer
from THREDDSExplorer.libvisor.providersmanagers.DownloadWorkerThread import DownloadWorkerThread

class WMSDownloadWorkerThread(DownloadWorkerThread):
    """
    Handles the download of multiple WCS objects.
    
    Through calling asynchronously its run() method, it can be
    run on the background and signals will notify of any progress
    update, success or failure for the operation.
    
    """
    # Custom signal which must return as first paramete, 
    # a dictionary with time:layer format, 
    # and a reference to itself as second parameter.
    WMSprocessdone = pyqtSignal(dict, DownloadWorkerThread) 
    WMSFrameStartsDownload = pyqtSignal()
    WMSFrameFinishedDownload = pyqtSignal()
    WMSSingleValueRangeProcessed = pyqtSignal()
    WMSMapDownloadFail = pyqtSignal(int, str)
    
    def __init__(self, capabilitiesURL, times, layerName, style, bbox, parent = None, jobName = None):
        """
        :param capabilitiesURL:     The URL to the capabilities.xml file for this map.
        :type  capabilitiesURL:     str
        
        :param times:     List of times to request maps from.
        :type  times:     [str]
        
        :param layerName: Name of the layer we must request.
        :type  layerName: str
        
        :param jobName: Identifier string for this work thread (optional)
        :type  jobName: str
        """
        super(WMSDownloadWorkerThread, self).__init__(parent)
        
        if jobName is None:
            jobName = layerName+"_"+style+"_"+str(len(times))
            
        DownloadWorkerThread.setJobName(self, jobName)
        
        self.failedDownloads = 0
        self.capabilitiesURL = capabilitiesURL
        self.times = times
        self.layerName = layerName
        self.bbox = bbox
        self.style = style
        self.cancel = False
        self.parser = WMSparser(self.capabilitiesURL)
        self.inTimeFormat = "%Y-%m-%dT%H:%M:%SZ"
        self.outTimeFormat = "%Y-%m-%d %H:%M:%S"
        self.selfReference = self #Self reference is not accurate from method run() due to some strange issues
                                    #when being called synchronously.
        
        
        #We do not care (right now) in which phase of this check we are.
        #We just want their signals to update our progress status.
        self.parser.singleRangeChecked.connect(self.WMSSingleValueRangeProcessed.emit, Qt.DirectConnection)
        #self.parser.singleRangeBeginsChecking.connect(self.WMSSingleValueRangeProcessed.emit, Qt.DirectConnection)
        
    def getLayerDict(self):
        return super(WMSDownloadWorkerThread, self).getLayerDict()    
        
    def getJobName(self):
        """
        Returns an automatically generated, human-readable
        name for this batch work.
        """
        return super(WMSDownloadWorkerThread, self).getJobName()
        
    def requestCancellation(self):
        self.cancel = True
        
    def run(self):
        #First, we will calculate the min and max values for this map in all
        #the instants we want to retrieve, to make a coherent color palette
        #so each color will represent the same values range across all the frames.
        valuesRange = self.parser.getMinMaxRasterValuesFromTimeRange(self.layerName, self.style,
                                                                      self.times, self.bbox)
        times = [x.replace(".000","") for x in self.times]
        for moment in times:
            if self.cancel == True:
                return
            self.WMSFrameStartsDownload.emit()
            self.parser.createMapLayer(self.layerName, self.style, self.bbox,
                                        layerTime = moment, minMaxRange = valuesRange)
            layer = self.parser.getLastCreatedMapLayer()
            if layer is not None and layer.isValid() == True:
                #outputFormattedTime = (datetime.strptime(moment, self.inTimeFormat))\
                #                            .strftime(self.outTimeFormat)
                (self.getLayerDict())[datetime.strptime(moment, self.inTimeFormat)] = \
                                (self.parser.getLastCreatedMapLayer())
            else:
                #If the layer couldn't be properly retrieved, we will reduce by one
                #the number of layers we expect to group.
                self.failedDownloads = self.failedDownloads + 1
                
            self.WMSFrameFinishedDownload.emit()
        if self.failedDownloads > 0:
            self.WMSMapDownloadFail.emit(self.failedDownloads, self.layerName)
            
        self.WMSprocessdone.emit(self.getLayerDict(), self.selfReference)
        
