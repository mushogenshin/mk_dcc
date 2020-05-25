import sys
from pathlib import Path
from importlib.machinery import SourceFileLoader
from PySide2.QtWidgets import QApplication, QMainWindow

MK_DCC_ROOT = Path(__file__).parent.parent

########################################## Import MainWindow ##########################################

MK_DCC_Main = MK_DCC_ROOT / 'gui/main.py'
MK_DCC_UI = MK_DCC_ROOT / 'gui/view_qt5.py'

MK_DCC_Main = SourceFileLoader('', MK_DCC_Main.as_posix()).load_module()
MK_DCC_UI = SourceFileLoader('', MK_DCC_UI.as_posix()).load_module()


class MK_DCC_Qt5(MK_DCC_Main.MK_DCC, QMainWindow):
    def __init__(self):
        super(MK_DCC_Qt5, self).__init__(MK_DCC_UI.Ui_MK_DCC)
        self.show()  # must-have

######################################################################################################

import bpy

################################## Import Blender QtWindowEventLoop ##################################

blender_qt_utils = MK_DCC_ROOT / 'utils/blender/qt.py'

if blender_qt_utils.exists():
    blender_qt_utils = SourceFileLoader('', blender_qt_utils.as_posix()).load_module()

######################################################################################################


class MK_DCC_WindowOperator(blender_qt_utils.QtWindowEventLoop):

    bl_idname = 'screen.mk_dcc'
    bl_label = 'MK DCC'

    def __init__(self):
        super(MK_DCC_WindowOperator, self).__init__(MK_DCC_Qt5)


class MK_DCC_QtPanel(bpy.types.Panel):
    
    bl_label = 'MK DCC'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'MK DCC'

    # def __init__(self, context):
    #     scene = context.scene
    #     layout = self.layout
    #     layout.operator('screen.mk_dcc')
    
    def draw(self, context):
        scene = context.scene
        layout = self.layout
        layout.operator('screen.mk_dcc')


if __name__ == '__main__':
    # mk_dcc_app = QApplication(sys.argv)
    # mk_dcc_win = MK_DCC_Qt5()
    # mk_dcc_win.show()    
    # sys.exit(mk_dcc_app.exec_())

    bpy.utils.register_class(MK_DCC_WindowOperator)
    bpy.ops.screen.mk_dcc()
