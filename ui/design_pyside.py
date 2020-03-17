# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '..\ui\design.ui'
#
# Created: Tue Mar 17 16:54:47 2020
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_MK_DCC(object):
    def setupUi(self, MK_DCC):
        MK_DCC.setObjectName("MK_DCC")
        MK_DCC.resize(320, 240)
        self.centralwidget = QtGui.QWidget(MK_DCC)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton = QtGui.QPushButton(self.centralwidget)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.pushButton_2 = QtGui.QPushButton(self.centralwidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout.addWidget(self.pushButton_2)
        MK_DCC.setCentralWidget(self.centralwidget)

        self.retranslateUi(MK_DCC)
        QtCore.QMetaObject.connectSlotsByName(MK_DCC)

    def retranslateUi(self, MK_DCC):
        MK_DCC.setWindowTitle(QtGui.QApplication.translate("MK_DCC", "miniTools3", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("MK_DCC", "Press me!", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_2.setText(QtGui.QApplication.translate("MK_DCC", "Press me, too!", None, QtGui.QApplication.UnicodeUTF8))

