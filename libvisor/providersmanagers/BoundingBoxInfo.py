'''
Created on 18 de ene. de 2016

@author: IHC
'''

class BoundingBox(object):
    def __init__(self):
        self.data = {}
        self.data["north"] = None
        self.data["south"] = None
        self.data["east"] = None
        self.data["west"] = None
        self.data["crs"] = None
        
    def __str__(self):
        return str(self.getWest())+","\
            +str(self.getSouth())+","\
            +str(self.getEast())+","\
            +str(self.getNorth())
        
    def setNorth(self, northBound):
        self.data["north"] = northBound
        
    def setSouth(self, southBound):
        self.data["south"] = southBound
        
    def setEast(self, eastBound):
        self.data["east"] = eastBound
        
    def setWest(self, westBound):
        self.data["west"] = westBound
        
    def setCRS(self, crs):
        self.data["crs"] = crs
        
    def getNorth(self):
        return self.data["north"]
        
    def getSouth(self):
        return self.data["south"]
        
    def getEast(self):
        return self.data["east"]
        
    def getWest(self):
        return self.data["west"]
        
    def getCRS(self):
        return self.data["crs"]