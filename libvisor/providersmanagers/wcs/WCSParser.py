# -*- coding=utf8 -*-
import urllib2
import xml.etree.ElementTree as ET
from THREDDSExplorer.libvisor.providersmanagers.BoundingBoxInfo import BoundingBox
from qgis.core import QgsRasterLayer
import uuid

class WCScoverage(object):
	"""
	Base model to store WCS coverage information.
	
	It includes the coverage name and time dimensions
	available for it.
	"""
	def __init__(self, nombre, listaTiemposDisponibles, boundingBox = None):
		"""
		:param nombre: 		The name this coverage is identified by.
        :type nombre: 		str
        
        :param  listaTiemposDisponibles:  Available time dimension values.
        :type listaTiemposDisponibles:    list of str
        
        :param boundingBox:	Bounding box and CRS information encapsulated as
        					an object.
		:type  boundingBox: BoundingBoxInfo.BoundingBox
		"""
		self.nombre = nombre
		self.listaTiemposDisponibles = listaTiemposDisponibles
	
	def getName(self):
		return self.nombre
	
	def getTiempos(self):
		return self.listaTiemposDisponibles
	
	def setBoundingBoxInfo(self, boundingBoxObject):
		self.bbox = boundingBoxObject
		
	def getBoundingBoxInfo(self):
		return self.bbox
	
class WCSparser(object):
	"""
	Parses information from WCS services and creates objects which 
	ease any operations we need to do with them.
	"""
	def __init__(self, URLcapabilities):
		"""
		:param URLcapabilities: Full URL to the capabilities.xml file of this 
								map.
        :type URLcapabilities: 	str
		"""
		self.availableCoverages = None
		self.URLcapabilities = URLcapabilities
		self.namespace = "{http://www.opengis.net/wcs}"
		self.gml="{http://www.opengis.net/gml}"
		urlBase = self.URLcapabilities.partition('?')[0] #Nos quedamos con la parte de URL
		self.urlDescribeCoverage = (urlBase + '?' 
		                            + 'service=WCS'
		                            + '&version=1.0.0'
		                            + '&request=DescribeCoverage')
		self.urlGetCoverage = (urlBase + '?' 
		                            + 'service=WCS'
		                            + '&version=1.0.0'
		                            + '&request=GetCoverage'
		                            + '&coverage={coverageName}'
		                            + '&TIME={timeCode}'
		                            + '&format=GeoTIFF')
	
	def getAvailableCoverages(self):
		"""
		Returns the cached coverage information for this map, or if
		not yet read, creates a new list of coverages and caches it
		for next uses.
		
		:returns: 	List of available coverages for this map, as published
					in the capabilities.xml file.
        :rtype: 	list of WCScoverage
		"""
		if self.availableCoverages is None:
			self.__extractCoverages()
			
		return self.availableCoverages
	
	def generateURLForGeoTIFF(self, nameCoverage, coverageTime):
		"""
		Generates a direct download URL for a GeoTiff formatted image
		for the map cached in this object, using the coverage and
		time provided to this method.
		
		
		:param nameCoverage: 		The name identifier of the coverage we want
									to retrieve..
        :type nameCoverage: 		str
        
        :param codTiempoCoverage: 	The time dimension of the coverage we want.
        :type codTiempoCoverage: 	str
		
		:returns: 	A direct URL link which we can download a GeoTIFF
					image from, using the given details.
        :rtype: 	str
		"""
		return self.urlGetCoverage.format(coverageName = nameCoverage, 
		    timeCode = coverageTime)
		
		
	def generateLayer(self, nameCoverage, coverageTime):
		"""
		Generates a raster layer for QGIS. 
		
		:param nameCoverage:      The name identifier of the coverage we want
		                            to retrieve..
		:type nameCoverage:       str
		
		:param coverageTime:   The time dimension of the coverage we want.
		:type coverageTime:    str
		
		:returns:   A QGIS-compatible raster layer object for the coverage and
		            times provided.
		:rtype:     QgsRasterLayer
		"""
		url = self.generateURLForGeoTIFF(nameCoverage , coverageTime)
		
		layerName = coverageTime+"_"+nameCoverage+"-"+str(uuid.uuid4())
		layer = QgsRasterLayer(url, layerName)
		
		if layer.isValid:
			return layer
		else:
			raise StandardError('Couldn\'t create a valid layer.')
		
	def generateLayerFromGeoTIFFURL(self, geoTiffUrl, layerName):
		"""
		Generates a new layer based on the GeoTIFF URL provided
		for the WCS service.
		This method also appends to the name an UUID so the uniqueness
		of it's name and ID is guaranteed to avoid problems when
		managing asynchronous generation of layers between different
		processes.
		
		:param geoTiffUrl:      The download URL for this image.
		:type  geoTiffUrl:       str
		
		:param layerName:   The name to give to this layer. The resultant layer
							will have an UUID appended.
		:type  layerName:    str
		
		"""
		layer = QgsRasterLayer(geoTiffUrl, layerName + str(uuid.uuid4()))
		if layer.isValid:
			return layer
		else:
			raise StandardError('Couldn\'t create a valid layer.')
		
		
	def __extractCoverages(self):
		"""
    	Extracts all the coverages published in the capabilities file, 
    	and stores them in this object.
    	"""
		self.availableCoverages = []
		page = urllib2.urlopen(self.urlDescribeCoverage)
		string = page.read()
		xml = ET.fromstring(string)
		treeCoverages = ET.ElementTree(xml)
		rootCoverages = treeCoverages.getroot()
		
		coveragesOffered = rootCoverages.findall('.//{0}CoverageOffering'.format(self.namespace))
		for coverage in coveragesOffered:
			
			nombreCoverage = coverage.find('.//{0}name'.format(self.namespace)).text
			coverageTimes = []
			elementsTiempos = coverage.findall('.//{0}domainSet//{0}temporalDomain//{1}timePosition'.format(self.namespace, self.gml))
			for item in elementsTiempos:
				coverageTimes.append(item.text)
			coverageObject = WCScoverage(nombreCoverage, coverageTimes)
			
			crs = (coverage.find('.//{0}lonLatEnvelope'.format(self.namespace)).attrib)["srsName"]	
			bbElements = coverage.findall('.//{0}lonLatEnvelope//{1}pos'.format(self.namespace, self.gml))
			#We will retrieve two gml:pos elements here. The first one will contain
			#the west and south elements separated by a blank space, and the second
			#one will contain the east and north ones, also separated by a blank space,
			#and in this order.
			west_south = (bbElements[0].text).split(" ")
			east_north = (bbElements[1].text).split(" ")
			boundingBox = BoundingBox()
			boundingBox.setCRS(crs)
			boundingBox.setEast(east_north[0])
			boundingBox.setWest(west_south[0])
			boundingBox.setNorth(east_north[1])
			boundingBox.setSouth(west_south[1])
			
			coverageObject.setBoundingBoxInfo(boundingBox)
			self.availableCoverages.append(coverageObject)
			
			
			
			
			
			