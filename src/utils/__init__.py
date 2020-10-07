import sys
import platform
from os.path import dirname
from functools import partial


is_py2 = True if sys.version_info.major < 3 else False
_PLATFORM_SYSTEM = platform.system()
MK_DCC_ROOT = dirname(dirname(dirname(__file__)))


def load_app_uic_gen_mod(app_name, is_py2=False, qt_version=5):
    uic_gen_mod = MK_DCC_ROOT + '/src/gui/app/{}/ui_qt{}.py'.format(app_name, qt_version)
    if is_py2:
        import imp
        return imp.load_source('{}_view_qt'.format(app_name), uic_gen_mod)
    else:
        from importlib.machinery import SourceFileLoader
        return SourceFileLoader('{}_view_qt'.format(app_name), uic_gen_mod).load_module()


def load_app_MVC(app_name, is_py2, module):
    """
    :param str module: either "control" or "model"
    """
    module_path = MK_DCC_ROOT + '/src/gui/app/{}/{}.py'.format(app_name, module)
    if is_py2:
        import imp
        return imp.load_source(module, module_path)
    else:
        from importlib.machinery import SourceFileLoader
        return SourceFileLoader(module, module_path).load_module()


def load_pathlib():
    if not is_py2:
        from pathlib import Path
    else:
        from pathlib2 import Path
    return Path


def load_pathlib2_from_venv():
    import imp  # Python 2 only
    if _PLATFORM_SYSTEM == "Windows":
        pathlib2 = MK_DCC_ROOT + '/.venv2/Lib/site-packages/pathlib2/__init__.py'
    elif _PLATFORM_SYSTEM == "Darwin":
        pathlib2 = MK_DCC_ROOT + '/.venv2/lib/python2.7/site-packages/pathlib2/__init__.py'
    return imp.load_source('pathlib2', pathlib2)


def load_scandir_from_venv():
    import imp  # Python 2 only
    if _PLATFORM_SYSTEM == "Windows":
        scandir = MK_DCC_ROOT + '/.venv2/Lib/site-packages/scandir.py'
    elif _PLATFORM_SYSTEM == "Darwin":
        scandir = MK_DCC_ROOT + '/.venv2/lib/python2.7/site-packages/scandir.py'
    return imp.load_source('scandir', scandir)


def uic_rebuild(app_name):
    import subprocess
    if _PLATFORM_SYSTEM == "Windows":
        ui_file = MK_DCC_ROOT + '/src/gui/app/{}/ui.ui'.format(app_name)
        rebuilt_qt5 = MK_DCC_ROOT + '/src/gui/app/{}/ui_qt5.py'.format(app_name)
        rebuilt_qt4 = MK_DCC_ROOT + '/src/gui/app/{}/ui_qt4.py'.format(app_name)
        try:
            subprocess.call([
                MK_DCC_ROOT + '/.venv3/Scripts/pyside2-uic.exe',
                ui_file,
                "-o",
                rebuilt_qt5
            ])
            subprocess.call([
                MK_DCC_ROOT + '/.venv2/Scripts/pyside-uic.exe',
                ui_file,
                "-o",
                rebuilt_qt4
            ])
        except:
            pass


load_app_control = partial(load_app_MVC, module="control")
load_app_model = partial(load_app_MVC, module="model")
