# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\projects\mk_dcc/src/gui/app/setDressMaster/ui.ui'
#
# Created: Sun Nov  8 11:19:35 2020
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(414, 557)
        MainWindow.setStyleSheet("QGroupBox {border: 0}")
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setStyleSheet("color: white;")
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_8 = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout_8.setSpacing(0)
        self.verticalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.scrollArea = QtGui.QScrollArea(self.centralwidget)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtGui.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, -254, 395, 809))
        self.scrollAreaWidgetContents.setStyleSheet("background-color: rgb(89, 22, 22);")
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout_11 = QtGui.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_11.setSpacing(0)
        self.verticalLayout_11.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.PhysXPainter_outer_container = QtGui.QGroupBox(self.scrollAreaWidgetContents)
        self.PhysXPainter_outer_container.setStyleSheet("background-color: rgb(89, 22, 22);")
        self.PhysXPainter_outer_container.setTitle("")
        self.PhysXPainter_outer_container.setObjectName("PhysXPainter_outer_container")
        self.verticalLayout_6 = QtGui.QVBoxLayout(self.PhysXPainter_outer_container)
        self.verticalLayout_6.setContentsMargins(-1, -1, -1, 5)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.phys_painter_main_group_box = QtGui.QGroupBox(self.PhysXPainter_outer_container)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.phys_painter_main_group_box.sizePolicy().hasHeightForWidth())
        self.phys_painter_main_group_box.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setWeight(50)
        font.setBold(False)
        self.phys_painter_main_group_box.setFont(font)
        self.phys_painter_main_group_box.setStyleSheet("background-color: rgb(38, 47, 42);")
        self.phys_painter_main_group_box.setAlignment(QtCore.Qt.AlignCenter)
        self.phys_painter_main_group_box.setCheckable(True)
        self.phys_painter_main_group_box.setObjectName("phys_painter_main_group_box")
        self.phys_painter_group_box_layout = QtGui.QVBoxLayout(self.phys_painter_main_group_box)
        self.phys_painter_group_box_layout.setContentsMargins(0, 20, 0, 0)
        self.phys_painter_group_box_layout.setObjectName("phys_painter_group_box_layout")
        self.PP_load_selection_grid_layout = QtGui.QGridLayout()
        self.PP_load_selection_grid_layout.setContentsMargins(9, -1, 9, -1)
        self.PP_load_selection_grid_layout.setObjectName("PP_load_selection_grid_layout")
        self.phys_painter_group_box_layout.addLayout(self.PP_load_selection_grid_layout)
        self.PP_dyn_parms_child_group_box = QtGui.QGroupBox(self.phys_painter_main_group_box)
        self.PP_dyn_parms_child_group_box.setStyleSheet("QLabel {font-size: 10px; color: rgb(146, 146, 146);} QGroupBox {color: rgb(105, 105, 105);}")
        self.PP_dyn_parms_child_group_box.setAlignment(QtCore.Qt.AlignCenter)
        self.PP_dyn_parms_child_group_box.setFlat(True)
        self.PP_dyn_parms_child_group_box.setCheckable(True)
        self.PP_dyn_parms_child_group_box.setObjectName("PP_dyn_parms_child_group_box")
        self.PP_dynamic_parameters_grid_layout = QtGui.QGridLayout(self.PP_dyn_parms_child_group_box)
        self.PP_dynamic_parameters_grid_layout.setContentsMargins(18, 20, 18, -1)
        self.PP_dynamic_parameters_grid_layout.setObjectName("PP_dynamic_parameters_grid_layout")
        self.phys_painter_group_box_layout.addWidget(self.PP_dyn_parms_child_group_box)
        self.groupBox_5 = QtGui.QGroupBox(self.phys_painter_main_group_box)
        self.groupBox_5.setStyleSheet("background-color: rgb(26, 31, 34)")
        self.groupBox_5.setTitle("")
        self.groupBox_5.setFlat(True)
        self.groupBox_5.setObjectName("groupBox_5")
        self.verticalLayout_5 = QtGui.QVBoxLayout(self.groupBox_5)
        self.verticalLayout_5.setContentsMargins(9, 6, 9, 12)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.PP_setup_mash_network_btn = QtGui.QPushButton(self.groupBox_5)
        self.PP_setup_mash_network_btn.setMinimumSize(QtCore.QSize(0, 40))
        font = QtGui.QFont()
        font.setPointSize(-1)
        font.setWeight(50)
        font.setBold(False)
        self.PP_setup_mash_network_btn.setFont(font)
        self.PP_setup_mash_network_btn.setStyleSheet("font-size: 12px; background-color: rgb(32, 69, 78);")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/baseline_wb_iridescent_white_48dp.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.PP_setup_mash_network_btn.setIcon(icon)
        self.PP_setup_mash_network_btn.setIconSize(QtCore.QSize(24, 24))
        self.PP_setup_mash_network_btn.setObjectName("PP_setup_mash_network_btn")
        self.verticalLayout_5.addWidget(self.PP_setup_mash_network_btn)
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.PP_toggle_interactive_playback_btn = QtGui.QToolButton(self.groupBox_5)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.PP_toggle_interactive_playback_btn.sizePolicy().hasHeightForWidth())
        self.PP_toggle_interactive_playback_btn.setSizePolicy(sizePolicy)
        self.PP_toggle_interactive_playback_btn.setStyleSheet("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/baseline_play_circle_outline_white_48dp.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.PP_toggle_interactive_playback_btn.setIcon(icon1)
        self.PP_toggle_interactive_playback_btn.setIconSize(QtCore.QSize(32, 32))
        self.PP_toggle_interactive_playback_btn.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.PP_toggle_interactive_playback_btn.setObjectName("PP_toggle_interactive_playback_btn")
        self.gridLayout.addWidget(self.PP_toggle_interactive_playback_btn, 0, 2, 1, 1)
        self.PP_show_paint_node_btn = QtGui.QToolButton(self.groupBox_5)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.PP_show_paint_node_btn.sizePolicy().hasHeightForWidth())
        self.PP_show_paint_node_btn.setSizePolicy(sizePolicy)
        self.PP_show_paint_node_btn.setStyleSheet("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icons/baseline_brush_white_48dp.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.PP_show_paint_node_btn.setIcon(icon2)
        self.PP_show_paint_node_btn.setIconSize(QtCore.QSize(32, 32))
        self.PP_show_paint_node_btn.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.PP_show_paint_node_btn.setObjectName("PP_show_paint_node_btn")
        self.gridLayout.addWidget(self.PP_show_paint_node_btn, 0, 1, 1, 1)
        self.PP_reset_playback_btn = QtGui.QToolButton(self.groupBox_5)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.PP_reset_playback_btn.sizePolicy().hasHeightForWidth())
        self.PP_reset_playback_btn.setSizePolicy(sizePolicy)
        self.PP_reset_playback_btn.setStyleSheet("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/icons/baseline_exposure_zero_white_48dp.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.PP_reset_playback_btn.setIcon(icon3)
        self.PP_reset_playback_btn.setIconSize(QtCore.QSize(32, 32))
        self.PP_reset_playback_btn.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.PP_reset_playback_btn.setObjectName("PP_reset_playback_btn")
        self.gridLayout.addWidget(self.PP_reset_playback_btn, 0, 0, 1, 1)
        self.PP_bake_current_btn = QtGui.QToolButton(self.groupBox_5)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.PP_bake_current_btn.sizePolicy().hasHeightForWidth())
        self.PP_bake_current_btn.setSizePolicy(sizePolicy)
        self.PP_bake_current_btn.setStyleSheet("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/icons/icon_bake_current.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.PP_bake_current_btn.setIcon(icon4)
        self.PP_bake_current_btn.setIconSize(QtCore.QSize(32, 32))
        self.PP_bake_current_btn.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.PP_bake_current_btn.setObjectName("PP_bake_current_btn")
        self.gridLayout.addWidget(self.PP_bake_current_btn, 1, 1, 1, 1)
        self.PP_show_all_baked_btn = QtGui.QToolButton(self.groupBox_5)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.PP_show_all_baked_btn.sizePolicy().hasHeightForWidth())
        self.PP_show_all_baked_btn.setSizePolicy(sizePolicy)
        self.PP_show_all_baked_btn.setStyleSheet("")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/icons/icon_show_all_baked.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.PP_show_all_baked_btn.setIcon(icon5)
        self.PP_show_all_baked_btn.setIconSize(QtCore.QSize(32, 32))
        self.PP_show_all_baked_btn.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.PP_show_all_baked_btn.setObjectName("PP_show_all_baked_btn")
        self.gridLayout.addWidget(self.PP_show_all_baked_btn, 1, 2, 1, 1)
        self.PP_show_instancer_node_btn = QtGui.QToolButton(self.groupBox_5)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.PP_show_instancer_node_btn.sizePolicy().hasHeightForWidth())
        self.PP_show_instancer_node_btn.setSizePolicy(sizePolicy)
        self.PP_show_instancer_node_btn.setStyleSheet("")
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":/icons/baseline_list_alt_white_48dp.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.PP_show_instancer_node_btn.setIcon(icon6)
        self.PP_show_instancer_node_btn.setIconSize(QtCore.QSize(32, 32))
        self.PP_show_instancer_node_btn.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.PP_show_instancer_node_btn.setObjectName("PP_show_instancer_node_btn")
        self.gridLayout.addWidget(self.PP_show_instancer_node_btn, 1, 0, 1, 1)
        self.verticalLayout_5.addLayout(self.gridLayout)
        self.PP_delete_all_setup_btn = QtGui.QPushButton(self.groupBox_5)
        self.PP_delete_all_setup_btn.setEnabled(True)
        self.PP_delete_all_setup_btn.setStyleSheet("background-color: black; color: rgb(158, 0, 0);")
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(":/icons/baseline_clear_white_48dp.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.PP_delete_all_setup_btn.setIcon(icon7)
        self.PP_delete_all_setup_btn.setIconSize(QtCore.QSize(24, 24))
        self.PP_delete_all_setup_btn.setObjectName("PP_delete_all_setup_btn")
        self.verticalLayout_5.addWidget(self.PP_delete_all_setup_btn)
        self.phys_painter_group_box_layout.addWidget(self.groupBox_5)
        self.verticalLayout_6.addWidget(self.phys_painter_main_group_box)
        self.verticalLayout_11.addWidget(self.PhysXPainter_outer_container)
        self.SwapMaster_outer_container = QtGui.QGroupBox(self.scrollAreaWidgetContents)
        self.SwapMaster_outer_container.setStyleSheet("background-color: rgb(89, 22, 22);")
        self.SwapMaster_outer_container.setTitle("")
        self.SwapMaster_outer_container.setObjectName("SwapMaster_outer_container")
        self.verticalLayout_7 = QtGui.QVBoxLayout(self.SwapMaster_outer_container)
        self.verticalLayout_7.setContentsMargins(-1, 5, 9, 2)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.swap_master_main_group_box = QtGui.QGroupBox(self.SwapMaster_outer_container)
        self.swap_master_main_group_box.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.swap_master_main_group_box.sizePolicy().hasHeightForWidth())
        self.swap_master_main_group_box.setSizePolicy(sizePolicy)
        self.swap_master_main_group_box.setStyleSheet("background-color: rgb(37, 35, 41)")
        self.swap_master_main_group_box.setAlignment(QtCore.Qt.AlignCenter)
        self.swap_master_main_group_box.setCheckable(True)
        self.swap_master_main_group_box.setObjectName("swap_master_main_group_box")
        self.swap_master_group_box_layout = QtGui.QVBoxLayout(self.swap_master_main_group_box)
        self.swap_master_group_box_layout.setContentsMargins(0, 20, 0, 0)
        self.swap_master_group_box_layout.setObjectName("swap_master_group_box_layout")
        self.groupBox_3 = QtGui.QGroupBox(self.swap_master_main_group_box)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_3.sizePolicy().hasHeightForWidth())
        self.groupBox_3.setSizePolicy(sizePolicy)
        self.groupBox_3.setStyleSheet("QGroupBox {color: rgb(140, 140, 140);} QRadioButton {color: rgb(140, 140, 140);}")
        self.groupBox_3.setObjectName("groupBox_3")
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.groupBox_3)
        self.verticalLayout_3.setSpacing(3)
        self.verticalLayout_3.setContentsMargins(18, 20, 18, 6)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_6 = QtGui.QHBoxLayout()
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.SM_prep_mash_scene_radio_btn = QtGui.QRadioButton(self.groupBox_3)
        self.SM_prep_mash_scene_radio_btn.setStyleSheet("")
        self.SM_prep_mash_scene_radio_btn.setChecked(True)
        self.SM_prep_mash_scene_radio_btn.setObjectName("SM_prep_mash_scene_radio_btn")
        self.horizontalLayout_6.addWidget(self.SM_prep_mash_scene_radio_btn)
        self.SM_prep_regular_scene_radio_btn = QtGui.QRadioButton(self.groupBox_3)
        self.SM_prep_regular_scene_radio_btn.setStyleSheet("")
        self.SM_prep_regular_scene_radio_btn.setObjectName("SM_prep_regular_scene_radio_btn")
        self.horizontalLayout_6.addWidget(self.SM_prep_regular_scene_radio_btn)
        self.verticalLayout_3.addLayout(self.horizontalLayout_6)
        self.SM_explode_and_group_btn = QtGui.QPushButton(self.groupBox_3)
        self.SM_explode_and_group_btn.setEnabled(True)
        self.SM_explode_and_group_btn.setStyleSheet("font-size: 10px; background-color: rgb(36, 34, 39);")
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap(":/icons/baseline_broken_image_white_48dp.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.SM_explode_and_group_btn.setIcon(icon8)
        self.SM_explode_and_group_btn.setIconSize(QtCore.QSize(24, 24))
        self.SM_explode_and_group_btn.setObjectName("SM_explode_and_group_btn")
        self.verticalLayout_3.addWidget(self.SM_explode_and_group_btn)
        self.SM_run_thru_scene_and_group_btn = QtGui.QPushButton(self.groupBox_3)
        self.SM_run_thru_scene_and_group_btn.setMinimumSize(QtCore.QSize(0, 32))
        self.SM_run_thru_scene_and_group_btn.setStyleSheet("font-size: 10px; background-color: rgb(36, 34, 39);")
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap(":/icons/baseline_language_white_48dp.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.SM_run_thru_scene_and_group_btn.setIcon(icon9)
        self.SM_run_thru_scene_and_group_btn.setIconSize(QtCore.QSize(20, 20))
        self.SM_run_thru_scene_and_group_btn.setObjectName("SM_run_thru_scene_and_group_btn")
        self.verticalLayout_3.addWidget(self.SM_run_thru_scene_and_group_btn)
        self.swap_master_group_box_layout.addWidget(self.groupBox_3)
        self.line_3 = QtGui.QFrame(self.swap_master_main_group_box)
        self.line_3.setFrameShape(QtGui.QFrame.HLine)
        self.line_3.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.swap_master_group_box_layout.addWidget(self.line_3)
        self.groupBox = QtGui.QGroupBox(self.swap_master_main_group_box)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setStyleSheet("QGroupBox {color: rgb(140, 140, 140);} QRadioButton {color: rgb(140, 140, 140);} QLabel {color: rgb(140, 140, 140);}")
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout = QtGui.QVBoxLayout(self.groupBox)
        self.verticalLayout.setContentsMargins(18, 15, 18, -1)
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
        self.groupBox_2 = QtGui.QGroupBox(self.swap_master_main_group_box)
        self.groupBox_2.setStyleSheet("QGroupBox {color: rgb(140, 140, 140);}")
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_2.setContentsMargins(18, 20, 18, -1)
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
        self.groupBox_4 = QtGui.QGroupBox(self.swap_master_main_group_box)
        self.groupBox_4.setStyleSheet("background-color: rgb(41, 23, 37)")
        self.groupBox_4.setTitle("")
        self.groupBox_4.setFlat(True)
        self.groupBox_4.setObjectName("groupBox_4")
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.groupBox_4)
        self.verticalLayout_4.setContentsMargins(9, 6, 9, 9)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.SM_orient_reconstruct_child_group_box = QtGui.QGroupBox(self.groupBox_4)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.SM_orient_reconstruct_child_group_box.sizePolicy().hasHeightForWidth())
        self.SM_orient_reconstruct_child_group_box.setSizePolicy(sizePolicy)
        self.SM_orient_reconstruct_child_group_box.setStyleSheet("QGroupBox {font-size: 10px; color: rgb(150, 150, 150);}")
        self.SM_orient_reconstruct_child_group_box.setAlignment(QtCore.Qt.AlignCenter)
        self.SM_orient_reconstruct_child_group_box.setCheckable(True)
        self.SM_orient_reconstruct_child_group_box.setObjectName("SM_orient_reconstruct_child_group_box")
        self.horizontalLayout_5 = QtGui.QHBoxLayout(self.SM_orient_reconstruct_child_group_box)
        self.horizontalLayout_5.setContentsMargins(18, 20, 18, 3)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.SM_preview_nuclei_btn = QtGui.QToolButton(self.SM_orient_reconstruct_child_group_box)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.SM_preview_nuclei_btn.sizePolicy().hasHeightForWidth())
        self.SM_preview_nuclei_btn.setSizePolicy(sizePolicy)
        self.SM_preview_nuclei_btn.setStyleSheet("")
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap(":/icons/baseline_engineering_white_48dp.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.SM_preview_nuclei_btn.setIcon(icon10)
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
        self.SM_abort_nuclei_btn.setStyleSheet("background-color: black; color: rgb(158, 0, 0);")
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
        self.SM_proceed_swapping_btn.setStyleSheet("")
        icon11 = QtGui.QIcon()
        icon11.addPixmap(QtGui.QPixmap(":/icons/baseline_scatter_plot_white_48dp.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.SM_proceed_swapping_btn.setIcon(icon11)
        self.SM_proceed_swapping_btn.setIconSize(QtCore.QSize(20, 20))
        self.SM_proceed_swapping_btn.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.SM_proceed_swapping_btn.setObjectName("SM_proceed_swapping_btn")
        self.horizontalLayout_5.addWidget(self.SM_proceed_swapping_btn)
        self.verticalLayout_4.addWidget(self.SM_orient_reconstruct_child_group_box)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(12)
        self.horizontalLayout_2.setContentsMargins(18, 0, 18, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout_9 = QtGui.QVBoxLayout()
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.SM_remove_proxies_check_box = QtGui.QCheckBox(self.groupBox_4)
        self.SM_remove_proxies_check_box.setStyleSheet("font-size: 10px;")
        self.SM_remove_proxies_check_box.setChecked(True)
        self.SM_remove_proxies_check_box.setObjectName("SM_remove_proxies_check_box")
        self.verticalLayout_9.addWidget(self.SM_remove_proxies_check_box)
        self.SM_swap_use_instancing_check_box = QtGui.QCheckBox(self.groupBox_4)
        self.SM_swap_use_instancing_check_box.setStyleSheet("font-size: 10px;")
        self.SM_swap_use_instancing_check_box.setChecked(True)
        self.SM_swap_use_instancing_check_box.setObjectName("SM_swap_use_instancing_check_box")
        self.verticalLayout_9.addWidget(self.SM_swap_use_instancing_check_box)
        self.horizontalLayout_2.addLayout(self.verticalLayout_9)
        self.verticalLayout_12 = QtGui.QVBoxLayout()
        self.verticalLayout_12.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_12.setObjectName("verticalLayout_12")
        self.SM_compute_scale_check_box = QtGui.QCheckBox(self.groupBox_4)
        self.SM_compute_scale_check_box.setStyleSheet("font-size: 10px;")
        self.SM_compute_scale_check_box.setChecked(True)
        self.SM_compute_scale_check_box.setObjectName("SM_compute_scale_check_box")
        self.verticalLayout_12.addWidget(self.SM_compute_scale_check_box)
        spacerItem = QtGui.QSpacerItem(20, 5, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.MinimumExpanding)
        self.verticalLayout_12.addItem(spacerItem)
        self.horizontalLayout_2.addLayout(self.verticalLayout_12)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.verticalLayout_4.addLayout(self.horizontalLayout_2)
        self.SM_fast_forward_swap_btn = QtGui.QPushButton(self.groupBox_4)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.SM_fast_forward_swap_btn.sizePolicy().hasHeightForWidth())
        self.SM_fast_forward_swap_btn.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(-1)
        font.setWeight(50)
        font.setBold(False)
        self.SM_fast_forward_swap_btn.setFont(font)
        self.SM_fast_forward_swap_btn.setStyleSheet("font-size: 13px; font-size: 12px; background-color: rgb(114, 44, 55);")
        icon12 = QtGui.QIcon()
        icon12.addPixmap(QtGui.QPixmap(":/icons/baseline_fast_forward_white_48dp.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.SM_fast_forward_swap_btn.setIcon(icon12)
        self.SM_fast_forward_swap_btn.setIconSize(QtCore.QSize(36, 36))
        self.SM_fast_forward_swap_btn.setObjectName("SM_fast_forward_swap_btn")
        self.verticalLayout_4.addWidget(self.SM_fast_forward_swap_btn)
        self.SM_show_swapped_btn = QtGui.QPushButton(self.groupBox_4)
        self.SM_show_swapped_btn.setMinimumSize(QtCore.QSize(0, 24))
        self.SM_show_swapped_btn.setStyleSheet("font-size: 10px; background-color: rgb(78, 46, 58)")
        self.SM_show_swapped_btn.setObjectName("SM_show_swapped_btn")
        self.verticalLayout_4.addWidget(self.SM_show_swapped_btn)
        self.swap_master_group_box_layout.addWidget(self.groupBox_4)
        self.verticalLayout_7.addWidget(self.swap_master_main_group_box)
        self.verticalLayout_11.addWidget(self.SwapMaster_outer_container)
        self.bottom_buffer_outer_container = QtGui.QGroupBox(self.scrollAreaWidgetContents)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bottom_buffer_outer_container.sizePolicy().hasHeightForWidth())
        self.bottom_buffer_outer_container.setSizePolicy(sizePolicy)
        self.bottom_buffer_outer_container.setStyleSheet("background-color: rgb(89, 22, 22);")
        self.bottom_buffer_outer_container.setTitle("")
        self.bottom_buffer_outer_container.setObjectName("bottom_buffer_outer_container")
        self.verticalLayout_10 = QtGui.QVBoxLayout(self.bottom_buffer_outer_container)
        self.verticalLayout_10.setSpacing(0)
        self.verticalLayout_10.setContentsMargins(9, 2, 9, 9)
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.SetDressMaster_about_btn = QtGui.QPushButton(self.bottom_buffer_outer_container)
        self.SetDressMaster_about_btn.setStyleSheet("color: rgb(140, 140, 140);")
        self.SetDressMaster_about_btn.setObjectName("SetDressMaster_about_btn")
        self.verticalLayout_10.addWidget(self.SetDressMaster_about_btn)
        spacerItem2 = QtGui.QSpacerItem(20, 8, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_10.addItem(spacerItem2)
        self.verticalLayout_11.addWidget(self.bottom_buffer_outer_container)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout_8.addWidget(self.scrollArea)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Set Dress Master", None, QtGui.QApplication.UnicodeUTF8))
        self.phys_painter_main_group_box.setTitle(QtGui.QApplication.translate("MainWindow", "--  PHYSX PAINTER  --", None, QtGui.QApplication.UnicodeUTF8))
        self.PP_dyn_parms_child_group_box.setTitle(QtGui.QApplication.translate("MainWindow", " --  Dynamics Parameter Preset  -- ", None, QtGui.QApplication.UnicodeUTF8))
        self.PP_setup_mash_network_btn.setText(QtGui.QApplication.translate("MainWindow", "Setup MASH Network", None, QtGui.QApplication.UnicodeUTF8))
        self.PP_toggle_interactive_playback_btn.setText(QtGui.QApplication.translate("MainWindow", "Interactive Playback", None, QtGui.QApplication.UnicodeUTF8))
        self.PP_show_paint_node_btn.setText(QtGui.QApplication.translate("MainWindow", "Show Paint Node", None, QtGui.QApplication.UnicodeUTF8))
        self.PP_reset_playback_btn.setText(QtGui.QApplication.translate("MainWindow", "Go to Time Zero", None, QtGui.QApplication.UnicodeUTF8))
        self.PP_bake_current_btn.setText(QtGui.QApplication.translate("MainWindow", "Bake Current", None, QtGui.QApplication.UnicodeUTF8))
        self.PP_show_all_baked_btn.setText(QtGui.QApplication.translate("MainWindow", "Show All Baked", None, QtGui.QApplication.UnicodeUTF8))
        self.PP_show_instancer_node_btn.setText(QtGui.QApplication.translate("MainWindow", "Show Instancer Node", None, QtGui.QApplication.UnicodeUTF8))
        self.PP_delete_all_setup_btn.setText(QtGui.QApplication.translate("MainWindow", "Delete MASH Setup", None, QtGui.QApplication.UnicodeUTF8))
        self.swap_master_main_group_box.setTitle(QtGui.QApplication.translate("MainWindow", "--  SWAP MASTER  --", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_3.setTitle(QtGui.QApplication.translate("MainWindow", "Prep", None, QtGui.QApplication.UnicodeUTF8))
        self.SM_prep_mash_scene_radio_btn.setText(QtGui.QApplication.translate("MainWindow", "MASH scene", None, QtGui.QApplication.UnicodeUTF8))
        self.SM_prep_regular_scene_radio_btn.setText(QtGui.QApplication.translate("MainWindow", "Regular scene", None, QtGui.QApplication.UnicodeUTF8))
        self.SM_explode_and_group_btn.setText(QtGui.QApplication.translate("MainWindow", "Explode MASH Mesh and Group by PolyCount", None, QtGui.QApplication.UnicodeUTF8))
        self.SM_run_thru_scene_and_group_btn.setText(QtGui.QApplication.translate("MainWindow", "Run Thru Scene and Group All by PolyCount", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("MainWindow", "Proxy Template Input", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("MainWindow", "Trace Type:", None, QtGui.QApplication.UnicodeUTF8))
        self.SM_trace_vertex_radio_btn.setText(QtGui.QApplication.translate("MainWindow", "Vertex", None, QtGui.QApplication.UnicodeUTF8))
        self.SM_trace_edge_radio_btn.setText(QtGui.QApplication.translate("MainWindow", "Edge", None, QtGui.QApplication.UnicodeUTF8))
        self.SM_trace_face_radio_btn.setText(QtGui.QApplication.translate("MainWindow", "Face", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_2.setTitle(QtGui.QApplication.translate("MainWindow", "Hi-Res Template Input", None, QtGui.QApplication.UnicodeUTF8))
        self.SM_orient_reconstruct_child_group_box.setTitle(QtGui.QApplication.translate("MainWindow", " --  2-step Swap  -- ", None, QtGui.QApplication.UnicodeUTF8))
        self.SM_preview_nuclei_btn.setText(QtGui.QApplication.translate("MainWindow", "Preview Reconstruction", None, QtGui.QApplication.UnicodeUTF8))
        self.SM_abort_nuclei_btn.setText(QtGui.QApplication.translate("MainWindow", "Abort", None, QtGui.QApplication.UnicodeUTF8))
        self.SM_proceed_swapping_btn.setText(QtGui.QApplication.translate("MainWindow", "Proceed w/ Swapping", None, QtGui.QApplication.UnicodeUTF8))
        self.SM_remove_proxies_check_box.setText(QtGui.QApplication.translate("MainWindow", "Remove Proxies", None, QtGui.QApplication.UnicodeUTF8))
        self.SM_swap_use_instancing_check_box.setText(QtGui.QApplication.translate("MainWindow", "Instancing", None, QtGui.QApplication.UnicodeUTF8))
        self.SM_compute_scale_check_box.setText(QtGui.QApplication.translate("MainWindow", "Compute Scale", None, QtGui.QApplication.UnicodeUTF8))
        self.SM_fast_forward_swap_btn.setText(QtGui.QApplication.translate("MainWindow", "Fast-Forward Swap Selected", None, QtGui.QApplication.UnicodeUTF8))
        self.SM_show_swapped_btn.setText(QtGui.QApplication.translate("MainWindow", "Show Last Swapped", None, QtGui.QApplication.UnicodeUTF8))
        self.SetDressMaster_about_btn.setText(QtGui.QApplication.translate("MainWindow", "About", None, QtGui.QApplication.UnicodeUTF8))
        self.SetDressMaster_about_btn.setProperty("about", QtGui.QApplication.translate("MainWindow", "Author: Truong CG Artist, Mushogenshin\n"
"Designer: Rkxg", None, QtGui.QApplication.UnicodeUTF8))
        self.SetDressMaster_about_btn.setProperty("version", QtGui.QApplication.translate("MainWindow", "0.1.2", None, QtGui.QApplication.UnicodeUTF8))

from src.gui.app.setDressMaster import resources_rc_qt4
