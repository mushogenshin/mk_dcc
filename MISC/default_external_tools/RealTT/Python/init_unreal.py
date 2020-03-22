import unreal
import jk_ui_lib
import STW_tt

def register_menus():
    """
    Borrowed heavily from Phi Hung, hung.nguyen_a@Virtuos-Sparx.com, aka. Joseph Kirk
    """

    # declare menu entry
    tt_setup_btn = jk_ui_lib.create_menu_button('tt_setup_btn', 'Step 1: Setup TT', 'STW_tt.setup_tt()')
    tt_focus_cam_btn = jk_ui_lib.create_menu_button('tt_focus_cam_btn', '* Focus Cam at Actor', 'STW_tt.focus_cam_at_actor()')
    tt_export_btn = jk_ui_lib.create_menu_button('tt_export_btn', 'Step 2: Export TT', 'STW_tt.export_tt()')
    tt_versioning_btn = jk_ui_lib.create_menu_button('tt_versioning_btn', 'Step 3: Commit as Latest', 'STW_tt.versioning_tt()')
    tt_show_results_btn = jk_ui_lib.create_menu_button('tt_show_results_btn', '* Show TT Results', 'STW_tt.show_results()')

    # create new menu on main menu
    stw_mainmenu = jk_ui_lib.create_submenu('stw_tools', 'STWookiees Tools')
    stw_mainmenu.add_section('tt_tools')
    stw_mainmenu.add_menu_entry('tt_tools', tt_setup_btn)
    stw_mainmenu.add_menu_entry('tt_tools', tt_focus_cam_btn)
    stw_mainmenu.add_menu_entry('tt_tools', tt_export_btn)
    stw_mainmenu.add_menu_entry('tt_tools', tt_versioning_btn)
    stw_mainmenu.add_menu_entry('tt_tools', tt_show_results_btn)

    # refresh menu
    jk_ui_lib.refresh()

def main():
    register_menus()

main()