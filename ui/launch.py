try:
    from PySide2.QtCore import Qt
    from PySide2.QtWidgets import QMainWindow, QWidget
    from shiboken2 import wrapInstance
except ImportError:
    from PySide.QtCore import Qt
    from PySide.QtGui import QMainWindow, QWidget
    from shiboken import wrapInstance


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
        # PySide 2 and above
        from mk_dcc.ui.design_pyside2 import Ui_MK_DCC
    else:
        # PySide
        from mk_dcc.ui.design_pyside import Ui_MK_DCC
    
    window = MK_DCC(Ui_MK_DCC)

    window.setParent(maya_main_window(
        maya.OpenMayaUI, 
        wrapInstance, 
        QWidget
    ), Qt.Window)

    window.show()
