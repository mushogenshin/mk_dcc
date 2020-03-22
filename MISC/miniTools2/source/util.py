import os
import sys
import glob
import json
import re
import time
import logging as logger
from distutils.dir_util import copy_tree
from collections import defaultdict
from operator import itemgetter

import maya.mel
import maya.cmds as cmds
import pymel.core as pm
import maya.api.OpenMaya as om2

_PATHLIB2_PATH = "C:/vsTools2/ALL/python"
sys.path.append(_PATHLIB2_PATH)
from pathlib2 import Path

import config as cfg
# reload(cfg)


def simple_mel(cmd=""):
    maya.mel.eval(cmd)


def current_scene_folder():
    filepath = cmds.file(q=True, sn=True)
    if filepath:
        return Path(filepath).parent.as_posix()
    else:
        return None


def add_to_sys_path(path):
    if path not in sys.path:
        sys.path.append(path)
        logger.info("{0} has been added to sys.path".format(path))
    else:
        logger.info("{0} is already in sys.path. Proceeding...".format(path))


def check_n_set_up_local_folder(folder_name, base_folder_path):

    full_folder_path = os.path.join(base_folder_path, folder_name)

    # checks if the subfolder exists
    if os.path.exists(full_folder_path):
        logger.info('Folder "{0}" already exists at {1}. Proceeding...'.format(folder_name, base_folder_path))
    else:
        logger.info('Folder "{0}" does NOT exist at {1}. Creating it...'.format(folder_name, base_folder_path))
        # creates the subfolder
        try:
            os.makedirs(full_folder_path)
        except:
            return False
        logger.info('Folder "{0}" has been created at {1}.'.format(folder_name, base_folder_path))

    return full_folder_path


def source_all_mel_scripts(mel_files_glob_string):

    mel_file_paths = glob.glob(mel_files_glob_string)

    for mel_file in mel_file_paths:
        mel_script_name = mel_file.split("\\")[-1].rpartition(".")[0]
        logger.info('Sourcing MEL script "{0}"...'.format(mel_script_name))
        try:
            maya.mel.eval('source "{0}"'.format(os.path.normpath(mel_file).replace("\\", "/")))
        except Exception as error:
            logger.info('Cannot source MEL script "{0}" due to: {1}...'.format(mel_script_name, error))
            pass

    return True


def check_n_load_plugin(plugin_name):
    # checks if the plugin is loaded, and loads it if not
    if not pm.pluginInfo(plugin_name, q=True, loaded=True):
        logger.info('Plugin "{0}" is not loaded. Loading it...'.format(plugin_name))
        try:
            pm.loadPlugin(plugin_name)
        except:
            return False
        else:
            logger.info('Plugin "{0}" is successfully loaded.'.format(plugin_name))
            return True
    else:
        logger.info('Plugin "{0}" is already loaded. Proceeding...'.format(plugin_name))


def simple_dir_dialog(dir=None):
    if not dir:
        return cmds.fileDialog2(fileMode=3, dialogStyle=2)[0]
    else:
        return cmds.fileDialog2(dir=dir, fileMode=3, dialogStyle=2)[0]


def select_every_edge(edge_type="", num=2):
    pm.mel.polySelectEdgesEveryN(edge_type, num)
    return True


def select_tris_or_n_gons(obj=None, n_gon=False):
    if not obj:
        pm.selectMode(object=True)
        obj = pm.selected()[0]

    if obj:
        obj_shape = obj.getShape()

        if not n_gon:
            found = [face for face in obj_shape.f if face.numVertices() == 3]
        else:
            found = [face for face in obj_shape.f if face.numVertices() > 4]

        if found:
            pm.selectMode(component=True)
            pm.select(found, r=True)
            return found, obj_shape
        else:
            logger.info("Nothing found")
            return False, obj_shape


def select_stray_vertices(num=2):

    n_gons, obj_shape = select_tris_or_n_gons(n_gon=True)

    if n_gons:

        verts_to_filter = set()

        for n_gon in n_gons:
            for vert_id in n_gon.getVertices():
                verts_to_filter.add(obj_shape.vtx[vert_id])

        found = filter(lambda x: len(x.connectedEdges().indices()) <= num, verts_to_filter)

        pm.select(found, r=True)

        return found


