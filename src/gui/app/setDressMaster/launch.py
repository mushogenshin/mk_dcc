import sys
from src.gui.dcc import StandAlone
from src.utils.qt import pattern


is_py2 = True if sys.version_info.major < 3 else False


def add_widgets(ui):

    load_label = "Load"
    clear_label = "X"

    load_cloud_pattern = pattern.LoadAndDisplayToLineEdit(
        "1. Cloud", load_label, clear_label, add_to_container=False
    )
    load_scatter_pattern = pattern.LoadAndDisplayToLineEdit(
        "2. Scatter",  load_label, clear_label, add_to_container=False
    )
    load_ground_pattern = pattern.LoadAndDisplayToLineEdit(
        "3. Grounds",  load_label, clear_label, add_to_container=False
    )

    for i, layout_pattern in enumerate(
        [load_cloud_pattern, load_scatter_pattern, load_ground_pattern]
    ):
        ui.phys_painter_load_selection_grid_layout.addWidget(
            layout_pattern.label, i, 0
        )
        ui.phys_painter_load_selection_grid_layout.addWidget(
            layout_pattern.line_edit, i, 1
        )
        ui.phys_painter_load_selection_grid_layout.addWidget(
            layout_pattern.load_btn, i, 2
        )

        layout_pattern.clear_btn.setMaximumWidth(20)
        ui.phys_painter_load_selection_grid_layout.addWidget(
            layout_pattern.clear_btn, i, 3
        )
    pass


def modify_view(app):
    add_widgets(app._view.ui)


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

        SDM_app = StandAlone(app_name)
        modify_view(SDM_app)
        SDM_app.show()
    else:
        try:
            SDM_app._view.close()
            SDM_app._view.deleteLater()
        except:
            pass
            
        SDM_app = src.gui.dcc.Maya('setDressMaster')
        modify_view(SDM_app)
        SDM_app._view.show()
