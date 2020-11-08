import sys
import logging
from collections import namedtuple

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


AxisCfg = namedtuple("AxisCfg", ["JO_aim_axis", "JO_up_axis", "aim_vec", "up_vec"])


class Control(object):
    def __init__(self):
        super(Control, self).__init__()
        self.SCENE_ENV = scene_utils.get_scene_env()

    def print_model_data(self):
        from pprint import pprint
        print("\n***UPDATED APP MODEL DATA:")
        pprint(self._model._data)

    ############################# PHYSX PAINTER #############################

    def get_PP_init_data(self, app_model_data_key):
        return self._model._data["PP_init"][app_model_data_key]

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
        
        scene_utils.disable_cached_playback()  # Maya 2019 onwards
        
        waiter = distribute = repro = None
        scatter_meshes = self.get_PP_init_data("scatter_meshes")

        network = self.get_PP_mash_data("mash_network")
        if not network and hasattr(mapi, "Network"):
            # Scatter Meshes must be being selected prior to MASH Network creation
            selection_utils.replace_selection(scatter_meshes)

            network = mapi.Network()  
            self.set_PP_mash_data("mash_network", network)  # MASH.api.Network instance, not PyNode

            if hasattr(network, "createNetwork") and \
                not node_utils.node_exists(MASH_NETWORK_NAME, as_string=True):  # force Singleton
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

    def remove_bullet_solver(self):
        logger.info("Removing Bullet Solver of {}".format(MASH_NETWORK_NAME))
        bullet_solver = self.get_PP_mash_data("mash_bullet")
        node_utils.delete_one(bullet_solver)
        self.set_PP_mash_data("mash_bullet", None)

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
        
        self.remove_bullet_solver()

        for data_key, node in self._model._data["PP_mash"].items():
            if data_key != "mash_network":
                node_utils.delete_one(node)
            else:
                scene_utils.delete(MASH_NETWORK_NAME)
                # scene_utils.delete(MASH_NETWORK_NAME)  # delete twice due to Maya|MASH bug

        # Reset MASH model data
        self._model.init_PP_mash_data()

        # There are two more nodes left to delete
        scene_utils.delete("{}_Distribute".format(MASH_NETWORK_NAME))
        scene_utils.delete("{}_ID".format(MASH_NETWORK_NAME))

        # Turn on visibility, which was turned off automatically by MASH, for scatter_meshes
        node_utils.set_visibility(self.get_PP_init_data("scatter_meshes"))

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

    def explode_mash_mesh_and_group_by_poly_count(self):
        logger.info("Exploding MASH mesh and group separated by poly count")
        mesh_utils.explode_and_group_by_poly_count(
            selection_utils.filter_meshes_in_selection()
        )

    def run_thru_scene_and_group_by_poly_count(self):
        logger.info("Running through meshes in scene and group all by poly count")
        mesh_utils.explode_and_group_by_poly_count()

    def get_SM_candidate_component_data(self, app_model_data_key):
        return self._model._data["SM_candidate_component"][app_model_data_key]
    
    def get_SM_substitute_root_data(self):
        SM_substitute_root = self._model._data["SM_substitute_root"]
        if SM_substitute_root is not None and node_utils.node_exists(SM_substitute_root):
            return SM_substitute_root
        else:
            return None

    def clear_SM_jobs_data(self):
        self._model._data["SM_jobs"] = []

    def register_swap_job(self, swap_job):
        self._model._data["SM_jobs"].append(swap_job)

    def clear_SM_last_swapped_data(self):
        self._model._data["SM_last_swapped"] = []

    def register_last_swapped(self, swapped):
        if swapped is not None:
            self._model._data["SM_last_swapped"].append(swapped)
    
    def init_swap_jobs(self, meshes, compute_scale):
        """
        """
        # Modify class variable of SwapMasterJob first
        SwapMasterJob.North_component_IDs = self.get_SM_candidate_component_data("north")
        SwapMasterJob.South_component_IDs = self.get_SM_candidate_component_data("south")
        SwapMasterJob._Yaw_component_IDs = self.get_SM_candidate_component_data("yaw")
        
        SwapMasterJob.get_statusquo_repr_hub_jnt_pole_dimension()
        SwapMasterJob.get_statusquo_repr_bbox_dimensions()
        SwapMasterJob.get_statusquo_repr_hub_jnt_start_to_rotate_pivot_vec()
        SwapMasterJob.get_hub_joint_axis_cfg()
        
        self.clear_SM_jobs_data()

        for mesh in meshes:
            swap_job = SwapMasterJob(mesh)
            swap_job.xform_reconstruction(compute_scale)
            self.register_swap_job(swap_job)

    def preview_SM_nuclei(self, get_compute_scale_mode_method):
        if callable(get_compute_scale_mode_method):
            compute_scale = get_compute_scale_mode_method()
        else:
            compute_scale = True
        self.init_swap_jobs(selection_utils.filter_meshes_in_selection(), compute_scale)
        self.print_model_data()

    def abort_SM_nuclei(self, verbose=True):
        logger.info("Removing Nucleus Locator and Hub Joint for all SwapJobs")
        for swap_job in  self._model._data["SM_jobs"]:
            swap_job.delete_hub_joint()
            swap_job.delete_nucleus_locator()
        self.clear_SM_jobs_data()
        if verbose:
            self.print_model_data()

    def group_last_swapped(self):
        if self._model._data["SM_last_swapped"]:
            transform_utils.make_null(
                name="SM_last_swapped", 
                children=self._model._data["SM_last_swapped"])

    def do_swap(self, get_use_instancing_mode_method, get_remove_proxies_mode_method, get_compute_scale_mode_method, post_cleanup=False):
        """
        :param callable get_use_instancing_mode_method, get_remove_proxies_mode_method, get_compute_scale_mode_method:
        """
        self.clear_SM_last_swapped_data()

        if callable(get_use_instancing_mode_method):
            use_instancing = get_use_instancing_mode_method()
        else:
            use_instancing = True
        if callable(get_remove_proxies_mode_method):
            remove_proxies = get_remove_proxies_mode_method()
        else:
            remove_proxies = True
        if callable(get_compute_scale_mode_method):
            compute_scale = get_compute_scale_mode_method()
        else:
            compute_scale = True
        logger.info("Use Instancing Mode: {}; Remove Proxies Mode: {}; Compute Scale Mode: {}".format(
            use_instancing, 
            remove_proxies,
            compute_scale)
        )

        statusquo_repr_mesh = SwapMasterJob.get_statusquo_repr_mesh()
        substitute_template_root = self.get_SM_substitute_root_data()
        for swap_job in  self._model._data["SM_jobs"]:
            swapped = swap_job.swap(
                statusquo_repr_mesh, 
                substitute_template_root, 
                use_instancing, 
                remove_proxies,
                compute_scale,
            )
            self.register_last_swapped(swapped)

        # Group all swapped
        self.group_last_swapped()

        if post_cleanup:
            self.abort_SM_nuclei(verbose=False)

        self.print_model_data()

    def fast_forward_swap(self, get_use_instancing_mode_method, get_remove_proxies_mode_method, get_compute_scale_mode_method):
        self.preview_SM_nuclei(get_compute_scale_mode_method)
        self.do_swap(get_use_instancing_mode_method, get_remove_proxies_mode_method, get_compute_scale_mode_method, post_cleanup=True)

    def show_swapped(self):
        selection_utils.replace_selection(self._model._data["SM_last_swapped"])


