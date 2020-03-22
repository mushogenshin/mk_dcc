#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import math
import logging as logger
from functools import partial
import shutil
import subprocess
import time
import copy
import os
import re
from collections import OrderedDict
from distutils.dir_util import copy_tree

import maya.cmds as cmds
import pymel.core as pm
import maya.OpenMaya as om
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

import config as cfg
import util as util

# during dev only
# reload(cfg)
# reload(util)

DEV_MODE = False

mnT2_folder_path = None

# FUNCTION GLOBAL VARIABLES SETUP
DDCONVEXHULL_PLUGIN_LOADED = False
MATERIALPICKER_PLUGIN_LOADED = False
SEAMSEASY_PLUGIN_LOADED = False
BOOLTOOL_PLUGIN_LOADED = False

# global variables for restore_mesh_orient1 function
RMO1_FROZEN_MESH_XFORM = None
RMO1_GUIDE_LOC = None
RMO1_GUIDE_LOC_BUFFER_SRT = None
# global variable for snap_to_scalp function
S2S_SCALP_MESH = None
# global variable for set_pivot_ground function
GROUND_MESH = None
# global variable for separate ASS export destination
ASS_DIR_PATH = None
# global variable for replace aiShaders resized image output destination
AI_SHADERS_RESIZED_OURPUT_DIR = None

# MAYA VARIABLES SETUP
SCENE_ENV = pm.language.Env()
COMPONENT_TYPES = (pm.general.MeshVertex, pm.general.MeshEdge, pm.general.MeshFace)


def initialization():

    global mnT2_folder_path

    # SOURCING ESSENTIAL MEL SCRIPTS
    if not DEV_MODE:
        util.source_all_mel_scripts(cfg.mnT2_mel_essentials_server_files_glob_string)
    else:
        util.source_all_mel_scripts(cfg.mnT2_mel_essentials_local_files_glob_string)
        util.source_all_mel_scripts(cfg.comet_mel_files_glob_string)

    util.add_to_sys_path(cfg.repo_tools_path)

    mnT2_folder_path = util.check_n_set_up_local_folder(cfg.mnT2_folder_name, cfg.user_home_path)
    # textures_folder_path = util.check_n_set_up_local_folder(textures_folder_name, mnT2_folder_path)

    util.install_all(current_only=True, do_presets=True)

    return True

initialization()
# logger.info("Local miniTools2 folder path is {0}".format(mnT2_folder_path))


def maya_main_window():
    """Returns Maya's main window for our GUI to be parented to"""

    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(long(main_window_ptr), QWidget)


def node_name_print(objs):
    """Returns more readable names of the selected objects"""

    return str([obj.nodeName() for obj in objs])


def extend_time_range(range_min=0, range_max=1000, f=0, force=False):
    # checks and sets Min & Max time
    if not force:
        if SCENE_ENV.getMinTime() > range_min:
            SCENE_ENV.setMinTime(range_min)
        if SCENE_ENV.getMaxTime() < range_max:
            SCENE_ENV.setMaxTime(range_max)
    else:
        SCENE_ENV.setMinTime(range_min)
        SCENE_ENV.setMaxTime(range_max)

    # then sets the time
    SCENE_ENV.setTime(f)


def open_content_browser(main_content_path="", landing_subfolder_name=""):
    """

    :param main_content_path: for example: repo_kitbash_path
    :param landing_subfolder_name: for example: repo_kitbash_folder_name
    :return:
    """

    cmds.scriptedPanel('contentBrowserPanel1', edit=True, tearOff=True, label='Content Browser')
    content_browser_panel_name = cmds.getPanel(scriptType='contentBrowserPanel')[0]
    content_browser_panel_complete_name = content_browser_panel_name + 'ContentBrowser'

    if main_content_path not in os.environ['MAYA_CONTENT_PATH'].split(";"):
        cmds.contentBrowser(content_browser_panel_complete_name, edit=True, addContentPath=main_content_path)

    cmds.contentBrowser(content_browser_panel_complete_name, edit=True,
                        location=landing_subfolder_name.replace("_", " "))

    def remove_unneeded_maya_content_path():

        for maya_content_path_to_remove in cfg.MAYA_DEFAULT_CONTENT_PATH:
            if maya_content_path_to_remove in os.environ['MAYA_CONTENT_PATH'].split(";"):
                try:
                    cmds.contentBrowser(content_browser_panel_complete_name, edit=True,
                                        removeContentPath=maya_content_path_to_remove)
                    logger.info("Removed {0} from Maya's default Content Path environment."
                             .format(maya_content_path_to_remove))
                except:
                    pass

        return True

    remove_unneeded_maya_content_path()

    return True


def replace_model_w_gpu_cache(gpu_cache_output_folder, separately=False, name_clue=0,
                              delete_original=True, blinn_color_enum="red"):
    """

    :param separately: bool, this determines whether to export multiple files or not.
    :param name_clue: integer, index of item in the selected object list, which is used to name the output file.
    Default, 0, is the name of the first object. Change this to -1 to take the name of last object.
    :param gpu_cache_output_folder: str, path to a temporary output folder in which to create subfolder corresponding to the user
    :param delete_original: bool
    :param blinn_color_enum: enum name of RGB color
    :return:
    """
    gpu_cache_plugin_name = 'gpuCache'
    util.check_n_load_plugin(gpu_cache_plugin_name)

    # queries the selected geometry and exports them
    selected_objs = pm.ls(sl=True)

    if selected_objs:

        exported_obj_name = selected_objs[name_clue].nodeName().replace(':', '_')
        # uses name of either first or last selected objects

        # checks if a custom blinn shader exists
        blinn_name = 'blinn'
        blinn_color = None

        # converts the enum data to RGB data
        if blinn_color_enum == "red":
            blinn_color = (.2, .039, .039)
        elif blinn_color_enum == "green":
            blinn_color = (.039, .2, .133)
        elif blinn_color_enum == "blue":
            blinn_color = (.039, .098, .2)

        blinn_shader_name = "_".join([cfg.unique_prefix, gpu_cache_plugin_name, blinn_name, blinn_color_enum])

        if pm.ls(blinn_shader_name):
            gpu_cache_shader = pm.PyNode(blinn_shader_name)
            gpu_cache_shading_engine = gpu_cache_shader.listConnections(type='shadingEngine')[0]
        else:
            # creates a corresponding color in RGB space
            gpu_cache_color = pm.datatypes.Color()
            gpu_cache_color.set('RGB', blinn_color[0], blinn_color[1], blinn_color[2])

            # creates a new Blinn shader
            gpu_cache_shader, gpu_cache_shading_engine = pm.createSurfaceShader(blinn_name, name=blinn_shader_name)
            gpu_cache_shader.color.set(gpu_cache_color)

        # assigns the created Blinn shader to all selected objects
        pm.sets(gpu_cache_shading_engine, e=True, fe=selected_objs)

        # exports selected
        pm.mel.gpuCache(selected_objs, fileName=exported_obj_name,
                        directory=gpu_cache_output_folder,
                        startTime=0, endTime=0,
                        optimize=True, optimizationThreshold=40000,
                        writeMaterials=True, dataFormat='ogawa',
                        saveMultipleFiles=separately)
        logger.info('Objects {0} have been exported to {1} with file name "{2}".'.format(node_name_print(selected_objs),
                                                                                      gpu_cache_output_folder,
                                                                                      exported_obj_name))
        # TODO: improves the log string (it currently has 'nt.Transform')

        # now imports the .abc file back in
        gpu_cache_node_name = "_".join([exported_obj_name, gpu_cache_plugin_name])
        gpu_cache_file_path = os.path.join(gpu_cache_output_folder, (exported_obj_name + ".abc"))

        gpu_cache_node = pm.createNode(gpu_cache_plugin_name, n=gpu_cache_node_name)
        logger.info('A "{0}" node named "{1}" has been created.'.format(gpu_cache_plugin_name, gpu_cache_node_name))

        gpu_cache_node.cacheFileName.set(gpu_cache_file_path)
        gpu_cache_node.cacheGeomPath.set("|")
        logger.info('GPU cache at "{0}" has been loaded to node "{1}".'.format(gpu_cache_file_path, gpu_cache_node_name))

        if delete_original:
            pm.delete(selected_objs)
        logger.info('Original objects {0} have been deleted.'.format(str(selected_objs)))

        # renames the transform of the GPU cache node
        gpu_cache_transform = gpu_cache_node.getParent()

        pm.rename(gpu_cache_transform, exported_obj_name)
        pm.select(gpu_cache_transform, r=True)

    else:
        logger.info('No object selected.')

    return True


def restore_mesh_orient2(objs=None, copyPivotTranslation=False, dirtyMode=False,
                         bringToWorld=False, deleteGuide=False):
    zero_grp_suffix = '_zero_grp'
    srt_grp_suffix = '_srt_buffer'

    if not objs:
        # obj(s) with frozen transformations must be selected first, and the guide selected last
        objs = pm.ls(sl=True, type='transform')

    if len(objs) > 1:

        # loads the matrixNodes plugin
        util.check_n_load_plugin(cfg.MATRIX_NODES_PLUGIN_NAME)

        guide = objs[0]

        # first makes sure the guide object have no scale values
        pm.makeIdentity(guide, s=True, apply=True, pn=True)

        logger.info('Using {0} as guide to restore orient of {1}'.format(str(guide), str(objs[1:])))

        # gets the world inverse matrix of the guide
        tmp_guide_decomp_matrix = pm.createNode('decomposeMatrix')

        guide.worldInverseMatrix[0].connect(tmp_guide_decomp_matrix.inputMatrix)
        # logger.info('World inverse matrix of guide {} obtained.'.format(str(guide)))

        for frozen_obj in objs[1:]:
            # first brings it to the world
            pm.parent(frozen_obj, world=True)

            if dirtyMode:
                pm.makeIdentity(frozen_obj, apply=True, pn=True)  # for use in the "quick'n'exact" action

            # assumes the mesh having no rotation
            has_rotation = False
            srt_grp = None

            obj_pos_vector = pm.dt.Vector(pm.xform(frozen_obj, q=True, rp=True))
            obj_rot_vector = pm.dt.Vector(pm.xform(frozen_obj, q=True, ro=True))

            if obj_rot_vector != pm.dt.Vector.zero:
                has_rotation = True
                # creates another SRT group
                srt_grp = pm.group(em=True, n=frozen_obj.nodeName() + srt_grp_suffix)
                srt_grp.translate.set(obj_pos_vector)

            # inverts the rotation of the frozen obj
            frozen_obj.rotate.set(tmp_guide_decomp_matrix.outputRotate.get())
            # freezes transform again to save its new alignment
            pm.makeIdentity(frozen_obj, apply=True, pn=True)

            # transfers the guide's orientation to a zero group
            zero_grp = pm.group(em=True, n=frozen_obj.nodeName() + zero_grp_suffix)
            zero_grp.translate.set(obj_pos_vector)

            guide_rot_vector = pm.dt.Vector(pm.xform(guide, q=True, ws=True, ro=True))
            zero_grp.rotate.set(guide_rot_vector)

            # zeroes the local transforms of the frozen obj
            pm.parent(frozen_obj, zero_grp)
            frozen_obj.rotate.set(pm.dt.Vector.zero)

            if has_rotation:
                logger.info('Object {} had local rotation.'.format(frozen_obj.nodeName()))
                pm.parent(zero_grp, srt_grp)
                # applies the SRT
                srt_grp.rotate.set(obj_rot_vector)

            if bringToWorld:
                pm.parent(frozen_obj, world=True)
                if srt_grp:
                    pm.delete(srt_grp)
                else:
                    pm.delete(zero_grp)

            if copyPivotTranslation:
                guide_translation_vector = pm.dt.Vector(pm.xform(guide, q=True, ws=True, rp=True))
                frozen_obj.setRotatePivot(guide_translation_vector, space='world')
                frozen_obj.setScalePivot(guide_translation_vector, space='world')

            logger.info('__Proper pivot orientation of {} has been restored.\n'.format(frozen_obj.nodeName()))
            pm.select(frozen_obj, r=True)

        pm.delete(tmp_guide_decomp_matrix)

        if deleteGuide:
            logger.info("Deleting {0}...".format(guide))
            pm.delete(guide)

    else:
        logger.info('Please select at least 2 valid objects (Do not select shape nodes).')

    return objs[1:]


def restore_mesh_orient1_setup():
    bbox_factor = 0.75
    selected = pm.selected()
    error = "Please select one polygon face."

    if selected:
        id_face = selected[0]  # queries the face selected by users

        if type(id_face) == pm.general.MeshFace:

            frozen_mesh = id_face.node()  # gets the mesh shape
            frozen_mesh_xform = frozen_mesh.getParent()  # gets the mesh transform

            id_face_normal_vec = id_face.getNormal(space='world')  # gets the selected face's normal
            id_face_normal_vec_rot = pm.dt.Vector(pm.angleBetween(v1=pm.dt.Vector.xAxis, v2=id_face_normal_vec, er=True))

            id_face_center = id_face.__apimfn__().center(om.MSpace.kWorld)  # finds the selected face's center
            id_face_center_point = pm.dt.Point(id_face_center)

            # creates a guide loc and its buffer SRT group
            guide_loc = pm.spaceLocator()
            guide_loc_buffer_srt = pm.group(em=True)
            pm.parent(guide_loc, guide_loc_buffer_srt)

            # moves the guide loc group to the face's center and aligns it to the face's normal
            guide_loc_buffer_srt.translate.set(id_face_center_point)
            guide_loc_buffer_srt.rotate.set(id_face_normal_vec_rot)

            guide_loc.translate.lock()
            # guide_loc.rotateY.lock()
            # guide_loc.rotateZ.lock()

            # makes the guide loc's display size relative to the mesh's bbox
            bbox_height = frozen_mesh.boundingBox().height() * bbox_factor
            guide_loc_scale_vec = pm.dt.Vector(bbox_height, bbox_height, bbox_height)

            guide_loc_shape = guide_loc.getShape()
            guide_loc_shape.localScale.set(guide_loc_scale_vec)
            guide_loc_shape.overrideEnabled.set(True)
            guide_loc_shape.overrideColor.set(13)

            return guide_loc, frozen_mesh_xform, guide_loc_buffer_srt


        else:
            logger.info(error)
            return None, None, None
    else:
        logger.info(error)
        return None, None, None


def restore_mesh_orient1_execute(guide_loc=None, frozen_mesh_xform=None, guide_loc_buffer_srt=None,
                                 move_pivot=False, dirty=False, debug=False):

    # defines enum 3D space coordinate axes
    # box_front_normal = pm.dt.Vector.zAxis  # front face
    # box_back_normal = pm.dt.Vector.zNegAxis  # back face
    # box_right_normal = pm.dt.Vector.xAxis  # right face
    # box_left_normal = pm.dt.Vector.xNegAxis  # left face
    # box_top_normal = pm.dt.Vector.yAxis  # top face
    # box_bottom_normal = pm.dt.Vector.yNegAxis  # bottom face

    # on execution
    guide_loc.translate.unlock()
    # guide_loc.rotateY.unlock()
    # guide_loc.rotateZ.unlock()

    pm.parent(guide_loc, world=True)

    # re-orients the mesh
    try:
        restore_mesh_orient2([guide_loc, frozen_mesh_xform], copyPivotTranslation=move_pivot, dirtyMode=dirty)
    except:
        pass

    if not debug:
        pm.delete(guide_loc, guide_loc_buffer_srt)

    return True


def bring_to_world_origin(nodes=None, reset=True):

    if not nodes:
        nodes = pm.selected()

    if nodes:
        for node in nodes:
            pm.xform(node, centerPivots=True)
            if reset:
                piv_ws_vec = pm.dt.Vector(pm.xform(node, q=True, rp=True, ws=True))
                node.translate.set(piv_ws_vec.__neg__())
                pm.makeIdentity(node, a=True, pn=True)
    else:
        logger.info("Please select at least one object.")

    return True


def pivot_to_bbox(target="minY", centered=False):

    for obj in pm.selected():
        if centered:
            pm.xform(obj, cp=True)
        bbox = pm.xform(obj, q=True, ws=True, bb=True)
        current_rotate_pivot = pm.xform(obj, q=True, ws=True, rp=True)
        # current_scale_pivot = pm.xform(obj, q=True, ws=True, sp=True)

        if target == "minY":
            obj.setRotatePivot(pm.dt.Vector(current_rotate_pivot[0], bbox[1], current_rotate_pivot[2]), space='world')
            obj.setScalePivot(pm.dt.Vector(current_rotate_pivot[0], bbox[1], current_rotate_pivot[2]), space='world')

    return True


def move_to_ground_mesh():

    if GROUND_MESH:
        for obj in pm.selected():
            current_rotate_pivot = pm.xform(obj, q=True, ws=True, rp=True)

            temp_loc = pm.spaceLocator()
            temp_loc.translate.set(current_rotate_pivot)

            pm.geometryConstraint(GROUND_MESH, temp_loc)

            target_pivot = pm.xform(temp_loc, q=True, ws=True, rp=True)

            pm.xform(obj, ws=True, t=(current_rotate_pivot[0], target_pivot[1], current_rotate_pivot[2]))

            pm.delete(temp_loc)

        return True

    else:
        logger.info("Please set the ground mesh first.")
        return False


def prep_for_animated_cb_thumbnail(nodes=None, anim_range=30):

    if not nodes:
        nodes = pm.selected()

    if nodes:
        extend_time_range(0, 30, 0, force=True)
        anim_cb_thumb_name = 'anim_cb_thumb'

        def assign_white_blinn(objs):
            blinn_name = 'blinn'

            # checks if a custom blinn shader exists

            blinn_shader_name = "_".join([cfg.unique_prefix, anim_cb_thumb_name, blinn_name])

            if pm.ls(blinn_shader_name):
                anim_cb_thumb_shader = pm.PyNode(blinn_shader_name)
                anim_cb_thumb_shading_engine = anim_cb_thumb_shader.listConnections(type='shadingEngine')[0]
            else:
                # creates a white color in RGB space
                anim_cb_thumb_color = pm.datatypes.Color()
                anim_cb_thumb_color.set('RGB', 1, 1, 1)

                # creates a new Blinn shader
                anim_cb_thumb_shader, anim_cb_thumb_shading_engine = pm.createSurfaceShader(blinn_name, name=blinn_shader_name)
                anim_cb_thumb_shader.color.set(anim_cb_thumb_color)

            # assigns the white Blinn shader to all selected objects
            pm.sets(anim_cb_thumb_shading_engine, e=True, fe=objs)

            return True

        assign_white_blinn(nodes)

        def add_disp_layer(objs):
            disp_lyr_name = "_".join([anim_cb_thumb_name, "Lyr"])

            if not pm.ls(disp_lyr_name):
                pm.select(objs, r=True)
                disp_lyr = pm.createDisplayLayer(n=disp_lyr_name)
            else:
                disp_lyr = pm.ls(disp_lyr_name)[0]
                disp_lyr.addMembers(objs)

            disp_lyr.displayType.set(2)  # sets to "referenced"

            return True

        add_disp_layer(nodes)

        # at frame 0
        pm.setKeyframe(nodes, at='rotateY', v=0, itt='linear', ott='linear')

        SCENE_ENV.setTime(anim_range)
        pm.setKeyframe(nodes, at='rotateY', v=360, itt='linear', ott='linear')
    else:
        logger.info("Please select at least an object or a group.")

    return True


