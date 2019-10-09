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

class Ui_AddServerDialog(object):
    def setupUi(self, AddServerDialog):
        AddServerDialog.setObjectName(_fromUtf8("AddServerDialog"))
        AddServerDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        AddServerDialog.resize(314, 122)
        AddServerDialog.setMaximumSize(QtCore.QSize(441, 157))
        self.gridLayout = QtWidgets.QGridLayout(AddServerDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setFieldGrowthPolicy(QtWidgets.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.labelServerBaseURL = QtWidgets.QLabel(AddServerDialog)
        self.labelServerBaseURL.setObjectName(_fromUtf8("labelServerBaseURL"))
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.labelServerBaseURL)
        self.editServerURL = QtWidgets.QLineEdit(AddServerDialog)
        self.editServerURL.setObjectName(_fromUtf8("editServerURL"))
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.editServerURL)
        self.labelThreddsPath = QtWidgets.QLabel(AddServerDialog)
        self.labelThreddsPath.setObjectName(_fromUtf8("labelThreddsPath"))
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.labelThreddsPath)
        self.editServerName = QtWidgets.QLineEdit(AddServerDialog)
        self.editServerName.setObjectName(_fromUtf8("editServerName"))
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.editServerName)
        self.label = QtWidgets.QLabel(AddServerDialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.SpanningRole, self.label)
        self.verticalLayout.addLayout(self.formLayout)
        self.buttonAddServer = QtWidgets.QPushButton(AddServerDialog)
        self.buttonAddServer.setObjectName(_fromUtf8("buttonAddServer"))
        self.verticalLayout.addWidget(self.buttonAddServer)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.retranslateUi(AddServerDialog)
        QtCore.QMetaObject.connectSlotsByName(AddServerDialog)
        AddServerDialog.setTabOrder(self.editServerName, self.editServerURL)
        AddServerDialog.setTabOrder(self.editServerURL, self.buttonAddServer)

    def retranslateUi(self, AddServerDialog):
        AddServerDialog.setWindowTitle(_translate("AddServerDialog", "Add new server", None))
        self.labelServerBaseURL.setText(_translate("AddServerDialog", "Server URL ", None))
        self.labelThreddsPath.setText(_translate("AddServerDialog", "Server name", None))
        self.label.setText(_translate("AddServerDialog", "(e.g. http://myserver.com/thredds)", None))
        self.buttonAddServer.setText(_translate("AddServerDialog", "Add server", None))


