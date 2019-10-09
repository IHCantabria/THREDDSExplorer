# -*- coding:utf8 -*-
"""
Created on 2016-01-04

@author: IHC
"""

from PyQt5.QtWidgets import QDialog, QMessageBox, QTableWidgetItem, QAbstractItemView
from PyQt5.QtCore import pyqtSlot, QSettings, pyqtSignal

from .Server_Manager_UI import Ui_serverListDialog
from .AddServerWindowManager import AddServerWindowManager
from .ThreddsServerInfo import ThreddsServerInfoObject, isValidName, isValidURL

class ServerStorageManager(QDialog):
    """Handles persistence of preferences for this application,
    using QGIS settings storage API. Will also handle
    user interaction with the persisted objects.

    This is currently used to store a list of THREDDS server data
    which we provide by default, and will be regenerated in
    every manager load through initializeDefaultServers(), the
    list of servers stored by the user himself/herself, and
    some user defined settings like pop-ups with "never show
    again"-like buttons.

    *** With proper configuration, this can be used to send
    configuration options across different modules created
    by IH (like publishing modules capabilities for animators,
    loaders, ... to be later read and executed by others)
    """
    serverSelected = pyqtSignal(ThreddsServerInfoObject)

    def __init__(self, parent=None):
        """Constructor."""

        super(ServerStorageManager, self).__init__(parent)
        self.IHDomain = "IHCANTABRIA"
        self.PluginDomain = "THREDDS_EXPLORER"
        self.ThreddsServerGroup = "/".join([self.IHDomain, self.PluginDomain, "servers"])
        self.SettingsGroup = "/".join([self.IHDomain, self.PluginDomain, "settings"])
        self.GDALVersionErrorSetting = "/".join([self.SettingsGroup, "show_gdal_error"])
        self.availableServers = []
        self.initializeDefaultServers()

        self.serverListDialog = Ui_serverListDialog()
        self.serverListDialog.setupUi(self)
        self.serverListDialog.buttonLoadData.clicked.connect(self._onbuttonLoadDataClick)
        self.serverListDialog.buttonAdd.clicked.connect(self._onbuttonAddClick)
        self.serverListDialog.buttonRemove.clicked.connect(self._onbuttonDeleteClick)
        self.reloadTable()
        #super(ServerStorageManager, self).show()

    def reloadTable(self):
        """Synchronizes the copy of the available servers this object
        holds with the ones stored in the Settings, and updates the
        table to show changes."""

        self.availableServers = self.retrieveAllStoredServerInfo()
        table = self.serverListDialog.tableWidget
        #table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        table.setRowCount(len(self.availableServers))
        table.setColumnCount(2)
        table.setHorizontalHeaderLabels("Server Name;Server full URL".split(';'))
        table.horizontalHeader().setStretchLastSection(True)
        table.setSelectionBehavior(QAbstractItemView.SelectRows)

        for (i, item) in enumerate(self.availableServers):
            table.setItem(i, 0, QTableWidgetItem(item.getName()))
            table.setItem(i, 1, QTableWidgetItem(item.getURL()))

    def storeServerInfo(self, serverInfoObject):
        """Saves the provided ThreddsServerInfo object into the underlying
        QSettings object for this application.

        It is stored under the namespace self.ThreddsServerGroup.
        """
        self._saveInSettings(serverInfoObject)
        self.reloadTable()

    def deleteServerInfo(self, serverName):
        """Deletes the ThreddsServerInfo object with the given name from
        the underlying settings.

        :param    serverName: The name of the server we have to delete.
        :type     serverName: str
        """
        settings = QSettings()
        settings.beginGroup(self.ThreddsServerGroup)
        settings.remove(serverName)
        settings.endGroup()

    def initializeDefaultServers(self):
        """Guarantees that this object has access to, at least, some default
        servers pre-configured in them. Will also restore their properties if they
        have previously been changed.
        """
        # settings = QSettings()
        # settings.beginGroup(self.ThreddsServerGroup)
        # for setting in settings.allKeys():
        #     settings.remove(setting)
        defaults = (
                ('NOAA Oceanwatch', r'http://oceanwatch.pfeg.noaa.gov/thredds'),
                ('NOAA Operational Model Archive', r'http://nomads.ncdc.noaa.gov/thredds'),
                ('Santander Meteorology Group', r'http://www.meteo.unican.es/thredds/')
        )
        for name,url in defaults:
            self._saveServerInSettings(ThreddsServerInfoObject(name, url))

    def _saveServerInSettings(self, serverInfoObject):
        """Stores an object containing the required information to access a thredds
        server in a settings object for persistence.

        :param serverInfoObject: the server object with the information we want to store
        :type  serverInfoObject: ThreddsServerInfoObject
        """
        settings = QSettings()
        k = "/".join([self.ThreddsServerGroup, serverInfoObject.getName()])
        v = serverInfoObject.getURL()
        settings.setValue(k, v)

    def retrieveAllStoredServerInfo(self):
        """Retrieves a list of ThreddsServerInfo objects stored in the
        underlying settings object for this application.

        Uses the Group definition "self.ThreddsServerGroup" to know
        under which 'namespace' are these elements stored. This allows
        us to store other configuration settings under other 'namespaces'
        using the same QSettings object.

        :returns A list of objects which contain information about the thredds
                 servers previously stored in the settings object.
        :rtype   [ThreddsServerInfoObject]
        """
        serverList = []
        settings = QSettings()
        settings.beginGroup(self.ThreddsServerGroup)

        for key in settings.childKeys():
            ret = settings.value(key)
            if type(ret) in [ str, unicode ]:
                name, url = key, ret
            else:
                try:
                    name, url = ret
                except:
                    continue

            serverList.append(ThreddsServerInfoObject(name, url));

        settings.endGroup()

        return serverList

    def _onbuttonLoadDataClick(self):
        selectedRowNumber = self.serverListDialog.tableWidget.currentRow()

        #Safeguard in case of empty server list or desynchronization between
        #the server list table and the internal server list.
        if selectedRowNumber >= 0 and selectedRowNumber < len(self.availableServers):
            self.serverSelected.emit(self.availableServers[selectedRowNumber])

    def _onbuttonAddClick(self):
        self.addServerWindowManager = AddServerWindowManager()
        self.addServerWindowManager.newServerSubmitted.connect(self._onAttemptToAddNewServer)
        self.addServerWindowManager.show()

    def _onbuttonDeleteClick(self):
        selectedRow = self.serverListDialog.tableWidget.currentRow()
        nameColumn = 0 #The column we have the names of the servers shown at.
        deleteTarget = self.serverListDialog.tableWidget.item(selectedRow, nameColumn)

        if deleteTarget: # just in case the user attempts to remove an element when none are shown or selected
            reply = QMessageBox.question(self, "Confirm deletion",
                        'Are you sure you want to remove server {s}?"'.format(s=deleteTarget.text()),
                        QMessageBox.Yes, QMessageBox.No)

            if reply == QMessageBox.Yes:
                self.deleteServerInfo(deleteTarget.text())
                self.reloadTable()

    @pyqtSlot(tuple)
    def _onAttemptToAddNewServer(self, inServerDetails):
        """Checks whether the server details provided are valid (or seem to be so)
        and then adds them to the underlying storage system. Will hide the add server
        window or show an error message depending on the outcome of this operation."""

        if not isValidName(inServerDetails[0]):
            msg  = "The provided name is not valid.\n"
            msg += "Make sure it is not empty, and doesn't have any slashes ('/') in it."
            QMessageBox.warning(self, "Warning", msg)

        elif not isValidURL(inServerDetails[1]):
            msg = "The provided URL is not valid.\nMake sure it is not empty."
            QMessageBox.warning(self, "Warning", msg)

        else:
            serverInfo = ThreddsServerInfoObject(inServerDetails[0], inServerDetails[1])
            self._saveServerInSettings(serverInfo)
            self.addServerWindowManager.close()
            self.addServerWindowManager = None
            self.reloadTable()

    @property
    def show_GDAL_error(self):
        """Return whether or not to show GDAL error.
        Default is True."""

        settings = QSettings()
        ret = settings.value(self.GDALVersionErrorSetting, True)

        if type(ret) == bool:
            return ret

        elif type(ret) in [ str, unicode ]:
            ret = ret.lower()
            if ret == "true":
                return True
            else:
                return False

        else:
            return True # default:

    @show_GDAL_error.setter
    def show_GDAL_error(self, val):
        """Set True/False to settings var of whether or not show GDAL error anymore.
        False means do not show error ever again."""

        settings = QSettings()
        settings.setValue(self.GDALVersionErrorSetting, val)