def save_as_w_file_name_from_selected(node=None, ext="ma"):

    current_scene_path = pm.sceneName()

    if current_scene_path:
        current_folder_path = current_scene_path.dirname()

        if not node:
            node = pm.selected()

        if node:
            node_name = node[0].nodeName().replace(':', '_')
            new_file_name = ".".join([node_name, ext])
            new_file_path = os.path.join(current_folder_path, new_file_name)

            try:
                pm.saveAs(new_file_path)
            except:
                logger.info("Cannot save file as: {0}.".format(new_file_path))
                return False

            logger.info('New file named "{0}" has been created at {1}.'.format(new_file_name, current_folder_path))

            pm.mel.SaveSceneOptions()
            pm.mel.fo_onCapturePlayblastbuttonClick("Save")
        else:
            logger.info("Please select one object.")
    else:
        logger.info("Please save the scene first.")

    return True


def aim_scale_manip_to_persp_cam(cam="persp"):
    error_no_selection = 'Please select some object(s) or component(s).'
    error_scale_mode = 'Please switch to Scale mode'
    components_selection = pm.selected()

    if components_selection:
        persp_cam = pm.PyNode(cam)

        if pm.mel.manipScaleContext("Scale", q=True, vis=True):
            selection_pivot_pos = pm.dt.Vector(pm.mel.manipScaleContext("Scale", q=True, p=True))
            temp_loc = pm.spaceLocator()
            temp_loc.translate.set(selection_pivot_pos)
            pm.aimConstraint(persp_cam, temp_loc, mo=False)  # TODO: improve by using a cam with an aim & an up
            aim_angle = list(temp_loc.rotate.get())
            pm.select(components_selection, r=True)
            pm.mel.manipPivot(o=aim_angle)
            pm.delete(temp_loc)
        else:
            logger.info(error_scale_mode)
    else:
        logger.info(error_no_selection)

    return True


def edit_on_morphed_UV():

    selected_objs = pm.ls(sl=True)

    if selected_objs:
        selected_xform = selected_objs[0]
        given_mesh = selected_xform.getShape()

        if given_mesh and type(given_mesh) == pm.nt.Mesh:
            # gets the height of the bounding box of the mesh
            bbox_height = given_mesh.boundingBox().height()

            # duplicates the mesh
            morphed_uv = pm.duplicate(given_mesh, n="_".join([cfg.unique_prefix, selected_xform.nodeName(), "morphed_UV"]))[0]
            morphed_uv_mesh = morphed_uv.getShape()

            # queries the vertices that have more than one UV
            vert_multi_uv = [vert for vert in morphed_uv_mesh.vtx if vert.numUVs() > 1]
            if vert_multi_uv:
                # splits those vertices
                pm.polySplitVertex(vert_multi_uv)
            # deletes the construction history
            pm.delete(morphed_uv_mesh, ch=True)

            # flattens the mesh
            for vert in morphed_uv_mesh.vtx:
                pos = vert.getUV()
                vert.setPosition((pos[0], pos[1]), space='world')

            # freezes the transform in case the selected object has transform
            pm.makeIdentity(morphed_uv, apply=True, pn=True)
            # resets the transform
            morphed_uv.resetFromRestPosition()
            # scales the flattened mesh to the height of the bounding box
            scale_vec = pm.dt.Vector(bbox_height, bbox_height, bbox_height)
            morphed_uv.scale.set(scale_vec)
            # freezes the transform to clear the scale
            pm.makeIdentity(morphed_uv, apply=True, pn=True)

            # duplicates the "morphed UV" for the blendShape node
            bs_target = pm.duplicate(morphed_uv_mesh, n="_".join([cfg.unique_prefix, selected_xform.nodeName(), 'target']))[0]
            bs_target_mesh = bs_target.getShape()
            # transfers the attributes to morph this "flattened UV, duplicated" back to the original shape
            pm.transferAttributes(given_mesh, bs_target_mesh, pos=True, nml=True, col=0, uvs=0, sampleSpace=3, searchMethod=3)

            # deletes the construction history
            pm.delete(bs_target_mesh, ch=True)

            # creates a blendShape between the morphed UV meshes
            pm.select(bs_target_mesh, morphed_uv_mesh, r=True)
            bs_node = pm.blendShape(origin='world', topologyCheck=0, n="_".join([cfg.unique_prefix,
                                                                                selected_xform.nodeName(), 'blendShape']))

            # deletes the blendShape target
            pm.delete(bs_target)

            # duplicates the "morphed UV" for the wrap node
            wrapped = pm.duplicate(morphed_uv_mesh, n="_".join([cfg.unique_prefix, selected_xform.nodeName(), 'wrapped']))[0]
            wrapped_mesh = wrapped.getShape()

            # creates an attribute on the to-be-wrapped
            pm.addAttr(wrapped, at='double', k=True, ln="morph_UV", min=0.0, max=1.0)
            wrapped.morph_UV.connect(bs_node[0].weight[0])

            # creates a wrap between the "to modify" and the "morphed UV"
            pm.select(wrapped_mesh, morphed_uv_mesh, r=True)
            pm.mel.CreateWrap()

            # organizes all resulted meshes into a group
            organize_grp = pm.group(em=True, n="_".join([cfg.unique_prefix, selected_xform.nodeName(), 'GRP']))

            # moves the "morphed UV" to this group
            pm.parent(morphed_uv, organize_grp)
            pm.hide(morphed_uv)  # and hides it

            # moves the base mesh resulted from the wrap creation to that group as well
            wrap_base_mesh_name = morphed_uv.nodeName() + "Base"
            wrap_base_mesh = pm.PyNode(wrap_base_mesh_name)
            pm.parent(wrap_base_mesh, organize_grp)

            # moves the wrapped mesh to that group
            pm.parent(wrapped, organize_grp)

            # selects the wrapped mesh
            pm.select(wrapped, r=True)
            active_pane = pm.paneLayout('viewPanes', q=True, pane1=1)
            pm.isolateSelect(active_pane, state=1)
            pm.isolateSelect(active_pane, addSelected=True)
        else:
            logger.info("No mesh found. Please select one mesh.")
    else:
        logger.info('No object selected.')

    return True


def combine_nurbs_crvs(crvs=None):

    combined_suffix = "combined"

    if not crvs:
        crvs = [crv for crv in pm.selected() if type(crv.getShape()) == pm.nt.NurbsCurve]

    if len(crvs) >= 2:
        pm.makeIdentity(crvs, apply=True)

        combined_crvs_xform = pm.group(em=True, n="_".join([crvs[0].nodeName(), combined_suffix]))

        for crv in crvs:
            pm.parent(crv.getShape(), combined_crvs_xform, r=True, s=True)
        pm.delete(crvs)
        pm.select(combined_crvs_xform, r=True)
    else:
        logger.info("Please select at least two(2) NURBS curves.")
        return False

    return True


def separate_nurbs_crvs(crvs=None):

    if not crvs:
        crvs = [crv for crv in pm.selected() if len(crv.getShapes()) >= 2]

    if crv:
        for crv in crvs:
            pm.makeIdentity(crv, apply=True)
            all_shapes = crv.getShapes()
            for shape in all_shapes:
                crv_xform = pm.group(em=True, n=shape.nodeName().replace('Shape', ''))
                pm.parent(shape, crv_xform, r=True, s=True)
            pm.delete(crv)
            pm.select(cl=True)
    else:
        logger.info("No compound NURBS curve selected.")

    return True


def tag_a_mesh(mesh_type):

    if len(pm.selected()) == 1 and type(pm.selected()[0].getShape()) == pm.nt.Mesh:
        return pm.selected()[0]
    else:
        logger.info("Please select one (and only one) mesh to use as {0}.".format(mesh_type))
        return False


def s2s_curves(crvs=None):

    s2s_grp_name = "hairSnappedToSurface"

    if not crvs:
        crvs = [crv for crv in pm.selected() if type(crv.getShape()) == pm.nt.NurbsCurve]

    if crvs:

        pm.makeIdentity(crvs, apply=True)

        if S2S_SCALP_MESH:
            # performs snap to surface
            pm.select(S2S_SCALP_MESH, add=True)
            pm.mel.eval('makeCurvesDynamic 2 { "1", "1", "1", "1", "0"};')

            # cleanups the dynamic nodes
            scalp_shape_node = S2S_SCALP_MESH.getShape()
            # finds the follicles
            follicles = scalp_shape_node.listConnections(type='follicle')
            if follicles:
                # finds the hair system
                hair_systems = follicles[0].getShape().listConnections(type='hairSystem', s=True, d=False)
                if hair_systems:
                    # finds the nuclei
                    nuclei = set(hair_systems[0].getShape().listConnections(type='nucleus', s=False))
                    if nuclei:
                        pm.delete(nuclei)
                    # for hair_system in hair_systems:
                    #     hair_sys_shape = hair_system.getShape()
                    #     for input in range(hair_sys_shape.inputHair.numElements()):
                    #         hair_sys_shape.inputHair[input].disconnect()

                # follicles = set(follicles)
                # for follicle in follicles:
                #     follicle_shape = follicle.getShape()
                #     for plug in follicle_shape.listConnections(plugs=True, s=False, d=True):
                #         if plug.name().find('create') != -1:
                #             plug.disconnect()

            s2s_grp = pm.group(em=True, n=s2s_grp_name)

            hair_system_output_crv_grps = pm.ls("hairSystem*OutputCurves")  # TODO: improve with actual name of
            # current hairSystem

            # duplicates the output curves

            for hair_system_output_crv_grp in hair_system_output_crv_grps:
                hair_system_output_crvs = hair_system_output_crv_grp.getChildren()
                output_crvs_duplicated = pm.duplicate(hair_system_output_crvs)
                pm.parent(output_crvs_duplicated, s2s_grp)

            pm.delete(hair_system_output_crv_grps)
            pm.delete(follicles)

            hair_system_follicle_grps = pm.ls("hairSystem*Follicles")
            for hair_system_follicle_grp in hair_system_follicle_grps:
                if not hair_system_follicle_grp.getChildren():
                    pm.delete(hair_system_follicle_grp)

            try:
                pm.delete(hair_systems)
            except:
                pass

            # cleanups the rebuild curve nodes resulted
            # rebuilt_curve_shape_grp = pm.ls("*rebuiltCurveShape")
            # pm.delete(rebuilt_curve_shape_grp)

            for crv in s2s_grp.getChildren():
                crv.getShape().overrideEnabled.set(False)
        else:
            logger.info("Please first tag a scalp mesh.")
            return False

    else:
        logger.info("Please select some NURBS curves.")
        return False

    return True


def pivot_to_curve_cv(crvs=None, last_cv=0):

    if not crvs:
        crvs = [crv for crv in pm.selected() if type(crv.getShape()) == pm.nt.NurbsCurve]

    if crvs:
        for crv in crvs:
            pm.makeIdentity(crv, apply=True)
            crv_shape = crv.getShape()
            if last_cv:
                last_cv = crv_shape.numCVs() - 1
            cv_pos = crv_shape.cv[last_cv].getPosition(space='world')
            crv.rotatePivot.set(cv_pos)
            crv.scalePivot.set(cv_pos)
    else:
        logger.info("Please select at least one NURBS curve.")
        return False

    return True


def create_convex_hull_one():

    global DDCONVEXHULL_PLUGIN_LOADED

    selection_error = "Please select either some components, or one object."

    generated_mesh = None
    hull = None
    selected = pm.selected()

    min_threshold_vertex = 8
    min_threshold_edge = 6
    min_threshold_face = 4

    def sum_component(components):
        sum_count = 0

        for obj in components:
            sum_count += len(obj.indices())

        logger.info("Total number of selected components is {0}.".format(sum_count))

        return sum_count

    if selected:
        if not DDCONVEXHULL_PLUGIN_LOADED:
            DDCONVEXHULL_PLUGIN_LOADED = util.check_n_load_plugin(cfg.DDCONVEXHULL_PLUGIN_NAME)

        import DDConvexHull.DDConvexHullUtils as DDConvexHullUtils

        if type(selected[0]) in COMPONENT_TYPES:
            # component modes
            if type(selected[0]) == COMPONENT_TYPES[0] and sum_component(selected) < min_threshold_vertex:  # MeshVertex
                logger.info("At least {0} vertices must be selected.".format(min_threshold_vertex))
                return False
            elif type(selected[0]) == COMPONENT_TYPES[1] and sum_component(selected) < min_threshold_edge:  # MeshEdge
                logger.info("At least {0} edges must be selected.".format(min_threshold_edge))
                return False
            elif type(selected[0]) == COMPONENT_TYPES[2] and sum_component(selected) < min_threshold_face:  # MeshFace
                logger.info("At least {0} faces must be selected.".format(min_threshold_face))
                return False
            else:
                logger.info("Generating convex hull from selected components...")
                hull, generated_mesh, xform = DDConvexHullUtils.createHull()
        elif len(selected) == 1:
            # object mode
            logger.info("Generating convex hull from selected object...")
            hull, generated_mesh, xform = DDConvexHullUtils.createHull()
        else:
            logger.info(selection_error)

        if generated_mesh:
            logger.info("A mesh named {0} resulted from {1} has been generated.".format(generated_mesh, hull))
            convex_hull_cleanup(generated_mesh)
    else:
        logger.info(selection_error)

    return True


def create_convex_hull_multiple():

    global DDCONVEXHULL_PLUGIN_LOADED

    # filters mesh objects only
    objs = [obj for obj in pm.selected() if type(obj.getShape()) == pm.nt.Mesh]

    if objs:
        if not DDCONVEXHULL_PLUGIN_LOADED:
            DDCONVEXHULL_PLUGIN_LOADED = util.check_n_load_plugin(cfg.DDCONVEXHULL_PLUGIN_NAME)

        import DDConvexHull.DDConvexHullUtils as DDConvexHullUtils

        generated_mesh = None
        hull = None

        for obj in objs:
            pm.select(obj, r=True)
            try:
                hull, generated_mesh, xform = DDConvexHullUtils.createHull()
            except:
                pass

            if generated_mesh:
                logger.info("A mesh named {0} resulted from {1} has been generated.".format(generated_mesh, hull))
                convex_hull_cleanup(generated_mesh)

    return True


def convex_hull_cleanup(mesh):

    # assigns shader
    lambert1_shading_engine = pm.PyNode(INITIALSHADINGGROUP)
    pm.sets(lambert1_shading_engine, e=True, fe=mesh)

    pm.polySetToFaceNormal(mesh)

    # deleteHistory
    pm.delete(mesh, ch=True)

    return True


def select_edge_alternate(round=0, every=2):

    edges = pm.selected(flatten=True)

    if not round:
        edge_alternate = edges[::every]
    else:
        edge_alternate = edges[1::every]

    pm.select(edge_alternate, r=True)


def launch_material_picker():

    global MATERIALPICKER_PLUGIN_LOADED

    if not MATERIALPICKER_PLUGIN_LOADED:
        MATERIALPICKER_PLUGIN_LOADED = util.check_n_load_plugin(cfg.MATERIALPICKER_PLUGIN_NAME)
        util.source_all_mel_scripts(cfg.jirka_material_picker_mel_files_glob_string)

    pm.mel.materialPicker()

    return True


def launch_seams_easy(stitch=False):

    global SEAMSEASY_PLUGIN_LOADED

    if not SEAMSEASY_PLUGIN_LOADED:
        SEAMSEASY_PLUGIN_LOADED = util.check_n_load_plugin(cfg.SEAMSEASY_PLUGIN_NAME)
        util.source_all_mel_scripts(cfg.jirka_seams_easy_mel_files_glob_string)

    if not stitch:
        pm.mel.seamsEasy()
    else:
        pm.mel.stitchEasy()

    pm.mel.AttributeEditor()

    return True


def launch_bool():
    
    global BOOLTOOL_PLUGIN_LOADED

    if not BOOLTOOL_PLUGIN_LOADED:
        BOOLTOOL_PLUGIN_LOADED = util.check_n_load_plugin(cfg.BOOL_PLUGIN_NAME)

    import booltoolUtils
    booltoolUtils.createBoolTool()

    pm.mel.AttributeEditor()


def mirror_ffd_lattices():

    op_name = "mirror"
    custom_lattice_name = "_".join([cfg.unique_prefix, op_name, "lattice"])
    negate_mdl_name = "_".join([cfg.unique_prefix, op_name, "multDoubleLinear"])

    if len(pm.selected()) == 2:

        # queries the lattices from selection
        src_Lattice = pm.selected()[0]
        dst_Lattice = pm.selected()[1]

        # gets the lattice shapes
        src_LatticeShape = src_Lattice.getShape()
        dst_LatticeShape = dst_Lattice.getShape()

        # gets the FFDs
        src_FFD = src_LatticeShape.worldMatrix[0].listConnections()[0]
        dst_FFD = dst_LatticeShape.worldMatrix[0].listConnections()[0]

        # creates a new lattice
        custom_LatticeShape = pm.createNode("lattice", n=custom_lattice_name)
        custom_Lattice = custom_LatticeShape.getParent()

        # connects the destination lattice xform to the custom lattice xform
        dst_Lattice.t.connect(custom_Lattice.t)
        dst_Lattice.r.connect(custom_Lattice.r)
        dst_Lattice.sy.connect(custom_Lattice.sy)
        dst_Lattice.sz.connect(custom_Lattice.sz)

        # negates the Scale X value
        negate_doubleLinear = pm.createNode("multDoubleLinear", n=negate_mdl_name)
        negate_doubleLinear.input2.set(-1)

        dst_Lattice.sx.connect(negate_doubleLinear.input1)
        negate_doubleLinear.output.connect(custom_Lattice.sx)

        # does the same for the lattice base
        dst_LatticeBase = dst_FFD.baseLatticeMatrix.listConnections(d=True)[0]
        negate_doubleLinear.output.connect(dst_LatticeBase.sx)

        # connects the lattice shapes
        src_LatticeShape.latticeOutput.connect(custom_LatticeShape.latticeInput)

        dst_FFD.deformedLatticePoints.disconnect()
        custom_LatticeShape.latticeOutput.connect(dst_FFD.deformedLatticePoints)

        dst_FFD.deformedLatticeMatrix.disconnect()
        custom_LatticeShape.worldMatrix[0].connect(dst_FFD.deformedLatticeMatrix)

        # connects the FFD attrs
        src_FFD.localInfluenceS.connect(dst_FFD.localInfluenceS)
        src_FFD.localInfluenceT.connect(dst_FFD.localInfluenceT)
        src_FFD.localInfluenceU.connect(dst_FFD.localInfluenceU)

        # cleans up the redundant lattice
        pm.delete(dst_Lattice)

        pm.select(src_Lattice, r=True)

    else:
        logger.info("Please select exactly two (2) lattices")
        return False


def mirror_across_object_pivot(axis="X", threshold=0.001):

    pm.selectMode(object=True)
    invert_scale = -1

    if pm.selected():
        # queries the mesh
        obj_xform = pm.selected()[0]
        # obj_shape = obj_xform.getShape()

        # deletes history
        pm.delete(ch=True)

        # queries the name
        obj_orig_name = obj_xform.nodeName()

        # queries the group
        obj_orig_parent = obj_xform.getParent()

        # brings it out to the world
        pm.parent(obj_xform, w=True)

        # matches a locator to it in order to store its original transforms
        pm.select(cl=True)
        loc_orig_xform = pm.spaceLocator(n="_".join([cfg.unique_prefix, obj_orig_name.rpartition(":")[-1], "loc"]))
        pm.matchTransform(loc_orig_xform, obj_xform)

        # duplicates the mesh
        obj_xform_duplicate = pm.duplicate(obj_xform)[0]

        # now flips it depending on the chosen axis
        if axis == "X":
            obj_xform_duplicate.scaleX.set(invert_scale)
        elif axis == "Y":
            obj_xform_duplicate.scaleY.set(invert_scale)
        elif axis == "Z":
            obj_xform_duplicate.scaleZ.set(invert_scale)

        # combines them
        logger.info("Combining the mirrored mesh...")
        obj_combined = pm.polyUnite(obj_xform, obj_xform_duplicate, ch=False,
                                    n="_".join([cfg.unique_prefix, obj_orig_name, "mirrored_combined"]))

        # merges them
        logger.info("Merging the vertices...")
        pm.polyMergeVertex(obj_combined, d=threshold, am=True, ch=False)

        pm.selectMode(object=True)

        # queries back the object after the mergeVertex
        obj_merged = pm.selected()[0]

        pm.xform(obj_merged, cp=True)

        # re-orients the mesh
        try:
            logger.info("Restoring the original transform...")
            restore_mesh_orient2([loc_orig_xform, obj_merged], bringToWorld=True, deleteGuide=True)
        except:
            pass

        # restores the grouping
        if obj_orig_parent:
            logger.info("Restoring the original grouping...")
            pm.parent(obj_merged, obj_orig_parent)

        # restores the name
        logger.info("Restoring the original name...")
        pm.rename(obj_merged, obj_orig_name)

    return True


