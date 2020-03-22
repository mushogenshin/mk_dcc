"""
By Phi Hung, hung.nguyen_a@Virtuos-Sparx.com, aka. Joseph Kirk
"""

import unreal

def refresh():
    unreal.ToolMenus.get().refresh_all_widgets()

def get_mainmenu():
    return unreal.ToolMenus.get().find_menu("MainFrame.MainMenu")

def create_menu_button(name, label , command_string):
    menu_button = unreal.ToolMenuEntry(name, type=unreal.MultiBlockType.MENU_ENTRY)
    menu_button.set_label(label)
    menu_button.set_string_command(unreal.ToolMenuStringCommandType.PYTHON, "python", command_string)
    return menu_button

def create_submenu(name, label, tooltip=""):
    main_menu = get_mainmenu()
    return main_menu.add_sub_menu(main_menu.menu_name, unreal.Name(), name, label , tooltip)
