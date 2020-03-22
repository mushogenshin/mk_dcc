# -*- coding: utf-8 -*-
# !/usr/bin/env python

import sys
import os
import subprocess
from functools import partial
import logging as logger

import maya.mel
import pymel.core as pm
import maya.OpenMayaUI as omui

PY3_PATH = 'C:/python3.7.0/Lib/site-packages'
PY3_PATH = os.path.normpath(PY3_PATH)

if PY3_PATH in sys.path:
    sys.path.remove(PY3_PATH)

try:
    from PySide2.QtCore import *
    from PySide2.QtGui import *
    from PySide2.QtWidgets import *
    from shiboken2 import wrapInstance
except ImportError:
    from PySide.QtCore import *
    from PySide.QtGui import *
    from shiboken import wrapInstance

_PATHLIB2_PATH = "C:/vsTools2/ALL/python"
sys.path.append(_PATHLIB2_PATH)
from pathlib2 import Path

import main as mnT2
import config as cfg
import label
import vsTools1UI

# during dev only
# reload(mnT2)
# reload(cfg)
#
# reload(label)
# reload(vsTools1UI)


def maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(long(main_window_ptr), QWidget)


class mnT2Dialog(QDialog):
    tool_version = "0.6.0"

    LOOT = True

    def __init__(self, parent=maya_main_window()):
        super(mnT2Dialog, self).__init__(parent)

        self.setWindowTitle("miniTools2 v{}".format(mnT2Dialog.tool_version))
        self.setMinimumWidth(347)
        self.setMaximumHeight(300)
        self.setWindowFlags(self.windowFlags() ^ Qt.WindowContextHelpButtonHint)

        # mnT2.update_modules()

        self.create_widgets()
        self.create_layouts()
        self.create_connections()

        self.switch_button_text(self.locale_toggle_cb.isChecked())

    def create_widgets(self):

        self.locale_toggle_cb = QCheckBox("ENG")
        self.locale_toggle_cb.setChecked(True)

        self.mat_picker_btn = QPushButton()
        self.mat_picker_btn.setIcon(QIcon(":eyeDropper.png"))  # colorPickCursor
        self.mat_picker_btn.setStyleSheet("background-color: rgb(133, 108, 136); "
                                          "min-width: 4.5em; "
                                          "padding: 1px")

        self.main_dialog_tabs = QTabWidget()
        self.A_tab = QWidget()
        self.B_tab = QWidget()
        self.C_tab = QWidget()
        self.D_tab = QWidget()
        self.E_tab = QWidget()
        self.F_tab = QWidget()
        self.G_tab = QWidget()

        # TAB A WIDGETS

        # button 'OKB'
        self.open_kitbash_browser_btn = QPushButton()
        self.open_kitbash_browser_btn.setStyleSheet(
            "{0}; background-color: rgb(90, 145, 90)".format(cfg.text_align_left_ss))
        self.open_kitbash_browser_btn.setIcon(QIcon(":weld24_NEX.png"))  # menuIconSkeletons.png

        self.open_repo_kitbash_lib_folder_btn = QPushButton()
        self.open_repo_kitbash_lib_folder_btn.setIcon(QIcon(":fileOpen.png"))
        self.open_repo_kitbash_lib_folder_btn.setStyleSheet(cfg.folder_btn_ss)
        # self.open_repo_kitbash_lib_folder_btn.setToolTip("Open folder")

        # button 'OEN'
        self.open_env_browser_btn = QPushButton()
        self.open_env_browser_btn.setStyleSheet(cfg.text_align_left_ss)
        self.open_env_browser_btn.setIcon(QIcon(":out_envBall.png"))

        self.open_repo_env_lib_folder_btn = QPushButton()
        self.open_repo_env_lib_folder_btn.setIcon(QIcon(":fileOpen.png"))
        self.open_repo_env_lib_folder_btn.setStyleSheet(cfg.folder_btn_ss)
        # self.open_repo_env_lib_folder_btn.setToolTip("Open folder")

        # button 'OCO'
        self.open_costume_browser_btn = QPushButton()
        self.open_costume_browser_btn.setStyleSheet(cfg.text_align_left_ss)
        self.open_costume_browser_btn.setIcon(QIcon(":nClothCreatePassive.png"))  # menuIconNCloth.png

        self.open_repo_costume_lib_folder_btn = QPushButton()
        self.open_repo_costume_lib_folder_btn.setIcon(QIcon(":fileOpen.png"))
        self.open_repo_costume_lib_folder_btn.setStyleSheet(cfg.folder_btn_ss)
        # self.open_repo_costume_lib_folder_btn.setToolTip("Open folder")

        # button 'OCH'
        self.open_char_browser_btn = QPushButton()
        self.open_char_browser_btn.setStyleSheet(cfg.text_align_left_ss)
        self.open_char_browser_btn.setIcon(QIcon(":HIKCharacterToolBodyPart.png"))  # animateSnapshot.png,
        # HIKCharacterToolFullBody.png, HIKCharacterToolStancePose.png

        self.open_repo_char_lib_folder_btn = QPushButton()
        self.open_repo_char_lib_folder_btn.setIcon(QIcon(":fileOpen.png"))
        self.open_repo_char_lib_folder_btn.setStyleSheet(cfg.folder_btn_ss)
        # self.open_repo_char_lib_folder_btn.setToolTip("Open folder")

        # button 'OAC'
        self.open_creature_browser_btn = QPushButton()
        self.open_creature_browser_btn.setStyleSheet(cfg.text_align_left_ss)
        self.open_creature_browser_btn.setIcon(QIcon(":HIKCharacterToolSkeleton.png"))  #

        self.open_repo_creature_lib_folder_btn = QPushButton()
        self.open_repo_creature_lib_folder_btn.setIcon(QIcon(":fileOpen.png"))
        self.open_repo_creature_lib_folder_btn.setStyleSheet(cfg.folder_btn_ss)
        # self.open_repo_creature_lib_folder_btn.setToolTip("Open folder")

        # button 'HDA'
        self.open_hda_browser_btn = QPushButton("Houdini Digital Asset Browser")
        self.open_hda_browser_btn.setStyleSheet(cfg.text_align_left_ss)
        self.open_hda_browser_btn.setStyleSheet("color: black; background-color: rgb(242, 103, 34)")
        # self.open_hda_browser_btn.setIcon(QIcon(":HIKCharacterToolBodyPart.png"))

        self.open_repo_hda_lib_folder_btn = QPushButton()
        self.open_repo_hda_lib_folder_btn.setIcon(QIcon(":fileOpen.png"))
        self.open_repo_hda_lib_folder_btn.setStyleSheet(cfg.folder_btn_ss)
        # self.open_repo_hda_lib_folder_btn.setToolTip("Open folder")

        # TAB B WIDGETS

        # button "VMTB"
        self.vmtb_btn = QPushButton("VIRTUOS Toolbox")
        self.vmtb_btn.setStyleSheet(cfg.terra_btn_ss)

        # button 'VMTB_?'
        self.vmtb_tutorials_btn = QPushButton("?")
        self.vmtb_tutorials_btn.setStyleSheet(cfg.readme_btn_ss)

        self.vmtb_download_btn = QPushButton("Download")
        self.vmtb_download_btn.setStyleSheet("color: black; background-color: rgb(173, 158, 217); max-width: 5.5em")

        self.vsTools1_btn = QPushButton("** ILM Tools **")
        self.vsTools1_btn.setStyleSheet(cfg.terra_btn_ss)

        # button "LQP"
        self.quick_pipe_btn = QPushButton("Q Pipe")
        self.quick_pipe_btn.setStyleSheet(cfg.dark_btn_ss)

        self.quick_pipe_tutorial_btn = QPushButton("?")
        self.quick_pipe_tutorial_btn.setStyleSheet(cfg.readme_btn_ss)

        # button "LND"
        self.ninja_dojo_btn = QPushButton("NJDJ (2016-17)")
        self.ninja_dojo_btn.setStyleSheet(cfg.dark_btn_ss)

        # button "ZEN"
        self.zen_tools_btn = QPushButton("ZEN (*req. BonusTools*)")
        self.zen_tools_btn.setStyleSheet(cfg.dark_btn_ss)

        # button "BOOL"
        self.bool_btn = QPushButton("***  BOOL (2018-19) ***")
        self.bool_btn.setStyleSheet("color: black; background-color: rgb(241, 90, 91)")
        # self.bool_btn.setEnabled(False)

        self.booltool_tutorial_btn = QPushButton("?")
        self.booltool_tutorial_btn.setStyleSheet(cfg.readme_btn_ss)

        self.speed_cut_btn = QPushButton("Speed Cut")
        self.speed_cut_btn.setStyleSheet('{}; {}'.format(cfg.sea_green5_btn_ss, cfg.medium_btn_width))

        self.speed_cut_tutorials_btn = QPushButton("?")
        self.speed_cut_tutorials_btn.setStyleSheet(cfg.readme_btn_ss)

        self.multi_renamer_btn = QPushButton("Multi-Renamer")
        self.multi_renamer_btn.setStyleSheet(cfg.dark_btn_ss)

        self.comet_rename_btn = QPushButton("Comet Rename")
        self.comet_rename_btn.setStyleSheet('{}; {}'.format(cfg.dark_btn_ss, cfg.medium_btn_width))

        self.rename_it_wider_btn = QPushButton("reNameIt")
        self.rename_it_wider_btn.setStyleSheet("{0}; {1}".format(cfg.row_multi_btns_max_width, cfg.dark_btn_ss))

        # button "CGM"
        self.cgm_toolbox_btn = QPushButton("CG Monks Toolbox")
        self.cgm_toolbox_btn.setStyleSheet('{}; {}'.format(cfg.dark_btn_ss, cfg.medium_btn_width2))

        # button 'PHP'
        self.open_physx_painter_dialog_btn = QPushButton()
        self.open_physx_painter_dialog_btn.setStyleSheet(cfg.text_align_left_ss)
        self.open_physx_painter_dialog_btn.setIcon(QIcon(":paintFXtoNurbs.png"))  # paintBlendshape,
        # paintCluster, paintJiggle, paintEffectsTools, paintSetMembership

        # button 'PHP_?'
        self.physx_painter_readme_btn = QPushButton("?")
        self.physx_painter_readme_btn.setStyleSheet(cfg.readme_btn_ss)

        # button 'PHP_??'
        self.physx_painter_tutorial_btn = QPushButton("??")
        self.physx_painter_tutorial_btn.setStyleSheet(cfg.readme_btn_ss)

        # button 'SBC'
        self.open_soft_body_collision_dialog_btn = QPushButton()
        self.open_soft_body_collision_dialog_btn.setStyleSheet(cfg.text_align_left_ss)
        self.open_soft_body_collision_dialog_btn.setIcon(QIcon(":soft.png"))

        # button 'DBT'
        self.open_dissect_n_transfer_dialog_btn = QPushButton()
        self.open_dissect_n_transfer_dialog_btn.setStyleSheet(cfg.text_align_left_ss)
        self.open_dissect_n_transfer_dialog_btn.setIcon(QIcon(":polyTransferAttributes.png"))  # polyTransfer,

        # button 'DBT_?'
        self.dissect_transfer_readme_btn = QPushButton("?")
        self.dissect_transfer_readme_btn.setStyleSheet(cfg.readme_btn_ss)

        # button 'FCC'
        self.croquet_couture_btn = QPushButton()
        self.croquet_couture_btn.setStyleSheet("{0}; {1}".format(cfg.text_align_left_ss, cfg.croquet_btn_ss))
        self.croquet_couture_btn.setIcon(QIcon(":nClothDisplayCurrent.png"))  # out_nCloth.png

        # button 'FCC_?'
        self.croquet_couture_promo_btn = QPushButton("?")
        self.croquet_couture_promo_btn.setStyleSheet(cfg.readme_btn_ss)

        # button 'FCC_??'
        self.croquet_couture_tutorial_btn = QPushButton("??")
        self.croquet_couture_tutorial_btn.setStyleSheet(cfg.readme_btn_ss)

        self.open_shader_doctor_btn = QPushButton(u"⚕    S H A D E R    D O C T O R    ⚕")
        self.open_shader_doctor_btn.setStyleSheet(cfg.pink_btn_ss)

        self.open_ttStamper_btn = QPushButton("TT STAMPER")
        self.open_ttStamper_btn.setStyleSheet(cfg.terra_btn_ss)

        # TAB C WIDGETS

        # button 'RMC'
        self.replace_mesh_red_gpu_cache_btn = QPushButton()
        # self.replace_mesh_red_gpu_cache_btn.setStyleSheet("{1}".format(cfg.text_align_left_ss, cfg.red_btn_ss))
        self.replace_mesh_red_gpu_cache_btn.setIcon(QIcon(":alignSurface.png"))

        self.replace_mesh_green_gpu_cache_btn = QPushButton('G')
        self.replace_mesh_green_gpu_cache_btn.setStyleSheet("{0}".format(cfg.row_multi_btns_max_width_narrower))

        self.replace_mesh_blue_gpu_cache_btn = QPushButton('B')
        self.replace_mesh_blue_gpu_cache_btn.setStyleSheet("{0}".format(cfg.row_multi_btns_max_width_narrower))

        self.open_gpu_cache_folder_btn = QPushButton()
        self.open_gpu_cache_folder_btn.setIcon(QIcon(":fileOpen.png"))
        self.open_gpu_cache_folder_btn.setStyleSheet(cfg.row_multi_btns_max_width_narrower)

        # QLabel UDIM
        self.udim_label = QLabel("UDIM & Bake")

        # button 'CMS'
        self.create_multi_udim_shaders_btn = QPushButton("Multi shaders")
        self.create_multi_udim_shaders_btn.setStyleSheet(cfg.brown_btn_ss)

        # button 'CUD'
        self.collapse_all_udims_btn = QPushButton("Collapse to 0-1")
        self.collapse_all_udims_btn.setStyleSheet(cfg.brown_btn_ss)

        self.bulk_udim_flip_btn = QPushButton("FlipU")
        self.bulk_udim_flip_btn.setStyleSheet("{0}; {1}".format(cfg.grey_green4_btn_ss,
                                                                cfg.row_multi_btns_max_width_narrower))

        self.explode_meshes_btn = QPushButton("EXPLODE")
        self.explode_meshes_btn.setStyleSheet("{0}; {1}".format(cfg.pink_btn_ss,
                                                                cfg.row_multi_btns_max_width))

        self.center_loc_btn = QPushButton("Locator @center of Selection")
        self.center_loc_btn.setStyleSheet(cfg.grey_green4_btn_ss)

        self.center_joint_btn = QPushButton("Joint")
        self.center_joint_btn.setStyleSheet("{0};{1}".format(cfg.row_multi_btns_max_width, cfg.grey_green4_btn_ss))

        self.basic_aim_constr_btn = QPushButton("Basic Aim Constr")
        self.basic_aim_constr_btn.setStyleSheet(cfg.medium_btn_width)

        # QLabel Mesh Orient
        self.restore_mesh_orient_label = QLabel("Local Axes")

        # button 'RMO1'
        self.restore_mesh_orient1_setup_btn = QPushButton()
        # self.restore_mesh_orient1_setup_btn.setStyleSheet(cfg.row_multi_btns_max_width)
        # self.restore_mesh_orient1_setup_btn.setIcon(QIcon(":polyTextureRotateUV.png"))

        self.restore_mesh_orient1_execute_btn = QPushButton('Restore')
        self.restore_mesh_orient1_execute_btn.setStyleSheet(cfg.row_multi_btns_max_width)

        self.restore_mesh_orient1_quick_n_exact_btn = QPushButton("Quick from Face")
        # self.restore_mesh_orient1_quick_n_exact_btn.setStyleSheet(cfg.dark_btn_ss)

        # button 'RMO2'
        self.restore_mesh_orient2_btn = QPushButton()
        self.restore_mesh_orient2_btn.setStyleSheet("padding: 4px")
        # self.restore_mesh_orient2_btn.setIcon(QIcon(":polyTextureRotateUV.png"))

        # HKLocalTools
        self.hklocaltools_btn = QPushButton("HK Local")
        self.hklocaltools_btn.setStyleSheet("padding: 4px; color: black; background-color: rgb(103, 138, 152);")

        # QLabel 'CCH0'
        self.create_convex_hull_label = QLabel("Convex Hull")

        # button 'CCH1'
        self.create_convex_hull_one_btn = QPushButton()
        self.create_convex_hull_one_btn.setStyleSheet(cfg.dark_btn_ss)

        # button 'CCH2'
        self.create_convex_hull_multiple_btn = QPushButton()
        # self.create_convex_hull_multiple_btn.setStyleSheet(cfg.text_align_left_ss)

        # button 'CCH3'
        self.create_convex_hull_full_btn = QPushButton()
        # self.create_convex_hull_full_btn.setStyleSheet(cfg.text_align_left_ss)

        # TAB C INIT
        self.create_convex_hull_full_btn.setEnabled(False)

        self.poly_remesh_btn = QPushButton("3. polyRemesh (tris)")
        # self.poly_remesh_btn.setStyleSheet(cfg.grey_green4_btn_ss)

        self.poly_retopo_btn = QPushButton("4. polyRetopo (quad)")
        # self.poly_retopo_btn.setStyleSheet(cfg.grey_green4_btn_ss)

        # TAB D WIDGETS

        # QLabel 'SEE'
        self.select_every_edge_label = QLabel()

        self.select_every_edge_ring_btn = QPushButton("Ring")
        self.select_every_edge_loop_btn = QPushButton("Loop")
        self.select_every_edge_border_btn = QPushButton("Border")

        self.select_every_edge_ring_btn.setStyleSheet(cfg.row_multi_btns_max_width)
        self.select_every_edge_loop_btn.setStyleSheet(cfg.row_multi_btns_max_width)
        self.select_every_edge_border_btn.setStyleSheet(cfg.row_multi_btns_max_width)

        self.select_every_edge_spinbox = QSpinBox()
        self.select_every_edge_spinbox.setRange(1, 10)
        self.select_every_edge_spinbox.setValue(2)
        self.select_every_edge_spinbox.setFixedWidth(30)
        self.select_every_edge_spinbox.setButtonSymbols(QAbstractSpinBox.NoButtons)

        # QLabel "SEA"
        self.select_all_label = QLabel()

        self.select_all_tris_btn = QPushButton("Tris")
        self.select_all_n_gons_btn = QPushButton("N-gons")
        self.select_all_stray_verts_btn = QPushButton("Stray Verts")

        self.select_all_tris_btn.setStyleSheet(cfg.row_multi_btns_max_width)
        self.select_all_n_gons_btn.setStyleSheet(cfg.row_multi_btns_max_width)

        # button 'SCP'
        self.straighten_components_btn = QPushButton("* Strictly * straighten vertices/edge/curve")
        self.straighten_components_btn.setStyleSheet(
            "{0}; {1}".format(cfg.text_align_left_ss, cfg.yellow_green2_btn_ss))
        self.straighten_components_btn.setIcon(QIcon(":modifyStraighten.png"))

        # button 'CNC'
        self.combine_curves_btn = QPushButton()
        # self.combine_curves_btn.setStyleSheet("{0}; color: black;"
        #                                       "background-color: rgb(135, 202, 189);".format(cfg.text_align_left_ss))
        self.combine_curves_btn.setStyleSheet(cfg.text_align_left_ss)
        self.combine_curves_btn.setIcon(QIcon(":mergeConnections.png"))

        # button 'SNC'
        self.separate_curves_btn = QPushButton()
        self.separate_curves_btn.setStyleSheet(cfg.text_align_left_ss)
        self.separate_curves_btn.setIcon(QIcon(":polySplitUVs.png"))

        # button 'TSM'
        self.tag_s2s_scalp_mesh_btn = QPushButton()
        self.tag_s2s_scalp_mesh_btn.setStyleSheet(cfg.text_align_left_ss)
        self.tag_s2s_scalp_mesh_btn.setIcon(QIcon(":CreativeMarket.png"))

        # button 'S2S'
        self.s2s_curves_btn = QPushButton()
        self.s2s_curves_btn.setStyleSheet(cfg.text_align_left_ss)
        self.s2s_curves_btn.setIcon(QIcon(":LM_snap_toGeo.png"))

        # button 'P2R'
        self.pivot_to_crv_root_btn = QPushButton()
        self.pivot_to_crv_root_btn.setStyleSheet(cfg.text_align_left_ss)
        self.pivot_to_crv_root_btn.setIcon(QIcon(":out_pfxHair.png"))  # hairConvertFollicles, zeroKey

        # button 'P2T'
        self.pivot_to_crv_tip_btn = QPushButton()
        self.pivot_to_crv_tip_btn.setStyleSheet(cfg.text_align_left_ss)
        self.pivot_to_crv_tip_btn.setIcon(QIcon(":bendNLD.png"))  # hairPaint, hairScaleTool, extend, modifyBend

        self.seams_easy_btn = QPushButton("SEAMS EASY")
        self.seams_easy_btn.setStyleSheet(cfg.deep_violet_btn_ss)

        self.seams_easy_tutorial_btn = QPushButton("?")
        self.seams_easy_tutorial_btn.setStyleSheet(cfg.readme_btn_ss)

        self.stitch_easy_btn = QPushButton("STITCH EASY")
        self.stitch_easy_btn.setStyleSheet(cfg.deep_violet_btn_ss)

        self.hair_strand_designer_btn = QPushButton("HAIR STRAND DESIGNER")

        hsd_pixmap = QPixmap(cfg.hsd_icon_path)
        # hsd_pixmap = hsd_pixmap.scaled(30, 30, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
        hsd_icon = QIcon(hsd_pixmap)

        self.hair_strand_designer_btn.setIcon(hsd_icon)
        self.hair_strand_designer_btn.setIconSize(hsd_pixmap.rect().size())
        # self.hair_strand_designer_btn.setStyleSheet(cfg.text_align_left_ss)

        self.open_hsd_sample_folder_btn = QPushButton()
        self.open_hsd_sample_folder_btn.setIcon(QIcon(":fileOpen.png"))
        self.open_hsd_sample_folder_btn.setFixedSize(30, 40)
        # self.open_hsd_sample_folder_btn.setStyleSheet("background-color: rgb(51, 41, 88)")
        self.open_hsd_sample_folder_btn.setStyleSheet(cfg.deep_violet_btn_ss)

        self.materialize_btn = QPushButton("MATERIALIZE")

        materialize_pixmap = QPixmap(cfg.materialize_icon_path)
        # materialize_pixmap = materialize_pixmap.scaled(30, 30, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
        materialize_icon = QIcon(materialize_pixmap)

        self.materialize_btn.setIcon(materialize_icon)
        self.materialize_btn.setIconSize(materialize_pixmap.rect().size())

        self.materialize_tutorial_btn = QPushButton("?")
        self.materialize_tutorial_btn.setStyleSheet(cfg.readme_btn_ss)
        self.materialize_tutorial_btn.setFixedHeight(40)

        self.open_software_folder_btn = QPushButton()
        self.open_software_folder_btn.setIcon(QIcon(":fileOpen.png"))
        self.open_software_folder_btn.setFixedSize(30, 40)
        # self.open_software_folder_btn.setStyleSheet(cfg.dark_btn_ss)

        # TAB E WIDGETS

        self.replace_all_ai_shaders_btn = QPushButton(u"☢  ( ! )    Replace All aiShaders for Proxy Render    ( ! )  ☢")
        self.replace_all_ai_shaders_btn.setStyleSheet(cfg.croquet_btn_ss)

        self.choose_resized_img_output_btn = QPushButton(">...")
        self.choose_resized_img_output_btn.setStyleSheet('{0}; {1}'.format(cfg.row_multi_btns_max_width, cfg.dark_btn_ss))

        self.osd_fvar_boundary_btn = QPushButton("OSD | UV Boundary: Preserve Edges + Corners")
        self.osd_fvar_boundary_btn.setStyleSheet(cfg.grey_green4_btn_ss)

        # QLabel "PI2"
        self.bring_pivot_to_label = QLabel()

        self.pivot_to_ymin_btn = QPushButton("Y min")
        self.pivot_to_ymin_btn.setStyleSheet("{0};{1}".format(cfg.row_multi_btns_max_width, cfg.green_btn_ss))

        self.pivot_to_center_n_ymin_btn = QPushButton("Center + Y min")
        self.pivot_to_center_n_ymin_btn.setStyleSheet(cfg.green_btn_ss)

        # button "SPG"
        self.set_ground_mesh_btn = QPushButton("* Set as ground*")
        self.set_ground_mesh_btn.setStyleSheet(cfg.brown_btn_ss)

        self.move_to_ground_mesh_btn = QPushButton("Snap objs to ground")
        self.move_to_ground_mesh_btn.setStyleSheet(cfg.brown_btn_ss)

        # button 'MFFD'
        self.mirror_ffd_lattice_btn = QPushButton("Mirror FFD Lattices")
        self.mirror_ffd_lattice_btn.setStyleSheet(cfg.text_align_left_ss)
        self.mirror_ffd_lattice_btn.setIcon(QIcon(":lattice.png"))

        # button Mirror Across Local Axes

        self.poly_merge_threshold_spinbox = QDoubleSpinBox()
        self.poly_merge_threshold_spinbox.setRange(0.000, 0.2)
        self.poly_merge_threshold_spinbox.setSingleStep(0.001)
        self.poly_merge_threshold_spinbox.setDecimals(3)
        self.poly_merge_threshold_spinbox.setFixedWidth(40)
        self.poly_merge_threshold_spinbox.setButtonSymbols(QAbstractSpinBox.NoButtons)

        self.poly_merge_threshold_spinbox.setValue(0.001)

        self.mirror_across_local_x_btn = QPushButton("Mirror Across Local X Axis")
        self.mirror_across_local_x_btn.setStyleSheet("background-color: rgb(162, 59, 59)")
        self.mirror_across_local_x_btn.setIcon(QIcon(":polyMirrorCut.png"))  # flipTube

        self.mirror_across_local_y_btn = QPushButton("Y")
        self.mirror_across_local_y_btn.setStyleSheet("{0};{1}".format(cfg.row_multi_btns_max_width, cfg.green_btn_ss))

        self.mirror_across_local_z_btn = QPushButton("Z")
        self.mirror_across_local_z_btn.setStyleSheet("{0};{1}".format(cfg.row_multi_btns_max_width, cfg.blue_btn_ss))

        # button 'SMP'
        self.aim_scale_manip_to_persp_cam_btn = QPushButton()
        self.aim_scale_manip_to_persp_cam_btn.setStyleSheet(cfg.text_align_left_ss)
        self.aim_scale_manip_to_persp_cam_btn.setIcon(QIcon(":cameraAim.png"))

        self.instant_clean_btn = QPushButton("\\\\\\\\\\\\     INSTANT OBJ CLEAN     //////")
        self.instant_clean_btn.setStyleSheet(cfg.grey_blue2_btn_ss)

        # QLabel "CCP"
        self.cam_clip_plane_label = QLabel("Camera clipping plane")
        self.cam_clip_plane_small_btn = QPushButton("S")
        self.cam_clip_plane_medium_btn = QPushButton("M")
        self.cam_clip_plane_large_btn = QPushButton("L")

        self.cam_clip_plane_small_btn.setStyleSheet(cfg.row_multi_btns_max_width)
        self.cam_clip_plane_medium_btn.setStyleSheet(cfg.row_multi_btns_max_width)
        self.cam_clip_plane_large_btn.setStyleSheet(cfg.row_multi_btns_max_width)

        self.force_restore_HUD_btn = QPushButton("Force restore HUD Poly Count")
        self.force_restore_HUD_btn.setStyleSheet("{0}; background-color: rgb(107, 56, 71)"
                                                 .format(cfg.text_align_left_ss))
        self.force_restore_HUD_btn.setIcon(QIcon(":kAlertCautionIcon.png"))

        self.name_from_group_separator_label = QLabel("Separator: ")
        self.name_from_group_separator_le = QLineEdit("_")
        self.name_from_group_separator_le.setFixedWidth(20)

        self.name_from_group_padding_label = QLabel("Zero Padding: ")
        self.name_from_group_padding_cb = QCheckBox()
        self.name_from_group_padding_cb.setChecked(True)

        self.name_from_group_padding_plus_label = QLabel("Plus: ")
        self.name_from_group_padding_plus_spinbox = QSpinBox()
        self.name_from_group_padding_plus_spinbox.setRange(0, 9)
        self.name_from_group_padding_plus_spinbox.setValue(0)
        self.name_from_group_padding_plus_spinbox.setFixedWidth(20)
        self.name_from_group_padding_plus_spinbox.setButtonSymbols(QAbstractSpinBox.NoButtons)

        self.name_from_group_execute_btn = QPushButton("Auto Name from Group")

        # button 'RAW'
        self.reset_all_windows_btn = QPushButton()
        self.reset_all_windows_btn.setStyleSheet("{0}; background-color: rgb(107, 56, 71)"
                                                 .format(cfg.text_align_left_ss))
        self.reset_all_windows_btn.setIcon(QIcon(":kAlertCautionIcon.png"))  # deletePreset

        # QLabel 'PFD'
        self.perform_file_drop_label = QLabel()
        self.perform_file_drop_label.setFixedHeight(20)

        self.pfd_do_current_btn = QPushButton("Setup one")
        self.pfd_do_all_btn = QPushButton("Setup all")
        self.pfd_remove_current_btn = QPushButton("Remove one")
        self.pfd_remove_all_btn = QPushButton("Remove all")

        # button 'MUV'
        # self.edit_morphed_UV_btn = QPushButton()
        # self.edit_morphed_UV_btn.setStyleSheet(cfg.text_align_left_ss)
        # self.edit_morphed_UV_btn.setIcon(QIcon(":polyUnfoldUV.png"))  # polyUnitizeUVs, layoutUV, polyLayoutUV,
        # polyMapMoveUV_S, polyNormalizeUV, polyNormalizeUVs, polyStraightenUVBorder

        # button "UMT"
        # self.udim_manual_tiling_btn = QPushButton()
        # self.udim_manual_tiling_btn.setStyleSheet(cfg.text_align_left_ss)
        # self.udim_manual_tiling_btn.setIcon(QIcon(":growUVSelection.png"))  # polyGridUV, UV_Grab_Brush,
        # UVDistributeUVs

        # button "MNT2"
        # self.update_mnt2_module_files_btn = QPushButton()
        # self.update_mnt2_module_files_btn.setStyleSheet(cfg.text_align_left_ss)
        # self.update_mnt2_module_files_btn.setIcon(QIcon(":RS_accept_update.png"))  # uvUpdate.png

        # TAB F WIDGETS

        self.remove_plugin_autoload_btn = QPushButton(u'🚀   Speed up Maya launch time   🚀')
        self.remove_plugin_autoload_btn.setStyleSheet(cfg.deep_violet_btn_ss)

        # button 'SAN'
        self.save_as_w_file_name_from_selected_btn = QPushButton()
        self.save_as_w_file_name_from_selected_btn.setStyleSheet(
            "{0}; {1}".format(cfg.text_align_left_ss, cfg.dark_gold_btn_ss))
        self.save_as_w_file_name_from_selected_btn.setIcon(QIcon(":fileSave.png"))  # leftArrowPlus.png

        # button 'ATP'
        self.prep_for_animated_cb_thumbnail_btn = QPushButton()
        self.prep_for_animated_cb_thumbnail_btn.setStyleSheet(cfg.text_align_left_ss)
        self.prep_for_animated_cb_thumbnail_btn.setIcon(QIcon(":render_imagePlane.png"))

        # button 'BTW'
        self.bring_all_to_world_origin_btn = QPushButton()
        self.bring_all_to_world_origin_btn.setStyleSheet(cfg.text_align_left_ss)
        self.bring_all_to_world_origin_btn.setIcon(QIcon(":zeroDepth.png"))  # defaultCrossHair.png, srfIntersect.png

        # TAB G WIDGETS

        # ultimate clipboard
        self.ultimate_clipboard_btn = QPushButton(u"❤    U L T I M A T E     C L I P B O A R D    ✉")
        self.ultimate_clipboard_btn.setStyleSheet("color: rgb(255, 79, 166); background-color: rgb(51, 34, 120)")

        self.maya_to_zbrush_btn = QPushButton(">>> To ZBrush")
        self.maya_to_zbrush_btn.setStyleSheet(cfg.bordeaux_btn_ss)

        self.zbrush_to_maya_btn = QPushButton("From ZBrush >>>")
        self.zbrush_to_maya_btn.setStyleSheet(cfg.sea_green5_btn_ss)

        self.ziniTools_btn = QPushButton("ZiniTools")
        self.ziniTools_btn.setStyleSheet("{0}; {1}".format(cfg.row_multi_btns_max_width, cfg.dark_btn_ss))

        # button 'ESM'
        self.export_separately_ma_btn = QPushButton()
        self.export_separately_ma_btn.setStyleSheet(cfg.text_align_left_ss)
        self.export_separately_ma_btn.setIcon(QIcon(":greasePencilExport.png"))

        self.open_exported_ma_output_folder_btn = QPushButton()
        self.open_exported_ma_output_folder_btn.setIcon(QIcon(":fileOpen.png"))
        self.open_exported_ma_output_folder_btn.setStyleSheet(cfg.folder_btn_ss)
        # self.open_exported_ma_output_folder_btn.setToolTip("Open output folder")

        # button 'ESF'
        self.export_separately_fbx_btn = QPushButton()
        self.export_separately_fbx_btn.setStyleSheet(cfg.text_align_left_ss)
        self.export_separately_fbx_btn.setIcon(QIcon(":greasePencilExport.png"))

        self.open_exported_fbx_output_folder_btn = QPushButton()
        self.open_exported_fbx_output_folder_btn.setIcon(QIcon(":fileOpen.png"))
        self.open_exported_fbx_output_folder_btn.setStyleSheet(cfg.folder_btn_ss)
        # self.open_exported_fbx_output_folder_btn.setToolTip("Open output folder")

        # button 'ESO'

        self.export_separately_obj_btn = QPushButton()
        self.export_separately_obj_btn.setStyleSheet(cfg.text_align_left_ss)
        self.export_separately_obj_btn.setIcon(QIcon(":greasePencilExport.png"))

        self.open_exported_obj_output_folder_btn = QPushButton()
        self.open_exported_obj_output_folder_btn.setIcon(QIcon(":fileOpen.png"))
        self.open_exported_obj_output_folder_btn.setStyleSheet(cfg.folder_btn_ss)

        self.choose_separately_ass_output_btn = QPushButton(">...")
        self.choose_separately_ass_output_btn.setStyleSheet(cfg.row_multi_btns_max_width)

        self.export_separately_ass_btn = QPushButton("Replace each with aiStandIn")
        # self.export_separately_ass_btn.setStyleSheet(cfg.text_align_left_ss)

        self.separately_ass_del_orig_cb = QCheckBox("Del Orig")
        self.separately_ass_del_orig_cb.setStyleSheet(cfg.medium_btn_width)
        self.separately_ass_del_orig_cb.setChecked(True)

        # button 'STR'
        self.strip_the_rig_btn = QPushButton()

        self.strip_the_rig_btn.setStyleSheet(cfg.text_align_left_ss)
        self.strip_the_rig_btn.setIcon(QIcon(":HIKcreateControlRig.png"))

    def create_layouts(self):
        # COMMON LAYOUT

        locale_picker_row_lo = QHBoxLayout()
        locale_picker_row_lo.addWidget(self.mat_picker_btn)
        locale_picker_row_lo.addStretch()
        locale_picker_row_lo.addWidget(self.locale_toggle_cb)

        VB_margin = 3
        VB_spacing = 2

        # TAB A LAYOUT

        A_main_layout = QVBoxLayout()
        A_main_layout.setContentsMargins(VB_margin, VB_margin, VB_margin, VB_margin)
        A_main_layout.setSpacing(VB_spacing)

        A_kitbash_browser_btns_row_lo = QHBoxLayout()
        A_kitbash_browser_btns_row_lo.addWidget(self.open_kitbash_browser_btn)
        A_kitbash_browser_btns_row_lo.addWidget(self.open_repo_kitbash_lib_folder_btn)

        A_env_browser_btns_row_lo = QHBoxLayout()
        A_env_browser_btns_row_lo.addWidget(self.open_env_browser_btn)
        A_env_browser_btns_row_lo.addWidget(self.open_repo_env_lib_folder_btn)

        A_costume_browser_btns_row_lo = QHBoxLayout()
        A_costume_browser_btns_row_lo.addWidget(self.open_costume_browser_btn)
        A_costume_browser_btns_row_lo.addWidget(self.open_repo_costume_lib_folder_btn)

        A_char_browser_btns_row_lo = QHBoxLayout()
        A_char_browser_btns_row_lo.addWidget(self.open_char_browser_btn)
        A_char_browser_btns_row_lo.addWidget(self.open_repo_char_lib_folder_btn)

        A_creature_browser_btns_row_lo = QHBoxLayout()
        A_creature_browser_btns_row_lo.addWidget(self.open_creature_browser_btn)
        A_creature_browser_btns_row_lo.addWidget(self.open_repo_creature_lib_folder_btn)

        A_hda_browser_btns_row_lo = QHBoxLayout()
        A_hda_browser_btns_row_lo.addWidget(self.open_hda_browser_btn)
        A_hda_browser_btns_row_lo.addWidget(self.open_repo_hda_lib_folder_btn)

        A_main_layout.addLayout(A_kitbash_browser_btns_row_lo)
        A_main_layout.addLayout(A_env_browser_btns_row_lo)
        A_main_layout.addLayout(A_costume_browser_btns_row_lo)
        A_main_layout.addLayout(A_char_browser_btns_row_lo)
        A_main_layout.addLayout(A_creature_browser_btns_row_lo)
        A_main_layout.addLayout(A_hda_browser_btns_row_lo)

        self.A_tab.setLayout(A_main_layout)

        # TAB B LAYOUT

        B_main_layout = QVBoxLayout()
        B_main_layout.setContentsMargins(VB_margin, VB_margin, VB_margin, VB_margin)
        B_main_layout.setSpacing(VB_spacing)

        B_vmtb_btns_row_lo = QHBoxLayout()
        B_vmtb_btns_row_lo.addWidget(self.vmtb_btn)
        B_vmtb_btns_row_lo.addWidget(self.vmtb_tutorials_btn)
        B_vmtb_btns_row_lo.addWidget(self.vmtb_download_btn)
        B_vmtb_btns_row_lo.addWidget(self.vsTools1_btn)

        B_loot_row_lo_1 = QHBoxLayout()
        B_loot_row_lo_1.addWidget(self.speed_cut_btn)
        B_loot_row_lo_1.addWidget(self.speed_cut_tutorials_btn)
        B_loot_row_lo_1.addWidget(self.quick_pipe_btn)
        B_loot_row_lo_1.addWidget(self.quick_pipe_tutorial_btn)
        B_loot_row_lo_1.addWidget(self.ninja_dojo_btn)

        B_zen_row_lo = QHBoxLayout()
        B_zen_row_lo.addWidget(self.rename_it_wider_btn)
        B_zen_row_lo.addWidget(self.zen_tools_btn)
        B_zen_row_lo.addWidget(self.bool_btn)
        B_zen_row_lo.addWidget(self.booltool_tutorial_btn)

        B_cgm_row_lo = QHBoxLayout()
        B_cgm_row_lo.addWidget(self.multi_renamer_btn)
        B_cgm_row_lo.addWidget(self.comet_rename_btn)
        B_cgm_row_lo.addWidget(self.cgm_toolbox_btn)

        B_croquet_couture_btns_row_lo = QHBoxLayout()
        B_croquet_couture_btns_row_lo.addWidget(self.dissect_transfer_readme_btn)
        B_croquet_couture_btns_row_lo.addWidget(self.open_dissect_n_transfer_dialog_btn)
        B_croquet_couture_btns_row_lo.addWidget(self.croquet_couture_btn)
        B_croquet_couture_btns_row_lo.addWidget(self.croquet_couture_promo_btn)
        B_croquet_couture_btns_row_lo.addWidget(self.croquet_couture_tutorial_btn)

        B_physx_painter_btns_row_lo = QHBoxLayout()
        B_physx_painter_btns_row_lo.addWidget(self.physx_painter_readme_btn)
        B_physx_painter_btns_row_lo.addWidget(self.physx_painter_tutorial_btn)
        B_physx_painter_btns_row_lo.addWidget(self.open_physx_painter_dialog_btn)
        B_physx_painter_btns_row_lo.addWidget(self.open_soft_body_collision_dialog_btn)

        B_shader_doctor_btns_row_lo = QHBoxLayout()
        B_shader_doctor_btns_row_lo.addWidget(self.open_shader_doctor_btn)
        B_shader_doctor_btns_row_lo.addWidget(self.open_ttStamper_btn)

        B_main_layout.addLayout(B_vmtb_btns_row_lo)

        if mnT2Dialog.LOOT:
            B_main_layout.addLayout(B_loot_row_lo_1)

        B_main_layout.addLayout(B_zen_row_lo)
        B_main_layout.addLayout(B_cgm_row_lo)
        B_main_layout.addLayout(B_physx_painter_btns_row_lo)
        B_main_layout.addLayout(B_croquet_couture_btns_row_lo)
        B_main_layout.addLayout(B_shader_doctor_btns_row_lo)

        self.B_tab.setLayout(B_main_layout)

        # TAB C LAYOUT

        C_main_layout = QVBoxLayout()
        C_main_layout.setContentsMargins(VB_margin, VB_margin, VB_margin, VB_margin)
        C_main_layout.setSpacing(VB_spacing)

        C_gpu_cache_btns_row_lo = QHBoxLayout()
        C_gpu_cache_btns_row_lo.addWidget(self.replace_mesh_red_gpu_cache_btn)
        C_gpu_cache_btns_row_lo.addWidget(self.replace_mesh_green_gpu_cache_btn)
        C_gpu_cache_btns_row_lo.addWidget(self.replace_mesh_blue_gpu_cache_btn)
        C_gpu_cache_btns_row_lo.addWidget(self.open_gpu_cache_folder_btn)

        C_collapse_udim_btns_row_lo = QHBoxLayout()
        C_collapse_udim_btns_row_lo.addWidget(self.udim_label)
        C_collapse_udim_btns_row_lo.addWidget(self.create_multi_udim_shaders_btn)
        C_collapse_udim_btns_row_lo.addWidget(self.collapse_all_udims_btn)
        C_collapse_udim_btns_row_lo.addWidget(self.bulk_udim_flip_btn)
        C_collapse_udim_btns_row_lo.addWidget(self.explode_meshes_btn)

        C_restore_mesh_orient1_btns_row_lo = QHBoxLayout()
        C_restore_mesh_orient1_btns_row_lo.addWidget(self.restore_mesh_orient_label)
        C_restore_mesh_orient1_btns_row_lo.addWidget(self.restore_mesh_orient1_setup_btn)
        C_restore_mesh_orient1_btns_row_lo.addWidget(self.restore_mesh_orient1_execute_btn)
        C_restore_mesh_orient1_btns_row_lo.addWidget(self.restore_mesh_orient1_quick_n_exact_btn)

        C_restore_mesh_orient2_btns_row_lo = QHBoxLayout()
        C_restore_mesh_orient2_btns_row_lo.addWidget(self.restore_mesh_orient2_btn)
        C_restore_mesh_orient2_btns_row_lo.addWidget(self.hklocaltools_btn)

        C_mirror_across_local_axis_btns_row_lo = QHBoxLayout()
        C_mirror_across_local_axis_btns_row_lo.addWidget(self.poly_merge_threshold_spinbox)
        C_mirror_across_local_axis_btns_row_lo.addWidget(self.mirror_across_local_x_btn)
        C_mirror_across_local_axis_btns_row_lo.addWidget(self.mirror_across_local_y_btn)
        C_mirror_across_local_axis_btns_row_lo.addWidget(self.mirror_across_local_z_btn)

        C_center_thingy_btns_row_lo = QHBoxLayout()
        C_center_thingy_btns_row_lo.addWidget(self.center_loc_btn)
        C_center_thingy_btns_row_lo.addWidget(self.center_joint_btn)
        C_center_thingy_btns_row_lo.addWidget(self.basic_aim_constr_btn)

        C_convex_hull_btns_row_lo = QHBoxLayout()
        C_convex_hull_btns_row_lo.addWidget(self.create_convex_hull_label)
        C_convex_hull_btns_row_lo.addWidget(self.create_convex_hull_one_btn)
        C_convex_hull_btns_row_lo.addWidget(self.create_convex_hull_multiple_btn)
        # C_convex_hull_btns_row_lo.addWidget(self.create_convex_hull_full_btn)

        C_poly_remesh_retopo_btns_row_lo = QHBoxLayout()
        C_poly_remesh_retopo_btns_row_lo.addWidget(self.poly_remesh_btn)
        C_poly_remesh_retopo_btns_row_lo.addWidget(self.poly_retopo_btn)

        C_main_layout.addLayout(C_gpu_cache_btns_row_lo)
        # C_main_layout.addWidget(self.udim_manual_tiling_btn)  # removes this button as Sparx* tool now has the same
        # functionality
        C_main_layout.addLayout(C_collapse_udim_btns_row_lo)
        C_main_layout.addLayout(C_convex_hull_btns_row_lo)
        C_main_layout.addLayout(C_restore_mesh_orient1_btns_row_lo)
        C_main_layout.addLayout(C_restore_mesh_orient2_btns_row_lo)
        C_main_layout.addLayout(C_mirror_across_local_axis_btns_row_lo)
        C_main_layout.addLayout(C_center_thingy_btns_row_lo)
        C_main_layout.addLayout(C_poly_remesh_retopo_btns_row_lo)

        self.C_tab.setLayout(C_main_layout)

        # TAB D LAYOUT

        D_main_layout = QVBoxLayout()
        D_main_layout.setContentsMargins(VB_margin, VB_margin, VB_margin, VB_margin)
        D_main_layout.setSpacing(VB_spacing)

        D_select_every_btns_row_lo = QHBoxLayout()
        D_select_every_btns_row_lo.addWidget(self.select_every_edge_label)
        D_select_every_btns_row_lo.addWidget(self.select_every_edge_spinbox)
        D_select_every_btns_row_lo.addWidget(self.select_every_edge_ring_btn)
        D_select_every_btns_row_lo.addWidget(self.select_every_edge_loop_btn)
        D_select_every_btns_row_lo.addWidget(self.select_every_edge_border_btn)

        D_select_all_btns_row_lo = QHBoxLayout()
        D_select_all_btns_row_lo.addWidget(self.select_all_label)
        D_select_all_btns_row_lo.addWidget(self.select_all_tris_btn)
        D_select_all_btns_row_lo.addWidget(self.select_all_n_gons_btn)
        D_select_all_btns_row_lo.addWidget(self.select_all_stray_verts_btn)

        D_combine_separate_crvs_btns_row_lo = QHBoxLayout()
        D_combine_separate_crvs_btns_row_lo.addWidget(self.combine_curves_btn)
        D_combine_separate_crvs_btns_row_lo.addWidget(self.separate_curves_btn)

        D_s2s_scalp_btns_row_lo = QHBoxLayout()
        D_s2s_scalp_btns_row_lo.addWidget(self.tag_s2s_scalp_mesh_btn)
        D_s2s_scalp_btns_row_lo.addWidget(self.s2s_curves_btn)

        D_pivot_snap_btns_row_lo = QHBoxLayout()
        D_pivot_snap_btns_row_lo.addWidget(self.pivot_to_crv_root_btn)
        D_pivot_snap_btns_row_lo.addWidget(self.pivot_to_crv_tip_btn)

        D_seams_easy_btns_row_lo = QHBoxLayout()
        D_seams_easy_btns_row_lo.addWidget(self.seams_easy_btn)
        D_seams_easy_btns_row_lo.addWidget(self.seams_easy_tutorial_btn)
        D_seams_easy_btns_row_lo.addWidget(self.stitch_easy_btn)

        D_app_btns_row_lo = QHBoxLayout()
        D_app_btns_row_lo.addWidget(self.open_hsd_sample_folder_btn)
        D_app_btns_row_lo.addWidget(self.hair_strand_designer_btn)
        D_app_btns_row_lo.addWidget(self.materialize_btn)
        D_app_btns_row_lo.addWidget(self.materialize_tutorial_btn)
        D_app_btns_row_lo.addWidget(self.open_software_folder_btn)

        D_main_layout.addLayout(D_select_every_btns_row_lo)
        D_main_layout.addLayout(D_select_all_btns_row_lo)
        D_main_layout.addWidget(self.straighten_components_btn)
        D_main_layout.addLayout(D_combine_separate_crvs_btns_row_lo)
        D_main_layout.addLayout(D_s2s_scalp_btns_row_lo)
        D_main_layout.addLayout(D_pivot_snap_btns_row_lo)
        D_main_layout.addLayout(D_seams_easy_btns_row_lo)
        D_main_layout.addLayout(D_app_btns_row_lo)

        self.D_tab.setLayout(D_main_layout)

        # TAB E LAYOUT

        E_main_layout = QVBoxLayout()
        E_main_layout.setContentsMargins(VB_margin, VB_margin, VB_margin, VB_margin)
        E_main_layout.setSpacing(VB_spacing)

        E_bring_pivot_to_btns_row_lo = QHBoxLayout()
        E_bring_pivot_to_btns_row_lo.addWidget(self.bring_pivot_to_label)
        E_bring_pivot_to_btns_row_lo.addWidget(self.pivot_to_ymin_btn)
        E_bring_pivot_to_btns_row_lo.addWidget(self.pivot_to_center_n_ymin_btn)

        E_move_to_ground_btns_row_lo = QHBoxLayout()
        E_move_to_ground_btns_row_lo.addWidget(self.set_ground_mesh_btn)
        E_move_to_ground_btns_row_lo.addWidget(self.move_to_ground_mesh_btn)

        E_name_from_group_row_lo = QHBoxLayout()
        E_name_from_group_row_lo.addWidget(self.name_from_group_separator_label)
        E_name_from_group_row_lo.addWidget(self.name_from_group_separator_le)
        E_name_from_group_row_lo.addWidget(self.name_from_group_padding_label)
        E_name_from_group_row_lo.addWidget(self.name_from_group_padding_cb)
        E_name_from_group_row_lo.addWidget(self.name_from_group_padding_plus_label)
        E_name_from_group_row_lo.addWidget(self.name_from_group_padding_plus_spinbox)
        E_name_from_group_row_lo.addWidget(self.name_from_group_execute_btn)

        E_replace_all_ai_shaders_btns_row_lo = QHBoxLayout()
        E_replace_all_ai_shaders_btns_row_lo.addWidget(self.choose_resized_img_output_btn)
        E_replace_all_ai_shaders_btns_row_lo.addWidget(self.replace_all_ai_shaders_btn)

        E_main_layout.addLayout(E_replace_all_ai_shaders_btns_row_lo)
        E_main_layout.addWidget(self.instant_clean_btn)
        E_main_layout.addLayout(E_bring_pivot_to_btns_row_lo)
        E_main_layout.addLayout(E_move_to_ground_btns_row_lo)

        E_main_layout.addWidget(self.mirror_ffd_lattice_btn)
        E_main_layout.addWidget(self.aim_scale_manip_to_persp_cam_btn)
        E_main_layout.addWidget(self.osd_fvar_boundary_btn)

        E_main_layout.addLayout(E_name_from_group_row_lo)

        self.E_tab.setLayout(E_main_layout)

        # TAB F LAYOUT

        F_main_layout = QVBoxLayout()
        F_main_layout.setContentsMargins(VB_margin, VB_margin, VB_margin, VB_margin)
        F_main_layout.setSpacing(VB_spacing)

        F_content_browser_btns_row_lo = QHBoxLayout()
        F_content_browser_btns_row_lo.addWidget(self.save_as_w_file_name_from_selected_btn)
        F_content_browser_btns_row_lo.addWidget(self.prep_for_animated_cb_thumbnail_btn)

        F_cam_clip_plane_btns_row_lo = QHBoxLayout()
        F_cam_clip_plane_btns_row_lo.addWidget(self.cam_clip_plane_label)
        F_cam_clip_plane_btns_row_lo.addWidget(self.cam_clip_plane_small_btn)
        F_cam_clip_plane_btns_row_lo.addWidget(self.cam_clip_plane_medium_btn)
        F_cam_clip_plane_btns_row_lo.addWidget(self.cam_clip_plane_large_btn)

        F_file_drop_btns_row_lo = QHBoxLayout()
        F_file_drop_btns_row_lo.addWidget(self.pfd_do_current_btn)
        F_file_drop_btns_row_lo.addWidget(self.pfd_do_all_btn)
        F_file_drop_btns_row_lo.addWidget(self.pfd_remove_current_btn)
        F_file_drop_btns_row_lo.addWidget(self.pfd_remove_all_btn)

        F_reset_btns_row_lo = QHBoxLayout()
        F_reset_btns_row_lo.addWidget(self.force_restore_HUD_btn)
        F_reset_btns_row_lo.addWidget(self.reset_all_windows_btn)

        F_main_layout.addWidget(self.remove_plugin_autoload_btn)
        F_main_layout.addLayout(F_content_browser_btns_row_lo)
        F_main_layout.addWidget(self.bring_all_to_world_origin_btn)
        F_main_layout.addLayout(F_cam_clip_plane_btns_row_lo)
        F_main_layout.addLayout(F_reset_btns_row_lo)
        F_main_layout.addWidget(self.perform_file_drop_label)
        F_main_layout.addLayout(F_file_drop_btns_row_lo)

        # F_main_layout.addWidget(self.edit_morphed_UV_btn)
        # F_main_layout.addWidget(self.update_mnt2_module_files_btn)

        self.F_tab.setLayout(F_main_layout)

        # TAB G LAYOUT

        G_main_layout = QVBoxLayout()
        G_main_layout.setContentsMargins(VB_margin, VB_margin, VB_margin, VB_margin)
        G_main_layout.setSpacing(VB_spacing)

        G_ma_to_zb_btns_row_lo = QHBoxLayout()
        G_ma_to_zb_btns_row_lo.addWidget(self.maya_to_zbrush_btn)
        G_ma_to_zb_btns_row_lo.addWidget(self.zbrush_to_maya_btn)
        G_ma_to_zb_btns_row_lo.addWidget(self.ziniTools_btn)

        G_export_ma_btns_row_lo = QHBoxLayout()
        G_export_ma_btns_row_lo.addWidget(self.export_separately_ma_btn)
        G_export_ma_btns_row_lo.addWidget(self.open_exported_ma_output_folder_btn)

        G_export_fbx_btns_row_lo = QHBoxLayout()
        G_export_fbx_btns_row_lo.addWidget(self.export_separately_fbx_btn)
        G_export_fbx_btns_row_lo.addWidget(self.open_exported_fbx_output_folder_btn)

        G_export_obj_btns_row_lo = QHBoxLayout()
        G_export_obj_btns_row_lo.addWidget(self.export_separately_obj_btn)
        G_export_obj_btns_row_lo.addWidget(self.open_exported_obj_output_folder_btn)

        G_export_ass_btns_row_lo = QHBoxLayout()
        G_export_ass_btns_row_lo.addWidget(self.separately_ass_del_orig_cb)
        G_export_ass_btns_row_lo.addWidget(self.choose_separately_ass_output_btn)
        G_export_ass_btns_row_lo.addWidget(self.export_separately_ass_btn)

        G_main_layout.addWidget(self.ultimate_clipboard_btn)
        G_main_layout.addLayout(G_ma_to_zb_btns_row_lo)
        G_main_layout.addLayout(G_export_ma_btns_row_lo)
        G_main_layout.addLayout(G_export_fbx_btns_row_lo)
        G_main_layout.addLayout(G_export_obj_btns_row_lo)
        G_main_layout.addLayout(G_export_ass_btns_row_lo)

        G_main_layout.addWidget(self.strip_the_rig_btn)

        self.G_tab.setLayout(G_main_layout)

        # MASTER LAYOUT

        self.tabA_index = self.main_dialog_tabs.addTab(self.A_tab, "")
        self.tabB_index = self.main_dialog_tabs.addTab(self.B_tab, "")
        self.tabC_index = self.main_dialog_tabs.addTab(self.C_tab, "")
        self.tabD_index = self.main_dialog_tabs.addTab(self.D_tab, "")
        self.tabE_index = self.main_dialog_tabs.addTab(self.E_tab, "")
        self.tabF_index = self.main_dialog_tabs.addTab(self.F_tab, "")
        self.tabG_index = self.main_dialog_tabs.addTab(self.G_tab, "")
        self.main_dialog_tabs.setCurrentIndex(self.tabD_index)

        # self.main_dialog_tabs.setTabIcon(self.tabB_index, QIcon(":toolSettings.png"))  # Toolbox
        # self.main_dialog_tabs.setTabIcon(self.tabD_index, QIcon(":lineTangent.png"))  # "Edge"  "lineV.png"
        # self.main_dialog_tabs.setTabIcon(self.tabG_index, QIcon(":outArrow.png"))  # Export

        master_layout = QVBoxLayout(self)
        master_layout.setContentsMargins(0, 0, 0, 0)
        master_layout.setSpacing(VB_spacing)
        master_layout.addLayout(locale_picker_row_lo)
        master_layout.addWidget(self.main_dialog_tabs)

    def create_connections(self):
        self.locale_toggle_cb.toggled.connect(self.switch_button_text)

        self.mat_picker_btn.clicked.connect(mnT2.launch_material_picker)

        self.open_kitbash_browser_btn.clicked.connect(partial(mnT2.open_content_browser,
                                                              main_content_path=cfg.repo_kitbash_path,
                                                              landing_subfolder_name=cfg.repo_kitbash_folder_name))
        self.open_env_browser_btn.clicked.connect(partial(mnT2.open_content_browser,
                                                          main_content_path=cfg.repo_env_path,
                                                          landing_subfolder_name=cfg.repo_env_folder_name))
        self.open_costume_browser_btn.clicked.connect(partial(mnT2.open_content_browser,
                                                              main_content_path=cfg.repo_costume_path,
                                                              landing_subfolder_name=cfg.repo_costume_folder_name))
        self.open_char_browser_btn.clicked.connect(partial(mnT2.open_content_browser,
                                                           main_content_path=cfg.repo_char_path,
                                                           landing_subfolder_name=cfg.repo_char_folder_name))
        self.open_creature_browser_btn.clicked.connect(partial(mnT2.open_content_browser,
                                                               main_content_path=cfg.repo_creature_path,
                                                               landing_subfolder_name=cfg.repo_creature_folder_name))
        self.open_hda_browser_btn.clicked.connect(partial(mnT2.open_content_browser,
                                                          main_content_path=cfg.repo_hda_path,
                                                          landing_subfolder_name=cfg.repo_hda_folder_name))

        self.open_repo_kitbash_lib_folder_btn.clicked.connect(partial(self.open_file_explorer,
                                                                      folder_path=cfg.repo_kitbash_path))
        self.open_repo_env_lib_folder_btn.clicked.connect(partial(self.open_file_explorer,
                                                                  folder_path=cfg.repo_env_path))
        self.open_repo_costume_lib_folder_btn.clicked.connect(partial(self.open_file_explorer,
                                                                      folder_path=cfg.repo_costume_path))
        self.open_repo_char_lib_folder_btn.clicked.connect(partial(self.open_file_explorer,
                                                                   folder_path=cfg.repo_char_path))
        self.open_repo_creature_lib_folder_btn.clicked.connect(partial(self.open_file_explorer,
                                                                       folder_path=cfg.repo_creature_path))
        self.open_repo_hda_lib_folder_btn.clicked.connect(partial(self.open_file_explorer,
                                                                  folder_path=cfg.repo_hda_path))

        self.vmtb_btn.clicked.connect(self.launch_vmtb)

        self.vmtb_tutorials_btn.clicked.connect(partial(self.open_instruction,
                                                        root=cfg.repo_tools_instructions_path,
                                                        topic="Virtuos_Maya_Toolbox",
                                                        folder=True))

        self.vmtb_download_btn.clicked.connect(mnT2.download_vmtb_to_maya_app_dir)

        self.vsTools1_btn.clicked.connect(self.launch_vsTools1)

        self.quick_pipe_btn.clicked.connect(self.launch_quick_pipe)

        self.quick_pipe_tutorial_btn.clicked.connect(partial(self.open_instruction,
                                                             root=cfg.repo_tools_instructions_path,
                                                             topic="Chaumette_QuickPipe"))

        self.ninja_dojo_btn.clicked.connect(self.launch_ninja_dojo)
        self.zen_tools_btn.clicked.connect(self.launch_zen_tools)
        self.bool_btn.clicked.connect(mnT2.launch_bool)
        self.booltool_tutorial_btn.clicked.connect(partial(self.open_instruction,
                                                           root=cfg.repo_tools_instructions_path,
                                                           topic="Mainframe_Bool",
                                                           type="Tutorial",
                                                           ext="mp4"))
        self.cgm_toolbox_btn.clicked.connect(self.launch_cgm_toolbox)

        self.rename_it_wider_btn.clicked.connect(partial(mnT2.util.source_all_mel_scripts,
                                                         mel_files_glob_string=cfg.escribano_mel_files_glob_string))

        self.multi_renamer_btn.clicked.connect(partial(mnT2.util.simple_mel, cmd='MultiRenamer'))
        self.comet_rename_btn.clicked.connect(partial(mnT2.util.simple_mel, cmd='cometRename'))

        self.speed_cut_btn.clicked.connect(self.launch_wu_super_cut)
        self.speed_cut_tutorials_btn.clicked.connect(partial(self.open_instruction,
                                                             root=cfg.repo_tools_instructions_path,
                                                             topic="Wu_SpeedCut",
                                                             folder=True))

        self.open_physx_painter_dialog_btn.clicked.connect(self.open_physx_painter_dialog)

        self.physx_painter_readme_btn.clicked.connect(partial(self.open_instruction,
                                                              topic="PhysXPainter"))
        self.physx_painter_tutorial_btn.clicked.connect(partial(self.open_instruction,
                                                                topic="PhysXPainter",
                                                                type="Tutorial"))

        self.open_soft_body_collision_dialog_btn.clicked.connect(self.open_soft_body_collision_dialog)

        self.open_dissect_n_transfer_dialog_btn.clicked.connect(mnT2.DissectNTransferDialog_showUI)

        self.dissect_transfer_readme_btn.clicked.connect(partial(self.open_instruction,
                                                                 topic="DissectBeforeTransfer"))

        self.croquet_couture_btn.clicked.connect(self.launch_croquet_couture)

        self.croquet_couture_promo_btn.clicked.connect(partial(self.open_instruction,
                                                               root=cfg.repo_tools_instructions_path,
                                                               topic="Croquet_Couture",
                                                               type="Promo",
                                                               ext="mp4"))
        self.croquet_couture_tutorial_btn.clicked.connect(partial(self.open_instruction,
                                                                  root=cfg.repo_tools_instructions_path,
                                                                  topic="Croquet_Couture",
                                                                  type="Tutorial",
                                                                  ext="mp4"))

        self.open_shader_doctor_btn.clicked.connect(mnT2.ShaderDoctorDialog_showUI)
        self.open_ttStamper_btn.clicked.connect(self.launch_ttStamper)

        self.replace_mesh_red_gpu_cache_btn.clicked.connect(self.replace_w_gpu_cache_red)
        self.replace_mesh_green_gpu_cache_btn.clicked.connect(self.replace_w_gpu_cache_green)
        self.replace_mesh_blue_gpu_cache_btn.clicked.connect(self.replace_w_gpu_cache_blue)
        self.open_gpu_cache_folder_btn.clicked.connect(self.open_gpu_cache_folder)

        self.create_multi_udim_shaders_btn.clicked.connect(mnT2.create_multi_udim_shaders)
        self.collapse_all_udims_btn.clicked.connect(mnT2.collapse_all_udims)

        self.bulk_udim_flip_btn.clicked.connect(mnT2.bulk_udim_flip)

        self.explode_meshes_btn.clicked.connect(mnT2.util.run_explode_meshes2)

        self.center_loc_btn.clicked.connect(mnT2.util.center_thingy)

        self.center_joint_btn.clicked.connect(partial(mnT2.util.center_thingy,
                                                      thing="joint"))

        self.basic_aim_constr_btn.clicked.connect(mnT2.util.do_default_aim_constraint)

        self.restore_mesh_orient1_setup_btn.clicked.connect(self.restore_mesh_orient1_common_setup)

        self.restore_mesh_orient1_execute_btn.clicked.connect(partial(mnT2.restore_mesh_orient1_execute,
                                                                      guide_loc=mnT2.RMO1_GUIDE_LOC,
                                                                      frozen_mesh_xform=mnT2.RMO1_FROZEN_MESH_XFORM,
                                                                      guide_loc_buffer_srt=mnT2.RMO1_GUIDE_LOC_BUFFER_SRT))

        self.restore_mesh_orient1_quick_n_exact_btn.clicked.connect(self.restore_mesh_orient1_quick_n_exact)

        self.restore_mesh_orient2_btn.clicked.connect(mnT2.restore_mesh_orient2)

        self.hklocaltools_btn.clicked.connect(self.launch_hklocaltools)

        self.create_convex_hull_one_btn.clicked.connect(mnT2.create_convex_hull_one)
        self.create_convex_hull_multiple_btn.clicked.connect(mnT2.create_convex_hull_multiple)

        self.poly_remesh_btn.clicked.connect(partial(mnT2.util.simple_mel,
                                                     cmd="polyRemesh"))

        self.poly_retopo_btn.clicked.connect(partial(mnT2.util.simple_mel,
                                                     cmd="polyRetopo"))

        self.select_every_edge_ring_btn.clicked.connect(partial(mnT2.util.select_every_edge,
                                                                edge_type="edgeRing",
                                                                num=self.select_every_edge_spinbox.value()))
        self.select_every_edge_loop_btn.clicked.connect(partial(mnT2.util.select_every_edge,
                                                                edge_type="edgeLoop",
                                                                num=self.select_every_edge_spinbox.value()))
        self.select_every_edge_border_btn.clicked.connect(partial(mnT2.util.select_every_edge,
                                                                  edge_type="edgeBorder",
                                                                  num=self.select_every_edge_spinbox.value()))

        self.select_all_tris_btn.clicked.connect(mnT2.util.select_tris_or_n_gons)
        self.select_all_n_gons_btn.clicked.connect(partial(mnT2.util.select_tris_or_n_gons, n_gon=True))
        self.select_all_stray_verts_btn.clicked.connect(mnT2.util.select_stray_vertices)

        self.straighten_components_btn.clicked.connect(mnT2.util.straighten_components)

        self.combine_curves_btn.clicked.connect(mnT2.combine_nurbs_crvs)
        self.separate_curves_btn.clicked.connect(mnT2.separate_nurbs_crvs)
        self.tag_s2s_scalp_mesh_btn.clicked.connect(self.tag_scalp_mesh)
        self.s2s_curves_btn.clicked.connect(mnT2.s2s_curves)

        self.pivot_to_crv_root_btn.clicked.connect(partial(mnT2.pivot_to_curve_cv, last_cv=0))
        self.pivot_to_crv_tip_btn.clicked.connect(partial(mnT2.pivot_to_curve_cv, last_cv=1))

        self.seams_easy_btn.clicked.connect(mnT2.launch_seams_easy)
        self.seams_easy_tutorial_btn.clicked.connect(partial(self.open_instruction,
                                                             root=cfg.repo_tools_instructions_path,
                                                             topic="Stepan_SeamsEasy",
                                                             type="Tutorial",
                                                             ext="mp4"))
        self.stitch_easy_btn.clicked.connect(partial(mnT2.launch_seams_easy, stitch=True))

        self.open_hsd_sample_folder_btn.clicked.connect(partial(self.open_file_explorer,
                                                                folder_path=cfg.hsd_sample_set_path))
        self.hair_strand_designer_btn.clicked.connect(partial(mnT2.download_software,
                                                              exe_key="HairStrand_Designer"))
        self.materialize_btn.clicked.connect(partial(mnT2.download_software,
                                                     exe_key="Materialize"))
        self.materialize_tutorial_btn.clicked.connect(partial(self.open_instruction,
                                                              root=cfg.repo_softwares_instructions_path,
                                                              topic="Materialize",
                                                              type="Tutorial",
                                                              ext="mp4"))
        self.open_software_folder_btn.clicked.connect(self.open_software_local_folder)

        self.choose_resized_img_output_btn.clicked.connect(self.choose_replace_aiShaders_resized_img_output)
        self.replace_all_ai_shaders_btn.clicked.connect(self.do_replace_all_aiShader)

        self.osd_fvar_boundary_btn.clicked.connect(mnT2.set_osdFvarBoundary)

        self.pivot_to_ymin_btn.clicked.connect(mnT2.pivot_to_bbox)
        self.pivot_to_center_n_ymin_btn.clicked.connect(partial(mnT2.pivot_to_bbox, centered=True))

        self.set_ground_mesh_btn.clicked.connect(self.set_ground_mesh)
        self.move_to_ground_mesh_btn.clicked.connect(mnT2.move_to_ground_mesh)

        self.mirror_ffd_lattice_btn.clicked.connect(mnT2.mirror_ffd_lattices)

        self.mirror_across_local_x_btn.clicked.connect(partial(mnT2.mirror_across_object_pivot,
                                                               threshold=self.poly_merge_threshold_spinbox.value()))
        self.mirror_across_local_y_btn.clicked.connect(partial(mnT2.mirror_across_object_pivot,
                                                               axis="Y",
                                                               threshold=self.poly_merge_threshold_spinbox.value()))
        self.mirror_across_local_z_btn.clicked.connect(partial(mnT2.mirror_across_object_pivot,
                                                               axis="Z",
                                                               threshold=self.poly_merge_threshold_spinbox.value()))

        self.aim_scale_manip_to_persp_cam_btn.clicked.connect(mnT2.aim_scale_manip_to_persp_cam)
        self.instant_clean_btn.clicked.connect(self.instant_clean)

        self.name_from_group_padding_cb.toggled.connect(self.auto_name_from_group_enable_padding)
        self.name_from_group_execute_btn.clicked.connect(self.auto_name_from_group)

        self.cam_clip_plane_small_btn.clicked.connect(partial(mnT2.util.set_cam_clip_plane, preset="small"))
        self.cam_clip_plane_medium_btn.clicked.connect(partial(mnT2.util.set_cam_clip_plane, preset="medium"))
        self.cam_clip_plane_large_btn.clicked.connect(partial(mnT2.util.set_cam_clip_plane, preset="large"))

        self.force_restore_HUD_btn.clicked.connect(mnT2.force_restore_HUD)
        self.reset_all_windows_btn.clicked.connect(mnT2.reset_all_windows)

        self.pfd_do_current_btn.clicked.connect(partial(mnT2.perform_file_drop_do_one,
                                                        destination_path=cfg.user_current_maya_script_path))

        self.pfd_do_all_btn.clicked.connect(mnT2.perform_file_drop_do_all)

        self.pfd_remove_current_btn.clicked.connect(partial(mnT2.perform_file_drop_remove_one,
                                                            destination_path=cfg.user_current_maya_script_path))

        self.pfd_remove_all_btn.clicked.connect(mnT2.perform_file_drop_remove_all)

        self.remove_plugin_autoload_btn.clicked.connect(partial(mnT2.remove_plugin_autoload,
                                                                plugins=cfg.MODELING_UNRELATED_PLUGINS))

        self.save_as_w_file_name_from_selected_btn.clicked.connect(mnT2.save_as_w_file_name_from_selected)
        self.prep_for_animated_cb_thumbnail_btn.clicked.connect(mnT2.prep_for_animated_cb_thumbnail)
        self.bring_all_to_world_origin_btn.clicked.connect(mnT2.bring_to_world_origin)

        self.ultimate_clipboard_btn.clicked.connect(self.open_ultimate_clipboard)

        self.maya_to_zbrush_btn.clicked.connect(mnT2.quick_maya_to_zbrush)
        self.zbrush_to_maya_btn.clicked.connect(mnT2.quick_zbrush_to_maya)
        self.ziniTools_btn.clicked.connect(self.launch_ziniTools)

        self.export_separately_ma_btn.clicked.connect(self.export_ma_separately)
        self.open_exported_ma_output_folder_btn.clicked.connect(self.open_exported_ma_output_folder)

        self.export_separately_fbx_btn.clicked.connect(self.export_fbx_separately)
        self.open_exported_fbx_output_folder_btn.clicked.connect(self.open_exported_fbx_output_folder)

        self.export_separately_obj_btn.clicked.connect(self.export_obj_separately)
        self.open_exported_obj_output_folder_btn.clicked.connect(self.open_exported_obj_output_folder)

        self.choose_separately_ass_output_btn.clicked.connect(self.choose_separately_ass_output)
        self.export_separately_ass_btn.clicked.connect(self.export_separately_ass)

        self.strip_the_rig_btn.clicked.connect(self.launch_StripTheRigDialog)

        # self.edit_morphed_UV_btn.clicked.connect(mnT2.edit_on_morphed_UV)
        # self.udim_manual_tiling_btn.clicked.connect(mnT2.UDIMManualTilingDialog_showUI)
        # self.update_mnt2_module_files_btn.clicked.connect(mnT2.update_modules)

    def switch_button_text(self, checked):

        if checked:
            locale = 'EN'
        else:
            locale = 'VI'

        # TAB TEXT
        self.main_dialog_tabs.setTabText(self.tabA_index, label.TAB_TEXTS['tabA'][locale])
        self.main_dialog_tabs.setTabText(self.tabB_index, label.TAB_TEXTS['tabB'][locale])
        self.main_dialog_tabs.setTabText(self.tabC_index, label.TAB_TEXTS['tabC'][locale])
        self.main_dialog_tabs.setTabText(self.tabD_index, label.TAB_TEXTS['tabD'][locale])
        self.main_dialog_tabs.setTabText(self.tabE_index, label.TAB_TEXTS['tabE'][locale])
        self.main_dialog_tabs.setTabText(self.tabF_index, label.TAB_TEXTS['tabF'][locale])
        self.main_dialog_tabs.setTabText(self.tabG_index, label.TAB_TEXTS['tabG'][locale])

        # BUTTON LABELS
        self.open_kitbash_browser_btn.setText(label.BUTTON_LABELS['OKB'][locale])
        self.open_env_browser_btn.setText(label.BUTTON_LABELS['OEN'][locale])
        self.open_costume_browser_btn.setText(label.BUTTON_LABELS['OCO'][locale])
        self.open_char_browser_btn.setText(label.BUTTON_LABELS['OCH'][locale])
        self.open_creature_browser_btn.setText(label.BUTTON_LABELS['OAC'][locale])

        self.open_physx_painter_dialog_btn.setText(label.BUTTON_LABELS['PHP'][locale])
        self.open_soft_body_collision_dialog_btn.setText(label.BUTTON_LABELS['SBC'][locale])

        self.replace_mesh_red_gpu_cache_btn.setText(label.BUTTON_LABELS['RMC'][locale])
        self.restore_mesh_orient1_setup_btn.setText(label.BUTTON_LABELS['RMO1'][locale])
        self.restore_mesh_orient2_btn.setText(label.BUTTON_LABELS['RMO2'][locale])

        self.bring_pivot_to_label.setText(label.BUTTON_LABELS['PI2'][locale])

        self.create_convex_hull_one_btn.setText(label.BUTTON_LABELS['CCH1'][locale])
        self.create_convex_hull_multiple_btn.setText(label.BUTTON_LABELS['CCH2'][locale])
        self.create_convex_hull_full_btn.setText(label.BUTTON_LABELS['CCH3'][locale])

        self.croquet_couture_btn.setText(label.BUTTON_LABELS['FCC'][locale])
        self.combine_curves_btn.setText(label.BUTTON_LABELS['CNC'][locale])
        self.separate_curves_btn.setText(label.BUTTON_LABELS['SNC'][locale])
        self.tag_s2s_scalp_mesh_btn.setText(label.BUTTON_LABELS['TSM'][locale])
        self.s2s_curves_btn.setText(label.BUTTON_LABELS['S2S'][locale])
        self.pivot_to_crv_root_btn.setText(label.BUTTON_LABELS['P2R'][locale])
        self.pivot_to_crv_tip_btn.setText(label.BUTTON_LABELS['P2T'][locale])

        self.open_dissect_n_transfer_dialog_btn.setText(label.BUTTON_LABELS['DBT'][locale])

        self.select_every_edge_label.setText(label.BUTTON_LABELS['SEE'][locale])
        self.select_all_label.setText(label.BUTTON_LABELS['SEA'][locale])
        self.aim_scale_manip_to_persp_cam_btn.setText(label.BUTTON_LABELS['SMP'][locale])

        self.save_as_w_file_name_from_selected_btn.setText(label.BUTTON_LABELS['SAN'][locale])
        self.prep_for_animated_cb_thumbnail_btn.setText(label.BUTTON_LABELS['ATP'][locale])
        self.bring_all_to_world_origin_btn.setText(label.BUTTON_LABELS['BTW'][locale])
        self.reset_all_windows_btn.setText(label.BUTTON_LABELS['RAW'][locale])

        self.perform_file_drop_label.setText(label.BUTTON_LABELS['PFD'][locale])

        self.export_separately_fbx_btn.setText(label.BUTTON_LABELS['ESF'][locale])
        self.export_separately_ma_btn.setText(label.BUTTON_LABELS['ESM'][locale])
        self.export_separately_obj_btn.setText(label.BUTTON_LABELS['ESO'][locale])
        self.strip_the_rig_btn.setText(label.BUTTON_LABELS['STR'][locale])

        # self.edit_morphed_UV_btn.setText(label.BUTTON_LABELS['MUV'][locale])
        # self.udim_manual_tiling_btn.setText(label.BUTTON_LABELS['UMT'][locale])
        # self.update_mnt2_module_files_btn.setText(label.BUTTON_LABELS['MNT2'][locale])

        # BUTTON TOOLTIPS
        self.open_kitbash_browser_btn.setToolTip(label.BUTTON_TOOLTIPS['OKB'][locale])
        self.open_env_browser_btn.setToolTip(label.BUTTON_TOOLTIPS['OEN'][locale])
        self.open_costume_browser_btn.setToolTip(label.BUTTON_TOOLTIPS['OCO'][locale])
        self.open_char_browser_btn.setToolTip(label.BUTTON_TOOLTIPS['OCH'][locale])
        self.open_creature_browser_btn.setToolTip(label.BUTTON_TOOLTIPS['OAC'][locale])

        self.open_physx_painter_dialog_btn.setToolTip(label.BUTTON_TOOLTIPS['PHP'][locale])
        self.open_soft_body_collision_dialog_btn.setToolTip(label.BUTTON_TOOLTIPS['SBC'][locale])
        self.croquet_couture_btn.setToolTip(label.BUTTON_TOOLTIPS['FCC'][locale])
        self.replace_mesh_red_gpu_cache_btn.setToolTip(label.BUTTON_TOOLTIPS['RMC'][locale])
        self.restore_mesh_orient1_setup_btn.setToolTip(label.BUTTON_TOOLTIPS['RMO1'][locale])
        self.restore_mesh_orient2_btn.setToolTip(label.BUTTON_TOOLTIPS['RMO2'][locale])

        self.create_convex_hull_one_btn.setToolTip(label.BUTTON_TOOLTIPS['CCH1'][locale])
        self.create_convex_hull_multiple_btn.setToolTip(label.BUTTON_TOOLTIPS['CCH2'][locale])
        self.create_convex_hull_full_btn.setToolTip(label.BUTTON_TOOLTIPS['CCH3'][locale])

        self.combine_curves_btn.setToolTip(label.BUTTON_TOOLTIPS['CNC'][locale])
        self.separate_curves_btn.setToolTip(label.BUTTON_TOOLTIPS['SNC'][locale])
        self.tag_s2s_scalp_mesh_btn.setToolTip(label.BUTTON_TOOLTIPS['TSM'][locale])
        self.s2s_curves_btn.setToolTip(label.BUTTON_TOOLTIPS['S2S'][locale])
        self.pivot_to_crv_root_btn.setToolTip(label.BUTTON_TOOLTIPS['P2R'][locale])
        self.pivot_to_crv_tip_btn.setToolTip(label.BUTTON_TOOLTIPS['P2T'][locale])

        self.open_dissect_n_transfer_dialog_btn.setToolTip(label.BUTTON_TOOLTIPS['DBT'][locale])

        self.export_separately_fbx_btn.setToolTip(label.BUTTON_TOOLTIPS['ESF'][locale])
        self.export_separately_ma_btn.setToolTip(label.BUTTON_TOOLTIPS['ESM'][locale])
        self.strip_the_rig_btn.setToolTip(label.BUTTON_TOOLTIPS['STR'][locale])

        self.bring_all_to_world_origin_btn.setToolTip(label.BUTTON_TOOLTIPS['BTW'][locale])
        self.prep_for_animated_cb_thumbnail_btn.setToolTip(label.BUTTON_TOOLTIPS['ATP'][locale])
        self.save_as_w_file_name_from_selected_btn.setToolTip(label.BUTTON_TOOLTIPS['SAN'][locale])
        self.aim_scale_manip_to_persp_cam_btn.setToolTip(label.BUTTON_TOOLTIPS['SMP'][locale])
        # self.edit_morphed_UV_btn.setToolTip(label.BUTTON_TOOLTIPS['MUV'][locale])
        self.reset_all_windows_btn.setToolTip(label.BUTTON_TOOLTIPS['RAW'][locale])
        # self.udim_manual_tiling_btn.setToolTip(label.BUTTON_TOOLTIPS['UMT'][locale])
        # self.update_mnt2_module_files_btn.setToolTip(label.BUTTON_TOOLTIPS['MNT2'][locale])

        return True

    def open_physx_painter_dialog(self):
        mnT2.PhysXPainterDialog_showUI(mnT2_dialog_passed=self)
        return True

    def open_soft_body_collision_dialog(self):

        mnT2.util.check_n_load_plugin(mnT2.SoftBodyCollisionDialog.DEFORM_PLUGIN)
        mnT2.SoftBodyCollisionDialog_showUI()

        return True

    def open_ultimate_clipboard(self):
        user_path_created = mnT2.util.check_n_set_up_local_folder(cfg.current_username, cfg.repo_exchange_path)
        logger.info("User path is {0}".format(user_path_created))
        mnT2.UltimateClipboardDialog_showUI(user_path_created)

    def export_ma_separately(self):
        output_folder = mnT2.util.check_n_set_up_local_folder(cfg.ma_separately_folder_name,
                                                              mnT2.mnT2_folder_path)
        mnT2.util.export_files_separately(files_separately_output_folder=output_folder,
                                          file_type="mayaAscii", fbx=False)

    def export_fbx_separately(self):
        output_folder = mnT2.util.check_n_set_up_local_folder(cfg.fbx_separately_folder_name,
                                                              mnT2.mnT2_folder_path)
        mnT2.util.export_files_separately(files_separately_output_folder=output_folder, fbx=True)

    def export_obj_separately(self):
        mnT2.util.check_n_load_plugin("objExport")
        output_folder = mnT2.util.check_n_set_up_local_folder(cfg.obj_separately_folder_name,
                                                              mnT2.mnT2_folder_path)
        mnT2.util.export_files_separately(files_separately_output_folder=output_folder,
                                          file_type="OBJexport", fbx=False)

    def export_separately_ass(self):

        if self.separately_ass_del_orig_cb.isChecked():
            mnT2.replace_with_aiStandIn()
        else:
            mnT2.replace_with_aiStandIn(delete_original=False)

    def replace_w_gpu_cache_red(self):
        output_folder = mnT2.util.check_n_set_up_local_folder(cfg.gpu_cache_folder_name,
                                                              mnT2.mnT2_folder_path)
        mnT2.replace_model_w_gpu_cache(output_folder)
        return True

    def replace_w_gpu_cache_green(self):
        output_folder = mnT2.util.check_n_set_up_local_folder(cfg.gpu_cache_folder_name,
                                                              mnT2.mnT2_folder_path)
        mnT2.replace_model_w_gpu_cache(output_folder, blinn_color_enum="green")
        return True

    def replace_w_gpu_cache_blue(self):
        output_folder = mnT2.util.check_n_set_up_local_folder(cfg.gpu_cache_folder_name,
                                                              mnT2.mnT2_folder_path)
        mnT2.replace_model_w_gpu_cache(output_folder, blinn_color_enum="blue")
        return True

    def restore_mesh_orient1_common_setup(self):
        mnT2.RMO1_GUIDE_LOC, mnT2.RMO1_FROZEN_MESH_XFORM, mnT2.RMO1_GUIDE_LOC_BUFFER_SRT = \
            mnT2.restore_mesh_orient1_setup()
        return True

    def restore_mesh_orient1_quick_n_exact(self):
        self.restore_mesh_orient1_common_setup()
        mnT2.restore_mesh_orient1_execute(mnT2.RMO1_GUIDE_LOC, mnT2.RMO1_FROZEN_MESH_XFORM,
                                          mnT2.RMO1_GUIDE_LOC_BUFFER_SRT, move_pivot=True, dirty=True)
        return True

    def tag_scalp_mesh(self):
        mnT2.S2S_SCALP_MESH = mnT2.tag_a_mesh("scalp")
        if mnT2.S2S_SCALP_MESH:
            logger.info("Working on {0} as scalp mesh.".format(mnT2.S2S_SCALP_MESH.nodeName()))
        return True

    def set_ground_mesh(self):
        mnT2.GROUND_MESH = mnT2.tag_a_mesh("ground")
        if mnT2.GROUND_MESH:
            logger.info("Working on {0} as ground mesh.".format(mnT2.GROUND_MESH.nodeName()))
        return True

    def instant_clean(self):
        temp_folder_path = mnT2.util.check_n_set_up_local_folder(mnT2.cfg.temp_folder_name, mnT2.mnT2_folder_path)
        mnT2.instant_obj_clean(temp_folder_path)
        return True

    def choose_separately_ass_output(self):
        scene_folder = mnT2.util.current_scene_folder()

        if scene_folder:
            mnT2.ASS_DIR_PATH = mnT2.util.simple_dir_dialog(dir=scene_folder)
        else:
            mnT2.ASS_DIR_PATH = mnT2.util.simple_dir_dialog()
        logger.info('Outputting .ASS separately to: {0}'.format(mnT2.ASS_DIR_PATH))

        return mnT2.ASS_DIR_PATH

    def choose_replace_aiShaders_resized_img_output(self):
        scene_folder = mnT2.util.current_scene_folder()

        if scene_folder:
            mnT2.AI_SHADERS_RESIZED_OURPUT_DIR = mnT2.util.simple_dir_dialog(dir=scene_folder)
        else:
            mnT2.AI_SHADERS_RESIZED_OURPUT_DIR = mnT2.util.simple_dir_dialog()
        logger.info('Outputting resized images to: {0}'.format(mnT2.AI_SHADERS_RESIZED_OURPUT_DIR))

        return mnT2.AI_SHADERS_RESIZED_OURPUT_DIR

    def auto_name_from_group_enable_padding(self, padding_enabled):
        self.name_from_group_padding_plus_spinbox.setEnabled(padding_enabled)
        self.name_from_group_padding_plus_label.setEnabled(padding_enabled)

    def auto_name_from_group(self):
        mnT2.auto_name_from_group(separator=self.name_from_group_separator_le.text(),
                                  padding=self.name_from_group_padding_cb.isChecked(),
                                  padding_plus=self.name_from_group_padding_plus_spinbox.value())

    def do_replace_all_aiShader(self):
        succeed = mnT2.util.prepare_OIIO()

        if not mnT2.AI_SHADERS_RESIZED_OURPUT_DIR:
            mnT2.replace_all_aiShaders(with_OIIO=succeed)
        else:
            # user specified output path via fileDialog
            mnT2.replace_all_aiShaders(output_path=Path(mnT2.AI_SHADERS_RESIZED_OURPUT_DIR), with_OIIO=succeed)

    def open_gpu_cache_folder(self):

        output_folder = mnT2.util.check_n_set_up_local_folder(cfg.gpu_cache_folder_name,
                                                              mnT2.mnT2_folder_path)
        self.open_file_explorer(output_folder)
        return True

    def open_exported_ma_output_folder(self):
        output_folder = mnT2.util.check_n_set_up_local_folder(cfg.ma_separately_folder_name,
                                                              mnT2.mnT2_folder_path)
        self.open_file_explorer(output_folder)
        return True

    def open_exported_fbx_output_folder(self):
        output_folder = mnT2.util.check_n_set_up_local_folder(cfg.fbx_separately_folder_name,
                                                              mnT2.mnT2_folder_path)
        self.open_file_explorer(output_folder)
        return True

    def open_exported_obj_output_folder(self):
        output_folder = mnT2.util.check_n_set_up_local_folder(cfg.obj_separately_folder_name,
                                                              mnT2.mnT2_folder_path)
        self.open_file_explorer(output_folder)
        return True

    def open_software_local_folder(self):
        output_folder = mnT2.util.check_n_set_up_local_folder(cfg.repo_softwares_folder_name,
                                                              mnT2.mnT2_folder_path)
        self.open_file_explorer(output_folder)
        return True

    def launch_StripTheRigDialog(self):
        sys.path.append(cfg.VSTOOLS2_MAYA_SCRIPT_PATH)
        import stripTheRig_gameSkelPrep as StripTheRig
        StripTheRig.StripTheRigDialog_showUI()

    def launch_croquet_couture(self):
        mnT2.util.add_to_sys_path(cfg.croquet_tools_path)
        import Couture.coutureUI as coutureUI
        reload(coutureUI)
        coutureUI.coutureInterface(dock=True)
        return True

    def launch_wu_super_cut(self):
        mnT2.util.add_to_sys_path(cfg.wu_tools_path)
        import speedCut
        speedCut.jwSpeedCutUI()
        return True

    def launch_vmtb(self):
        pm.evalDeferred('maya.mel.eval("rehash")')
        pm.evalDeferred('maya.mel.eval("source VirtuosMayaTB")')
        pm.evalDeferred('maya.mel.eval("VirtuosMayaTB")', lowestPriority=True)
        return True

    def launch_vsTools1(self):
        if not mnT2.DEV_MODE:
            mnT2.util.source_all_mel_scripts(cfg.vsTools1_mel_server_files_glob_string)
            vsTools1UI.createUI(cfg.vsTools1_ui_server_file_path)
        else:
            mnT2.util.source_all_mel_scripts(cfg.vsTools1_mel_local_files_glob_string)
            vsTools1UI.createUI(cfg.vsTools1_ui_local_file_path)

        return True

    def launch_cgm_toolbox(self):
        mnT2.util.add_to_sys_path(cfg.cgm_tools_path)
        maya.mel.eval("cgmToolbox")

    def launch_hklocaltools(self):
        maya.mel.eval('source "{0}"'.format(os.path.normpath(cfg.korol_local_tools_file_path).replace("\\", "/")))

        pm.evalDeferred('maya.mel.eval("mnT2_HKLocalTools")')
        pm.evalDeferred('maya.mel.eval("mnT2_HKLTOptionBox")', lowestPriority=True)

    def launch_quick_pipe(self):
        maya.mel.eval('source "{0}"'.format(os.path.normpath(cfg.chaumette_qpipe_file_path).replace("\\", "/")))

        pm.mel.evalDeferred("LaunchQuickPipe")
        pm.mel.evalDeferred("QuickPipeUserMenu")
        return True

    def launch_ninja_dojo(self):
        pm.mel.source(cfg.ninjadojo_script_path)
        pm.mel.Ninja_Dojo(cfg.ninjadojo_tools_path)
        return True

    def launch_zen_tools(self):
        mnT2.util.add_to_sys_path(cfg.zen_tools_path)
        import zen
        pm.evalDeferred('maya.mel.eval("zenTools")')
        pm.evalDeferred('maya.mel.eval("layoutZenLoop")', lowestPriority=True)

    def launch_ziniTools(self):
        subprocess.Popen(cfg.znT_batch_file_path)

    def launch_ttStamper(self):
        _PILLOW_PACKAGE = 'python_module/Pillow-6.2.0'
        _SVN_PILLOW_PATH = "C:/vsTools2/library/python_module/Pillow-6.2.0/"
        _TTSTAMPER_BATCH_PATH = "C:/vsTools2/SPD/python/asset/tools/default_external_tools/ttStamper/batch/ttStamper_run.bat"

        if not os.path.exists(_SVN_PILLOW_PATH):
            try:
                import svn.library
                svn.library.addsitedir(_PILLOW_PACKAGE)
            except Exception as error:
                print('(!) Cannot perform "addsitedir" from SVN due to: {}.'.format(error))

        subprocess.Popen(_TTSTAMPER_BATCH_PATH)


    def open_file_explorer(self, folder_path):
        try:
            # os.startfile(folder_path)
            subprocess.Popen(["explorer", os.path.normpath(folder_path)])
        except:
            pass

        return True

    def open_instruction(self, root=cfg.mnT2_instructions_path, topic="", type="ReadMe", ext="pdf", folder=False):
        if not folder:
            file_path = os.path.join(root,
                                     topic,
                                     "{0}.{1}".format("_".join([topic, type]), ext))
            subprocess.Popen(file_path, shell=True)
        else:
            folder_path = os.path.join(root, topic)
            logger.info('Attempting to open folder {0}...'.format(folder_path))
            subprocess.Popen(["explorer", os.path.normpath(folder_path)])
        return True