def get_distorted_quad(threshold=15.0):

    def average(a):
        return sum(a) / len(a)

    mesh = pm.selected()[0].getShape()
    mesh_name = mesh.nodeName()

    # queries non-planar faces
    pm.mel.eval(
        'polyCleanupArgList 4 { "0","2","0","0","0","0","0","1","0","1e-05","0","1e-05","0","1e-05","0","-1","0","0" };')

    # working on all the non-planar faces found now
    non_planar_faces = pm.selected()

    distorted_faces = []

    for face_series in non_planar_faces:
        for face_id in face_series.indices():
            face = pm.PyNode(mesh_name + ".f[{}]".format(face_id))

            face_normal = face.getNormal()
            edge_list = face.getEdges()

            dot_list = []

            for edge_id in edge_list:
                edge = pm.PyNode(mesh_name + ".e[{}]".format(edge_id))
                edge_vec = edge.getPoint(0, space='world') - edge.getPoint(1, space='world')
                edge_vec.normalize()

                dot_prod = face_normal.dot(edge_vec)
                angle_dif = math.fabs(90 - math.degrees(math.acos(dot_prod)))
                dot_list.append(angle_dif)

            epsilon = average(dot_list)

            if epsilon > threshold:
                distorted_faces.append(face)
                logger.info("Found face [{0}] of epsilon {1}.".format(face_id, epsilon))

    if distorted_faces:
        pm.select(distorted_faces, r=True)
    else:
        pm.selectMode(object=True)
        pm.select(clear=True)
        logger.info("Found no distorted face beyond threshold of {0}".format(threshold))

    return distorted_faces


def get_udim_list(name, udimList):
    selList = om.MSelectionList()
    selList.add(name)
    selListIter = om.MItSelectionList(selList, om.MFn.kMesh)
    pathToShape = om.MDagPath()
    selListIter.getDagPath(pathToShape)
    meshNode = pathToShape.fullPathName()
    uvSets = cmds.polyUVSet(meshNode, query=True, allUVSets=True)
    allSets = []

    for uvset in uvSets:
        shapeFn = om.MFnMesh(pathToShape)
        shells = om.MScriptUtil()
        shells.createFromInt(0)
        # shellsPtr = shells.asUintPtr()
        nbUvShells = shells.asUintPtr()

        uArray = om.MFloatArray()  # array for U coords
        vArray = om.MFloatArray()  # array for V coords
        uvShellIds = om.MIntArray()  # The container for the uv shell Ids

        shapeFn.getUVs(uArray, vArray)
        shapeFn.getUvShellsIds(uvShellIds, nbUvShells, uvset)

        # shellCount = shells.getUint(shellsPtr)

        # udimList = {}
        for i, n in enumerate(uvShellIds):
            # Round up uv
            uCoord = int(uArray[i]) + 1

            vCoord = int(vArray[i])

            # Udim adress
            udimAdress = str(1000 + vCoord * 10 + uCoord)
            #
            if udimAdress in udimList:
                udimList[udimAdress].append('{0}.map[{1}]'.format(name, i))
            else:
                udimList[udimAdress] = ['{0}.map[{1}]'.format(name, i)]

        allSets.append({uvset: udimList})

    return udimList


def bulk_udim_flip(direction=0):

    objs = cmds.ls(sl=True)
    center = 0.5

    if objs:

        # resets udimList
        uList = {}

        for obj in objs:
            uList = get_udim_list(obj, uList)

        for udimCoord in uList.keys():

            uv_pivot = util.udim_coord_to_u_v(int(udimCoord))

            # selects the UV shell
            cmds.select(uList[udimCoord])

            # gets contained face
            # faces = cmds.polyListComponentConversion(fuv=True, toFace=True)
            # cmds.select(faces)

            # flips it
            # direction: 0==U, 1==V
            try:
                cmds.polyFlipUV(flipType=direction, local=True, usePivot=True,
                                pivotU=uv_pivot[0] + center, pivotV=uv_pivot[1] + center)
            except Exception as error:
                logger.info("(!) Cannot perform polyFlipUV due to: {0}".format(error))
            else:
                logger.info("***polyFlipUV done for UDIM {0}".format(udimCoord))

        # cmds.select(objs=True, r=True)
        # cmds.selectMode(object=True)
        cmds.select(cl=True)

        return True

    else:
        logger.info("Nothing selected. Aborted.")
        return False


def create_multi_udim_shaders(unique_prefix=""):

    # shapesList = pm.ls(type="mesh")
    # transformList = pm.listRelatives(shapesList, parent=True)
    #
    # pm.select(transformList)

    objs = cmds.ls(sl=True)

    # resets udimList
    uList = {}

    for obj in objs:
        uList = get_udim_list(obj, uList)

    for udimCoord in uList.keys():

        # logger.info(udimCoord)

        # creates shader
        if unique_prefix:
            newShad = cmds.shadingNode('blinn', n='{0}_Mat{1}'.format(unique_prefix, udimCoord), asShader=True)
        else:
            newShad = cmds.shadingNode('blinn', n='Mat{0}'.format(udimCoord), asShader=True)

        # # creates texture file
        # file_node = cmds.shadingNode("file", asTexture=True)
        # # sets file path
        # texturePath = textures_folder_path + 'diffColor.%s.tif' % udimCoord
        # # sets texture atribute
        # cmds.setAttr('%s.fileTextureName' % file_node, texturePath, type="string")
        # # connects attribute
        # cmds.connectAttr('%s.outColor' % file_node, '%s.color' % newShad)

        # selects the UV shell
        cmds.select(uList[udimCoord])
        # gets contained face
        faces = cmds.polyListComponentConversion(fuv=True, toFace=True)
        # assigns shader
        cmds.select(faces)
        cmds.hyperShade(assign=newShad)

    cmds.select(cl=True)


def collapse_all_udims():

    cmds.undoInfo(openChunk=True)

    pm.select(hi=True)
    xforms = util.filter_transforms()

    pm.select(xforms, r=True)
    meshes = util.filter_polygonal_meshes()

    if meshes:

        for mesh in meshes:
            # working with cmds now
            mesh_name = mesh.name(long=True)
            # logger.info("Working on mesh {0}...".format(mesh_name))

            uv_shells = util.get_uv_shells(mesh_name)
            if uv_shells:
                for shell in uv_shells:
                    # queries where the shell lies
                    shell_u_pos, shell_v_pos = cmds.polyEditUV(shell[0], q=True)  # just picks the first uv point

                    shell_u_pos_diff = math.floor(shell_u_pos)
                    shell_v_pos_diff = math.floor(shell_v_pos)

                    cmds.select(shell, r=True)

                    if shell_u_pos_diff:
                        cmds.polyEditUV(u=-shell_u_pos_diff)
                    if shell_v_pos_diff:
                        cmds.polyEditUV(v=-shell_v_pos_diff)
        pm.select(meshes, r=True)

    else:
        cmds.undoInfo(closeChunk=True)
        return False

    cmds.undoInfo(closeChunk=True)
    return True


def set_osdFvarBoundary(value=1):

    pm.select(hi=True)
    xforms = util.filter_transforms()

    pm.select(xforms, r=True)
    meshes = util.filter_polygonal_meshes()

    if meshes:
        for mesh in meshes:
            mesh.osdFvarBoundary.set(value)
    else:
        logger.info("Found no polygonal mesh. Aborted.")
        return False


def instant_obj_clean(destination):

    file_type = "OBJexport"

    pm.select(hi=True)
    xforms = util.filter_transforms()

    pm.select(xforms, r=True)
    meshes = util.filter_polygonal_meshes()

    if meshes:

        util.check_n_load_plugin(cfg.OBJ_EXPORT_PLUGIN_NAME)

        for mesh in meshes:
            mesh_xform = mesh.getParent()
            mesh_name = mesh_xform.name().replace(":", "_")

            exported_file_path = os.path.join(destination, mesh_name)
            import_file_path = os.path.join(destination, "{0}.{1}".format(mesh_name, cfg.FILE_EXT[file_type]))

            # exports the mesh
            pm.select(mesh_xform, r=True)
            cmds.file(exported_file_path, options="groups=0;ptgroups=0;materials=0;smoothing=0;normals=0",
                      type=file_type, exportSelected=True, preserveReferences=True)
            logger.info("Exported {0} to {1}".format(mesh_name, import_file_path))

            # deletes the original mesh
            pm.delete(mesh_xform)
            logger.info("Deleted original mesh {0}".format(mesh_name))

            # imports the exported mesh
            try:
                cleaned_mesh = pm.importFile(import_file_path, defaultNamespace=True,
                                             preserveReferences=True, returnNewNodes=True)
                logger.info("Imported {0} as {1}".format(import_file_path, cleaned_mesh))
                # returns a list containing a transform and a mesh
                pm.rename(cleaned_mesh[0], mesh_name)
                logger.info("Restoring original name...")
            except Exception as error:
                logger.info("Cannot import mesh {0} due to: {1}.".format(import_file_path, error))
                continue

            # deletes the file
            try:
                os.remove(import_file_path)
                logger.info("Deleted file {0}".format(import_file_path))
            except Exception as error:
                logger.info("Cannot remove file {0} due to: {1}.".format(import_file_path, error))
                continue

        return True

    else:
        logger.info("Found no polygonal mesh. Aborted.")
        return False


def replace_with_aiStandIn(delete_original=True):

    if ASS_DIR_PATH:

        ass_typ = "ASS Export"
        AISTANDIN = "aiStandIn"

        util.check_n_load_plugin(cfg.ARNOLD_PLUGIN_NAME)
        import mtoa.ui.arnoldmenu as arnoldMenu

        sel = pm.ls(sl=1)

        for obj in sel:
            obj_name = obj.name().replace(":", "_")

            output_path = os.path.normpath(os.path.join(ASS_DIR_PATH,
                                                        ".".join([obj_name, cfg.FILE_EXT[ass_typ]])))

            # exports each as an ASS file
            pm.select(obj, r=True)

            # file -force -options "-shadowLinks 1;-mask 6399;-lightLinks 1;-boundingBox" -typ "ASS Export" -pr -es
            # "someName.ass";

            cmds.file(output_path, force=True, typ=ass_typ, pr=True, es=True, options="-boundingBox")

            # pm.mel.arnoldExportAss(output_path, selected=True, boundingBox=True)

            # creates each a new aiStandIn
            new_aiStandIn = pm.PyNode(arnoldMenu.createStandIn())
            # and loads ASS file to Path attr
            new_aiStandIn.dso.set(output_path)
            new_aiStandIn.getParent().rename('_'.join([obj_name, AISTANDIN]))

        if delete_original:
            pm.delete(sel)

    else:
        logger.info("No output folder specified. Aborted.")
        return False


def force_restore_HUD():

    HUDs = ["HUDPolyCountVerts", "HUDPolyCountEdges", "HUDPolyCountFaces", "HUDPolyCountTriangles", "HUDPolyCountUVs"]

    force_restore_HUD_command = '''
    
    menuItem -e -cb 1 polyCountItem;
    optionVar -iv "polyCountVisibility" 1;

    headsUpDisplay -s 0
    	-b 0
    	-vis (`optionVar -q polyCountVisibility`)
    	-label (uiRes("m_initHUD.kHUDTitleVerts"))
    	-lw 50
    	-dw 65
    	-da "right"
    	-pre "polyVerts"
    	HUDPolyCountVerts;

    headsUpDisplay -s 0
    	-b 1
    	-vis (`optionVar -q polyCountVisibility`)
    	 -label (uiRes("m_initHUD.kHUDTitleEdges"))
    	-lw 50
    	-dw 65
    	-da "right"
    	-pre "polyEdges"
    	HUDPolyCountEdges;

    headsUpDisplay -s 0
    	-b 2
    	-vis (`optionVar -q polyCountVisibility`)
    	-label (uiRes("m_initHUD.kHUDTitleFaces"))
    	-lw 50
    	-dw 65
    	-da "right"
    	-pre "polyFaces"
    	HUDPolyCountFaces;

    headsUpDisplay -s 0
    	-b 3
    	-vis (`optionVar -q polyCountVisibility`)
    	 -label (uiRes("m_initHUD.kHUDTitleTris"))
    	-lw 50
    	-dw 65
    	-da "right"
    	-pre "polyTriangles"
    	HUDPolyCountTriangles;

    headsUpDisplay -s 0
    	-b 4
    	-vis (`optionVar -q polyCountVisibility`)
    	 -label (uiRes("m_initHUD.kHUDTitleUVs"))
    	-lw 50
    	-dw 65
    	-da "right"
    	-pre "polyUVs"
    	HUDPolyCountUVs;
    '''

    for HUD in HUDs:
        if pm.headsUpDisplay(HUD, q=True, ex=True):
            pm.headsUpDisplay(HUD, rem=True)
            logger.info("Deleted {0}...".format(HUD))


    pm.mel.eval(force_restore_HUD_command)

    return True


def reset_all_windows():
    open_windows = cmds.lsUI(windows=True)

    for open_window in open_windows:
        if open_window != "MayaWindow":
            cmds.deleteUI(open_window)
            cmds.windowPref(open_window, remove=True)
            print("***Window: {0} deleted and reset.".format(open_window))

    return True


def download_software(exe_key):

    exe_folder_server_path = os.path.join(cfg.repo_softwares_path, cfg.SOFTWARES[exe_key][0])

    mnT2_software_folder_local_path = util.check_n_set_up_local_folder(cfg.repo_softwares_folder_name, mnT2_folder_path)

    exe_folder_local_path = os.path.join(mnT2_software_folder_local_path, cfg.SOFTWARES[exe_key][0])

    exe_file_local_path = os.path.join(mnT2_software_folder_local_path,
                                       cfg.SOFTWARES[exe_key][0],
                                       cfg.SOFTWARES[exe_key][1])

    if not os.path.exists(exe_file_local_path):
        logger.info('Downloading app "{0}" to {1}.'.format(cfg.SOFTWARES[exe_key][1], exe_folder_local_path))
        copy_tree(exe_folder_server_path, exe_folder_local_path)
    else:
        logger.info('Found app "{0}" in {1}.'.format(cfg.SOFTWARES[exe_key][1], exe_folder_local_path))

    logger.info('Attempting to launch app "{0}"...'.format(cfg.SOFTWARES[exe_key][1]))
    subprocess.Popen(exe_file_local_path, shell=True)

    return True


def track_user():
    pass


def auto_name_from_group(separator, padding, padding_plus):

    # user select a group
    if pm.selected():

        logger.info("Separator is: {0}; Zero padding: {1}; Padding plus: {2}.\n".format(separator, padding, padding_plus))

        pm.select(hi=True)
        mesh_selected = pm.selected(type="mesh")

        groups = []

        for mesh in mesh_selected:
            xform = mesh.getParent()

            group = xform.getParent()
            if group:
                groups.append(group)

        groups = set(groups)

        for group in groups:
            group_name = group.name()
            xforms = group.getChildren(shapes=False)

            group_len = len(xforms)
            pad_amount = int(math.floor(math.log10(group_len) + 1)) + padding_plus

            print('Number of mesh within group "{0}": {1}. Padding = {2}.\n'.format(group_name, group_len, pad_amount))

            for i, xform in enumerate(xforms, start=1):
                if padding:
                    new_name = separator.join([group_name, str(i).zfill(pad_amount)])
                else:
                    new_name = separator.join([group_name, str(i)])

                pm.rename(xform, new_name)
    else:
        print("Please select a group.")


def download_vmtb_to_maya_app_dir():

    # queries the MAYA_APP_DIR
    current_maya_app_dir = os.environ['MAYA_APP_DIR']  # C:/Users/%USERNAME%/Documents/maya.ABC

    # opens destination location
    subprocess.Popen(["explorer", os.path.normpath(current_maya_app_dir)])

    vmtb_folders = ["2016", "2017", "plug-ins", "prefs", "scripts"]

    for folder in vmtb_folders:
        src_folder = os.path.normpath(os.path.join(cfg.vmtb_tools_path, folder))
        dst_folder = os.path.normpath(os.path.join(current_maya_app_dir, folder))
        copy_tree(src_folder, dst_folder)

    return True


def download_vmtb_old(wait_time=3):

    # copies the virtuos folder from server to local
    vmtb_local_tools_path = os.path.join(mnT2_folder_path, cfg.vmtb_folder_name)

    if os.path.exists(vmtb_local_tools_path):
        try:
            shutil.rmtree(vmtb_local_tools_path)
        except:
            logger.info('Cannot delete.')
            pass

    try:
        shutil.copytree(cfg.vmtb_tools_path, vmtb_local_tools_path)
    except:
        logger.info('Cannot copy.')
        pass

    # opens location of the .bat file
    time.sleep(wait_time)
    try:
        subprocess.Popen(["explorer", os.path.normpath(vmtb_local_tools_path)])
    except:
        logger.info('Cannot open.')
        pass

    return True


def perform_file_drop_do_one(destination_path):

    try:
        shutil.copy2(cfg.perform_file_drop_script_source_path, destination_path)
    except:
        pass

    return True


def perform_file_drop_do_all():

    for maya_version in cfg.MAYA_VERSIONS:
        user_maya_path = os.path.join(cfg.user_maya_app_dir, maya_version, cfg.script_folder_name)
        if os.path.exists(user_maya_path):
            perform_file_drop_do_one(user_maya_path)

    return True


def perform_file_drop_remove_one(destination_path):

    perform_file_drop_script_current_path = os.path.join(destination_path, cfg.perform_file_drop_script_name)

    if os.path.exists(perform_file_drop_script_current_path):
        os.remove(perform_file_drop_script_current_path)

    return True


def perform_file_drop_remove_all():

    for maya_version in cfg.MAYA_VERSIONS:
        user_maya_path = os.path.join(cfg.user_maya_app_dir, maya_version, cfg.script_folder_name)
        if os.path.exists(user_maya_path):
            perform_file_drop_remove_one(user_maya_path)

    return True


def update_modules(module_name=cfg.mnT2_folder_name, source_dir=cfg.mnT2_source_modules_folder_path):

    module_ext = "mod"
    module_file = ".".join([module_name, module_ext])

    source_module_file_path = os.path.join(source_dir, module_file)

    logger.info("Attempting to update all {0} .{1} files.".format(cfg.mnT2_folder_name, module_ext))

    for target_module_folder_path in os.environ["MAYA_MODULE_PATH"].split(";"):
        if os.path.exists(os.path.join(target_module_folder_path, module_file)):
            try:
                shutil.copy2(source_module_file_path, target_module_folder_path)
                logger.info('Module "{0}" at {1} has been updated to the latest version.'
                         .format(module_name, target_module_folder_path))
            except:
                pass

    return True


