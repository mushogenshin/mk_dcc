import sys
import logging

try:
    from PySide2.QtCore import Qt
    from PySide2.QtWidgets import QApplication, QWidget
except ImportError:
    from PySide.QtCore import Qt
    from PySide.QtGui import QApplication, QWidget

from src.gui.core import AbstractMainWindow

is_py2 = True if sys.version_info.major < 3 else False
logger = logging.getLogger(__name__)


class StandAlone(object):
    def __init__(self, app_name):
        import src.utils
        qt_version = 4 if is_py2 else 5
        uic_gen_mod = src.utils.load_app_uic_gen_mod(app_name, is_py2, qt_version)

        self._app = QApplication(sys.argv)

        self._model = src.utils.load_model_component(app_name, is_py2)
        self._control = src.utils.load_control_component(app_name, is_py2)
        self._control._model = self._model

        self._view = AbstractMainWindow(uic_gen_mod.Ui_MainWindow, self._control)

    def show(self):
        self._view.show()
        sys.exit(self._app.exec_())


class Maya(object):
    def __init__(self, app_name):
        import src.utils
        
        if is_py2:
            reload(src.utils)

        # Check Maya's Qt version
        from src.utils.maya.introspection_utils import get_maya_qt_version
        from src.utils.maya.ui_utils import maya_main_window

        maya_qt_version = get_maya_qt_version()
        uic_gen_mod = src.utils.load_app_uic_gen_mod(app_name, is_py2, maya_qt_version)

        if maya_qt_version > 4:
            from shiboken2 import wrapInstance  # PySide 2
        else:
            from shiboken import wrapInstance  # PySide

        self._model = src.utils.load_model_component(app_name, is_py2)
        self._control = src.utils.load_control_component(app_name, is_py2)
        self._control._model = self._model

        self._view = AbstractMainWindow(uic_gen_mod.Ui_MainWindow, self._control)
        self._view.setParent(maya_main_window(wrapInstance, QWidget), Qt.Window)


class Houdini(object):
    def __init__(self, app_name):
        import src.utils
        import hou
        uic_gen_mod = src.utils.load_app_uic_gen_mod(app_name, is_py2, 5)

        self._model = src.utils.load_model_component(app_name, is_py2)
        self._control = src.utils.load_control_component(app_name, is_py2)
        self._control._model = self._model

        self._view = AbstractMainWindow(uic_gen_mod.Ui_MainWindow, self._control)
        self._view.setParent(hou.ui.mainQtWindow(), Qt.Window)
