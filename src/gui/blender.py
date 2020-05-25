import sys
from pathlib import Path
from importlib.machinery import SourceFileLoader


########################################## Import MainWindow ##########################################

_MK_DCC_ROOT = Path(__file__).parent.parent.parent
MK_DCC_Main = SourceFileLoader('', (_MK_DCC_ROOT / 'src/gui/main.py').as_posix()).load_module()


class MK_DCC_Qt5(MK_DCC_Main.MK_DCC):
    def __init__(self):
        super(MK_DCC_Qt5, self).__init__()
        self.show()  # must-have


################################## Import Blender QtWindowEventLoop ##################################

import bpy

blender_qt_utils = SourceFileLoader('', (_MK_DCC_ROOT / 'src/utils/blender/qt.py').as_posix()).load_module()

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
    
    def draw(self, context):
        scene = context.scene
        layout = self.layout
        layout.operator('screen.mk_dcc')


if __name__ == '__main__':
    bpy.utils.register_class(MK_DCC_WindowOperator)
    bpy.ops.screen.mk_dcc()