def quick_maya_to_zbrush():

    if cmds.ls(sl=True):
        temp_meshes = pm.duplicate()

        # freezes transforms
        pm.select(temp_meshes, r=True)
        cmds.makeIdentity(apply=True, preserveNormals=True)

        # deletes all UV sets except the first one
        for mesh in temp_meshes:
            all_uv_sets = pm.polyUVSet(mesh, q=True, auv=True)
            for uv_set in all_uv_sets[1:]:
                pm.polyUVSet(mesh, uvSet=uv_set, delete=True)
                logger.info('Deleted UV set "{0}" on object "{1}"'.format(uv_set, mesh))

        cmds.file(cfg.QUICK_MA_TO_ZB_FILE, exportSelected=True, type="mayaAscii", force=True)
        logger.info("Exported the mesh(es) to {0}".format(cfg.QUICK_MA_TO_ZB_FILE))

        pm.delete(temp_meshes)
        pm.selectMode(object=True)

    cmds.select(cl=True)  # doesn't work :(
    try:
        cmds.setToolTo("selectSuperContext")
    except:
        pass

    return True


def quick_zbrush_to_maya():

    util.check_n_load_plugin(cfg.FBX_PLUGIN_NAME)

    if os.path.exists(cfg.QUICK_ZB_TO_MA_FILE):
        zzz_mesh = pm.importFile(cfg.QUICK_ZB_TO_MA_FILE, defaultNamespace=True, returnNewNodes=True)
    else:
        logger.info('File "{0}" doesn\'t exist.'.format(cfg.QUICK_ZB_TO_MA_FILE))
        return False

    # print(zzz_mesh)

    return True


def replace_all_aiShaders(output_path=None, with_OIIO=True, optimize_scene=True):
    _AI_SHADER = 'aiStandardSurface'
    _SHADING_ENGINE = 'shadingEngine'
    _SUB_SHADER = 'lambert'
    _SUB_SHADER_PREFIX = 'proxy'
    _VAR_CHAR = '$'
    _UDIM_TILING_MODE = 3
    _EXTENSION = '.png'

    # queries current data for later use
    shader_assignments = {}

    all_other_udims = []

    for ai_shader in pm.ls(type=_AI_SHADER):
        ai_se = ai_shader.listConnections(type=_SHADING_ENGINE)[0]
        shader_assignments[ai_shader] = cmds.sets(ai_se.name(), q=True)

    # substitutes each aiShader with a lambert
    for ai_shader, assigned_objs in shader_assignments.items():

        # creates a substitute shader and names it accordingly
        sub_shader, sub_engine = pm.createSurfaceShader(_SUB_SHADER, name='_'.join([_SUB_SHADER_PREFIX,
                                                                                    ai_shader.name()]))

        # queries the file connection at the Base Color channel
        base_color_file_plug = ai_shader.baseColor.listConnections(p=True)

        # connects the file to the lambert
        if base_color_file_plug:
            out_color_attr = base_color_file_plug[0]

            out_color_attr.connect(sub_shader.color)

            # queries the file node
            file_node = out_color_attr.node()

            file_texture_path = os.path.normpath(file_node.fileTextureName.get())
            # $REV_ASSET\prop\Shell\last\medRes\textures\Shell_1001_clr.tif

            file_texture_path = Path(os.path.expandvars(file_texture_path))
            logger.info('Full texture path: {}'.format(file_texture_path))

            if file_texture_path.as_posix().find(_VAR_CHAR) != -1:
                logger.warning('(!) Cannot expand variable(s) in path.')

            if file_node.uvTilingMode.get() == _UDIM_TILING_MODE:  # UDIM mode
                all_other_udims.extend(util.find_all_UDIM_textures(file_texture_path))

            if with_OIIO:
                # resize images and replaces the path
                succeed, resized_img_path = util.oiio_resize_image(file_texture_path,
                                                                   output_folder=output_path, extension=_EXTENSION)
                if succeed:
                    logger.info('<<< Entering OIIO land >>>')
                    file_node.fileTextureName.set(resized_img_path.as_posix())

        # assigns to the corresponding objects/polygons
        pm.sets(sub_engine, fe=assigned_objs)

        # now removes the aiShader
        pm.delete(ai_shader)

    if optimize_scene:
        # cleans up unused shader nodes
        pm.mel.source('cleanUpScene')
        pm.mel.scOpt_performOneCleanup({'shaderOption', 'shadingNetworksOption'})

    # now processes all other UDIMs
    if with_OIIO:
        all_other_udims = set(all_other_udims)  # just to be sure

        logger.info('<<< Entering OIIO land >>>')

        for other_udim in all_other_udims:
            util.oiio_resize_image(other_udim, output_folder=output_path, extension=_EXTENSION)


def remove_plugin_autoload(plugins):

    for plugin in plugins:
        try:
            cmds.pluginInfo(plugin, e=True, autoload=False)
        except Exception as e:
            logger.info('{}: Plugin {} is not registered.'.format(e, plugin))
        else:
            logger.info('Success. Plugin {} will not Auto Load next time.'.format(plugin))


class PhysXPainterDialog(QDialog):
    """This is the class of our tool dialog"""

    # BUTTON_LABELS = {'load_Clouds': {'EN': 'Paint meshes', 'VI': u'Mây'},
    #                  'load_Scatters': {'EN': 'Obj to scatters', 'VI': u'Mưa'},
    #                  'load_Grounds': {'EN': 'Ground & colliders', 'VI': u'Đất'},
    #                  4: {'EN': '', 'VI': u''}}

    ORIENT_NUCLEUS_NAME = "orient_nucleus"
    BAKED_MESH_IDENTIFIER = "ReproMesh"

    def __init__(self, parent=maya_main_window(), mnT2_dialog=None):
        super(PhysXPainterDialog, self).__init__(parent)

        self.setWindowTitle('PhysX Painter')
        # self.setMinimumWidth(200)
        # disables the question mark button in Windows
        self.setWindowFlags(self.windowFlags() ^ Qt.WindowContextHelpButtonHint)

        self.Clouds = None
        self.Scatters = None
        self.Grounds = None

        self.Scattered_Grp = None

        self.NUM_VERTS_N_SCATTER_NAMES = {}

        self.php_mash_network = None
        self.php_mash_placer = None
        self.php_mash_bullet = None

        self.create_widgets()
        self.create_layouts()
        self.create_connections()

        # if mnT2_dialog.locale_toggle_cb.isChecked():
        #     logger.info("LOCALE IS EN!")
        # else:
        #     logger.info("LOCALE IS VI!")

    def create_widgets(self):
        """Creates the Qt widgets"""
        
        self.main_dialog_tabs = QTabWidget()
        self.A_tab = QWidget()
        self.B_tab = QWidget()

        load_btns_label = ">>"
        load_btns_styleSheet = "padding: 2px"

        setup_btn_styleSheet = "color: black; background-color: rgb(104, 161, 150)"

        execute_btn_styleSheet = "Text-align: left; padding: 1px"

        self.clouds_le = QLineEdit()
        self.scatters_le = QLineEdit()
        self.grounds_le = QLineEdit()

        self.load_clouds_btn = QPushButton(load_btns_label)
        self.load_scatters_btn = QPushButton(load_btns_label)
        self.load_grounds_btn = QPushButton(load_btns_label)

        self.add_orient_nucleus_cb = QCheckBox('Inject "orient nuclei"')

        self.setup_btn = QPushButton("*** Setup ***")
        self.setup_btn.setStyleSheet(setup_btn_styleSheet)

        self.play_pause_btn = QPushButton()
        self.play_pause_btn.setIcon(QIcon(":play_S.png"))
        self.play_pause_btn.setStyleSheet("padding: 2px; background-color: rgb(165, 102, 111)")

        self.reset_btn = QPushButton("zero")
        self.reset_btn.setIcon(QIcon(":out_time.png"))  # out_timeEditor
        self.reset_btn.setStyleSheet(execute_btn_styleSheet)

        self.select_paint_node_btn = QPushButton("Paint node")
        self.select_paint_node_btn.setStyleSheet("Text-align: left")
        self.select_paint_node_btn.setIcon(QIcon(":paintVertexColour.png"))  # paintSetMembership
        # art3dPaint, selectPaint, makePaintable, artPaintSelect, toonPaintWidth, paintJiggle

        self.delete_setup_btn = QPushButton("Del all")
        self.delete_setup_btn.setIcon(QIcon(":deleteGeneric.png"))
        self.delete_setup_btn.setStyleSheet("Text-align: left; padding: 1px; background-color: rgb(165, 102, 111)")

        self.bake_current_btn = QPushButton("Bake current")

        # TAB A: SET INIT
        self.add_orient_nucleus_cb.setChecked(True)

        # STYLESHEETS & TOOLTIPS

        self.load_clouds_btn.setStyleSheet(load_btns_styleSheet)
        self.load_scatters_btn.setStyleSheet(load_btns_styleSheet)
        self.load_grounds_btn.setStyleSheet(load_btns_styleSheet)

        self.load_clouds_btn.setToolTip("Load selected as Cloud")
        self.load_scatters_btn.setToolTip("Load selected as objs to scatter")
        self.load_grounds_btn.setToolTip("Load selected as Ground")

        # TAB B WIDGETS

        self.edit_paint_meshes_grp_box = QGroupBox("Edit Clouds")
        self.edit_scattered_grp_box = QGroupBox("Edit Scattered")
        self.edit_colliders_grp_box = QGroupBox("Edit Grounds")

        self.add_as_paint_mesh_btn = QPushButton("Add")
        self.remove_as_paint_mesh_btn = QPushButton("Remove")

        self.restore_scattered_xforms_btn = QPushButton("Restore Scattered's Transforms")

        self.add_as_collider_btn = QPushButton("Add")
        self.remove_as_collider_btn = QPushButton("Remove")

    def create_layouts(self):
        """Creates the Qt layouts"""

        F_spacing = 3
        VB_margin = 2
        VB_spacing = 3

        # TAB A LAYOUT

        A_main_layout = QVBoxLayout()
        A_main_layout.setContentsMargins(VB_margin, VB_margin, VB_margin, VB_margin)
        A_main_layout.setSpacing(VB_spacing)

        load_clouds_row_lo = QHBoxLayout()
        load_clouds_row_lo.addWidget(self.clouds_le)
        load_clouds_row_lo.addWidget(self.load_clouds_btn)

        load_scatters_row_lo = QHBoxLayout()
        load_scatters_row_lo.addWidget(self.scatters_le)
        load_scatters_row_lo.addWidget(self.load_scatters_btn)

        load_grounds_row_lo = QHBoxLayout()
        load_grounds_row_lo.addWidget(self.grounds_le)
        load_grounds_row_lo.addWidget(self.load_grounds_btn)

        common_load_form_lo = QFormLayout()
        common_load_form_lo.setSpacing(F_spacing)
        common_load_form_lo.addRow('Clouds:', load_clouds_row_lo)
        common_load_form_lo.addRow('Scatters:', load_scatters_row_lo)
        common_load_form_lo.addRow('Grounds:', load_grounds_row_lo)
        common_load_form_lo.addRow("", self.add_orient_nucleus_cb)

        play_row_lo = QHBoxLayout()
        play_row_lo.addWidget(self.reset_btn)
        play_row_lo.addStretch()
        play_row_lo.addWidget(self.select_paint_node_btn)
        play_row_lo.addWidget(self.play_pause_btn)

        bake_row_lo = QHBoxLayout()
        bake_row_lo.addWidget(self.delete_setup_btn)
        bake_row_lo.addStretch()
        bake_row_lo.addWidget(self.bake_current_btn)

        A_main_layout.addLayout(common_load_form_lo)
        A_main_layout.addWidget(self.setup_btn)
        A_main_layout.addLayout(play_row_lo)
        A_main_layout.addLayout(bake_row_lo)

        self.A_tab.setLayout(A_main_layout)

        # TAB B LAYOUT

        B_main_layout = QVBoxLayout()
        B_main_layout.setContentsMargins(VB_margin, VB_margin, VB_margin, VB_margin)
        B_main_layout.setSpacing(VB_spacing)

        edit_paint_meshes_row_lo = QHBoxLayout()
        edit_paint_meshes_row_lo.addWidget(self.add_as_paint_mesh_btn)
        edit_paint_meshes_row_lo.addWidget(self.remove_as_paint_mesh_btn)

        edit_scattered_row_lo = QHBoxLayout()
        edit_scattered_row_lo.addWidget(self.restore_scattered_xforms_btn)

        edit_colliders_row_lo = QHBoxLayout()
        edit_colliders_row_lo.addWidget(self.add_as_collider_btn)
        edit_colliders_row_lo.addWidget(self.remove_as_collider_btn)

        self.edit_paint_meshes_grp_box.setLayout(edit_paint_meshes_row_lo)
        self.edit_scattered_grp_box.setLayout(edit_scattered_row_lo)
        self.edit_colliders_grp_box.setLayout(edit_colliders_row_lo)

        # B_main_layout.addWidget(self.edit_paint_meshes_grp_box)
        B_main_layout.addWidget(self.edit_scattered_grp_box)
        # B_main_layout.addWidget(self.edit_colliders_grp_box)

        self.B_tab.setLayout(B_main_layout)

        # MASTER LAYOUT

        self.tabA_index = self.main_dialog_tabs.addTab(self.A_tab, "Create")
        self.tabB_index = self.main_dialog_tabs.addTab(self.B_tab, "Edit")
        self.main_dialog_tabs.setCurrentIndex(self.tabA_index)

        master_layout = QVBoxLayout(self)
        master_layout.setContentsMargins(0, 0, 0, 0)
        master_layout.setSpacing(VB_spacing)

        master_layout.addWidget(self.main_dialog_tabs)

    def create_connections(self):
        """Connects the Qt signals and slots"""
        self.load_clouds_btn.clicked.connect(self.load_clouds)
        self.load_scatters_btn.clicked.connect(self.load_scatters)
        self.load_grounds_btn.clicked.connect(self.load_grounds)

        self.setup_btn.clicked.connect(self.setup_PhysXPaint)
        self.delete_setup_btn.clicked.connect(self.delete_setup)

        self.play_pause_btn.clicked.connect(self.play_pause_toggle)
        self.reset_btn.clicked.connect(self.reset_playback)

        self.select_paint_node_btn.clicked.connect(self.select_paint_node)

        self.bake_current_btn.clicked.connect(self.do_bake_current)

        self.restore_scattered_xforms_btn.clicked.connect(self.restore_scattered_xforms)

    def load_clouds(self):
        """Set the Rig_Grp attribute of the class"""

        self.Clouds = pm.selected()
        le_txt = self.nodeName_print(self.Clouds)

        self.clouds_le.setText(le_txt)
        logger.info('Clouds selected: {}'.format(le_txt))

        return True

    def load_scatters(self):
        """Set the Skel_Grp attribute of the class"""

        self.Scatters = pm.selected()
        le_txt = self.nodeName_print(self.Scatters)

        self.scatters_le.setText(le_txt)
        logger.info('Objects to scatter selected: {}'.format(le_txt))

        return True

    def filter_polygonal_scatters(self):

        if self.Scatters:
            # filters mesh-only objects from the Scatters
            scatter_objs_polygonal = [obj for obj in self.Scatters if type(obj.getShape()) == pm.nt.Mesh]
            num_instances = len(scatter_objs_polygonal)
            logger.info("{0} scatter mesh(es) found: {1}".format(str(num_instances), str(scatter_objs_polygonal)))
        else:
            logger.info("Please load some meshes to scatter.")
            return None, 0

        return scatter_objs_polygonal, num_instances

    def log_num_verts_n_scatter_names(self, nodes):
        for node in nodes:
            self.NUM_VERTS_N_SCATTER_NAMES[node.getShape().numVertices()] = node.nodeName()

    def load_grounds(self):
        """Set the Geo_Grp attribute of the class"""

        self.Grounds = pm.selected()
        le_txt = self.nodeName_print(self.Grounds)

        self.grounds_le.setText(le_txt)
        logger.info('Grounds selected: {}'.format(le_txt))

        return True

    def nodeName_print(self, objs):
        """Returns more readable names of the selected objects"""

        return str([obj.nodeName() for obj in objs])

    def setup_PhysXPaint(self):

        util.check_n_load_plugin(cfg.MASH_PLUGIN_NAME)

        import MASH.api as mapi

        if self.Clouds:
            # gets the Clouds' shapes
            cloud_paint_meshes = [cloud.getShape() for cloud in self.Clouds if type(cloud.getShape()) == pm.nt.Mesh]
            logger.info("Paint mesh(es) found: {0}".format(str(cloud_paint_meshes)))
        else:
            cloud_paint_meshes = None
            logger.info("No paint mesh found.")

        if self.Grounds:
            # gets the Grounds' shapes
            ground_collide_meshes = [ground.getShape() for ground in self.Grounds
                                     if type(ground.getShape()) == pm.nt.Mesh]
            logger.info("Ground & collider mesh(es) found: {0}".format(str(ground_collide_meshes)))
        else:
            ground_collide_meshes = None
            logger.info("No ground nor collider found.")

        self.Scatters, num_instances = self.filter_polygonal_scatters()

        try:
            self.log_num_verts_n_scatter_names(self.Scatters)
        except:
            logger.info("Numbers of vertices of the Scatters are not unique.")
            pass
        
        if self.Scatters:
            if self.add_orient_nucleus_cb.isChecked():
                scatter_objs_processed = self.inject_orient_nucleus_foreach_scatter()
            else:
                scatter_objs_processed = self.Scatters

            if scatter_objs_processed:
                # selects only the objects to scatter
                pm.select(scatter_objs_processed, r=True)

                # initiates a MASH network
                self.php_mash_network = mapi.Network()
                self.php_mash_network.createNetwork(name="_".join([cfg.unique_prefix, cfg.MASH_PLUGIN_NAME]))
                logger.info("MASH network created: {0}.".format(self.php_mash_network.waiter))

                # accesses the default Distribute node
                php_mash_dist = pm.PyNode(self.php_mash_network.distribute)
                php_mash_dist.pointCount.set(0)  # disables this distribute node

                # accesses the default Repro node
                # php_mash_repro = pm.PyNode(self.php_mash_network.instancer)

                # adds a Placer node
                self.php_mash_placer = self.php_mash_network.addNode("MASH_Placer")
                logger.info("MASH Placer node added: {0}.".format(self.php_mash_placer.name))

                self.php_mash_placer = pm.PyNode(self.php_mash_placer.name)
                self.php_mash_placer.scatter.set(True)
                self.php_mash_placer.idMode.set(2)  # sets it to "Random"
                self.php_mash_placer.randomId1.set(num_instances - 1)  # array index
                #  TODO: elaborate this with large/small objs

                if cloud_paint_meshes:
                    # connects the Clouds to the Placer's paint meshes
                    for i, cloud in enumerate(cloud_paint_meshes):
                        cloud.worldMesh[0].connect(self.php_mash_placer.paintMeshes[i])
                        logger.info("{0} added as a paint mesh for {1}.".format(cloud.nodeName(),
                                                                             self.php_mash_placer.nodeName()))

                # adds a Dynamics node
                php_mash_dyn = self.php_mash_network.addNode("MASH_Dynamics")
                logger.info("MASH Dynamics node added: {0}.".format(php_mash_dyn.name))

                php_mash_dyn = pm.PyNode(php_mash_dyn.name)

                php_mash_dyn.collisionShape.set(4)  # sets it to "Convex Hull"

                # dynamics parameters
                dyn_friction = 0.4  # 0.3
                dyn_rolling_friction = 0.4  # 0.2
                dyn_damping = 0.3  # 0.1
                dyn_rolling_damping = 0.1  # 0.02
                dyn_bounce = 0.02  # 0.05
                dyn_collision_jitter = 0.005

                # TODO: tweak the Dynamics parameters
                php_mash_dyn.friction.set(dyn_friction)
                php_mash_dyn.rollingFriction.set(dyn_rolling_friction)
                php_mash_dyn.damping.set(dyn_damping)
                php_mash_dyn.rollingDamping.set(dyn_rolling_damping)
                php_mash_dyn.bounce.set(dyn_bounce)
                php_mash_dyn.collisionJitter.set(dyn_collision_jitter)

                # accesses the Bullet Solver
                self.php_mash_bullet = pm.PyNode(self.php_mash_network.getSolver())
                logger.info("Bullet Solver automatically created: {0}.".format(self.php_mash_bullet.nodeName()))

                if not ground_collide_meshes:
                    self.php_mash_bullet.groundPlanePositionY.set(0)  # overrides the default value of -20
                else:
                    self.php_mash_bullet.groundPlane.set(False)  # disables the Bullet's built-in ground
                    # loads the Grounds to the Bullet Solver's colliders
                    for collider in ground_collide_meshes:
                        self.php_mash_network.addCollider(collider.nodeName())
                        logger.info("{0} added as a collider in {1}.".format(collider.nodeName(),
                                                                          self.php_mash_bullet.nodeName()))

                # increases the time range; go to first frame
                extend_time_range(0, 3000, 0)

                # raises the MASH Outliner
                pm.mel.MASHOutliner()

                # selects the Placer node
                self.select_paint_node()

        else:
            logger.info("No valid object to scatter. Please load at least one polygonal mesh.")
            return False

        return True

    def import_orient_nucleus_obj(self):

        orient_nucleus_file_name = "_".join([cfg.unique_prefix,
                                             PhysXPainterDialog.ORIENT_NUCLEUS_NAME,
                                             "geo.obj"])  # "mnT2_orient_nucleus_geo.obj"
        orient_nucleus_file_path = os.path.join(cfg.tool_meshes_path, orient_nucleus_file_name)

        try:
            imported_orient_nucleus = pm.importFile(orient_nucleus_file_path,
                                                    defaultNamespace=True, returnNewNodes=True)
            # returns a list containing a transform and a mesh
        except:
            logger.info("Cannot import mesh {0}.".format(orient_nucleus_file_name))
            return False

        return imported_orient_nucleus[0]

    def inject_orient_nucleus_foreach_scatter(self, cleanup=True):

        op_name = "injected"
        spawn_suffix_name = "_".join([op_name, PhysXPainterDialog.ORIENT_NUCLEUS_NAME])

        orient_nucleus_stem = self.import_orient_nucleus_obj()  # xform of the imported "orient nucleus" mesh

        if orient_nucleus_stem:
            for scatter in self.Scatters:
                orient_nucleus_spawn = pm.duplicate(orient_nucleus_stem)[0]

                # matches their supposedly centered pivots
                pm.xform(scatter, centerPivots=True)
                scatter_pos_vector = pm.dt.Vector(pm.xform(scatter, q=True, rp=True, ws=True))
                orient_nucleus_spawn.translate.set(scatter_pos_vector)

                # does the "injection"
                pm.polyUnite(orient_nucleus_spawn, scatter, ch=False,
                             n="_".join([scatter.nodeName(), spawn_suffix_name]))

            if cleanup:
                pm.delete(orient_nucleus_stem)

        return pm.ls("*{0}".format(spawn_suffix_name))

    def play_pause_toggle(self):
        if not cmds.play(q=True, st=True):  # not playing
            self.play_pause_btn.setIcon(QIcon(":pause_S.png"))
            # activates interactive playback
            pm.mel.InteractivePlayback()
        else:
            self.play_pause_btn.setIcon(QIcon(":play_S.png"))
            cmds.play(st=0)  # pauses the playback

        return True

    def reset_playback(self):
        if cmds.play(q=True, st=True):  # playing
            cmds.play(st=0)  # pauses the playback
            self.play_pause_btn.setIcon(QIcon(":play_S.png"))

        SCENE_ENV.setTime(0)

        return True

    def select_paint_node(self):
        if self.php_mash_placer:
            pm.select(self.php_mash_placer, r=True)
            pm.mel.AttributeEditor()  # raises the Attribute Editor
            pm.mel.updateAE(self.php_mash_placer)  # updates it
            logger.info("Paint node {0} selected.".format(self.php_mash_placer.nodeName()))
            logger.info('Click "Play" and then click "Add" to start painting.')

        return True

    def delete_setup(self):
        success = "Custom MASH network removed."

        if self.php_mash_network:
            pm.delete(self.php_mash_network.waiter)
            logger.info(success)
        else:
            mash_waiters = [waiter for waiter in pm.ls(typ='MASH_Waiter') if waiter.nodeName().find(cfg.unique_prefix) != -1]

            if mash_waiters:
                pm.delete(mash_waiters)
                logger.info(success)
            else:
                logger.info("No custom MASH network found.")

        # resets the variables

        self.php_mash_network = None
        self.php_mash_placer = None
        self.php_mash_bullet = None

        pm.select(cl=True)  # clear the selection

        self.load_clouds()  # resets self.Clouds
        self.load_scatters()  # resets self.Scatters
        self.load_grounds()  # resets self.Grounds

        return True

    def do_bake_current(self):

        is_playing = cmds.play(q=True, st=True)

        if is_playing:
            cmds.play(st=0)  # pauses the playback

        if self.php_mash_network:
            # gets the Repro
            php_mash_repro = pm.PyNode(self.php_mash_network.instancer)
            php_mash_repro_mesh = php_mash_repro.outMesh.outputs()[0]  # gets the Repro mesh
            pm.duplicate(php_mash_repro_mesh, n="_".join([cfg.unique_prefix, "baked",
                                                          "f" + str(int(SCENE_ENV.time)),
                                                          PhysXPainterDialog.BAKED_MESH_IDENTIFIER]))

        if is_playing:
            pm.mel.InteractivePlayback()  # resumes the playback

        return True

    def add_selected_as_paint_mesh(self):
        pass

    def remove_selected_as_paint_mesh(self):
        pass

    def restore_scattered_xforms(self, cleanup_all=True):
        """
        This method calls these methods:
            _self.extract_orient_nuclei
        :return:
        """
        repro_mesh = pm.selected()

        if repro_mesh and repro_mesh[0].nodeName().find(PhysXPainterDialog.BAKED_MESH_IDENTIFIER) != -1:
            dist_threshold = 0.1  # TODO: allow user to tweak this parameter
            meshes = [obj for obj in pm.selected() if type(obj.getShape()) == pm.nt.Mesh]

            separated_meshes, extracted_orient_nuclei = self.extract_orient_nuclei(meshes)

            num_frozen_meshes = len(separated_meshes)
            num_successes = 0

            failed_meshes = []

            self.Scattered_Grp = pm.ls("*baked*PhysXPainter")
            if len(self.Scattered_Grp) > 1 or not self.Scattered_Grp:
                # doesn't know which group to use, making a new group instead
                self.Scattered_Grp = pm.group(em=True, n="_".join([cfg.unique_prefix,
                                                                "baked_PhysXPainter"]))
            else:
                self.Scattered_Grp = self.Scattered_Grp[0]

            for mesh_id, frozen_mesh in enumerate(separated_meshes, 1):
                logger.info("///***  WORKING ON MESH #{0} of {1}: {2}  ***///"
                         .format(mesh_id, num_frozen_meshes, frozen_mesh.nodeName()))
                nearest_nuclei = []
                frozen_mesh_pos = pm.dt.Vector(pm.xform(frozen_mesh, q=True, rp=True, ws=True))

                num_nuclei_left = len(extracted_orient_nuclei)

                for nucleus_id, nucleus in enumerate(extracted_orient_nuclei, 1):
                    logger.info("Calculating distance to nucleus #{0} of {1}: {2}"
                             .format(nucleus_id, num_nuclei_left, nucleus.nodeName()))
                    nucleus_pos = pm.dt.Vector(pm.xform(nucleus, q=True, rp=True, ws=True))
                    dist = (frozen_mesh_pos - nucleus_pos).length()
                    logger.info("__Distance = {}".format(dist))
                    if dist < dist_threshold:
                        nearest_nuclei.append(nucleus)
                        # for now just pick the first found "orient nucleus"
                        extracted_orient_nuclei.remove(nucleus)
                        break

                if nearest_nuclei:
                    logger.info("____Nearest nucleus found: {0}\n".format(str(nearest_nuclei)))
                    # processes this "orient nucleus"
                    processed_nucleus = self.process_orient_nucleus(nearest_nuclei[0], cleanup_nucleus=cleanup_all)
                    scattered_w_orient_restored = restore_mesh_orient2([frozen_mesh, processed_nucleus],
                                                                       bringToWorld=True, deleteGuide=cleanup_all)
                    num_successes += 1
                    pm.parent(scattered_w_orient_restored, self.Scattered_Grp)
                else:
                    logger.info("____(!)Found NO nearest nucleus within {0} distance threshold.\n".format(dist_threshold))
                    failed_meshes.append(frozen_mesh)

            logger.info("______Number of successes: {0} of {1}.".format(num_successes, num_frozen_meshes))
            if len(failed_meshes):
                logger.info("______(!)Meshes failed to restore orient: {0}.".format(str(failed_meshes)))
                pm.select(failed_meshes, r=True)

            if self.NUM_VERTS_N_SCATTER_NAMES:
                try:
                    logger.info("Attempting to restore names all the Scattered using their numbers of vertices...")
                    self.restore_scattered_names()
                except:
                    logger.info("Failed to restore names of the Scattered.")
                    pass
        else:
            logger.info('Please select the baked {0}'.format(PhysXPainterDialog.BAKED_MESH_IDENTIFIER))
        return True

    def extract_orient_nuclei(self, meshes):
        orient_nucleus_mesh_num_vertices = 4  # "mnT2_orient_nucleus_geo.obj"

        if meshes:
            separated_meshes = []
            # polySeparates them
            for mesh in meshes:
                try:
                    separated_meshes.extend(pm.polySeparate(mesh, ch=False))
                except:
                    pass

            # centers all their pivots
            pm.xform(separated_meshes, centerPivots=True)

            extracted_orient_nuclei = [obj for obj in separated_meshes
                                       if obj.getShape().numVertices() == orient_nucleus_mesh_num_vertices]

            if extracted_orient_nuclei:
                for nucleus in extracted_orient_nuclei:
                    separated_meshes.remove(nucleus)  # splits two lists with no overlapped objects
            else:
                logger.info('Found no "orient nucleus" to work on. Aborted...')

        else:
            logger.info("Please select the baked Repro mesh(es).")
            return None, None

        return separated_meshes, extracted_orient_nuclei
    
    def process_orient_nucleus(self, orient_nucleus_xform, cleanup_nucleus=True):
        op_name = "extracted"
        orient_nucleus_mesh = orient_nucleus_xform.getShape()

        vert0_vec = pm.dt.Vector(
            orient_nucleus_mesh.vtx[0].getPosition())  # origin point of the "orient nucleus" mesh
        vert1_vec = pm.dt.Vector(
            orient_nucleus_mesh.vtx[1].getPosition())  # front point of the "orient nucleus" mesh
        front_vec = vert1_vec.__sub__(vert0_vec)
        front_vec.normalize()  # front vector of the "orient nucleus"

        aligning_z_axis = pm.angleBetween(v1=front_vec, v2=pm.dt.Vector.zAxis, er=True)

        orient_nucleus_inverse_null = pm.group(em=True)
        orient_nucleus_pos_vector = pm.dt.Vector(pm.xform(orient_nucleus_xform, q=True, rp=True, ws=True))
        orient_nucleus_inverse_null.translate.set(orient_nucleus_pos_vector)

        orient_nucleus_null = pm.duplicate(orient_nucleus_inverse_null,
                                           n="_".join([op_name,
                                                       PhysXPainterDialog.ORIENT_NUCLEUS_NAME]))[0]
        # this will be used to contain the final rotation

        pm.parent(orient_nucleus_inverse_null, orient_nucleus_xform)
        orient_nucleus_xform.rotate.set(aligning_z_axis)  # aligns Z axis for the "orient nucleus"
        pm.parent(orient_nucleus_inverse_null, world=True)
        # resets the transforms of "orient nucleus" in order to
        # ensures the vectors properly queried from the vertices' world pos
        pm.makeIdentity(orient_nucleus_xform, apply=True, pn=True)
        pm.parent(orient_nucleus_inverse_null, orient_nucleus_xform)

        vert0_vec = pm.dt.Vector(
            orient_nucleus_mesh.vtx[0].getPosition())  # origin point of the "orient nucleus" mesh
        vert3_vec = pm.dt.Vector(
            orient_nucleus_mesh.vtx[3].getPosition())  # up point of the "orient nucleus" mesh
        up_vec = vert3_vec.__sub__(vert0_vec)
        up_vec.normalize()  # up vector of the "orient nucleus"

        # calculates the sign of the twist amount
        up_vec_cross_prod_y_axis_vec = up_vec.cross(pm.dt.Vector.yAxis)
        up_vec_cross_prod_y_axis_vec.normalize()
        up_vec_dot_prod_y_axis = up_vec_cross_prod_y_axis_vec.dot(pm.dt.Vector.zAxis)
        # logger.info("Dot product with Y axis: {0}".format(str(up_vec_dot_prod_y_axis)))

        aligning_y_axis = pm.dt.degrees(pm.dt.angle(up_vec, pm.dt.Vector.yAxis))
        orient_nucleus_xform.rotateZ.set(aligning_y_axis * up_vec_dot_prod_y_axis)  # aligns Y axis
        # for the "orient nucleus"
        pm.parent(orient_nucleus_inverse_null, world=True)

        # gets the world inverse matrix of the buffer SRT of the "orient nucleus"
        tmp_decomp_matrix = pm.createNode('decomposeMatrix')

        orient_nucleus_inverse_null.worldInverseMatrix[0].connect(tmp_decomp_matrix.inputMatrix)
        # logger.info('World inverse matrix of {0} obtained.'.format(orient_nucleus_inverse_null.nodeName()))

        # now inverts the reset motion of the "orient nucleus"
        orient_nucleus_null.rotate.set(tmp_decomp_matrix.outputRotate.get())

        pm.delete(tmp_decomp_matrix, orient_nucleus_inverse_null)
        if cleanup_nucleus:
            pm.delete(orient_nucleus_xform)

        return orient_nucleus_null

    def restore_scattered_names(self):
        for child in self.Scattered_Grp.getChildren():
            child.rename(self.NUM_VERTS_N_SCATTER_NAMES[child.getShape().numVertices()])
        return True

    def add_selected_as_collider(self):
        if self.php_mash_network:

            collider_meshes = [collider.getShape() for collider in pm.ls(sl=True) if
                               type(collider.getShape()) == pm.nt.Mesh]

            for collider in collider_meshes:
                self.php_mash_network.addCollider(collider.nodeName())
                logger.info("{0} added as a collider in {1}.".format(collider.nodeName(), self.php_mash_bullet.nodeName()))

        return True

    def remove_selected_as_collider(self):
        pass


