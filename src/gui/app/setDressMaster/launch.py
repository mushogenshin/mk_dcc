import logging
from functools import partial

import src.gui.dcc
from src.utils.qt import pattern_utils
from src.utils.maya import selection_utils, scene_utils

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# SCENE_ENV = scene_utils.get_scene_env()


def add_widgets(ui):
    # Load Selection
    load_btn_label = "Load"
    clear_btn_label = "X"

    ui.load_cloud_ui_grp = pattern_utils.LoadAndDisplayToLineEdit(
        "1. Paint Surface(s)", load_btn_label, clear_btn_label
    )
    ui.load_scatter_ui_grp = pattern_utils.LoadAndDisplayToLineEdit(
        "2. Meshes to Scatter",  load_btn_label, clear_btn_label
    )
    ui.load_ground_ui_grp = pattern_utils.LoadAndDisplayToLineEdit(
        "3. Landing Surface(s)",  load_btn_label, clear_btn_label
    )

    for i, layout_pattern in enumerate(
        [ui.load_cloud_ui_grp, ui.load_scatter_ui_grp, ui.load_ground_ui_grp]
    ):
        layout_pattern.add_to_container(
            target=ui.phys_painter_load_selection_grid_layout,
            row=i
        )


def modify_premade_view(app):
    add_widgets(app._view.ui)


def create_connections(app):
    ui = app._view.ui
    model_data = app._model._data

    for layout_pattern in (ui.load_cloud_ui_grp, ui.load_scatter_ui_grp, ui.load_ground_ui_grp):
        layout_pattern.create_connections(
            selection_utils.filter_meshes_in_selection, 
            lambda: (),
            selection_utils.ls_node_name
        )

    ui.load_cloud_ui_grp.connect_app_model_update(model_data, "init.cloud_meshes")
    ui.load_scatter_ui_grp.connect_app_model_update(model_data, "init.scatter_meshes")
    ui.load_ground_ui_grp.connect_app_model_update(model_data, "init.ground_meshes")

    ui.setup_mash_network_btn.clicked.connect(app._control.setup_physx_painter)

    ui.reset_playback_btn.clicked.connect(scene_utils.reset_playback)
    ui.show_paint_node_btn.clicked.connect(app._control.focus_to_placer_node)
    ui.toggle_interactive_playback_btn.clicked.connect(scene_utils.toggle_interactive_playback)


    # # Debugging
    # ui.setup_mash_network_btn.clicked.connect(partial(
    #     print_app_model_data,
    #     app=app
    # ))


def print_app_model_data(app):
    print(app._model._data)


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
