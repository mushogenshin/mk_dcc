from functools import partial

import logging
logger = logging.getLogger(__name__)

from src.utils.qt import pattern_utils
from src.utils.maya import (
    selection_utils, 
    scene_utils, 
    node_utils,
    mesh_utils
)


def add_widgets(ui):
    # Load Selection
    load_btn_label = "Load"
    clear_btn_label = "X"

    ############################# PHYSX PAINTER #############################

    ui.PP_load_cloud_ui_grp = pattern_utils.LoadAndDisplayToLineEdit(
        "1. Paint Surface(s)", load_btn_label, clear_btn_label
    )
    ui.PP_load_scatter_ui_grp = pattern_utils.LoadAndDisplayToLineEdit(
        "2. Meshes to Scatter",  load_btn_label, clear_btn_label
    )
    ui.PP_load_ground_ui_grp = pattern_utils.LoadAndDisplayToLineEdit(
        "3. Landing Surface(s)",  load_btn_label, clear_btn_label
    )

    for i, input_grp in enumerate(
        (ui.PP_load_cloud_ui_grp, ui.PP_load_scatter_ui_grp, ui.PP_load_ground_ui_grp)
    ):
        input_grp.add_to_container(
            target=ui.PP_load_selection_grid_layout,
            row=i
        )

    # Dynamics Parameters
    ui.PP_dyn_parm_friction = pattern_utils.LabeledSpinBox(
        "Friction", "friction", double=True, default_value=0.4
    )
    ui.PP_dyn_parm_rolling_friction = pattern_utils.LabeledSpinBox(
        "Rolling Friction", "rollingFriction", double=True, default_value=0.4
    )
    ui.PP_dyn_parm_damping = pattern_utils.LabeledSpinBox(
        "Damping", "damping", double=True, default_value=0.3
    )
    ui.PP_dyn_parm_rolling_damping = pattern_utils.LabeledSpinBox(
        "Rolling Damping", "rollingDamping", double=True, default_value=0.1
    )
    ui.PP_dyn_parm_bounce = pattern_utils.LabeledSpinBox(
        "Bounce", "bounce", double=True, default_value=0.02
    )
    ui.PP_dyn_parm_collision_jitter = pattern_utils.LabeledSpinBox(
        "Collision Jitter", "collisionJitter", double=True, default_value=0.005
    )

    for i, spin_box in enumerate(
        (ui.PP_dyn_parm_friction,
        ui.PP_dyn_parm_rolling_friction,
        ui.PP_dyn_parm_damping,
        ui.PP_dyn_parm_rolling_damping,
        ui.PP_dyn_parm_bounce,
        ui.PP_dyn_parm_collision_jitter,)
    ):
        spin_box.set_step(0.01)
        spin_box.set_decimals(3)
        spin_box.add_to_container(
            target=ui.PP_dynamic_parameters_grid_layout,
            row=int(i / 2),
            start_column=0 if i % 2 == 0 else 2,
        )

    ui.PP_dyn_parms_group_box = pattern_utils.CollapsibleGroupBox(
        ui.PP_dyn_parms_child_group_box,
        expanded_height=105
    )

    ui.PP_main_group_box = pattern_utils.CollapsibleGroupBox(
        ui.phys_painter_main_group_box,
        expanded_height=460
    )

    ui.PP_main_group_box.toggled()
    ui.PP_dyn_parms_group_box.toggled()

    ############################# SWAP MASTER #############################

    ui.SM_load_north_compos_ui_grp = pattern_utils.LoadAndDisplayToLineEdit(
        "1. NORTH\ncomponents", load_btn_label, clear_btn_label
    )
    ui.SM_load_south_compos_ui_grp = pattern_utils.LoadAndDisplayToLineEdit(
        "2. SOUTH\ncomponents",  load_btn_label, clear_btn_label
    )
    ui.SM_load_yaw_compos_ui_grp = pattern_utils.LoadAndDisplayToLineEdit(
        "3. YAW components\n(optional)",  load_btn_label, clear_btn_label
    )

    for i, input_grp in enumerate(
        (ui.SM_load_north_compos_ui_grp, ui.SM_load_south_compos_ui_grp, ui.SM_load_yaw_compos_ui_grp)
    ):
        input_grp.add_to_container(
            target=ui.SM_load_trace_components_grid_layout,
            row=i
        )

    ui.SM_load_substitute_ui_grp = pattern_utils.LoadAndDisplayToLineEdit(
        "Mesh | Root Node", load_btn_label, clear_btn_label
    )

    for i, input_grp in enumerate(
        (ui.SM_load_substitute_ui_grp,)
    ):
        input_grp.add_to_container(
            target=ui.SM_load_substitute_grid_layout,
            row=i
        )

    # ui.SM_main_group_box = pattern_utils.CollapsibleGroupBox(
    #     ui.swap_master_main_group_box,
    #     expanded_height=320
    # )
    

def get_PP_dynamics_parameters(ui):
    params = {}
    for spin_box in (
        ui.PP_dyn_parm_friction,
        ui.PP_dyn_parm_rolling_friction,
        ui.PP_dyn_parm_damping,
        ui.PP_dyn_parm_rolling_damping,
        ui.PP_dyn_parm_bounce,
        ui.PP_dyn_parm_collision_jitter,
    ):
        params[spin_box.data_key] = spin_box.value()
    return params