def export_files_separately(files_separately_output_folder, file_type="", fbx=False):

    selected_objs = pm.ls(sl=True)

    if selected_objs:
        if not fbx:
            for obj in selected_objs:
                pm.select(obj, r=True)
                pm.exportSelected(os.path.join(files_separately_output_folder,
                                               "{0}.{1}".format(obj.nodeName().replace(":", "_"), cfg.FILE_EXT[file_type])),
                                  type=file_type)
        else:
            check_n_load_plugin(cfg.FBX_PLUGIN_NAME)
            for obj in selected_objs:
                pm.select(obj, r=True)
                pm.mel.FBXExport(f=os.path.join(files_separately_output_folder,
                                                "{0}.fbx".format(obj.nodeName().replace(":", "_"))), s=True)

        pm.select(cl=True)
    else:
        logger.info("Please select at least one object.")

    return True


def set_cam_clip_plane(preset=None):

    cam = pm.PyNode('perspShape')

    if cam:
        cam.nearClipPlane.set(cfg.CAM_CLIP_PLANE_DIST[preset][0])
        cam.farClipPlane.set(cfg.CAM_CLIP_PLANE_DIST[preset][1])

    return True


def get_uv_shells(mesh, uv_set=None):
    """ Return UVs per shell ID for a given mesh.

    :return: list(list)
    :rtype: Return a list of UVs per shell.
    """

    # define which uv_set to process
    uv_sets = cmds.polyUVSet(mesh, q=True, allUVSets=True)
    if not uv_set or uv_set not in uv_sets:
        uv_set = cmds.polyUVSet(mesh, q=True, cuv=True)[0]

    # get the api dag path
    sel = om2.MSelectionList()
    sel.add(mesh)
    dag_path = sel.getDagPath(0)
    dag_path.extendToShape()

    # Note:
    # Maya returns the .map[id] on the transform instead of shape if you select it.
    # For convenience for now let's do the same (whether you want this is up to you)
    mesh = cmds.ls(dag_path.fullPathName(), long=True, o=True)[0]
    mesh = mesh.rsplit('|', 1)[0]  # get the parent transform

    # get shell uv ids
    fn_mesh = om2.MFnMesh(dag_path)
    uv_count, uv_shell_array = fn_mesh.getUvShellsIds(uv_set)

    # convert to a format we like it (per shell)
    uv_shells = defaultdict(list)
    for i, shellId in enumerate(uv_shell_array):
        uv = '{0}.map[{1}]'.format(mesh, i)
        uv_shells[shellId].append(uv)

    # return a list per shell
    return uv_shells.values()


def udim_coord_to_u_v(udim_coord):
    u_coord = (udim_coord - 1001) % 10
    v_coord = (udim_coord - 1001) / 10
    return u_coord, v_coord


def filter_transforms():

    if pm.selected():
        # filters transform-only objects from the selection
        transforms = [obj for obj in pm.selected() if type(obj) == pm.nt.Transform]
    else:
        logger.info("Nothing selected. Aborted")
        return None

    return transforms


def filter_polygonal_meshes():
    
    if pm.selected():
        # filters polygonal-mesh-only objects from the selection
        polygonal_meshes = [obj.getShape() for obj in pm.selected() if type(obj.getShape()) == pm.nt.Mesh]
    else:
        logger.info("Nothing selected. Aborted")
        return None
    
    return polygonal_meshes


def do_default_aim_constraint():

    sel = pm.selected()

    if sel:
        driver = sel[0]
        driven = sel[1]

        pm.aimConstraint(driver, driven, mo=False)

    return True


def center_thingy(thing="locator"):

    centered_thing = None

    sel = cmds.ls(sl=True, fl=True)
    pos = [cmds.xform(x, q=True, ws=True, bb=True) for x in sel]
    val = len(pos)
    pos = [sum(e) for e in zip(*pos)]
    pos = [e / val for e in pos]

    cmds.select(cl=True)

    posX = (pos[0] + pos[3]) / 2
    posY = (pos[1] + pos[4]) / 2
    posZ = (pos[2] + pos[5]) / 2

    if thing == "null":
        centered_thing = pm.group(em=True)
        centered_thing.translate.set(posX, posY, posZ)

    elif thing == "locator":
        centered_thing = pm.spaceLocator()
        centered_thing.translate.set(posX, posY, posZ)

    elif thing == "joint":
        centered_thing = pm.joint(p=(posX, posY, posZ))

    cmds.select(sel, r=True)

    return centered_thing


