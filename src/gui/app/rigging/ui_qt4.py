# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '..\ui.ui'
#
# Created: Tue Oct  6 03:06:14 2020
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(282, 426)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.central_widget_layout = QtGui.QVBoxLayout(self.centralwidget)
        self.central_widget_layout.setContentsMargins(0, 0, 0, 0)
        self.central_widget_layout.setObjectName("central_widget_layout")
        self.tabWidget = QtGui.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        self.houdini_tab = QtGui.QWidget()
        self.houdini_tab.setObjectName("houdini_tab")
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.houdini_tab)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.tabWidget.addTab(self.houdini_tab, "")
        self.maya_tab = QtGui.QWidget()
        self.maya_tab.setObjectName("maya_tab")
        self.verticalLayout_7 = QtGui.QVBoxLayout(self.maya_tab)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.tabWidget.addTab(self.maya_tab, "")
        self.tab = QtGui.QWidget()
        self.tab.setObjectName("tab")
        self.tabWidget.addTab(self.tab, "")
        self.cfg_tab = QtGui.QWidget()
        self.cfg_tab.setObjectName("cfg_tab")
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.cfg_tab)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.tabWidget.addTab(self.cfg_tab, "")
        self.central_widget_layout.addWidget(self.tabWidget)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MK DCC - Rigging", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.houdini_tab), QtGui.QApplication.translate("MainWindow", "houdini", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.maya_tab), QtGui.QApplication.translate("MainWindow", "maya", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QtGui.QApplication.translate("MainWindow", "blender", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.cfg_tab), QtGui.QApplication.translate("MainWindow", "cfg", None, QtGui.QApplication.UnicodeUTF8))

