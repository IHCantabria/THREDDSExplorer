'''
Created on 12 de ene. de 2016

@author: IHC
'''
import THREDDSExplorer.libvisor.persistence.Server_Manager_Add_Server as AddServerUI
from PyQt4.QtCore import pyqtSignal
from PyQt4.QtGui import QDialog

class AddServerWindowManager(QDialog):
    '''
    Manager for the window which will allow the user to input new 
    server data to store.
    '''

    #Signals the submission, by an user, of new server details to be
    #added. The server details are sent away in the form of a tuple,
    #consisting of (name, url)
    newServerSubmitted = pyqtSignal(tuple)

    def __init__(self):
        '''
        Constructor
        '''
        super(AddServerWindowManager, self).__init__()
        self.addServerDialog = AddServerUI.Ui_AddServerDialog()
        self.addServerDialog.setupUi(self)
        self.addServerDialog.buttonAddServer.clicked.connect(self._onAddServerClicked)
        
    def _onAddServerClicked(self):
        """
        Signals the submission, by an user, of new server details to be
        added. The server details are sent away in the form of a tuple,
        consisting of (name, url)
        """
        name = self.addServerDialog.editServerName.text()
        url = self.addServerDialog.editServerURL.text()
        self.newServerSubmitted.emit((name,url))
        pass
        