def joint_based_realign(mesh, comp_grp1, comp_grp2, comp_type='vtx'):
    """
    mesh: str,
    comp_grp1, comp_grp2: lists or tuples of component IDs,
    comp_type: 'vtx', 'e', 'f'
    """

    comp_grp1_sel = [".".join([mesh, comp_type + '[{}]'.format(i)]) for i in comp_grp1]
    comp_grp2_sel = [".".join([mesh, comp_type + '[{}]'.format(i)]) for i in comp_grp2]

    try:
        pm.select(comp_grp1_sel, r=True)
        joint_parent = center_thingy("joint")

        pm.select(comp_grp2_sel, r=True)
        joint_child = center_thingy("joint")
    except Exception as e:
        print('(!) Cannot execute due to: {}.\n'.format(e))
    else:
        pm.parent(joint_child, joint_parent)

        # orients joint
        pm.select(joint_parent, r=True)
        pm.joint(e=True, oj='xyz', sao='yup')

        # parents the mesh
        constr = pm.parentConstraint(joint_parent, mesh, mo=True)
        # TODO: improve the pivot

        # now "resets" the joint orient

        def nearest_90(num):
            return round(num / 90) * 90

        joint_parent.jointOrientX.set(nearest_90(joint_parent.jointOrientX.get()))
        joint_parent.jointOrientY.set(nearest_90(joint_parent.jointOrientY.get()))
        joint_parent.jointOrientZ.set(nearest_90(joint_parent.jointOrientZ.get()))

        # cleans up the constraint
        pm.delete(constr, joint_parent)

    cmds.select(cl=True)


def remove_duplicates(vertex_list):
    # type: (list) -> list
    """Removes duplicate entries in the given list. Returns the cleand list."""
    # Source: http://stackoverflow.com/questions/480214/
    #         how-do-you-remove-duplicates-from-a-list-in-python-whilst-preserving-order
    seen = set()
    seen_add = seen.add
    return [x for x in vertex_list if not (x in seen or seen_add(x))]


def convert_selection_to_vertices(selection_list):
    # type: (list) -> list
    """Converts multi-selection (vertices, edges, NurbsCurveCV, NurbsCurve)
       to a simple vertex list.

    e.g.
    [nt.Transform(u'curve1')] =>
    [NurbsCurveCV(u'curveShape1.cv[0]'), NurbsCurveCV(u'curveShape1.cv[1]'),
     NurbsCurveCV(u'curveShape1.cv[2]'), NurbsCurveCV(u'curveShape1.cv[3]'),
     NurbsCurveCV(u'curveShape1.cv[4]')]

    or

    [MeshEdge(u'polySurfShape.e[5]'), MeshEdge(u'polySurfShape.e[8]')] =>
    [MeshVertex(u'polySurfShape.vtx[4]'), MeshVertex(u'polySurfShape.vtx[0]'),
     MeshVertex(u'polySurfShape.vtx[6]'), MeshVertex(u'polySurfShape.vtx[4]')]
    """

    vertex_list = []

    edge_in_selection = False

    for i in range(0, len(selection_list)):
        # Poly Mesh Vertex
        if isinstance(selection_list[i], pm.general.MeshVertex):
            vertex_list.append(selection_list[i])
        # Poly Mesh Edge
        elif isinstance(selection_list[i], pm.general.MeshEdge):
            vertex_list.extend(selection_list[i].connectedVertices())
            # duplicates might are in resulting list --> Get rid of it later
            edge_in_selection = True
        # Nurbs Curve CV
        elif isinstance(selection_list[i], pm.general.NurbsCurveCV):
            vertex_list.append(selection_list[i])
        # Nurbs Curve Transform Node
        elif selection_list[i].nodeType() == "transform" and \
                selection_list[i].getShape() != None and \
                selection_list[i].getShape().nodeType() == "nurbsCurve":
            vertex_list.extend(selection_list[i].getShape().cv)
        # Nurbs Curve
        elif selection_list[i].nodeType() == "nurbsCurve":
            vertex_list.extend(selection_list[i].cv)
        # Not supported selection type
        else:
            pm.warning("Selection {} not supported.".format(selection_list[i]))

    # In case of edges there might be duplicates in the list => get rid of them
    if edge_in_selection:
        vertex_list = remove_duplicates(vertex_list)

    return vertex_list


