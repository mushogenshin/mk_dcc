import sys
from os.path import dirname

try:
    from PySide2.QtCore import Qt
    from PySide2.QtWidgets import QApplication, QMainWindow, QWidget
except ImportError:
    from PySide.QtCore import Qt
    from PySide.QtGui import QApplication, QMainWindow, QWidget

PYTHON2 = True if sys.version_info.major < 3 else False

MK_DCC_ROOT = dirname(dirname(dirname(__file__)))
sys.path.append(MK_DCC_ROOT)
import mk_dcc.gui.main
if PYTHON2:
    reload(mk_dcc.gui.main)
else:
    from importlib import reload


def standalone():
    if PYTHON2:
        # PySide
        from mk_dcc.gui import design_qt4
        reload(design_qt4)
        Ui_MK_DCC = design_qt4.Ui_MK_DCC
    else:
        # PySide 2
        from mk_dcc.gui import design_qt5
        reload(design_qt5)
        Ui_MK_DCC = design_qt5.Ui_MK_DCC

    mk_dcc_app = QApplication(sys.argv)
    mk_dcc_win = mk_dcc.gui.main.MK_DCC(Ui_MK_DCC)

    mk_dcc_win.show()    
    sys.exit(mk_dcc_app.exec_())


def maya():
    import maya
    from mk_dcc.utils.maya.ui import maya_main_window

    # Check Maya's Qt version
    from mk_dcc.utils.maya.introspection import get_maya_qt_version
    maya_qt_version = get_maya_qt_version(maya)

    if maya_qt_version > 4:
        # PySide 2
        from shiboken2 import wrapInstance
        from mk_dcc.gui import design_qt5
        reload(design_qt5)

        Ui_MK_DCC = design_qt5.Ui_MK_DCC
    else:
        # PySide
        from shiboken import wrapInstance
        from mk_dcc.gui import design_qt4
        reload(design_qt4)

        Ui_MK_DCC = design_qt4.Ui_MK_DCC
    
    mk_dcc_win = mk_dcc.gui.main.MK_DCC(Ui_MK_DCC)
    mk_dcc_win.setParent(maya_main_window(maya, wrapInstance, QWidget), Qt.Window)

    return mk_dcc_win


def houdini():
    import hou

    # PySide 2
    from mk_dcc.gui import design_qt5
    reload(design_qt5)

    mk_dcc_win = mk_dcc.gui.main.MK_DCC(design_qt5.Ui_MK_DCC)
    mk_dcc_win.setParent(hou.ui.mainQtWindow(), Qt.Window)

    return mk_dcc_win


# Invoke the mk_dcc_win:

# Maya

# import mk_dcc.gui.launch
# reload(mk_dcc.gui.launch)

# if __name__ == "__main__":
#     try:
#         mk_dcc_win.close()
#         mk_dcc_win.deleteLater()
#     except:
#         pass
        
#     mk_dcc_win = mk_dcc.gui.launch.maya()
#     mk_dcc_win.show()

# Houdini

# import sys
# sys.path.append('F:/dev/git')

# import mk_dcc.gui.launch
# reload(mk_dcc.gui.launch)

# if __name__ == "hou.session":
#     try:
#         mk_dcc_win.close()
#         mk_dcc_win.deleteLater()
#     except:
#         pass
        
#     mk_dcc_win = mk_dcc.gui.launch.houdini()
#     mk_dcc_win.show()

if __name__ == '__main__':
    standalone()
