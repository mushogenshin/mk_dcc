# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '..\ui\design.ui',
# licensing of '..\ui\design.ui' applies.
#
# Created: Tue Mar 17 16:51:32 2020
#      by: pyside2-uic  running on PySide2 5.13.1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_MK_DCC(object):
    def setupUi(self, MK_DCC):
        MK_DCC.setObjectName("MK_DCC")
        MK_DCC.resize(320, 240)
        self.centralwidget = QtWidgets.QWidget(MK_DCC)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout.addWidget(self.pushButton_2)
        MK_DCC.setCentralWidget(self.centralwidget)

        self.retranslateUi(MK_DCC)
        QtCore.QMetaObject.connectSlotsByName(MK_DCC)

    def retranslateUi(self, MK_DCC):
        MK_DCC.setWindowTitle(QtWidgets.QApplication.translate("MK_DCC", "miniTools3", None, -1))
        self.pushButton.setText(QtWidgets.QApplication.translate("MK_DCC", "Press me!", None, -1))
        self.pushButton_2.setText(QtWidgets.QApplication.translate("MK_DCC", "Press me, too!", None, -1))

