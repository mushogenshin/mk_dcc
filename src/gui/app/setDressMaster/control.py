import sys

is_py2 = True if sys.version_info.major < 3 else False

# if not is_py2:
#     from pathlib import Path
# else:
#     import src.utils
#     scandir = src.utils.load_scandir_from_venv()
#     pathlib2 = src.utils.load_pathlib2_from_venv()
#     import scandir
#     from pathlib2 import Path

class Control(object):
    def __init__(self):
        super(Control, self).__init__()


# import os
# import logging as logger

# import maya.cmds as cmds
# import pymel.core as pm
# import maya.OpenMayaUI as omui

# try:
#     from PySide2.QtCore import *
#     from PySide2.QtGui import *
#     from PySide2.QtWidgets import *
#     from shiboken2 import wrapInstance
# except ImportError:
#     from PySide.QtCore import *
#     from PySide.QtGui import *
#     from shiboken import wrapInstance

# unique_prefix = 'mnT2'
# MASH_PLUGIN_NAME = "MASH"

# # //vietsap002/projects/ILM/lib/scripts/miniTools2
# repo_lib_path = "//vietsap002/projects/ILM/lib"
# script_folder_name = "scripts"
# mnT2_folder_name = "miniTools2"
# mnT2_script_path = os.path.join(repo_lib_path, script_folder_name, mnT2_folder_name)

# # //vietsap002/projects/ILM/lib/scripts/miniTools2/tool_meshes
# tool_meshes_folder_name = "tool_meshes"
# tool_meshes_path = os.path.join(mnT2_script_path, tool_meshes_folder_name)

# SCENE_ENV = pm.language.Env()

# def maya_main_window():
#     main_window_ptr = omui.MQtUtil.mainWindow()
#     return wrapInstance(long(main_window_ptr), QWidget)

# class PhysXPainterDialog(QDialog):
#     """This is the class of our tool dialog"""

#     # BUTTON_LABELS = {'load_Clouds': {'EN': 'Paint meshes', 'VI': u'Mây'},
#     #                  'load_Scatters': {'EN': 'Obj to scatters', 'VI': u'Mưa'},
#     #                  'load_Grounds': {'EN': 'Ground & colliders', 'VI': u'Đất'},
#     #                  4: {'EN': '', 'VI': u''}}

#     ORIENT_NUCLEUS_NAME = "orient_nucleus"
#     BAKED_MESH_IDENTIFIER = "ReproMesh"

#     def __init__(self, parent=maya_main_window(), mnT2_dialog=None):
#         super(PhysXPainterDialog, self).__init__(parent)

#         self.setWindowTitle('PhysX Painter')
#         # self.setMinimumWidth(200)
#         # disables the question mark button in Windows
#         self.setWindowFlags(self.windowFlags() ^ Qt.WindowContextHelpButtonHint)

#         self.Clouds = None
#         self.Scatters = None
#         self.Grounds = None

#         self.Scattered_Grp = None

#         self.NUM_VERTS_N_SCATTER_NAMES = {}

#         self.php_mash_network = None
#         self.php_mash_placer = None
#         self.php_mash_bullet = None

#         self.create_widgets()
#         self.create_layouts()
#         self.create_connections()

#         # if mnT2_dialog.locale_toggle_cb.isChecked():
#         #     logger.info("LOCALE IS EN!")
#         # else:
#         #     logger.info("LOCALE IS VI!")

#     def create_widgets(self):
#         """Creates the Qt widgets"""
        
#         self.main_dialog_tabs = QTabWidget()
#         self.A_tab = QWidget()
#         self.B_tab = QWidget()

#         load_btns_label = ">>"
#         load_btns_styleSheet = "padding: 2px"

#         setup_btn_styleSheet = "color: black; background-color: rgb(104, 161, 150)"

#         execute_btn_styleSheet = "Text-align: left; padding: 1px"

#         self.clouds_le = QLineEdit()
#         self.scatters_le = QLineEdit()
#         self.grounds_le = QLineEdit()

