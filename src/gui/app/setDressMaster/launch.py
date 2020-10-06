import sys
from functools import partial

import src.gui.dcc
from src.utils.qt import pattern
from src.utils.maya import selection

is_py2 = True if sys.version_info.major < 3 else False


def add_widgets(ui):

    # Load Selection
    load_btn_label = "Load"
    clear_btn_label = "X"

    ui.load_cloud_pattern = pattern.LoadAndDisplayToLineEdit(
        "1. Cloud", load_btn_label, clear_btn_label
    )
    ui.load_scatter_pattern = pattern.LoadAndDisplayToLineEdit(
        "2. Scatter",  load_btn_label, clear_btn_label
    )
    ui.load_ground_pattern = pattern.LoadAndDisplayToLineEdit(
        "3. Grounds",  load_btn_label, clear_btn_label
    )

    for i, layout_pattern in enumerate(
        [ui.load_cloud_pattern, ui.load_scatter_pattern, ui.load_ground_pattern]
    ):
        layout_pattern.add_to_container(
            target=ui.phys_painter_load_selection_grid_layout,
            row=i
        )

    # 


def modify_premade_view(app):
    add_widgets(app._view.ui)


def create_connections(app):
    ui = app._view.ui
    model_data = app._model.data

    # TODO: not sure why these do not behave properly when being fed in loop
    ui.load_cloud_pattern.create_connections(
        selection.filter_meshes_in_selection, 
        lambda: (),
        selection.ls_node_name
    )
    ui.load_scatter_pattern.create_connections(
        selection.filter_meshes_in_selection, 
        lambda: (),
        selection.ls_node_name
    )
    ui.load_ground_pattern.create_connections(
        selection.filter_meshes_in_selection, 
        lambda: (),
        selection.ls_node_name
    )

    ui.load_cloud_pattern.connect_app_model_update(
        model_data,
        "cloud_meshes"
    )
    ui.load_scatter_pattern.connect_app_model_update(
        model_data,
        "scatter_meshes"
    )
    ui.load_ground_pattern.connect_app_model_update(
        model_data,
        "ground_meshes"
    )

    # Debugging
    ui.setup_mash_network_btn.clicked.connect(partial(
        print_app_model_data,
        app=app
    ))


def print_app_model_data(app):
    print(app._model.data)


if __name__ == '__main__':
    try:
        import maya
    except ImportError:
        if not is_py2:
            from pathlib import Path
        else:
            from pathlib2 import Path
            
        app_name = Path(__file__).parent.stem

        from src.utils import uic_rebuild
        uic_rebuild(app_name)

        SDM_app = src.gui.dcc.StandAlone(app_name)
        modify_premade_view(SDM_app)
        create_connections(SDM_app)
        SDM_app.show()
    else:
        reload(pattern)
        reload(selection)
        try:
            SDM_app._view.close()
            SDM_app._view.deleteLater()
        except:
            pass
            
        SDM_app = src.gui.dcc.Maya('setDressMaster')
        modify_premade_view(SDM_app)
        create_connections(SDM_app)
        SDM_app._view.show()
