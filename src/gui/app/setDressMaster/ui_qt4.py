# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'F:\dev\git\mk_dcc/src/gui/app/setDressMaster/ui.ui'
#
# Created: Tue Oct 27 13:46:55 2020
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(373, 673)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setStyleSheet("")
        self.centralwidget.setObjectName("centralwidget")
        self.central_widget_layout = QtGui.QVBoxLayout(self.centralwidget)
        self.central_widget_layout.setObjectName("central_widget_layout")
        self.phys_painter_main_group_box = QtGui.QGroupBox(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.phys_painter_main_group_box.sizePolicy().hasHeightForWidth())
        self.phys_painter_main_group_box.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setWeight(50)
        font.setBold(False)
        self.phys_painter_main_group_box.setFont(font)
        self.phys_painter_main_group_box.setStyleSheet("")
        self.phys_painter_main_group_box.setAlignment(QtCore.Qt.AlignCenter)
        self.phys_painter_main_group_box.setCheckable(True)
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
        self.PP_setup_mash_network_btn.setStyleSheet("font-size: 12px;")
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
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
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
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
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
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
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
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
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
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.PP_bake_current_btn.sizePolicy().hasHeightForWidth())
        self.PP_bake_current_btn.setSizePolicy(sizePolicy)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/icons/icon_bake_current.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.PP_bake_current_btn.setIcon(icon5)
        self.PP_bake_current_btn.setIconSize(QtCore.QSize(32, 32))
        self.PP_bake_current_btn.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.PP_bake_current_btn.setObjectName("PP_bake_current_btn")
        self.gridLayout.addWidget(self.PP_bake_current_btn, 1, 1, 1, 1)
        self.PP_show_all_baked_btn = QtGui.QToolButton(self.phys_painter_main_group_box)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.PP_show_all_baked_btn.sizePolicy().hasHeightForWidth())
        self.PP_show_all_baked_btn.setSizePolicy(sizePolicy)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":/icons/icon_show_all_baked.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.PP_show_all_baked_btn.setIcon(icon6)
        self.PP_show_all_baked_btn.setIconSize(QtCore.QSize(32, 32))
        self.PP_show_all_baked_btn.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.PP_show_all_baked_btn.setObjectName("PP_show_all_baked_btn")
        self.gridLayout.addWidget(self.PP_show_all_baked_btn, 1, 2, 1, 1)
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
        self.swap_master_main_group_box = QtGui.QGroupBox(self.centralwidget)
        self.swap_master_main_group_box.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.swap_master_main_group_box.sizePolicy().hasHeightForWidth())
        self.swap_master_main_group_box.setSizePolicy(sizePolicy)
        self.swap_master_main_group_box.setStyleSheet("")
        self.swap_master_main_group_box.setAlignment(QtCore.Qt.AlignCenter)
        self.swap_master_main_group_box.setCheckable(True)
        self.swap_master_main_group_box.setObjectName("swap_master_main_group_box")
        self.swap_master_group_box_layout = QtGui.QVBoxLayout(self.swap_master_main_group_box)
        self.swap_master_group_box_layout.setObjectName("swap_master_group_box_layout")
        self.groupBox_3 = QtGui.QGroupBox(self.swap_master_main_group_box)
        self.groupBox_3.setObjectName("groupBox_3")
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.groupBox_3)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.pushButton_3 = QtGui.QPushButton(self.groupBox_3)
        self.pushButton_3.setEnabled(False)
        self.pushButton_3.setObjectName("pushButton_3")
        self.horizontalLayout_2.addWidget(self.pushButton_3)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.swap_master_group_box_layout.addWidget(self.groupBox_3)
        self.groupBox = QtGui.QGroupBox(self.swap_master_main_group_box)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout = QtGui.QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setEnabled(False)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.SM_trace_vertex_radio_btn = QtGui.QRadioButton(self.groupBox)
        self.SM_trace_vertex_radio_btn.setChecked(True)
        self.SM_trace_vertex_radio_btn.setObjectName("SM_trace_vertex_radio_btn")
        self.horizontalLayout.addWidget(self.SM_trace_vertex_radio_btn)
        self.SM_trace_edge_radio_btn = QtGui.QRadioButton(self.groupBox)
        self.SM_trace_edge_radio_btn.setEnabled(False)
        self.SM_trace_edge_radio_btn.setObjectName("SM_trace_edge_radio_btn")
        self.horizontalLayout.addWidget(self.SM_trace_edge_radio_btn)
        self.SM_trace_face_radio_btn = QtGui.QRadioButton(self.groupBox)
        self.SM_trace_face_radio_btn.setEnabled(False)
        self.SM_trace_face_radio_btn.setObjectName("SM_trace_face_radio_btn")
        self.horizontalLayout.addWidget(self.SM_trace_face_radio_btn)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.SM_load_trace_components_grid_layout = QtGui.QGridLayout()
        self.SM_load_trace_components_grid_layout.setObjectName("SM_load_trace_components_grid_layout")
        self.verticalLayout.addLayout(self.SM_load_trace_components_grid_layout)
        self.swap_master_group_box_layout.addWidget(self.groupBox)
        self.line_2 = QtGui.QFrame(self.swap_master_main_group_box)
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.swap_master_group_box_layout.addWidget(self.line_2)
        self.groupBox_2 = QtGui.QGroupBox(self.swap_master_main_group_box)
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.SM_load_substitute_grid_layout = QtGui.QGridLayout()
        self.SM_load_substitute_grid_layout.setObjectName("SM_load_substitute_grid_layout")
        self.verticalLayout_2.addLayout(self.SM_load_substitute_grid_layout)
        self.swap_master_group_box_layout.addWidget(self.groupBox_2)
        self.line = QtGui.QFrame(self.swap_master_main_group_box)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName("line")
        self.swap_master_group_box_layout.addWidget(self.line)
        self.SM_orient_reconstruct_child_group_box = QtGui.QGroupBox(self.swap_master_main_group_box)
        self.SM_orient_reconstruct_child_group_box.setAlignment(QtCore.Qt.AlignCenter)
        self.SM_orient_reconstruct_child_group_box.setCheckable(True)
        self.SM_orient_reconstruct_child_group_box.setObjectName("SM_orient_reconstruct_child_group_box")
        self.horizontalLayout_5 = QtGui.QHBoxLayout(self.SM_orient_reconstruct_child_group_box)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.SM_preview_nuclei_btn = QtGui.QToolButton(self.SM_orient_reconstruct_child_group_box)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.SM_preview_nuclei_btn.sizePolicy().hasHeightForWidth())
        self.SM_preview_nuclei_btn.setSizePolicy(sizePolicy)
        self.SM_preview_nuclei_btn.setStyleSheet("font-size: 10px;")
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap(":/icons/baseline_engineering_white_48dp.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.SM_preview_nuclei_btn.setIcon(icon8)
        self.SM_preview_nuclei_btn.setIconSize(QtCore.QSize(20, 20))
        self.SM_preview_nuclei_btn.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.SM_preview_nuclei_btn.setObjectName("SM_preview_nuclei_btn")
        self.horizontalLayout_5.addWidget(self.SM_preview_nuclei_btn)
        self.SM_abort_nuclei_btn = QtGui.QToolButton(self.SM_orient_reconstruct_child_group_box)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.SM_abort_nuclei_btn.sizePolicy().hasHeightForWidth())
        self.SM_abort_nuclei_btn.setSizePolicy(sizePolicy)
        self.SM_abort_nuclei_btn.setStyleSheet("font-size: 10px;")
        self.SM_abort_nuclei_btn.setIcon(icon7)
        self.SM_abort_nuclei_btn.setIconSize(QtCore.QSize(20, 20))
        self.SM_abort_nuclei_btn.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.SM_abort_nuclei_btn.setObjectName("SM_abort_nuclei_btn")
        self.horizontalLayout_5.addWidget(self.SM_abort_nuclei_btn)
        self.SM_proceed_swapping_btn = QtGui.QToolButton(self.SM_orient_reconstruct_child_group_box)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.SM_proceed_swapping_btn.sizePolicy().hasHeightForWidth())
        self.SM_proceed_swapping_btn.setSizePolicy(sizePolicy)
        self.SM_proceed_swapping_btn.setStyleSheet("font-size: 10px;")
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap(":/icons/baseline_scatter_plot_white_48dp.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.SM_proceed_swapping_btn.setIcon(icon9)
        self.SM_proceed_swapping_btn.setIconSize(QtCore.QSize(20, 20))
        self.SM_proceed_swapping_btn.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.SM_proceed_swapping_btn.setObjectName("SM_proceed_swapping_btn")
        self.horizontalLayout_5.addWidget(self.SM_proceed_swapping_btn)
        self.swap_master_group_box_layout.addWidget(self.SM_orient_reconstruct_child_group_box)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.verticalLayout_4 = QtGui.QVBoxLayout()
        self.verticalLayout_4.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.SM_swap_use_instancing_check_box = QtGui.QCheckBox(self.swap_master_main_group_box)
        self.SM_swap_use_instancing_check_box.setChecked(True)
        self.SM_swap_use_instancing_check_box.setObjectName("SM_swap_use_instancing_check_box")
        self.verticalLayout_4.addWidget(self.SM_swap_use_instancing_check_box)
        self.SM_remove_proxies_check_box = QtGui.QCheckBox(self.swap_master_main_group_box)
        self.SM_remove_proxies_check_box.setChecked(True)
        self.SM_remove_proxies_check_box.setObjectName("SM_remove_proxies_check_box")
        self.verticalLayout_4.addWidget(self.SM_remove_proxies_check_box)
        self.horizontalLayout_4.addLayout(self.verticalLayout_4)
        self.SM_fast_forward_swap_btn = QtGui.QPushButton(self.swap_master_main_group_box)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.SM_fast_forward_swap_btn.sizePolicy().hasHeightForWidth())
        self.SM_fast_forward_swap_btn.setSizePolicy(sizePolicy)
        self.SM_fast_forward_swap_btn.setStyleSheet("font-size: 13px;")
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap(":/icons/baseline_fast_forward_white_48dp.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.SM_fast_forward_swap_btn.setIcon(icon10)
        self.SM_fast_forward_swap_btn.setIconSize(QtCore.QSize(36, 36))
        self.SM_fast_forward_swap_btn.setObjectName("SM_fast_forward_swap_btn")
        self.horizontalLayout_4.addWidget(self.SM_fast_forward_swap_btn)
        self.swap_master_group_box_layout.addLayout(self.horizontalLayout_4)
        self.central_widget_layout.addWidget(self.swap_master_main_group_box)
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
        self.PP_show_all_baked_btn.setText(QtGui.QApplication.translate("MainWindow", "Show All Baked", None, QtGui.QApplication.UnicodeUTF8))
        self.PP_delete_all_setup_btn.setText(QtGui.QApplication.translate("MainWindow", "Delete MASH Setup", None, QtGui.QApplication.UnicodeUTF8))
        self.swap_master_main_group_box.setTitle(QtGui.QApplication.translate("MainWindow", "SWAP MASTER", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_3.setTitle(QtGui.QApplication.translate("MainWindow", "Prep", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_3.setText(QtGui.QApplication.translate("MainWindow", "Explode and Group by Num of Vertices", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("MainWindow", "Proxy Template Input", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("MainWindow", "Trace Type:", None, QtGui.QApplication.UnicodeUTF8))
        self.SM_trace_vertex_radio_btn.setText(QtGui.QApplication.translate("MainWindow", "Vertex", None, QtGui.QApplication.UnicodeUTF8))
        self.SM_trace_edge_radio_btn.setText(QtGui.QApplication.translate("MainWindow", "Edge", None, QtGui.QApplication.UnicodeUTF8))
        self.SM_trace_face_radio_btn.setText(QtGui.QApplication.translate("MainWindow", "Face", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_2.setTitle(QtGui.QApplication.translate("MainWindow", "Hi-Res Template Input", None, QtGui.QApplication.UnicodeUTF8))
        self.SM_orient_reconstruct_child_group_box.setTitle(QtGui.QApplication.translate("MainWindow", "2-step Swap", None, QtGui.QApplication.UnicodeUTF8))
        self.SM_preview_nuclei_btn.setText(QtGui.QApplication.translate("MainWindow", "Preview Reconstruction", None, QtGui.QApplication.UnicodeUTF8))
        self.SM_abort_nuclei_btn.setText(QtGui.QApplication.translate("MainWindow", "Abort", None, QtGui.QApplication.UnicodeUTF8))
        self.SM_proceed_swapping_btn.setText(QtGui.QApplication.translate("MainWindow", "Proceed Swapping", None, QtGui.QApplication.UnicodeUTF8))
        self.SM_swap_use_instancing_check_box.setText(QtGui.QApplication.translate("MainWindow", "Instancing", None, QtGui.QApplication.UnicodeUTF8))
        self.SM_remove_proxies_check_box.setText(QtGui.QApplication.translate("MainWindow", "Remove Proxies", None, QtGui.QApplication.UnicodeUTF8))
        self.SM_fast_forward_swap_btn.setText(QtGui.QApplication.translate("MainWindow", "Fast-Forward Swap", None, QtGui.QApplication.UnicodeUTF8))

from src.gui.app.setDressMaster import resources_rc_qt4
