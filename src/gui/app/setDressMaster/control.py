import sys

from src.utils.maya import ui_utils, plugin_utils

is_py2 = True if sys.version_info.major < 3 else False

# if not is_py2:
#     from pathlib import Path
# else:
#     import src.utils
#     scandir = src.utils.load_scandir_from_venv()
#     pathlib2 = src.utils.load_pathlib2_from_venv()
#     import scandir
#     from pathlib2 import Path

MASH_PLUGIN_NAME = "MASH"


class Control(object):
    def __init__(self):
        super(Control, self).__init__()

    def setup_physx_painter(self):

        plugin_utils.safe_load_plugin(MASH_PLUGIN_NAME)

        import MASH.api as mapi

        # Check cloud_meshes
        # Check ground_meshes

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
                pmc.select(scatter_objs_processed, r=True)

                # initiates a MASH network
                self.mash_network = mapi.Network()
                self.mash_network.createNetwork(name="_".join([unique_prefix, MASH_PLUGIN_NAME]))
                logger.info("MASH network created: {0}.".format(self.mash_network.waiter))

                # accesses the default Distribute node
                php_mash_dist = pmc.PyNode(self.mash_network.distribute)
                php_mash_dist.pointCount.set(0)  # disables this distribute node

                # accesses the default Repro node
                # php_mash_repro = pmc.PyNode(self.mash_network.instancer)

                # adds a Placer node
                self.mash_placer = self.mash_network.addNode("MASH_Placer")
                logger.info("MASH Placer node added: {0}.".format(self.mash_placer.name))

                self.mash_placer = pmc.PyNode(self.mash_placer.name)
                self.mash_placer.scatter.set(True)
                self.mash_placer.idMode.set(2)  # sets it to "Random"
                self.mash_placer.randomId1.set(num_instances - 1)  # array index
                #  TODO: elaborate this with large/small objs

                if cloud_paint_meshes:
                    # connects the Clouds to the Placer's paint meshes
                    for i, cloud in enumerate(cloud_paint_meshes):
                        cloud.worldMesh[0].connect(self.mash_placer.paintMeshes[i])
                        logger.info("{0} added as a paint mesh for {1}.".format(cloud.nodeName(),
                                                                             self.mash_placer.nodeName()))

                # adds a Dynamics node
                php_mash_dyn = self.mash_network.addNode("MASH_Dynamics")
                logger.info("MASH Dynamics node added: {0}.".format(php_mash_dyn.name))

                php_mash_dyn = pmc.PyNode(php_mash_dyn.name)

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
                self.mash_bullet = pmc.PyNode(self.mash_network.getSolver())
                logger.info("Bullet Solver automatically created: {0}.".format(self.mash_bullet.nodeName()))

                if not ground_collide_meshes:
                    self.mash_bullet.groundPlanePositionY.set(0)  # overrides the default value of -20
                else:
                    self.mash_bullet.groundPlane.set(False)  # disables the Bullet's built-in ground
                    # loads the Grounds to the Bullet Solver's colliders
                    for collider in ground_collide_meshes:
                        self.mash_network.addCollider(collider.nodeName())
                        logger.info("{0} added as a collider in {1}.".format(collider.nodeName(),
                                                                          self.mash_bullet.nodeName()))

                # increases the time range; go to first frame
                extend_time_range(0, 3000, 0)

                # raises the MASH Outliner
                pmc.mel.MASHOutliner()

                # selects the Placer node
                self.select_paint_node()

        else:
            logger.info("No valid object to scatter. Please load at least one polygonal mesh.")
            return False

        return True


#         self.Clouds = None
#         self.Scatters = None
#         self.Grounds = None

#         self.painted_and_baked_grp = None

#         self.NUM_VERTS_N_SCATTER_NAMES = {}

#         self.mash_network = None
#         self.mash_placer = None
#         self.mash_bullet = None


#     def setup_physx_painter(self):

#         safe_load_plugin(MASH_PLUGIN_NAME)

#         import MASH.api as mapi

#         if self.Clouds:
#             # gets the Clouds' shapes
#             cloud_paint_meshes = [cloud.getShape() for cloud in self.Clouds if type(cloud.getShape()) == pmc.nt.Mesh]
#             logger.info("Paint mesh(es) found: {0}".format(str(cloud_paint_meshes)))
#         else:
#             cloud_paint_meshes = None
#             logger.info("No paint mesh found.")

