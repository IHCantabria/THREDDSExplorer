# -*- coding=utf8 -*-
import xml.etree.ElementTree as ET
from THREDDSExplorer.libvisor.providersmanagers.wms import WmsLayerInfo
import urllib2
import json
import time
import threading
from THREDDSExplorer.libvisor.providersmanagers.BoundingBoxInfo import BoundingBox
from qgis.core import QgsRasterLayer
from qgis.utils import iface
import uuid
from threading import RLock
from PyQt4.Qt import pyqtSignal, QObject

class WMSparser(QObject):
    """
    Parsers to make objects from WMS service based maps.
    
    Due to limits in QGIS API (read: 'Raster Layers' section, last paragraph
    http://docs.qgis.org/testing/en/docs/pyqgis_developer_cookbook/loadlayer.html)
    we have to process the capabilities.xml file ourselves
    to extract all the data about available layers and
    time dimensions for our own use.
    
    """
    
    lock = RLock()
    singleRangeBeginsChecking = pyqtSignal()
    singleRangeChecked = pyqtSignal() #Useful for progress reporting. This is a 'long'
                                        #operation which might make it seem the system
                                        #is blocked while being performed.
    
    def __init__(self, urlXML):
        """
        :param urlXML: Full URL to the capabilities.xml file of this 
                                map.
        :type urlXML:  str
        """
        super(WMSparser, self).__init__()
        self.namespace = '{http://www.opengis.net/wms}'
        self.xlink = '{http://www.w3.org/1999/xlink}'
        self.qgisWMSThack = 'IgnoreGetMapUrl=1&'#IgnoreGetFeatureInfoUrl=1&
        self.baseWMSUrl = (
                        '&crs=EPSG:4326'
                        '&srs=EPSG:4326'
                        '&dpiMode=7'
                        '&format=image/png'
                        '&WIDTH=2048&HEIGHT=2048'
                        '&SERVICE=WMS'
                        '&layers={layer}'
                        '&styles={style}'
                        '&url={url}')
        
        #URL to check the metadata for max and min
        #values in the requested raster. This way,
        #we can customize how it'll be retrieved by
        #setting them in our map request.
        baseResourceURL = urlXML.split("?")
        self.WMSValueRangeCheckURL = (str(baseResourceURL[0]) +
                        '?item=minmax'
                        '&request=GetMetadata'
                        '&crs=EPSG:4326'
                        '&srs=EPSG:4326'
                        '&dpiMode=7'
                        '&WIDTH=2048&HEIGHT=2048'
                        '&layers={layer}'
                        '&BBOX={bbox}'
                        '&TIME={time}' )
        XML = urllib2.urlopen(urlXML).read()
        self.tree = ET.fromstring(XML)
        self.mapInfo = None
        self.mapLayer = None


    def getMapInfoFromCapabilities(self):
        """
        Will create a tree-like object with all the information
        of interest in this WMS service about the map we are
        requesting, using the WmsLayerInfo data models.
        
        The created object follows the following structure:
        
        MapInfo
           |__Name        (Map name)
           |__Url         (Server URL map)
           |__Layers      (Layer list, WMSLayer)
                    |
                    |__Name         (Layer name)
                    |__Title        (Layer title)
                    |__Abstract     (Layer abstract description)
                    |__Times        (Available time dimensions)
                    |__Styles       (Available styles for this layer, WMSStyle)
                                |
                                |__Name     (Style name)
                                |__Abstract (Style abstract description)
                                |__Url      (Style URL)
                                
        """
        
        nombre = self.tree.find('.//{0}Layer/{0}Layer/{0}Title'.format(self.namespace)).text
        getMapAttrib = self.tree.find('.//{0}Capability/{0}Request/{0}GetMap/{0}DCPType/{0}HTTP/{0}Get/{0}OnlineResource'.format(self.namespace)).attrib
        url = getMapAttrib[self.xlink+'href']
        search = self.tree.findall('.//{0}Layer/{0}Layer/{0}Layer'.format(self.namespace))
        self.mapInfo = WmsLayerInfo.WMSMapInfo(nombre, url)
        #('+ Creating mapInfo: '+nombre+'\n'
        #    +'with url: '+url)
        for result in search:
            layerObject = WmsLayerInfo.WMSLayer()
            layerObject.setName(result.find('.//{0}Name'.format(self.namespace)).text)
            layerObject.setTitle(result.find('.//{0}Title'.format(self.namespace)).text)
            layerObject.setAbstract(result.find('.//{0}Abstract'.format(self.namespace)).text)
            BoundingBoxInfo = (result.find('.//{0}BoundingBox'.format(self.namespace))).attrib
            bbObject = BoundingBox()
            bbObject.setCRS(BoundingBoxInfo["CRS"])
            bbObject.setNorth(BoundingBoxInfo["maxy"])
            bbObject.setSouth(BoundingBoxInfo["miny"])
            bbObject.setEast(BoundingBoxInfo["maxx"])
            bbObject.setWest(BoundingBoxInfo["minx"])
            layerObject.setBoundingBoxInfo(bbObject)
            try:
                preFormatTimes = result.find('.//{0}Dimension[@name=\'time\']'.format(self.namespace)).text;
                for entry in preFormatTimes.strip().split(','):
                    layerObject.addTime(entry);
            except AttributeError:
                pass #If this has no time dimension, we ignore it.
            
            styles = result.findall('.//{0}Style'.format(self.namespace))
            for style in styles:
                styleObject = WmsLayerInfo.WMSStyle()
                styleObject.setName(style.find('.//{0}Name'.format(self.namespace)).text)
                styleObject.setAbstract(style.find('.//{0}Abstract'.format(self.namespace)).text)
                tags = style.find('.//{0}LegendURL//{0}OnlineResource'.format(self.namespace)).attrib
                styleObject.setUrl(tags[self.xlink+'href'])
                layerObject.addStyle(styleObject)
            
            self.mapInfo.addLayer(layerObject)
        
    def createMapLayer(self, mapLayerName, layerStyleName, layerTime="", minMaxRange=None):
        """
        Will create a QGIS valid raster layer for the
        parsed map, using the passed parameters to get the
        layer we need, with the requested style, and optionally
        a time dimension.
        The possibility of using WMS-T (Time) is provided by
        a 'hack' (QGIS does not allow it through its WMS provider
        API), taken from Anita Graser's Time Manager (GPL2).
        
        :param mapLayerName:      The name identifier of the coverage we want
                                  to retrieve..
        :type mapLayerName:       str
        
        :param layerStyleName:      The name identifier of the layer style we want
                                    used to paint our layer.
        :type layerStyleName:       str
        
        :param layerTime:   The time dimension we want (optional).
        :type layerTime:    str
        
        :param minMaxRange:   A tuple or list containing the min and max values to 
                              be used in the request of this map. Used for rendering
                              the proper colors. If none or not provided, it will
                              ask the server for the max-min values of this time-defined
                              map and use them instead.
        :type minMaxRange:    list or tuple with floats (min, max)
        
        :returns:   A QGIS-compatible raster layer object with the given parameters.
        :rtype:     QgsRasterLayer
        """
        if self.mapInfo is None:
            self.getMapInfoFromCapabilities()
            
        if minMaxRange == None:
            minMaxRange = self.getMinMaxRasterValuesFromTimeRange(mapLayerName, layerStyleName, [layerTime])
            
        rasterMinMaxValues = str(minMaxRange[0])+","+str(minMaxRange[1])
        #print("Raster range for "+mapLayerName+"_"+layerStyleName+": "+rasterMinMaxValues)
        
        finalUrl = self.baseWMSUrl.format(layer=mapLayerName, 
                        style=layerStyleName,
                        url=self.mapInfo.getURL())
        
        #We add an UUID to guarantee uniqueness in the layer name and id
        layerName = self.mapInfo.getName()+"-"+str(uuid.uuid4())
        resultLayer = QgsRasterLayer(finalUrl, layerName, 'wms')
        
        #HACK taken from Anita Graser's Time Manager:
        #https://github.com/anitagraser/TimeManager/blob/master/raster/wmstlayer.py
        #(Under GPL2 license) with an extra added for COLORSCALERANGE ncWMS attribute.
        resultLayer.dataProvider().setDataSourceUri(self.qgisWMSThack
                                                    + resultLayer.dataProvider().dataSourceUri() 
                                                    + "?TIME={time}%26COLORSCALERANGE={scale}"
                                                        .format(time = layerTime, scale=rasterMinMaxValues))
        

        
        if resultLayer.isValid():
            self.mapLayer = resultLayer
        else:
            raise StandardError('No se pudo crear una capa válida.')
    
    def getMapInfo(self):
        """
        Retrieves our cached map information object
        or creates it anew if null.
        """
        if self.mapInfo is None:
            self.getMapInfoFromCapabilities()
        
        return self.mapInfo
        
    def getLastCreatedMapLayer(self):
        """
        Retrieves the last created layer in this object.
        """
        return self.mapLayer;
    
    def getMinMaxRasterValuesFromTimeRange(self, mapLayerName, layerStyleName, listOfTimes):
        """
        Returns a tuple of the (minimum, maximum) values for
        this raster. Useful if we want to create a coherent
        legend for an animation or between a number of different
        times for the same area.
        """
        #We retrieve the bounding box data to be sent with the 
        #request to find the min/max range values for the raster.
        if self.mapInfo == None:
            self.getMapInfoFromCapabilities()
            
        boundingBoxData = ([x.getBoundingBoxInfo() for x in self.mapInfo.getLayers() 
                                if x.getName() == mapLayerName])[0]
                               
        threads = []
         
        for moment in listOfTimes:
            #print("BATCH RANGES CALCULATOR: "+str(moment)+" at system time "+str(datetime.datetime.now()))
            while len([x for x in threads if x.isAlive() == True]) > 4:
                time.sleep(0.2)
            self.singleRangeBeginsChecking.emit()
            pathForJSON = self.WMSValueRangeCheckURL.format(
                          layer=mapLayerName,
                          style=layerStyleName,
                          bbox=boundingBoxData.getWest()+','+boundingBoxData.getSouth()
                                +','+boundingBoxData.getEast()+','+boundingBoxData.getNorth(),
                          time = moment)
            thread = threading.Thread(target = self._getRangeValuesFromJSONPath, args=(pathForJSON,))
            threads.append(thread)
            thread.start()
        
        try:
            while len([x for x in threads if x.isAlive() == True]) != 0:
                time.sleep(0.2)
            
            #print(str(self.minRange) +"_"+ str(self.maxRange))
            return (self.minRange, self.maxRange)
        except (NameError, AttributeError):
            return None
    
    def _getRangeValuesFromJSONPath(self, jsonPath):
            #print("CALCULATING RANGE: "+jsonPath+" at system time "+str(datetime.datetime.now()))
            jsonRawData = urllib2.urlopen(jsonPath)
            jsonObject = json.load(jsonRawData)
            newMin = jsonObject["min"]
            newMax = jsonObject["max"]
            self.checkAgainstRanges(newMin, newMax)
            #print("RANGE CALCULATED: "+jsonPath+" at system time "+str(datetime.datetime.now()))
            self.singleRangeChecked.emit()
        
    def checkAgainstRanges(self, newMin, newMax):
        with self.lock:
            #print(">> CHECKING RANGE"+str(newMin)+"_"+str(newMax)+" at system time "+str(datetime.datetime.now()))
            try:
                if self.maxRange < newMax:
                    self.maxRange = newMax
            except (NameError, AttributeError):
                self.maxRange = newMax
            
            try:
                if self.minRange < newMin:
                    self.minRange = newMin
            except (NameError, AttributeError):
                self.minRange = newMin
                
            #print(">> CHECKED RANGE"+str(newMin)+"_"+str(newMax)+" at system time "+str(datetime.datetime.now()))
            
        