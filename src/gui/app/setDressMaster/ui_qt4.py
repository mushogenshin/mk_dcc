# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'F:\dev\git\mk_dcc/src/gui/app/setDressMaster/ui.ui'
#
# Created: Wed Oct  7 17:03:42 2020
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(405, 365)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setStyleSheet("")
        self.centralwidget.setObjectName("centralwidget")
        self.central_widget_layout = QtGui.QVBoxLayout(self.centralwidget)
        self.central_widget_layout.setObjectName("central_widget_layout")
        self.phys_painter_group_box = QtGui.QGroupBox(self.centralwidget)
        font = QtGui.QFont()
        font.setWeight(50)
        font.setBold(False)
        self.phys_painter_group_box.setFont(font)
        self.phys_painter_group_box.setStyleSheet("")
        self.phys_painter_group_box.setAlignment(QtCore.Qt.AlignCenter)
        self.phys_painter_group_box.setObjectName("phys_painter_group_box")
        self.phys_painter_group_box_layout = QtGui.QVBoxLayout(self.phys_painter_group_box)
        self.phys_painter_group_box_layout.setObjectName("phys_painter_group_box_layout")
        self.phys_painter_load_selection_grid_layout = QtGui.QGridLayout()
        self.phys_painter_load_selection_grid_layout.setObjectName("phys_painter_load_selection_grid_layout")
        self.phys_painter_group_box_layout.addLayout(self.phys_painter_load_selection_grid_layout)
        self.setup_mash_network_btn = QtGui.QPushButton(self.phys_painter_group_box)
        self.setup_mash_network_btn.setMinimumSize(QtCore.QSize(0, 40))
        self.setup_mash_network_btn.setObjectName("setup_mash_network_btn")
        self.phys_painter_group_box_layout.addWidget(self.setup_mash_network_btn)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.reset_playback_btn = QtGui.QPushButton(self.phys_painter_group_box)
        self.reset_playback_btn.setObjectName("reset_playback_btn")
        self.horizontalLayout_2.addWidget(self.reset_playback_btn)
        self.pushButton_5 = QtGui.QPushButton(self.phys_painter_group_box)
        self.pushButton_5.setObjectName("pushButton_5")
        self.horizontalLayout_2.addWidget(self.pushButton_5)
        self.toggle_interactive_playback_btn = QtGui.QPushButton(self.phys_painter_group_box)
        self.toggle_interactive_playback_btn.setObjectName("toggle_interactive_playback_btn")
        self.horizontalLayout_2.addWidget(self.toggle_interactive_playback_btn)
        self.phys_painter_group_box_layout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton_2 = QtGui.QPushButton(self.phys_painter_group_box)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout.addWidget(self.pushButton_2)
        self.pushButton_3 = QtGui.QPushButton(self.phys_painter_group_box)
        self.pushButton_3.setObjectName("pushButton_3")
        self.horizontalLayout.addWidget(self.pushButton_3)
        self.phys_painter_group_box_layout.addLayout(self.horizontalLayout)
        self.central_widget_layout.addWidget(self.phys_painter_group_box)
        self.swap_master_group_box = QtGui.QGroupBox(self.centralwidget)
        self.swap_master_group_box.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.swap_master_group_box.sizePolicy().hasHeightForWidth())
        self.swap_master_group_box.setSizePolicy(sizePolicy)
        self.swap_master_group_box.setStyleSheet("")
        self.swap_master_group_box.setAlignment(QtCore.Qt.AlignCenter)
        self.swap_master_group_box.setObjectName("swap_master_group_box")
        self.swap_master_group_box_layout = QtGui.QVBoxLayout(self.swap_master_group_box)
        self.swap_master_group_box_layout.setObjectName("swap_master_group_box_layout")
        self.central_widget_layout.addWidget(self.swap_master_group_box)
        self.restore_instancing_group_box = QtGui.QGroupBox(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.restore_instancing_group_box.sizePolicy().hasHeightForWidth())
        self.restore_instancing_group_box.setSizePolicy(sizePolicy)
        self.restore_instancing_group_box.setAlignment(QtCore.Qt.AlignCenter)
        self.restore_instancing_group_box.setObjectName("restore_instancing_group_box")
        self.restore_instancing_group_box_layout = QtGui.QVBoxLayout(self.restore_instancing_group_box)
        self.restore_instancing_group_box_layout.setObjectName("restore_instancing_group_box_layout")
        self.central_widget_layout.addWidget(self.restore_instancing_group_box)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Set Dress Master", None, QtGui.QApplication.UnicodeUTF8))
        self.phys_painter_group_box.setTitle(QtGui.QApplication.translate("MainWindow", "PHYSX PAINTER", None, QtGui.QApplication.UnicodeUTF8))
        self.setup_mash_network_btn.setText(QtGui.QApplication.translate("MainWindow", "Setup MASH Network", None, QtGui.QApplication.UnicodeUTF8))
        self.reset_playback_btn.setText(QtGui.QApplication.translate("MainWindow", "Go to Time Zero", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_5.setText(QtGui.QApplication.translate("MainWindow", "Show Paint Node", None, QtGui.QApplication.UnicodeUTF8))
        self.toggle_interactive_playback_btn.setText(QtGui.QApplication.translate("MainWindow", "Interactive Playback", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_2.setText(QtGui.QApplication.translate("MainWindow", "Bake Current", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_3.setText(QtGui.QApplication.translate("MainWindow", "Delete All Setup", None, QtGui.QApplication.UnicodeUTF8))
        self.swap_master_group_box.setTitle(QtGui.QApplication.translate("MainWindow", "SWAP MASTER", None, QtGui.QApplication.UnicodeUTF8))
        self.restore_instancing_group_box.setTitle(QtGui.QApplication.translate("MainWindow", "RESTORE INSTANCING", None, QtGui.QApplication.UnicodeUTF8))

