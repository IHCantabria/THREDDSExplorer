# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'THREDDS_Explorer_dockwidget_base.ui'
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


class Ui_THREDDSViewer(object):
    def setupUi(self, THREDDSViewer):
        THREDDSViewer.setObjectName(_fromUtf8("THREDDSViewer"))
        THREDDSViewer.resize(396, 773)
        THREDDSViewer.setMinimumSize(QtCore.QSize(98, 11))
        THREDDSViewer.setFloating(True)
        self.dockWidgetContents = QtWidgets.QWidget()
        self.dockWidgetContents.setObjectName(_fromUtf8("dockWidgetContents"))
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.dockWidgetContents)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.scrollArea = QtWidgets.QScrollArea(self.dockWidgetContents)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName(_fromUtf8("scrollArea"))
        self.scrollAreaWidgetContents_7 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_7.setGeometry(QtCore.QRect(0, 0, 376, 731))
        self.scrollAreaWidgetContents_7.setObjectName(
            _fromUtf8("scrollAreaWidgetContents_7")
        )
        self.gridLayout_2 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents_7)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtWidgets.QLabel(self.scrollAreaWidgetContents_7)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.tree_widget = QtWidgets.QTreeWidget(self.scrollAreaWidgetContents_7)
        self.tree_widget.setMinimumSize(QtCore.QSize(250, 200))
        self.tree_widget.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.tree_widget.setObjectName(_fromUtf8("tree_widget"))
        self.verticalLayout.addWidget(self.tree_widget)
        self.tabWidget = QtWidgets.QTabWidget(self.scrollAreaWidgetContents_7)
        self.tabWidget.setMinimumSize(QtCore.QSize(0, 300))
        self.tabWidget.setMaximumSize(QtCore.QSize(10000, 500))
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tab_WMS = QtWidgets.QWidget()
        self.tab_WMS.setObjectName(_fromUtf8("tab_WMS"))
        self.gridLayout_4 = QtWidgets.QGridLayout(self.tab_WMS)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.tab_WMS_layout = QtWidgets.QVBoxLayout()
        self.tab_WMS_layout.setObjectName(_fromUtf8("tab_WMS_layout"))
        self.combo_wms_layer = QtWidgets.QComboBox(self.tab_WMS)
        self.combo_wms_layer.setObjectName(_fromUtf8("combo_wms_layer"))
        self.tab_WMS_layout.addWidget(self.combo_wms_layer)
        self.layout_wms_style = QtWidgets.QHBoxLayout()
        self.layout_wms_style.setObjectName(_fromUtf8("layout_wms_style"))
        self.combo_wms_style_type = QtWidgets.QComboBox(self.tab_WMS)
        self.combo_wms_style_type.setObjectName(_fromUtf8("combo_wms_style_type"))
        self.layout_wms_style.addWidget(self.combo_wms_style_type)
        self.combo_wms_style_palette = QtWidgets.QComboBox(self.tab_WMS)
        self.combo_wms_style_palette.setObjectName(_fromUtf8("combo_wms_style_palette"))
        self.layout_wms_style.addWidget(self.combo_wms_style_palette)
        self.tab_WMS_layout.addLayout(self.layout_wms_style)
        self.WMSLabelTimeRange = QtWidgets.QLabel(self.tab_WMS)
        self.WMSLabelTimeRange.setObjectName(_fromUtf8("WMSLabelTimeRange"))
        self.tab_WMS_layout.addWidget(self.WMSLabelTimeRange)
        self.combo_wms_time = QtWidgets.QComboBox(self.tab_WMS)
        self.combo_wms_time.setObjectName(_fromUtf8("combo_wms_time"))
        self.tab_WMS_layout.addWidget(self.combo_wms_time)
        self.combo_wms_time_last = QtWidgets.QComboBox(self.tab_WMS)
        self.combo_wms_time_last.setObjectName(_fromUtf8("combo_wms_time_last"))
        self.tab_WMS_layout.addWidget(self.combo_wms_time_last)
        self.WMSBoundingBoxInfo = QtWidgets.QLabel(self.tab_WMS)
        self.WMSBoundingBoxInfo.setObjectName(_fromUtf8("WMSBoundingBoxInfo"))
        self.tab_WMS_layout.addWidget(self.WMSBoundingBoxInfo)
        self.WMS_Bounds = QtWidgets.QGridLayout()
        self.WMS_Bounds.setObjectName(_fromUtf8("WMS_Bounds"))
        self.WMS_northLabel = QtWidgets.QLabel(self.tab_WMS)
        self.WMS_northLabel.setText(_fromUtf8(""))
        self.WMS_northLabel.setObjectName(_fromUtf8("WMS_northLabel"))
        self.WMS_Bounds.addWidget(self.WMS_northLabel, 1, 1, 1, 1)
        self.WMS_eastBound = QtWidgets.QLineEdit(self.tab_WMS)
        self.WMS_eastBound.setEnabled(False)
        self.WMS_eastBound.setObjectName(_fromUtf8("WMS_eastBound"))
        self.WMS_Bounds.addWidget(self.WMS_eastBound, 1, 2, 1, 1)
        self.WMS_westBound = QtWidgets.QLineEdit(self.tab_WMS)
        self.WMS_westBound.setEnabled(False)
        self.WMS_westBound.setObjectName(_fromUtf8("WMS_westBound"))
        self.WMS_Bounds.addWidget(self.WMS_westBound, 1, 0, 1, 1)
        self.WMS_southBound = QtWidgets.QLineEdit(self.tab_WMS)
        self.WMS_southBound.setEnabled(False)
        self.WMS_southBound.setObjectName(_fromUtf8("WMS_southBound"))
        self.WMS_Bounds.addWidget(self.WMS_southBound, 2, 1, 1, 1)
        self.WMS_northBound = QtWidgets.QLineEdit(self.tab_WMS)
        self.WMS_northBound.setEnabled(False)
        self.WMS_northBound.setObjectName(_fromUtf8("WMS_northBound"))
        self.WMS_Bounds.addWidget(self.WMS_northBound, 0, 1, 1, 1)
        self.tab_WMS_layout.addLayout(self.WMS_Bounds)
        self.gridLayout_4.addLayout(self.tab_WMS_layout, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab_WMS, _fromUtf8(""))
        self.tab_WCS = QtWidgets.QWidget()
        self.tab_WCS.setObjectName(_fromUtf8("tab_WCS"))
        self.gridLayout_6 = QtWidgets.QGridLayout(self.tab_WCS)
        self.gridLayout_6.setObjectName(_fromUtf8("gridLayout_6"))
        self.tab_WCS_layout = QtWidgets.QVBoxLayout()
        self.tab_WCS_layout.setObjectName(_fromUtf8("tab_WCS_layout"))
        self.combo_wcs_coverage = QtWidgets.QComboBox(self.tab_WCS)
        self.combo_wcs_coverage.setObjectName(_fromUtf8("combo_wcs_coverage"))
        self.tab_WCS_layout.addWidget(self.combo_wcs_coverage)
        self.WCSLabelTimeRange = QtWidgets.QLabel(self.tab_WCS)
        self.WCSLabelTimeRange.setMaximumSize(QtCore.QSize(16777215, 25))
        self.WCSLabelTimeRange.setObjectName(_fromUtf8("WCSLabelTimeRange"))
        self.tab_WCS_layout.addWidget(self.WCSLabelTimeRange)
        self.combo_wcs_time = QtWidgets.QComboBox(self.tab_WCS)
        self.combo_wcs_time.setObjectName(_fromUtf8("combo_wcs_time"))
        self.tab_WCS_layout.addWidget(self.combo_wcs_time)
        self.combo_wcs_time_last = QtWidgets.QComboBox(self.tab_WCS)
        self.combo_wcs_time_last.setObjectName(_fromUtf8("combo_wcs_time_last"))
        self.tab_WCS_layout.addWidget(self.combo_wcs_time_last)
        self.WCSBoundingBoxInfo = QtWidgets.QLabel(self.tab_WCS)
        self.WCSBoundingBoxInfo.setObjectName(_fromUtf8("WCSBoundingBoxInfo"))
        self.tab_WCS_layout.addWidget(self.WCSBoundingBoxInfo)
        self.WCS_Bounds = QtWidgets.QGridLayout()
        self.WCS_Bounds.setObjectName(_fromUtf8("WCS_Bounds"))
        self.WCS_southBound = QtWidgets.QLineEdit(self.tab_WCS)
        self.WCS_southBound.setObjectName(_fromUtf8("WCS_southBound"))
        self.WCS_Bounds.addWidget(self.WCS_southBound, 2, 1, 1, 1)
        self.WCS_northBound = QtWidgets.QLineEdit(self.tab_WCS)
        self.WCS_northBound.setObjectName(_fromUtf8("WCS_northBound"))
        self.WCS_Bounds.addWidget(self.WCS_northBound, 0, 1, 1, 1)
        self.WCS_westBound = QtWidgets.QLineEdit(self.tab_WCS)
        self.WCS_westBound.setObjectName(_fromUtf8("WCS_westBound"))
        self.WCS_Bounds.addWidget(self.WCS_westBound, 1, 0, 1, 1)
        self.WCS_eastBound = QtWidgets.QLineEdit(self.tab_WCS)
        self.WCS_eastBound.setObjectName(_fromUtf8("WCS_eastBound"))
        self.WCS_Bounds.addWidget(self.WCS_eastBound, 1, 2, 1, 1)
        self.tab_WCS_layout.addLayout(self.WCS_Bounds)
        self.gridLayout_6.addLayout(self.tab_WCS_layout, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab_WCS, _fromUtf8(""))
        self.verticalLayout.addWidget(self.tabWidget)
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.button_req_map = QtWidgets.QPushButton(self.scrollAreaWidgetContents_7)
        self.button_req_map.setMaximumSize(QtCore.QSize(256, 23))
        self.button_req_map.setObjectName(_fromUtf8("button_req_map"))
        self.gridLayout_3.addWidget(self.button_req_map, 8, 0, 1, 1)
        self.button_req_animation = QtWidgets.QPushButton(
            self.scrollAreaWidgetContents_7
        )
        self.button_req_animation.setObjectName(_fromUtf8("button_req_animation"))
        self.gridLayout_3.addWidget(self.button_req_animation, 9, 0, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout_3)
        self.gridLayout.addLayout(self.verticalLayout, 3, 0, 1, 1)
        self.combo_dataset_list = QtWidgets.QComboBox(self.scrollAreaWidgetContents_7)
        self.combo_dataset_list.setObjectName(_fromUtf8("combo_dataset_list"))
        self.gridLayout.addWidget(self.combo_dataset_list, 2, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(-1, -1, -1, 5)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.buttonManageServers = QtWidgets.QPushButton(
            self.scrollAreaWidgetContents_7
        )
        self.buttonManageServers.setObjectName(_fromUtf8("buttonManageServers"))
        self.horizontalLayout.addWidget(self.buttonManageServers)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents_7)
        self.verticalLayout_2.addWidget(self.scrollArea)
        THREDDSViewer.setWidget(self.dockWidgetContents)

        self.retranslateUi(THREDDSViewer)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(THREDDSViewer)

    def retranslateUi(self, THREDDSViewer):
        THREDDSViewer.setWindowTitle(
            _translate("THREDDSViewer", "THREDDS Explorer", None)
        )
        self.label.setText(
            _translate("THREDDSViewer", "Choose an available DataSet", None)
        )
        self.tree_widget.headerItem().setText(
            0, _translate("THREDDSViewer", "SubDatasets and Maps", None)
        )
        self.combo_wms_style_type.setToolTip(
            _translate("THREDDSViewer", "Style draw type", None)
        )
        self.combo_wms_style_palette.setToolTip(
            _translate("THREDDSViewer", "Style color palette to use", None)
        )
        self.WMSLabelTimeRange.setText(
            _translate("THREDDSViewer", "Time range to download:", None)
        )
        self.combo_wms_time.setToolTip(
            _translate(
                "THREDDSViewer", "First time value to download for this layer", None
            )
        )
        self.combo_wms_time_last.setToolTip(
            _translate(
                "THREDDSViewer",
                "Last time value to download for this layer\n"
                "(If set, will download all the layers between the first and last times)",
                None,
            )
        )
        self.WMSBoundingBoxInfo.setText(
            _translate("THREDDSViewer", "No bounding box info available", None)
        )
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.tab_WMS),
            _translate("THREDDSViewer", "WMS", None),
        )
        self.WCSLabelTimeRange.setText(
            _translate("THREDDSViewer", "Time range to download:", None)
        )
        self.combo_wcs_time.setToolTip(
            _translate(
                "THREDDSViewer", "First time value to download for this layer", None
            )
        )
        self.combo_wcs_time_last.setToolTip(
            _translate(
                "THREDDSViewer",
                "Last time value to download for this layer\n"
                "(If set, will download all the layers between the first and last times)",
                None,
            )
        )
        self.WCSBoundingBoxInfo.setText(
            _translate("THREDDSViewer", "No bounding box info available", None)
        )
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.tab_WCS),
            _translate("THREDDSViewer", "WCS", None),
        )
        self.button_req_map.setText(
            _translate("THREDDSViewer", "Show map in view", None)
        )
        self.button_req_animation.setText(
            _translate("THREDDSViewer", "Show animation menu >>", None)
        )
        self.buttonManageServers.setText(
            _translate("THREDDSViewer", "Manage servers...", None)
        )
