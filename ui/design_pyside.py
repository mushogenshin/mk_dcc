# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '..\ui\design.ui'
#
# Created: Tue Mar 17 18:15:30 2020
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
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabWidget = QtGui.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        self.maya_tab = QtGui.QWidget()
        self.maya_tab.setObjectName("maya_tab")
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.maya_tab)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.pushButton = QtGui.QPushButton(self.maya_tab)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout_2.addWidget(self.pushButton)
        self.radioButton = QtGui.QRadioButton(self.maya_tab)
        self.radioButton.setObjectName("radioButton")
        self.verticalLayout_2.addWidget(self.radioButton)
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
        self.verticalLayout.addWidget(self.tabWidget)
        MK_DCC.setCentralWidget(self.centralwidget)

        self.retranslateUi(MK_DCC)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MK_DCC)

    def retranslateUi(self, MK_DCC):
        MK_DCC.setWindowTitle(QtGui.QApplication.translate("MK_DCC", "miniTools3", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("MK_DCC", "PushButton", None, QtGui.QApplication.UnicodeUTF8))
        self.radioButton.setText(QtGui.QApplication.translate("MK_DCC", "RadioButton", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.maya_tab), QtGui.QApplication.translate("MK_DCC", "Maya", None, QtGui.QApplication.UnicodeUTF8))
        self.lineEdit.setText(QtGui.QApplication.translate("MK_DCC", "LineEdit", None, QtGui.QApplication.UnicodeUTF8))
        self.spinBox.setPrefix(QtGui.QApplication.translate("MK_DCC", "$ ", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.houdini_tab), QtGui.QApplication.translate("MK_DCC", "Houdini", None, QtGui.QApplication.UnicodeUTF8))