def PhysXPainterDialog_showUI(mnT2_dialog_passed=None):

    global PhysXPainterDialogInstance  # mnT2_ui.mnT2.PhysXPainterDialogInstance

    if __name__ == "main":
        try:
            # closes and deletes previous instance if found
            PhysXPainterDialogInstance.close()
            PhysXPainterDialogInstance.deleteLater()
        except:
            pass

        # instantiates the tool dialog class
        PhysXPainterDialogInstance = PhysXPainterDialog(mnT2_dialog=mnT2_dialog_passed)
        # summons the beast
        PhysXPainterDialogInstance.show()


class SoftBodyCollisionDialog(QDialog):
    """This is the class of our tool dialog"""

    DEFORM_PLUGIN = "iDeform"
    COLLISION_OBJ = "iCollide"
    
    ATTRS = (('sbc_attrs_block', '*** SOFT-BODY'),
             ('sbc_envelope', 'Envelope'),
             ('sbc_mode', 'Mode'),
             ('sbc_bulge', 'Bulge'),
             ('sbc_radius', 'Radius'),
             ('sbc_offset', 'Offset'),
             ('sbc_useColors', 'Use Colors'),
             ('sbc_useGround', 'Use Ground'),
             ('sbc_groundHeight', 'Ground Height'),
             ('sbc_threshold', 'Threshold'))

    def __init__(self, parent=maya_main_window()):
        super(SoftBodyCollisionDialog, self).__init__(parent)

        self.setWindowTitle('Setup Soft-Body Collision')
        self.setMaximumWidth(261)
        self.setMaximumHeight(59)
        # disables the question mark button in Windows
        self.setWindowFlags(self.windowFlags() ^ Qt.WindowContextHelpButtonHint)

        self.create_widgets()
        self.create_layouts()
        self.create_connections()

    def create_widgets(self):
        """Creates the Qt widgets"""
        btn_style_sheet = "Text-align: left; min-width:9em"

        self.make_soft_body_btn = QPushButton("Make Soft-Body")
        self.make_soft_body_btn.setStyleSheet(btn_style_sheet)
        self.make_soft_body_btn.setIcon(QIcon(":fluidObjectEmit.png"))

        self.add_collider_btn = QPushButton("Add Collider")
        self.add_collider_btn.setStyleSheet(btn_style_sheet)
        self.add_collider_btn.setIcon(QIcon(":QR_add.png"))

        self.remove_collider_btn = QPushButton("Remove Collider")
        self.remove_collider_btn.setStyleSheet(btn_style_sheet)
        self.remove_collider_btn.setIcon(QIcon(":smallTrash.png"))  # removeBlendShape

        self.cleanup_soft_body_btn = QPushButton("Cleanup Soft-Body")
        self.cleanup_soft_body_btn.setStyleSheet(btn_style_sheet)
        self.cleanup_soft_body_btn.setIcon(QIcon(":confirm.png"))

    def create_layouts(self):
        """Creates the Qt layouts"""
        F_margin = 2
        F_spacing = 3
        
        main_layout = QFormLayout(self)
        main_layout.setContentsMargins(F_margin, F_margin, F_margin, F_margin)
        main_layout.setSpacing(F_spacing)
        
        main_layout.addRow(self.make_soft_body_btn, self.add_collider_btn)
        main_layout.addRow(self.remove_collider_btn, self.cleanup_soft_body_btn)

    def create_connections(self):
        """Connects the Qt signals and slots"""
        self.make_soft_body_btn.clicked.connect(self.make_soft_body)
        self.add_collider_btn.clicked.connect(self.add_collider)
        self.remove_collider_btn.clicked.connect(self.remove_collider)
        self.cleanup_soft_body_btn.clicked.connect(self.cleanup_soft_body)

    def make_soft_body(self):

        collision_class = pm.nt.ICollide

        for soft_body in pm.selected():
            # checks if any "iCollide" node exists
            soft_body_shape = soft_body.getShape()
            collision_nodes = soft_body_shape.listConnections(d=False, s=True, type=collision_class)
            if not collision_nodes and type(soft_body_shape) == pm.nt.Mesh:
                soft_body_shape.displayColors.set(True)

                pm.select(soft_body, r=True)
                collision_node = pm.PyNode(pm.mel.iCollide(1))  # creates new iCollide node and returns the created node
                logger.info("***An {0} node named {1} has been setup for object {2}.\n"
                         "Object {2} is now a Soft-Body!".
                         format(SoftBodyCollisionDialog.COLLISION_OBJ, collision_node.nodeName(), soft_body.nodeName()))
                self.setup_attrs(soft_body)
                collision_node.colorMode.set(1)
                soft_body.sbc_radius.set(self.guess_radius(soft_body_shape))
                self.connect_attrs(soft_body, collision_node)
            else:
                logger.info("Found {0} node(s) on object {1}. Skipped.".format(collision_nodes, soft_body))

        return True

    def setup_attrs(self, node):

        pm.addAttr(node, ln=SoftBodyCollisionDialog.ATTRS[0][0], nn=SoftBodyCollisionDialog.ATTRS[0][1], 
                   at='enum', k=True, enumName='ATTRS')  # sbc_attrs_block
        pm.addAttr(node, ln=SoftBodyCollisionDialog.ATTRS[1][0], nn=SoftBodyCollisionDialog.ATTRS[1][1], 
                   at='double', k=True, dv=1.0, min=0.0, max=1.0)  # sbc_envelope
        pm.addAttr(node, ln=SoftBodyCollisionDialog.ATTRS[2][0], nn=SoftBodyCollisionDialog.ATTRS[2][1],
                   at='enum', k=True, enumName='Relax:Trace', dv=0)  # sbc_mode
        pm.addAttr(node, ln=SoftBodyCollisionDialog.ATTRS[3][0], nn=SoftBodyCollisionDialog.ATTRS[3][1],
                   at='double', k=True, dv=1.0, min=0.0)  # sbc_bulge
        pm.addAttr(node, ln=SoftBodyCollisionDialog.ATTRS[4][0], nn=SoftBodyCollisionDialog.ATTRS[4][1],
                   at='double', k=True, min=0.0)  # sbc_radius
        pm.addAttr(node, ln=SoftBodyCollisionDialog.ATTRS[5][0], nn=SoftBodyCollisionDialog.ATTRS[5][1],
                   at='double', k=True, dv=0.0)  # sbc_offset
        pm.addAttr(node, ln=SoftBodyCollisionDialog.ATTRS[6][0], nn=SoftBodyCollisionDialog.ATTRS[6][1],
                   at='bool', k=True, dv=True)  # sbc_useColors
        pm.addAttr(node, ln=SoftBodyCollisionDialog.ATTRS[7][0], nn=SoftBodyCollisionDialog.ATTRS[7][1],
                   at='bool', k=True, dv=False)  # sbc_useGround
        pm.addAttr(node, ln=SoftBodyCollisionDialog.ATTRS[8][0], nn=SoftBodyCollisionDialog.ATTRS[8][1],
                   at='double', k=True, dv=0.0)  # sbc_groundHeight

        node.sbc_attrs_block.lock()

    def guess_radius(self, mesh):
        scale_factor = 5.55
        bbox = mesh.boundingBox()
        return max(bbox.width(), bbox.height(), bbox.depth()) / scale_factor

    def connect_attrs(self, node, deform_node):

        try:
            node.sbc_envelope.connect(deform_node.envelope)
            node.sbc_mode.connect(deform_node.mode)
            node.sbc_bulge.connect(deform_node.bulge)
            node.sbc_radius.connect(deform_node.radius)
            node.sbc_offset.connect(deform_node.offset)
            node.sbc_useColors.connect(deform_node.useColors)
            node.sbc_useGround.connect(deform_node.useGround)
            node.sbc_groundHeight.connect(deform_node.groundHeight)
        except:
            pass

        return True

    def add_collider(self):

        if len(pm.selected()) >= 2:
            # soft_body_shape = pm.selected()[-1].getShape()

            pm.mel.iCollide(0)

            # soft_body_shape.displayColors.set(False)
            # soft_body_shape.displayColors.set(True)
        else:
            logger.info("Please select the collider(s) first, and the soft-body last.")
            return False

        return True

    def remove_collider(self):

        if pm.selected():
            try:
                pm.mel.iCollideRemove()
            except:
                pass

        return True

    def cleanup_soft_body(self):

        collision_class = pm.nt.ICollide
        locked_attr = SoftBodyCollisionDialog.ATTRS[0][0]

        for soft_body in pm.selected():
            # checks if the "iCollide" node exists
            soft_body_shape = soft_body.getShape()
            collision_nodes = soft_body_shape.listConnections(d=False, s=True, type=collision_class)
            if collision_nodes:
                # stores the original mesh's name
                orig_name = soft_body.nodeName()
                # duplicates the resulted mesh
                soft_body_duplicated = pm.duplicate(soft_body)[0]
                # deletes the original mesh
                pm.delete(soft_body)  # this also effectively deletes the "iCollide" node
                # renames the duplicated mesh
                pm.rename(soft_body_duplicated, orig_name)
            else:
                soft_body_duplicated = soft_body
            # cleanups all the sbc_attrs
            for attr in SoftBodyCollisionDialog.ATTRS[1:]:
                if soft_body_duplicated.hasAttr(attr[0]):
                    pm.deleteAttr(soft_body_duplicated, at=attr[0])

            if soft_body_duplicated.hasAttr(locked_attr):
                pm.setAttr(".".join([soft_body_duplicated.nodeName(), locked_attr]), lock=False)
                pm.deleteAttr(soft_body_duplicated, at=locked_attr)

        return True

    
