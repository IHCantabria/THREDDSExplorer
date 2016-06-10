# -*- coding: utf-8 -*-

#
# Created: Fri Jun 10 13:27:53 2016
#      by: PyQt4 UI code generator 4.10.4
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

class Ui_AddLayerDialog(object):
    def setupUi(self, AddLayerDialog):
        AddLayerDialog.setObjectName(_fromUtf8("AddLayerDialog"))
        AddLayerDialog.resize(296, 138)
        AddLayerDialog.setMinimumSize(QtCore.QSize(296, 138))
        AddLayerDialog.setMaximumSize(QtCore.QSize(523, 138))
        self.verticalLayout = QtGui.QVBoxLayout(AddLayerDialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label = QtGui.QLabel(AddLayerDialog)
        self.label.setMinimumSize(QtCore.QSize(278, 13))
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.layerSelector = QtGui.QComboBox(AddLayerDialog)
        self.layerSelector.setObjectName(_fromUtf8("layerSelector"))
        self.layerSelector.addItem(_fromUtf8(""))
        self.verticalLayout.addWidget(self.layerSelector)
        self.beginTimeSelector = QtGui.QComboBox(AddLayerDialog)
        self.beginTimeSelector.setObjectName(_fromUtf8("beginTimeSelector"))
        self.beginTimeSelector.addItem(_fromUtf8(""))
        self.verticalLayout.addWidget(self.beginTimeSelector)
        self.finishTimeSelector = QtGui.QComboBox(AddLayerDialog)
        self.finishTimeSelector.setObjectName(_fromUtf8("finishTimeSelector"))
        self.finishTimeSelector.addItem(_fromUtf8(""))
        self.verticalLayout.addWidget(self.finishTimeSelector)
        self.buttonAddLayer = QtGui.QPushButton(AddLayerDialog)
        self.buttonAddLayer.setObjectName(_fromUtf8("buttonAddLayer"))
        self.verticalLayout.addWidget(self.buttonAddLayer)

        self.retranslateUi(AddLayerDialog)
        QtCore.QMetaObject.connectSlotsByName(AddLayerDialog)

    def retranslateUi(self, AddLayerDialog):
        AddLayerDialog.setWindowTitle(_translate("AddLayerDialog", "Add new layer to animation", None))
        self.label.setText(_translate("AddLayerDialog", "Selected map: ", None))
        self.layerSelector.setItemText(0, _translate("AddLayerDialog", "Select a layer...", None))
        self.beginTimeSelector.setItemText(0, _translate("AddLayerDialog", "Animation begins at...", None))
        self.finishTimeSelector.setItemText(0, _translate("AddLayerDialog", "Animation finishes at...", None))
        self.buttonAddLayer.setText(_translate("AddLayerDialog", "Add to layer list", None))