class SwapMasterJob(object):

    North_component_IDs = {"component_enum": 0, "children": [], "mesh": None}
    South_component_IDs = {"component_enum": 0, "children": [], "mesh": None}
    Yaw_component_IDs = {"component_enum": 0, "children": [], "mesh": None}
    
    axis_cfg = None
    statusquo_repr_hub_jnt_pole_dimension = 0
    statusquo_repr_bbox_dimensions = (1, 1, 1)
    statusquo_repr_hub_jnt_start_to_rotate_pivot_vec = None

    def __init__(self, status_quo_mesh, app_model_data=None):
        """
        Operate on a given mesh
        """
        self.status_quo_mesh = status_quo_mesh
        self.status_quo_mesh_name = self.get_status_quo_mesh_name()
        logger.info('Initializing new SwapMasterJob for mesh {}'.format(self.status_quo_mesh_name))
        
        self.North_components = mesh_utils.expand_mesh_with_component_IDs(
            self.status_quo_mesh,
            SwapMasterJob.North_component_IDs["children"],
            SwapMasterJob.North_component_IDs["component_enum"],
        )
        self.South_components = mesh_utils.expand_mesh_with_component_IDs(
            self.status_quo_mesh,
            SwapMasterJob.South_component_IDs["children"],
            SwapMasterJob.South_component_IDs["component_enum"],
        )
        self.Yaw_components = mesh_utils.expand_mesh_with_component_IDs(
            self.status_quo_mesh,
            SwapMasterJob._Yaw_component_IDs["children"],
            SwapMasterJob._Yaw_component_IDs["component_enum"],
        )
        
        self.hub_joint_start = None
        self.hub_joint_end = None
        self.hub_joint_yaw = None
        self.hub_joint_pole_dimension = 0
        self.scale_factor = 1
        
        self.nucleus_locator = None
        self.swapped = None

    def get_status_quo_mesh_name(self):
        return node_utils.get_node_name(self.status_quo_mesh)

    @classmethod
    def get_statusquo_repr_mesh(cls):
        return cls.South_component_IDs["mesh"]

    @staticmethod
    def get_statusquo_repr_hub_jnt_end_point():
        return transform_utils.get_center_position(
            mesh_utils.expand_mesh_with_component_IDs(
                SwapMasterJob.North_component_IDs["mesh"],
                SwapMasterJob.North_component_IDs["children"],
                SwapMasterJob.North_component_IDs["component_enum"]
            ),
            as_point=True
        )

    @staticmethod
    def get_statusquo_repr_hub_jnt_start_point():
        return transform_utils.get_center_position(
            mesh_utils.expand_mesh_with_component_IDs(
                SwapMasterJob.South_component_IDs["mesh"],
                SwapMasterJob.South_component_IDs["children"],
                SwapMasterJob.South_component_IDs["component_enum"]
            ),
            as_point=True
        )

    @staticmethod
    def get_statusquo_repr_rotate_pivot_point():
        return transform_utils.get_rotate_pivot(
            SwapMasterJob.get_statusquo_repr_mesh(),
            is_mesh=True
        )

    @classmethod
    def get_statusquo_repr_hub_jnt_start_to_rotate_pivot_vec(cls):
        # zero out any rotation on statusquo_repr mesh first
        with transform_utils.zero_but_restore_transforms_afterwards(
            cls.get_statusquo_repr_mesh(),
            is_mesh=True
        ):
            cls.statusquo_repr_hub_jnt_start_to_rotate_pivot_vec = transform_utils.get_translation_between_two_points(
                cls.get_statusquo_repr_hub_jnt_start_point(),
                cls.get_statusquo_repr_rotate_pivot_point()
            )

        logger.info("Translation from start of Hub Joint to RotatePivot: {}".format(
            cls.statusquo_repr_hub_jnt_start_to_rotate_pivot_vec
        ))

    @classmethod
    def get_hub_joint_axis_cfg(cls):
        """
        :rtype AxisCfg:
        """
        scene_up_axis = scene_utils.get_scene_up_axis()
        if scene_up_axis:
            logger.info("Current Maya scene up axis: {}".format(scene_up_axis))
        
        if scene_up_axis == "y":
            JO_aim_axis = "yzx"  # Y-axis pointing down the bone
            JO_up_axis = "zup"
            aim_vec = (0, 1, 0)
            up_vec = (0, 0, 1)
        elif scene_up_axis == "z":
            JO_aim_axis = "zxy"  # Z-axis pointing down the bone
            JO_up_axis = "xup"
            aim_vec = (0, 0, 1)
            up_vec = (1, 0, 0)
        else:
            JO_aim_axis = "xyz"  # X-axis pointing down the bone
            JO_up_axis = "yup"
            aim_vec = (1, 0, 0)
            up_vec = (0, 1, 0)
        
        logger.info('Using Joint Orient aim axis "{}"; Joint Orient up axis "{}"'.format(JO_aim_axis, JO_up_axis))
        logger.info('Using Aim vector {}; Up vector {}'.format(aim_vec, up_vec))

        cls.axis_cfg = AxisCfg(JO_aim_axis, JO_up_axis, aim_vec, up_vec)

    @classmethod
    def get_statusquo_repr_hub_jnt_pole_dimension(cls):
        cls.statusquo_repr_hub_jnt_pole_dimension = transform_utils.get_translation_between_two_points(
            cls.get_statusquo_repr_hub_jnt_start_point(),
            cls.get_statusquo_repr_hub_jnt_end_point(),
            as_length=True
        )

    @classmethod
    def get_statusquo_repr_bbox_dimensions(cls):
        cls.statusquo_repr_bbox_dimensions = mesh_utils.get_bounding_box_dimensions(
            cls.get_statusquo_repr_mesh()
        )

    def prepare_hub_joint_elements(self):

        if self.South_components:
            self.hub_joint_start = transform_utils.create_center_thingy_from(
                self.South_components,
                thingy="joint",
                name="_".join(["SM_hubjoint_start", self.status_quo_mesh_name])
            )
        if self.North_components:
            self.hub_joint_end = transform_utils.create_center_thingy_from(
                self.North_components,
                thingy="joint",
                name="_".join(["SM_hubjoint_end", self.status_quo_mesh_name])
            )
        
        if self.Yaw_components:
            self.hub_joint_yaw = transform_utils.create_center_thingy_from(
                self.Yaw_components,
                thingy="joint",
                name="_".join(["SM_hubjoint_yaw", self.status_quo_mesh_name])
            )


    def has_hub_joint_elements(self):
        return self.hub_joint_start and self.hub_joint_end

    def orient_hub_joint(self):
        """
        Connect hub joints and orient it
        """
        if self.has_hub_joint_elements():
            if not self.hub_joint_yaw:
                # Use parent and joint orient
                node_utils.parent_A_to_B(self.hub_joint_end, self.hub_joint_start)
                transform_utils.orient_joint(
                    self.hub_joint_start, 
                    SwapMasterJob.axis_cfg.JO_aim_axis, 
                    SwapMasterJob.axis_cfg.JO_up_axis, 
                )
                logger.info("Parented and oriented HubJoint for SwapMasterJob")
            else:
                # Use aimConstraint
                transform_utils.aim_constrain_with_world_up_object(
                    self.hub_joint_end,
                    self.hub_joint_start,
                    SwapMasterJob.axis_cfg.aim_vec,
                    SwapMasterJob.axis_cfg.up_vec,
                    self.hub_joint_yaw,  # world up object
                )
                logger.info("Aim constrained HubJoint for SwapMasterJob")
            # Hide the hub joints
            for jnt in (self.hub_joint_start, self.hub_joint_end, self.hub_joint_yaw):
                if hasattr(jnt, "visibility"):
                    jnt.visibility.set(False)
        else:
            logger.warning("Either HubJoint start or HubJoint end is missing")

    def make_nucleus_locator_from_hub_joint(self, compute_scale):
        if compute_scale and SwapMasterJob.statusquo_repr_hub_jnt_pole_dimension:
            self.hub_joint_pole_dimension = transform_utils.get_translation_between_two_points(
                transform_utils.get_rotate_pivot(self.hub_joint_start),
                transform_utils.get_rotate_pivot(self.hub_joint_end),
                as_length=True
            )
            self.scale_factor = self.hub_joint_pole_dimension / SwapMasterJob.statusquo_repr_hub_jnt_pole_dimension
        self.scale_factor = self.scale_factor if self.scale_factor else 1
        logger.info("Scale factor: {}".format(self.scale_factor))

        # Create new locator at HubJoint start
        self.nucleus_locator = transform_utils.make_space_locator(
            name="_".join(["SM_nucleus_locator", self.status_quo_mesh_name])
        )
        transform_utils.match_transforms(self.nucleus_locator, self.hub_joint_start, rotation=False)

        if self.hub_joint_yaw:
            transform_utils.bake_aim_constraint_to_joint_orient(self.hub_joint_start)

        # Copy orient from HubJoint
        transform_utils.set_rotation_from_joint_orient(
            self.nucleus_locator,
            self.hub_joint_start
        )

        # Move nucleus locator to supposed rotatePivot of object
        dummy_locator_parent = node_utils.duplicate(self.nucleus_locator)
        if dummy_locator_parent:
            dummy_locator_parent = dummy_locator_parent[0]
            node_utils.parent_A_to_B(self.nucleus_locator, dummy_locator_parent, zero_child_transforms=True)
        
            transform_utils.set_translation(
                self.nucleus_locator, 
                SwapMasterJob.statusquo_repr_hub_jnt_start_to_rotate_pivot_vec * self.scale_factor
            )
            node_utils.parent_to_world(
                self.nucleus_locator,
                former_parent_to_delete=dummy_locator_parent
            )
        
        # set display Local Scale of locator relative to the mesh's bounding box
        transform_utils.set_locator_local_scale(
            self.nucleus_locator,
            SwapMasterJob.statusquo_repr_bbox_dimensions
        )

    def xform_reconstruction(self, compute_scale):
        """
        Make Nucleus Locator from Hub Joint
        """
        self.prepare_hub_joint_elements()
        self.orient_hub_joint()
        self.make_nucleus_locator_from_hub_joint(compute_scale)

    def delete_hub_joint(self):
        joints = [jnt for jnt in (self.hub_joint_yaw, self.hub_joint_end, self.hub_joint_start) \
            if jnt is not None]
        node_utils.delete_many(joints)
        for jnt in joints:
            jnt = None
    
    def delete_nucleus_locator(self):
        if self.nucleus_locator is not None:
            node_utils.delete_one(self.nucleus_locator)
            self.nucleus_locator = None

    def remove_proxy(self):
        node_utils.delete_one(self.status_quo_mesh)

    def swap(self, statusquo_repr_mesh, substitute_template_root, use_instancing, remove_proxy, compute_scale):
        """
        :param pmc.nt.Mesh|None statusquo_repr_mesh:
        :param pmc.nt.Mesh|None substitute_template_root:
        :param bool use_instancing, remove_proxy:
        """
        # Duplicate|Instance
        if substitute_template_root:
            logger.info("Running SwapJob with given substitute template root: {}".format(substitute_template_root))
            self.swapped = node_utils.duplicate(
                substitute_template_root, 
                as_instance=use_instancing
            )  
        else:
            logger.info("Running SwapJob with given representative of status quo: {}".format(statusquo_repr_mesh))
            self.swapped = node_utils.duplicate(
                statusquo_repr_mesh,
                as_instance=use_instancing
            )
            
        self.swapped = self.swapped[0] if self.swapped else None

        # Match transforms with Nucleus Locator
        if self.swapped is None:
            return
        else:
            transform_utils.match_transforms(self.swapped, self.nucleus_locator)
            if compute_scale:
                transform_utils.set_scale(self.swapped, self.scale_factor)

        if remove_proxy:
            logger.info("Removing original pre-swapped mesh")
            node_utils.delete_one(self.status_quo_mesh, is_mesh=True)
            self.status_quo_mesh = None

        return self.swapped