#         if self.Grounds:
#             # gets the Grounds' shapes
#             ground_collide_meshes = [ground.getShape() for ground in self.Grounds
#                                      if type(ground.getShape()) == pmc.nt.Mesh]
#             logger.info("Ground & collider mesh(es) found: {0}".format(str(ground_collide_meshes)))
#         else:
#             ground_collide_meshes = None
#             logger.info("No ground nor collider found.")

#         self.Scatters, num_instances = self.filter_polygonal_scatters()

#         try:
#             self.log_num_verts_n_scatter_names(self.Scatters)
#         except:
#             logger.info("Numbers of vertices of the Scatters are not unique.")
#             pass
        
#         if self.Scatters:
#             if self.add_orient_nucleus_cb.isChecked():
#                 scatter_objs_processed = self.inject_orient_nucleus_foreach_scatter()
#             else:
#                 scatter_objs_processed = self.Scatters

#             if scatter_objs_processed:
#                 # selects only the objects to scatter
#                 pmc.select(scatter_objs_processed, r=True)

#                 # initiates a MASH network
#                 self.mash_network = mapi.Network()
#                 self.mash_network.createNetwork(name="_".join([unique_prefix, MASH_PLUGIN_NAME]))
#                 logger.info("MASH network created: {0}.".format(self.mash_network.waiter))

#                 # accesses the default Distribute node
#                 php_mash_dist = pmc.PyNode(self.mash_network.distribute)
#                 php_mash_dist.pointCount.set(0)  # disables this distribute node

#                 # accesses the default Repro node
#                 # php_mash_repro = pmc.PyNode(self.mash_network.instancer)

#                 # adds a Placer node
#                 self.mash_placer = self.mash_network.addNode("MASH_Placer")
#                 logger.info("MASH Placer node added: {0}.".format(self.mash_placer.name))

#                 self.mash_placer = pmc.PyNode(self.mash_placer.name)
#                 self.mash_placer.scatter.set(True)
#                 self.mash_placer.idMode.set(2)  # sets it to "Random"
#                 self.mash_placer.randomId1.set(num_instances - 1)  # array index
#                 #  TODO: elaborate this with large/small objs

#                 if cloud_paint_meshes:
#                     # connects the Clouds to the Placer's paint meshes
#                     for i, cloud in enumerate(cloud_paint_meshes):
#                         cloud.worldMesh[0].connect(self.mash_placer.paintMeshes[i])
#                         logger.info("{0} added as a paint mesh for {1}.".format(cloud.nodeName(),
#                                                                              self.mash_placer.nodeName()))

#                 # adds a Dynamics node
#                 php_mash_dyn = self.mash_network.addNode("MASH_Dynamics")
#                 logger.info("MASH Dynamics node added: {0}.".format(php_mash_dyn.name))

#                 php_mash_dyn = pmc.PyNode(php_mash_dyn.name)

#                 php_mash_dyn.collisionShape.set(4)  # sets it to "Convex Hull"

#                 # dynamics parameters
#                 dyn_friction = 0.4  # 0.3
#                 dyn_rolling_friction = 0.4  # 0.2
#                 dyn_damping = 0.3  # 0.1
#                 dyn_rolling_damping = 0.1  # 0.02
#                 dyn_bounce = 0.02  # 0.05
#                 dyn_collision_jitter = 0.005

#                 # TODO: tweak the Dynamics parameters
#                 php_mash_dyn.friction.set(dyn_friction)
#                 php_mash_dyn.rollingFriction.set(dyn_rolling_friction)
#                 php_mash_dyn.damping.set(dyn_damping)
#                 php_mash_dyn.rollingDamping.set(dyn_rolling_damping)
#                 php_mash_dyn.bounce.set(dyn_bounce)
#                 php_mash_dyn.collisionJitter.set(dyn_collision_jitter)

#                 # accesses the Bullet Solver
#                 self.mash_bullet = pmc.PyNode(self.mash_network.getSolver())
#                 logger.info("Bullet Solver automatically created: {0}.".format(self.mash_bullet.nodeName()))