def find_max_distance(vertex_list):
    # type: (list) -> (int, int)
    """Looks for the max distance between all vertices in the given list.
       Returns the indexes of the two resulting vertices. """

    # print "Finding max distance between selected vertices ..."

    max_distance = 0
    min_point = 0
    max_point = 0
    start_index = 0

    while start_index < len(vertex_list) - 1:
        for i in range(start_index + 1, len(vertex_list)):
            cur_vector = vertex_list[start_index].getPosition(space='world') - vertex_list[i].getPosition(space='world')
            cur_distance = cur_vector.length()
            if cur_distance > max_distance:
                max_distance = cur_distance
                min_point = start_index
                max_point = i

        start_index += 1

        # print "Max distance of {} found between {} ({}) and {} ({})".format(max_distance,
        # vertex_list[min_point].getPosition(space='world'), vertex_list[min_point],
        # vertex_list[max_point].getPosition(space='world'), vertex_list[max_point])

        return min_point, max_point


def straighten_components(mode="maxDistance"):
    # type: (str) -> None
    """Straightens the selected vertices to a common line."""

    # Get current selection
    sel = pm.ls(os=True, fl=True)
    # print "Current Selection: {}".format(sel)

    # convert selection
    sel = convert_selection_to_vertices(sel)
    # print "Converted Selection: {}".format(sel)

    # check for minimal selection
    if len(sel) < 3:
        pm.warning("Selection must consist of at least 3 points. Nothing done.")
        return

    # Define main vector points
    # start_i = end_i = 0
    if mode == "maxDistance":
        start_i, end_i = find_max_distance(sel)
    elif mode == "firstTwo":
        start_i = 0
        end_i = 1
    elif mode == "lastTwo":
        start_i = len(sel) - 1
        end_i = len(sel) - 2
    else:
        pm.warning("Unknown mode '{}'. Nothing done.".format(mode))
        return

    # set main vector
    main_vector = sel[end_i].getPosition(space='world') - sel[start_i].getPosition(space='world')
    # print "Main vector defined through {} and {}".format(sel[start_i], sel[end_i])
    # print "Main vector for moving points: {} (= {} --> {})".format(main_vector,
    # sel[start_i].getPosition(space='world'),
    # sel[end_i].getPosition(space='world'))
    # main_vector_length = main_vector.length()

    # Normalize main vector
    main_vector.normalize()

    # move points (except start_i and end_i
    for i in range(0, len(sel)):
        if i not in (start_i, end_i):
            vec_to_cur_vert = sel[i].getPosition(space='world') - sel[start_i].getPosition(space='world')
            lambdaValue = main_vector.dot(vec_to_cur_vert)
            new_position = main_vector * lambdaValue + sel[start_i].getPosition(space='world')
            # print "Moving {} from {} to {}".format(sel[i], sel[i].getPosition(space='world'), new_position)
            # Should work, but causes undo issues in non-centimeter space (see fixes 1.0.1)
            # sel[i].setPosition(new_position, space='world')

            # By using Maya.cmds "undo" is working
            scaleFactor = sel[i].getPosition(space='world')[3]
            new_position = [new_position[0] * scaleFactor, new_position[1] * scaleFactor,
                            new_position[2] * scaleFactor]
            cmds.xform(sel[i].__str__(), ws=True, t=new_position)

            if isinstance(sel[i], pm.general.NurbsCurveCV):
                    sel[i].updateCurve()


def save_json(data_dict, json_path, verbose=0):

    if not os.path.exists((os.path.dirname(json_path))):
        os.makedirs((os.path.dirname(json_path)))

    with open(json_path, 'w') as json_file:
        new_string = json.dumps(data_dict, indent=4, sort_keys=True)
        json_file.write(new_string)
        if verbose:
            logger.info('Saved data to JSON successfully : {}'.format(json_path))


def load_json(json_path, verbose=0):

    if not os.path.exists(json_path):
        json_dir = os.path.dirname(json_path)
        if not os.path.exists(json_dir):
            os.makedirs(json_dir)
        with open(json_path, 'w') as json_file:
            data = {}
            json.dump(data, json_file, indent=4, sort_keys=True)

    data_dict = {}

    with open(json_path) as json_file:
        data_dict = json.loads(json_file.read())
        if verbose:
            logger.info('Loaded data from JSON successfully : {}'.format(json_path))

    return data_dict


def prepare_OIIO():

    _SVN_OIIO_PATH = "C:/vsTools2/library/python_module/OpenImageIO-1.6.18"
    _OIIO_PACKAGE = 'python_module/OpenImageIO-1.6.18'
    succeed = 1

    if not Path(_SVN_OIIO_PATH).exists():
        try:
            import svn.library
            svn.library.addsitedir(_OIIO_PACKAGE)
        except Exception as error:
            logger.info('(!) Cannot get OpenImageIO from SVN repo due to: {}.'.format(error))
            succeed = 0
    else:
        sys.path.append(_SVN_OIIO_PATH)

    return succeed


