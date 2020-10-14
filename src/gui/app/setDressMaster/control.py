import sys
import logging

from src.utils.maya import (
    plugin_utils, 
    node_utils, 
    ui_utils, 
    scene_utils,
    selection_utils,
    attrib_utils
)

logger = logging.getLogger(__name__)
is_py2 = True if sys.version_info.major < 3 else False

MASH_PLUGIN_NAME = "MASH"
MASH_NETWORK_NAME = "SDM_MASH_Network"
MASH_PLACER = "MASH_Placer"
MASH_DYNAMICS = "MASH_Dynamics"
TIME_RANGE = 3000


def load_mash_api():
    try:
        import MASH.api
    except ImportError:
        logger.warning("Unable to import MASH.api")
        return None
    else:
        return MASH.api


class Control(object):
    def __init__(self):
        super(Control, self).__init__()
        self.SCENE_ENV = scene_utils.get_scene_env()

    def get_init_data(self, app_model_data_key):
        return self._model._data["init"][app_model_data_key]

    def set_init_data(self, app_model_data_key, value):
        self._model._data["init"][app_model_data_key] = value

    def get_mash_data(self, app_model_data_key):
        return self._model._data["mash"][app_model_data_key]

    def set_mash_data(self, app_model_data_key, value):
        self._model._data["mash"][app_model_data_key] = value

    def get_baked_data(self):
        return self._model._data["baked"]

    def set_baked_data(self, frame, mesh):
        if frame in self._model._data["baked"]:
            self._model._data["baked"][frame].append(mesh)
        else:
            self._model._data["baked"][frame] = [mesh]


    def create_mash_network(self, mapi):
        """
        Initialize a MASH Network
        """
        logger.info("Constructing MASH Network {}".format(MASH_NETWORK_NAME))
        waiter = distribute = repro = None
        scatter_meshes = self.get_init_data("scatter_meshes")

        network = self.get_mash_data("mash_network")
        if not network and hasattr(mapi, "Network"):
            # Scatter Meshes must be being selected prior to MASH Network creation
            selection_utils.replace_selection(scatter_meshes)

            network = mapi.Network()  
            self.set_mash_data("mash_network", network)  # MASH.api.Network instance, not PyNode

            if hasattr(network, "createNetwork") and \
                not node_utils.node_exists(MASH_NETWORK_NAME):  # force Singleton
                network.createNetwork(name=MASH_NETWORK_NAME)

        if hasattr(network, "__dict__"):
            waiter = network.__dict__.get("waiter")
            distribute = network.__dict__.get("distribute")
            repro = network.__dict__.get("instancer")

        self.set_mash_data("mash_waiter", node_utils.get_PyNode(waiter))
        self.set_mash_data("mash_distribute", node_utils.get_PyNode(distribute))
        self.set_mash_data("mash_repro", node_utils.get_PyNode(repro))

    def disable_distribute_node(self):
        logger.info("Disabling MASH Distribute of {}".format(MASH_NETWORK_NAME))
        distribute_node = self.get_mash_data("mash_distribute")
        if hasattr(distribute_node, "pointCount"):
            distribute_node.pointCount.set(0)

    def add_generic_node(self, node_type, app_model_data_key):
        logger.info("Adding node {} to {}".format(node_type, MASH_NETWORK_NAME))
        network = self.get_mash_data("mash_network")
        if hasattr(network, "addNode"):
            node = network.addNode(node_type)  # not PyNode
            self.set_mash_data(app_model_data_key, node_utils.get_PyNode(node.name))
            logger.info("--Added to MASH network: {}".format(node))
            logger.info("--Added to MASH data: {}".format(self.get_mash_data(app_model_data_key)))

    def config_placer_node(self):
        logger.info("Configuring MASH Placer of {}".format(MASH_NETWORK_NAME))
        placer = self.get_mash_data("mash_placer")
        if hasattr(placer, "scatter"):
            placer.scatter.set(True)
        if hasattr(placer, "idMode"):
            placer.idMode.set(2)  # set it to "Random"
        if hasattr(placer, "randomId1"):
            num_instances = len(self.get_init_data("scatter_meshes"))
            placer.randomId1.set(max(num_instances - 1, 0))  # array index
        # TODO: support for large/small objs

    def config_dynamics_node(self, dynamics_parameters):
        """
        :param dict dynamics_parameters: e.g.
            {
                "friction" = 0.4
                "rollingFriction" = 0.4
                "damping" = 0.3
                "rollingDamping" = 0.1
                "bounce" = 0.02
                "collisionJitter" = 0.005
            }
        """
        logger.info("Configuring MASH Dynamics of {}".format(MASH_NETWORK_NAME))
        dynamics = self.get_mash_data("mash_dynamics")

        if hasattr(dynamics, "collisionShape"):
            dynamics.collisionShape.set(4)  # set it to "Convex Hull"

        for attr, v in dynamics_parameters.items():
            if hasattr(dynamics, attr):
                attrib_utils.set_attrib(dynamics, attr, v)

    def add_paint_meshes(self):
        logger.info("Connecting Paint Meshes to MASH Placer of {}".format(MASH_NETWORK_NAME))
        cloud_meshes = self.get_init_data("cloud_meshes")
        placer = self.get_mash_data("mash_placer")

        for i, cloud_mesh in enumerate(cloud_meshes):
            if hasattr(cloud_mesh, "worldMesh") and hasattr(placer, "paintMeshes"):
                logger.info("Connecting Paint Mesh {}".format(cloud_mesh))
                cloud_mesh.worldMesh[0].connect(placer.paintMeshes[i])

    def get_bullet_solver(self):
        logger.info("Getting Bullet Solver of {}".format(MASH_NETWORK_NAME))
        network = self.get_mash_data("mash_network")
        bullet_solver = None
        if hasattr(network, "getSolver"):
            bullet_solver = network.getSolver()  # not PyNode
        self.set_mash_data("mash_bullet", node_utils.get_PyNode(bullet_solver))
        logger.info("Using Bullet Solver: {}".format(self.get_mash_data("mash_bullet")))

    def add_ground_meshes(self):
        ground_meshes = self.get_init_data("ground_meshes")
        bullet_solver = self.get_mash_data("mash_bullet")
        if not ground_meshes and hasattr(bullet_solver, "groundPlanePositionY"):
            logger.info("Configuring Ground Plane of Bullet Solver")
            bullet_solver.groundPlanePositionY.set(0)  # override the default value of -20
        elif hasattr(bullet_solver, "groundPlane"):
            logger.info("Connecting Ground Meshes as Colliders of {}".format(MASH_NETWORK_NAME))
            bullet_solver.groundPlane.set(False)  # disable the Bullet Solver's built-in ground
            
            # Load the Ground Meshes to the Bullet Solver's colliders
            network = self.get_mash_data("mash_network")
            if hasattr(network, "addCollider"):
                for ground_mesh in ground_meshes:
                    logger.info("Adding Collider {}".format(ground_mesh))
                    network.addCollider(node_utils.get_node_name(ground_mesh))

    def prepare_time_range(self):
        scene_utils.set_playback_range(0, TIME_RANGE, self.SCENE_ENV)
        scene_utils.reset_playback(self.SCENE_ENV)

    def focus_to_placer_node(self):
        placer = self.get_mash_data("mash_placer")
        ui_utils.raise_attribute_editor(placer)
        # TODO: show below message as UI prompt
        logger.info('Start "Interactive Playback" then click "Add" to start painting.')

    def print_model_data(self):
        logger.info("Updated Model Data: {}".format(self._model._data))

    def setup_physx_painter(self, dynamics_parameters={}):
        logger.info("Setting up PhysX Painter")
        mash_plugin_loaded = plugin_utils.safe_load_plugin(MASH_PLUGIN_NAME)
        mapi = load_mash_api()
        
        # TODO: Check cloud_meshes
        # TODO: Check scatter_meshes

        # Load mash_network and register related nodes to model data
        self.create_mash_network(mapi)
        self.print_model_data()

        self.disable_distribute_node()

        # Placer node
        self.add_generic_node(MASH_PLACER, "mash_placer")
        self.config_placer_node()
        # Paint meshes
        self.add_paint_meshes()

        # Dynamics node
        self.add_generic_node(MASH_DYNAMICS, "mash_dynamics")
        self.config_dynamics_node(dynamics_parameters)

        # Bullet Solver
        self.get_bullet_solver()
        # Ground meshes
        self.add_ground_meshes()

        # Allow for painting
        self.prepare_time_range()
        ui_utils.raise_mash_outliner()
        self.focus_to_placer_node()

        self.print_model_data()

    def delete_setup(self):
        logger.info("Deleting all setup related to {}".format(MASH_NETWORK_NAME))
        for data_key, node in self._model._data["mash"].items():
            if data_key != "mash_network":
                node_utils.delete(node)
            else:
                scene_utils.delete(MASH_NETWORK_NAME)
                scene_utils.delete(MASH_NETWORK_NAME)  # delete twice due to Maya|MASH bug

        # Reset MASH model data
        self._model.init_mash_data()

        # There are two more nodes left to delete
        scene_utils.delete("{}_Distribute".format(MASH_NETWORK_NAME))
        scene_utils.delete("{}_ID".format(MASH_NETWORK_NAME))

        self.print_model_data()

    def bake_current(self):
        was_playback_running = scene_utils.is_playback_running()
        scene_utils.toggle_interactive_playback(force_pause=True)  # pause the playback
        
        current_frame = scene_utils.get_current_frame(self.SCENE_ENV)
        logger.info("Baking from frame {}".format(current_frame))
        repro = self.get_mash_data("mash_repro")

        if repro and hasattr(repro, "outMesh"):
            repro_mesh = repro.outMesh.outputs()[0]   # get the Repro mesh
            duplicated = node_utils.duplicate(
                repro_mesh, 
                name="{}_baked_f{}".format(
                    node_utils.get_node_name(repro_mesh),
                    current_frame
                )   
            )
            # Add to Model Data
            self.set_baked_data(current_frame, duplicated)

        if was_playback_running:
            scene_utils.toggle_interactive_playback(force_play=True)  # resume the playback

    def show_all_baked(self):
        logger.info("Showing all baked meshes from {}".format(MASH_NETWORK_NAME))
        baked_meshes = []
        baked_data = self.get_baked_data()
        for frame, meshes in baked_data.items():
            baked_meshes.extend(meshes)
        if baked_meshes:
            selection_utils.replace_selection(baked_meshes)

    def focus_to_instancer_node(self):
        logger.info("Showing Instancer node of {}".format(MASH_NETWORK_NAME))
        repro = self.get_mash_data("mash_repro")
        if repro:
            selection_utils.replace_selection(repro)
            ui_utils.raise_attribute_editor(repro)
