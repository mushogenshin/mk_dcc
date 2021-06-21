"""
__author__ = "Truong CG Artist"
__email__ = "truongcgartist@gmail.com"
"""

def onMayaDroppedPythonFile(*args, **kwargs):
    print("Python file dropped into Maya")
    reset_all_windows()
    reset_all_panels()


def reset_all_windows():
    import maya.cmds as cmds
    ret = False
    open_windows = cmds.lsUI(windows=True)

    for win in open_windows:
        if win != "MayaWindow":
            cmds.deleteUI(win)
            cmds.windowPref(win, remove=True)
            print('Window "{}" deleted and reset.'.format(win))
    else:
        ret = True

    return ret        


def reset_all_panels():
    import maya.cmds as cmds
    
    ##################################################################################
            
    regular_panel_types = cmds.getPanel(allTypes=True)  # excluding scripted types,
    # e.g. [u'posePanel', u'shapePanel', u'blendShapePanel', 
    # u'hardwareRenderPanel', u'devicePanel', u'hyperPanel', 
    # u'outlinerPanel', u'modelPanel']
    
    _EXCLUDED_REGULAR_PANEL_LABELS = (
        "modelPanel",
    )
    
    for typ in regular_panel_types:
        panels = cmds.getPanel(type=typ) or []
        for panel_name in panels:
            for excluded_label in _EXCLUDED_REGULAR_PANEL_LABELS:
                if excluded_label in panel_name:
                    continue
                else:
                    cmds.deleteUI(panel_name, panel=True)
                    print('Panel "{}" deleted.'.format(panel_name))

    ##################################################################################

    scripted_panel_types = cmds.getPanel(allScriptedTypes=True)  # e.g.
    # [u'Stereo', u'blindDataEditor', u'clipEditorPanel', u'componentEditorPanel', 
    # u'contentBrowserPanel', u'createNodePanel', u'dopeSheetPanel', 
    # u'dynPaintScriptedPanelType', u'dynRelEdPanel', u'graphEditor', 
    # u'hyperGraphPanel', u'hyperShadePanel', u'multiListerPanel', 
    # u'nodeEditorPanel', u'polySelectionConstraintPanel', u'polyTexturePlacementPanel', 
    # u'profilerPanel', u'referenceEditorPanel', u'relationshipPanel', u'rendRelPanel', 
    # u'renderWindowPanel', u'scriptEditorPanel', u'sequenceEditorPanel', 
    # u'shotPlaylistPanel', u'timeEditorPanel', u'visorPanel', u'webBrowserPanel']

    _EXCLUDED_SCRIPTED_PANELS = (
        "scriptEditorPanel1", 
        "createNodePanel1", 
        "dynPaintScriptedPanel",
    )

    for typ in scripted_panel_types:
        panels = cmds.getPanel(scriptType=typ) or []
        for panel_name in [p for p in panels if p not in _EXCLUDED_SCRIPTED_PANELS]:
            cmds.deleteUI(panel_name, panel=True)
            print('Panel "{}" deleted.'.format(panel_name))

    ##################################################################################

    cmds.windowPref(removeAll=True)
    cmds.workspaceLayoutManager(setCurrent="Maya Classic", reset=True)


if __name__ == "__main__":
    reset_all_windows()
    reset_all_panels()
