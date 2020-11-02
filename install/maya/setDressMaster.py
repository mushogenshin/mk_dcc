def onMayaDroppedPythonFile(*args, **kwargs):
    from os.path import dirname
    mk_dcc_root = dirname(dirname(dirname(__file__)))

    print("Adding mk_dcc root to sys.path:", mk_dcc_root)
    
    import sys
    sys.path.append(mk_dcc_root)

    import src.gui.dcc
    import src.gui.app.setDressMaster.view_wrapper as view_wrapper

    import pymel.core as pmc

    try:
        SDM_app._view.close()
        SDM_app._view.deleteLater()
    except:
        pass
        
    SDM_app = src.gui.dcc.Maya('setDressMaster')
    view_wrapper.modify_premade_view(SDM_app)
    view_wrapper.create_connections(SDM_app)
    view_wrapper.init_gui(SDM_app)
    SDM_app._view.show()
