def get_maya_qt_version(maya):
    '''
    :param module maya: Autodesk's maya scripting library
    '''
    return int(maya.cmds.about(qt=True).partition('.')[0])

def get_maya_version(maya):
    pass