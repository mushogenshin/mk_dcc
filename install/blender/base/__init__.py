from pathlib import Path
from importlib.machinery import SourceFileLoader

# import logging

# logger = logging.getLogger('blender_id')
# logger.setLevel(logging.DEBUG)

# formatter = logging.Formatter('%(levelname)s:%(message)s')
# stream_handler = logging.StreamHandler()
# stream_handler.setFormatter(formatter)
# stream_handler.setLevel(logging.DEBUG)
# file_handler = logging.FileHandler('log.txt')
# file_handler.setFormatter(formatter)
# file_handler.setLevel(logging.DEBUG)

# logger.addHandler(stream_handler)
# logger.addHandler(file_handler)


# Resolving symbolic link
app_name = Path(__file__).resolve().parent.stem
MK_DCC_ROOT = Path(__file__).resolve().parent.parent.parent.parent

import bpy

################################## Import Blender QtWindowEventLoop ##################################

qt_utils = MK_DCC_ROOT / 'src/utils/blender/qt_utils.py'
qt_utils = SourceFileLoader('', qt_utils.as_posix()).load_module()
# logger.debug('QtWindowEventLoop: {}'.format(qt_utils.QtWindowEventLoop))

######################################### Import Custom UI #########################################

mk_dcc_blender = MK_DCC_ROOT / 'src/gui/app/{}/blender.py'.format(app_name)
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
