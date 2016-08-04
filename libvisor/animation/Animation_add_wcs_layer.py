# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'libvisor\animation\Animation_add_wcs_layer.ui'
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

class Ui_AddLayerDialog(object):
    def setupUi(self, AddLayerDialog):
        AddLayerDialog.setObjectName(_fromUtf8("AddLayerDialog"))
        AddLayerDialog.resize(350, 265)
        AddLayerDialog.setMinimumSize(QtCore.QSize(350, 265))
        AddLayerDialog.setMaximumSize(QtCore.QSize(523, 500))
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
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setSizeConstraint(QtGui.QLayout.SetMinimumSize)
        self.gridLayout.setContentsMargins(-1, 0, -1, -1)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.southBound = QtGui.QLineEdit(AddLayerDialog)
        self.southBound.setObjectName(_fromUtf8("southBound"))
        self.gridLayout.addWidget(self.southBound, 3, 1, 1, 1)
        self.westBound = QtGui.QLineEdit(AddLayerDialog)
        self.westBound.setObjectName(_fromUtf8("westBound"))
        self.gridLayout.addWidget(self.westBound, 2, 0, 1, 1)
        self.eastBound = QtGui.QLineEdit(AddLayerDialog)
        self.eastBound.setObjectName(_fromUtf8("eastBound"))
        self.gridLayout.addWidget(self.eastBound, 2, 2, 1, 1)
        self.northBound = QtGui.QLineEdit(AddLayerDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.northBound.sizePolicy().hasHeightForWidth())
        self.northBound.setSizePolicy(sizePolicy)
        self.northBound.setObjectName(_fromUtf8("northBound"))
        self.gridLayout.addWidget(self.northBound, 1, 1, 1, 1)
        self.labelCRS = QtGui.QLabel(AddLayerDialog)
        self.labelCRS.setMinimumSize(QtCore.QSize(276, 13))
        self.labelCRS.setObjectName(_fromUtf8("labelCRS"))
        self.gridLayout.addWidget(self.labelCRS, 0, 0, 1, 3)
        self.verticalLayout.addLayout(self.gridLayout)
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
        self.labelCRS.setText(_translate("AddLayerDialog", "CRS INFO", None))
        self.buttonAddLayer.setText(_translate("AddLayerDialog", "Add to layer list", None))