def SoftBodyCollisionDialog_showUI():

    util.source_all_mel_scripts(cfg.ingo_mel_files_glob_string)

    global SoftBodyCollisionDialogInstance  # mnT2_ui.mnT2.SoftBodyCollisionDialogInstance

    if __name__ == "main":
        try:
            # closes and deletes previous instance if found
            SoftBodyCollisionDialogInstance.close()
            SoftBodyCollisionDialogInstance.deleteLater()
        except:
            pass

        # instantiates the tool dialog class
        SoftBodyCollisionDialogInstance = SoftBodyCollisionDialog()
        # summons the beast
        SoftBodyCollisionDialogInstance.show()


# class UDIMManualTilingDialog(QDialog):
#     """This is the class of our tool dialog"""
# 
#     def __init__(self, parent=maya_main_window()):
#         super(UDIMManualTilingDialog, self).__init__(parent)
# 
#         self.setWindowTitle('UDIM Manual Tiling Creator')
#         self.setMinimumWidth(220)
#         # disables the question mark button in Windows
#         self.setWindowFlags(self.windowFlags() ^ Qt.WindowContextHelpButtonHint)
# 
#         self.ASSET_NAME = "tree_fig_a"
#         self.SPECIFIED_UDIM_STR = "1001-1005, 1009"
#         self.SPECIFIED_UDIM_INT = []
# 
#         self.MAP_TYPES_FULL = {'clr': (1, 0, 1), 'dif': (1, 0, 1), 'col': (1, 0, 1),
#                                'met': (0, 1, 2), 'rgh': (0, 1, 3),
#                                'spc': (0, 1, 4), 'spc_wt': (0, 1, 5),
#                                'opac': (0, 1, 6), 'tran': (1, 0, 7), 'tran_wt': (0, 1, 8),
#                                'nrml': (0, 0, 9), 'bmp': (0, 1, 10), 'dis': (0, 1, 11),
#                                'sss': (1, 0, 12), 'sss_wt': (0, 1, 13),
#                                'emi': (1, 0, 14), 'emi_wt': (0, 1, 15),
#                                'sheen': (1, 0, 16), 'sheen_wt': (0, 1, 17)}
# 
#         # {"map_name": (sRBG?, alpha_is_luminance?, sort_order_in_line_edit)}
# 
#         self.MAP_TYPES_TO_SKIP = ("dif", "col", "met", "spc", "spc_wt", "opac", "tran", "tran_wt", "sss", "sss_wt",
#                                   "emi", "emi_wt", "sheen", "sheen_wt")
# 
#         self.SPECIFIED_MAP_TYPES_STR = None
#         self.SPECIFIED_MAP_TYPES_LIST = None
# 
#         self.DEFAULT_TEXTURE_PATH = r"\\vnnas\Projects\WIZ\05_ForReview\asset"
#         self.CUSTOM_TEXTURE_PATH = ""
#         self.TEXTURE_SUFFIX = "hi_v1"
#         self.FILE_EXT = 'tif'
# 
#         self.create_widgets()
#         self.create_layouts()
#         self.load_default_map_types_to_le()  # loads starting maps using data from self.MAP_TYPES_FULL
#         self.load_link_texture_files_cb(self.link_texture_files_cb.isChecked())
#         self.update_map_types_from_le_text(self.map_types_le.text())
#         self.create_connections()
# 
#     def create_widgets(self):
#         """Creates the Qt widgets"""
#         self.asset_name_le = QLineEdit(self.ASSET_NAME)
#         self.udim_set_le = QLineEdit(self.SPECIFIED_UDIM_STR)
# 
#         self.map_types_le = QLineEdit()
# 
#         self.link_texture_files_cb = QCheckBox("Link texture files")
# 
#         self.texture_path_le = QLineEdit(self.DEFAULT_TEXTURE_PATH)
#         self.browse_btn = QPushButton()
#         self.browse_btn.setIcon(QIcon(":fileOpen.png"))
#         self.browse_btn.setToolTip("Browse to folder of texture files")
# 
#         self.texture_suffix_le = QLineEdit(self.TEXTURE_SUFFIX)
#         self.file_ext_le = QLineEdit(self.FILE_EXT)
# 
#         self.create_udim_manual_tiling_btn = QPushButton("Execute")
# 
#         # self.asset_name_le.setText()
#         # self.udim_set_le.setText()
#         # self.texture_path_le.setText()
#         # self.file_ext_le.setText()
#         self.link_texture_files_cb.setChecked(False)
# 
#     def create_layouts(self):
#         """Creates the Qt layouts"""
# 
#         F_spacing = 3
# 
#         texture_path_ro = QHBoxLayout()
#         texture_path_ro.addWidget(self.texture_path_le)
#         texture_path_ro.addWidget(self.browse_btn)
# 
#         file_format_row_lo = QHBoxLayout()
#         file_format_row_lo.addWidget(self.file_ext_le)
#         file_format_row_lo.addStretch()
#         file_format_row_lo.addWidget(self.create_udim_manual_tiling_btn)
# 
#         main_form_lo = QFormLayout()
#         main_form_lo.setSpacing(F_spacing)
#         main_form_lo.addRow("Asset Name:", self.asset_name_le)
#         main_form_lo.addRow("UDIM Set:", self.udim_set_le)
#         main_form_lo.addRow("Map Types:", self.map_types_le)
# 
#         main_form_lo.addRow("", self.link_texture_files_cb)
#         main_form_lo.addRow("Texture Path:", texture_path_ro)
#         main_form_lo.addRow("Texture Suffix:", self.texture_suffix_le)
#         main_form_lo.addRow("File Format:", file_format_row_lo)
# 
#         main_layout = QVBoxLayout(self)
#         main_layout.addLayout(main_form_lo)
# 
#     def create_connections(self):
#         """Connects the Qt signals and slots"""
# 
#         self.asset_name_le.textChanged.connect(self.update_asset_name_from_le_text)
#         self.udim_set_le.textChanged.connect(self.update_udim_set_from_le_text)
#         self.map_types_le.textChanged.connect(self.update_map_types_from_le_text)
# 
#         self.link_texture_files_cb.toggled.connect(self.load_link_texture_files_cb)
# 
#         self.texture_path_le.textChanged.connect(self.update_texture_path_from_le_text)
#         self.browse_btn.clicked.connect(self.load_browse_btn)
#         self.texture_suffix_le.textChanged.connect(self.update_texture_suffix_from_le_text)
#         self.file_ext_le.textChanged.connect(self.update_file_extension_from_le_text)
# 
#         self.create_udim_manual_tiling_btn.clicked.connect(self.do_create_udim_manual_tiling)
# 
#     def update_asset_name_from_le_text(self, text):
#         self.ASSET_NAME = text
#         logger.info('Asset name set to: {0}'.format(self.ASSET_NAME))
# 
#         return True
# 
#     def update_udim_set_from_le_text(self, text):
#         self.SPECIFIED_UDIM_STR = text
#         logger.info('UDIM specified: {0}'.format(self.SPECIFIED_UDIM_STR))
# 
#         return True
# 
#     def update_map_types_from_le_text(self, text):
#         self.SPECIFIED_MAP_TYPES_STR = text
#         logger.info('Map types specified: {0}'.format(self.SPECIFIED_MAP_TYPES_STR))
# 
#         return True
# 
#     def load_link_texture_files_cb(self, checked):
#         self.texture_path_le.setEnabled(checked)
#         self.browse_btn.setEnabled(checked)
#         self.texture_suffix_le.setEnabled(checked)
#         self.file_ext_le.setEnabled(checked)
# 
#         log_dict = {True: '', False: 'NOT '}
#         logger.info("Texture files will {0}be connected automatically.".format(log_dict[checked]))
# 
#         return True
# 
#     def update_texture_path_from_le_text(self, text):
#         self.CUSTOM_TEXTURE_PATH = text
#         logger.info('Custom Texture Path: {0}'.format(self.CUSTOM_TEXTURE_PATH))
# 
#         return True
# 
#     def update_texture_suffix_from_le_text(self, text):
#         self.TEXTURE_SUFFIX = text
#         logger.info('Texture suffix: {0}'.format(self.TEXTURE_SUFFIX))
# 
#         return True
# 
#     def update_file_extension_from_le_text(self, text):
#         self.FILE_EXT = text
#         logger.info('File Format: {0}'.format(self.FILE_EXT))
# 
#         return True
# 
#     def load_default_map_types_to_le(self):
#         map_types_list = []
#         for map_name in self.MAP_TYPES_FULL.keys():
#             if map_name not in self.MAP_TYPES_TO_SKIP:
#                 map_types_list.append(map_name)
# 
#         map_types_list.sort(key=lambda x: self.MAP_TYPES_FULL[x][-1])  # sorts it using the last parm of the value
# 
#         map_types_le_text = str(map_types_list)[1:-1]  # removes the square bracket from string conversion of a list
#         map_types_le_text = re.sub('\'', '', map_types_le_text)  # removes the ''
# 
#         self.map_types_le.setText(map_types_le_text)
# 
#         return True
# 
#     def load_browse_btn(self):
#         custom_texture_path = QFileDialog.getExistingDirectory(self, "Select Output Directory",
#                                                                             self.DEFAULT_TEXTURE_PATH,
#                                                                             QFileDialog.DontUseNativeDialog)
# 
#         if custom_texture_path:
#             self.texture_path_le.setText(custom_texture_path)
#             self.CUSTOM_TEXTURE_PATH = custom_texture_path
# 
#         logger.info('Custom Texture Path: {0}'.format(self.CUSTOM_TEXTURE_PATH))
# 
#         return True
# 
#     def process_udim_set_le_text(self):
#         # first removes the white space
#         self.SPECIFIED_UDIM_STR = re.sub("\s", "", self.SPECIFIED_UDIM_STR)
# 
#         # splits by comma
#         udim_comma_split = self.SPECIFIED_UDIM_STR.split(",")  # list of strings
# 
#         # processes the ranges, if any
#         udim_int_list = []
#         for udim in udim_comma_split:
#             if udim.find("-") != -1:
#                 # converts to range
#                 range_begin, range_end = udim.split("-")
#                 udim_int_list.extend(range(int(range_begin), int(range_end) + 1))
#             else:
#                 udim_int_list.append(int(udim))
# 
#         udim_int_list.sort(reverse=True)
# 
#         self.SPECIFIED_UDIM_INT = udim_int_list
# 
#         logger.info('Individual UDIM to process: {0}'.format(str(self.SPECIFIED_UDIM_INT)))
# 
#         return True
# 
#     def process_map_types_le_text(self):
#         # first removes the white space
#         self.SPECIFIED_MAP_TYPES_STR = re.sub("\s", "", self.SPECIFIED_MAP_TYPES_STR)
# 
#         # splits by comma
#         self.SPECIFIED_MAP_TYPES_LIST = self.SPECIFIED_MAP_TYPES_STR.split(",")  # list of strings
# 
#         logger.info('Maps to setup: {0}'.format(str(self.SPECIFIED_MAP_TYPES_LIST)))
# 
#         return True
# 
#     def do_create_udim_manual_tiling(self):
# 
#         self.process_udim_set_le_text()
#         self.process_map_types_le_text()
# 
#         logger.info("Creating UDIM manual tiling...")
# 
#         for i, UDIM in enumerate(self.SPECIFIED_UDIM_INT):
#             # calculates the frame translation
#             translate_u = (UDIM - 1001) % 10
#             translate_v = (UDIM - 1001) / 10
#             # creates the place2dTexture node
#             place2d_node = pm.shadingNode("place2dTexture", asUtility=1, n="_".join(["place2dTexture", str(UDIM),
#                                                                                      "U" + str(translate_u),
#                                                                                      "V" + str(translate_v)]))
#             # translates its frame
#             place2d_node.translateFrameU.set(translate_u)
#             place2d_node.translateFrameV.set(translate_v)
# 
#             for map_name in self.SPECIFIED_MAP_TYPES_LIST:
#                 # TODO: check if the texture file exists before creating a file node for it?
#                 map_file_node = pm.shadingNode("file", asTexture=1, isColorManaged=1,
#                                                n="_".join([self.ASSET_NAME, str(UDIM), map_name]))
# 
#                 # links the place2d_node with the files
#                 place2d_node.coverage.connect(map_file_node.coverage)
#                 place2d_node.translateFrame.connect(map_file_node.translateFrame)
#                 place2d_node.rotateFrame.connect(map_file_node.rotateFrame)
#                 place2d_node.mirrorU.connect(map_file_node.mirrorU)
#                 place2d_node.mirrorV.connect(map_file_node.mirrorV)
#                 place2d_node.stagger.connect(map_file_node.stagger)
# 
#                 place2d_node.wrapU.set(False)
#                 place2d_node.wrapU.connect(map_file_node.wrapU)
#                 place2d_node.wrapV.set(False)
#                 place2d_node.wrapV.connect(map_file_node.wrapV)
# 
#                 place2d_node.repeatUV.connect(map_file_node.repeatUV)
#                 place2d_node.offset.connect(map_file_node.offset)
#                 place2d_node.rotateUV.connect(map_file_node.rotateUV)
#                 place2d_node.noiseUV.connect(map_file_node.noiseUV)
#                 place2d_node.vertexUvOne.connect(map_file_node.vertexUvOne)
#                 place2d_node.vertexUvTwo.connect(map_file_node.vertexUvTwo)
#                 place2d_node.vertexUvThree.connect(map_file_node.vertexUvThree)
#                 place2d_node.vertexCameraOne.connect(map_file_node.vertexCameraOne)
#                 place2d_node.outUV.connect(map_file_node.uv)
#                 place2d_node.outUvFilterSize.connect(map_file_node.uvFilterSize)
# 
#                 if self.link_texture_files_cb.isChecked():
#                     # prepares the files' paths
#                     map_file_name = "_".join([self.ASSET_NAME, str(UDIM), map_name, self.TEXTURE_SUFFIX])
#                     map_file = ".".join([map_file_name, self.FILE_EXT])
# 
#                     if self.CUSTOM_TEXTURE_PATH:
#                         map_file_path = os.path.join(self.CUSTOM_TEXTURE_PATH, map_file)
#                     else:
#                         map_file_path = os.path.join(self.DEFAULT_TEXTURE_PATH, map_file)
# 
#                     # links the actual files
#                     # if os.path.exists(map_file_path):
#                     map_file_node.fileTextureName.set(map_file_path)
# 
#                 search_map_type_result = self.MAP_TYPES_FULL.get(map_name, -1)
#                 # sets it to -1 if specified map not found in predefined dict
# 
#                 if search_map_type_result != -1:
#                     # sets the proper color space
#                     if search_map_type_result[0]:  # if sRGB
#                         map_file_node.colorSpace.set('sRGB')
#                     else:
#                         map_file_node.colorSpace.set('Raw')
# 
#                     # sets the alphaIsLuminance
#                     map_file_node.alphaIsLuminance.set(search_map_type_result[1])
# 
#         # now connect the files to mimic UDIM tiling
# 
#         for map_name in self.SPECIFIED_MAP_TYPES_LIST:
#             for i, UDIM in enumerate(self.SPECIFIED_UDIM_INT):
#                 current_udim_file = pm.PyNode("_".join([self.ASSET_NAME, str(UDIM), map_name]))
#                 next_udim_file = pm.PyNode("_".join([self.ASSET_NAME, str(self.SPECIFIED_UDIM_INT[i + 1]), map_name]))
# 
#                 current_udim_file.outColor.connect(next_udim_file.defaultColor, force=True)
# 
#                 if i == len(self.SPECIFIED_UDIM_INT) - 2:  # skips the connecting for the last UDIM
#                     break
# 
#         return True
# 
# 
# def UDIMManualTilingDialog_showUI():
# 
#     global UDIMManualTilingDialogInstance  # mnT2_ui.mnT2.UDIMManualTilingDialogInstance
# 
#     if __name__ == "main":
#         try:
#             # closes and deletes previous instance if found
#             UDIMManualTilingDialogInstance.close()
#             UDIMManualTilingDialogInstance.deleteLater()
#         except:
#             pass
# 
#         # instantiates the tool dialog class
#         UDIMManualTilingDialogInstance = UDIMManualTilingDialog()
#         # summons the beast
#         UDIMManualTilingDialogInstance.show()


