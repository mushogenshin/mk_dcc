import sys
import logging
from src.utils.maya import maya_common


logger = logging.getLogger(__name__)


@maya_common.libs
def maya_main_window(wrapInstance, QWidget, **kwargs):
    '''
    Python 2 only
    :param function wrapInstance: of shiboken module
    :param module QWidget:
    '''
    omui = kwargs[maya_common._OMUI] 
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(long(main_window_ptr), QWidget)


def maya_main_window_qt(QApplication):
    '''
    For Python 3, as `long` is obsolete and `int` doesn't work properly with `wrapInstance`
    :param module QApplication:
    '''
    app = QApplication.instance()  # get the qApp instance if it exists.

    if not app:
        app = QApplication(sys.argv)

    def get_maya_main_window():
        maya_win = next(w for w in app.topLevelWidgets() if w.objectName() == 'MayaWindow')
        return maya_win

    return get_maya_main_window()


@maya_common.libs
def raise_attribute_editor(node=None, **kwargs):
    pmc = kwargs[maya_common._PMC]
    logger.info("Raising Attribute Editor on specified node")
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

    @maya_common.libs
    @staticmethod
    def get_current_shelf(*args, **kwargs):
        cmds = kwargs[maya_common._CMDS]
        mel = kwargs[maya_common._MEL]
        try:
            shelf_top_level = mel.eval("string $_shelf_top_level = $gShelfTopLevel")
            current_shelf = cmds.tabLayout(shelf_top_level, q=True, selectTab=True)
        except Exception:
            return ""
        else:
            return current_shelf

    @maya_common.libs
    def get_existing_buttons_in_shelf(self, **kwargs):
        cmds = kwargs[maya_common._CMDS]
        ret = []
        try:
            ret = cmds.shelfLayout(self.shelf_name, q=True, childArray=True) if self.shelf_name else ret
            ret = [button for button in ret if cmds.shelfButton(button, q=True, exists=True)]
        except Exception:
            pass
        finally:
            return ret

    @maya_common.libs
    def button_with_label_exists_in_shelf(self, button_label, **kwargs):
        cmds = kwargs[maya_common._CMDS]
        for button in self.get_existing_buttons_in_shelf():
            if cmds.shelfButton(button, q=True, label=True) == button_label:
                return True
        else:
            return False

    @maya_common.libs
    def add_button(self, button_label, command="pass", icon="commandButton.png", overlay_icon_with_label=False, **kwargs):
        '''Add a shelf button with the specified label, command, and icon'''
        cmds = kwargs[maya_common._CMDS]
        ret = None
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


@maya_common.libs
def raise_mash_outliner(**kwargs):
    pmc = kwargs[maya_common._PMC]
    logger.info("Raising MASH Outliner")
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


if __name__ == "__main__":
    # print(_IS_PY2)
    pass