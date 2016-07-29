# -*- coding: utf-8 -*-

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

class Ui_THREDDSViewer(object):
    def setupUi(self, THREDDSViewer):
        THREDDSViewer.setObjectName(_fromUtf8("THREDDSViewer"))
        THREDDSViewer.resize(396, 773)
        THREDDSViewer.setMinimumSize(QtCore.QSize(98, 11))
        THREDDSViewer.setFloating(True)

        self.retranslateUi(THREDDSViewer)
        QtCore.QMetaObject.connectSlotsByName(THREDDSViewer)

    def retranslateUi(self, THREDDSViewer):
        THREDDSViewer.setWindowTitle(_translate("THREDDSViewer", "THREDDS Explorer", None))


