import logging as logger


def open_content_browser(cmds, main_content_path="", landing_subfolder_name=""):
    """
    :param module cmds: maya.cmds
    :param main_content_path: for example: repo_kitbash_path
    :param landing_subfolder_name: for example: repo_kitbash_folder_name
    :return:
    """

    cmds.scriptedPanel('contentBrowserPanel1', edit=True, tearOff=True, label='Content Browser')
    content_browser_panel_name = cmds.getPanel(scriptType='contentBrowserPanel')[0]
    content_browser_panel_complete_name = content_browser_panel_name + 'ContentBrowser'

    if main_content_path not in os.environ['MAYA_CONTENT_PATH'].split(";"):
        cmds.contentBrowser(content_browser_panel_complete_name, edit=True, addContentPath=main_content_path)

    cmds.contentBrowser(content_browser_panel_complete_name, edit=True,
                        location=landing_subfolder_name.replace("_", " "))

    def remove_unneeded_maya_content_path():

        for maya_content_path_to_remove in cfg.MAYA_DEFAULT_CONTENT_PATH:
            if maya_content_path_to_remove in os.environ['MAYA_CONTENT_PATH'].split(";"):
                try:
                    cmds.contentBrowser(content_browser_panel_complete_name, edit=True,
                                        removeContentPath=maya_content_path_to_remove)
                    logger.info("Removed {0} from Maya's default Content Path environment."
                             .format(maya_content_path_to_remove))
                except:
                    pass

        return True

    remove_unneeded_maya_content_path()

    return True
