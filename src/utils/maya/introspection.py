
def get_maya_qt_version():
    '''
    return int major of Maya Qt version
    '''
    import maya
    return int(maya.cmds.about(qt=True).partition('.')[0])

# def get_maya_version():
#     import maya
#     # TODO
#     # print('Maya version: ')
#     pass