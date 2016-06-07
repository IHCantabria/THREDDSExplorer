# -*- coding=utf8 -*-
import urllib2
import xml.etree.ElementTree as ET
import threading
import time
from THREDDSExplorer.libvisor.utilities.Utilities import combineURLS
from PyQt4.QtCore import pyqtSignal, QObject
from httplib import HTTPException
from urllib2 import URLError
from qgis.core import QgsMessageLog
import traceback

class Map(object):
    """
    Model for any maps found in the thredds server.

    This object holds information for the map name, WMS
    capabilities.xml full path, and a WCSinfo object
    holding both the capabilities.xml URL and the
    coverage information path (this last path is not,
    as of now, strictly required).
    """
    def __init__(self, name, WMS, WCS):
        """
        :param    nombre:    Name of this map object.
        :type     nombre:    str

        :param    WMS:       Full path to WMS capabilities.xml file.
        :type     WMS:       str

        :param    WCS:       Name of this map object.
        :type     WCS:       Map.WCSinfo
        """
        self.name = name
        self.WMS = WMS
        self.WCS = WCS

    def getName(self):
        return self.name
    def getWMS(self):
        return self.WMS
    def getWCS(self):
        return self.WCS

    class WCSinfo(object):
        """
        Container for WCS access information for a single map.
        """
        namespace = '{http://www.opengis.net/wcs}'
        xlink = '{http://www.w3.org/1999/xlink}'

        def __init__(self, URLcapabilities):
            self.URLcapabilities = URLcapabilities
            self._generateCoverageURL()

        def getCoverageURL(self):
            return self.URLcoverage

        def getCapabilitiesURL(self):
            return self.URLcapabilities

        def setCapabilitiesURL(self, newCapabilitiesURL):
            self.URLcapabilities = newCapabilitiesURL
            self._generateCoverageURL()

        def _generateCoverageURL(self):
            urlBase = self.URLcapabilities.partition('?')[0]
            self.URLcoverage = (urlBase + '?'
                                    + 'service=WCS'
                                    + '&version=1.0.0'
                                    + '&request=DescribeCoverage')


class DataSet(object):
    """
    Model object to hold information about
    a thredds based data set or catalog.

    It is a tree structure, which can be followed
    both ways, and will hold child datasets and
    maps, plus any required information to access
    the reported services.
    """

    """
    :param url     full URL to this dataset
    :type  url     String

    :param parent  Dataset to which this set belongs.
    :type parent   DataSet
    """
    def __init__(self, name, url, parent = None):
        self.name = name
        self.url = url
        self.subDataset = []
        self.mapList = []
        self.parent = parent

    def __str__(self):
        string = 'DataSet '+self.name +'\nURL: '+self.url
        if len(self.mapList) > 0:
            string += '\n + Available maps:\n'
            for mapa in self.mapList:
                string += '    - ' + mapa.getName() + '\n'

        if len(self.subDataset) > 0:
            string += '\n + Available sub-datasets: \n'
            for element in self.subDataset:
                subString = str(element)
                newString = ''
                for line in subString.split('\n'):
                    newString += '     ' + line +'\n'
                string += newString

        return string


    def getName(self):
        return self.name

    def getParent(self):
        return self.parent
    def getMainCatalogURL(self):
        return self.url

    def getAvailableMapList(self):
        return self.mapList

    def addSubSet(self, dataset):
        """
        Appends a single dataSet as a children to this one.
        """
        self.subDataset.append(dataset)

    def getSubSets(self):
        return self.subDataset

    def addMap(self, mapa):
        self.mapList.append(mapa)

    def searchMapsByName(self, stringToFind, exactMatch = False, recursive = True):
        """
        Returns a list of maps found within this set,
        which contain the specified text in their name or whose
        names are equal to the provided parameter.
        (case insensitive)
        """
        resultado = {}
        for mapa in self.mapList:
            match = False
            if (exactMatch == False):
                match = (stringToFind.lower() in mapa.getName().lower())
            elif(exactMatch == True ):
                match = (stringToFind.lower() == mapa.getName().lower())
            if(match):
                resultado[mapa.getName()] = mapa
        if recursive is True:
            for subSet in self.subDataset:
                resultado.update(subSet.searchMapsByName(stringToFind, exactMatch, recursive))
        return resultado

    def searchSubsetsByName(self, criterioBusqueda, exactMatch = False, recursive = True):
        """
        Returns a list of sub data sets found within this set,
        which contain the specified text in their name or whose
        names are equal to the provided parameter.
        (case insensitive)
        """
        resultado = []

        match = False
        for subSet in self.subDataset:
            match = False
            if (exactMatch == False):
                match = (criterioBusqueda.lower() in subSet.getName().lower())
            elif(exactMatch == True ):
                match = (criterioBusqueda == subSet.getName())
            if(match):
                resultado.append(subSet)

            if recursive is True:
                resultado.extend(subSet.searchSubsetsByName(criterioBusqueda, exactMatch, recursive))

        return resultado