#         self.load_clouds_btn = QPushButton(load_btns_label)
#         self.load_scatters_btn = QPushButton(load_btns_label)
#         self.load_grounds_btn = QPushButton(load_btns_label)

#         self.add_orient_nucleus_cb = QCheckBox('Inject "orient nuclei"')

#         self.setup_btn = QPushButton("*** Setup ***")
#         self.setup_btn.setStyleSheet(setup_btn_styleSheet)

#         self.play_pause_btn = QPushButton()
#         self.play_pause_btn.setIcon(QIcon(":play_S.png"))
#         self.play_pause_btn.setStyleSheet("padding: 2px; background-color: rgb(165, 102, 111)")

#         self.reset_btn = QPushButton("zero")
#         self.reset_btn.setIcon(QIcon(":out_time.png"))  # out_timeEditor
#         self.reset_btn.setStyleSheet(execute_btn_styleSheet)

#         self.select_paint_node_btn = QPushButton("Paint node")
#         self.select_paint_node_btn.setStyleSheet("Text-align: left")
#         self.select_paint_node_btn.setIcon(QIcon(":paintVertexColour.png"))  # paintSetMembership
#         # art3dPaint, selectPaint, makePaintable, artPaintSelect, toonPaintWidth, paintJiggle

#         self.delete_setup_btn = QPushButton("Del all")
#         self.delete_setup_btn.setIcon(QIcon(":deleteGeneric.png"))
#         self.delete_setup_btn.setStyleSheet("Text-align: left; padding: 1px; background-color: rgb(165, 102, 111)")

#         self.bake_current_btn = QPushButton("Bake current")

#         # TAB A: SET INIT
#         self.add_orient_nucleus_cb.setChecked(True)

#         # STYLESHEETS & TOOLTIPS

#         self.load_clouds_btn.setStyleSheet(load_btns_styleSheet)
#         self.load_scatters_btn.setStyleSheet(load_btns_styleSheet)
#         self.load_grounds_btn.setStyleSheet(load_btns_styleSheet)

#         self.load_clouds_btn.setToolTip("Load selected as Cloud")
#         self.load_scatters_btn.setToolTip("Load selected as objs to scatter")
#         self.load_grounds_btn.setToolTip("Load selected as Ground")

#         # TAB B WIDGETS

#         self.edit_paint_meshes_grp_box = QGroupBox("Edit Clouds")
#         self.edit_scattered_grp_box = QGroupBox("Edit Scattered")
#         self.edit_colliders_grp_box = QGroupBox("Edit Grounds")

#         self.add_as_paint_mesh_btn = QPushButton("Add")
#         self.remove_as_paint_mesh_btn = QPushButton("Remove")

#         self.restore_scattered_xforms_btn = QPushButton("Restore Scattered's Transforms")

#         self.add_as_collider_btn = QPushButton("Add")
#         self.remove_as_collider_btn = QPushButton("Remove")

#     def create_layouts(self):
#         """Creates the Qt layouts"""

#         F_spacing = 3
#         VB_margin = 2
#         VB_spacing = 3

#         # TAB A LAYOUT

#         A_main_layout = QVBoxLayout()
#         A_main_layout.setContentsMargins(VB_margin, VB_margin, VB_margin, VB_margin)
#         A_main_layout.setSpacing(VB_spacing)

#         load_clouds_row_lo = QHBoxLayout()
#         load_clouds_row_lo.addWidget(self.clouds_le)
#         load_clouds_row_lo.addWidget(self.load_clouds_btn)

#         load_scatters_row_lo = QHBoxLayout()
#         load_scatters_row_lo.addWidget(self.scatters_le)
#         load_scatters_row_lo.addWidget(self.load_scatters_btn)

#         load_grounds_row_lo = QHBoxLayout()
#         load_grounds_row_lo.addWidget(self.grounds_le)
#         load_grounds_row_lo.addWidget(self.load_grounds_btn)

