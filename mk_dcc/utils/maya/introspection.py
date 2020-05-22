import maya

def get_maya_qt_version():
    '''
    :param module maya: Autodesk's maya scripting library
    '''
    return int(maya.cmds.about(qt=True).partition('.')[0])

def get_maya_version():
    print('Maya version: ')
    pass