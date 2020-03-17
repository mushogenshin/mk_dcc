try:
    from PySide2.QtCore import Qt
    from PySide2.QtWidgets import QMainWindow, QWidget
    from shiboken2 import wrapInstance
except ImportError:
    from PySide.QtCore import Qt
    from PySide.QtWidgets import QMainWindow, QWidget
    from shiboken import wrapInstance

from mk_dcc.utils.maya.ui import maya_main_window
from mk_dcc.ui.design import Ui_MK_DCC

class MK_DCC(QMainWindow):
    '''
    Load Qt UI from generated uic module
    '''
    def __init__(self):
        super(MK_DCC, self).__init__()
        self.ui = Ui_MK_DCC()
        self.ui.setupUi(self)

def maya():
    import maya.OpenMayaUI

    window = MK_DCC()

    window.setParent(maya_main_window(
        maya.OpenMayaUI, 
        wrapInstance, 
        QWidget
    ), Qt.Window)

    window.show()