def find_all_UDIM_textures(img_path):
    """
    :parm img_path: one Path object to find all other textures of other UDIMs
    :return: list of Path objects of those textures except that of the originally given one
    """
    _UDIM_PATTERN = r'\d\d\d\d'
    _GLOB_PATTERN = '*'

    folder_path = img_path.parent
    img_name = img_path.name  # Shell_1001_clr.tif
    # img_stem = img_path.stem  # Shell_1001_clr
    # img_ext = img_path.suffix  # .tif

    udim_num = re.findall(_UDIM_PATTERN, img_name)[0]  # just gets the first one
    prefix, suffix = img_name.split(udim_num)  # 'Shell_', '_clr.tif'

    all_udims = list(folder_path.glob(prefix + _GLOB_PATTERN + suffix))  # list of WindowsPath objects

    if img_path in all_udims:
        all_udims.remove(img_path)

    all_udim_names = [udim.stem for udim in all_udims]
    logger.info('Found these additional UDIMs to be processed: {}.'.format(all_udim_names))

    return all_udims


def oiio_resize_image(orig_path, output_folder=None, factor=2, extension='.jpg'):
    """
    :parm orig_path: Path object of original image
    :parm output_folder: Path object of custom output folder, or None
    :return: succeed, Path object of output image
    """
    succeed = 1

    orig_img_stem = orig_path.stem

    import OpenImageIO as oiio

    orig_img_buf = oiio.ImageBuf(orig_path.as_posix())  # ImageBuf object
    orig_img_spec = orig_img_buf.spec()  # ImageSpec object

    resized_img_spec = oiio.ImageSpec(orig_img_spec.width / factor, orig_img_spec.height / factor, 3, orig_img_spec.format)
    resized_img_buf = oiio.ImageBuf(resized_img_spec)

    oiio.ImageBufAlgo.resize(resized_img_buf, orig_img_buf)

    if not output_folder:
        output_path = orig_path.with_name(orig_img_stem + extension)
        # logger.info('Output path: {}'.format(output_path))
    else:
        output_path = output_folder / (orig_img_stem + extension)

    try:
        resized_img_buf.write(output_path.as_posix())
    except Exception as error:
        logger.warning('(!) Cannot resize image due to: {}'.format(error))
        succeed = 0
    else:
        logger.info('Resized image {} successfully.'.format(orig_img_stem))

    return succeed, output_path


def get_dagnode(mesh):
    sel = om2.MSelectionList()
    sel.add(mesh)
    return om2.MFnDagNode(sel.getDagPath(0))


def intersections_exist(dagnodes):
    bounds = [dagnode.boundingBox for dagnode in dagnodes]

    while bounds:
        a = bounds.pop()
        for b in bounds:
            if a.intersects(b):
                return True

    return False


def intersects_with(a, dagnodes):
    abounds = a.boundingBox
    for dagnode in dagnodes:
        if a == dagnode:
            continue

        if abounds.intersects(dagnode.boundingBox):
            return True

    return False


def explode_meshes(meshes, origin=None, factor=None, iterations=-1):
    origin = origin or om2.MVector(0, 0, 0)
    factor = factor or om2.MVector(1, 1, 1)
    dagnodes = [get_dagnode(mesh) for mesh in meshes]
    vectors = []
    for dagnode in dagnodes:
        v = om2.MVector(dagnode.boundingBox.center - origin)
        v = om2.MVector(*[a * b for a, b in zip(v, factor)])
        vectors.append(v)

    i = 0
    while intersections_exist(dagnodes):

        if iterations > 0 and i > iterations:
            break
        for mesh, dagnode, vector in zip(meshes, dagnodes, vectors):
            if not intersects_with(dagnode, list(dagnodes)):
                continue
            cmds.xform(mesh, ws=True, relative=True, translation=vector)

        cmds.refresh()
        time.sleep(0.01)
        i += 1

    return True


def run_explode_meshes():

    if __name__ == "util":
        cmds.undoInfo(openChunk=True)
        explode_meshes(cmds.ls(sl=True),
                       factor=om2.MVector(1, 0.01, 1),
                       iterations=1000)
        cmds.undoInfo(closeChunk=True)

    return True


def get_node(mesh):

    sel = om2.MSelectionList()
    sel.add(mesh)
    return om2.MFnDagNode(sel.getDagPath(0))


def intersects_with2(a, nodes):

    bb = a.boundingBox
    for node in nodes:
        if a == node:
            continue
        if bb.intersects(node.boundingBox):
            return True
    return False


