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


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(265, 126)
        Dialog.setMinimumSize(QtCore.QSize(265, 99))
        Dialog.setMaximumSize(QtCore.QSize(265, 999))
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.progressInfoLabel = QtWidgets.QLabel(Dialog)
        self.progressInfoLabel.setObjectName(_fromUtf8("progressInfoLabel"))
        self.verticalLayout.addWidget(self.progressInfoLabel)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Add a new animation", None))
        self.progressInfoLabel.setText(_translate("Dialog", "TextLabel", None))
