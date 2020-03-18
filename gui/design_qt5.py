# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '..\gui\design.ui',
# licensing of '..\gui\design.ui' applies.
#
# Created: Wed Mar 18 14:08:11 2020
#      by: pyside2-uic  running on PySide2 5.13.1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_MK_DCC(object):
    def setupUi(self, MK_DCC):
        MK_DCC.setObjectName("MK_DCC")
        MK_DCC.resize(282, 426)
        self.centralwidget = QtWidgets.QWidget(MK_DCC)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        self.maya_tab = QtWidgets.QWidget()
        self.maya_tab.setObjectName("maya_tab")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.maya_tab)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.radioButton = QtWidgets.QRadioButton(self.maya_tab)
        self.radioButton.setObjectName("radioButton")
        self.horizontalLayout.addWidget(self.radioButton)
        self.pushButton = QtWidgets.QPushButton(self.maya_tab)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.tabWidget.addTab(self.maya_tab, "")
        self.houdini_tab = QtWidgets.QWidget()
        self.houdini_tab.setObjectName("houdini_tab")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.houdini_tab)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.lineEdit = QtWidgets.QLineEdit(self.houdini_tab)
        self.lineEdit.setObjectName("lineEdit")
        self.verticalLayout_3.addWidget(self.lineEdit)
        self.spinBox = QtWidgets.QSpinBox(self.houdini_tab)
        self.spinBox.setObjectName("spinBox")
        self.verticalLayout_3.addWidget(self.spinBox)
        self.tabWidget.addTab(self.houdini_tab, "")
        self.cfg_tab = QtWidgets.QWidget()
        self.cfg_tab.setObjectName("cfg_tab")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.cfg_tab)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.themes_grpBox = QtWidgets.QGroupBox(self.cfg_tab)
        self.themes_grpBox.setObjectName("themes_grpBox")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.themes_grpBox)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.theme_comboBox = QtWidgets.QComboBox(self.themes_grpBox)
        self.theme_comboBox.setObjectName("theme_comboBox")
        self.theme_comboBox.addItem("")
        self.theme_comboBox.addItem("")
        self.theme_comboBox.addItem("")
        self.theme_comboBox.addItem("")
        self.verticalLayout_2.addWidget(self.theme_comboBox)
        self.verticalLayout_4.addWidget(self.themes_grpBox)
        self.misc_grpBox = QtWidgets.QGroupBox(self.cfg_tab)
        self.misc_grpBox.setObjectName("misc_grpBox")
        self.verticalLayout_4.addWidget(self.misc_grpBox)
        self.tabWidget.addTab(self.cfg_tab, "")
        self.verticalLayout.addWidget(self.tabWidget)
        MK_DCC.setCentralWidget(self.centralwidget)

        self.retranslateUi(MK_DCC)
        self.tabWidget.setCurrentIndex(2)
        self.theme_comboBox.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MK_DCC)

    def retranslateUi(self, MK_DCC):
        MK_DCC.setWindowTitle(QtWidgets.QApplication.translate("MK_DCC", "miniTools3", None, -1))
        self.radioButton.setText(QtWidgets.QApplication.translate("MK_DCC", "RadioButton", None, -1))
        self.pushButton.setText(QtWidgets.QApplication.translate("MK_DCC", "PushButton", None, -1))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.maya_tab), QtWidgets.QApplication.translate("MK_DCC", "Maya", None, -1))
        self.lineEdit.setText(QtWidgets.QApplication.translate("MK_DCC", "LineEdit", None, -1))
        self.spinBox.setPrefix(QtWidgets.QApplication.translate("MK_DCC", "$ ", None, -1))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.houdini_tab), QtWidgets.QApplication.translate("MK_DCC", "Houdini", None, -1))
        self.themes_grpBox.setTitle(QtWidgets.QApplication.translate("MK_DCC", "THEMES", None, -1))
        self.theme_comboBox.setItemText(0, QtWidgets.QApplication.translate("MK_DCC", "Default", None, -1))
        self.theme_comboBox.setItemText(1, QtWidgets.QApplication.translate("MK_DCC", "Aqua", None, -1))
        self.theme_comboBox.setItemText(2, QtWidgets.QApplication.translate("MK_DCC", "Console", None, -1))
        self.theme_comboBox.setItemText(3, QtWidgets.QApplication.translate("MK_DCC", "Ubuntu", None, -1))
        self.misc_grpBox.setTitle(QtWidgets.QApplication.translate("MK_DCC", "MISC.", None, -1))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.cfg_tab), QtWidgets.QApplication.translate("MK_DCC", "Cfg", None, -1))

