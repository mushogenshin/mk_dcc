import sys
from pathlib import Path
from importlib.machinery import SourceFileLoader


########################################## Import MainWindow ##########################################

_MK_DCC_ROOT = Path(__file__).parent.parent.parent.parent.parent

mk_dcc_core = SourceFileLoader('', (_MK_DCC_ROOT / 'src/gui/core.py').as_posix()).load_module()
mk_dcc_utils = SourceFileLoader('', (_MK_DCC_ROOT / 'src/utils/__init__.py').as_posix()).load_module()

uic_gen_mod = mk_dcc_utils.load_app_uic_gen_mod('base', False, 5)  # 'app_name' -- change this accordingly for each add-on


################################## Import BlenderWidget QtWindowEventLoop ##################################

import bpy
blender_qt_utils = SourceFileLoader('', (_MK_DCC_ROOT / 'src/utils/blender/qt.py').as_posix()).load_module()

######################################################################################################


class WindowOperator(blender_qt_utils.QtWindowEventLoop):
    '''
    This class will be registered with the add-on
    '''
    bl_idname = 'screen.mk_dcc'
    bl_label = 'MK DCC'

    def __init__(self):
        super(WindowOperator, self).__init__(mk_dcc_core.AbstractMainWindow, uic_gen_mod.Ui_MainWindow)


class QtPanel(bpy.types.Panel):
    '''
    This class will be registered with the add-on
    '''
    bl_label = 'MK DCC'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'MK DCC'
    
    def draw(self, context):
        scene = context.scene
        layout = self.layout
        layout.operator('screen.mk_dcc')


if __name__ == '__main__':
    bpy.utils.register_class(WindowOperator)
    bpy.ops.screen.mk_dcc()