#         common_load_form_lo = QFormLayout()
#         common_load_form_lo.setSpacing(F_spacing)
#         common_load_form_lo.addRow('Clouds:', load_clouds_row_lo)
#         common_load_form_lo.addRow('Scatters:', load_scatters_row_lo)
#         common_load_form_lo.addRow('Grounds:', load_grounds_row_lo)
#         common_load_form_lo.addRow("", self.add_orient_nucleus_cb)

#         play_row_lo = QHBoxLayout()
#         play_row_lo.addWidget(self.reset_btn)
#         play_row_lo.addStretch()
#         play_row_lo.addWidget(self.select_paint_node_btn)
#         play_row_lo.addWidget(self.play_pause_btn)

#         bake_row_lo = QHBoxLayout()
#         bake_row_lo.addWidget(self.delete_setup_btn)
#         bake_row_lo.addStretch()
#         bake_row_lo.addWidget(self.bake_current_btn)

#         A_main_layout.addLayout(common_load_form_lo)
#         A_main_layout.addWidget(self.setup_btn)
#         A_main_layout.addLayout(play_row_lo)
#         A_main_layout.addLayout(bake_row_lo)

#         self.A_tab.setLayout(A_main_layout)

#         # TAB B LAYOUT

#         B_main_layout = QVBoxLayout()
#         B_main_layout.setContentsMargins(VB_margin, VB_margin, VB_margin, VB_margin)
#         B_main_layout.setSpacing(VB_spacing)

#         edit_paint_meshes_row_lo = QHBoxLayout()
#         edit_paint_meshes_row_lo.addWidget(self.add_as_paint_mesh_btn)
#         edit_paint_meshes_row_lo.addWidget(self.remove_as_paint_mesh_btn)

#         edit_scattered_row_lo = QHBoxLayout()
#         edit_scattered_row_lo.addWidget(self.restore_scattered_xforms_btn)

#         edit_colliders_row_lo = QHBoxLayout()
#         edit_colliders_row_lo.addWidget(self.add_as_collider_btn)
#         edit_colliders_row_lo.addWidget(self.remove_as_collider_btn)

#         self.edit_paint_meshes_grp_box.setLayout(edit_paint_meshes_row_lo)
#         self.edit_scattered_grp_box.setLayout(edit_scattered_row_lo)
#         self.edit_colliders_grp_box.setLayout(edit_colliders_row_lo)

#         # B_main_layout.addWidget(self.edit_paint_meshes_grp_box)
#         B_main_layout.addWidget(self.edit_scattered_grp_box)
#         # B_main_layout.addWidget(self.edit_colliders_grp_box)

#         self.B_tab.setLayout(B_main_layout)

#         # MASTER LAYOUT

#         self.tabA_index = self.main_dialog_tabs.addTab(self.A_tab, "Create")
#         self.tabB_index = self.main_dialog_tabs.addTab(self.B_tab, "Edit")
#         self.main_dialog_tabs.setCurrentIndex(self.tabA_index)

#         master_layout = QVBoxLayout(self)
#         master_layout.setContentsMargins(0, 0, 0, 0)
#         master_layout.setSpacing(VB_spacing)

#         master_layout.addWidget(self.main_dialog_tabs)

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

        check_n_load_plugin(MASH_PLUGIN_NAME)

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
                self.php_mash_network.createNetwork(name="_".join([unique_prefix, MASH_PLUGIN_NAME]))
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

        orient_nucleus_file_name = "_".join([unique_prefix,
                                             PhysXPainterDialog.ORIENT_NUCLEUS_NAME,
                                             "geo.obj"])  # "mnT2_orient_nucleus_geo.obj"
        orient_nucleus_file_path = os.path.join(tool_meshes_path, orient_nucleus_file_name)

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
            mash_waiters = [waiter for waiter in pm.ls(typ='MASH_Waiter') if waiter.nodeName().find(unique_prefix) != -1]

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
            pm.duplicate(php_mash_repro_mesh, n="_".join([unique_prefix, "baked",
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
                self.Scattered_Grp = pm.group(em=True, n="_".join([unique_prefix,
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

PhysXPainterDialog_showUI()
