from os import getcwd
from os.path import dirname


MK_DCC_ROOT = dirname(dirname(dirname(__file__)))


def load_app_uic_gen_mod(app_name, use_py2=False, qt_version=5):
    uic_gen_mod = MK_DCC_ROOT + '/src/gui/app/{}/ui_qt{}.py'.format(app_name, qt_version)
    if use_py2:
        import imp
        return imp.load_source('{}_view_qt'.format(app_name), uic_gen_mod)
    else:
        from importlib.machinery import SourceFileLoader
        return SourceFileLoader('{}_view_qt'.format(app_name), uic_gen_mod).load_module()

def load_pathlib2_from_venv():
    import imp  # Python 2 only
    pathlib2 = MK_DCC_ROOT + '/venv27/Lib/site-packages/pathlib2/__init__.py'
    return imp.load_source('pathlib2', pathlib2)

def load_scandir_from_venv():
    import imp  # Python 2 only
    scandir = MK_DCC_ROOT + '/venv27/Lib/site-packages/scandir.py'
    return imp.load_source('scandir', scandir)

