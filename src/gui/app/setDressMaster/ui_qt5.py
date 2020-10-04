# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '..\ui.ui',
# licensing of '..\ui.ui' applies.
#
# Created: Sun Oct  4 20:41:18 2020
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
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox_4 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_4.setObjectName("groupBox_4")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(self.groupBox_4)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.pushButton_2 = QtWidgets.QPushButton(self.groupBox_4)
        self.pushButton_2.setObjectName("pushButton_2")
        self.verticalLayout_9.addWidget(self.pushButton_2)
        self.radioButton = QtWidgets.QRadioButton(self.groupBox_4)
        self.radioButton.setObjectName("radioButton")
        self.verticalLayout_9.addWidget(self.radioButton)
        self.verticalLayout.addWidget(self.groupBox_4)
        self.groupBox_5 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_5.setObjectName("groupBox_5")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout(self.groupBox_5)
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.pushButton_3 = QtWidgets.QPushButton(self.groupBox_5)
        self.pushButton_3.setObjectName("pushButton_3")
        self.verticalLayout_10.addWidget(self.pushButton_3)
        self.radioButton_2 = QtWidgets.QRadioButton(self.groupBox_5)
        self.radioButton_2.setObjectName("radioButton_2")
        self.verticalLayout_10.addWidget(self.radioButton_2)
        self.verticalLayout.addWidget(self.groupBox_5)
        self.groupBox_3 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_3.setObjectName("groupBox_3")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.groupBox_3)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.pushButton = QtWidgets.QPushButton(self.groupBox_3)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout_8.addWidget(self.pushButton)
        self.radioButton_3 = QtWidgets.QRadioButton(self.groupBox_3)
        self.radioButton_3.setObjectName("radioButton_3")
        self.verticalLayout_8.addWidget(self.radioButton_3)
        self.verticalLayout.addWidget(self.groupBox_3)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtWidgets.QApplication.translate("MainWindow", "SetDressMaster", None, -1))
        self.groupBox_4.setTitle(QtWidgets.QApplication.translate("MainWindow", "PHYSX PAINTER", None, -1))
        self.pushButton_2.setText(QtWidgets.QApplication.translate("MainWindow", "PushButton", None, -1))
        self.radioButton.setText(QtWidgets.QApplication.translate("MainWindow", "RadioButton", None, -1))
        self.groupBox_5.setTitle(QtWidgets.QApplication.translate("MainWindow", "SWAP MASTER", None, -1))
        self.pushButton_3.setText(QtWidgets.QApplication.translate("MainWindow", "PushButton", None, -1))
        self.radioButton_2.setText(QtWidgets.QApplication.translate("MainWindow", "RadioButton", None, -1))
        self.groupBox_3.setTitle(QtWidgets.QApplication.translate("MainWindow", "RESTORE INSTANCING", None, -1))
        self.pushButton.setText(QtWidgets.QApplication.translate("MainWindow", "PushButton", None, -1))
        self.radioButton_3.setText(QtWidgets.QApplication.translate("MainWindow", "RadioButton", None, -1))

