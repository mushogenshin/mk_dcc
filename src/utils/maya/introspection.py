import maya

def get_maya_qt_version():
    '''
    return int major of Maya Qt version
    '''
    return int(maya.cmds.about(qt=True).partition('.')[0])

def get_maya_version():
    print('Maya version: ')
    pass