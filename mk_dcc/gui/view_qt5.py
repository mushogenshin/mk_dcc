# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'view.ui'
##
## Created by: Qt User Interface Compiler version 5.14.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import (QCoreApplication, QDate, QDateTime, QMetaObject,
    QObject, QPoint, QRect, QSize, QTime, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter,
    QPixmap, QRadialGradient)
from PySide2.QtWidgets import *


class Ui_MK_DCC(object):
    def setupUi(self, MK_DCC):
        if not MK_DCC.objectName():
            MK_DCC.setObjectName(u"MK_DCC")
        MK_DCC.resize(282, 426)
        self.centralwidget = QWidget(MK_DCC)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.maya_tab = QWidget()
        self.maya_tab.setObjectName(u"maya_tab")
        self.verticalLayout_7 = QVBoxLayout(self.maya_tab)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.groupBox_4 = QGroupBox(self.maya_tab)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.verticalLayout_9 = QVBoxLayout(self.groupBox_4)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.pushButton_2 = QPushButton(self.groupBox_4)
        self.pushButton_2.setObjectName(u"pushButton_2")

        self.verticalLayout_9.addWidget(self.pushButton_2)

        self.radioButton = QRadioButton(self.groupBox_4)
        self.radioButton.setObjectName(u"radioButton")

        self.verticalLayout_9.addWidget(self.radioButton)


        self.verticalLayout_7.addWidget(self.groupBox_4)

        self.groupBox_3 = QGroupBox(self.maya_tab)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.verticalLayout_8 = QVBoxLayout(self.groupBox_3)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.pushButton = QPushButton(self.groupBox_3)
        self.pushButton.setObjectName(u"pushButton")

        self.verticalLayout_8.addWidget(self.pushButton)


        self.verticalLayout_7.addWidget(self.groupBox_3)

        self.tabWidget.addTab(self.maya_tab, "")
        self.houdini_tab = QWidget()
        self.houdini_tab.setObjectName(u"houdini_tab")
        self.verticalLayout_3 = QVBoxLayout(self.houdini_tab)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.groupBox = QGroupBox(self.houdini_tab)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout_5 = QVBoxLayout(self.groupBox)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.lineEdit = QLineEdit(self.groupBox)
        self.lineEdit.setObjectName(u"lineEdit")

        self.verticalLayout_5.addWidget(self.lineEdit)


        self.verticalLayout_3.addWidget(self.groupBox)

        self.groupBox_2 = QGroupBox(self.houdini_tab)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.verticalLayout_6 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.spinBox = QSpinBox(self.groupBox_2)
        self.spinBox.setObjectName(u"spinBox")

        self.verticalLayout_6.addWidget(self.spinBox)


        self.verticalLayout_3.addWidget(self.groupBox_2)

        self.tabWidget.addTab(self.houdini_tab, "")
        self.cfg_tab = QWidget()
        self.cfg_tab.setObjectName(u"cfg_tab")
        self.verticalLayout_4 = QVBoxLayout(self.cfg_tab)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.themes_grpBox = QGroupBox(self.cfg_tab)
        self.themes_grpBox.setObjectName(u"themes_grpBox")
        self.verticalLayout_2 = QVBoxLayout(self.themes_grpBox)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.theme_comboBox = QComboBox(self.themes_grpBox)
        self.theme_comboBox.addItem("")
        self.theme_comboBox.addItem("")
        self.theme_comboBox.addItem("")
        self.theme_comboBox.addItem("")
        self.theme_comboBox.setObjectName(u"theme_comboBox")

        self.verticalLayout_2.addWidget(self.theme_comboBox)


        self.verticalLayout_4.addWidget(self.themes_grpBox)

        self.misc_grpBox = QGroupBox(self.cfg_tab)
        self.misc_grpBox.setObjectName(u"misc_grpBox")

        self.verticalLayout_4.addWidget(self.misc_grpBox)

        self.tabWidget.addTab(self.cfg_tab, "")

        self.verticalLayout.addWidget(self.tabWidget)

        MK_DCC.setCentralWidget(self.centralwidget)

        self.retranslateUi(MK_DCC)

        self.tabWidget.setCurrentIndex(0)
        self.theme_comboBox.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MK_DCC)
    # setupUi

    def retranslateUi(self, MK_DCC):
        MK_DCC.setWindowTitle(QCoreApplication.translate("MK_DCC", u"miniTools3", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("MK_DCC", u"UDIM", None))
        self.pushButton_2.setText(QCoreApplication.translate("MK_DCC", u"PushButton", None))
        self.radioButton.setText(QCoreApplication.translate("MK_DCC", u"RadioButton", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("MK_DCC", u"LEGACY", None))
        self.pushButton.setText(QCoreApplication.translate("MK_DCC", u"PushButton", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.maya_tab), QCoreApplication.translate("MK_DCC", u"maya", None))
        self.groupBox.setTitle(QCoreApplication.translate("MK_DCC", u"SOLARIS", None))
        self.lineEdit.setText(QCoreApplication.translate("MK_DCC", u"LineEdit", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("MK_DCC", u"PDG", None))
        self.spinBox.setPrefix(QCoreApplication.translate("MK_DCC", u"$ ", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.houdini_tab), QCoreApplication.translate("MK_DCC", u"houdini", None))
        self.themes_grpBox.setTitle(QCoreApplication.translate("MK_DCC", u"THEMES", None))
        self.theme_comboBox.setItemText(0, QCoreApplication.translate("MK_DCC", u"Default", None))
        self.theme_comboBox.setItemText(1, QCoreApplication.translate("MK_DCC", u"Aqua", None))
        self.theme_comboBox.setItemText(2, QCoreApplication.translate("MK_DCC", u"Console", None))
        self.theme_comboBox.setItemText(3, QCoreApplication.translate("MK_DCC", u"Ubuntu", None))

        self.misc_grpBox.setTitle(QCoreApplication.translate("MK_DCC", u"MISC.", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.cfg_tab), QCoreApplication.translate("MK_DCC", u"cfg", None))
    # retranslateUi

