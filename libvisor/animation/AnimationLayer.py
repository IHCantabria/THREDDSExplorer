'''
Created on 27 de ene. de 2016

@author: IHC
'''

class AnimationLayer(object):
    '''
    Main object interpreted by the Animator module.
    
    This object holds all the required information for that module
    to generate an animation from it. In the case of WMS/WCS layers
    in THREDDS Explorer, if no animationData and no animationGroup
    is defined (=None) the animator component will attempt to download
    it as defined through it's parsers (defined in .providersmanagers
    package). 
    
    If, instead, those two attributes are assigned, the animator will
    not do any download action assuming the AnimationLayer object
    is complete and requires no further intervention.
    
    The reasoning for this is that we can, this way, generate full
    fledged AnimationLayer objects which hold a component we want
    to include in our animation without any post-processing in a
    final Animator object, just interpreting it, from any other controller
    which can generate this type of object.
    
    A practical example of this is TESEO Spill Simulator. A call to its
    controller will generate an AnimationLayer object, which can later
    be injected into THREDDS Explorer Animator module to be animated
    along other layers from other providers. 
    
    '''


    def __init__(self, mapObject, layerName, times, service, boundingBox = None, selectedStyle = None):
        '''
        :param    mapObject:    The map object which defines all the required
                                information to access this map and it's layers
                                through the network map service.
        :type     mapObject:    ThreddsMapperGeneric.Map
        
        :param    layerName:    The name of the layer we will animate.
        :type     layerName:    [str]
        
        :param    times:        The list of times which will be our frames.
        :type     times:        [str]
        
        :param    service:      The service used to retrieve the images
        :type     service:      [str] {WMS/WCS/...}
        
        :param    boundingBox:      The service used to retrieve the images
        :type     boundingBox:      BoundingBoxInfo
        
        :param    selectedStyle:      The style this map will be drawn with (WMS only)
        :type     selectedStyle:      [str]
        '''
        self.mapObject = mapObject;
        self.layerName = layerName;
        self.times = times
        self.service = service
        self.bbox = boundingBox
        self.style = selectedStyle
        self.animationData = None  #Animation2.AnimationData
        self.animationGroup = None #QgsLayerTreeGroup
        
    def getTimes(self):
        return self.times
    
    def getLayerName(self):
        return self.layerName
    
    def getStyle(self):
        return self.style
    
    def getMapObject(self):
        return self.mapObject
    
    def getService(self):
        return self.service
    
    def getBBOX(self):
        return self.bbox
    
    def setAnimationData(self, animationData):
        """
        Sets AnimationData information for those animated layers which
        already have them.
        """
        self.animationData = animationData
        
    def getAnimationData(self):
        return self.animationData
    
    def setAnimationLegendGroups(self, qgisLayerGroup):
        """
        Sets the group of layers which can be managed for this object
        in the QGIS interface for those animated layers which
        already have them.. 
        """
        self.animationGroup = qgisLayerGroup
        
    def getAnimationLegendGroups(self):
        return self.animationGroup
        