# -*- coding: utf-8 -*-

#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtWidgets

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:

    def _fromUtf8(s):
        return s


try:
    _encoding = QtWidgets.QApplication.UnicodeUTF8

    def _translate(context, text, disambig):
        return QtWidgets.QApplication.translate(context, text, disambig, _encoding)

except AttributeError:

    def _translate(context, text, disambig):
        return QtWidgets.QApplication.translate(context, text, disambig)


class Ui_serverListDialog(object):
    def setupUi(self, serverListDialog):
        serverListDialog.setObjectName(_fromUtf8("serverListDialog"))
        serverListDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        serverListDialog.resize(499, 267)
        serverListDialog.setMinimumSize(QtCore.QSize(499, 267))
        self.gridLayout = QtWidgets.QGridLayout(serverListDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.baseVerticalLayout = QtWidgets.QVBoxLayout()
        self.baseVerticalLayout.setObjectName(_fromUtf8("baseVerticalLayout"))
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.tableWidget = QtWidgets.QTableWidget(serverListDialog)
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableWidget.setObjectName(_fromUtf8("tableWidget"))
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.horizontalLayout.addWidget(self.tableWidget)
        self.buttonLayout = QtWidgets.QVBoxLayout()
        self.buttonLayout.setObjectName(_fromUtf8("buttonLayout"))
        self.buttonLoadData = QtWidgets.QPushButton(serverListDialog)
        self.buttonLoadData.setMinimumSize(QtCore.QSize(0, 0))
        self.buttonLoadData.setObjectName(_fromUtf8("buttonLoadData"))
        self.buttonLayout.addWidget(self.buttonLoadData)
        self.buttonAdd = QtWidgets.QPushButton(serverListDialog)
        self.buttonAdd.setCheckable(False)
        self.buttonAdd.setObjectName(_fromUtf8("buttonAdd"))
        self.buttonLayout.addWidget(self.buttonAdd)
        self.buttonRemove = QtWidgets.QPushButton(serverListDialog)
        self.buttonRemove.setObjectName(_fromUtf8("buttonRemove"))
        self.buttonLayout.addWidget(self.buttonRemove)
        spacerItem = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding
        )
        self.buttonLayout.addItem(spacerItem)
        self.horizontalLayout.addLayout(self.buttonLayout)
        self.baseVerticalLayout.addLayout(self.horizontalLayout)
        self.gridLayout.addLayout(self.baseVerticalLayout, 0, 0, 1, 1)

        self.retranslateUi(serverListDialog)
        QtCore.QMetaObject.connectSlotsByName(serverListDialog)

    def retranslateUi(self, serverListDialog):
        serverListDialog.setWindowTitle(
            _translate("serverListDialog", "Available server settings", None)
        )
        self.buttonLoadData.setText(_translate("serverListDialog", "Load data", None))
        self.buttonLoadData.setShortcut(_translate("serverListDialog", "Alt+L", None))
        self.buttonAdd.setText(_translate("serverListDialog", "Add server...", None))
        self.buttonAdd.setShortcut(_translate("serverListDialog", "Alt+A", None))
        self.buttonRemove.setText(_translate("serverListDialog", "Remove server", None))
        self.buttonRemove.setShortcut(_translate("serverListDialog", "Alt+R", None))