def explode_meshes2(meshes, origin=om2.MVector(0, 3, 0), factor=None):

    nodes = []
    queue = []

    for mesh in meshes:
        node = get_node(mesh)
        nodes.append(node)
        bb = node.boundingBox
        v = om2.MVector(bb.center - origin).normalize()
        v = om2.MVector(v.x * factor.x, v.y * factor.y, v.z * factor.z)
        area = bb.width * bb.height * bb.depth
        queue.append((mesh, node, v, area))

    queue = sorted(queue, key=itemgetter(3))

    while queue:
        mesh, node, vector, _ = queue.pop()
        while intersects_with2(node, nodes):
            cmds.xform(mesh, ws=True, relative=True, translation=vector)

    return True


def run_explode_meshes2(explode_factor=5):

    explode_factor_vec = om2.MVector(explode_factor, 1, explode_factor)

    if __name__ == "util":
        cmds.undoInfo(openChunk=True)
        explode_meshes2(cmds.ls(sl=True), factor=explode_factor_vec)
        cmds.undoInfo(closeChunk=True)

    return True


def install_all(current_only=False, do_modules=False, do_prefs=False, do_presets=False):
    # queries user paths

    if current_only:
        if do_presets:
            current_maya_presets_folder = os.path.join(cfg.user_maya_app_dir,
                                                       cfg.user_current_maya_version,
                                                       cfg.PRESETS)

            try:
                copy_tree(cfg.mnT2_source_presets_folder_path, current_maya_presets_folder)
            except Exception as error:
                logger.info('////Cannot copy due to: {0}...'.format(error))
            else:
                logger.info('////Copied folder "{0}" to current Maya at {1}'
                         .format(cfg.PRESETS, current_maya_presets_folder))

    else:

        user_maya_projects = [folder.rstrip("\\") for folder in glob.glob(os.path.join(cfg.user_home_path, "*/")) if
                              folder.find(cfg.MAYA) != -1]

        logger.info("Found these Maya folders: {0}".format(user_maya_projects))

        for maya_project in user_maya_projects:
            logger.info('***Found Maya project: "{0}".'.format(maya_project))
            for version in cfg.MAYA_VERSIONS:
                maya_project_version = os.path.join(maya_project, version)
                if os.path.exists(maya_project_version):
                    # logger.info("Found Maya version {0}.".format(version))

                    if do_modules:
                        maya_modules_folder = os.path.normpath(os.path.join(maya_project_version, cfg.MODULES))
                        # logger.info("Destination folder: {0}.".format(maya_modules_folder))

                        try:
                            copy_tree(cfg.mnT2_source_modules_folder_path, maya_modules_folder)
                        except Exception as error:
                            logger.info('////Cannot copy {0} for Maya version {1} within project "{2}" due to: {3}...'
                                     .format(cfg.MODULES, version, os.path.basename(maya_project), error))
                        else:
                            logger.info('////Copied folder "{0}" for Maya version {1} within project "{2}"...'
                                     .format(cfg.MODULES, version, os.path.basename(maya_project)))

                    if do_prefs:
                        maya_prefs_folder = os.path.normpath(os.path.join(maya_project_version, cfg.PREFS))
                        # logger.info("Destination folder: {0}.".format(maya_prefs_folder))

                        try:
                            copy_tree(cfg.mnT2_source_prefs_folder_path, maya_prefs_folder)
                        except Exception as error:
                            logger.info('////Cannot copy {0} for Maya version {1} within project "{2}" due to: {3}...'
                                     .format(cfg.PREFS, version, os.path.basename(maya_project), error))
                        else:
                            logger.info('////Copied folder "{0}" for Maya version {1} within project "{2}"...'
                                     .format(cfg.PREFS, version, os.path.basename(maya_project)))

                    if do_presets:
                        maya_presets_folder = os.path.normpath(os.path.join(maya_project_version, cfg.PRESETS))
                        # logger.info("Destination folder: {0}.".format(maya_presets_folder))

                        try:
                            copy_tree(cfg.mnT2_source_presets_folder_path, maya_presets_folder)
                        except Exception as error:
                            logger.info('////Cannot copy {0} for Maya version {1} within project "{2}" due to: {3}...'
                                     .format(cfg.PRESETS, version, os.path.basename(maya_project), error))
                        else:
                            logger.info('////Copied folder "{0}" for Maya version {1} within project "{2}"...'
                                     .format(cfg.PRESETS, version, os.path.basename(maya_project)))

    return True
