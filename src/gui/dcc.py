import sys

try:
    from PySide2.QtCore import Qt
    from PySide2.QtWidgets import QApplication, QWidget
except ImportError:
    from PySide.QtCore import Qt
    from PySide.QtGui import QApplication, QWidget

from src.gui.core import AbstractMainWindow
from src.utils import load_app_uic_gen_mod

py2 = True if sys.version_info.major < 3 else False


class StandAlone(object):
    def __init__(self, app_name):
        qt_version = 4 if py2 else 5
        uic_gen_mod = load_app_uic_gen_mod(app_name, py2, qt_version)

        self._app = QApplication(sys.argv)
        self._model = None
        self._control = None
        self._view = AbstractMainWindow(uic_gen_mod.Ui_MainWindow, self._control)
        
        self._view.show()
        sys.exit(self._app.exec_())


class Maya(object):
    def __init__(self, app_name):
        # Check Maya's Qt version
        from src.utils.maya.introspection import get_maya_qt_version
        from src.utils.maya.ui import maya_main_window

        maya_qt_version = get_maya_qt_version()
        uic_gen_mod = load_app_uic_gen_mod(app_name, py2, maya_qt_version)

        if maya_qt_version > 4:
            from shiboken2 import wrapInstance  # PySide 2
        else:
            from shiboken import wrapInstance  # PySide

        self._model = None
        self._control = None
        self._view = AbstractMainWindow(uic_gen_mod.Ui_MainWindow, self._control)

        self._view.setParent(maya_main_window(wrapInstance, QWidget), Qt.Window)


class Houdini(object):
    def __init__(self, app_name):
        import hou
        uic_gen_mod = load_app_uic_gen_mod(app_name, py2, 5)

        self._model = None
        self._control = None
        self._view = AbstractMainWindow(uic_gen_mod.Ui_MainWindow, self._control)

        self._view.setParent(hou.ui.mainQtWindow(), Qt.Window)


if __name__ == '__main__':
    base_app = StandAlone('base')
