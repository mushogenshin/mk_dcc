# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'F:\dev\git\mk_dcc/src/gui/app/setDressMaster/ui.ui',
# licensing of 'F:\dev\git\mk_dcc/src/gui/app/setDressMaster/ui.ui' applies.
#
# Created: Thu Oct  8 03:19:07 2020
#      by: pyside2-uic  running on PySide2 5.13.1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(405, 365)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setStyleSheet("")
        self.centralwidget.setObjectName("centralwidget")
        self.central_widget_layout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.central_widget_layout.setObjectName("central_widget_layout")
        self.phys_painter_group_box = QtWidgets.QGroupBox(self.centralwidget)
        font = QtGui.QFont()
        font.setWeight(50)
        font.setBold(False)
        self.phys_painter_group_box.setFont(font)
        self.phys_painter_group_box.setStyleSheet("")
        self.phys_painter_group_box.setAlignment(QtCore.Qt.AlignCenter)
        self.phys_painter_group_box.setObjectName("phys_painter_group_box")
        self.phys_painter_group_box_layout = QtWidgets.QVBoxLayout(self.phys_painter_group_box)
        self.phys_painter_group_box_layout.setObjectName("phys_painter_group_box_layout")
        self.phys_painter_load_selection_grid_layout = QtWidgets.QGridLayout()
        self.phys_painter_load_selection_grid_layout.setObjectName("phys_painter_load_selection_grid_layout")
        self.phys_painter_group_box_layout.addLayout(self.phys_painter_load_selection_grid_layout)
        self.setup_mash_network_btn = QtWidgets.QPushButton(self.phys_painter_group_box)
        self.setup_mash_network_btn.setMinimumSize(QtCore.QSize(0, 40))
        self.setup_mash_network_btn.setObjectName("setup_mash_network_btn")
        self.phys_painter_group_box_layout.addWidget(self.setup_mash_network_btn)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.reset_playback_btn = QtWidgets.QPushButton(self.phys_painter_group_box)
        self.reset_playback_btn.setObjectName("reset_playback_btn")
        self.horizontalLayout_2.addWidget(self.reset_playback_btn)
        self.show_paint_node_btn = QtWidgets.QPushButton(self.phys_painter_group_box)
        self.show_paint_node_btn.setObjectName("show_paint_node_btn")
        self.horizontalLayout_2.addWidget(self.show_paint_node_btn)
        self.toggle_interactive_playback_btn = QtWidgets.QPushButton(self.phys_painter_group_box)
        self.toggle_interactive_playback_btn.setObjectName("toggle_interactive_playback_btn")
        self.horizontalLayout_2.addWidget(self.toggle_interactive_playback_btn)
        self.phys_painter_group_box_layout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton = QtWidgets.QPushButton(self.phys_painter_group_box)
        self.pushButton.setEnabled(False)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.pushButton_2 = QtWidgets.QPushButton(self.phys_painter_group_box)
        self.pushButton_2.setEnabled(False)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout.addWidget(self.pushButton_2)
        self.pushButton_3 = QtWidgets.QPushButton(self.phys_painter_group_box)
        self.pushButton_3.setEnabled(False)
        self.pushButton_3.setObjectName("pushButton_3")
        self.horizontalLayout.addWidget(self.pushButton_3)
        self.phys_painter_group_box_layout.addLayout(self.horizontalLayout)
        self.central_widget_layout.addWidget(self.phys_painter_group_box)
        self.swap_master_group_box = QtWidgets.QGroupBox(self.centralwidget)
        self.swap_master_group_box.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.swap_master_group_box.sizePolicy().hasHeightForWidth())
        self.swap_master_group_box.setSizePolicy(sizePolicy)
        self.swap_master_group_box.setStyleSheet("")
        self.swap_master_group_box.setAlignment(QtCore.Qt.AlignCenter)
        self.swap_master_group_box.setObjectName("swap_master_group_box")
        self.swap_master_group_box_layout = QtWidgets.QVBoxLayout(self.swap_master_group_box)
        self.swap_master_group_box_layout.setObjectName("swap_master_group_box_layout")
        self.central_widget_layout.addWidget(self.swap_master_group_box)
        self.restore_instancing_group_box = QtWidgets.QGroupBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.restore_instancing_group_box.sizePolicy().hasHeightForWidth())
        self.restore_instancing_group_box.setSizePolicy(sizePolicy)
        self.restore_instancing_group_box.setAlignment(QtCore.Qt.AlignCenter)
        self.restore_instancing_group_box.setObjectName("restore_instancing_group_box")
        self.restore_instancing_group_box_layout = QtWidgets.QVBoxLayout(self.restore_instancing_group_box)
        self.restore_instancing_group_box_layout.setObjectName("restore_instancing_group_box_layout")
        self.central_widget_layout.addWidget(self.restore_instancing_group_box)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtWidgets.QApplication.translate("MainWindow", "Set Dress Master", None, -1))
        self.phys_painter_group_box.setTitle(QtWidgets.QApplication.translate("MainWindow", "PHYSX PAINTER", None, -1))
        self.setup_mash_network_btn.setText(QtWidgets.QApplication.translate("MainWindow", "Setup MASH Network", None, -1))
        self.reset_playback_btn.setText(QtWidgets.QApplication.translate("MainWindow", "Go to Time Zero", None, -1))
        self.show_paint_node_btn.setText(QtWidgets.QApplication.translate("MainWindow", "Show Paint Node", None, -1))
        self.toggle_interactive_playback_btn.setText(QtWidgets.QApplication.translate("MainWindow", "Interactive Playback", None, -1))
        self.pushButton.setText(QtWidgets.QApplication.translate("MainWindow", "Show Instancer Node", None, -1))
        self.pushButton_2.setText(QtWidgets.QApplication.translate("MainWindow", "Bake Current", None, -1))
        self.pushButton_3.setText(QtWidgets.QApplication.translate("MainWindow", "Delete All Setup", None, -1))
        self.swap_master_group_box.setTitle(QtWidgets.QApplication.translate("MainWindow", "SWAP MASTER", None, -1))
        self.restore_instancing_group_box.setTitle(QtWidgets.QApplication.translate("MainWindow", "RESTORE INSTANCING", None, -1))

