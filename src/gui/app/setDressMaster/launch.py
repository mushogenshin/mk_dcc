import logging
from functools import partial
# from math import ceil

import src.gui.dcc
from src.utils.qt import pattern_utils
from src.utils.maya import selection_utils, scene_utils, node_utils

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def add_widgets(ui):
    # Load Selection
    load_btn_label = "Load"
    clear_btn_label = "X"

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
    ui.PP_dyn_parms_group_box.toggled()
    

def get_dynamics_parameters(ui):
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

    # Load and Clear Selection
    for input_grp in (ui.PP_load_cloud_ui_grp, ui.PP_load_scatter_ui_grp, ui.PP_load_ground_ui_grp):
        input_grp.create_connections(
            selection_utils.filter_meshes_in_selection, 
            lambda: (),
            node_utils.ls_node_name
        )

    ui.PP_load_cloud_ui_grp.connect_app_model_update(model_data, "init.cloud_meshes")
    ui.PP_load_scatter_ui_grp.connect_app_model_update(model_data, "init.scatter_meshes")
    ui.PP_load_ground_ui_grp.connect_app_model_update(model_data, "init.ground_meshes")

    # Setup MASH Network
    def setup_mash_network():
        dynamics_params = get_dynamics_parameters(ui)
        app._control.setup_physx_painter(dynamics_params)
    
    ui.PP_setup_mash_network_btn.clicked.connect(setup_mash_network)

    # Helpers
    ui.PP_reset_playback_btn.clicked.connect(scene_utils.reset_playback)
    ui.PP_show_paint_node_btn.clicked.connect(app._control.focus_to_placer_node)
    ui.PP_toggle_interactive_playback_btn.clicked.connect(scene_utils.toggle_interactive_playback)

    ui.PP_bake_current_btn.clicked.connect(app._control.bake_current)

    # Destruct Setup
    def delete_setup():
        for input_grp in (ui.PP_load_cloud_ui_grp, ui.PP_load_scatter_ui_grp, ui.PP_load_ground_ui_grp):
            input_grp.cleared()
        app._control.delete_setup()

    ui.PP_delete_all_setup_btn.clicked.connect(delete_setup)


if __name__ == '__main__':
    try:
        import pymel.core as pmc
    except ImportError:
        from src.utils import load_pathlib
        Path = load_pathlib()
            
        app_name = Path(__file__).parent.stem

        from src.utils import uic_rebuild
        uic_rebuild(app_name)

        SDM_app = src.gui.dcc.StandAlone(app_name)
        modify_premade_view(SDM_app)
        create_connections(SDM_app)
        SDM_app.show()
    else:
        reload(src.gui.dcc)
        reload(pattern_utils)
        reload(selection_utils)
        try:
            SDM_app._view.close()
            SDM_app._view.deleteLater()
        except:
            pass
            
        SDM_app = src.gui.dcc.Maya('setDressMaster')
        modify_premade_view(SDM_app)
        create_connections(SDM_app)
        SDM_app._view.show()
