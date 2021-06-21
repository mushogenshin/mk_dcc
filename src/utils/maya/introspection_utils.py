from src.utils.maya import maya_common

@maya_common.libs
def get_maya_qt_version(*args, **kwargs):
    '''
    return int major of Maya Qt version
    '''
    cmds = kwargs[maya_common._CMDS]
    return int(cmds.about(qt=True).partition('.')[0])
