'''
Created on 13 de abr. de 2016

@author: IHC
'''
from PyQt4.QtCore import QObject

class DownloadWorkerThread(QObject):
    '''
    Base class for download worker threads with common attributes.
    
    TODO: Signals should be declared here, as should a 
    template run() method. This is not an issue in itself,
    but would help when implementing new inheriting classes.
    '''


    def __init__(self, parent):
        '''
        Constructor
        '''
        super(DownloadWorkerThread, self).__init__(parent)
        self.jobName = ""
        self.layerDict = {}
    
    
    def setJobName(self, jobName):
        self.jobName = jobName
        
    def getJobName(self):
        return self.jobName
    
    def getLayerDict(self):
        """
        Be advised, this object will be empty on first
        retrieval, and should later be populated by 
        overriding classes.
        """
        return self.layerDict