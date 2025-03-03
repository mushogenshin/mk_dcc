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


MASH_SCENE_SAVE_PROMPT = "There're bugs with MASH that may cause Maya to crash when \n\
performing this action.\nPlease make sure you have your changes saved.\n\
Do you want to proceed?"

PRE_SWAP_SAVE_PROMPT = "Please make sure you have your changes saved.\n\
Do you want to proceed?"


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

    # Collapsible GroupBox

    ui.PP_dyn_parms_group_box = pattern_utils.CollapsibleGroupBox(
        ui.PP_dyn_parms_child_group_box,
        expanded_height=105
    )

    ui.PP_main_group_box = pattern_utils.CollapsibleGroupBox(
        ui.phys_painter_main_group_box,
        expanded_height=470
    )

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
        "Mesh | Root Node  ", load_btn_label, clear_btn_label
    )

    for i, input_grp in enumerate(
        (ui.SM_load_substitute_ui_grp,)
    ):
        input_grp.add_to_container(
            target=ui.SM_load_substitute_grid_layout,
            row=i
        )

    # Collapsible GroupBox

    ui.SM_orient_reconstruct_group_box = pattern_utils.CollapsibleGroupBox(
         ui.SM_orient_reconstruct_child_group_box,
         expanded_height=75
    )

    ui.SM_main_group_box = pattern_utils.CollapsibleGroupBox(
        ui.swap_master_main_group_box,
        expanded_height=600
    )
    

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


def set_stylesheet(ui):
    # LoadAndDisplayToLineEdit
    for line_edit_grp in (
        ui.PP_load_cloud_ui_grp,
        ui.PP_load_scatter_ui_grp,
        ui.PP_load_ground_ui_grp):
        
        line_edit_grp.line_edit.setStyleSheet("background-color: rgb(12, 12, 12); color: rgb(85, 85, 85)")
        line_edit_grp.label.setStyleSheet("color: rgb(146, 146, 146)")
        line_edit_grp.load_btn.setStyleSheet("background-color: rgb(28, 28, 28); color: rgb(85, 85, 85)")
        line_edit_grp.clear_btn.setStyleSheet("background-color: rgb(28, 28, 28); color: rgb(85, 85, 85)")

    for line_edit_grp in (
        ui.SM_load_north_compos_ui_grp,
        ui.SM_load_south_compos_ui_grp,
        ui.SM_load_yaw_compos_ui_grp,
        ui.SM_load_substitute_ui_grp):
    
        line_edit_grp.line_edit.setStyleSheet("background-color: rgb(12, 12, 12); color: rgb(85, 85, 85)")
        line_edit_grp.label.setStyleSheet("color: rgb(140, 140, 140)")
        line_edit_grp.load_btn.setStyleSheet("background-color: rgb(24, 24, 24); color: rgb(85, 85, 85)")
        line_edit_grp.clear_btn.setStyleSheet("background-color: rgb(24, 24, 24); color: rgb(85, 85, 85)")


def insert_version_in_window_title(app):
    version = app._view.ui.SetDressMaster_about_btn.property("version")
    app._view.setWindowTitle("{} v{}".format(
        app._view.windowTitle(),
        version
    ))


def modify_premade_view(app):
    insert_version_in_window_title(app)
    add_widgets(app._view.ui)
    set_stylesheet(app._view.ui)


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
        proceed = True
        is_scene_modified = scene_utils.is_scene_modified()

        if is_scene_modified:
            # Prompt Yes-No MessageBox
            from src.utils.qt.prompt import show_warning_box
            proceed = show_warning_box(
                ui.centralwidget,
                MASH_SCENE_SAVE_PROMPT
            )
            
        if proceed:
            app._control.delete_PP_setup()
            for input_grp in (ui.PP_load_cloud_ui_grp, ui.PP_load_scatter_ui_grp, ui.PP_load_ground_ui_grp):
                input_grp.cleared()

    ui.PP_delete_all_setup_btn.clicked.connect(delete_PP_setup)

    ############################# SWAP MASTER #############################

    # Prep
    def scene_prep_strategy(checked):
        ui.SM_explode_and_group_btn.setDisabled(not checked)
        ui.SM_run_thru_scene_and_group_btn.setDisabled(checked)

    ui.SM_prep_mash_scene_radio_btn.toggled.connect(scene_prep_strategy)
    ui.SM_explode_and_group_btn.clicked.connect(app._control.explode_mash_mesh_and_group_by_poly_count)
    ui.SM_run_thru_scene_and_group_btn.clicked.connect(app._control.run_thru_scene_and_group_by_poly_count)

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
            func=lambda: {"component_enum": 0, "children": [], "mesh": None}
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

    # Do Swap

    def get_SM_use_instancing_mode_from_UI():
        return ui.SM_swap_use_instancing_check_box.isChecked()

    def get_SM_remove_proxies_mode_from_UI():
        return ui.SM_remove_proxies_check_box.isChecked()
    
    def get_SM_compute_scale_mode_from_UI():
        return ui.SM_compute_scale_check_box.isChecked()

    # Orientation Reconstruction

    ui.SM_preview_nuclei_btn.clicked.connect(partial(
        app._control.preview_SM_nuclei,
        get_compute_scale_mode_method=get_SM_compute_scale_mode_from_UI
    ))
    ui.SM_abort_nuclei_btn.clicked.connect(app._control.abort_SM_nuclei)

    def fast_forward_swap():
        proceed = True
        is_scene_modified = scene_utils.is_scene_modified()
        
        if is_scene_modified:
            # Prompt Yes-No MessageBox
            from src.utils.qt.prompt import show_warning_box
            proceed = show_warning_box(
                ui.centralwidget,
                PRE_SWAP_SAVE_PROMPT
            )

        if proceed:
            app._control.fast_forward_swap(
                get_use_instancing_mode_method=get_SM_use_instancing_mode_from_UI,
                get_remove_proxies_mode_method=get_SM_remove_proxies_mode_from_UI,
                get_compute_scale_mode_method=get_SM_compute_scale_mode_from_UI
            )

    ui.SM_proceed_swapping_btn.clicked.connect(partial(
        app._control.do_swap,
        get_use_instancing_mode_method=get_SM_use_instancing_mode_from_UI,
        get_remove_proxies_mode_method=get_SM_remove_proxies_mode_from_UI,
        get_compute_scale_mode_method=get_SM_compute_scale_mode_from_UI
    ))
    ui.SM_fast_forward_swap_btn.clicked.connect(fast_forward_swap)

    # Show Results
    ui.SM_show_swapped_btn.clicked.connect(app._control.show_swapped)

    scene_prep_strategy(ui.SM_prep_mash_scene_radio_btn.isChecked())

    ############################# ABOUT #############################

    def show_app_about():
        from src.utils.qt.prompt import show_info_box
        about_app = ui.SetDressMaster_about_btn.property("about")
        show_info_box(
            ui.centralwidget,
            about_app
        )

    ui.SetDressMaster_about_btn.clicked.connect(show_app_about)


def init_gui(app):
    ui = app._view.ui

    # ui.PP_main_group_box.toggled()
    ui.PP_dyn_parms_group_box.toggled()
    # ui.SM_main_group_box.toggled()
    ui.SM_orient_reconstruct_group_box.toggled()
