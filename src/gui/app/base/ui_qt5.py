# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '..\ui.ui',
# licensing of '..\ui.ui' applies.
#
# Created: Tue Oct  6 03:06:03 2020
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
        self.central_widget_layout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.central_widget_layout.setContentsMargins(0, 0, 0, 0)
        self.central_widget_layout.setObjectName("central_widget_layout")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        self.houdini_tab = QtWidgets.QWidget()
        self.houdini_tab.setObjectName("houdini_tab")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.houdini_tab)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.groupBox = QtWidgets.QGroupBox(self.houdini_tab)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.lineEdit = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit.setObjectName("lineEdit")
        self.verticalLayout_5.addWidget(self.lineEdit)
        self.verticalLayout_3.addWidget(self.groupBox)
        self.groupBox_2 = QtWidgets.QGroupBox(self.houdini_tab)
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.spinBox = QtWidgets.QSpinBox(self.groupBox_2)
        self.spinBox.setObjectName("spinBox")
        self.verticalLayout_6.addWidget(self.spinBox)
        self.verticalLayout_3.addWidget(self.groupBox_2)
        self.tabWidget.addTab(self.houdini_tab, "")
        self.maya_tab = QtWidgets.QWidget()
        self.maya_tab.setObjectName("maya_tab")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.maya_tab)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.groupBox_4 = QtWidgets.QGroupBox(self.maya_tab)
        self.groupBox_4.setObjectName("groupBox_4")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(self.groupBox_4)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.pushButton_2 = QtWidgets.QPushButton(self.groupBox_4)
        self.pushButton_2.setObjectName("pushButton_2")
        self.verticalLayout_9.addWidget(self.pushButton_2)
        self.radioButton = QtWidgets.QRadioButton(self.groupBox_4)
        self.radioButton.setObjectName("radioButton")
        self.verticalLayout_9.addWidget(self.radioButton)
        self.verticalLayout_7.addWidget(self.groupBox_4)
        self.groupBox_3 = QtWidgets.QGroupBox(self.maya_tab)
        self.groupBox_3.setObjectName("groupBox_3")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.groupBox_3)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.pushButton = QtWidgets.QPushButton(self.groupBox_3)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout_8.addWidget(self.pushButton)
        self.verticalLayout_7.addWidget(self.groupBox_3)
        self.tabWidget.addTab(self.maya_tab, "")
        self.blender_tab = QtWidgets.QWidget()
        self.blender_tab.setObjectName("blender_tab")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.blender_tab)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.themes_grpBox = QtWidgets.QGroupBox(self.blender_tab)
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
        self.misc_grpBox = QtWidgets.QGroupBox(self.blender_tab)
        self.misc_grpBox.setObjectName("misc_grpBox")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.misc_grpBox)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.plainTextEdit = QtWidgets.QPlainTextEdit(self.misc_grpBox)
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.horizontalLayout.addWidget(self.plainTextEdit)
        self.verticalLayout_4.addWidget(self.misc_grpBox)
        self.tabWidget.addTab(self.blender_tab, "")
        self.central_widget_layout.addWidget(self.tabWidget)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        self.theme_comboBox.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtWidgets.QApplication.translate("MainWindow", "MK DCC - Base", None, -1))
        self.groupBox.setTitle(QtWidgets.QApplication.translate("MainWindow", "SOLARIS", None, -1))
        self.lineEdit.setText(QtWidgets.QApplication.translate("MainWindow", "LineEdit", None, -1))
        self.groupBox_2.setTitle(QtWidgets.QApplication.translate("MainWindow", "PDG", None, -1))
        self.spinBox.setPrefix(QtWidgets.QApplication.translate("MainWindow", "$ ", None, -1))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.houdini_tab), QtWidgets.QApplication.translate("MainWindow", "houdini", None, -1))
        self.groupBox_4.setTitle(QtWidgets.QApplication.translate("MainWindow", "UDIM", None, -1))
        self.pushButton_2.setText(QtWidgets.QApplication.translate("MainWindow", "PushButton", None, -1))
        self.radioButton.setText(QtWidgets.QApplication.translate("MainWindow", "RadioButton", None, -1))
        self.groupBox_3.setTitle(QtWidgets.QApplication.translate("MainWindow", "LEGACY", None, -1))
        self.pushButton.setText(QtWidgets.QApplication.translate("MainWindow", "PushButton", None, -1))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.maya_tab), QtWidgets.QApplication.translate("MainWindow", "maya", None, -1))
        self.themes_grpBox.setTitle(QtWidgets.QApplication.translate("MainWindow", "THEMES", None, -1))
        self.theme_comboBox.setItemText(0, QtWidgets.QApplication.translate("MainWindow", "Default", None, -1))
        self.theme_comboBox.setItemText(1, QtWidgets.QApplication.translate("MainWindow", "Aqua", None, -1))
        self.theme_comboBox.setItemText(2, QtWidgets.QApplication.translate("MainWindow", "Console", None, -1))
        self.theme_comboBox.setItemText(3, QtWidgets.QApplication.translate("MainWindow", "Ubuntu", None, -1))
        self.misc_grpBox.setTitle(QtWidgets.QApplication.translate("MainWindow", "MISC.", None, -1))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.blender_tab), QtWidgets.QApplication.translate("MainWindow", "blender", None, -1))

