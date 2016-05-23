class WMSMapInfo(object):
    def __init__(self, name, URL):
        self.name = name
        self.layerListForMap = []
        self.URL = URL
    
    def getName(self):
        return self.name
        
    def getLayers(self):
        return self.layerListForMap
        
    def addLayer(self, layer):
        self.layerListForMap.append(layer)
        
    def getURL(self):
        return self.URL
        


class WMSLayer(object):
    
    def setName(self, name):
        self.name = name
        
    def setTitle(self, title):
        self.title = title
        
    def setAbstract(self, abstract):
        self.abstract = abstract
        
    def setBoundingBoxInfo(self, bboxInfo):
        """
        :type    bboxInfo:    BoundingBox
        """
        self.bboxInfo = bboxInfo
    
    def addStyle(self, style):
        try: 
            self.styles
        except: 
            self.styles = []
            
        self.styles.append(style)
        
    def addTime(self, time):
        try:
            self.times
        except AttributeError:
            self.times = []
        self.times.append(time)
        
        
    def getName(self):
        return self.name
        
    def getAbstract(self):
        return self.abstract
    
    def getStyles(self):
        return self.styles
    
    def getTimes(self):
        try:
            return self.times
        except AttributeError:
            self.times = []
            return self.times
    
    def getBoundingBoxInfo(self):
        return self.bboxInfo
    
        
        
        
class WMSStyle(object):
    
    def setName(self, name):
        self.name = name
        
    def setAbstract(self, abstract):
        self.abstract = abstract
        
    def setUrl(self, url):
            self.url = url
        
        
    def getName(self):
        return self.name
        
    def getAbstract(self):
        return self.abstract
        
    def getUrl(self):
            return self.url