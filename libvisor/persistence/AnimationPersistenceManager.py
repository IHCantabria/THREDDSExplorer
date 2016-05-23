'''
Created on 9 de feb. de 2016

@author: IHC
'''
from PyQt4.Qt import QFileDialog

class AnimationPersistenceManager(object):
    '''
    TODO: Should be able to persist AnimationLayer objects, their 
    AnimationData information, the QGIS QgsLayerTreeGroup information
    (or provide a way to restore it from AnimatioData object, which
    is good enough).
    '''


    def __init__(self):
        '''
        Constructor
        '''
        pass
    
    def saveAnimation(self, listOfAnimatedElements, description=""):
        """
        TODO: Doesn't work. Implement.
        
        Serializes the animation after showing the user a dialog to
        choose where to do so.
        
        :param    listOfAnimatedElements: The list of objects which compose this
                                          animation.
        :type     listOfAnimatedElements: [Animation2]
        .
        :param    fileName:               The name of the file in which this animation
                                          should be saved.
        :type     fileName:               str
        
        :param    description:            (optional) Brief description for this animation.
        :type     description:            str
        """
        filename = QFileDialog.getSaveFileName(
                                   parent = None,
                                   caption = "Save animation layer",
                                   filter=("All Files (*.*)"));
        #print filename
        pass
    
    
    def loadAnimation(self, fileName):
        """
        TODO: Doesn't work. Implement.
        
        Deserializes the stored animation and returns it to the caller.
        
        :param    fileName:               The name of the file which stores
                                          the animation information.
        :type     fileName:               str
        """
        pass
    
    