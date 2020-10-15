import sys
import platform
import logging
from os.path import dirname
from functools import partial, wraps


is_py2 = True if sys.version_info.major < 3 else False
logger = logging.getLogger(__name__)
_PLATFORM_SYSTEM = platform.system()
MK_DCC_ROOT = dirname(dirname(dirname(__file__)))


# def maya_python(func):

#     @wraps(func)
#     def wrapper(*args, **kwargs):
#         print("Calling decorated function")
#         try:
#             import maya.cmds as cmds
#             import pymel.core as pmc
#         except ImportError:
#             print("Unable to import maya.cmds and pymel.core")
#         else:
#             print("Maya.cmds: {}".format(cmds))
#             print("Pymel.core: {}".format(pmc))
#             return func(*args, **kwargs)

#     return wrapper


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


load_app_model_module = partial(load_app_MVC, module="model")
load_app_control_module = partial(load_app_MVC, module="control")


def load_model_component(app_name, is_py2):
    model = None
    try:
        model = load_app_model_module(app_name, is_py2)
    except Exception as e:
        logger.exception("Unable to load app Model of {} due to {}".format(app_name, e))
        return None
    else:
        logger.info("App Model of {} loaded successfully: {}".format(app_name, model))
        if hasattr(model, "Model"):
            return model.Model()


def load_control_component(app_name, is_py2):
    control = None
    try:
        control = load_app_control_module(app_name, is_py2)
    except Exception as e:
        logger.exception("Unable to load app Control of {} due to {}".format(app_name, e))
        return None
    else:
        logger.info("App Control of {} loaded successfully: {}".format(app_name, control))
        if hasattr(control, "Control"):
            return control.Control()


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
            # Qt5
            subprocess.call([
                MK_DCC_ROOT + '/.venv3/Scripts/pyside2-uic.exe',
                ui_file,
                "-o",
                rebuilt_qt5
            ])
            rename_resources_rc_module(app_name, rebuilt_qt5, 5)

            # Qt4
            subprocess.call([
                MK_DCC_ROOT + '/.venv2/Scripts/pyside-uic.exe',
                ui_file,
                "-o",
                rebuilt_qt4
            ])
            rename_resources_rc_module(app_name, rebuilt_qt4, 4)
        except:
            pass


def rename_resources_rc_module(app_name, uic_output_path, qt_version):
    """
    :param str uic_output_path: path to the uic-generated file
    """
    import inspect
    func_name = inspect.currentframe().f_code.co_name
    print("***(!) Ensure that {} is being enabled (!)***".format(func_name))

    # # DANGER: Maya will fail to parse this, but it won't tell you so

    # import fileinput
    # replaced = 'from src.gui.app.{} import resources_rc_qt{}'

    # if is_py2:
    #     for line in fileinput.input(files=uic_output_path, inplace=True):
    #         print(
    #             line.replace(
    #                 'import resources_rc', 
    #                 replaced.format(app_name, qt_version)
    #             ), 
    #             end=''
    #         )
    # else:
    #     with fileinput.input(files=uic_output_path, inplace=True) as uic_output_file:
    #         for line in uic_output_file:
    #             print(
    #                 line.replace(
    #                     'import resources_rc', 
    #                     replaced.format(app_name, qt_version)
    #                 ),
    #                 end=''
    #             )

    # pass
