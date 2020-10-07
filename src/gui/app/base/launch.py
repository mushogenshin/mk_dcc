import src.gui.dcc

if __name__ == '__main__':
    from src.utils import load_pathlib
    Path = load_pathlib()
    app_name = Path(__file__).parent.stem

    # from src.utils import uic_rebuild
    # uic_rebuild(app_name)
    
    base_app = src.gui.dcc.StandAlone(app_name)
    base_app.show()
    pass
