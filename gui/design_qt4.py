# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '..\gui\design.ui'
#
# Created: Wed Mar 18 14:08:12 2020
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_MK_DCC(object):
    def setupUi(self, MK_DCC):
        MK_DCC.setObjectName("MK_DCC")
        MK_DCC.resize(282, 426)
        self.centralwidget = QtGui.QWidget(MK_DCC)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabWidget = QtGui.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        self.maya_tab = QtGui.QWidget()
        self.maya_tab.setObjectName("maya_tab")
        self.horizontalLayout = QtGui.QHBoxLayout(self.maya_tab)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.radioButton = QtGui.QRadioButton(self.maya_tab)
        self.radioButton.setObjectName("radioButton")
        self.horizontalLayout.addWidget(self.radioButton)
        self.pushButton = QtGui.QPushButton(self.maya_tab)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.tabWidget.addTab(self.maya_tab, "")
        self.houdini_tab = QtGui.QWidget()
        self.houdini_tab.setObjectName("houdini_tab")
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.houdini_tab)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.lineEdit = QtGui.QLineEdit(self.houdini_tab)
        self.lineEdit.setObjectName("lineEdit")
        self.verticalLayout_3.addWidget(self.lineEdit)
        self.spinBox = QtGui.QSpinBox(self.houdini_tab)
        self.spinBox.setObjectName("spinBox")
        self.verticalLayout_3.addWidget(self.spinBox)
        self.tabWidget.addTab(self.houdini_tab, "")
        self.cfg_tab = QtGui.QWidget()
        self.cfg_tab.setObjectName("cfg_tab")
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.cfg_tab)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.themes_grpBox = QtGui.QGroupBox(self.cfg_tab)
        self.themes_grpBox.setObjectName("themes_grpBox")
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.themes_grpBox)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.theme_comboBox = QtGui.QComboBox(self.themes_grpBox)
        self.theme_comboBox.setObjectName("theme_comboBox")
        self.theme_comboBox.addItem("")
        self.theme_comboBox.addItem("")
        self.theme_comboBox.addItem("")
        self.theme_comboBox.addItem("")
        self.verticalLayout_2.addWidget(self.theme_comboBox)
        self.verticalLayout_4.addWidget(self.themes_grpBox)
        self.misc_grpBox = QtGui.QGroupBox(self.cfg_tab)
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
        MK_DCC.setWindowTitle(QtGui.QApplication.translate("MK_DCC", "miniTools3", None, QtGui.QApplication.UnicodeUTF8))
        self.radioButton.setText(QtGui.QApplication.translate("MK_DCC", "RadioButton", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("MK_DCC", "PushButton", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.maya_tab), QtGui.QApplication.translate("MK_DCC", "Maya", None, QtGui.QApplication.UnicodeUTF8))
        self.lineEdit.setText(QtGui.QApplication.translate("MK_DCC", "LineEdit", None, QtGui.QApplication.UnicodeUTF8))
        self.spinBox.setPrefix(QtGui.QApplication.translate("MK_DCC", "$ ", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.houdini_tab), QtGui.QApplication.translate("MK_DCC", "Houdini", None, QtGui.QApplication.UnicodeUTF8))
        self.themes_grpBox.setTitle(QtGui.QApplication.translate("MK_DCC", "THEMES", None, QtGui.QApplication.UnicodeUTF8))
        self.theme_comboBox.setItemText(0, QtGui.QApplication.translate("MK_DCC", "Default", None, QtGui.QApplication.UnicodeUTF8))
        self.theme_comboBox.setItemText(1, QtGui.QApplication.translate("MK_DCC", "Aqua", None, QtGui.QApplication.UnicodeUTF8))
        self.theme_comboBox.setItemText(2, QtGui.QApplication.translate("MK_DCC", "Console", None, QtGui.QApplication.UnicodeUTF8))
        self.theme_comboBox.setItemText(3, QtGui.QApplication.translate("MK_DCC", "Ubuntu", None, QtGui.QApplication.UnicodeUTF8))
        self.misc_grpBox.setTitle(QtGui.QApplication.translate("MK_DCC", "MISC.", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.cfg_tab), QtGui.QApplication.translate("MK_DCC", "Cfg", None, QtGui.QApplication.UnicodeUTF8))

