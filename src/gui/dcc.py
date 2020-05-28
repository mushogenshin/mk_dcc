import sys

try:
    from PySide2.QtCore import Qt
    from PySide2.QtWidgets import QApplication, QWidget
except ImportError:
    from PySide.QtCore import Qt
    from PySide.QtGui import QApplication, QWidget

from src.gui.core import AbstractMainWindow
from src.utils import load_app_view_qt_module

PYTHON2 = True if sys.version_info.major < 3 else False


class StandAlone(object):
    def __init__(self, app_name):
        qt_version = 4 if PYTHON2 else 5
        view_qt = load_app_view_qt_module(app_name, PYTHON2, qt_version)

        self.app = QApplication(sys.argv)
        self.win = AbstractMainWindow(view_qt.Ui_MainWindow)
        self.win.show()
        sys.exit(self.app.exec_())


class Maya(object):
    def __init__(self, app_name):
        # Check Maya's Qt version
        from src.utils.maya.introspection import get_maya_qt_version
        from src.utils.maya.ui import maya_main_window

        maya_qt_version = get_maya_qt_version()
        view_qt = load_app_view_qt_module(app_name, PYTHON2, maya_qt_version)

        if maya_qt_version > 4:
            from shiboken2 import wrapInstance  # PySide 2
        else:
            from shiboken import wrapInstance  # PySide

        self.win = AbstractMainWindow(view_qt.Ui_MainWindow)
        self.win.setParent(maya_main_window(wrapInstance, QWidget), Qt.Window)


class Houdini(object):
    def __init__(self, app_name):
        import hou
        view_qt = load_app_view_qt_module(app_name, PYTHON2, 5)

        self.win = AbstractMainWindow(view_qt.Ui_MainWindow)
        self.win.setParent(hou.ui.mainQtWindow(), Qt.Window)
    

if __name__ == '__main__':
    # test with 'base' app
    base_app = StandAlone('base')

    pass
