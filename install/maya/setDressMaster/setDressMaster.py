from os.path import dirname


_SetDressMaster_shelf_button_command = """import sys
sys.path.append("{0}")

import src.gui.dcc
import src.gui.app.setDressMaster.view_wrapper as view_wrapper

import pymel.core as pmc

try:
    SDM_app._view.close()
    SDM_app._view.deleteLater()
except Exception:
    pass
    
SDM_app = src.gui.dcc.Maya("setDressMaster")
view_wrapper.modify_premade_view(SDM_app)
view_wrapper.create_connections(SDM_app)
view_wrapper.init_gui(SDM_app)
SDM_app._view.show()
"""


def add_repo_root_to_sys_path():
    repo_root = dirname(dirname(dirname(dirname(__file__))))
    
    print("Adding mk_dcc root to sys.path:", repo_root)
    import sys
    sys.path.append(repo_root)

    return repo_root
    

def get_icon_path_prefix():
    from os.path import join
    return join(dirname(__file__), "icons")


def make_button(command, repo_root, icon_path_prefix):
    from src.utils.maya.ui_utils import ShelfBuilder
    
    shelf_builder = ShelfBuilder(icon_path_prefix=icon_path_prefix)  # using current shelf
    print('Making button for "Set Dress Master" in current shelf')

    shelf_builder.add_button(
        "SetDressMaster",
        command=command.format(repo_root),
        icon="setDressMaster_icon.png"
    )


def onMayaDroppedPythonFile(*args, **kwargs):
    repo_root = add_repo_root_to_sys_path()

    import src.gui.dcc
    import src.gui.app.setDressMaster.view_wrapper as view_wrapper

    import pymel.core as pmc

    try:
        SDM_app._view.close()
        SDM_app._view.deleteLater()
    except Exception:
        pass
        
    SDM_app = src.gui.dcc.Maya("setDressMaster")
    view_wrapper.modify_premade_view(SDM_app)
    view_wrapper.create_connections(SDM_app)
    view_wrapper.init_gui(SDM_app)
    SDM_app._view.show()
    
    make_button(
        _SetDressMaster_shelf_button_command,
        repo_root, 
        get_icon_path_prefix()
    )


if __name__ == "__main__":
    repo_root = add_repo_root_to_sys_path()
    make_button(
        _SetDressMaster_shelf_button_command,
        repo_root, 
        get_icon_path_prefix()
    )
