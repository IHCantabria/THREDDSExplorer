# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'F:\PROYECTOS_IH\trunk\Visor_WMS_QGIS\VisorWMS\libvisor\animation\Animation_add_others.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(265, 126)
        Dialog.setMinimumSize(QtCore.QSize(265, 99))
        Dialog.setMaximumSize(QtCore.QSize(265, 999))
        self.verticalLayout = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.addTeseoLayerButton = QtGui.QPushButton(Dialog)
        self.addTeseoLayerButton.setObjectName(_fromUtf8("addTeseoLayerButton"))
        self.verticalLayout.addWidget(self.addTeseoLayerButton)
        self.placeholderButton1 = QtGui.QPushButton(Dialog)
        self.placeholderButton1.setObjectName(_fromUtf8("placeholderButton1"))
        self.verticalLayout.addWidget(self.placeholderButton1)
        self.placeholderButton2 = QtGui.QPushButton(Dialog)
        self.placeholderButton2.setObjectName(_fromUtf8("placeholderButton2"))
        self.verticalLayout.addWidget(self.placeholderButton2)
        self.progressInfoLabel = QtGui.QLabel(Dialog)
        self.progressInfoLabel.setObjectName(_fromUtf8("progressInfoLabel"))
        self.verticalLayout.addWidget(self.progressInfoLabel)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Add a new animation", None))
        self.addTeseoLayerButton.setText(_translate("Dialog", "Add a TESEO animated layer...", None))
        self.placeholderButton1.setText(_translate("Dialog", "Placeholder 1", None))
        self.placeholderButton2.setText(_translate("Dialog", "Placeholder 2", None))
        self.progressInfoLabel.setText(_translate("Dialog", "TextLabel", None))