class ShaderDoctorDialog(QDialog):
    """This is the class of our tool dialog"""

    MAP_FILE = "file"

    MAPS = {"alpha": "", "ao": "", "col": "", "dmg": "", "ems": "", "hgt": "",
            "msk": "", "mtl": "", "nml": "", "rgb": "", "rgh": "", "trns": ""}

    MAPS_SORTED = OrderedDict(sorted(MAPS.items()))
    
    CHANNELS = {"specColor": ""}

    CHANNELS_SORTED = OrderedDict(sorted(CHANNELS.items()))

    def __init__(self, parent=maya_main_window()):
        super(ShaderDoctorDialog, self).__init__(parent)

        self.setWindowTitle('Shader Doctor')
        self.setMinimumWidth(390)
        # disables the question mark button in Windows
        self.setWindowFlags(self.windowFlags() ^ Qt.WindowContextHelpButtonHint)

        self.SCENE_SHADERS = None
        self.SCENE_MAP_FILES = None

        self.CRITERIA_CHANNELS = None
        self.CRITERIA_MAP_FILES = None
        
        self.create_widgets()

        self.SHADER_TYPE = {self.arnold_shader_rb: ("aiStandardSurface",),
                            self.l_b_p_shader_rb: ("lambert", "blinn", "phong")}

        self.create_layouts()
        self.create_connections()

        self.init_text_label()

    def create_widgets(self):
        """Creates the Qt widgets"""

        self.map_info_label = QLabel()
        self.channel_info_label = QLabel()
        
        self.mapped_le = QLineEdit()
        self.channel_le = QLineEdit()
        
        # self.browse_btn = QPushButton()
        # self.browse_btn.setIcon(QIcon(":fileOpen.png"))
        # self.browse_btn.setToolTip("Click this you fool!")

        self.mapped_invert_cb = QCheckBox("Invert")
        self.channel_invert_cb = QCheckBox("Invert")
        
        self.arnold_shader_rb = QRadioButton("Arnold")
        self.l_b_p_shader_rb = QRadioButton("Lambert / Blinn / Phong")

        self.search_shader_btn = QPushButton("Search SHADERS")
        self.search_shader_btn.setStyleSheet(cfg.grey_green4_btn_ss)

        self.search_texture_btn = QPushButton("Search TEXTURES")

        self.search_mesh_btn = QPushButton("Search MESHES")
        self.search_mesh_btn.setStyleSheet(cfg.grey_pink2_btn_ss)

        self.map_info_label.setEnabled(False)
        self.channel_info_label.setEnabled(False)

        self.arnold_shader_rb.setChecked(True)

        # WIP
        self.channel_le.setEnabled(False)
        self.channel_invert_cb.setEnabled(False)

    def create_layouts(self):
        """Creates the Qt layouts"""

        map_settings_row_lo = QHBoxLayout()
        map_settings_row_lo.addWidget(self.mapped_le)
        map_settings_row_lo.addWidget(self.mapped_invert_cb)

        channel_settings_row_lo = QHBoxLayout()
        channel_settings_row_lo.addWidget(self.channel_le)
        channel_settings_row_lo.addWidget(self.channel_invert_cb)

        shader_option_row_lo = QHBoxLayout()
        shader_option_row_lo.addWidget(self.arnold_shader_rb)
        shader_option_row_lo.addWidget(self.l_b_p_shader_rb)

        form_layout = QFormLayout()
        form_layout.addRow("", self.map_info_label)
        form_layout.addRow("Mapped:", map_settings_row_lo)

        form_layout.addRow("", self.channel_info_label)
        form_layout.addRow("Configured:", channel_settings_row_lo)

        form_layout.addRow("Shader", shader_option_row_lo)

        btn_layout = QHBoxLayout()
        # btn_layout.addStretch()
        btn_layout.addWidget(self.search_shader_btn)
        btn_layout.addWidget(self.search_texture_btn)
        btn_layout.addWidget(self.search_mesh_btn)

        main_layout = QVBoxLayout(self)
        main_layout.addLayout(form_layout)
        main_layout.addLayout(btn_layout)

    def create_connections(self):
        """Connects the Qt signals and slots"""

        # self.mapped_le.textChanged.connect(self.load_text_line_edit)
        # self.browse_btn.clicked.connect(self.load_browse_btn)
        # self.mapped_invert_cb.toggled.connect(self.load_check_box)
        # self.arnold_shader_rb.toggled.connect(self.load_radio_btn_A)
        # self.l_b_p_shader_rb.toggled.connect(self.load_radio_btn_B)

        self.search_shader_btn.clicked.connect(partial(self.do_search, centric="shader"))
        self.search_texture_btn.clicked.connect(partial(self.do_search, centric="texture"))
        self.search_mesh_btn.clicked.connect(partial(self.do_search, centric="mesh"))

    def init_text_label(self):

        map_types = str(ShaderDoctorDialog.MAPS_SORTED.keys()).replace("'", "")[1:-1]
        self.map_info_label.setText(str(map_types))

        channel_types = str(ShaderDoctorDialog.CHANNELS_SORTED.keys()).replace("'", "")[1:-1]
        self.channel_info_label.setText(str(channel_types))

    def do_search(self, centric=""):
        
        parsed_criteria_map_files = self.mapped_le.text().replace(" ", "")
        
        if parsed_criteria_map_files:

            SHADER_OPTION = None
    
            # queries the selected shader type
            for shader_option_rb in self.SHADER_TYPE.keys():
                if shader_option_rb.isChecked():
                    SHADER_OPTION = shader_option_rb
                    break
    
            # resets these before every search
            SUSPECTED_MAP_FILES = set()
    
            # firstly queries the scene
            self.SCENE_SHADERS = pm.ls(type=self.SHADER_TYPE[SHADER_OPTION])
            self.SCENE_MAP_FILES = pm.ls(type=ShaderDoctorDialog.MAP_FILE)

            # secondly reads the user input
            self.CRITERIA_MAP_FILES = parsed_criteria_map_files.split(",")
    
            # now processes the map files in the scene
            if self.CRITERIA_MAP_FILES:
                for MAP_FILE in self.SCENE_MAP_FILES:
                    for CRITERIA_MAP_FILE in self.CRITERIA_MAP_FILES:
                        if re.findall(CRITERIA_MAP_FILE, MAP_FILE.fileTextureName.get()):
                            SUSPECTED_MAP_FILES.add(MAP_FILE)

            def shader_from_map_file(map_files):
                """
                :param map_files: a set of map file nodes
                :return: a set of shader nodes each of which has one of the map file node indirectly connects to
                """
                suspected_shaders = set()
    
                for map_file in map_files:
                    for shader in self.SHADER_TYPE[SHADER_OPTION]:
                        future_shader_list = pm.listHistory(map_file, future=True, type=shader)
                        for future_shader in future_shader_list:
                            suspected_shaders.add(future_shader)
    
                if suspected_shaders:
                    logger.info("Found shaders {0}".format(suspected_shaders))
                else:
                    logger.info("Found no shader from map files {0}".format(map_files))
    
                return suspected_shaders

            def mesh_from_shader(shaders):

                suspected_meshes = set()

                for shader in shaders:
                    shading_engine = shader.listConnections(type='shadingEngine')[0]
                    suspected_meshes_list = pm.sets(shading_engine, q=True)
                    for suspected_mesh in suspected_meshes_list:
                        suspected_meshes.add(suspected_mesh)

                return suspected_meshes

    
            if not self.mapped_invert_cb.isChecked():
    
                if centric == "texture":
                    pm.select(SUSPECTED_MAP_FILES, r=True)
                    return True
    
                if centric == "shader":
                    SUSPECTED_SHADERS = shader_from_map_file(SUSPECTED_MAP_FILES)
                    pm.select(SUSPECTED_SHADERS, r=True)
                    return True
    
                if centric == "mesh":
                    SUSPECTED_SHADERS = shader_from_map_file(SUSPECTED_MAP_FILES)
                    SUSPECTED_MESHES = mesh_from_shader(SUSPECTED_SHADERS)
                    pm.select(SUSPECTED_MESHES, r=True)
                    return True
    
            else:
                # inverse mode
    
                if centric == "texture":
                    SUSPECTED_MAP_FILES = set(self.SCENE_MAP_FILES) - SUSPECTED_MAP_FILES
                    pm.select(SUSPECTED_MAP_FILES, r=True)
                    return True
    
                if centric == "shader":
                    SUSPECTED_SHADERS = shader_from_map_file(SUSPECTED_MAP_FILES)
                    SUSPECTED_SHADERS = set(self.SCENE_SHADERS) - SUSPECTED_SHADERS
                    pm.select(SUSPECTED_SHADERS, r=True)
                    return True
    
                if centric == "mesh":
                    SUSPECTED_SHADERS = shader_from_map_file(SUSPECTED_MAP_FILES)
                    SUSPECTED_MESHES = mesh_from_shader(SUSPECTED_SHADERS)

                    SUSPECTED_MESHES = set(pm.ls(type="mesh")) - SUSPECTED_MESHES
                    pm.select(SUSPECTED_MESHES, r=True)
                    return True

        else:
            logger.info("No criteria given. Aborted.")


def ShaderDoctorDialog_showUI():

    global ShaderDoctorDialogInstance  # mnT2_ui.mnT2.ShaderDoctorDialogInstance

    if __name__ == "main":
        try:
            # closes and deletes previous instance if found
            ShaderDoctorDialogInstance.close()
            ShaderDoctorDialogInstance.deleteLater()
        except:
            pass

        # instantiates the tool dialog class
        ShaderDoctorDialogInstance = ShaderDoctorDialog()
        # summons the beast
        ShaderDoctorDialogInstance.show()


class DissectNTransferDialog(QDialog):
    """This is the class of our tool dialog"""

    tool_version = "0.0.1"

    SOURCE_NAME = "source"
    TARGET_NAME = "target"
    STRAY_PIECES_SET_NAME = 'Stray_Pieces'
    # MESSAGE_ATTR = 'Pair_to_Transfer'

    def __init__(self, parent=maya_main_window()):
        super(DissectNTransferDialog, self).__init__(parent)

        self.setWindowTitle("Dissect before Transfer v{}".format(DissectNTransferDialog.tool_version))
        # self.setMinimumWidth(350)
        self.setMaximumHeight(290)

        # disables the question mark button in Windows
        self.setWindowFlags(self.windowFlags() ^ Qt.WindowContextHelpButtonHint)

        ###################################################

        self.Source_Compound_Mesh = None
        self.Target_Compound_Mesh = None

        self.Source_Compound_Mesh_Backup = None
        self.Target_Compound_Mesh_Backup = None

        self.Orig_Names = []

        self.Source_Separate_Pieces = None
        self.Target_Separate_Pieces = None

        self.RECORDED_PAIRS = {}
        self.STRAY_PIECES = []

        ###################################################

        self.create_widgets()
        self.create_layouts()
        self.create_connections()

    def create_widgets(self):

        self.source_mesh_le = QLineEdit()
        self.target_mesh_le = QLineEdit()

        self.load_source_mesh_btn = QPushButton("Load")
        # self.load_source_mesh_btn.setToolTip("Load selected as Control Rig group")

        self.load_target_mesh_btn = QPushButton("Load")
        # self.load_target_mesh_btn.setToolTip("Load selected as Bind Skeleton group")
        
        self.max_lookup_spinbox = QSpinBox()
        self.max_lookup_spinbox.setRange(1, 10)
        self.max_lookup_spinbox.setFixedWidth(40)
        self.max_lookup_spinbox.setButtonSymbols(QAbstractSpinBox.NoButtons)

        self.distance_threshold_spinbox = QDoubleSpinBox()
        self.distance_threshold_spinbox.setRange(0.001, 10.0)
        self.distance_threshold_spinbox.setSingleStep(0.01)
        self.distance_threshold_spinbox.setDecimals(3)
        self.distance_threshold_spinbox.setFixedWidth(40)
        self.distance_threshold_spinbox.setButtonSymbols(QAbstractSpinBox.NoButtons)

        self.lower_bound_spinbox = QDoubleSpinBox()
        self.lower_bound_spinbox.setRange(0.1, 1.0)
        self.lower_bound_spinbox.setSingleStep(0.1)
        self.lower_bound_spinbox.setDecimals(1)
        self.lower_bound_spinbox.setFixedWidth(40)
        self.lower_bound_spinbox.setButtonSymbols(QAbstractSpinBox.NoButtons)

        self.upper_bound_spinbox = QDoubleSpinBox()
        self.upper_bound_spinbox.setRange(1.0, 15.0)
        self.upper_bound_spinbox.setSingleStep(0.1)
        self.upper_bound_spinbox.setDecimals(1)
        self.upper_bound_spinbox.setFixedWidth(40)
        self.upper_bound_spinbox.setButtonSymbols(QAbstractSpinBox.NoButtons)

        self.preprocess_btn = QPushButton("* Pre-process *")
