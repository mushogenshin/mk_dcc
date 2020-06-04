from pathlib import Path
import logging
from importlib.machinery import SourceFileLoader

logger = logging.getLogger(__name__)
MK_DCC_ROOT = Path(__file__).resolve().parent.parent.parent.parent  # resolving symbolic link

import bpy

################################## Import Blender QtWindowEventLoop ##################################

qt_utils = MK_DCC_ROOT / 'src/utils/blender/qt.py'
qt_utils = SourceFileLoader('', qt_utils.as_posix()).load_module()
# logger.debug('QtWindowEventLoop: {}'.format(qt_utils.QtWindowEventLoop))

######################################### Import Custom UI #########################################

mk_dcc_blender = MK_DCC_ROOT / 'src/gui/app/base/blender.py'  # change this accordingly for each add-on
mk_dcc_blender = SourceFileLoader('', mk_dcc_blender.as_posix()).load_module()

########################################## Register Add-on ##########################################

bl_info = {
    "name" : "MK DCC",
    "author" : "Mushogenshin K",
    "description" : "",
    "blender" : (2, 82, 0),
    "version" : (0, 0, 1),
    "location" : "",
    "warning" : "",
    "category" : "Generic"
}

def register():
    bpy.utils.register_class(qt_utils.QtWindowEventLoop)
    bpy.utils.register_class(mk_dcc_blender.WindowOperator)
    bpy.utils.register_class(mk_dcc_blender.QtPanel)

def unregister():
    bpy.utils.unregister_class(qt_utils.QtWindowEventLoop)
    bpy.utils.unregister_class(mk_dcc_blender.WindowOperator)
    bpy.utils.unregister_class(mk_dcc_blender.QtPanel)
