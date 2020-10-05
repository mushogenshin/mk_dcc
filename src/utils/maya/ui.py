import os
import logging as logger


MAYA_DEFAULT_CONTENT_PATH = ['C:/Program Files/Autodesk/Maya2018/Examples',
                             'C:/Program Files/Autodesk/Bifrost/Maya2018/examples/Bifrost_Fluids',
                             'C:/Program Files/Autodesk/Maya2018/plug-ins/MASH/MASH Examples',
                             'C:/Program Files/Autodesk/Maya2018/plug-ins/MASH/Smart Presets']


def maya_main_window(wrapInstance, QWidget):
    '''
    :param function wrapInstance: of shiboken module
    :param module QWidget:
    '''
    import maya
    main_window_ptr = maya.OpenMayaUI.MQtUtil.mainWindow()
    return wrapInstance(long(main_window_ptr), QWidget)


def open_content_browser(main_content_path="", landing_subfolder_name=""):
    """
    :param main_content_path: for example: repo_kitbash_path
    :param landing_subfolder_name: for example: repo_kitbash_folder_name
    :return:
    """
    import maya

    maya.cmds.scriptedPanel('contentBrowserPanel1', edit=True, tearOff=True, label='Content Browser')
    content_browser_panel_name = maya.cmds.getPanel(scriptType='contentBrowserPanel')[0]
    content_browser_panel_complete_name = content_browser_panel_name + 'ContentBrowser'

    if main_content_path not in os.environ['MAYA_CONTENT_PATH'].split(";"):
        maya.cmds.contentBrowser(content_browser_panel_complete_name, edit=True, addContentPath=main_content_path)

    maya.cmds.contentBrowser(content_browser_panel_complete_name, edit=True,
                        location=landing_subfolder_name.replace("_", " "))

    def remove_unneeded_maya_content_path():

        for maya_content_path_to_remove in MAYA_DEFAULT_CONTENT_PATH:
            if maya_content_path_to_remove in os.environ['MAYA_CONTENT_PATH'].split(";"):
                try:
                    maya.cmds.contentBrowser(content_browser_panel_complete_name, edit=True,
                                        removeContentPath=maya_content_path_to_remove)
                    logger.info("Removed {0} from Maya's default Content Path environment."
                             .format(maya_content_path_to_remove))
                except:
                    pass

        return True

    remove_unneeded_maya_content_path()

    return True