#         self.preprocess_btn.setToolTip("First please load Skel grp and Geo grp,\
# then click to run the check")

        self.check_result_print_le = QLineEdit('//Result:')

        self.tag_pair_btn = QPushButton("Tag")
        self.untag_pair_btn = QPushButton("Remove Tag")
        self.clear_all_tagged_btn = QPushButton("Clear All")

        self.select_stray_pieces_btn = QPushButton("Select Untagged")

        self.pairs_list_wdg = QListWidget()
        self.pairs_list_wdg.setSelectionMode(QAbstractItemView.ExtendedSelection)

        # EXECUTION BUTTON WIDGET

        self.abort_cleanup_btn = QPushButton("Abort + Cleanup")
        self.select_linked_btn = QPushButton("(+) Select Linked")
        self.do_transfer_btn = QPushButton("*** Transfer UV ***")

        # TAB A: SET INIT
        self.max_lookup_spinbox.setValue(3)
        self.distance_threshold_spinbox.setValue(0.3)
        self.lower_bound_spinbox.setValue(0.7)
        self.upper_bound_spinbox.setValue(10.0)

        self.abort_cleanup_btn.setEnabled(False)

    def create_layouts(self):

        # LOAD SELECTION LAYOUTS

        load_source_mesh_row_lo = QHBoxLayout()
        load_source_mesh_row_lo.addWidget(self.source_mesh_le)
        load_source_mesh_row_lo.addWidget(self.load_source_mesh_btn)

        load_target_mesh_row_lo = QHBoxLayout()
        load_target_mesh_row_lo.addWidget(self.target_mesh_le)
        load_target_mesh_row_lo.addWidget(self.load_target_mesh_btn)

        common_load_meshes_form_lo = QFormLayout()
        common_load_meshes_form_lo.addRow('Mesh w/ Correct UV:', load_source_mesh_row_lo)
        common_load_meshes_form_lo.addRow('Reduced Mesh:', load_target_mesh_row_lo)

        # PREPOCESSING PARAMETERS LAYOUT

        max_lookup_spinbox_lo = QFormLayout()
        max_lookup_spinbox_lo.addRow("Max Candidates", self.max_lookup_spinbox)
        max_lookup_spinbox_lo.addRow("Lower Ratio", self.lower_bound_spinbox)

        distance_threshold_spinbox_lo = QFormLayout()
        distance_threshold_spinbox_lo.addRow("Tolerance Dist.", self.distance_threshold_spinbox)
        distance_threshold_spinbox_lo.addRow("Upper Ratio", self.upper_bound_spinbox)

        lookup_spinboxes_row_lo = QHBoxLayout()
        lookup_spinboxes_row_lo.addLayout(max_lookup_spinbox_lo)
        lookup_spinboxes_row_lo.addLayout(distance_threshold_spinbox_lo)

        # TAGGING LAYOUT

        tag_pair_row_lo = QHBoxLayout()
        tag_pair_row_lo.addWidget(self.tag_pair_btn)
        tag_pair_row_lo.addWidget(self.untag_pair_btn)
        tag_pair_row_lo.addWidget(self.clear_all_tagged_btn)

        stray_pieces_row_lo = QHBoxLayout()
        stray_pieces_row_lo.addWidget(self.select_stray_pieces_btn)

        tag_pair_form_lo = QFormLayout()
        tag_pair_form_lo.addRow('Future Pair:', tag_pair_row_lo)
        # tag_pair_form_lo.addRow('Stray Pieces:', stray_pieces_row_lo)

        utility_btns_row_lo = QHBoxLayout()
        utility_btns_row_lo.addWidget(self.abort_cleanup_btn)
        utility_btns_row_lo.addWidget(self.select_linked_btn)

        # process_execute_vbox_lo.addLayout(tag_pair_form_lo)
        # process_execute_vbox_lo.addWidget(self.pairs_list_wdg)

        master_layout = QVBoxLayout(self)
        master_layout.setContentsMargins(3, 3, 3, 3)

        master_layout.addLayout(common_load_meshes_form_lo)
        master_layout.addLayout(lookup_spinboxes_row_lo)
        master_layout.addWidget(self.preprocess_btn)
        master_layout.addWidget(self.check_result_print_le)
        master_layout.addLayout(utility_btns_row_lo)
        master_layout.addWidget(self.do_transfer_btn)

    def create_connections(self):
        """Connects the Qt signals and slots for tab B"""

        self.load_source_mesh_btn.clicked.connect(self.load_source_mesh)
        self.load_target_mesh_btn.clicked.connect(self.load_target_mesh)

        self.preprocess_btn.clicked.connect(self.do_preprocess)
        # self.tag_pair_btn.clicked.connect(self.tag_future_pair)
        # self.untag_pair_btn.clicked.connect(self.untag_future_pair)
        # self.clear_all_tagged_btn.clicked.connect(self.clear_all_pairs)
        # self.select_stray_pieces_btn.clicked.connect(self.select_untagged_stray_pieces)

        self.select_linked_btn.clicked.connect(self.select_linked)

        self.do_transfer_btn.clicked.connect(self.transfer_uvs)

    def load_source_mesh(self):
        """Set the Source Mesh attribute of the class"""

        self.Source_Compound_Mesh = pm.selected()[0]
        le_txt = self.Source_Compound_Mesh.nodeName()

        self.source_mesh_le.setText(le_txt)
        logger.info('Source mesh selected: {}'.format(le_txt))

        return True

    def load_target_mesh(self):
        """Set the Target Mesh attribute of the class"""

        self.Target_Compound_Mesh = pm.selected()[0]
        le_txt = self.Target_Compound_Mesh.nodeName()

        self.target_mesh_le.setText(le_txt)
        logger.info('Target mesh selected: {}'.format(le_txt))
        
        return True

    def do_preprocess(self):

        if self.Source_Compound_Mesh and self.Target_Compound_Mesh:

            self.Orig_Names.extend((self.Source_Compound_Mesh.nodeName(), self.Target_Compound_Mesh.nodeName()))

            def duplicate_for_backup(obj):
                backup = pm.duplicate(obj, n="_".join([cfg.unique_prefix,
                                                       obj.nodeName(),
                                                       "backup"]))
                backup[0].visibility.set(False)
                return backup[0]

            self.Source_Compound_Mesh_Backup = duplicate_for_backup(self.Source_Compound_Mesh)
            self.Target_Compound_Mesh_Backup = duplicate_for_backup(self.Target_Compound_Mesh)

            def sorted_separate(obj, piece_type=""):
                separated = pm.polySeparate(obj, ch=False)

                # centers pivot the pieces
                pm.xform(separated, centerPivots=True)

                pieces_list = [(piece, piece.getShape().numVertices()) for piece in separated]
                sorted(pieces_list, key=lambda x: x[1])

                for piece_id, piece in enumerate(pieces_list, 1):
                    pm.rename(piece[0], "_".join([piece_type,
                                                  str(piece_id)]))
                return pieces_list

            self.Source_Separate_Pieces = sorted_separate(self.Source_Compound_Mesh,
                                                          piece_type=DissectNTransferDialog.SOURCE_NAME)
            self.Target_Separate_Pieces = sorted_separate(self.Target_Compound_Mesh,
                                                          piece_type=DissectNTransferDialog.TARGET_NAME)

            self.RECORDED_PAIRS, self.STRAY_PIECES = self.search_closest_piece(self.Source_Separate_Pieces,
                                                                               self.Target_Separate_Pieces)

            # pm.select(self.RECORDED_PAIRS, r=True)

        return True

    def search_closest_piece(self, source, target):

        remaining_source_pieces = copy.deepcopy(source)

        num_target_pieces = len(target)
        num_successes = 0

        recorded_pairs = {}
        failed_target_pieces = []

        progress_dialog = QProgressDialog("Pre-processing...", "Stop", 0, num_target_pieces, self)
        progress_dialog.setWindowTitle("Analyzing...")
        progress_dialog.setValue(0)
        progress_dialog.setWindowModality(Qt.WindowModal)
        progress_dialog.show()

        QCoreApplication.processEvents()

        for target_piece_id, target_piece in enumerate(target, 1):

            if progress_dialog.wasCanceled():
                break

            progress_label_text = "Working on target piece: {0} of {1}: {2}".format(target_piece_id,
                                                                                    num_target_pieces,
                                                                                    target_piece[0].nodeName())
            progress_dialog.setLabelText(progress_label_text)
            progress_dialog.setValue(target_piece_id)

            QCoreApplication.processEvents()

            target_piece_pos = pm.dt.Vector(pm.xform(target_piece[0], q=True, rp=True, ws=True))

            # num_remaining_source_pieces = len(remaining_source_pieces)

            lower_bound_num_vertices = target_piece[1] * self.lower_bound_spinbox.value()
            upper_bound_num_vertices = target_piece[1] * self.upper_bound_spinbox.value()

            source_pieces_search_range = filter(lambda x: lower_bound_num_vertices <= x[1] <= upper_bound_num_vertices,
                                                remaining_source_pieces)

            # num_source_pieces_search_range = len(source_pieces_search_range)

            nearest_pieces = []
            nearest_piece = None
            found = 0

            for source_piece_from_range_id, source_piece_from_range in enumerate(source_pieces_search_range, 1):

                # logger.info("Calculating distance to source piece #{0} of range {1}: {2}"
                #          .format(source_piece_from_range_id,
                #                  num_source_pieces_search_range,
                #                  source_piece_from_range[0].nodeName()))

                source_piece_from_range_pos = pm.dt.Vector(pm.xform(source_piece_from_range[0], q=True, rp=True, ws=True))
                dist = (target_piece_pos - source_piece_from_range_pos).length()

                # logger.info("__Distance = {}".format(dist))

                if dist < self.distance_threshold_spinbox.value():
                    valid_candidate = tuple([source_piece_from_range[0], dist])
                    nearest_pieces.append(valid_candidate)
                    found += 1
                    if found >= self.max_lookup_spinbox.value():
                        break

            # logger.info("Nearest pieces: {0}".format(str(nearest_pieces)))
            # using distance as key

            sorted(nearest_pieces, key=lambda x: x[1])
            # logger.info("___Found {0} candidates: {1}".format(found, str()))

            if nearest_pieces:
                nearest_piece = nearest_pieces[0][0]
                source_piece_to_remove = (nearest_piece, nearest_piece.getShape().numVertices())
                remaining_source_pieces.remove(source_piece_to_remove)

            if nearest_piece:
                recorded_pairs[target_piece[0]] = nearest_piece
                # logger.info("____Nearest source piece found: {0}\n".format(str(nearest_piece)))
                num_successes += 1

            else:
                # logger.info("____(!)Found NO nearest source piece within {0} distance threshold.\n"
                #          .format(self.distance_threshold_spinbox.value()))
                failed_target_pieces.append(target_piece[0])

        preprocess_result = "Successes: {0} of {1}. Percentage: {2:.2f}%."\
            .format(num_successes,
                    num_target_pieces,
                    100*num_successes/float(num_target_pieces))

        self.result_print(preprocess_result)

        if failed_target_pieces:
            logger.info("______(!)Pieces failed to locate corresponding source: {0}.".format(str(failed_target_pieces)))
            pm.select(failed_target_pieces, r=True)

            # creates a set
            if not pm.ls(DissectNTransferDialog.STRAY_PIECES_SET_NAME):
                pm.sets(n=DissectNTransferDialog.STRAY_PIECES_SET_NAME)
            logger.info('All stray pieces are added to set "{}"'.format(DissectNTransferDialog.STRAY_PIECES_SET_NAME))

            # pm.select(cl=True)

        progress_dialog.close()

        return recorded_pairs, failed_target_pieces

    def select_linked(self):

        if pm.selected():
            query_obj = pm.selected()[0]

            if self.STRAY_PIECES:
                if query_obj in self.STRAY_PIECES:
                    logger.info("Cannot find linked of a stray piece.")
                    return False

            if query_obj.nodeName().find(DissectNTransferDialog.TARGET_NAME) != -1:
                # target piece selected, looks for corresponding source
                pm.select(self.RECORDED_PAIRS[query_obj], add=True)
            elif query_obj.nodeName().find(DissectNTransferDialog.SOURCE_NAME) != -1:
                # source piece selected, looks for corresponding piece
                for target, source in self.RECORDED_PAIRS.items():
                    if source == query_obj:
                        pm.select(target, add=True)

        return True

    def transfer_uvs(self):

        if self.RECORDED_PAIRS:
            for target, source in self.RECORDED_PAIRS.items():
                pm.transferAttributes(source, target, pos=0, nml=0, col=0, uvs=2, fuv=0, sampleSpace=0, searchMethod=3)
                pm.delete(target, ch=True)

            # combines all the target pieces
            target_combined = pm.polyUnite(self.RECORDED_PAIRS.keys(), n="_".join([self.Orig_Names[1], "transferred"]))

            # deletes all the source pieces
            pm.delete(self.RECORDED_PAIRS.values()[0].getParent())  # just pick a random value and find its parent

            # cleanups history
            pm.delete(target_combined, ch=True)

            # deletes the target backup and restores the source backup
            pm.delete(self.Target_Compound_Mesh_Backup)

            pm.rename(self.Source_Compound_Mesh_Backup, self.Orig_Names[0])
            self.Source_Compound_Mesh_Backup.visibility.set(True)

            # combines the stray target pieces
            if self.STRAY_PIECES:
                if len(self.STRAY_PIECES) >= 2:
                    pm.polyUnite(self.STRAY_PIECES, ch=False,
                                 n="_".join([self.Orig_Names[1], "stray"]))

                pm.sets(DissectNTransferDialog.STRAY_PIECES_SET_NAME, e=True, clear=True)
                pm.delete(DissectNTransferDialog.STRAY_PIECES_SET_NAME)

            pm.select(target_combined, r=True)
            self.result_print("// DONE.")

        return True

    def result_print(self, message):
        self.check_result_print_le.setText(message)
        return True

    def create_n_connect_message_attr(self, objs):

        for obj in objs[:-1]:
            if not obj.hasAttr(self.MESSAGE_ATTR):
                pm.addAttr(obj, ln=self.MESSAGE_ATTR, at='message')
                pm.connectAttr(objs[-1].message, obj.SH_parentJnt)

        return True

    def delete_message_attr(self, QListWidget_item):

        # removes the recently created custom message attrs
        jnts = QListWidget_item.data(Qt.UserRole)

        for jnt in jnts[:-1]:
            jntNode = pm.PyNode(jnt)

            if jntNode.hasAttr(self.MESSAGE_ATTR):
                jntNode.deleteAttr(self.MESSAGE_ATTR)
                logger.info('Removed custom attribute "{0}" on {1}'.format(self.MESSAGE_ATTR, jnt))

    def tag_future_pair(self):

        objs = pm.ls(sl=True)

        for obj in objs:
            if obj.type() != 'joint':
                logger.info('Please select joints only.')
                break

        else:
            if len(objs) > 1:

                self.create_n_connect_message_attr(objs)

                tag_line = "PARENT: {}___ CHILD: {}".format(objs[-1].nodeName(),
                                                            self.nodeName_print(objs[:-1]))

                list_wdg_item = QListWidgetItem(tag_line)

                # since QListWidgetItem.data does not work with PyNode objects
                list_wdg_item.setData(Qt.UserRole, [x.longName() for x in objs])

                self.pairs_list_wdg.addItem(list_wdg_item)
                return True

            else:
                logger.info('Please select at least 2 joints.')
                return False

    def untag_future_pair(self):

        selectedItems = self.pairs_list_wdg.selectedItems()

        for i in selectedItems:
            # deletes the custom message attr
            self.delete_message_attr(i)

            # removes item from the QListWidget
            QIndex = self.pairs_list_wdg.indexFromItem(i)
            self.pairs_list_wdg.takeItem(QIndex.row())

    def clear_all_pairs(self):

        for row in range(self.pairs_list_wdg.count()):
            self.delete_message_attr(self.pairs_list_wdg.item(row))

        self.pairs_list_wdg.clear()

    def select_untagged_stray_pieces(self):

        if self.stray_pieces:
            pm.select(cl=True)
            for jnt in self.stray_pieces:
                if not jnt.hasAttr(self.MESSAGE_ATTR):
                    pm.select(jnt, add=True)

        return True

    
def DissectNTransferDialog_showUI():

    global DissectNTransferDialogInstance  # mnT2_ui.mnT2.DissectNTransferDialogInstance

    if __name__ == "main":
        try:
            # closes and deletes previous instance if found
            DissectNTransferDialogInstance.close()
            DissectNTransferDialogInstance.deleteLater()
        except:
            pass

        # instantiates the tool dialog class
        DissectNTransferDialogInstance = DissectNTransferDialog()
        # summons the beast
        DissectNTransferDialogInstance.show()


class UltimateClipboardDialog(QDialog):
    """This is the class of our tool dialog"""

    JSON_EXT = {True: "json", False: "ma"}
    MA_EXT = "mayaAscii"
    STR_DIVIDER = "@"
    ATTRS = {"transform": ("tx", "ty", "tz",
                           "rx", "ry", "rz",
                           "sx", "sy", "sz")}
    # STR_EXAMPLE = "cam01@nambinh"

    tool_version = "0.0.1"

    def __init__(self, parent=maya_main_window(), user_exchange_path="", exchange_repo_root=cfg.repo_exchange_path):
        super(UltimateClipboardDialog, self).__init__(parent)

        self.setWindowTitle('Ultimate Clipboard  v{0}'.format(UltimateClipboardDialog.tool_version))
        self.setMinimumWidth(200)
        # disables the question mark button in Windows
        self.setWindowFlags(self.windowFlags() ^ Qt.WindowContextHelpButtonHint)

        self.user_exchange_path = user_exchange_path
        self.exchange_repo_root = exchange_repo_root

        self.create_widgets()

        self.EXCHANGE_MODE = {self.generic_dag_rb: "generic_dag",
                              self.mesh_rb: "mesh",
                              self.camera_shape_rb: "camera",
                              self.ai_light_shape_rb: "ai_light",
                              self.ai_shader_rb: "ai_shader"}

        self.create_layouts()
        self.create_connections()

    def create_widgets(self):
        """Creates the Qt widgets"""

        self.reminder_label = QLabel("your username is: {0}".format(cfg.current_username))
        self.reminder_label.setStyleSheet("color: rgb(255, 79, 166)")

        self.data_string_le = QLineEdit()

        self.browse_btn = QPushButton()
        self.browse_btn.setIcon(QIcon(":fileOpen.png"))
        # self.browse_btn.setEnabled(False)

        self.transform_cb = QCheckBox("Transform")
        self.transform_cb.setChecked(True)

        self.generic_dag_rb = QRadioButton("Generic DAG")
        self.mesh_rb = QRadioButton("Mesh")
        
        self.camera_shape_rb = QRadioButton("Camera Settings")
        self.ai_light_shape_rb = QRadioButton("ai Light")
        self.ai_shader_rb = QRadioButton("ai Shader")
        
        self.copy_btn = QPushButton("COPY   (*Write*)")
        self.copy_btn.setStyleSheet("background-color: rgb(51, 34, 120)")
        self.copy_btn.setIcon(QIcon(":copySkinWeight.png"))

        self.paste_btn = QPushButton("PASTE   (*Read*)")
        self.paste_btn.setStyleSheet("background-color: rgb(175, 52, 97)")
        self.paste_btn.setIcon(QIcon(":pasteUV.png"))

        self.generic_dag_rb.setChecked(True)

        self.camera_shape_rb.setEnabled(False)
        self.ai_light_shape_rb.setEnabled(False)
        self.ai_shader_rb.setEnabled(False)

    def create_layouts(self):
        """Creates the Qt layouts"""

        row_layout = QHBoxLayout()
        row_layout.addWidget(self.data_string_le)
        row_layout.addWidget(self.browse_btn)

        option_row_lo_1 = QHBoxLayout()
        option_row_lo_1.addWidget(self.generic_dag_rb)
        option_row_lo_1.addWidget(self.mesh_rb)

        option_row_lo_2 = QHBoxLayout()
        option_row_lo_2.addWidget(self.camera_shape_rb)

        option_row_lo_3 = QHBoxLayout()
        option_row_lo_3.addWidget(self.ai_light_shape_rb)
        option_row_lo_3.addWidget(self.ai_shader_rb)

        form_layout = QFormLayout()
        form_layout.addRow("Data String:", row_layout)
        form_layout.addRow(self.transform_cb, option_row_lo_1)
        form_layout.addRow("", option_row_lo_2)
        form_layout.addRow("", option_row_lo_3)

        execute_btn_layout = QHBoxLayout()
        execute_btn_layout.addWidget(self.copy_btn)
        execute_btn_layout.addWidget(self.paste_btn)

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.reminder_label)
        main_layout.addLayout(form_layout)
        main_layout.addLayout(option_row_lo_1)
        main_layout.addLayout(execute_btn_layout)

    def create_connections(self):
        """Connects the Qt signals and slots"""
        self.browse_btn.clicked.connect(self.browse_data_file)

        self.mesh_rb.toggled.connect(self.disable_transform_cb)
        self.ai_shader_rb.toggled.connect(self.disable_transform_cb)

        self.copy_btn.clicked.connect(self.write_data)
        self.paste_btn.clicked.connect(self.read_data)

    def load_browse_btn(self):
        logger.info('TODO: Browse button clicked')
        return True

    def disable_transform_cb(self, clicked):
        logger.info('Option "Transform" is disabled as either "Mesh" or "ai Shader" is selected.')
        self.transform_cb.setEnabled(not clicked)
        return True

    def process_data(self, process_mode):
        """
        :param process_mode: str, either "read" or "write"
        :return:
        """

        data_string_le_text = self.data_string_le.text()

        def get_shape_exchange_mode():
            for radio_button in self.EXCHANGE_MODE.keys():
                if radio_button.isChecked():
                    return self.EXCHANGE_MODE[radio_button]

        current_shape_exchange_mode = get_shape_exchange_mode()
        # logger.info('Shape exchange mode is set to "{0}"'.format(current_shape_exchange_mode))

        def parse_data_string(given_data_string, json=True):

            # bisects the data string
            if given_data_string.find(UltimateClipboardDialog.STR_DIVIDER) != -1:
                # collaborative mode
                data_file, divider, collaborator = \
                    given_data_string.rpartition(UltimateClipboardDialog.STR_DIVIDER)

                file_name = ".".join([data_file, UltimateClipboardDialog.JSON_EXT[json]])
                target_path = os.path.join(self.exchange_repo_root, collaborator, file_name)

            else:
                # solo mode
                file_name = ".".join([given_data_string, UltimateClipboardDialog.JSON_EXT[json]])
                target_path = os.path.join(self.user_exchange_path, file_name)

            return target_path

        sel = pm.selected()
        data_dict = {}

        if data_string_le_text:

            if current_shape_exchange_mode != "mesh":
                # working with JSON
                if sel:
                    target_file_path = parse_data_string(data_string_le_text, json=True)

                    obj_xform = sel[0]
                    obj_name = obj_xform.nodeName()

                    if process_mode == "write":
                        if self.transform_cb.isChecked() and self.transform_cb.isEnabled():
                            for attr in UltimateClipboardDialog.ATTRS["transform"]:
                                data_dict[attr] = cmds.getAttr(".".join([obj_name, attr]))

                        util.save_json(data_dict, target_file_path, 1)

                    elif process_mode == "read":

                        data_dict = util.load_json(target_file_path, 1)

                        if data_dict:
                            if self.transform_cb.isChecked() and self.transform_cb.isEnabled():
                                for attr in UltimateClipboardDialog.ATTRS["transform"]:
                                    current_attr = pm.PyNode(".".join([obj_name, attr]))
                                    if not current_attr.isLocked():
                                        current_attr.set(data_dict[attr])
                        else:
                            logger.info("Empty data file. Please check the data string again.")
                else:
                    logger.info("Nothing selected. Aborted.")
                    return False

            else:
                # working with meshes
                target_file_path = parse_data_string(data_string_le_text, json=False)

                if process_mode == "write":
                    # saves the selected meshes
                    pm.exportSelected(target_file_path, type=UltimateClipboardDialog.MA_EXT)

                elif process_mode == "read":
                    # imports the .ma file
                    try:
                        pm.importFile(target_file_path)
                    except Exception as error:
                        logger.info("Cannot paste due to: {0}.".format(error))
                    pass

        else:
            logger.info("Unspecified data string. Aborted.")
            return False

        return True

    def write_data(self):
        self.process_data(process_mode="write")

    def read_data(self):
        self.process_data(process_mode="read")
        
    def browse_data_file(self):

        custom_data_file, filters = QFileDialog.getOpenFileName(self, "Select the data file", self.exchange_repo_root)

        if custom_data_file:
            # queries the file name
            data_file_full_name = os.path.basename(custom_data_file)
            # logger.info("data_file_full_name: {0}".format(data_file_full_name))

            data_file_name, dot, data_file_type = data_file_full_name.rpartition(".")
            # logger.info("data_file_type: {0}".format(data_file_type))

            # queries the folder that contains it
            data_folder_name = os.path.dirname(custom_data_file).rpartition("/")[-1]
            # logger.info("data_folder_name: {0}".format(data_folder_name))

            if data_folder_name == cfg.current_username:
                # self mode
                parsed_data_string = data_file_name
            else:
                # collaborative mode
                parsed_data_string = data_file_name + UltimateClipboardDialog.STR_DIVIDER + data_folder_name

            # logger.info("Parsed_data_string: {0}".format(parsed_data_string))

            self.data_string_le.setText(parsed_data_string)

            if data_file_type == UltimateClipboardDialog.JSON_EXT[False]:
                self.mesh_rb.setChecked(True)

            return parsed_data_string


def UltimateClipboardDialog_showUI(user_path):

    global UltimateClipboardDialogInstance  # mnT2_ui.mnT2.UltimateClipboardDialogInstance

    if __name__ == "main":
        try:
            # closes and deletes previous instance if found
            UltimateClipboardDialogInstance.close()
            UltimateClipboardDialogInstance.deleteLater()
        except:
            pass

        # instantiates the tool dialog class
        UltimateClipboardDialogInstance = UltimateClipboardDialog(user_exchange_path=user_path)
        # summons the beast
        UltimateClipboardDialogInstance.show()
