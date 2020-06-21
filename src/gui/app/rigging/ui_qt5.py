# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '..\ui.ui',
# licensing of '..\ui.ui' applies.
#
# Created: Sun Jun 21 20:48:24 2020
#      by: pyside2-uic  running on PySide2 5.13.1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(282, 426)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        self.houdini_tab = QtWidgets.QWidget()
        self.houdini_tab.setObjectName("houdini_tab")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.houdini_tab)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.tabWidget.addTab(self.houdini_tab, "")
        self.maya_tab = QtWidgets.QWidget()
        self.maya_tab.setObjectName("maya_tab")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.maya_tab)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.tabWidget.addTab(self.maya_tab, "")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.tabWidget.addTab(self.tab, "")
        self.cfg_tab = QtWidgets.QWidget()
        self.cfg_tab.setObjectName("cfg_tab")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.cfg_tab)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.tabWidget.addTab(self.cfg_tab, "")
        self.verticalLayout.addWidget(self.tabWidget)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtWidgets.QApplication.translate("MainWindow", "MK DCC - Rigging", None, -1))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.houdini_tab), QtWidgets.QApplication.translate("MainWindow", "houdini", None, -1))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.maya_tab), QtWidgets.QApplication.translate("MainWindow", "maya", None, -1))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QtWidgets.QApplication.translate("MainWindow", "blender", None, -1))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.cfg_tab), QtWidgets.QApplication.translate("MainWindow", "cfg", None, -1))

