'''
Created on 22 de feb. de 2016

@author: IHC
'''
from THREDDSExplorer.libvisor.animation import Animation_add_others
from PyQt4.QtGui import QWidget, QPushButton
from PyQt4.QtCore import pyqtSlot, pyqtSignal
from THREDDSExplorer.libvisor.animation.AnimationLayer import AnimationLayer
from THREDDSExplorer.libvisor.animation.Animation2 import AnimationData

class AnimationOtherLayerManager(QWidget):
    '''
    This should be the "standard" way to load layers into the animator,
    and could conceivably be used to unify all types of AnimationLayer
    creation, including WMS/WCS currently hardcoded in 
    AnimationController.Controller.
    
    When an user requests a layer to be added, this window (TODO) reads
    through the available packages supporting the generation of
    AnimationLayer objects (which define the data to generate an animation
    for a map). Several buttons are enabled, one for every found service
    
    *** This "reading" through all the packages supporting creation of
    AnimationLayer objects could be done by forcing them to store (using
    this project persistence module, for example) a known key in QGIS
    as a QSettings() object, and forcing them to overwrite it on plug-in
    exit or destruction. This would keep a record of available modules,
    and could even provide code to be executed automatically, if they do
    not all follow the same interface.
    *** Currently only used for TESEO Spill Simulator layers.
    
    This object will then access that module controller method to request
    the user information to generate that layer, and proceed to do so. 
    
    Advice: To simplify, stuff, you can check _onTeseoButtonClicked()
    method in this file as a template on how to do it to any layer.
    A couple signals and a single method which is what should be required to
    generate any kind of layer while providing the user for progress feedback
    (if not already implemented in the other module UI)
    '''
    
    
    
    #AnimationLayer object for table representation, animation2
    #object which contains the actual animation data, and the
    #layer groups for QGIS.
    animationLayerCreated = pyqtSignal(object) 

    def __init__(self, parent = None):
        '''
        Constructor
        '''
        super(AnimationOtherLayerManager, self).__init__()
        self.dialog = Animation_add_others.Ui_Dialog()
        self.dialog.setupUi(self)
        self.animationReadyObject = None
        self.animationReadyDetails = None
        self.dialog.progressInfoLabel.hide()
        self.numberOfButtons = 0;
        #We set up the available buttons depending on
        #what other associated modules from IH are available
        #in user QGIS installation.
        try:
            from TeseoSpillVisualizer.libteseo.MainController import MainController as TESEOController
            button = QPushButton("Add a TESEO animated layer...")            
            self.TeseoController = TESEOController()
            button.clicked.connect(self._onTeseoButtonClicked)
            self.dialog.verticalLayout.addWidget(button)
            self.numberOfButtons = self.numberOfButtons + 1;
        except ImportError:
            pass
        
        if self.numberOfButtons == 0:
            self.dialog.progressInfoLabel.setText("No supported modules were found.")
            self.dialog.progressInfoLabel.show()
            
        
    @pyqtSlot()
    def _onTeseoButtonClicked(self):
        self.TeseoController.animationReady.connect(self._onAnimatedLayerCreated)
        self.TeseoController.animationReady.connect(self._onCreationStepDone)
        self.TeseoController.animationGenerationUpdate.connect(self._onCreationStepDone)
        self.TeseoController.generateAnimation()
        self.dialog.progressInfoLabel.show()
        
    @pyqtSlot(str)
    def _onCreationStepDone(self, infoString):
        self.dialog.progressInfoLabel.setText(infoString)
    
    @pyqtSlot(str)
    def _onAnimatedLayerCreated(self, descriptionString):
        animationObjects = self.TeseoController.getAnimationLayerObjects()
        for item in animationObjects:
            self.animationLayerCreated.emit(item)