def modify_premade_view(app):
    add_widgets(app._view.ui)


def create_connections(app):
    ui = app._view.ui
    model_data = app._model._data

    # Debugging
    def print_model_data():
        from pprint import pprint
        print("***APP MODEL DATA:")
        pprint(model_data)

    ############################# PHYSX PAINTER #############################

    # Load and Clear Selection
    for input_grp in (ui.PP_load_cloud_ui_grp, ui.PP_load_scatter_ui_grp, ui.PP_load_ground_ui_grp):
        input_grp.create_simple_connections(
            selection_utils.filter_meshes_in_selection,  # load_func
            lambda: (),  # clear_func
            node_utils.ls_node_name  # print_func
        )

    ui.PP_load_cloud_ui_grp.connect_app_model_update(model_data, "PP_init.cloud_meshes")
    ui.PP_load_scatter_ui_grp.connect_app_model_update(model_data, "PP_init.scatter_meshes")
    ui.PP_load_ground_ui_grp.connect_app_model_update(model_data, "PP_init.ground_meshes")

    # Setup MASH Network
    def setup_PP_mash_network():
        dynamics_params = get_PP_dynamics_parameters(ui)
        app._control.setup_physx_painter(dynamics_params)
    
    ui.PP_setup_mash_network_btn.clicked.connect(setup_PP_mash_network)

    # Helpers
    ui.PP_reset_playback_btn.clicked.connect(scene_utils.reset_playback)
    ui.PP_show_paint_node_btn.clicked.connect(app._control.focus_to_placer_node)
    ui.PP_toggle_interactive_playback_btn.clicked.connect(scene_utils.toggle_interactive_playback)
    ui.PP_show_instancer_node_btn.clicked.connect(app._control.focus_to_instancer_node)

    ui.PP_bake_current_btn.clicked.connect(app._control.PP_bake_current)
    ui.PP_show_all_baked_btn.clicked.connect(app._control.PP_show_all_baked)

    # Destruct Setup
    def delete_PP_setup():
        for input_grp in (ui.PP_load_cloud_ui_grp, ui.PP_load_scatter_ui_grp, ui.PP_load_ground_ui_grp):
            input_grp.cleared()
        app._control.delete_PP_setup()

    ui.PP_delete_all_setup_btn.clicked.connect(delete_PP_setup)

    ############################# SWAP MASTER #############################

    # Status Quo's Traces
    
    def get_SM_component_enum_from_UI():
        if ui.SM_trace_vertex_radio_btn.isChecked():
            return 1
        elif ui.SM_trace_edge_radio_btn.isChecked():
            return 2
        elif ui.SM_trace_face_radio_btn.isChecked():
            return 3

    def print_component_IDs(data):
        return data["children"]

    for input_grp in (ui.SM_load_north_compos_ui_grp, ui.SM_load_south_compos_ui_grp, ui.SM_load_yaw_compos_ui_grp):
        # Manually connect three load_func, clear_func, print_func
        input_grp.load_btn.clicked.connect(partial(
            input_grp.load_btn_clicked,
            # func=mesh_utils.filter_mesh_components_of_type_in_selection,
            func=mesh_utils.filter_mesh_components_of_type_in_selection_as_IDs,
            get_component_enum_method=get_SM_component_enum_from_UI
        ))
        input_grp.clear_btn.clicked.connect(partial(
            input_grp.clear_btn_clicked,
            func=lambda: {"component_enum": 0, "children": []}
        ))
        input_grp.print_line_edit_method = print_component_IDs

    ui.SM_load_north_compos_ui_grp.connect_app_model_update(model_data, "SM_candidate_component.north")
    ui.SM_load_south_compos_ui_grp.connect_app_model_update(model_data, "SM_candidate_component.south")
    ui.SM_load_yaw_compos_ui_grp.connect_app_model_update(model_data, "SM_candidate_component.yaw")   

    # Substitute Input

    ui.SM_load_substitute_ui_grp.create_simple_connections(
        selection_utils.get_first_xform_in_selection,  # load_func
        lambda: None,  # clear_func
        node_utils.get_node_name  # print_func
    )

    ui.SM_load_substitute_ui_grp.connect_app_model_update(model_data, "SM_substitute_root")

    # Orientation Reconstruction

    def preview_SM_nuclei():
        app._control.preview_SM_nuclei()
        print_model_data()

    ui.SM_preview_nuclei_btn.clicked.connect(preview_SM_nuclei)
    ui.SM_abort_nuclei_btn.clicked.connect(app._control.abort_SM_nuclei)

    # Do Swap

    def get_SM_use_instancing_mode_from_UI():
        return ui.SM_swap_use_instancing_check_box.isChecked()

    ui.SM_proceed_swapping_btn.clicked.connect(partial(
        app._control.do_swap,
        get_use_instancing_mode_method=get_SM_use_instancing_mode_from_UI
    ))
    ui.SM_fast_forward_swap_btn.clicked.connect(partial(
        app._control.fast_forward_swap,
        get_use_instancing_mode_method=get_SM_use_instancing_mode_from_UI
    ))


def init_gui(app):
    ui = app._view.ui
    model_data = app._model._data
