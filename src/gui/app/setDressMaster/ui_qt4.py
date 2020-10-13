# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'F:\dev\git\mk_dcc/src/gui/app/setDressMaster/ui.ui'
#
# Created: Tue Oct 13 14:39:24 2020
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(373, 428)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setStyleSheet("")
        self.centralwidget.setObjectName("centralwidget")
        self.central_widget_layout = QtGui.QVBoxLayout(self.centralwidget)
        self.central_widget_layout.setObjectName("central_widget_layout")
        self.phys_painter_main_group_box = QtGui.QGroupBox(self.centralwidget)
        font = QtGui.QFont()
        font.setWeight(50)
        font.setBold(False)
        self.phys_painter_main_group_box.setFont(font)
        self.phys_painter_main_group_box.setStyleSheet("")
        self.phys_painter_main_group_box.setAlignment(QtCore.Qt.AlignCenter)
        self.phys_painter_main_group_box.setObjectName("phys_painter_main_group_box")
        self.phys_painter_group_box_layout = QtGui.QVBoxLayout(self.phys_painter_main_group_box)
        self.phys_painter_group_box_layout.setObjectName("phys_painter_group_box_layout")
        self.PP_load_selection_grid_layout = QtGui.QGridLayout()
        self.PP_load_selection_grid_layout.setObjectName("PP_load_selection_grid_layout")
        self.phys_painter_group_box_layout.addLayout(self.PP_load_selection_grid_layout)
        self.PP_dyn_parms_child_group_box = QtGui.QGroupBox(self.phys_painter_main_group_box)
        self.PP_dyn_parms_child_group_box.setAlignment(QtCore.Qt.AlignCenter)
        self.PP_dyn_parms_child_group_box.setCheckable(True)
        self.PP_dyn_parms_child_group_box.setObjectName("PP_dyn_parms_child_group_box")
        self.PP_dynamic_parameters_grid_layout = QtGui.QGridLayout(self.PP_dyn_parms_child_group_box)
        self.PP_dynamic_parameters_grid_layout.setObjectName("PP_dynamic_parameters_grid_layout")
        self.phys_painter_group_box_layout.addWidget(self.PP_dyn_parms_child_group_box)
        self.PP_setup_mash_network_btn = QtGui.QPushButton(self.phys_painter_main_group_box)
        self.PP_setup_mash_network_btn.setMinimumSize(QtCore.QSize(0, 40))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/baseline_wb_iridescent_white_48dp.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.PP_setup_mash_network_btn.setIcon(icon)
        self.PP_setup_mash_network_btn.setIconSize(QtCore.QSize(24, 24))
        self.PP_setup_mash_network_btn.setObjectName("PP_setup_mash_network_btn")
        self.phys_painter_group_box_layout.addWidget(self.PP_setup_mash_network_btn)
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.PP_toggle_interactive_playback_btn = QtGui.QToolButton(self.phys_painter_main_group_box)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.PP_toggle_interactive_playback_btn.sizePolicy().hasHeightForWidth())
        self.PP_toggle_interactive_playback_btn.setSizePolicy(sizePolicy)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/baseline_play_circle_outline_white_48dp.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.PP_toggle_interactive_playback_btn.setIcon(icon1)
        self.PP_toggle_interactive_playback_btn.setIconSize(QtCore.QSize(32, 32))
        self.PP_toggle_interactive_playback_btn.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.PP_toggle_interactive_playback_btn.setObjectName("PP_toggle_interactive_playback_btn")
        self.gridLayout.addWidget(self.PP_toggle_interactive_playback_btn, 0, 2, 1, 1)
        self.PP_show_paint_node_btn = QtGui.QToolButton(self.phys_painter_main_group_box)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.PP_show_paint_node_btn.sizePolicy().hasHeightForWidth())
        self.PP_show_paint_node_btn.setSizePolicy(sizePolicy)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icons/baseline_brush_white_48dp.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.PP_show_paint_node_btn.setIcon(icon2)
        self.PP_show_paint_node_btn.setIconSize(QtCore.QSize(32, 32))
        self.PP_show_paint_node_btn.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.PP_show_paint_node_btn.setObjectName("PP_show_paint_node_btn")
        self.gridLayout.addWidget(self.PP_show_paint_node_btn, 0, 1, 1, 1)
        self.PP_reset_playback_btn = QtGui.QToolButton(self.phys_painter_main_group_box)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.PP_reset_playback_btn.sizePolicy().hasHeightForWidth())
        self.PP_reset_playback_btn.setSizePolicy(sizePolicy)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/icons/baseline_exposure_zero_white_48dp.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.PP_reset_playback_btn.setIcon(icon3)
        self.PP_reset_playback_btn.setIconSize(QtCore.QSize(32, 32))
        self.PP_reset_playback_btn.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.PP_reset_playback_btn.setObjectName("PP_reset_playback_btn")
        self.gridLayout.addWidget(self.PP_reset_playback_btn, 0, 0, 1, 1)
        self.PP_show_instancer_node_btn = QtGui.QToolButton(self.phys_painter_main_group_box)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.PP_show_instancer_node_btn.sizePolicy().hasHeightForWidth())
        self.PP_show_instancer_node_btn.setSizePolicy(sizePolicy)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/icons/baseline_list_alt_white_48dp.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.PP_show_instancer_node_btn.setIcon(icon4)
        self.PP_show_instancer_node_btn.setIconSize(QtCore.QSize(32, 32))
        self.PP_show_instancer_node_btn.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.PP_show_instancer_node_btn.setObjectName("PP_show_instancer_node_btn")
        self.gridLayout.addWidget(self.PP_show_instancer_node_btn, 1, 0, 1, 1)
        self.PP_bake_current_btn = QtGui.QToolButton(self.phys_painter_main_group_box)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.PP_bake_current_btn.sizePolicy().hasHeightForWidth())
        self.PP_bake_current_btn.setSizePolicy(sizePolicy)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/icons/baseline_save_alt_white_48dp.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.PP_bake_current_btn.setIcon(icon5)
        self.PP_bake_current_btn.setIconSize(QtCore.QSize(32, 32))
        self.PP_bake_current_btn.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.PP_bake_current_btn.setObjectName("PP_bake_current_btn")
        self.gridLayout.addWidget(self.PP_bake_current_btn, 1, 1, 1, 1)
        self.toolButton_3 = QtGui.QToolButton(self.phys_painter_main_group_box)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toolButton_3.sizePolicy().hasHeightForWidth())
        self.toolButton_3.setSizePolicy(sizePolicy)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":/icons/baseline_waves_white_48dp.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolButton_3.setIcon(icon6)
        self.toolButton_3.setIconSize(QtCore.QSize(32, 32))
        self.toolButton_3.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.toolButton_3.setObjectName("toolButton_3")
        self.gridLayout.addWidget(self.toolButton_3, 1, 2, 1, 1)
        self.phys_painter_group_box_layout.addLayout(self.gridLayout)
        self.PP_delete_all_setup_btn = QtGui.QPushButton(self.phys_painter_main_group_box)
        self.PP_delete_all_setup_btn.setEnabled(True)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(":/icons/baseline_clear_white_48dp.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.PP_delete_all_setup_btn.setIcon(icon7)
        self.PP_delete_all_setup_btn.setIconSize(QtCore.QSize(24, 24))
        self.PP_delete_all_setup_btn.setObjectName("PP_delete_all_setup_btn")
        self.phys_painter_group_box_layout.addWidget(self.PP_delete_all_setup_btn)
        self.central_widget_layout.addWidget(self.phys_painter_main_group_box)
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
        self.phys_painter_main_group_box.setTitle(QtGui.QApplication.translate("MainWindow", "PHYSX PAINTER", None, QtGui.QApplication.UnicodeUTF8))
        self.PP_dyn_parms_child_group_box.setTitle(QtGui.QApplication.translate("MainWindow", "Dynamics Parameter Preset", None, QtGui.QApplication.UnicodeUTF8))
        self.PP_setup_mash_network_btn.setText(QtGui.QApplication.translate("MainWindow", "Setup MASH Network", None, QtGui.QApplication.UnicodeUTF8))
        self.PP_toggle_interactive_playback_btn.setText(QtGui.QApplication.translate("MainWindow", "Interactive Playback", None, QtGui.QApplication.UnicodeUTF8))
        self.PP_show_paint_node_btn.setText(QtGui.QApplication.translate("MainWindow", "Show Paint Node", None, QtGui.QApplication.UnicodeUTF8))
        self.PP_reset_playback_btn.setText(QtGui.QApplication.translate("MainWindow", "Go to Time Zero", None, QtGui.QApplication.UnicodeUTF8))
        self.PP_show_instancer_node_btn.setText(QtGui.QApplication.translate("MainWindow", "Show Instancer Node", None, QtGui.QApplication.UnicodeUTF8))
        self.PP_bake_current_btn.setText(QtGui.QApplication.translate("MainWindow", "Bake Current", None, QtGui.QApplication.UnicodeUTF8))
        self.toolButton_3.setText(QtGui.QApplication.translate("MainWindow", "Show All Baked", None, QtGui.QApplication.UnicodeUTF8))
        self.PP_delete_all_setup_btn.setText(QtGui.QApplication.translate("MainWindow", "Delete All Setup", None, QtGui.QApplication.UnicodeUTF8))
        self.swap_master_group_box.setTitle(QtGui.QApplication.translate("MainWindow", "SWAP MASTER", None, QtGui.QApplication.UnicodeUTF8))
        self.restore_instancing_group_box.setTitle(QtGui.QApplication.translate("MainWindow", "RESTORE INSTANCING", None, QtGui.QApplication.UnicodeUTF8))

from src.gui.app.setDressMaster import resources_rc_qt4