class ThreddsCatalogInfo(QObject):
    """
    Maps thredds-based data sets.

    It will return a DataSet object type, which will
    contain both child dataSets within them and any
    maps found. These maps include information
    about their names, and capabilities.xml file
    routes.
    """

    threddsServerMapObjectRetrieved = pyqtSignal(list, str)
    singleDataSetMapComplete = pyqtSignal(DataSet) #Emitted every time a new DataSet is mapped completely.


    def __init__(self, threddsMainCatalog, serverUserReadableName="No server name specified"):
        """

        :param    threddsMainCatalog:    Full path to this thredds server main catalog.xml
                                         file
        :type     threddsMainCatalog:    str

        :param    serverUserReadableName:    A server name useful for the user.
        :type     serverUserReadableName:    str

        """
        super(ThreddsCatalogInfo, self).__init__()
        self.namespace = '{http://www.unidata.ucar.edu/namespaces/thredds/InvCatalog/v1.0}'
        self.xlink = '{http://www.w3.org/1999/xlink}'
        self.threddsMainCatalog = threddsMainCatalog.rstrip(r'/')
        self.threddsCatalogFileName = 'catalog.xml'
        self.AvailableDataSetList = []
        self.NetworkRequestTimeout = 20
        self.maxDownloadThreadsPerSet = 80
        self.serverName = serverUserReadableName

    def setThreddsMainCatalog(self, threddsMainCatalog):
        self.threddsMainCatalog = threddsMainCatalog


    def getServerName(self):
        return self.serverName


    def fetchAvailableDatasets(self, depth = -1):
        """
        Will parse all the dataSet info from the URL
        this object points to, and return once it's completely
        mapped.

        The mapping is done through threads, one per available set.

        A signal will be emitted when this process is finished.

        :param    depth:    The depth of mapping done to the server.
                            If left at -1, a full map will be done.
                            If not, a max of depth steps will be done
                            per dataset found.
        :type     depth:    int
        """
        try:
            page = urllib2.urlopen(self.threddsMainCatalog+r'/'+self.threddsCatalogFileName,
                                timeout=self.NetworkRequestTimeout)
        except (HTTPException, URLError, ValueError) as e:
            QgsMessageLog.logMessage(traceback.format_exc(), "THREDDS Explorer", QgsMessageLog.CRITICAL )
            raise e

        string = page.read()
        xml = ET.fromstring(string)
        tree = ET.ElementTree(xml)
        root = tree.getroot()
        dataSets = root.findall('.//{0}catalogRef'.format(self.namespace))
        self.AvailableDataSetList = []
        asyncProcesses = []

        for item in dataSets:
            nombre = item.attrib['{0}title'.format(self.xlink)]
            url = item.attrib[self.xlink+'href']
            asyncProcess = threading.Thread(target = self._startBaseSetCreation,
                                           args=(nombre,url, depth), name=nombre)
            asyncProcesses.append(asyncProcess)


        for item in asyncProcesses:
            aliveThreads = {x for x in asyncProcesses if x.is_alive() == True }
            while(len(aliveThreads) > self.maxDownloadThreadsPerSet): #We limit the amount of concurrent threads.
                aliveThreads = {x for x in asyncProcesses if x.is_alive() == True }
                time.sleep(0.5)
            item.start()

        #Workaround. For some reasons, joining the threads cause QGIS to
        #break and die.
        while len(aliveThreads) > 0:
            time.sleep(0.5)
            aliveThreads = {x for x in asyncProcesses if x.is_alive() == True }

        asyncProcesses = None
        self.threddsServerMapObjectRetrieved.emit(self.AvailableDataSetList, self.serverName)




    def _startBaseSetCreation(self, name, url, depth = -1):
        """
        Should be called asynchronously.

        Will create a base DataSet, which will be added to this
        object available dataset list, and call fillDataSet on it.

        It should be called asynchronously to speed-up this process.

        :param name     DataSet base name.
        :type name      String

        :param url      Base URL to the resource
        :type url       String

        :param    depth:    The depth of mapping done to the server.
                            If left at -1, a full map will be done.
                            If not, a max of depth steps will be done
                            per dataset found.
        :type     depth:    int

        """
        try:
            dataset = DataSet(name, url)
            self.fillDataSet(dataset, depth)
            self.AvailableDataSetList.append(dataset)
        except Exception:
            pass #We can not do much at this point.

    def _asyncFillDataSet(self, dataSet, depth=-1):
        """
        Look at: fillDataSet()

        This is a function to be called in another thread by that
        one so any network operations are done off the main thread.
        """
        url = self.translateCatalogURL(dataSet.getMainCatalogURL())

        try:
            page = urllib2.urlopen(url, timeout=self.NetworkRequestTimeout)
        except Exception as e:
            QgsMessageLog.logMessage(traceback.format_exc(), "THREDDS Explorer", QgsMessageLog.CRITICAL )
            raise e

        string = page.read()
        xml = ET.fromstring(string)
        tree = ET.ElementTree(xml)
        root = tree.getroot()


        #Si no hay catalogRefs, nos encontramos en un directorio
        #con 'mapas'. Si hay catalogRefs, es un subcatálogo..
        subDataSets = root.findall('.//{0}catalogRef'.format(self.namespace))
        if(len(subDataSets) > 0):
            for item in subDataSets:
                try:
                    nombre = item.attrib['ID']
                except KeyError:
                    nombre = item.attrib[self.xlink+'title']

                #We will look for any attribute which MAY be an URL..
                #... this means, which contains a slash.
                attribute = None
                for att in item.attrib:
                    if '/' in att:
                        attribute = att
                        break
                subUrl = self.translateCatalogURL(item.attrib[attribute], parentCatalogURL=url) #url is parent URL





                #IF this subset is already assigned to this dataSet
                #as a subcatalog, we will not add it again. If we do not
                #perform this check, and we try to re-map an already mapped
                #dataset, we will end up duplicating entries for subsets.
                subcatalogSearchResult = (dataSet.searchSubsetsByName(
                                               nombre, exactMatch = True, recursive = False))
                alreadySubcatalogOfDataset = len(subcatalogSearchResult) > 0
                if alreadySubcatalogOfDataset is False:
                    subSet = DataSet(nombre, subUrl, parent=dataSet)
                    dataSet.addSubSet(subSet)
                else:
                    subSet = subcatalogSearchResult[0]

                #Rationale for when I forget: We are substracting one per step,
                #thus if negative (default for whole server map) we won't find a zero...
                if depth is not 0:
                    self.fillDataSet(subSet, depth-1)



        mapas = root.findall('.//{0}dataset//{0}dataset'.format(self.namespace))
        if(len(mapas)>0):
            #First, we get the url for the WMS/WCS servers of this
            #dataset...
            try:
                wcsService = (root
                              .findall('.//{0}service//{0}service[@serviceType=\"WCS\"]'
                                       .format(self.namespace))[0]).attrib['base']
            except Exception:
                wcsService = None

            try:
                wmsService = (root
                              .findall('.//{0}service//{0}service[@serviceType=\"WMS\"]'
                                       .format(self.namespace))[0]).attrib['base']
            except Exception:
                wmsService = None

            #If the server does not provide access to any of the services
            #we support, we return right here.
            if wcsService is None and wmsService is None:
                return

            for item in mapas:
                nombre = item.attrib['name']


                #IF this map is already assigned to this dataSet
                #we will not add it again. If we do not perform this check,
                #and we try to re-map an already mapped
                #dataset, we will end up duplicating entries for each map.
                alreadyBelongsToDataset = (len(dataSet.searchMapsByName(
                                               nombre, exactMatch = True, recursive = False)) > 0)
                if alreadyBelongsToDataset is True:
                    continue



                try:
                    itemFinalPath = item.attrib['urlPath']
                except Exception:
                    itemFinalPath = nombre #We try.. just in case.. you know.. it works.

                if '.xml' in nombre or '.xml' in itemFinalPath:
                    continue

                #If WMS is supported by the server, we attempt to map it's access url
                rutaWMS = None
                if wmsService is not None:
                    #We first combine the base URL of this dataSet with the one which points
                    #to the service..
                    rutaWMS = (combineURLS(url.replace('catalog.xml',''), wmsService))
                    #And then combine the previous URL which points to the service with the
                    #one pointing to the resource, appending the request string.
                    rutaWMS = (combineURLS(rutaWMS, itemFinalPath)
                                + '?service=WMS&version=1.3.0&request=GetCapabilities')

                #If WCS is supported by the server, we attempt to map it's access url
                rutaWCS = None
                objWCS = None
                if wcsService is not None:
                    #We first combine the base URL of this dataSet with the one which points
                    #to the service..
                    rutaWCS = (combineURLS(url.replace('catalog.xml',''), wcsService))
                    #And then combine the previous URL which points to the service with the
                    #one pointing to the resource, appending the request string.
                    rutaWCS = (combineURLS(rutaWCS, itemFinalPath)
                                + '?service=WCS&version=1.0.0&request=GetCapabilities')

                    objWCS = Map.WCSinfo(rutaWCS)

                mapObject = Map(nombre, rutaWMS, objWCS)
                dataSet.addMap(mapObject)

        self.singleDataSetMapComplete.emit(dataSet)

    def fillDataSet(self, dataSet, depth=-1):
        """
        Function which will create a tree-like
        structure from a given dataSet, creating both it's
        own sub-data sets retrieved from it's catalog.xml
        and any maps it might have.
        Any maps found will always get added to the set
        passed as parameter to this method, but any
        sub datasets/sub catalogs found on it will only be
        fully mapped (not only referenced) if depth > 0.

        :param    dataSet:    The dataset we have to build a tree from.
        :type     dataSet:    DataSet


        :param    depth:      The depth of the map. If left by default,
                              the whole dataSet will be mapped, and any
                              sub sets of data founds will be recursively
                              mapped. Otherwise, a max of depth steps will
                              be done.
        :type     depth:      int
        """
        self._asyncFillDataSet(dataSet, depth)



    def getAvailableDatasets(self, depth=0):
        """
        Returns the current information about the thredds
        server catalog mapping or retrieves them with
        depth 0 by default if the tree has not yet
        been created.

        :param    depth:      The depth of the tree to be created, if
                              one does not yet exist. If left by default,
                              the whole dataSet will be mapped, and any
                              sub sets of data founds will be recursively
                              mapped. Otherwise, a max of depth steps will
                              be done.
                              This option is ignored if a tree is already
                              stored in this object.
        :type     depth:      int
        """
        if (self.AvailableDataSetList is None
            or len(self.AvailableDataSetList) < 1):
                self.fetchAvailableDatasets(depth)

        return self.AvailableDataSetList


    def translateCatalogURL(self, dataSetCatalogURL, parentCatalogURL=None):
        """
        Processes the URL of a sub-catalog in a THREDDS server, and
        uses different approaches to check if it is a full URL to
        the subcatalog, a relative URL from the main thredds directory,
        or a relative URL from the base URL (....com/) of the server.

        :param   dataSetCatalogURL: the URL informed in the catalog.xml for
                                    the map or set of data.
        :type    String

        :param   parentCatalogURL: the URL informed in the catalog.xml for
                                    the parent set this item belongs to.
        :type    String

        :returns The (expected) proper URL to access the resource.
        :rtype   String
        """

        if "http:" in dataSetCatalogURL.lower() or "www." in dataSetCatalogURL.lower():
            url = dataSetCatalogURL
        else:
            if parentCatalogURL == None:
                url= combineURLS(self.threddsMainCatalog, dataSetCatalogURL)
            else:
                url = combineURLS(parentCatalogURL,dataSetCatalogURL)
        return url
