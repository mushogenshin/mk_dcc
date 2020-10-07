import os
import logging


logger = logging.getLogger(__name__)


def maya_main_window(wrapInstance, QWidget):
    '''
    :param function wrapInstance: of shiboken module
    :param module QWidget:
    '''
    import maya.OpenMayaUI as omui
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(long(main_window_ptr), QWidget)


def raise_attribute_editor(node=None):
    logger.info("Raising Attribute Editor on specified node")
    try:
        import pymel.core as pmc
    except ImportError:
        pass
    else:
        if node:
            pmc.select(node, r=True)
            pmc.mel.AttributeEditor()  # raise the Attribute Editor
            pmc.mel.updateAE(node)  # update it


def raise_mash_outliner():
    logger.info("Raising MASH Outliner")
    try:
        import pymel.core as pmc
    except ImportError:
        pass
    else:
        pmc.mel.MASHOutliner()
            

# def open_content_browser(main_content_path="", landing_subfolder_name=""):
#     """
#     :param main_content_path: for example: repo_kitbash_path
#     :param landing_subfolder_name: for example: repo_kitbash_folder_name
#     :return:
#     """
#     import maya.cmds as cmds

#     MAYA_DEFAULT_CONTENT_PATH = ['C:/Program Files/Autodesk/Maya2018/Examples',
#                              'C:/Program Files/Autodesk/Bifrost/Maya2018/examples/Bifrost_Fluids',
#                              'C:/Program Files/Autodesk/Maya2018/plug-ins/MASH/MASH Examples',
#                              'C:/Program Files/Autodesk/Maya2018/plug-ins/MASH/Smart Presets']

#     cmds.scriptedPanel('contentBrowserPanel1', edit=True, tearOff=True, label='Content Browser')
#     content_browser_panel_name = cmds.getPanel(scriptType='contentBrowserPanel')[0]
#     content_browser_panel_complete_name = content_browser_panel_name + 'ContentBrowser'

#     if main_content_path not in os.environ['MAYA_CONTENT_PATH'].split(";"):
#         cmds.contentBrowser(content_browser_panel_complete_name, edit=True, addContentPath=main_content_path)

#     cmds.contentBrowser(content_browser_panel_complete_name, edit=True,
#                         location=landing_subfolder_name.replace("_", " "))

#     def remove_unneeded_maya_content_path():

#         for maya_content_path_to_remove in MAYA_DEFAULT_CONTENT_PATH:
#             if maya_content_path_to_remove in os.environ['MAYA_CONTENT_PATH'].split(";"):
#                 try:
#                     cmds.contentBrowser(content_browser_panel_complete_name, edit=True,
#                                         removeContentPath=maya_content_path_to_remove)
#                     logger.info("Removed {0} from Maya's default Content Path environment."
#                              .format(maya_content_path_to_remove))
#                 except:
#                     pass

#         return True

#     remove_unneeded_maya_content_path()

#     return True
