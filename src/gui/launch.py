import sys

try:
    from PySide2.QtCore import Qt
    from PySide2.QtWidgets import QApplication, QWidget
except ImportError:
    from PySide.QtCore import Qt
    from PySide.QtGui import QApplication, QWidget

PYTHON2 = True if sys.version_info.major < 3 else False

import src.gui.main
if not PYTHON2:
    from importlib import reload
reload(src.gui.main)


def standalone():
    mk_dcc_app = QApplication(sys.argv)
    mk_dcc_win = src.gui.main.MK_DCC()

    mk_dcc_win.show()    
    sys.exit(mk_dcc_app.exec_())

def maya():
    from src.utils.maya.ui import maya_main_window

    # Check Maya's Qt version
    from src.utils.maya.introspection import get_maya_qt_version
    maya_qt_version = get_maya_qt_version()

    if maya_qt_version > 4:
        from shiboken2 import wrapInstance  # PySide 2
    else:
        from shiboken import wrapInstance  # PySide

    mk_dcc_win = src.gui.main.MK_DCC()
    mk_dcc_win.setParent(maya_main_window(wrapInstance, QWidget), Qt.Window)

    return mk_dcc_win

def houdini():
    import hou
    mk_dcc_win = src.gui.main.MK_DCC()
    mk_dcc_win.setParent(hou.ui.mainQtWindow(), Qt.Window)

    return mk_dcc_win


if __name__ == '__main__':
    standalone()
    pass
