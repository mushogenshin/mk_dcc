import logging
logging.basicConfig(level=logging.INFO)


import src.gui.dcc
import src.gui.app.setDressMaster.view_wrapper as view_wrapper


if __name__ == '__main__':
    try:
        import pymel.core as pmc
    except ImportError:
        from src.utils import load_pathlib
        Path = load_pathlib()
            
        app_name = Path(__file__).parent.stem

        from src.utils import uic_rebuild
        # uic_rebuild(app_name)

        SDM_app = src.gui.dcc.StandAlone(app_name)
        view_wrapper.modify_premade_view(SDM_app)
        view_wrapper.create_connections(SDM_app)
        view_wrapper.init_gui(SDM_app)
        SDM_app.show()
    else:
        # reload(src.gui.dcc)
        # reload(view_wrapper)
        try:
            SDM_app._view.close()
            SDM_app._view.deleteLater()
        except Exception:
            pass
            
        SDM_app = src.gui.dcc.Maya('setDressMaster')
        view_wrapper.modify_premade_view(SDM_app)
        view_wrapper.create_connections(SDM_app)
        view_wrapper.init_gui(SDM_app)
        SDM_app._view.show()
