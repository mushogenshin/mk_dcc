try:
    from PySide2.QtCore import Qt
    from PySide2.QtWidgets import QMainWindow, QWidget
    from shiboken2 import wrapInstance
except ImportError:
    from PySide.QtCore import Qt
    from PySide.QtGui import QMainWindow, QWidget
    from shiboken import wrapInstance

import sys
PYTHON2 = True if sys.version_info.major < 3 else False


class MK_DCC(QMainWindow):
    '''
    Main UI
    '''
    def __init__(self, Ui_MK_DCC):
        '''
        :param module Ui_MK_DCC: generated uic module, depending on version of uic used
        '''
        super(MK_DCC, self).__init__()
        self.ui = Ui_MK_DCC()
        self.ui.setupUi(self)


def maya():
    import maya
    from mk_dcc.utils.maya.ui import maya_main_window

    # Check Maya's Qt version
    from mk_dcc.utils.maya.introspection import get_maya_qt_version
    maya_qt_version = get_maya_qt_version(maya)

    if maya_qt_version > 4:
        # PySide 2
        from mk_dcc.gui import design_pyside2
        if PYTHON2:
            reload(design_pyside2)

        Ui_MK_DCC = design_pyside2.Ui_MK_DCC
    else:
        # PySide
        from mk_dcc.gui import design_pyside
        if PYTHON2:
            reload(design_pyside)

        Ui_MK_DCC = design_pyside.Ui_MK_DCC
    
    mk_dcc_win = MK_DCC(Ui_MK_DCC)
    mk_dcc_win.setParent(maya_main_window(maya, wrapInstance, QWidget), Qt.Window)

    return mk_dcc_win


def houdini():
    import hou

    # PySide 2
    from mk_dcc.gui import design_pyside2
    if PYTHON2:
        reload(design_pyside2)

    mk_dcc_win = MK_DCC(design_pyside2.Ui_MK_DCC)
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
