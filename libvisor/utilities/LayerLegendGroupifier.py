'''
Created on 28 de mar. de 2016

@author: IHC
'''
from PyQt4.QtCore import QObject, pyqtSignal
from qgis.core import QgsRectangle, QgsLayerTreeLayer, QgsLayerTreeGroup, \
                         QgsProject, QgsMapLayerRegistry
from qgis.utils import iface
from threading import RLock

class LayerGroupifier(QObject):
    """
    Utility class which handles the creation of layer groups through
    QGIS legend interface, and notifies about the operation actual
    completion, progress and errors.
    """
    groupAssignmentLock = RLock()
    errorsFound = pyqtSignal(int) #Number of errors found during the groupify operation
    groupifyComplete = pyqtSignal(QgsLayerTreeGroup, list) #Emits the created group and the list of layers assigned to it
    statusSignal = pyqtSignal(str)
    
    def __init__(self, layerList, groupName, parent = None):
        """
        :param layerList: List of layers to be added to this group.
        :type  layerList: [QgsLayer]
        
        :param groupName: Name to give to this group
        :type  groupName: [QgsLayer]
        
        """
        super(LayerGroupifier, self).__init__(parent)
        self.layerList = layerList
        self.groupName = groupName
        self.errorCount = 0
        self.layersToBeGrouped = 0
        self.layersAddedToGroups = 0
        self.singleLayerSelectionModeInGroup = True
        self.generatedGroup = None
        
    def getGeneratedGroup(self):
        """
        Returns the generated group, which may still
        be unpopulated.
        """
        with self.groupAssignmentLock:
            if self.generatedGroup is None:
                root = QgsProject.instance().layerTreeRoot()
                self.generatedGroup = root.addGroup(self.groupName)
                self.generatedGroup.setExpanded(False)
                self.generatedGroup.setIsMutuallyExclusive(self.singleLayerSelectionModeInGroup)
                self.generatedGroup.addedChildren.connect(self.onChildrenAddedToNodeGroup)
            return self.generatedGroup
        
    def setSingleLayerSelectionModeInGroup(self, booleanValue):
        """
        Defines if more than one layers in this group will be able
        to be selected and/or shown at once by the user.
        """
        self.singleLayerSelectionModeInGroup = booleanValue
        
        
    def groupify(self):
        with self.groupAssignmentLock:
            self.layersToBeGrouped = len(self.layerList)
            self.getGeneratedGroup()
            registryAddedLayers = QgsMapLayerRegistry.instance().addMapLayers(self.layerList, False)
            for item in registryAddedLayers:
                if item not in self.layerList:
                    #print("****WARNING: A LAYER WAS NOT ADDED TO THE REGISTRY: "+str(item)+" --- ID : "+item.id())
                    self.errorCount = self.errorCount + 1
                    pass
            self.correctlyRegisteredLayers = sorted(self.layerList, key=lambda layer: layer.name())
            for layer in self.correctlyRegisteredLayers:
                self.generatedGroup.addLayer(layer)
                iface.legendInterface().setLayerVisible(layer, False)
            
            #We combine the group extents so all the layers are zoomed
            #equally on play.
            extent = QgsRectangle()
            extent.setMinimal()
            for child in self.generatedGroup.children():
                if isinstance(child, QgsLayerTreeLayer):
                    extent.combineExtentWith( child.layer().extent() )
        
            iface.mapCanvas().setExtent( extent )
            iface.mapCanvas().refresh()
            
            if self.errorCount > 0:
                self.errorsFound.emit(self.errorCount)
                
        
        
    def onChildrenAddedToNodeGroup(self, node, indexFrom, indexTo):
        """
        Will be called every time QGIS loads a new layer into a 
        layer group in the legend interface. Useful for progress
        tracking purposes.
        """
        self.layersAddedToGroups = self.layersAddedToGroups + 1          
        self.statusSignal.emit("Layers ready: "+str(self.layersAddedToGroups)
                               +" / "+str(self.layersToBeGrouped))
        #If we have already added all the layers to nodes, we will notify 
        #the operation has finished.
        if self.layersToBeGrouped == self.layersAddedToGroups:
            self.statusSignal.emit("Group ready - "+self.groupName)
            self.groupifyComplete.emit(self.generatedGroup, self.correctlyRegisteredLayers)
    