import sys
from copy import deepcopy
import logging

from src.utils.maya import (
    plugin_utils, 
    node_utils, 
    ui_utils, 
    scene_utils,
    selection_utils,
    attrib_utils,
    transform_utils,
    mesh_utils
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

    ############################# PHYSX PAINTER #############################

    def get_PP_init_data(self, app_model_data_key):
        return self._model._data["PP_init"][app_model_data_key]

    # def set_init_data(self, app_model_data_key, value):
    #     self._model._data["PP_init"][app_model_data_key] = value

    def get_PP_mash_data(self, app_model_data_key):
        return self._model._data["PP_mash"][app_model_data_key]

    def set_PP_mash_data(self, app_model_data_key, value):
        self._model._data["PP_mash"][app_model_data_key] = value

    def get_PP_baked_data(self):
        return self._model._data["PP_baked"]

    def set_PP_baked_data(self, frame, meshes):
        """
        :param list meshes:
        """
        if frame in self._model._data["PP_baked"]:
            self._model._data["PP_baked"][frame].extend(meshes)
        else:
            self._model._data["PP_baked"][frame] = meshes


    def create_mash_network(self, mapi):
        """
        Initialize a MASH Network
        """
        logger.info("Constructing MASH Network {}".format(MASH_NETWORK_NAME))
        waiter = distribute = repro = None
        scatter_meshes = self.get_PP_init_data("scatter_meshes")

        network = self.get_PP_mash_data("mash_network")
        if not network and hasattr(mapi, "Network"):
            # Scatter Meshes must be being selected prior to MASH Network creation
            selection_utils.replace_selection(scatter_meshes)

            network = mapi.Network()  
            self.set_PP_mash_data("mash_network", network)  # MASH.api.Network instance, not PyNode

            if hasattr(network, "createNetwork") and \
                not node_utils.node_exists(MASH_NETWORK_NAME):  # force Singleton
                network.createNetwork(name=MASH_NETWORK_NAME)

        if hasattr(network, "__dict__"):
            waiter = network.__dict__.get("waiter")
            distribute = network.__dict__.get("distribute")
            repro = network.__dict__.get("instancer")

        self.set_PP_mash_data("mash_waiter", node_utils.get_PyNode(waiter))
        self.set_PP_mash_data("mash_distribute", node_utils.get_PyNode(distribute))
        self.set_PP_mash_data("mash_repro", node_utils.get_PyNode(repro))

    def disable_distribute_node(self):
        logger.info("Disabling MASH Distribute of {}".format(MASH_NETWORK_NAME))
        distribute_node = self.get_PP_mash_data("mash_distribute")
        if hasattr(distribute_node, "pointCount"):
            distribute_node.pointCount.set(0)

    def add_generic_mash_node(self, node_type, app_model_data_key):
        logger.info("Adding node {} to {}".format(node_type, MASH_NETWORK_NAME))
        network = self.get_PP_mash_data("mash_network")
        if hasattr(network, "addNode"):
            node = network.addNode(node_type)  # not PyNode
            self.set_PP_mash_data(app_model_data_key, node_utils.get_PyNode(node.name))
            logger.info("--Added to MASH network: {}".format(node))
            logger.info("--Added to MASH data: {}".format(self.get_PP_mash_data(app_model_data_key)))

    def config_placer_node(self):
        logger.info("Configuring MASH Placer of {}".format(MASH_NETWORK_NAME))
        placer = self.get_PP_mash_data("mash_placer")
        if hasattr(placer, "scatter"):
            placer.scatter.set(True)
        if hasattr(placer, "idMode"):
            placer.idMode.set(2)  # set it to "Random"
        if hasattr(placer, "randomId1"):
            num_instances = len(self.get_PP_init_data("scatter_meshes"))
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
        dynamics = self.get_PP_mash_data("mash_dynamics")

        if hasattr(dynamics, "collisionShape"):
            dynamics.collisionShape.set(4)  # set it to "Convex Hull"

        for attr, v in dynamics_parameters.items():
            if hasattr(dynamics, attr):
                attrib_utils.set_attrib(dynamics, attr, v)

    def add_paint_meshes(self):
        logger.info("Connecting Paint Meshes to MASH Placer of {}".format(MASH_NETWORK_NAME))
        cloud_meshes = self.get_PP_init_data("cloud_meshes")
        placer = self.get_PP_mash_data("mash_placer")

        for i, cloud_mesh in enumerate(cloud_meshes):
            if hasattr(cloud_mesh, "worldMesh") and hasattr(placer, "paintMeshes"):
                logger.info("Connecting Paint Mesh {}".format(cloud_mesh))
                cloud_mesh.worldMesh[0].connect(placer.paintMeshes[i])

    def get_bullet_solver(self):
        logger.info("Getting Bullet Solver of {}".format(MASH_NETWORK_NAME))
        network = self.get_PP_mash_data("mash_network")
        bullet_solver = None
        if hasattr(network, "getSolver"):
            bullet_solver = network.getSolver()  # not PyNode
        self.set_PP_mash_data("mash_bullet", node_utils.get_PyNode(bullet_solver))
        logger.info("Using Bullet Solver: {}".format(self.get_PP_mash_data("mash_bullet")))

    def add_ground_meshes(self):
        ground_meshes = self.get_PP_init_data("ground_meshes")
        bullet_solver = self.get_PP_mash_data("mash_bullet")
        if not ground_meshes and hasattr(bullet_solver, "groundPlanePositionY"):
            logger.info("Configuring Ground Plane of Bullet Solver")
            bullet_solver.groundPlanePositionY.set(0)  # override the default value of -20
        elif hasattr(bullet_solver, "groundPlane"):
            logger.info("Connecting Ground Meshes as Colliders of {}".format(MASH_NETWORK_NAME))
            bullet_solver.groundPlane.set(False)  # disable the Bullet Solver's built-in ground
            
            # Load the Ground Meshes to the Bullet Solver's colliders
            network = self.get_PP_mash_data("mash_network")
            if hasattr(network, "addCollider"):
                for ground_mesh in ground_meshes:
                    logger.info("Adding Collider {}".format(ground_mesh))
                    network.addCollider(node_utils.get_node_name(ground_mesh))

    def prepare_time_range(self):
        scene_utils.set_playback_range(0, TIME_RANGE, self.SCENE_ENV)
        scene_utils.reset_playback(self.SCENE_ENV)

    def focus_to_placer_node(self):
        placer = self.get_PP_mash_data("mash_placer")
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
        self.add_generic_mash_node(MASH_PLACER, "mash_placer")
        self.config_placer_node()
        # Paint meshes
        self.add_paint_meshes()

        # Dynamics node
        self.add_generic_mash_node(MASH_DYNAMICS, "mash_dynamics")
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

    def delete_PP_setup(self):
        logger.info("Deleting all setup related to {}".format(MASH_NETWORK_NAME))
        for data_key, node in self._model._data["PP_mash"].items():
            if data_key != "mash_network":
                node_utils.delete_one(node)
            else:
                scene_utils.delete(MASH_NETWORK_NAME)
                scene_utils.delete(MASH_NETWORK_NAME)  # delete twice due to Maya|MASH bug

        # Reset MASH model data
        self._model.init_PP_mash_data()

        # There are two more nodes left to delete
        scene_utils.delete("{}_Distribute".format(MASH_NETWORK_NAME))
        scene_utils.delete("{}_ID".format(MASH_NETWORK_NAME))

        self.print_model_data()

    def PP_bake_current(self):
        was_playback_running = scene_utils.is_playback_running()
        logger.info("Playback was running: {}".format(was_playback_running))

        scene_utils.toggle_interactive_playback(force_pause=True)  # pause the playback
        
        current_frame = scene_utils.get_current_frame(self.SCENE_ENV)
        logger.info("Baking from frame {}".format(current_frame))
        repro = self.get_PP_mash_data("mash_repro")

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
            self.set_PP_baked_data(current_frame, duplicated)

        if was_playback_running:
            scene_utils.toggle_interactive_playback(force_play=True)  # resume the playback

    def PP_show_all_baked(self):
        logger.info("Showing all baked meshes from {}".format(MASH_NETWORK_NAME))
        baked_meshes = []
        baked_data = self.get_PP_baked_data()
        for frame, meshes in baked_data.items():
            baked_meshes.extend(meshes)
        if baked_meshes:
            selection_utils.replace_selection(baked_meshes)

    def focus_to_instancer_node(self):
        logger.info("Showing Instancer node of {}".format(MASH_NETWORK_NAME))
        repro = self.get_PP_mash_data("mash_repro")
        if repro:
            selection_utils.replace_selection(repro)
            ui_utils.raise_attribute_editor(repro)


    ############################# SWAP MASTER #############################

    def get_SM_candidate_component_data(self, app_model_data_key):
        return self._model._data["SM_candidate_component"][app_model_data_key]
    
    def get_SM_substitute_root_data(self):
        return self._model._data["SM_substitute_root"]

    def clear_SM_jobs_data(self):
        self._model._data["SM_jobs"] = []
    
    def init_swap_jobs(self, meshes):
        """
        """
        # Modify class variable of SwapMasterJob first
        SwapMasterJob._North_component_IDs = self.get_SM_candidate_component_data("north")
        SwapMasterJob._South_component_IDs = self.get_SM_candidate_component_data("south")
        SwapMasterJob._Yaw_component_IDs = self.get_SM_candidate_component_data("yaw")
        
        self.clear_SM_jobs_data()

        for mesh in meshes:
            swap_job = SwapMasterJob(mesh)
            swap_job.xform_reconstruction()
            self._model._data["SM_jobs"].append(swap_job)

    def preview_SM_nuclei(self):
        self.init_swap_jobs(selection_utils.filter_meshes_in_selection())

    def abort_SM_nuclei(self):
        for swap_job in  self._model._data["SM_jobs"]:
            swap_job.delete_hub_joint()
            swap_job.delete_nucleus_locator()
        self.clear_SM_jobs_data()

    def do_swap(self, get_use_instancing_mode_method, post_cleanup=False):
        """
        :param callable get_use_instancing_mode_method:
        """
        if callable(get_use_instancing_mode_method):
            use_instancing = get_use_instancing_mode_method()
        else:
            use_instancing = True
        logger.info("Use Instancing Mode: {}".format(use_instancing))

        SwapMasterJob._substitute_root = self.get_SM_substitute_root_data()

        if SwapMasterJob._substitute_root:
            for swap_job in  self._model._data["SM_jobs"]:
                swap_job.swap(use_instancing)

        if post_cleanup:
            self.abort_SM_nuclei()

    def fast_forward_swap(self, get_use_instancing_mode_method):
        self.preview_SM_nuclei()
        self.do_swap(get_use_instancing_mode_method, post_cleanup=True)


class SwapMasterJob(object):

    _North_component_IDs = {"component_enum": 0, "children": []}
    _South_component_IDs = {"component_enum": 0, "children": []}
    _Yaw_component_IDs = {"component_enum": 0, "children": []}
    _substitute_root = None

    def __init__(self, mesh, app_model_data=None):
        """
        Operate on a given mesh
        """
        self.status_quo_mesh = mesh
        logger.info('Initializing new SwapMasterJob for mesh {}'.format(node_utils.get_node_name(self.status_quo_mesh)))
        
        self.North_components = mesh_utils.expand_mesh_with_component_IDs(
            self.status_quo_mesh,
            SwapMasterJob._North_component_IDs["children"],
            SwapMasterJob._North_component_IDs["component_enum"],
        )
        self.South_components = mesh_utils.expand_mesh_with_component_IDs(
            self.status_quo_mesh,
            SwapMasterJob._South_component_IDs["children"],
            SwapMasterJob._South_component_IDs["component_enum"],
        )
        self.Yaw_components = mesh_utils.expand_mesh_with_component_IDs(
            self.status_quo_mesh,
            SwapMasterJob._Yaw_component_IDs["children"],
            SwapMasterJob._Yaw_component_IDs["component_enum"],
        )
        
        self.hub_joint_start = None
        self.hub_joint_end = None
        self.hub_joint_aim = None
        
        self.nucleus_locator = None

    def prepare_hub_joint_elements(self):
        """
        :param dict app_model_data: to update
        mesh: {"hub_joint": [self.hub_joint_start, self.hub_joint_end]}
        """
        if self.South_components:
            self.hub_joint_start = transform_utils.create_center_thingy_from(
                self.South_components,
                thingy="joint"
            )
        if self.North_components:
            self.hub_joint_end = transform_utils.create_center_thingy_from(
                self.North_components,
                thingy="joint"
            )
            
        # TODO: create self.hub_joint_aim from self.Yaw_components as well


    def has_hub_joint_elements(self):
        return self.hub_joint_start and self.hub_joint_end

    def make_hub_joint(self):
        """
        Connect hub joints and orient it
        """
        if self.has_hub_joint_elements():
            # parent joint
            node_utils.parent_A_to_B(self.hub_joint_end, self.hub_joint_start)
            # orient joint start to joint end
            transform_utils.orient_joint(self.hub_joint_start, "xyz", "yup")
            # TODO: aimConstraint HubJoint to self.hub_joint_aim
            logger.info("Parented and oriented HubJoint for SwapMasterJob")
        else:
            logger.warning("Either HubJoint start or HubJoint end is missing")

    def make_nucleus_locator_from_hub_joint(self):
        """
        :param dict app_model_data: to update
        mesh: {"nucleus_locator": self.nucleus_locator}
        """
        bounding_objs = deepcopy(self.North_components)
        bounding_objs.extend(self.South_components)

        # logger.info("Creating nucleus locator from bounding objects: {}".format(bounding_objs))
        
        # Create new locator virtually at the center of the HubJoint
        self.nucleus_locator = transform_utils.create_center_thingy_from(
            bounding_objs,
            thingy="locator"
        )
        # Copy orient from HubJoint
        transform_utils.set_rotation_from_joint_orient(
            self.nucleus_locator,
            self.hub_joint_start
        )
        
        # TODO: set display Local Scale of locator relative 
        # to the mesh's bounding box

        # Hide the hub joint
        if hasattr(self.hub_joint_start, "visibility"):
            self.hub_joint_start.visibility.set(False)

    def xform_reconstruction(self):
        """
        Make Nucleus Locator from Hub Joint
        """
        self.prepare_hub_joint_elements()
        self.make_hub_joint()
        self.make_nucleus_locator_from_hub_joint()

    def delete_hub_joint(self):
        joints = [jnt for jnt in (self.hub_joint_aim, self.hub_joint_end, self.hub_joint_start) \
            if jnt is not None]
        node_utils.delete_many(joints)
    
    def delete_nucleus_locator(self):
        if self.nucleus_locator is not None:
            node_utils.delete_one(self.nucleus_locator)

    def swap(self, use_instancing):
        print("TODO: perform swapping using data from class variable _substitute_root")
        # Duplicate
        duplicated = node_utils.duplicate(
            SwapMasterJob._substitute_root, 
            as_instance=use_instancing
        )
        # TODO: Match transforms with Nucleus Locator
