from pathlib import Path
import logging
from importlib.machinery import SourceFileLoader

logger = logging.getLogger(__name__)
MK_DCC_ROOT = Path(__file__).resolve().parent.parent.parent.parent

import bpy

###################################### Import QtWindowEventLoop ######################################

blender_ui_utils = MK_DCC_ROOT / 'utils/blender/ui.py'

if blender_ui_utils.exists():
    blender_ui_utils = SourceFileLoader('', blender_ui_utils.as_posix()).load_module()

logger.debug('QtWindowEventLoop: {}'.format(blender_ui_utils.QtWindowEventLoop))


######################################### Import Custom UI #########################################

blender_custom_ui = MK_DCC_ROOT / 'gui/blender.py'

if blender_custom_ui.exists():
    blender_custom_ui = SourceFileLoader('', blender_custom_ui.as_posix()).load_module()


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
    bpy.utils.register_class(blender_ui_utils.QtWindowEventLoop)
    bpy.utils.register_class(blender_custom_ui.MK_DCC_WindowOperator)
    bpy.utils.register_class(blender_custom_ui.MK_DCC_QtPanel)

def unregister():
    bpy.utils.unregister_class(blender_ui_utils.QtWindowEventLoop)
    bpy.utils.unregister_class(blender_custom_ui.MK_DCC_WindowOperator)
    bpy.utils.unregister_class(blender_custom_ui.MK_DCC_QtPanel)
