import sys

try:
    from PySide2.QtCore import Qt
    from PySide2.QtWidgets import QApplication, QMainWindow, QWidget
except ImportError:
    from PySide.QtCore import Qt
    from PySide.QtGui import QApplication, QMainWindow, QWidget

PYTHON2 = True if sys.version_info.major < 3 else False

import src.gui.main

if PYTHON2:
    reload(src.gui.main)
else:
    from importlib import reload


def standalone():
    if PYTHON2:
        # PySide
        from src.gui import view_qt4
        reload(view_qt4)
        Ui_MK_DCC = view_qt4.Ui_MK_DCC
    else:
        # PySide 2
        from src.gui import view_qt5
        reload(view_qt5)
        Ui_MK_DCC = view_qt5.Ui_MK_DCC

    mk_dcc_app = QApplication(sys.argv)
    mk_dcc_win = src.gui.main.MK_DCC(Ui_MK_DCC)

    mk_dcc_win.show()    
    sys.exit(mk_dcc_app.exec_())


def maya():
    from src.utils.maya.ui import maya_main_window

    # Check Maya's Qt version
    from src.utils.maya.introspection import get_maya_qt_version
    maya_qt_version = get_maya_qt_version()

    if maya_qt_version > 4:
        # PySide 2
        from shiboken2 import wrapInstance
        from src.gui import view_qt5
        reload(view_qt5)
        Ui_MK_DCC = view_qt5.Ui_MK_DCC
    else:
        # PySide
        from shiboken import wrapInstance
        from src.gui import view_qt4
        reload(view_qt4)
        Ui_MK_DCC = view_qt4.Ui_MK_DCC

    mk_dcc_win = src.gui.main.MK_DCC(Ui_MK_DCC)
    mk_dcc_win.setParent(maya_main_window(wrapInstance, QWidget), Qt.Window)

    return mk_dcc_win


def houdini():
    import hou

    # PySide 2
    from src.gui import view_qt5
    reload(view_qt5)

    mk_dcc_win = src.gui.main.MK_DCC(view_qt5.Ui_MK_DCC)
    mk_dcc_win.setParent(hou.ui.mainQtWindow(), Qt.Window)

    return mk_dcc_win


# Invoke the mk_dcc_win:

# Maya

# import src.gui.launch
# reload(src.gui.launch)

# if __name__ == "__main__":
#     try:
#         mk_dcc_win.close()
#         mk_dcc_win.deleteLater()
#     except:
#         pass
        
#     mk_dcc_win = src.gui.launch.maya()
#     mk_dcc_win.show()

# Houdini

# import sys
# sys.path.append('F:/dev/git/mk_dcc')

# import src.gui.launch
# reload(src.gui.launch)

# if __name__ == "hou.session":
#     try:
#         mk_dcc_win.close()
#         mk_dcc_win.deleteLater()
#     except:
#         pass
        
#     mk_dcc_win = src.gui.launch.houdini()
#     mk_dcc_win.show()

if __name__ == '__main__':
    standalone()
    pass
