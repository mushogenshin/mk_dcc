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


class ShelfBuilder(object):

    label_background = (0, 0, 0, 0)
    label_color = (1, 1, 1)
    button_size = 37

    def __init__(self, shelf_name="", icon_path_prefix=""):
        """
        Operate on a new shelf if shelf_name is given, otherwise operate on the currently selected shelf
        """
        super(ShelfBuilder, self).__init__()
        self.shelf_name = shelf_name if shelf_name else ShelfBuilder.get_current_shelf()
        self.icon_path_prefix = icon_path_prefix

        # self.clean_old_shelf()
        # self.build_shelf()

    @staticmethod
    def get_current_shelf():
        try:
            import maya.mel as mel
            import maya.cmds as cmds
        except ImportError:
            return ""
        else:
            try:
                shelf_top_level = mel.eval("string $_shelf_top_level = $gShelfTopLevel")
                current_shelf = cmds.tabLayout(shelf_top_level, q=True, selectTab=True)
            except Exception:
                return ""
            else:
                return current_shelf

    def get_existing_buttons_in_shelf(self):
        ret = []
        try:
            import maya.cmds as cmds
        except ImportError:
            return ret
        else:
            try:
                ret = cmds.shelfLayout(self.shelf_name, q=True, childArray=True) if self.shelf_name else ret
                ret = [button for button in ret if cmds.shelfButton(button, q=True, exists=True)]
            except Exception:
                pass
            finally:
                return ret

    def button_with_label_exists_in_shelf(self, button_label):
        try:
            import maya.cmds as cmds
        except ImportError:
            return True
        else:
            for button in self.get_existing_buttons_in_shelf():
                if cmds.shelfButton(button, q=True, label=True) == button_label:
                    return True
            else:
                return False

    def add_button(self, button_label, command="pass", icon="commandButton.png", overlay_icon_with_label=False):
        '''Add a shelf button with the specified label, command, and icon'''
        ret = None
        try:
            import maya.cmds as cmds
        except ImportError:
            pass
        else:
            if not self.button_with_label_exists_in_shelf(button_label):
                from os.path import join
                try:
                    if self.shelf_name:
                        cmds.setParent(self.shelf_name)
                    ret = cmds.shelfButton(
                        label=button_label, 
                        command=command, 
                        sourceType="python",
                        image=join(self.icon_path_prefix, icon), 
                        imageOverlayLabel=button_label if overlay_icon_with_label else "", 
                        width=ShelfBuilder.button_size, 
                        height=ShelfBuilder.button_size, 
                        overlayLabelBackColor=ShelfBuilder.label_background, 
                        overlayLabelColor=ShelfBuilder.label_color
                    )
                except Exception:
                    pass
            else:
                logger.warning('Button with label "{}" already exists in shelf "{}". Skipped.'.format(button_label, self.shelf_name))
        finally:
            return ret

    # def add_menu_item(self, parent, label, command="pass", icon=""):
    #     '''Add a shelf button with the specified label, command, double click command and image.'''
    #     if icon:
    #         icon = self.icon_path_prefix + icon
    #     return cmds.menuItem(p=parent, l=label, c=command, i="")

    # def add_sub_menu(self, parent, label, icon=None):
    #     '''Add a sub menu item with the specified label and icon to the specified parent popup menu.'''
    #     if icon:
    #         icon = self.icon_path_prefix + icon
    #     return cmds.menuItem(p=parent, l=label, i=icon, subMenu=1)

    # def clean_old_shelf(self):
    #     '''Check if the shelf exists and empties it if it does or creates it if it does not.'''
    #     if cmds.shelfLayout(self.shelf_name, ex=1):
    #         if cmds.shelfLayout(self.shelf_name, q=1, childArray=True):
    #             for each in cmds.shelfLayout(self.shelf_name, q=1, childArray=True):
    #                 cmds.deleteUI(each)
    #     else:
    #         cmds.shelfLayout(self.shelf_name, p="ShelfLayout")

    # def build_shelf(self):
    #     cmds.setParent(self.shelf_name)
    #     pass


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