#                 if not ground_collide_meshes:
#                     self.mash_bullet.groundPlanePositionY.set(0)  # overrides the default value of -20
#                 else:
#                     self.mash_bullet.groundPlane.set(False)  # disables the Bullet's built-in ground
#                     # loads the Grounds to the Bullet Solver's colliders
#                     for collider in ground_collide_meshes:
#                         self.mash_network.addCollider(collider.nodeName())
#                         logger.info("{0} added as a collider in {1}.".format(collider.nodeName(),
#                                                                           self.mash_bullet.nodeName()))

#                 # increases the time range; go to first frame
#                 extend_time_range(0, 3000, 0)

#                 # raises the MASH Outliner
#                 pmc.mel.MASHOutliner()

#                 # selects the Placer node
#                 self.select_paint_node()

#         else:
#             logger.info("No valid object to scatter. Please load at least one polygonal mesh.")
#             return False

#         return True


#     def select_paint_node(self):
#         if self.mash_placer:
#             pmc.select(self.mash_placer, r=True)
#             pmc.mel.AttributeEditor()  # raises the Attribute Editor
#             pmc.mel.updateAE(self.mash_placer)  # updates it
#             logger.info("Paint node {0} selected.".format(self.mash_placer.nodeName()))
#             logger.info('Click "Play" and then click "Add" to start painting.')

#         return True

#     def delete_setup(self):
#         success = "Custom MASH network removed."

#         if self.mash_network:
#             pmc.delete(self.mash_network.waiter)
#             logger.info(success)
#         else:
#             mash_waiters = [waiter for waiter in pmc.ls(typ='MASH_Waiter') if waiter.nodeName().find(unique_prefix) != -1]

#             if mash_waiters:
#                 pmc.delete(mash_waiters)
#                 logger.info(success)
#             else:
#                 logger.info("No custom MASH network found.")

#         # resets the variables

#         self.mash_network = None
#         self.mash_placer = None
#         self.mash_bullet = None

#         pmc.select(cl=True)  # clear the selection

#         self.load_clouds()  # resets self.Clouds
#         self.load_scatters()  # resets self.Scatters
#         self.load_grounds()  # resets self.Grounds

#         return True

#     def do_bake_current(self):

#         is_playing = cmds.play(q=True, st=True)

#         if is_playing:
#             cmds.play(st=0)  # pauses the playback

#         if self.mash_network:
#             # gets the Repro
#             php_mash_repro = pmc.PyNode(self.mash_network.instancer)
#             php_mash_repro_mesh = php_mash_repro.outMesh.outputs()[0]  # gets the Repro mesh
#             pmc.duplicate(php_mash_repro_mesh, n="_".join([unique_prefix, "baked",
#                                                           "f" + str(int(SCENE_ENV.time)),
#                                                           PhysXPainterDialog.BAKED_MESH_IDENTIFIER]))

#         if is_playing:
#             pmc.mel.InteractivePlayback()  # resumes the playback

#         return True

#     def add_selected_as_paint_mesh(self):
#         pass

#     def remove_selected_as_paint_mesh(self):
#         pass

#     def add_selected_as_collider(self):
#         if self.mash_network:

#             collider_meshes = [collider.getShape() for collider in pmc.ls(sl=True) if
#                                type(collider.getShape()) == pmc.nt.Mesh]

#             for collider in collider_meshes:
#                 self.mash_network.addCollider(collider.nodeName())
#                 logger.info("{0} added as a collider in {1}.".format(collider.nodeName(), self.mash_bullet.nodeName()))

#         return True

#     def remove_selected_as_collider(self):
#         pass


# def extend_time_range(range_min=0, range_max=1000, f=0, force=False):
#     # checks and sets Min & Max time
#     if not force:
#         if SCENE_ENV.getMinTime() > range_min:
#             SCENE_ENV.setMinTime(range_min)
#         if SCENE_ENV.getMaxTime() < range_max:
#             SCENE_ENV.setMaxTime(range_max)
#     else:
#         SCENE_ENV.setMinTime(range_min)
#         SCENE_ENV.setMaxTime(range_max)

#     # then sets the time
#     SCENE_ENV.setTime(f)

# PhysXPainterDialog_showUI()
