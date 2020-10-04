# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '..\ui.ui'
#
# Created: Sun Oct  4 20:41:27 2020
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
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox_4 = QtGui.QGroupBox(self.centralwidget)
        self.groupBox_4.setObjectName("groupBox_4")
        self.verticalLayout_9 = QtGui.QVBoxLayout(self.groupBox_4)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.pushButton_2 = QtGui.QPushButton(self.groupBox_4)
        self.pushButton_2.setObjectName("pushButton_2")
        self.verticalLayout_9.addWidget(self.pushButton_2)
        self.radioButton = QtGui.QRadioButton(self.groupBox_4)
        self.radioButton.setObjectName("radioButton")
        self.verticalLayout_9.addWidget(self.radioButton)
        self.verticalLayout.addWidget(self.groupBox_4)
        self.groupBox_5 = QtGui.QGroupBox(self.centralwidget)
        self.groupBox_5.setObjectName("groupBox_5")
        self.verticalLayout_10 = QtGui.QVBoxLayout(self.groupBox_5)
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.pushButton_3 = QtGui.QPushButton(self.groupBox_5)
        self.pushButton_3.setObjectName("pushButton_3")
        self.verticalLayout_10.addWidget(self.pushButton_3)
        self.radioButton_2 = QtGui.QRadioButton(self.groupBox_5)
        self.radioButton_2.setObjectName("radioButton_2")
        self.verticalLayout_10.addWidget(self.radioButton_2)
        self.verticalLayout.addWidget(self.groupBox_5)
        self.groupBox_3 = QtGui.QGroupBox(self.centralwidget)
        self.groupBox_3.setObjectName("groupBox_3")
        self.verticalLayout_8 = QtGui.QVBoxLayout(self.groupBox_3)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.pushButton = QtGui.QPushButton(self.groupBox_3)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout_8.addWidget(self.pushButton)
        self.radioButton_3 = QtGui.QRadioButton(self.groupBox_3)
        self.radioButton_3.setObjectName("radioButton_3")
        self.verticalLayout_8.addWidget(self.radioButton_3)
        self.verticalLayout.addWidget(self.groupBox_3)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "SetDressMaster", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_4.setTitle(QtGui.QApplication.translate("MainWindow", "PHYSX PAINTER", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_2.setText(QtGui.QApplication.translate("MainWindow", "PushButton", None, QtGui.QApplication.UnicodeUTF8))
        self.radioButton.setText(QtGui.QApplication.translate("MainWindow", "RadioButton", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_5.setTitle(QtGui.QApplication.translate("MainWindow", "SWAP MASTER", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_3.setText(QtGui.QApplication.translate("MainWindow", "PushButton", None, QtGui.QApplication.UnicodeUTF8))
        self.radioButton_2.setText(QtGui.QApplication.translate("MainWindow", "RadioButton", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_3.setTitle(QtGui.QApplication.translate("MainWindow", "RESTORE INSTANCING", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("MainWindow", "PushButton", None, QtGui.QApplication.UnicodeUTF8))
        self.radioButton_3.setText(QtGui.QApplication.translate("MainWindow", "RadioButton", None, QtGui.QApplication.UnicodeUTF8))

