"""
    User-Interface for Nightshade UV editor (NSUV) v1.6.1
        
    NSUV offers extended utility to Maya's native UV Texture Editor
    Made by Martin (Nightshade) Dahlin - martin.dahlin@live.com - martin.dahlin.net
        
    Also included is this fantastic python script CalcUVStats by Guido Neumann.
    His site can be found here: http://blog.kernphase.com/
        
    Special thanks to:
    NaughtyNathan, Robert (rgkovach123) and David Johnson from CGTalk for all the coding help.
    And thanks to Anton Palmqvist, Malcolm Andrieshyn, and my former coworker Alexander Lilja 
    for all the feedback, bug reports and feature ideas.
        
    Script downloaded from Creative Crash
"""

## Imports

import pymel.core as pm
import NSUV.core as core
import calcUVStats
import inspect
import os

## Initialization

# Vars
frameWidth = 121
gap0 = 0
gap1 = 1
gap2 = 2
gap3 = 3
gap4 = 4
iconSizeBig = 48
iconSmall = 18
pointLeft = [0.0, 0.0]
scrollListUVSet = []  
windowX = 888
windowY = 837

# UI names
NSUV_title = "Nightshade UV Editor v1.6.1"
panelUV = "NSUV_panel"
winCalcPx = "NSUV_calcPxWin"
winCopyNewUVSet = "NSUV_copyNewUVSetWin"
winMain = "NSUV_mainWin"
winMatchTol = "NSUV_matchTolWin"
winMapAuto = "NSUV_mapAutoWin"
winMapCamera = "NSUV_mapCameraWin"
winMapCylindrical = "NSUV_mapCylindricalWin"
winMapNormal = "NSUV_mapNormalWin"
winMapPlanar = "NSUV_mapPlanarWin"
winMapSpherical = "NSUV_mapSphericalWin"
winNewUVSet = "NSUV_newUVSetWin"
winOrient = "NSUV_shellsOrientWin"
winRandom = "NSUV_rndWin"
winRelax = "NSUV_relaxWin"
winRenameUVSet = "NSUV_renameUVSetWin"
winSS = "NSUV_snapshotWin"
winStrUVs = "NSUV_straightenUVsWin"
winTDwUnits = "NSUV_workingUnitsWin"
winUnfold = "NSUV_unfoldWin"
winUpdate = "NSUV_updateWin"


########## User-interfaces ##########

# Main UI
def createUI():
    
    # Check for window duplicate
    if pm.window( winMain, exists=True ):
        pm.deleteUI( winMain )
        
    # Main window
    window = pm.window(
        winMain,
        maximizeButton=True, 
        minimizeButton=True,
        sizeable=True,
        title=NSUV_title, 
        widthHeight=(windowX, windowY)
    )
    
    # Main pane layout
    paneMain = pm.paneLayout(
        configuration="vertical2", 
        paneSize=( [1, 5, 100], [2, 95, 100]), 
        separatorThickness=4,
        staticWidthPane=1    
    )

    formMain = pm.formLayout( height=1 )
    
    ## Manipulator frame - UI elements:
    frameManip = pm.frameLayout(
        borderStyle="etchedOut", 
        collapsable=True,
        collapse=pm.optionVar["frameManipOptVar"],
        collapseCommand=lambda *args: core.updateFrame(1, True),
        expandCommand=lambda *args: core.updateFrame(1, False),
        label="Manipulator",
        parent=formMain,
        width=frameWidth
    )
    
    # Formlayout for the child elements
    formManip = pm.formLayout()
    
    # Flip   
    btnFlip = pm.iconTextButton(
        annotation="Flip UVs along U or V",
        command=lambda *args: core.flipUVs("U"),
        commandRepeatable=True, 
        image1="NS_flip.bmp",    
        label="Flip UVs along U or V" 
    )
    btnFlipPop = pm.popupMenu( 
        button=3,
        parent=btnFlip,
        postMenuCommand=lambda *args: core.flipUVs("V"),
    )    
    
    # Scale
    btnScaleU = pm.iconTextButton(
        annotation="Scale UVs along U only", 
        command=lambda *args: core.scaleUVs("U"),
        commandRepeatable=True, 
        image1="NS_manipScaleU.bmp",
        label="Scale UVs along U only" 
    )
    btnFlipPop = pm.popupMenu( 
        button=3,
        parent=btnScaleU,
        postMenuCommand=lambda *args: core.scaleUVs("relU"),
    )  
    
    btnScaleV = pm.iconTextButton(
        annotation="Scale UVs along V only", 
        command=lambda *args: core.scaleUVs("V"),
        commandRepeatable=True, 
        image1="NS_manipScaleV.bmp",
        label="Scale UVs along V only" 
    )
    btnFlipPop = pm.popupMenu( 
        button=3,
        parent=btnScaleV,
        postMenuCommand=lambda *args: core.scaleUVs("relV"),
    )  
    
    btnScale = pm.iconTextButton(
        annotation="Scale UVs", 
        command=lambda *args: core.scaleUVs("UV"), 
        commandRepeatable=True, 
        image1="NS_manipScaleUV.bmp",
        label="Scale UVs" 
    )
    btnFlipPop = pm.popupMenu( 
        button=3,
        parent=btnScale,
        postMenuCommand=lambda *args: core.scaleUVs("relUV"),
    )  
    
    # Rotate
    btnRot90CCW = pm.iconTextButton(
        annotation="Rotate UVs 90 degrees counterclockwise", 
        command=lambda *args: core.rotateUVs("90"),
        commandRepeatable=True, 
        image1="NS_rot90CCW.bmp",
        label="Rotate UVs 90 degrees counterclockwise"
    )        
    btnRot90CW = pm.iconTextButton(
        annotation="Rotate UVs 90 degrees clockwise", 
        command=lambda *args: core.rotateUVs("-90"),
        commandRepeatable=True, 
        image1="NS_rot90CW.bmp",
        label="Rotate UVs 90 degrees clockwise" 
    )
    btnRotCCW = pm.iconTextButton(
        annotation="Rotate UVs counterclockwise", 
        command=lambda *args: core.rotateUVs("CCW"),
        commandRepeatable=True, 
        image1="NS_manipRotCCW.bmp",
        label="Rotate UVs counterclockwise" 
    )
    btnRotCW = pm.iconTextButton(
        annotation="Rotate UVs clockwise", 
        command=lambda *args: core.rotateUVs("CW"),
        commandRepeatable=True, 
        image1="NS_manipRotCW.bmp", 
        label="Rotate UVs clockwise"
    )
    
    # Translate   
    btnMoveUpLeft = pm.iconTextButton(
        annotation="Move UVs up and to the left", 
        command=lambda *args: core.translateUVs("upLeft"),
        commandRepeatable=True, 
        image1="NS_manipMoveUpLeft.bmp",
        label="Move UVs up and to the left" 
    )
    btnMoveUp = pm.iconTextButton(
        annotation="Move UVs up", 
        command=lambda *args: core.translateUVs("up"),
        commandRepeatable=True, 
        image1="NS_manipMoveUp.bmp",
        label="Move UVs up" 
    )
    btnMoveUpRight = pm.iconTextButton(
        annotation="Move UVs up and to the right", 
        command=lambda *args: core.translateUVs("upRight"),
        commandRepeatable=True, 
        image1="NS_manipMoveUpRight.bmp",
        label="Move UVs up and to the right" 
    ) 
    btnMoveDownLeft = pm.iconTextButton(
        annotation="Move UVs down and to the left", 
        command=lambda *args: core.translateUVs("downLeft"),
        commandRepeatable=True, 
        image1="NS_manipMoveDownLeft.bmp",
        label="Move UVs down and to the left" 
    )
    btnMoveDown = pm.iconTextButton(
        annotation="Move UVs down", 
        command=lambda *args: core.translateUVs("down"),
        commandRepeatable=True, 
        image1="NS_manipMoveDown.bmp",
        label="Move UVs down" 
    )
    btnMoveDownRight = pm.iconTextButton(
        annotation="Move UVs down and to the right", 
        command=lambda *args: core.translateUVs("downRight"),
        commandRepeatable=True, 
        image1="NS_manipMoveDownRight.bmp",
        label="Move UVs down and to the right" 
    )
    btnMoveRight = pm.iconTextButton(
        annotation="Move UVs to the right", 
        command=lambda *args: core.translateUVs("right"),
        commandRepeatable=True, 
        image1="NS_manipMoveRight.bmp",
        label="Move UVs to the right" 
    )        
    btnMoveLeft = pm.iconTextButton(
        annotation="Move UVs to the left", 
        command=lambda *args: core.translateUVs("left"),
        commandRepeatable=True, 
        image1="NS_manipMoveLeft.bmp",
        label="Move UVs to the left" 
    )
    btnAbsolute = pm.iconTextCheckBox(
        annotation="Toggle between absolute and relative translation",     
        disabledImage="NS_absRelToggleOff.bmp",
        image="NS_absRelToggleOff.bmp",
        label="Toggle between absolute and relative translation", 
        offCommand=lambda *args: core.absToggle(False),
        onCommand=lambda *args: core.absToggle(True),
        selectionImage="NS_absRelToggle.bmp",
        value=pm.optionVar["absToggleOptVar"]
    )  

    # Text field
    fieldManip = pm.floatField(
        annotation="Enter manipulation value", 
        changeCommand=lambda *args: core.manipField( fieldManip, "get" ),
        editable=True, 
        # minValue=0,
        precision=4,    
        value=pm.optionVar["manipAmtOptVar"],
        width=60 
    )
    
    # Field value buttons   
    btnReset = pm.iconTextButton(
        annotation="Reset the manipulation field back to 0",     
        command=lambda *args: core.manipField( fieldManip, 0 ),
        commandRepeatable=True, 
        image1="NS_manipValReset.bmp",
        label="Reset the manipulation field back to 0" 
    )
    btnResetPop = pm.popupMenu(
        button=3,
        parent=btnReset, 
        postMenuCommand=lambda *args: core.manipField( fieldManip, 1 )
    )       
    btnDoubleSplit = pm.iconTextButton(
        annotation="Multiply/Divide the manipulation value by/with 2", 
        command=lambda *args: core.manipField( fieldManip, "double" ),
        commandRepeatable=True, 
        image1="NS_manipVal2.bmp",
        label="Multiply/Divide the manipulation value by 2",
        visible=True,
        )
    btnDoubleSplitPop = pm.popupMenu(
        button=3,
        parent=btnDoubleSplit, 
        postMenuCommand=lambda *args: core.manipField( fieldManip, "split" )
    )
    
    # Distance calc buttons
    btnDist = pm.iconTextButton(
        annotation="Calculate the U or V distance between two UVs and copy it to the value field", 
        command=lambda *args: core.manipField( fieldManip, "distU" ),
        commandRepeatable=True, 
        image1="NS_manipCalcDist.bmp",
        label="Calculate the U or V distance between two UVs and copy it to the value field",
        visible=True,
    )
    btnDistPop = pm.popupMenu(
        button=3,
        parent=btnDist, 
        postMenuCommand=lambda *args: core.manipField( fieldManip, "distV" )
    ) 
    btnPxDist = pm.iconTextButton(
        annotation="Calculate the pixel distance between two UVs", 
        command=lambda *args: calcPxDistUI(),
        commandRepeatable=True, 
        image1="NS_calcPixelDist.bmp", 
        label="Calculate the pixel distance between two UVs",
        visible=True,
    )

    # Field value variables
    btnVarA = pm.iconTextButton(
        annotation="Read/store variable A", 
        command=lambda *args: core.manipField( fieldManip, "getA"),
        commandRepeatable=True, 
        image1="NS_manipVarA.bmp", 
        label="Read/store variable A",
        visible=True,
    )
    btnVarAPop = pm.popupMenu(
        button=3,
        parent=btnVarA,
        postMenuCommand=lambda *args: core.manipField( fieldManip, "setA" )
    )
    btnVarB = pm.iconTextButton(
        annotation="Read/store variable B", 
        command=lambda *args: core.manipField( fieldManip, "getB" ),
        commandRepeatable=True, 
        image1="NS_manipVarB.bmp", 
        label="Read/store variable B",
        visible=True,
    )
    btnVarBPop = pm.popupMenu(
        button=3,
        parent=btnVarB,  
        postMenuCommand=lambda *args: core.manipField( fieldManip, "setB" )
    )

    # Comp space checkbox
    sep2 = pm.separator( 
        height=1,
        horizontal=True,
        style="in", 
        width=121
    )
    cBoxCSpace = pm.checkBox(
        align="left",
        annotation="Retain comp. space",     
        label="Retain comp. space", 
        offCommand=lambda *args: core.compSpaceToggle(cBoxCSpace, 0), 
        onCommand=lambda *args: core.compSpaceToggle(cBoxCSpace, 1), 
        value=pm.optionVar["compSpaceOptVar"]
    )    

    # Layout the elements in the formLayout
    pm.formLayout(
        formManip, edit=True, 
        attachForm=[
            (btnScale, "top", gap2 ), 
            (btnScale, "left", gap1 ),
            (btnScaleU, "top", gap2 ), 
            (btnScaleV, "top", gap2 ),
            (btnFlip, "top", gap2 ), 

            (btnRot90CCW, "left", gap1), 
            
            (btnRotCCW, "left", gap1), 
            
            (btnDist, "left", gap1), 
            
            (btnPxDist, "left", gap1),            
            
            (sep2, "left", 0), 
            (cBoxCSpace, "left", gap3), 
            (cBoxCSpace, "bottom", gap3*4), 
        ], 
        attachControl=[           
            (btnScaleU, "left", gap3, btnScale), 
            (btnScaleV, "left", gap3, btnScaleU), 
            (btnFlip, "left", gap3, btnScaleV), 
            
            (btnRot90CCW, "top", gap1, btnScale), 

            (btnRot90CW, "top", gap1, btnScaleV), 
            (btnRot90CW, "left", gap3, btnMoveUpRight), 
            (btnRotCCW, "top", gap1, btnRot90CCW), 
            (btnRotCW, "top", gap1, btnRot90CW), 
            (btnRotCW, "left", gap1, btnMoveDownRight), 
            
            (btnMoveUpLeft, "top", gap1, btnScaleV), 
            (btnMoveUpLeft, "left", gap3, btnRot90CCW),             
            (btnMoveUp, "top", gap1, btnScaleV), 
            (btnMoveUp, "left", gap0, btnMoveUpLeft), 
            (btnMoveUpRight, "top", gap1, btnScaleU), 
            (btnMoveUpRight, "left", gap0, btnMoveUp), 
            (btnMoveLeft, "top", gap0, btnMoveUp), 
            (btnMoveLeft, "left", gap3, btnRotCCW), 
            (btnAbsolute, "top", gap0, btnMoveUp), 
            (btnAbsolute, "left", gap0, btnMoveLeft), 
            (btnMoveRight, "top", gap0, btnMoveUp), 
            (btnMoveRight, "left", gap0, btnAbsolute),      
            (btnMoveDownLeft, "top", gap0, btnAbsolute), 
            (btnMoveDownLeft, "left", gap3, btnRot90CCW),             
            (btnMoveDown, "top", gap0, btnAbsolute), 
            (btnMoveDown, "left", gap0, btnMoveDownLeft), 
            (btnMoveDownRight, "top", gap0, btnAbsolute), 
            (btnMoveDownRight, "left", gap0, btnMoveDown), 
            
            (btnDist, "top", gap1, btnRotCCW), 
            (fieldManip, "top", gap0, btnMoveDown), 
            (fieldManip, "left", gap3, btnDist),
            (btnReset, "top", gap1, btnRotCW), 
            (btnReset, "left", gap0, fieldManip),             
            
            (btnPxDist, "top", gap4+1, fieldManip), 
            (btnVarA, "top", gap4+1, fieldManip), 
            (btnVarA, "left", gap3, btnPxDist),
            (btnVarB, "top", gap4+1, fieldManip), 
            (btnVarB, "left", gap3, btnVarA),
            (btnDoubleSplit, "top", gap4+1, fieldManip), 
            (btnDoubleSplit, "left", gap3, btnVarB), 

            (sep2, "top", gap1, btnPxDist), 
            (cBoxCSpace, "top", gap2, sep2), 
        ]
    )
        
    ## Align frame - UI elements:
    frameAlign = pm.frameLayout(
        borderStyle="etchedOut", 
        collapsable=True,
        collapse=pm.optionVar["frameAlignOptVar"],
        collapseCommand=lambda *args: core.updateFrame(2, True),
        expandCommand=lambda *args: core.updateFrame(2, False),
        label="Align/Snap",
        parent=formMain,
        width=frameWidth
    )
    
    # Formlayout for the child elements
    formAlign = pm.formLayout()
    
    # Copy, paste and delete UV buttons
    btnCopy = pm.iconTextButton(
        annotation="Copy coordinate of the selected UV", 
        command=lambda *args: pm.mel.eval("textureWindowCreateToolBar_uvCopy"),
        commandRepeatable=True, 
        image1="NS_copyUV.bmp",
        label="Copy coordinate of the selected UV" 
    )
    btnPaste = pm.iconTextButton(
        annotation="Paste coordinate of the selected UV", 
        command=lambda *args: pm.mel.eval("textureWindowCreateToolBar_uvPaste 1 1"),
        commandRepeatable=True, 
        image1="NS_pasteUV.bmp",
        label="Paste coordinate of the selected UV" 
    )
    btnDelete = pm.iconTextButton(
        annotation="Delete selected UVs from the active UV set", 
        command=lambda *args: pm.polyMapDel(),
        commandRepeatable=True, 
        image1="NS_deleteUV.bmp",
        label="Delete selected UVs from the active UV set" 
    )
    
    # Align UVs
    btnAlignMinU = pm.iconTextButton(
        annotation="Align UVs to the minimum U value",
        command=lambda *args: core.alignUVs("minU"),
        commandRepeatable=True, 
        image1="NS_alignUmin.bmp",
        label="Align UVs to the minimum U value", 
    )

    btnAlignAvgU = pm.iconTextButton(
        annotation="Align UVs to the average U", 
        command=lambda *args: core.alignUVs("avgU"),
        commandRepeatable=True,
        image1="NS_alignUmid.bmp",
        label="Align UVs to the average U",
    )
    btnAlignAvgUPop = pm.popupMenu(
        button=3,
        parent=btnAlignAvgU, 
        postMenuCommand=lambda *args: core.alignUVs("singularity"),
    ) 

    btnAlignMaxU = pm.iconTextButton(
        annotation="Align UVs to the maximum U value", 
        command=lambda *args: core.alignUVs("maxU"),
        commandRepeatable=True,
        image1="NS_alignUmax.bmp", 
        label="Align UVs to the maximum U value",
    )

    btnAlignMinV = pm.iconTextButton(
        annotation="Align UVs to the minimum V value",
        command=lambda *args: core.alignUVs("minV"),
        commandRepeatable=True,
        image1="NS_alignVmin.bmp",
        label="Align UVs to the minimum V value",
    )
        
    btnAlignAvgV = pm.iconTextButton(
        annotation="Align UVs to the average V", 
        command=lambda *args: core.alignUVs("avgV"),
        commandRepeatable=True,
        image1="NS_alignVmid.bmp",
        label="Align UVs to the average V",
    )
    btnAlignAvgVPop = pm.popupMenu(
        button=3,
        parent=btnAlignAvgV, 
        postMenuCommand=lambda *args: core.alignUVs("singularity"),
    )

    btnAlignMaxV = pm.iconTextButton(
        annotation="Align UVs to the maximum V value", 
        command=lambda *args: core.alignUVs("maxV"),
        commandRepeatable=True, 
        image1="NS_alignVmax.bmp",
        label="Align UVs to the maximum V value", 
    )        
    
    # Align shells
    btnAlignShellAvgU = pm.iconTextButton(
        annotation="Center shells at average U", 
        command=lambda *args: core.alignShells("uAvg"),
        commandRepeatable=True, 
        image1="NS_alUVCenterU.bmp",
        label="Center shells at average U", 
    )
        
    btnAlignShellMaxU = pm.iconTextButton(
        annotation="Align shells to the furthest right UV", 
        command=lambda *args: core.alignShells("uMax"),
        commandRepeatable=True, 
        image1="NS_alUVRight.bmp",
        label="Align shells to the furthest right UV", 
    )
        
    btnAlignShellMinU = pm.iconTextButton(
        annotation="Align shells to the furthest left UV", 
        command=lambda *args: core.alignShells("uMin"),
        commandRepeatable=True, 
        image1="NS_alUVLeft.bmp",
        label="Align shells to the furthest left UV", 
    )        
        
    btnAlignShellAvgV = pm.iconTextButton(
        annotation="Center shells at average V", 
        command=lambda *args: core.alignShells("vAvg"),
        commandRepeatable=True, 
        image1="NS_alUVCenterV.bmp",
        label="Center shells at average V", 
    )

    btnAlignShellMaxV = pm.iconTextButton(
        annotation="Align shells to the furthest top UV", 
        command=lambda *args: core.alignShells("vMax"),
        commandRepeatable=True, 
        image1="NS_alUVTop.bmp",
        label="Align shells to the furthest top UV", 
    )
        
    btnAlignShellMinV = pm.iconTextButton(
        annotation="Align shells to the furthest bottom UV", 
        command=lambda *args: core.alignShells("vMin"),
        commandRepeatable=True, 
        image1="NS_alUVBottom.bmp", 
        label="Align shells to the furthest bottom UV",  
    )

    # Normalize
    btnNorm = pm.iconTextButton(
        annotation="Normalize selected shells", 
        command=lambda *args: core.normalizeShells(0),
        commandRepeatable=True, 
        image1="NS_normalize.bmp",
        label="Normalize selected shells", 
    )    
    btnNormPop = pm.popupMenu(
        button=3,
        parent=btnNorm, 
        postMenuCommand=lambda *args: core.normalizeShells(1),
    ) 
    btnNormUV = pm.iconTextButton(
        annotation="Normalize selected shells along U/V only", 
        command=lambda *args: core.normalizeShells(3),
        commandRepeatable=True, 
        image1="NS_normalizeUV.bmp",
        label="Normalize along U/V only", 
    )        
    btnNormUVPop = pm.popupMenu(
        button=3,
        parent=btnNormUV, 
        postMenuCommand=lambda *args: core.normalizeShells(4),
    )
    
    # Shell snapping
    btnSnapAtoB = pm.iconTextButton(
        annotation="Snap shells via UV coords",
        command=lambda *args: core.snapPoints(0),
        commandRepeatable=True,
        image1="NS_snapAtoB.bmp",
        label="Snap shells via UV coords",
    )        
    btnSnapAtoBPop = pm.popupMenu( 
        button=3,
        parent=btnSnapAtoB,
        postMenuCommand=lambda *args: core.snapPoints(1),
    )
    
    btnSnapTopLeft = pm.iconTextButton(
        annotation="Snap shells to the top left", 
        command=lambda *args: core.snapShells(1),
        commandRepeatable=True, 
        height=iconSmall, 
        image1="NS_snapTopLeft.bmp",
        label="Snap shells to the top left", 
        width=iconSmall, 
    )    
    btnSnapTop = pm.iconTextButton(
        annotation="Snap shells to the top", 
        command=lambda *args: core.snapShells(2),
        commandRepeatable=True, 
        height=iconSmall, 
        image1="NS_snapTop.bmp",
        label="Snap shells to the top", 
        width=iconSmall,
    )
    btnSnapTopRight = pm.iconTextButton(
        annotation="Snap shells to the top right", 
        command=lambda *args: core.snapShells(3),
        commandRepeatable=True, 
        height=iconSmall, 
        image1="NS_snapTopRight.bmp",
        label="Snap shells to the top right",
        width=iconSmall,
    )
    btnSnapLeft = pm.iconTextButton(
        annotation="Snap shells to the left", 
        command=lambda *args: core.snapShells(4),
        commandRepeatable=True, 
        height=iconSmall, 
        image1="NS_snapLeft.bmp",
        label="Snap shells to the left", 
        width=iconSmall, 
    )
    btnSnapCenter = pm.iconTextButton(
        annotation="Snap shells to the center", 
        command=lambda *args: core.snapShells(0),
        commandRepeatable=True, 
        height=iconSmall, 
        image1="NS_snapCenter.bmp",
        label="Snap shells to the center", 
        width=iconSmall, 
    )        
    btnSnapRight = pm.iconTextButton(
        annotation="Snap shells to the right",
        command=lambda *args: core.snapShells(5),
        commandRepeatable=True, 
        height=iconSmall, 
        image1="NS_snapRight.bmp",
        label="Snap shells to the right", 
        width=iconSmall,
    )
    btnSnapBottomLeft = pm.iconTextButton(
        annotation="Snap shells to the bottom left", 
        command=lambda *args: core.snapShells(6),
        commandRepeatable=True, 
        height=iconSmall, 
        image1="NS_snapDownLeft.bmp",
        label="Snap shells to the bottom left", 
        width=iconSmall, 
    )
    btnSnapBottom = pm.iconTextButton(
        annotation="Snap shells to the bottom", 
        command=lambda *args: core.snapShells(7),
        commandRepeatable=True, 
        height=iconSmall, 
        image1="NS_snapDown.bmp",
        label="Snap shells to the bottom", 
        width=iconSmall
    )
    btnSnapBottomRight = pm.iconTextButton(
        annotation="Snap shells to the bottom right", 
        command=lambda *args: core.snapShells(8),
        commandRepeatable=True, 
        height=iconSmall, 
        image1="NS_snapDownRight.bmp",
        label="Snap shells to the bottom right", 
        width=iconSmall,
    )
    
    # Randomize
    btnRandomize = pm.iconTextButton(
        annotation="Randomize UV shells",
        command=lambda *args: randomizeUI(),
        commandRepeatable=True, 
        image1="NS_randomizeUV.bmp", 
        label="Randomize UV shells"
    )
    
    # Layout the elements in the formLayout
    pm.formLayout(
        formAlign, edit=True, 
        attachForm=[
            (btnCopy, "top", gap2 ), 
            (btnCopy, "left", gap2 ), 
            (btnAlignMinU, "top", gap2), 
            (btnAlignAvgU, "top", gap2), 
            (btnAlignMaxU, "top", gap2), 

            (btnPaste, "left", gap2 ), 
            
            (btnDelete, "left", gap2 ), 
            
            (btnAlignShellMinV, "left", 31),     
            
            (btnSnapAtoB, "left", gap1), 
            
            (btnRandomize, "left", gap1), 
            (btnRandomize, "bottom", gap3*4), 
        ], 
        attachControl=[ 
            (btnAlignMinU, "left", gap3, btnCopy), 
            (btnAlignAvgU, "left", gap3, btnAlignMinU), 
            (btnAlignMaxU, "left", gap3, btnAlignAvgU), 
        
            (btnPaste, "top", gap1, btnCopy), 
            (btnAlignMinV, "top", gap1, btnAlignMinU),
            (btnAlignMinV, "left", gap3, btnPaste),
            (btnAlignAvgV, "top", gap1, btnAlignAvgU),
            (btnAlignAvgV, "left", gap3, btnAlignMinV),
            (btnAlignMaxV, "top", gap1, btnAlignMaxU),
            (btnAlignMaxV, "left", gap3, btnAlignAvgV),
            
            (btnDelete, "top", gap1, btnPaste),         
            (btnAlignShellMinU, "top", gap1, btnAlignMinV), 
            (btnAlignShellMinU, "left", gap2, btnDelete),             
            (btnAlignShellAvgU, "top", gap1, btnAlignAvgV), 
            (btnAlignShellAvgU, "left", gap3, btnAlignShellMinU), 
            (btnAlignShellMaxU, "top", gap1, btnAlignMaxV), 
            (btnAlignShellMaxU, "left", gap3, btnAlignShellAvgU), 
            
            (btnAlignShellMinV, "top", gap1, btnAlignShellMinU),        
            (btnAlignShellAvgV, "top", gap1, btnAlignShellAvgU), 
            (btnAlignShellAvgV, "left", gap3, btnAlignShellMinV),            
            (btnAlignShellMaxV, "top", gap1, btnAlignShellMaxU), 
            (btnAlignShellMaxV, "left", gap3, btnAlignShellAvgV), 
            
            (btnSnapAtoB, "top", 29, btnDelete), 
            (btnRandomize, "top", gap1, btnSnapAtoB), 
            
            (btnSnapTopLeft, "top", gap1, btnAlignShellMinV), 
            (btnSnapTopLeft, "left", gap4, btnRandomize), 
            (btnSnapTop, "top", gap1, btnAlignShellMinV), 
            (btnSnapTop, "left", gap0, btnSnapTopLeft), 
            (btnSnapTopRight, "top", gap1, btnAlignShellMinV), 
            (btnSnapTopRight, "left", gap0, btnSnapTop), 
            
            (btnSnapLeft, "top", gap0, btnSnapTopLeft), 
            (btnSnapLeft, "left", gap4, btnRandomize), 
            (btnSnapCenter, "top", gap0, btnSnapTop), 
            (btnSnapCenter, "left", gap0, btnSnapLeft), 
            (btnSnapRight, "top", gap0, btnSnapTopRight), 
            (btnSnapRight, "left", gap0, btnSnapCenter), 
            
            (btnSnapBottomLeft, "top", gap0, btnSnapLeft), 
            (btnSnapBottomLeft, "left", gap4, btnRandomize), 
            (btnSnapBottom, "top", gap0, btnSnapCenter), 
            (btnSnapBottom, "left", gap0, btnSnapBottomLeft), 
            (btnSnapBottomRight, "top", gap0, btnSnapRight), 
            (btnSnapBottomRight, "left", gap0, btnSnapBottom), 
            
            (btnNorm, "top", gap1, btnAlignShellMaxV), 
            (btnNorm, "left", gap4+1, btnSnapTopRight), 
            (btnNormUV, "top", gap1, btnNorm), 
            (btnNormUV, "left", gap4+1, btnSnapBottomRight), 
        ]
    )
    
    ## UV sets frame - UI elements:
    frameUVSet = pm.frameLayout(
        borderStyle="etchedOut", 
        collapsable=True,
        collapse=pm.optionVar["frameSetOptVar"],
        collapseCommand=lambda *args: core.updateFrame(3, True),
        expandCommand=lambda *args: core.updateFrame(3, False),
        label="UV Sets",
        parent=formMain,
        width=frameWidth
    )
    
    # Formlayout for the child elements
    formUVSet = pm.formLayout()
    
    btnUVSetNew = pm.iconTextButton( 
        annotation="Create new UV set", 
        command=lambda *args: core.createSet(scrollListUVSet), 
        commandRepeatable=True, 
        image1="NS_uvSetNew.bmp", 
        label="Create new UV set" 
    )
    btnUVSetNewOpts = pm.popupMenu( 
        button=3, 
        parent=btnUVSetNew, 
        postMenuCommand=lambda *args: createSetUI(scrollListUVSet) 
    )
    btnUVSetCopy = pm.iconTextButton( 
        annotation="Copy UV set or part of UV set to...", 
        command="", 
        image1="NS_uvSetCopy.bmp", 
        label="Copy UV set or part of UV set to..." 
    )
    btnUVSetCopyPop = pm.popupMenu( 
        button=1, 
        markingMenu=True, 
        parent=btnUVSetCopy, 
        postMenuCommand=lambda *args: copySetMenu(btnUVSetCopyPop, scrollListUVSet)
    )
    btnUVSetDupe = pm.iconTextButton(
        annotation="Duplicate UV set", 
        command=lambda *args: core.dupeSet(scrollListUVSet),
        commandRepeatable=True, 
        image1="NS_uvSetDupe.bmp", 
        label="Duplicate UV set" 
    ) 
    btnUVSetProp = pm.iconTextButton(        
        annotation="If the selected UV set does not exist on all selected meshes, dupe it to said meshes.", 
        command=lambda *args: core.propagateSets(scrollListUVSet), 
        commandRepeatable=True, 
        image1="NS_uvSetPropagate.bmp",
        label="If the selected UV set does not exist on all selected meshes, dupe it to said meshes."
    )
    btnUVSetFind = pm.iconTextButton(
        annotation="Select all unmapped faces", 
        command=lambda *args: core.selectUnmapped(), 
        commandRepeatable=True, 
        image1="NS_uvSetUnmapped.bmp", 
        label="Select all unmapped faces" 
    ) 
    btnUVSetFindPop = pm.popupMenu(
        button=3, 
        parent=btnUVSetFind, 
        postMenuCommand=lambda *args: core.mapping("auto")
    )
    btnUVSetShareInst = pm.iconTextButton(
        annotation="Share instances", 
        command=lambda *args: pm.runtime.ShareUVInstances(), 
        commandRepeatable=True, 
        image1="NS_uvSetShareInst.bmp", 
        label="Share instances" 
    )
    btnUVSetSelShared = pm.iconTextButton(
        annotation="Select shared instances", 
        command=lambda *args: pm.runtime.SelectSharedUVInstances(),
        commandRepeatable=True, 
        image1="NS_uvSetSelInst.bmp", 
        label="Select shared instances" 
    )  
    btnUVSetSnapshot = pm.iconTextButton(
        annotation="Take a snapshot of the current UV layout", 
        command=lambda *args: snapshotUI(),
        commandRepeatable=True, 
        image1="NS_uvSnapshot.bmp", 
        label="Take a snapshot of the current UV layout" 
    )
    btnUVSetSnapshotPop = pm.popupMenu( 
        button=3, 
        markingMenu=True, 
        parent=btnUVSetSnapshot, 
        postMenuCommand=lambda *args: core.ssTakeShot()
    )

    # UV Sets list
    scrollListUVSet = pm.textScrollList(
        allowMultiSelection=True, 
        deleteKeyCommand=lambda *args: core.deleteSet(scrollListUVSet),
        doubleClickCommand=lambda *args: renameSetUI(scrollListUVSet),
        selectCommand=lambda *args: core.setCurrent(scrollListUVSet),
        width=frameWidth-2 
    )
    
    # Layout the elements in the formLayout
    pm.formLayout(
        formUVSet, edit=True, 
        attachForm=[
            (btnUVSetNew, "top", gap2), 
            (btnUVSetNew, "left", gap1), 
            (btnUVSetCopy, "top", gap2), 
            (btnUVSetDupe, "top", gap2),
            (btnUVSetProp, "top", gap2),
            (btnUVSetFind, "left", gap1),         
            (scrollListUVSet, "left", 0), 
            (scrollListUVSet, "bottom", gap3*4), 
        
        ], 
        attachControl=[           
            (btnUVSetCopy, "left", gap3, btnUVSetNew), 
            (btnUVSetDupe, "left", gap3, btnUVSetCopy), 
            (btnUVSetProp, "left", gap3, btnUVSetDupe), 
        
            (btnUVSetFind, "top", gap1, btnUVSetNew),          
            (btnUVSetShareInst, "top", gap1, btnUVSetCopy), 
            (btnUVSetShareInst, "left", gap3, btnUVSetFind), 
            (btnUVSetSelShared, "top", gap1, btnUVSetDupe),
            (btnUVSetSelShared, "left", gap3, btnUVSetShareInst), 
            (btnUVSetSnapshot, "top", gap1, btnUVSetProp),
            (btnUVSetSnapshot, "left", gap3, btnUVSetSelShared), 
        
            (scrollListUVSet, "top", gap3, btnUVSetFind), 
        ]
    )
    
    ## UV mapping frame - UI elements:
    frameUVmapping = pm.frameLayout(
        borderStyle="etchedOut", 
        collapsable=True,
        collapse=pm.optionVar["frameMappingOptVar"],
        collapseCommand=lambda *args: core.updateFrame(4, True),
        expandCommand=lambda *args: core.updateFrame(4, False),
        label="UV Mapping",
        parent=formMain,
        width=frameWidth
    )
    
    # Formlayout for the child elements
    formUVmapping = pm.formLayout()
    
    btnUVmapPlaneX = pm.iconTextButton(
        annotation="Planar mapping: X", 
        command=lambda *args: core.mapping("plane", "x"),
        commandRepeatable=True, 
        image1="NS_projPlaneX.bmp", 
        label="Planar mapping: X" 
    )    
    btnUVmapPlaneXPop = pm.popupMenu( 
        button=3, 
        markingMenu=True, 
        parent=btnUVmapPlaneX, 
        postMenuCommand=lambda *args: mapPlanarUI("x")
    )
    btnUVmapPlaneY = pm.iconTextButton(
        annotation="Planar mapping: Y", 
        command=lambda *args: core.mapping("plane", "y"),
        commandRepeatable=True, 
        image1="NS_projPlaneY.bmp", 
        label="Planar mapping: Y" 
    )   
    btnUVmapPlaneYPop = pm.popupMenu( 
        button=3, 
        markingMenu=True, 
        parent=btnUVmapPlaneY, 
        postMenuCommand=lambda *args: mapPlanarUI("y")
    )
    btnUVmapPlaneZ = pm.iconTextButton(
        annotation="Planar mapping: Z", 
        command=lambda *args: core.mapping("plane", "z"),
        commandRepeatable=True, 
        image1="NS_projPlaneZ.bmp", 
        label="Planar mapping: Z" 
    )
    btnUVmapPlaneZPop = pm.popupMenu( 
        button=3, 
        markingMenu=True, 
        parent=btnUVmapPlaneZ, 
        postMenuCommand=lambda *args: mapPlanarUI("z")
    )    
    btnUVmapCam = pm.iconTextButton(
        annotation="Planar mapping: From camera", 
        command=lambda *args: core.mapping("plane", "c"),
        commandRepeatable=True, 
        image1="NS_projCam.bmp", 
        label="Camera mapping" 
    ) 
    btnUVmapCamPop = pm.popupMenu( 
        button=3, 
        markingMenu=True, 
        parent=btnUVmapCam, 
        postMenuCommand=lambda *args: mapPlanarUI("cam"),
    )        
    btnUVmapAuto = pm.iconTextButton(
        annotation="Automatic mapping", 
        command=lambda *args: core.mapping("auto"),
        commandRepeatable=True, 
        image1="NS_projAuto.bmp", 
        label="Automatic mapping" 
    )  
    btnUVmapAutoPop = pm.popupMenu( 
        button=3, 
        markingMenu=True, 
        parent=btnUVmapAuto, 
        postMenuCommand=lambda *args: mapAutoUI()
    )
    btnUVmapCyl = pm.iconTextButton(
        annotation="Cylindrical mapping", 
        command=lambda *args: core.mapping("cyl"),
        commandRepeatable=True, 
        image1="NS_projCyl.bmp", 
        label="Cylindrical mapping" 
    )
    btnUVmapCylPop = pm.popupMenu( 
        button=3, 
        markingMenu=True, 
        parent=btnUVmapCyl, 
        postMenuCommand=lambda *args: mapCylindricalUI()
    )
    btnUVmapSphere = pm.iconTextButton(
        annotation="Spherical mapping", 
        command=lambda *args: core.mapping("sphere"),
        commandRepeatable=True, 
        image1="NS_projSphere.bmp", 
        label="Spherical mapping"
    )
    btnUVmapSpherePop = pm.popupMenu( 
        button=3, 
        markingMenu=True, 
        parent=btnUVmapSphere, 
        postMenuCommand=lambda *args: mapSphericalUI()
    )
    btnUVmapNormal = pm.iconTextButton(
        annotation="Normal based mapping", 
        command=lambda *args: core.mapping("normal"),
        commandRepeatable=True, 
        image1="NS_projNormal.bmp", 
        label="Normal based mapping"
    )
    btnUVmapNormalPop = pm.popupMenu( 
        button=3, 
        markingMenu=True, 
        parent=btnUVmapNormal, 
        postMenuCommand=lambda *args: mapNormalUI()
    )
    
    # Layout the elements in the formLayout
    pm.formLayout(
        formUVmapping, edit=True, 
        attachForm=[
            (btnUVmapPlaneX, "top", gap2), 
            (btnUVmapPlaneX, "left", gap3), 
            (btnUVmapPlaneY, "top", gap2), 
            (btnUVmapPlaneZ, "top", gap2), 
            (btnUVmapCam, "top", gap2), 
            (btnUVmapAuto, "left", gap1),
            (btnUVmapAuto, "bottom", gap3*4),
        ], 
        attachControl=[           
            (btnUVmapPlaneY, "left", gap1, btnUVmapPlaneX),    
            (btnUVmapPlaneZ, "left", gap3, btnUVmapPlaneY),    
            (btnUVmapCam, "left", gap3, btnUVmapPlaneZ),    
            (btnUVmapAuto, "top", gap3, btnUVmapPlaneX),    
            (btnUVmapCyl, "top", gap3, btnUVmapPlaneY), 
            (btnUVmapCyl, "left", gap3, btnUVmapAuto), 
            (btnUVmapSphere, "top", gap3, btnUVmapPlaneZ), 
            (btnUVmapSphere, "left", gap3, btnUVmapCyl), 
            (btnUVmapNormal, "top", gap3, btnUVmapCam), 
            (btnUVmapNormal, "left", gap3, btnUVmapSphere), 
        ]
    )
    
    ## TD frame - UI elements:
    frameTD = pm.frameLayout(
        borderStyle="etchedOut", 
        collapsable=True,
        collapse=pm.optionVar["frameTDOptVar"],
        collapseCommand=lambda *args: core.updateFrame(5, True),
        expandCommand=lambda *args: core.updateFrame(5, False),
        label="Texel Density",
        parent=formMain,
        width=frameWidth
    )
    
    # Formlayout for the child elements
    formTD = pm.formLayout()
    
    fieldGrpTD = pm.floatFieldGrp(
        changeCommand=lambda *args: core.tdVar("updateTD", fieldGrpTD),
        columnAlign=[1, "left"], 
        columnWidth2=[70, 42], 
        label="TD (px/unit)", 
        numberOfFields=1,
        precision=1, 
        value1=pm.optionVar["tdOptVar"], 
        width=frameWidth 
    )    
    fieldGrpSize = pm.intFieldGrp(
        changeCommand=lambda *args: core.tdVar("updateSize", fieldGrpSize),
        columnAlign=[1, "left"], 
        columnWidth2=[70, 42], 
        label="Map size (px)", 
        numberOfFields=1,
        value1=pm.optionVar["tdSizeOptVar"], 
        width=frameWidth 
    )
    btnTDUnits = pm.iconTextButton(
        annotation="Set working units", 
        command=lambda *args: setWorkingUnitsUI(),
        commandRepeatable=True, 
        image1="NS_tdUnits.bmp", 
        label="Set working units" 
    )
    btnTDVarA = pm.iconTextButton(
        annotation="Read/store fields into variable A", 
        command=lambda *args: core.tdVar("getA", fieldGrpTD, fieldGrpSize),
        commandRepeatable=True, 
        image1="NS_tdVarA.bmp", 
        label="Read/store fields into variable A"
    )
    btnTDVarAPop = pm.popupMenu(
        button=3, 
        parent=btnTDVarA, 
        postMenuCommand=lambda *args: core.tdVar("setA", fieldGrpTD, fieldGrpSize),
    )
    btnTDVarB = pm.iconTextButton(
        annotation="Read/store fields into variable B", 
        command=lambda *args: core.tdVar("getB", fieldGrpTD, fieldGrpSize),
        commandRepeatable=True, 
        image1="NS_tdVarB.bmp", 
        label="Read/store fields into variable B"
    )
    btnTDVarBPop = pm.popupMenu(
        button=3, 
        parent=btnTDVarB, 
        postMenuCommand=lambda *args: core.tdVar("setB", fieldGrpTD, fieldGrpSize),
    )
    btnTD = pm.iconTextButton(
        annotation="Set texel density", 
        command=lambda *args: core.setTD(fieldGrpTD, fieldGrpSize),
        commandRepeatable=True, 
        image1="NS_tdSet.bmp", 
        label="Set texel density" 
    )

    # Layout the elements in the formLayout
    pm.formLayout(
        formTD, edit=True, 
        attachForm=[
            (fieldGrpTD, "top", gap1), 
            (fieldGrpTD, "left", gap1), 
            (fieldGrpSize, "left", gap1), 
            (btnTDUnits, "left", gap1), 
        ], 
        attachControl=[           
            (fieldGrpSize, "top", gap2, fieldGrpTD), 
        
            (btnTDUnits, "top", gap3, fieldGrpSize), 
            (btnTDVarA, "top", gap3, fieldGrpSize), 
            (btnTDVarA, "left", gap3, btnTDUnits), 
            (btnTDVarB, "top", gap3, fieldGrpSize), 
            (btnTDVarB, "left", gap3, btnTDVarA), 
            (btnTD, "top", gap3, fieldGrpSize), 
            (btnTD, "left", gap3, btnTDVarB), 
        ]
    )
    
    #btnUpdateNSUV = pm.button(
    #    annotation="Look for NSUV update",
    #    backgroundColor=[0.33, 0.33, 0.33],
    #    command=lambda *args: updateUI(),
    #    label="Update NSUV",
    #    parent=formMain,
    #    width=frameWidth,
    #)
    
    btnUpdateNSUV = pm.button(
        annotation="Open documentation",
        backgroundColor=[0.33, 0.33, 0.33],
        command=lambda *args: opendoc(),
        label="Help",
        parent=formMain,
        width=frameWidth,
    )
    
    btnSwitchEditor = pm.button(
        annotation="Switch to the default UV Texture Editor",
        backgroundColor=[0.33, 0.33, 0.33],
        command=lambda *args: core.defaultUV(winMain),
        label="Default UV editor",
        parent=formMain,
        width=frameWidth,
    )
    
    # Layout the frames inside the main formLayout
    pm.formLayout(
        formMain, edit=True, 
        attachForm=[
            (frameManip, "top", 0), 
            (frameManip, "left", 0), 
            (frameAlign, "left", 0), 
            (frameUVmapping, "left", 0), 
            (frameUVSet, "left", 0), 
            (frameTD, "left", 0), 
            (btnUpdateNSUV, "left", 0), 
            (btnSwitchEditor, "left", 0), 
        ], 
        attachControl=[
            (frameAlign, "top", 0, frameManip), 
            (frameUVmapping, "top", 0, frameAlign), 
            (frameUVSet, "top", 0, frameUVmapping), 
            (frameTD, "top", 0, frameUVSet),  
            (btnUpdateNSUV, "top", 10, frameTD),  
            (btnSwitchEditor, "top", 0, btnUpdateNSUV),  
        ]
    )
    
    # Create second paneLayout. Holds the UV editor modelPanel
    paneUV = pm.paneLayout(
        configuration="single",
        parent=paneMain,
        staticWidthPane=1 
    )

    # Get all panels, delete duplicate entries of NSUV
    panelList = pm.getPanel(allPanels=True)
    for p in panelList:
        if p.getLabel() == NSUV_title:
            pm.deleteUI(p, panel=True)   
    
    # Create new panel and replace native one
    panelUV = pm.modelPanel(
        label=NSUV_title,
        parent=paneUV
    )    
    pm.scriptedPanel( 
        "polyTexturePlacementPanel1", edit=True,
            replacePanel=panelUV,            
    )

    # Display the window
    pm.showWindow( window ) 
    
    # Create script jobs
    core.createScriptJobs(window, scrollListUVSet, cBoxCSpace)
    
    # Update the UV set editor (else it's blank)
    core.updateUVSetEditor(scrollListUVSet)
    

# UI for calculating pixel distance between two UVs
def calcPxDistUI():

    # Vars
    c1 = 0.3
    c2 = 0.45
    c3 = 0.25
    c4 = 0.39
    c5 = c3
    c6 = c2
    btnRow = 274
    calcPxCellHeight = 17
    calcPxCellWidth = (btnRow/4)
    # calcPxCellWidth = 69
    winHeight = 194
    winWidth = 300
    

    # Get values
    distU, distV, distUV = core.calcPxDist()

    # Check for window duplicate
    if pm.window( winCalcPx, exists=True ):
        pm.deleteUI( winCalcPx )
    
    # Calculate pixel distances
    # U
    distU4096 = "%.2f" % ( 4096*distU )
    distU2048 = "%.2f" % ( float(distU4096) / 2 )
    distU1024 = "%.2f" % ( float(distU4096) / 4 )
    distU512 = "%.2f" % ( float(distU4096) / 8 )
    distU256 = "%.2f" % ( float(distU4096) / 16 )
    distU128 = "%.2f" % ( float(distU4096) / 32 )
    
    # V
    distV4096 = "%.2f" % ( 4096*distV )
    distV2048 = "%.2f" % ( float(distV4096) / 2 )
    distV1024 = "%.2f" % ( float(distV4096) / 4 )
    distV512 = "%.2f" % ( float(distV4096) / 8 )
    distV256 = "%.2f" % ( float(distV4096) / 16 )
    distV128 = "%.2f" % ( float(distV4096) / 32 )

    # Diagonal
    distUV4096 = "%.2f" % ( 4096*distUV )
    distUV2048 = "%.2f" % ( float(distUV4096) / 2 )
    distUV1024 = "%.2f" % ( float(distUV4096) / 4 )
    distUV512 = "%.2f" % ( float(distUV4096) / 8 )
    distUV256 = "%.2f" % ( float(distUV4096) / 16 )
    distUV128 = "%.2f" % ( float(distUV4096) / 32 )
    
    # Construct result strings
    # U
    distU4096L = str(distU4096) + " px"
    distU2048L = str(distU2048) + " px"
    distU1024L = str(distU1024) + " px"
    distU512L = str(distU512) + " px"
    distU256L = str(distU256) + " px"
    distU128L = str(distU128) + " px"
    
    # V
    distV4096L = str(distV4096) + " px"
    distV2048L = str(distV2048) + " px"
    distV1024L = str(distV1024) + " px"
    distV512L = str(distV512) + " px"
    distV256L = str(distV256) + " px"
    distV128L = str(distV128) + " px"

    # Diagonal
    distUV4096L = str(distUV4096) + " px"
    distUV2048L = str(distUV2048) + " px"
    distUV1024L = str(distUV1024) + " px"
    distUV512L = str(distUV512) + " px"
    distUV256L = str(distUV256) + " px"
    distUV128L = str(distUV128) + " px"
    
    # Create window
    window = pm.window(
        winCalcPx,
        height=winHeight,
        minimizeButton=False, 
        maximizeButton=False, 
        resizeToFitChildren=True, 
        sizeable=True, 
        title="Pixel distance", 
        width=winWidth 
    )
    
    # Create layouts
    frameCalcPx = pm.frameLayout(
        borderStyle="etchedIn", 
        collapsable=False, 
        collapse=False, 
        height=winHeight,
        label="Results", 
        marginHeight=10,  
        marginWidth=10, 
        width=winWidth,     
        )
    colMatchTol = pm.columnLayout(
        adjustableColumn=False,
        columnAlign="left",
        rowSpacing=6,
    )
    gridCalcPx = pm.gridLayout(
        backgroundColor=[0.16, 0.16, 0.16],
        cellWidthHeight=[calcPxCellWidth, calcPxCellHeight],
        numberOfRowsColumns=[7,4],
        parent=colMatchTol,
    )
    pm.text( 
        align="center", 
        font="boldLabelFont", 
        height=calcPxCellHeight, 
        label="Map size", 
        width=calcPxCellWidth
    )
    pm.text( 
        align="center", 
        font="boldLabelFont", 
        height=calcPxCellHeight,     
        label="U Distance", 
        width=calcPxCellWidth
    )
    pm.text( 
        align="center", 
        font="boldLabelFont", 
        height=calcPxCellHeight,     
        label="V Distance", 
        width=calcPxCellWidth
    )
    pm.text( 
        align="center", 
        font="boldLabelFont", 
        height=calcPxCellHeight,         
        label="Distance", 
        width=calcPxCellWidth
    )    
    pm.text(
        align="center", 
        backgroundColor=[c1, c1, c1], 
        height=calcPxCellHeight,  
        label="4096 px", 
        width=calcPxCellWidth
    )   
    pm.text( 
        align="center", 
        backgroundColor=[c2, c3, c3], 
        height=calcPxCellHeight,     
        label=distU4096L, 
        width=calcPxCellWidth
    )    
    pm.text( 
        align="center", 
        backgroundColor=[c3, c3, c2], 
        height=calcPxCellHeight,     
        label=distV4096L, 
        width=calcPxCellWidth
    )
    pm.text( 
        align="center", 
        backgroundColor=[c4, c5, c6],  
        height=calcPxCellHeight,     
        label=distUV4096L, 
        width=calcPxCellWidth
    )
    pm.text(
        align="center", 
        backgroundColor=[c1, c1, c1], 
        height=calcPxCellHeight,  
        label="2048 px", 
        width=calcPxCellWidth
    )    
    pm.text( 
        align="center", 
        backgroundColor=[c2, c3, c3],
        height=calcPxCellHeight,     
        label=distU2048L, 
        width=calcPxCellWidth
    ) 
    pm.text( 
        align="center", 
        backgroundColor=[c3, c3, c2], 
        height=calcPxCellHeight,     
        label=distV2048L, 
        width=calcPxCellWidth
    )
    pm.text( 
        align="center", 
        backgroundColor=[c4, c5, c6],  
        height=calcPxCellHeight,     
        label=distUV2048L, 
        width=calcPxCellWidth
    )
    pm.text(
        align="center", 
        backgroundColor=[c1, c1, c1], 
        height=calcPxCellHeight,  
        label="1024 px", 
        width=calcPxCellWidth
    )    
    pm.text( 
        align="center", 
        backgroundColor=[c2, c3, c3],
        height=calcPxCellHeight,     
        label=distU1024L, 
        width=calcPxCellWidth
    )
    pm.text( 
        align="center", 
        backgroundColor=[c3, c3, c2], 
        height=calcPxCellHeight,     
        label=distV1024L, 
        width=calcPxCellWidth
    )
    pm.text( 
        align="center", 
        backgroundColor=[c4, c5, c6],  
        height=calcPxCellHeight,     
        label=distUV1024L, 
        width=calcPxCellWidth
    )
    pm.text(
        align="center", 
        backgroundColor=[c1, c1, c1], 
        height=calcPxCellHeight,  
        label="512 px", 
        width=calcPxCellWidth
    ) 
    pm.text( 
        align="center", 
        backgroundColor=[c2, c3, c3],
        height=calcPxCellHeight,     
        label=distU512L,
        width=calcPxCellWidth
    )
    pm.text( 
        align="center", 
        backgroundColor=[c3, c3, c2], 
        height=calcPxCellHeight,     
        label=distV512L, 
        width=calcPxCellWidth
    )
    pm.text( 
        align="center", 
        backgroundColor=[c4, c5, c6],  
        height=calcPxCellHeight,     
        label=distUV512L, 
        width=calcPxCellWidth
    )
    pm.text(
        align="center", 
        backgroundColor=[c1, c1, c1], 
        height=calcPxCellHeight,  
        label="256 px", 
        width=calcPxCellWidth
    )      
    pm.text( 
        align="center", 
        backgroundColor=[c2, c3, c3],
        height=calcPxCellHeight,     
        label=distU256L, 
        width=calcPxCellWidth
    )
    pm.text( 
        align="center", 
        backgroundColor=[c3, c3, c2], 
        height=calcPxCellHeight,     
        label=distV256L, 
        width=calcPxCellWidth
    )
    pm.text( 
        align="center", 
        backgroundColor=[c4, c5, c6],  
        height=calcPxCellHeight,     
        label=distUV256L, 
        width=calcPxCellWidth
    )
    pm.text(
        align="center", 
        backgroundColor=[c1, c1, c1], 
        height=calcPxCellHeight,  
        label="128 px", 
        width=calcPxCellWidth
    )
    pm.text( 
        align="center", 
        backgroundColor=[c2, c3, c3],
        height=calcPxCellHeight,     
        label=distU128L, 
        width=calcPxCellWidth
    ) 
    pm.text( 
        align="center", 
        backgroundColor=[c3, c3, c2], 
        height=calcPxCellHeight,     
        label=distV128L, 
        width=calcPxCellWidth
    )
    pm.text( 
        align="center", 
        backgroundColor=[c4, c5, c6],
        height=calcPxCellHeight,     
        label=distUV128L,
        width=calcPxCellWidth
    )    

    pm.setParent( '..' ) # Parent children to gridLayout
    
    # Row layout
    rowBtnCalcPx = pm.rowLayout(
        columnAttach2=["both", "both"], 
        numberOfColumns=2, 
        parent=colMatchTol,
    )
    btnOkCalcPx = pm.button(
        command=lambda *args: calcPxDistUI(), 
        label="Recalculate", 
        parent=rowBtnCalcPx,
        width=(btnRow/2),
    )        
    btnCancelCalcPx = pm.button(
        command=lambda *args: pm.deleteUI(winCalcPx),
        label="Close", 
        parent=rowBtnCalcPx,
        width=(btnRow/2),
    )
    
    # Display the window
    pm.showWindow( window  ) 
 
 
# Menu listing all UV sets the user can copy to
def copySetMenu(menu, scrollList):

    # Delete popup menu contents, as we need to rebuild...
    menu.deleteAllItems()
    
    # Get mesh from the current selection
    shapes = core.getShapes()

    # If a mesh is selected, rebuild the popup menu
    if shapes != []:
    
        # Get sets
        uvSets = core.getSet("all", shapes) 
        
        # Get current set
        uvSetCurrent = core.getSet("current", shapes)
        
        # For every UV-set, create a menuItem
        for item in uvSets:
        
            # Create menuItem
            pm.menuItem(
                command=lambda *args: core.copySet(scrollList, uvSetCurrent, item),
                label=item,
                parent=menu
            )        
        
        # Create default button
        pm.menuItem(
            command=lambda *args: copySetUI(scrollList, uvSetCurrent),
            label="Copy into new UV set",       
            parent=menu
        )

    else: # No mesh is selected
        pm.menuItem(
            enable=False,
            label="No mesh selected",
            parent=menu
        ) 
        
        
# UI for copying to a new UV set
def copySetUI(scrollList, copyFrom):

    btnRow=274
    
    ## Internal method
    
    # Update optVar
    def copySetOptVar():
        pm.optionVar["copyNewUVSetOptVar"] = fieldCopyNewUVSet.getText()


    ## Create UI
    
    # Check for window duplicate
    if pm.window( winCopyNewUVSet, exists=True ):
        pm.deleteUI( winCopyNewUVSet )
        
    # Window
    window = pm.window(
        winCopyNewUVSet,
        minimizeButton=False, 
        maximizeButton=False, 
        resizeToFitChildren=False, 
        sizeable=False, 
        title="Copy to new UV Set", 
        width=300 
    )
    
    # Layouts
    frameCopyNewUVSet = pm.frameLayout(
        borderStyle="etchedIn", 
        collapsable=False, 
        collapse=False, 
        label="Options", 
        marginHeight=9, 
        marginWidth=9, 
        width=300 
    )
    colCopyNewUVSet = pm.columnLayout(
        adjustableColumn=True, 
        columnAlign="left", 
        rowSpacing=6,
        parent=frameCopyNewUVSet
    )
    
    # Text field
    version = pm.about(version=True)
    if version.startswith("2012"): # Because the textChangedCommand didnt exist in Maya 2012...
        fieldCopyNewUVSet = pm.textFieldGrp(
            changeCommand=lambda *args: copySetOptVar(),
            columnAlign=[1, "right"], 
            columnWidth2=[80, 195],
            forceChangeCommand=True,
            insertionPosition=0,
            label="UV Set name: ", 
            parent=colCopyNewUVSet,
            text=pm.optionVar["copyNewUVSetOptVar"],
        )        
    else:     
        fieldCopyNewUVSet = pm.textFieldGrp(
            changeCommand=lambda *args: copySetOptVar(),
            columnAlign=[1, "right"], 
            columnWidth2=[80, 195],
            forceChangeCommand=True,
            insertionPosition=0,
            label="UV Set name: ", 
            parent=colCopyNewUVSet,
            text=pm.optionVar["copyNewUVSetOptVar"],
            textChangedCommand=lambda *args: copySetOptVar(),
        )
    
    # Button row
    rowCopyNewUVSet = pm.rowLayout(
        columnAttach2=["both", "both"], 
        numberOfColumns=2, 
        parent=frameCopyNewUVSet    
    )
    btnCreate = pm.button(
        command=lambda *args: core.dupeSet(scrollList, True, winCopyNewUVSet),
        label="Create",
        parent=rowCopyNewUVSet,
        width=(btnRow/2)
    )        
    btnClose = pm.button(
        command=lambda *args: pm.deleteUI(window), 
        label="Close",
        parent=rowCopyNewUVSet,
        width=(btnRow/2)
    ) 
    
    # Display the window
    pm.showWindow( window ) 
    

# UI for creating a new UV set
def createSetUI(scrollList):

    btnRow = 274
    winWidth = 300
    
    ## Internal method
    
    # Update optVars
    def createSetUpdateOptVar(varType):
    
        if varType == 0:
            pm.optionVar["newUVSetOptVar"] = fieldNewUVSet.getText()
        
        elif varType == 1:
            pm.optionVar["newUVSetShareOptVar"] = radGrpNewUVSet.getSelect()
        
        else:
            print("Error. Wrong variable passed to createSetUpdateOptVar()")
        

    ## Create UI
        
    # Check for window duplicate
    if pm.window( winNewUVSet, exists=True ):
        pm.deleteUI( winNewUVSet )

    # Window
    window = pm.window(
        winNewUVSet,
        minimizeButton=False, 
        maximizeButton=False, 
        resizeToFitChildren=True, 
        sizeable=False, 
        title="Create new UV Set", 
        width=winWidth 
    )
    
    # Layouts
    frameNewUVSet = pm.frameLayout(
        borderStyle="etchedIn", 
        collapsable=False, 
        collapse=False, 
        label="Options", 
        marginHeight=9, 
        marginWidth=9, 
        width=winWidth 
    )
    colNewUVSet = pm.columnLayout(
        adjustableColumn=True, 
        columnAlign="left", 
        rowSpacing=6,
        parent=frameNewUVSet
    )
    
    # Text field
    version = pm.about(version=True)
    if version.startswith("2012"): # Because the textChangedCommand didnt exist in Maya 2012...
        fieldNewUVSet = pm.textFieldGrp(
            changeCommand=lambda *args: createSetUpdateOptVar(0),
            columnAlign=[1, "right"], 
            columnWidth2=[80, 195],
            forceChangeCommand=True,
            insertionPosition=0,
            label="UV Set name: ", 
            parent=colNewUVSet,
            text=pm.optionVar["newUVSetOptVar"],
        )
    else:
        fieldNewUVSet = pm.textFieldGrp(
            changeCommand=lambda *args: createSetUpdateOptVar(0),
            columnAlign=[1, "right"], 
            columnWidth2=[80, 195],
            forceChangeCommand=True,
            insertionPosition=0,
            label="UV Set name: ", 
            parent=colNewUVSet,
            text=pm.optionVar["newUVSetOptVar"],
            textChangedCommand=lambda *args: createSetUpdateOptVar(0),
        )    
    
    # Radio collection and radio buttons
    radGrpNewUVSet = pm.radioButtonGrp(
        changeCommand=lambda *args: createSetUpdateOptVar(1), 
        columnAlign=[1, "right"],
        columnWidth2=[80, 195],
        label1="Shared (default)",
        label2="Per Instance Shared",
        label3="Per Instance Unshared",
        label="UV Set sharing: ", 
        numberOfRadioButtons=3,
        parent=colNewUVSet,
        vertical=True,
    )
    
    # Edit the radio collection and select item
    radGrpNewUVSet.setSelect( pm.optionVar["newUVSetShareOptVar"] )

    pm.setParent('..') # Parent up
    
    # Button row
    rowNewUVSet = pm.rowLayout(
        columnAttach3=["both", "both", "both"], 
        numberOfColumns=3, 
        parent=frameNewUVSet    
    )    
    btnCreate = pm.button(
        command=lambda *args: core.createSet(scrollList, winNewUVSet, False), 
        label="Create",
        parent=rowNewUVSet,
        width=(btnRow/3)
    )    
    btnApply = pm.button(
        command=lambda *args: core.createSet(scrollList, winNewUVSet, True), 
        label="Apply",
        parent=rowNewUVSet,
        width=(btnRow/3)
    )    
    btnClose = pm.button(
        command=lambda *args: pm.deleteUI(window), 
        label="Close",
        parent=rowNewUVSet,
        width=(btnRow/3)
    ) 
    
    # Display the window
    pm.showWindow( window ) 
    

# Ui for changing the automatic mapping options    
def mapAutoUI():

    # Vars    
    col1 = 170
    col2 = 110
    col3 = 150
    sepSpace = 5
    visState1 = False
    visState2 = True
    visState3 = False
    visState4 = True
    winWidth = 460


    ## Internal methods
    
    # Load selected as projection object
    def mapAutoLoadSel():
        
        # Check for mesh selection
        core.checkSel("mesh")
        
        # Get name from object
        projObj = pm.ls(selection=True, flatten=True)[0]
        
        # Update control, then the optVar
        fieldProjMapAuto.setText(projObj)
        mapAutoUpdateOptVar(5)
        
    
    # Switch projection method
    def mapAutoSwitch():
    
        if radGrpMethodMapAuto.getSelect() == 1:
            frameMSMapAuto.setVisible(True)
            frameProjMapAuto.setVisible(True)
            frameLayoutMapAuto.setVisible(True)
            frameSpaceMapAuto.setVisible(True)
            frameSetMapAuto.setVisible(True)
            textQuickMapAuto.setVisible(False)
        
        elif radGrpMethodMapAuto.getSelect() == 2:
            frameMSMapAuto.setVisible(False)
            frameProjMapAuto.setVisible(False)
            frameLayoutMapAuto.setVisible(False)
            frameSpaceMapAuto.setVisible(False)
            frameSetMapAuto.setVisible(False)
            textQuickMapAuto.setVisible(True)

        # Save optVar
        pm.optionVar["mapAutoMethodOptVar"] = radGrpMethodMapAuto.getSelect()       
        
        
    # Reset UI
    def mapAutoReset():
    
        # Update controls and optVars
        radGrpMethodMapAuto.setSelect(1)
        pm.optionVar["mapAutoMethodOptVar"] = 1
        
        menuMSMapAuto.setValue(6)
        menuMSMapAuto.setEnable(True)
        pm.optionVar["mapAutoMSMenuOptVar"] = 6

        radGrpMS1MapAuto.setSelect(2)
        pm.optionVar["mapAutoMS1RadGrpOptVar"] = 2
        
        radGrpMS2MapAuto.setSelect(1)
        pm.optionVar["mapAutoMS2RadGrpOptVar"] = 1
        
        cBox1MSMapAuto.setValue1(True)
        pm.optionVar["mapAutoMSBox1OptVar"] = True
        
        cBox2MSMapAuto.setValue1(True)
        pm.optionVar["mapAutoMSBox2OptVar"] = True
        
        cBoxProjMapAuto.setValue1(False)
        pm.optionVar["mapAutoProjBox1OptVar"] = False
        
        fieldProjMapAuto.setText("")
        fieldProjMapAuto.setEnable(False)
        pm.optionVar["mapAutoProjObjOptVar"] = ""
        
        cBoxProjBothMapAuto.setValue1(False)
        pm.optionVar["mapAutoProjBox2OptVar"] = False
        
        btnLoadProjMapAuto.setEnable(False)

        menuLayoutMapAuto.setValue("Into Square")
        pm.optionVar["mapAutoLayoutMenuOptVar"] = "Into Square"
        
        radGrpLayoutScaleMapAuto.setSelect(2)
        pm.optionVar["mapAutoLayoutRadGrp1OptVar"] = 2
        
        radGrpLayoutStackMapAuto.setSelect(1)
        pm.optionVar["mapAutoLayoutRadGrp2OptVar"] = 1
        
        cBoxNormMapAuto.setValue1(False)
        pm.optionVar["mapAutoNormBoxOptVar"] = False
        
        menuSpaceMapAuto.setSelect(5)
        menuSpaceMapAuto.setEnable(True)
        pm.optionVar["mapAutoSpaceMenuOptVar"] = "512 Map"
        
        sliderSpaceMapAuto.setValue(0.2000)
        sliderSpaceMapAuto.setEnable(True)
        pm.optionVar["mapAutoSpaceValOptVar"] = 0.2000
        
        cBoxSetMapAuto.setValue1(False)
        pm.optionVar["mapAutoSetBoxOptVar"] = False
        
        fieldSetMapAuto.setText("uvSet1")
        fieldSetMapAuto.setEnable(False)
        pm.optionVar["mapAutoSetOptVar"] = "uvSet1"        
        
        # Hide inactive
        mapAutoSwitch()
        
        
    # Update optVar
    def mapAutoUpdateOptVar(varType):
    
        if varType == 1:
            pm.optionVar["mapAutoMSMenuOptVar"] = menuMSMapAuto.getValue()
            
        elif varType == 2:
            pm.optionVar["mapAutoMS1RadGrpOptVar"] = radGrpMS1MapAuto.getSelect()
            
        elif varType == 3:
            pm.optionVar["mapAutoMSBox1OptVar"] = cBox1MSMapAuto.getValue1()
        
        elif varType == 4:
            pm.optionVar["mapAutoProjBox1OptVar"] = cBoxProjMapAuto.getValue1()

            # Turn on/off UI controls
            if pm.optionVar["mapAutoProjBox1OptVar"] == False:
                menuMSMapAuto.setEnable(True)
                fieldProjMapAuto.setEnable(False)
                cBoxProjBothMapAuto.setEnable(False)
                btnLoadProjMapAuto.setEnable(False)
            else:
                menuMSMapAuto.setEnable(False)
                fieldProjMapAuto.setEnable(True)
                cBoxProjBothMapAuto.setEnable(True)
                btnLoadProjMapAuto.setEnable(True)
        
        elif varType == 5:
            pm.optionVar["mapAutoProjObjOptVar"] = fieldProjMapAuto.getText()
        
        elif varType == 6:
            pm.optionVar["mapAutoProjBox2OptVar"] = cBoxProjBothMapAuto.getValue1()
        
        elif varType == 7:
            pm.optionVar["mapAutoLayoutMenuOptVar"] = menuLayoutMapAuto.getValue()
        
            # Turn on/off UI controls
            if pm.optionVar["mapAutoLayoutMenuOptVar"] == "Into Square":
                menuSpaceMapAuto.setEnable(True)
                sliderSpaceMapAuto.setEnable(True)
            else:
                menuSpaceMapAuto.setEnable(False)
                sliderSpaceMapAuto.setEnable(False)             
        
        elif varType == 8:
            pm.optionVar["mapAutoLayoutRadGrp1OptVar"] = radGrpLayoutScaleMapAuto.getSelect()
        
        elif varType == 9:
            pm.optionVar["mapAutoLayoutRadGrp2OptVar"] = radGrpLayoutStackMapAuto.getSelect()
        
        elif varType == 10:
            pm.optionVar["mapAutoSpaceMenuOptVar"] = menuSpaceMapAuto.getValue()
            
            # Update slider w preset
            if pm.optionVar["mapAutoSpaceMenuOptVar"] == "4096 Map":
                sliderSpaceMapAuto.setValue(0.0250)
                pm.optionVar["mapAutoSpaceValOptVar"] = 0.0250
            
            elif pm.optionVar["mapAutoSpaceMenuOptVar"] == "2048 Map":
                sliderSpaceMapAuto.setValue(0.0500)
                pm.optionVar["mapAutoSpaceValOptVar"] = 0.0500
            
            elif pm.optionVar["mapAutoSpaceMenuOptVar"] == "1024 Map":
                sliderSpaceMapAuto.setValue(0.1000)
                pm.optionVar["mapAutoSpaceValOptVar"] = 0.1000
                
            elif pm.optionVar["mapAutoSpaceMenuOptVar"] == "512 Map":
                sliderSpaceMapAuto.setValue(0.2000)
                pm.optionVar["mapAutoSpaceValOptVar"] = 0.2000
                
            elif pm.optionVar["mapAutoSpaceMenuOptVar"] == "256 Map":
                sliderSpaceMapAuto.setValue(0.4000)
                pm.optionVar["mapAutoSpaceValOptVar"] = 0.4000
                
            elif pm.optionVar["mapAutoSpaceMenuOptVar"] == "128 Map":
                sliderSpaceMapAuto.setValue(0.8000)
                pm.optionVar["mapAutoSpaceValOptVar"] = 0.8000
                
            elif pm.optionVar["mapAutoSpaceMenuOptVar"] == "64 Map":
                sliderSpaceMapAuto.setValue(1.6000)
                pm.optionVar["mapAutoSpaceValOptVar"] = 1.6000
            
        elif varType == 11:
            pm.optionVar["mapAutoSpaceValOptVar"] = sliderSpaceMapAuto.getValue()
            
            # Select custom in preset menu
            menuSpaceMapAuto.setValue("Custom")
            
            
        elif varType == 12:
            pm.optionVar["mapAutoSetBoxOptVar"] = cBoxSetMapAuto.getValue1()     

            # Turn on/off UI controls
            if pm.optionVar["mapAutoSetBoxOptVar"] == False:
                fieldSetMapAuto.setEnable(False)
            else:
                fieldSetMapAuto.setEnable(True)
                
        elif varType == 13:
            pm.optionVar["mapAutoSetOptVar"] = fieldSetMapAuto.getText()
        
        elif varType == 14:
            pm.optionVar["mapAutoNormBoxOptVar"] = cBoxNormMapAuto.getValue1()
            
        elif varType == 15:
            pm.optionVar["mapAutoMS2RadGrpOptVar"] = radGrpMS2MapAuto.getSelect()
            
        elif varType == 16:
            pm.optionVar["mapAutoMSBox2OptVar"] = cBox2MSMapAuto.getValue1()
        
        
    ## Create UI
    
    # Check for window duplicate
    if pm.window( winMapAuto, exists=True ):
        pm.deleteUI( winMapAuto )
        
    # Read UI control optVars - Set visibility states
    if pm.optionVar["mapAutoProjBox1OptVar"] == True:    
        visState1 = True
    
    if pm.optionVar["mapAutoLayoutMenuOptVar"] != "Into Square":
        visState2 = False
    
    if pm.optionVar["mapAutoSetBoxOptVar"] == True:
        visState3 = True
        
    # Window 
    window = pm.window(
        winMapAuto,
        minimizeButton=True, 
        maximizeButton=True, 
        sizeable=True, 
        title="UV Mapping: Automatic Projection", 
        width=winWidth
    )
        
    # Create layouts
    form1MapAuto = pm.formLayout()
    scrollMapAuto = pm.scrollLayout( childResizable=True )
    form2MapAuto = pm.formLayout( parent=scrollMapAuto )
    
    frameMainMapAuto = pm.frameLayout(
        borderVisible=False,
        collapsable=False, 
        label="Projection Options",
        parent=form2MapAuto
    )
    
    # Method radioBtnGrp
    radGrpMethodMapAuto = pm.radioButtonGrp(
        changeCommand=lambda *args: mapAutoSwitch(),
        columnWidth2=[col1, col2],
        label="Method: ",
        labelArray2=["Custom", "Quick"],
        numberOfRadioButtons=2,
        parent=frameMainMapAuto,
        select=pm.optionVar["mapAutoMethodOptVar"],
        vertical=True,
    )
    
    ## Custom
    # Mapping Settings: Frame and column
    frameMSMapAuto = pm.frameLayout(
        borderStyle="out",
        label="Mapping Settings",
        parent=form2MapAuto
    )
    colMSMapAuto = pm.columnLayout(
        parent=frameMSMapAuto
    )
        
    # Mapping Settings: UI elements
    menuMSMapAuto = pm.optionMenuGrp(
        changeCommand=lambda *args: mapAutoUpdateOptVar(1),
        columnWidth2=[col1, col2],
        enable=visState4,
        label="Planes: ",
        parent=colMSMapAuto,
    )    
    
    planes3 = pm.menuItem( label="3")
    planes4 = pm.menuItem( label="4")
    planes6 = pm.menuItem( label="6")
    planes8 = pm.menuItem( label="8")
    planes10 = pm.menuItem( label="10")
    planes12 = pm.menuItem( label="12")
    
    menuMSMapAuto.setValue(pm.optionVar["mapAutoMSMenuOptVar"])
    
    radGrpMS1MapAuto = pm.radioButtonGrp(
        changeCommand=lambda *args: mapAutoUpdateOptVar(2),
        columnWidth2=[col1, col2],
        label1="Less distortion",
        label2="Fewer pieces",
        label="Optimize for: ",
        numberOfRadioButtons=2,
        parent=colMSMapAuto,
        select=pm.optionVar["mapAutoMS1RadGrpOptVar"],
        vertical=True,
    )
    sep1MapAuto = pm.separator(
        height=sepSpace,
        horizontal=True,
        parent=colMSMapAuto,
        visible=True,
    )
    radGrpMS2MapAuto = pm.radioButtonGrp(
        changeCommand=lambda *args: mapAutoUpdateOptVar(15),
        columnWidth2=[col1, col2],
        label1="World",
        label2="Local",
        label="Sample space: ",
        numberOfRadioButtons=2,
        parent=colMSMapAuto,
        select=pm.optionVar["mapAutoMS2RadGrpOptVar"],
        vertical=True,
    )
    cBox1MSMapAuto = pm.checkBoxGrp(
        changeCommand=lambda *args: mapAutoUpdateOptVar(3),
        columnWidth2=[col1, col2],
        label="",
        label1="Insert projection before deformers",
        parent=colMSMapAuto,
        value1=pm.optionVar["mapAutoMSBox1OptVar"],
    )
    cBox2MSMapAuto = pm.checkBoxGrp(
        changeCommand=lambda *args: mapAutoUpdateOptVar(16),
        columnWidth2=[col1, col2],
        label="",
        label1="Show projection manipulator(s)",
        parent=colMSMapAuto,
        value1=pm.optionVar["mapAutoMSBox2OptVar"],
    )
    sep2MapAuto = pm.separator(
        height=sepSpace,
        horizontal=True,
        parent=colMSMapAuto,
        visible=True,
    )
    
    # Projection: Frame and column
    frameProjMapAuto = pm.frameLayout(
        borderStyle="out",
        label="Custom Projection",
        parent=form2MapAuto
    )
    colProjMapAuto = pm.columnLayout(
        parent=frameProjMapAuto
    )
    
    # Projection: UI elements
    cBoxProjMapAuto = pm.checkBoxGrp(
        changeCommand=lambda *args: mapAutoUpdateOptVar(4),
        columnWidth2=[col1, col2],
        label="",
        label1="Load projection",
        parent=colProjMapAuto,
        value1=pm.optionVar["mapAutoProjBox1OptVar"],
    )
    version = pm.about(version=True)
    if version.startswith("2012"): # Because the textChangedCommand didnt exist in Maya 2012...
        fieldProjMapAuto = pm.textFieldGrp(
            changeCommand=lambda *args: mapAutoUpdateOptVar(5),
            columnWidth2=[col1, (col2+col3)],
            enable=visState1,
            label="Projection object: ",
            parent=colProjMapAuto,
            text=pm.optionVar["mapAutoProjObjOptVar"],
        )
    else:
        fieldProjMapAuto = pm.textFieldGrp(
            changeCommand=lambda *args: mapAutoUpdateOptVar(5),
            columnWidth2=[col1, (col2+col3)],
            enable=visState1,
            label="Projection object: ",
            parent=colProjMapAuto,
            text=pm.optionVar["mapAutoProjObjOptVar"],
            textChangedCommand=lambda *args: mapAutoUpdateOptVar(5),
        )
    cBoxProjBothMapAuto = pm.checkBoxGrp(
        changeCommand=lambda *args: mapAutoUpdateOptVar(6),
        columnWidth2=[col1, col2],
        enable=visState1,
        label="",
        label1="Project both directions",
        parent=colProjMapAuto,
        value1=pm.optionVar["mapAutoProjBox2OptVar"],
    )
    rowLoadSelMapAuto = pm.rowLayout(
        columnWidth=[col1, col2],
        numberOfColumns=2,
        parent=colProjMapAuto, 
    )
    fillerMapAuto = pm.text(label="", width=col1)
    btnLoadProjMapAuto = pm.button(
        command=lambda *args: mapAutoLoadSel(),
        enable=visState1,
        label="Load Selected",
        parent=rowLoadSelMapAuto,
        width=(col2+col3),
    )
    sep3MapAuto = pm.separator(
        height=sepSpace,
        horizontal=True,
        parent=colProjMapAuto,
        visible=True,
    )
    
    # Layout: Frame and column
    frameLayoutMapAuto = pm.frameLayout(
        borderStyle="out",
        label="Layout Shells",
        parent=form2MapAuto
    )
    colLayoutMapAuto = pm.columnLayout(
        parent=frameLayoutMapAuto
    )
    
    # Layout: UI elements
    menuLayoutMapAuto = pm.optionMenuGrp(
        changeCommand=lambda *args: mapAutoUpdateOptVar(7),
        columnWidth2=[col1, col2],
        label="Shell layout: ",
        parent=colLayoutMapAuto,
    )    
    
    layout1 = pm.menuItem( label="Overlap")
    layout2 = pm.menuItem( label="Along U")
    layout3 = pm.menuItem( label="Into Square")
    layout4 = pm.menuItem( label="Tile")
    
    menuLayoutMapAuto.setValue(pm.optionVar["mapAutoLayoutMenuOptVar"])
    
    radGrpLayoutScaleMapAuto = pm.radioButtonGrp(
        changeCommand=lambda *args: mapAutoUpdateOptVar(8),
        columnWidth2=[col1, col2],
        label1="None",
        label2="Uniform",
        label3="Stretch to square",
        label="Scale mode: ",
        numberOfRadioButtons=3,
        parent=colLayoutMapAuto,
        select=pm.optionVar["mapAutoLayoutRadGrp1OptVar"],
        vertical=True,
    )
    sep4MapAuto = pm.separator(
        height=sepSpace,
        horizontal=True,
        parent=colLayoutMapAuto,
        visible=True,
    )
    radGrpLayoutStackMapAuto = pm.radioButtonGrp(
        changeCommand=lambda *args: mapAutoUpdateOptVar(9),
        columnWidth2=[col1, col2],
        label1="Bounding box",
        label2="Shape",
        label="Shell stacking: ",
        numberOfRadioButtons=2,
        parent=colLayoutMapAuto,
        select=pm.optionVar["mapAutoLayoutRadGrp2OptVar"],
        vertical=True,
    )
    cBoxNormMapAuto = pm.checkBoxGrp(
        changeCommand=lambda *args: mapAutoUpdateOptVar(14),
        columnWidth2=[col1, col2],
        label="",
        label1="Normalize",
        parent=colLayoutMapAuto,
        value1=pm.optionVar["mapAutoNormBoxOptVar"],
    )
    sep5MapAuto = pm.separator(
        height=sepSpace,
        horizontal=True,
        parent=colLayoutMapAuto,
        visible=True,
    )
    
    # Shell spacing: Frame and column
    frameSpaceMapAuto = pm.frameLayout(
        borderStyle="out",
        label="Shell Spacing",
        parent=form2MapAuto
    )
    colSpaceMapAuto = pm.columnLayout(
        parent=frameSpaceMapAuto
    )
    
    # Shell spacing: UI elements
    menuSpaceMapAuto = pm.optionMenuGrp(
        changeCommand=lambda *args: mapAutoUpdateOptVar(10),
        columnWidth2=[col1, col2],
        enable=visState2,
        label="Spacing preset: ",
        parent=colSpaceMapAuto,
    )    
    
    preset1 = pm.menuItem( label="Custom")
    preset2 = pm.menuItem( label="4096 Map")
    preset3 = pm.menuItem( label="2048 Map")
    preset4 = pm.menuItem( label="1024 Map")
    preset5 = pm.menuItem( label="512 Map")
    preset6 = pm.menuItem( label="256 Map")
    preset7 = pm.menuItem( label="128 Map")
    preset8 = pm.menuItem( label="64 Map")
    
    menuSpaceMapAuto.setValue(pm.optionVar["mapAutoSpaceMenuOptVar"])
    
    sliderSpaceMapAuto = pm.floatSliderGrp(
        changeCommand=lambda *args: mapAutoUpdateOptVar(11),
        columnWidth3=[col1, col2, col3],
        enable=visState2,
        field=True,
        fieldMinValue=0.0000,
        fieldMaxValue=5.0000,
        label="Percentage Space: ",
        minValue=0.0000,
        maxValue=5.0000,
        parent=colSpaceMapAuto,
        precision=4,
        step=0.1,
        value=pm.optionVar["mapAutoSpaceValOptVar"],
    )
    sep6MapAuto = pm.separator(
        height=sepSpace,
        horizontal=True,
        parent=colSpaceMapAuto,
        visible=True,
    )
    
    # UV Set: Frame and column
    frameSetMapAuto = pm.frameLayout(
        borderStyle="out",
        label="UV Set",
        parent=form2MapAuto
    )
    colSetMapAuto = pm.columnLayout(
        parent=frameSetMapAuto
    )
    
    # UV Set: UI elements
    cBoxSetMapAuto = pm.checkBoxGrp(
        changeCommand=lambda *args: mapAutoUpdateOptVar(12),
        columnWidth2=[col1, col2],
        label="",
        label1="Create new UV set",
        parent=colSetMapAuto,
        value1=pm.optionVar["mapAutoSetBoxOptVar"],
    )
    version = pm.about(version=True)
    if version.startswith("2012"): # Because the textChangedCommand didnt exist in Maya 2012...
        fieldSetMapAuto = pm.textFieldGrp(
            changeCommand=lambda *args: mapAutoUpdateOptVar(13),
            columnWidth2=[col1, (col2+col3)],
            enable=visState3,
            label="UV set name: ",
            parent=colSetMapAuto,
            text=pm.optionVar["mapAutoSetOptVar"],
        )
    else:
        fieldSetMapAuto = pm.textFieldGrp(
            changeCommand=lambda *args: mapAutoUpdateOptVar(13),
            columnWidth2=[col1, (col2+col3)],
            enable=visState3,
            label="UV set name: ",
            parent=colSetMapAuto,
            text=pm.optionVar["mapAutoSetOptVar"],
            textChangedCommand=lambda *args: mapAutoUpdateOptVar(13),
        )
    sep7MapAuto = pm.separator(
        height=sepSpace,
        horizontal=True,
        parent=colSetMapAuto,
        visible=True,
    )
    
    
    ## Quick
    textQuickMapAuto = pm.text(
        label="No options here - Things just get done!!",
        parent=form2MapAuto
    )
    
    # Buttons
    btnApplyCloseMapAuto = pm.button(
        command=lambda *args: core.mapping("auto", None, winMapAuto), 
        label="Confirm",
        parent=form1MapAuto,
    )
    btnApplyMapAuto = pm.button(
        command=lambda *args: core.mapping("auto"), 
        label="Apply",
        parent=form1MapAuto,
    )
    btnResetMapAuto = pm.button( 
        command=lambda *args: mapAutoReset(),
        label="Reset", 
        parent=form1MapAuto,  
    )
    btnCloseMapAuto = pm.button( 
        command=lambda *args: pm.deleteUI( winMapAuto ),
        label="Close", 
        parent=form1MapAuto,  
    )
   
    # Layout frames
    pm.formLayout(
        form2MapAuto, edit=True, 
        attachForm=[
        
            (frameMainMapAuto, "top", 0), 
            (frameMainMapAuto, "left", 0), 
            (frameMainMapAuto, "right", 0),  
        
            (frameMSMapAuto, "left", 0), 
            (frameMSMapAuto, "right", 0), 

            (frameProjMapAuto, "left", 0), 
            (frameProjMapAuto, "right", 0), 

            (frameLayoutMapAuto, "left", 0), 
            (frameLayoutMapAuto, "right", 0), 
            
            (frameSpaceMapAuto, "left", 0), 
            (frameSpaceMapAuto, "right", 0), 
            
            (frameSetMapAuto, "left", 0), 
            (frameSetMapAuto, "right", 0), 
            
            (textQuickMapAuto, "left", 0), 
            (textQuickMapAuto, "right", 0), 
        ], 
        attachControl=[            
            (frameMSMapAuto, "top", 10, frameMainMapAuto), 
            
            (frameProjMapAuto, "top", 10, frameMSMapAuto), 
            
            (frameLayoutMapAuto, "top", 10, frameProjMapAuto), 
            
            (frameSpaceMapAuto, "top", 10, frameLayoutMapAuto), 
            
            (frameSetMapAuto, "top", 10, frameSpaceMapAuto),
            
            (textQuickMapAuto, "top", 0, frameSetMapAuto), 
        ],
        attachNone=[
            (frameMSMapAuto, "bottom"),
            
            (frameProjMapAuto, "bottom"), 
            
            (frameLayoutMapAuto, "bottom"), 
            
            (frameSpaceMapAuto, "bottom"), 
            
            (frameSetMapAuto, "bottom"), 
            
            (textQuickMapAuto, "bottom"), 
        ]
    )

    # Layout main frame
    pm.formLayout(
        form1MapAuto, edit=True, 
        attachForm=[
            (scrollMapAuto, "top", 0),
            (scrollMapAuto, "left", 0),
            (scrollMapAuto, "right", 0),

            (btnApplyCloseMapAuto, "left", 5),         
            (btnApplyCloseMapAuto, "bottom", 5),         
            (btnApplyMapAuto, "bottom", 5),                
            (btnResetMapAuto, "bottom", 5),         
            (btnCloseMapAuto, "right", 5),         
            (btnCloseMapAuto, "bottom", 5),     
        ], 
        attachControl=[
            (scrollMapAuto, "bottom", 0, btnApplyCloseMapAuto), 
        ],
        attachPosition=[
            (btnApplyCloseMapAuto, "right", 3, 25),                   
            (btnApplyMapAuto, "left", 2, 25),                   
            (btnApplyMapAuto, "right", 3, 50),                   
            (btnResetMapAuto, "right", 3, 75),                   
            (btnResetMapAuto, "left", 2, 50),                   
            (btnCloseMapAuto, "left", 2, 75),       
        ],
        attachNone=[
            (btnApplyCloseMapAuto, "top"),    
            (btnApplyMapAuto, "top"),    
            (btnResetMapAuto, "top"),    
            (btnCloseMapAuto, "top"),    
        ],
    )
    
    # Hide inactive
    mapAutoSwitch()
    
    # Display the window
    pm.showWindow( window ) 
    
    
# UI for changing the cylindrical mapping options 
def mapCylindricalUI():

    # Vars
    col1 = 170
    col2 = 110
    col3 = 150
    sepSpace = 5
    visState = False
    winWidth = 460
    
    
    ## Internal methods
    
    # Reset UI
    def mapCylindricalReset():
        
        # Update controls and optVars
        sliderMapCylindrical.setValue(180)
        pm.optionVar["mapCylindricalSweepOptVar"] = 180
        
        cBox1MSMapCylindrical.setValue1(True)
        pm.optionVar["mapCylindricalMS1BoxOptVar"] = True
        
        cBox2MSMapCylindrical.setValue1(True)
        pm.optionVar["mapCylindricalMS2BoxOptVar"] = True
        
        cBoxSetMapCylindrical.setValue1(False)
        fieldSetMapCylindrical.setEnable(False)
        pm.optionVar["mapCylindricalSetBoxOptVar"] = False
        
        fieldSetMapCylindrical.setText("uvSet1")
        pm.optionVar["mapCylindricalSetOptVar"] = "uvSet1"
        
    
    # Update optVar
    def mapCylindricalUpdateOptVar(varType):

        if varType == 1:
            pm.optionVar["mapCylindricalMS1BoxOptVar"] = cBox1MSMapCylindrical.getValue1()
            
        elif varType == 2:
            pm.optionVar["mapCylindricalMS2BoxOptVar"] = cBox2MSMapCylindrical.getValue1()
    
        elif varType == 3:
            pm.optionVar["mapCylindricalSetBoxOptVar"] = cBoxSetMapCylindrical.getValue1()
            
            # Turn on/off UI controls
            if pm.optionVar["mapCylindricalSetBoxOptVar"] == False:
                fieldSetMapCylindrical.setEnable(False)
            else:
                fieldSetMapCylindrical.setEnable(True)
    
        elif varType == 4:
            pm.optionVar["mapCylindricalSetOptVar"] = fieldSetMapCylindrical.getText()
            
        elif varType == 5:
            pm.optionVar["mapCylindricalSweepOptVar"] = sliderMapCylindrical.getValue()
            
            
    ## Create UI
    
    # Check for window duplicate
    if pm.window( winMapCylindrical, exists=True ):
        pm.deleteUI( winMapCylindrical )
       
    # Read UI control optVar - Set visibility state
    if pm.optionVar["mapCylindricalSetOptVar"] == True:    
        visState = True
       
    # Window 
    window = pm.window(
        winMapCylindrical,
        minimizeButton=True, 
        maximizeButton=True, 
        sizeable=True, 
        title="UV Mapping: Cylindrical Projection", 
        width=winWidth
    )
        
    # Create layout
    form1MapCylindrical = pm.formLayout()
    scrollMapCylindrical = pm.scrollLayout( childResizable=True )
    form2MapCylindrical = pm.formLayout( parent=scrollMapCylindrical )
    
    # Mapping Settings: Frame and column
    frameMainMapCylindrical = pm.frameLayout(
        borderVisible=False,
        label="Mapping Settings",
        parent=form2MapCylindrical,
    )
    colSetCylindrical = pm.columnLayout(
        parent=frameMainMapCylindrical
    )
    
    # Mapping Settings: UI elements
    sliderMapCylindrical = pm.floatSliderGrp(
        changeCommand=lambda *args: mapCylindricalUpdateOptVar(5),
        columnWidth3=[col1, col2, col3],
        field=True,
        fieldMinValue=0.00,
        fieldMaxValue=360.00,
        label="Projection Sweep: ",
        minValue=0.00,
        maxValue=360.00,
        parent=colSetCylindrical,
        precision=2,
        step=0.1,
        value=pm.optionVar["mapCylindricalSweepOptVar"], 
    )    
    cBox1MSMapCylindrical = pm.checkBoxGrp(
        changeCommand=lambda *args: mapCylindricalUpdateOptVar(1),
        columnWidth2=[col1, col2],
        label="",
        label1="Insert projection before deformers",
        parent=colSetCylindrical,
        value1=pm.optionVar["mapCylindricalMS1BoxOptVar"],
    )
    cBox2MSMapCylindrical = pm.checkBoxGrp(
        changeCommand=lambda *args: mapCylindricalUpdateOptVar(2),
        columnWidth2=[col1, col2],
        label="",
        label1="Show projection manipulator(s)",
        parent=colSetCylindrical,
        value1=pm.optionVar["mapCylindricalMS2BoxOptVar"],
    )
    sep1MapCylindrical = pm.separator(
        height=sepSpace,
        horizontal=True,
        parent=colSetCylindrical,
        visible=True,
    )
    
    # UV Set: Frame and column
    frameSetMapCylindrical = pm.frameLayout(
        borderStyle="out",
        label="UV Set",
        parent=form2MapCylindrical
    )
    colSetMapCylindrical = pm.columnLayout(
        parent=frameSetMapCylindrical
    )
    
    # UV Set: UI elements
    cBoxSetMapCylindrical = pm.checkBoxGrp(
        changeCommand=lambda *args: mapCylindricalUpdateOptVar(3),
        columnWidth2=[col1, col2],
        label="",
        label1="Create new UV set",
        parent=colSetMapCylindrical,
        value1=pm.optionVar["mapCylindricalSetBoxOptVar"],
    )
    version = pm.about(version=True)
    if version.startswith("2012"): # Because the textChangedCommand didnt exist in Maya 2012...
        fieldSetMapCylindrical = pm.textFieldGrp(
            changeCommand=lambda *args: mapCylindricalUpdateOptVar(4),
            columnWidth2=[col1, (col2+col3)],
            enable=visState,
            label="UV set name: ",
            parent=colSetMapCylindrical,
            text=pm.optionVar["mapCylindricalSetOptVar"],
        )
    else:
        fieldSetMapCylindrical = pm.textFieldGrp(
            changeCommand=lambda *args: mapCylindricalUpdateOptVar(4),
            columnWidth2=[col1, (col2+col3)],
            enable=visState,
            label="UV set name: ",
            parent=colSetMapCylindrical,
            text=pm.optionVar["mapCylindricalSetOptVar"],
            textChangedCommand=lambda *args: mapCylindricalUpdateOptVar(4),
        )
    sep2MapCylindrical = pm.separator(
        height=sepSpace,
        horizontal=True,
        parent=colSetMapCylindrical,
        visible=True,
    )
    
    # Buttons
    btnApplyCloseMapCylindrical = pm.button(
        command=lambda *args: core.mapping("cyl", None, winMapCylindrical), 
        label="Confirm",
        parent=form1MapCylindrical,
    )
    btnApplyMapCylindrical = pm.button(
        command=lambda *args: core.mapping("cyl"), 
        label="Apply",
        parent=form1MapCylindrical,
    )
    btnResetMapCylindrical = pm.button( 
        command=lambda *args: mapCylindricalReset(),
        label="Reset", 
        parent=form1MapCylindrical,  
    )
    btnCloseMapCylindrical = pm.button( 
        command=lambda *args: pm.deleteUI( winMapCylindrical ),
        label="Close", 
        parent=form1MapCylindrical,  
    )
    
    # Layout frames
    pm.formLayout(
        form2MapCylindrical, edit=True, 
        attachForm=[
            (frameMainMapCylindrical, "top", 0), 
            (frameMainMapCylindrical, "left", 0),
            (frameMainMapCylindrical, "right", 0), 
            
            (frameSetMapCylindrical, "left", 0),
            (frameSetMapCylindrical, "right", 0), 
        ], 
        attachControl=[ 
            (frameSetMapCylindrical, "top", 10, frameMainMapCylindrical), 
        ],
        attachNone=[
            (frameSetMapCylindrical, "bottom"),    
        ],
    )

    # Layout main frame
    pm.formLayout(
        form1MapCylindrical, edit=True, 
        attachForm=[
            (scrollMapCylindrical, "top", 0),
            (scrollMapCylindrical, "left", 0),
            (scrollMapCylindrical, "right", 0),
    
            (btnApplyCloseMapCylindrical, "left", 5),         
            (btnApplyCloseMapCylindrical, "bottom", 5),         
            (btnApplyMapCylindrical, "bottom", 5),
            (btnResetMapCylindrical, "bottom", 5),
            (btnCloseMapCylindrical, "right", 5),         
            (btnCloseMapCylindrical, "bottom", 5),
        ],
        attachControl=[ 
            (scrollMapCylindrical, "bottom", 0, btnApplyCloseMapCylindrical), 
        ],
        attachPosition=[
            (btnApplyCloseMapCylindrical, "right", 3, 25),                   
            (btnApplyMapCylindrical, "left", 2, 25),                   
            (btnApplyMapCylindrical, "right", 3, 50),     
            (btnResetMapCylindrical, "right", 3, 75),                   
            (btnResetMapCylindrical, "left", 2, 50),     
            (btnCloseMapCylindrical, "left", 2, 75),       
        ],
        attachNone=[
            (btnApplyCloseMapCylindrical, "top"),    
            (btnApplyMapCylindrical, "top"),    
            (btnResetMapCylindrical, "top"),    
            (btnCloseMapCylindrical, "top"),      
        ],
    )
    
    # Display the window
    pm.showWindow( window )  


# UI for changing the normal based mapping options 
def mapNormalUI():

    # Vars
    col1 = 170
    col2 = 110
    col3 = 150
    sepSpace = 5
    visState = False
    winWidth = 460
    
    
    ## Internal methods
    
    # Reset UI
    def mapNormalReset():
        
        # Update controls and optVars
        cBox1MSMapNormal.setValue1(True)
        pm.optionVar["mapNormalMS1OptVar"] = True
        
        cBox2MSMapNormal.setValue1(True)
        pm.optionVar["mapNormalMS2OptVar"] = True
        
        cBox3MSMapNormal.setValue1(True)
        pm.optionVar["mapNormalMS3OptVar"] = True
        
        cBoxSetMapNormal.setValue1(False)
        fieldSetMapNormal.setEnable(False)
        pm.optionVar["mapNormalSetBoxOptVar"] = False

        fieldSetMapNormal.setText("uvSet1")
        fieldSetMapNormal.setEnable(False)
        pm.optionVar["mapNormalSetOptVar"] = "uvSet1"        
        
    
    # Update optVar
    def mapNormalUpdateOptVar(varType):

        if varType == 1:
            pm.optionVar["mapNormalMS1OptVar"] = cBox1MSMapNormal.getValue1()
            
            # Turn on/off UI controls
            if pm.optionVar["mapNormalSetBoxOptVar"] == False:
                fieldSetMapNormal.setEnable(False)
            else:
                fieldSetMapNormal.setEnable(True)
            
        elif varType == 2:
            pm.optionVar["mapNormalMS2OptVar"] = cBox2MSMapNormal.getValue1()
            
        elif varType == 3:
            pm.optionVar["mapNormalMS3OptVar"] = cBox3MSMapNormal.getValue1()
    
        elif varType == 4:
            pm.optionVar["mapNormalSetBoxOptVar"] = cBoxSetMapNormal.getValue1()

            if pm.optionVar["mapNormalSetBoxOptVar"] == True:
                fieldSetMapNormal.setEnable(True)
            else:
                fieldSetMapNormal.setEnable(False)
                
            
        elif varType == 5:
            pm.optionVar["mapNormalSetOptVar"] = fieldSetMapNormal.getText()

            
            
    ## Create UI
    
    # Check for window duplicate
    if pm.window( winMapNormal, exists=True ):
        pm.deleteUI( winMapNormal )
       
    # Read UI control optVar - Set visibility state
    if pm.optionVar["mapNormalSetOptVar"] == True:    
        visState = True
       
    # Window 
    window = pm.window(
        winMapNormal,
        minimizeButton=True, 
        maximizeButton=True, 
        sizeable=True, 
        title="UV Mapping: Normal Based Projection", 
        width=winWidth
    )
        
    # Create layout
    form1MapNormal = pm.formLayout()
    scrollMapNormal = pm.scrollLayout( childResizable=True )
    form2MapNormal = pm.formLayout( parent=scrollMapNormal )
    
    frameMainMapNormal = pm.frameLayout(
        borderVisible=False,
        collapsable=False, 
        label="Description",
        parent=form2MapNormal
    )    
    
    sep1MapNormal = pm.separator(
        height=1,
        horizontal=True,
        parent=frameMainMapNormal,
        style="none",
        visible=True,
    )
    
    # Description text
    textDescMapNormal = pm.text(
        label="Creates a planar projection based on the average \n"
              "vector of the face normals in the active selection.\n"
              "Try and avoid backface selections for best results.",
        parent=frameMainMapNormal,
        width=(col1 + col2 + col3),
    )
    
    sep2MapNormal = pm.separator(
        height=sepSpace,
        horizontal=True,
        parent=frameMainMapNormal,
        style="none",
        visible=True,
    )

    # Mapping Settings: Frame and column
    frameMSMapNormal = pm.frameLayout(
        borderVisible=False,
        label="Mapping Settings",
        parent=form2MapNormal,
    )
    colSetNormal = pm.columnLayout(
        parent=frameMSMapNormal
    )
    
    # Mapping Settings: UI elements
    cBox1MSMapNormal = pm.checkBoxGrp(
        changeCommand=lambda *args: mapNormalUpdateOptVar(1),
        columnWidth2=[col1, col2],
        label="",
        label1="Keep width/height ratio",
        parent=colSetNormal,
        value1=pm.optionVar["mapNormalMS1OptVar"],
    )
    cBox2MSMapNormal = pm.checkBoxGrp(
        changeCommand=lambda *args: mapNormalUpdateOptVar(2),
        columnWidth2=[col1, col2],
        label="",
        label1="Insert projection before deformers",
        parent=colSetNormal,
        value1=pm.optionVar["mapNormalMS2OptVar"],
    )
    cBox3MSMapNormal = pm.checkBoxGrp(
        changeCommand=lambda *args: mapNormalUpdateOptVar(3),
        columnWidth2=[col1, col2],
        label="",
        label1="Show projection manipulator(s)",
        parent=colSetNormal,
        value1=pm.optionVar["mapNormalMS3OptVar"],
    )
    
    sep3MapNormal = pm.separator(
        height=sepSpace,
        horizontal=True,
        parent=colSetNormal,
        visible=True,
    )
    
    # UV Set: Frame and column
    frameSetMapNormal = pm.frameLayout(
        borderStyle="out",
        label="UV Set",
        parent=form2MapNormal
    )
    colSetMapNormal = pm.columnLayout(
        parent=frameSetMapNormal
    )
    
    # UV Set: UI elements
    cBoxSetMapNormal = pm.checkBoxGrp(
        changeCommand=lambda *args: mapNormalUpdateOptVar(4),
        columnWidth2=[col1, col2],
        label="",
        label1="Create new UV set",
        parent=colSetMapNormal,
        value1=pm.optionVar["mapNormalSetBoxOptVar"],
    )
    version = pm.about(version=True)
    if version.startswith("2012"): # Because the textChangedCommand didnt exist in Maya 2012...
        fieldSetMapNormal = pm.textFieldGrp(
            changeCommand=lambda *args: mapNormalUpdateOptVar(5),
            columnWidth2=[col1, (col2+col3)],
            enable=visState,
            label="UV set name: ",
            parent=colSetMapNormal,
            text=pm.optionVar["mapNormalSetOptVar"],
        )
    else:
        fieldSetMapNormal = pm.textFieldGrp(
            changeCommand=lambda *args: mapNormalUpdateOptVar(5),
            columnWidth2=[col1, (col2+col3)],
            enable=visState,
            label="UV set name: ",
            parent=colSetMapNormal,
            text=pm.optionVar["mapNormalSetOptVar"],
            textChangedCommand=lambda *args: mapNormalUpdateOptVar(5),
        )
    sep3MapAuto = pm.separator(
        height=sepSpace,
        horizontal=True,
        parent=colSetMapNormal,
        visible=True,
    )
    
    # Buttons
    btnApplyCloseMapNormal = pm.button(
        command=lambda *args: core.mapping("normal", None, winMapNormal), 
        label="Confirm",
        parent=form1MapNormal,
    )
    btnApplyMapNormal = pm.button(
        command=lambda *args: core.mapping("normal"), 
        label="Apply",
        parent=form1MapNormal,
    )
    btnResetMapNormal = pm.button( 
        command=lambda *args: mapNormalReset(),
        label="Reset", 
        parent=form1MapNormal,  
    )
    btnCloseMapNormal = pm.button( 
        command=lambda *args: pm.deleteUI( winMapNormal ),
        label="Close", 
        parent=form1MapNormal,  
    )
    
    # Layout frames
    pm.formLayout(
        form2MapNormal, edit=True, 
        attachForm=[
            (frameMainMapNormal, "top", 0), 
            (frameMainMapNormal, "left", 0),
            (frameMainMapNormal, "right", 0), 
            
            (frameMSMapNormal, "left", 0),
            (frameMSMapNormal, "right", 0), 
            
            (frameSetMapNormal, "left", 0),
            (frameSetMapNormal, "right", 0), 
        ], 
        attachControl=[ 
            (frameMSMapNormal, "top", 10, frameMainMapNormal), 
            
            (frameSetMapNormal, "top", 10, frameMSMapNormal), 
        ],
        attachNone=[
            (frameMSMapNormal, "bottom"),    
            
            (frameSetMapNormal, "bottom"),    
        ],
    )

    # Layout main frame
    pm.formLayout(
        form1MapNormal, edit=True, 
        attachForm=[
            (scrollMapNormal, "top", 0),
            (scrollMapNormal, "left", 0),
            (scrollMapNormal, "right", 0),
    
            (btnApplyCloseMapNormal, "left", 5),         
            (btnApplyCloseMapNormal, "bottom", 5),         
            (btnApplyMapNormal, "bottom", 5),
            (btnResetMapNormal, "bottom", 5),
            (btnCloseMapNormal, "right", 5),         
            (btnCloseMapNormal, "bottom", 5),
        ],
        attachControl=[ 
            (scrollMapNormal, "bottom", 0, btnApplyCloseMapNormal), 
        ],
        attachPosition=[
            (btnApplyCloseMapNormal, "right", 3, 25),                   
            (btnApplyMapNormal, "left", 2, 25),                   
            (btnApplyMapNormal, "right", 3, 50),     
            (btnResetMapNormal, "right", 3, 75),                   
            (btnResetMapNormal, "left", 2, 50),     
            (btnCloseMapNormal, "left", 2, 75),       
        ],
        attachNone=[
            (btnApplyCloseMapNormal, "top"),    
            (btnApplyMapNormal, "top"),    
            (btnResetMapNormal, "top"),    
            (btnCloseMapNormal, "top"),      
        ],
    )
    
    # Display the window
    pm.showWindow( window )  
    
    
# UI for changing the spherical mapping options 
def mapSphericalUI():

    # Vars
    col1 = 170
    col2 = 110
    col3 = 150
    sepSpace = 5
    visState = False
    winWidth = 460
    
    
    ## Internal methods
    
    # Reset UI
    def mapSphericalReset():
        
        # Update controls and optVars
        slider1MapSpherical.setValue(180)
        pm.optionVar["mapSphericalSweep1OptVar"] = 180
        
        slider2MapSpherical.setValue(90)
        pm.optionVar["mapSphericalSweep2OptVar"] = 90
        
        cBox1MSMapSpherical.setValue1(True)
        pm.optionVar["mapSphericalMS1BoxOptVar"] = True
        
        cBox2MSMapSpherical.setValue1(True)
        pm.optionVar["mapSphericalMS2BoxOptVar"] = True
        
        cBoxSetMapSpherical.setValue1(False)
        fieldSetMapSpherical.setEnable(False)
        pm.optionVar["mapSphericalSetBoxOptVar"] = False
        
        fieldSetMapSpherical.setText("uvSet1")
        pm.optionVar["mapSphericalSetOptVar"] = "uvSet1"        
        
    
    # Update optVar
    def mapSphericalUpdateOptVar(varType):

        if varType == 1:
            pm.optionVar["mapSphericalMS1BoxOptVar"] = cBox1MSMapSpherical.getValue1()
    
        elif varType == 2:
            pm.optionVar["mapSphericalMS2BoxOptVar"] = cBox2MSMapSpherical.getValue1()
    
        if varType == 3:
            pm.optionVar["mapSphericalSetBoxOptVar"] = cBoxSetMapSpherical.getValue1()
            
            # Turn on/off UI controls
            if pm.optionVar["mapSphericalSetBoxOptVar"] == False:
                fieldSetMapSpherical.setEnable(False)
            else:
                fieldSetMapSpherical.setEnable(True)
    
        elif varType == 4:
            pm.optionVar["mapSphericalSetOptVar"] = fieldSetMapSpherical.getText()
            
        elif varType == 5:
            pm.optionVar["mapSphericalSweep1OptVar"] = slider1MapSpherical.getValue()
            
        elif varType == 6:
            pm.optionVar["mapSphericalSweep2OptVar"] = slider2MapSpherical.getValue()
        
            
    ## Create UI
    
    # Check for window duplicate
    if pm.window( winMapSpherical, exists=True ):
        pm.deleteUI( winMapSpherical )
       
    # Read UI control optVar - Set visibility state
    if pm.optionVar["mapSphericalSetOptVar"] == True:    
        visState = True
       
    # Window 
    window = pm.window(
        winMapSpherical,
        minimizeButton=True, 
        maximizeButton=True, 
        sizeable=True, 
        title="UV Mapping: Spherical Projection", 
        width=winWidth
    )
        
    # Create layout
    form1MapSpherical = pm.formLayout()
    scrollMapSpherical = pm.scrollLayout( childResizable=True )
    form2MapSpherical = pm.formLayout( parent=scrollMapSpherical )
    
    # Mapping Settings: Frame and column
    frameMainMapSpherical = pm.frameLayout(
        borderVisible=False,
        label="Mapping Settings",
        parent=form2MapSpherical,
    )
    colSetSpherical = pm.columnLayout(
        parent=frameMainMapSpherical
    )
    
    # Mapping Settings: UI elements
    slider1MapSpherical = pm.floatSliderGrp(
        changeCommand=lambda *args: mapSphericalUpdateOptVar(5),
        columnWidth3=[col1, col2, col3],
        field=True,
        fieldMinValue=0.00,
        fieldMaxValue=360.00,
        label="Projection Sweep (H): ",
        minValue=0.00,
        maxValue=360.00,
        parent=colSetSpherical,
        precision=2,
        step=0.1,
        value=pm.optionVar["mapSphericalSweep1OptVar"], 
    )
    slider2MapSpherical = pm.floatSliderGrp(
        changeCommand=lambda *args: mapSphericalUpdateOptVar(6),
        columnWidth3=[col1, col2, col3],
        field=True,
        fieldMinValue=0.00,
        fieldMaxValue=180.00,
        label="Projection Sweep (V): ",
        minValue=0.00,
        maxValue=180.00,
        parent=colSetSpherical,
        precision=2,
        step=0.1,
        value=pm.optionVar["mapSphericalSweep2OptVar"], 
    )
    cBox1MSMapSpherical = pm.checkBoxGrp(
        changeCommand=lambda *args: mapSphericalUpdateOptVar(1),
        columnWidth2=[col1, col2],
        label="",
        label1="Insert projection before deformers",
        parent=colSetSpherical,
        value1=pm.optionVar["mapSphericalMS1BoxOptVar"],
    )
    cBox2MSMapSpherical = pm.checkBoxGrp(
        changeCommand=lambda *args: mapSphericalUpdateOptVar(2),
        columnWidth2=[col1, col2],
        label="",
        label1="Show projection manipulator(s)",
        parent=colSetSpherical,
        value1=pm.optionVar["mapSphericalMS2BoxOptVar"],
    )    
    sep1MapSpherical = pm.separator(
        height=sepSpace,
        horizontal=True,
        parent=colSetSpherical,
        visible=True,
    )
    
    # UV Set: Frame and column
    frameSetMapSpherical = pm.frameLayout(
        borderStyle="out",
        label="UV Set",
        parent=form2MapSpherical
    )
    colSetMapSpherical = pm.columnLayout(
        parent=frameSetMapSpherical
    )
    
    # UV Set: UI elements
    cBoxSetMapSpherical = pm.checkBoxGrp(
        changeCommand=lambda *args: mapSphericalUpdateOptVar(3),
        columnWidth2=[col1, col2],
        label="",
        label1="Create new UV set",
        parent=colSetMapSpherical,
        value1=pm.optionVar["mapSphericalSetBoxOptVar"],
    )
    version = pm.about(version=True)
    if version.startswith("2012"): # Because the textChangedCommand didnt exist in Maya 2012...
        fieldSetMapSpherical = pm.textFieldGrp(
            changeCommand=lambda *args: mapSphericalUpdateOptVar(4),
            columnWidth2=[col1, (col2+col3)],
            enable=visState,
            label="UV set name: ",
            parent=colSetMapSpherical,
            text=pm.optionVar["mapSphericalSetOptVar"],
        )
    else:
        fieldSetMapSpherical = pm.textFieldGrp(
            changeCommand=lambda *args: mapSphericalUpdateOptVar(4),
            columnWidth2=[col1, (col2+col3)],
            enable=visState,
            label="UV set name: ",
            parent=colSetMapSpherical,
            text=pm.optionVar["mapSphericalSetOptVar"],
            textChangedCommand=lambda *args: mapSphericalUpdateOptVar(4),
        )
    sep2MapSpherical = pm.separator(
        height=sepSpace,
        horizontal=True,
        parent=colSetMapSpherical,
        visible=True,
    )
    
    # Buttons
    btnApplyCloseMapSpherical = pm.button(
        command=lambda *args: core.mapping("sphere", None, winMapSpherical), 
        label="Confirm",
        parent=form1MapSpherical,
    )
    btnApplyMapSpherical = pm.button(
        command=lambda *args: core.mapping("sphere"), 
        label="Apply",
        parent=form1MapSpherical,
    )
    btnResetMapSpherical = pm.button( 
        command=lambda *args: mapSphericalReset(),
        label="Reset", 
        parent=form1MapSpherical,  
    )
    btnCloseMapSpherical = pm.button( 
        command=lambda *args: pm.deleteUI( winMapSpherical ),
        label="Close", 
        parent=form1MapSpherical,  
    )
    
    # Layout frames
    pm.formLayout(
        form2MapSpherical, edit=True, 
        attachForm=[
            (frameMainMapSpherical, "top", 0), 
            (frameMainMapSpherical, "left", 0),
            (frameMainMapSpherical, "right", 0), 
            
            (frameSetMapSpherical, "left", 0),
            (frameSetMapSpherical, "right", 0), 
        ], 
        attachControl=[ 
            (frameSetMapSpherical, "top", 10, frameMainMapSpherical), 
        ],
        attachNone=[
            (frameSetMapSpherical, "bottom"),    
        ],
    )

    # Layout main frame
    pm.formLayout(
        form1MapSpherical, edit=True, 
        attachForm=[
            (scrollMapSpherical, "top", 0),
            (scrollMapSpherical, "left", 0),
            (scrollMapSpherical, "right", 0),
    
            (btnApplyCloseMapSpherical, "left", 5),         
            (btnApplyCloseMapSpherical, "bottom", 5),         
            (btnApplyMapSpherical, "bottom", 5),
            (btnResetMapSpherical, "bottom", 5),
            (btnCloseMapSpherical, "right", 5),         
            (btnCloseMapSpherical, "bottom", 5),
        ],
        attachControl=[ 
            (scrollMapSpherical, "bottom", 0, btnApplyCloseMapSpherical), 
        ],
        attachPosition=[
            (btnApplyCloseMapSpherical, "right", 3, 25),                   
            (btnApplyMapSpherical, "left", 2, 25),                   
            (btnApplyMapSpherical, "right", 3, 50),     
            (btnResetMapSpherical, "right", 3, 75),                   
            (btnResetMapSpherical, "left", 2, 50),     
            (btnCloseMapSpherical, "left", 2, 75),       
        ],
        attachNone=[
            (btnApplyCloseMapSpherical, "top"),    
            (btnApplyMapSpherical, "top"),    
            (btnResetMapSpherical, "top"),    
            (btnCloseMapSpherical, "top"),      
        ],
    )
    
    # Display the window
    pm.showWindow( window )  
    
    
# UI for changing the planar mapping options 
def mapPlanarUI(axis):

    # Vars    
    col1 = 170
    col2 = 110
    col3 = 150
    sepSpace = 5
    visState1 = False
    visState2 = False
    winWidth = 460
    
    # Overwrite optVar
    if axis == "x":
        pm.optionVar["mapPlanarMS2RadGrpOptVar"] = 1    
    elif axis == "y":
        pm.optionVar["mapPlanarMS2RadGrpOptVar"] = 2    
    elif axis == "z":
        pm.optionVar["mapPlanarMS2RadGrpOptVar"] = 3
    elif axis == "cam":
        pm.optionVar["mapPlanarMS2RadGrpOptVar"] = 4    
    
    
    ## Internal methods
    
    # Switch projection method
    def mapPlanarSwitch():
    
        if radGrpMethodMapPlanar.getSelect() == 1:
            frameMSMapPlanar.setVisible(True)
            frameSetMapPlanar.setVisible(True)
            textQuickMapPlanar.setVisible(False)
        
        elif radGrpMethodMapPlanar.getSelect() == 2:
            frameMSMapPlanar.setVisible(False)
            frameSetMapPlanar.setVisible(False)
            textQuickMapPlanar.setVisible(True)
            
        # Save optVar
        pm.optionVar["mapPlanarMethodOptVar"] = radGrpMethodMapPlanar.getSelect()
        
        
    # Reset UI
    def mapPlanarReset():

        # Update controls and optVars
        radGrpMethodMapPlanar.setSelect(1)
        pm.optionVar["mapPlanarMethodOptVar"] = 1 
        
        radGrp1MSMapPlanar.setSelect(2)
        pm.optionVar["mapPlanarMS1RadGrpOptVar"] = 2
        
        radGrp2MSMapPlanar.setSelect(1)
        radGrp2MSMapPlanar.setEnable(True)
        pm.optionVar["mapPlanarMS2RadGrpOptVar"] = 1
        
        cBox1MSMapPlanar.setValue1(False)
        pm.optionVar["mapPlanarMS1BoxOptVar"] = False 
        
        cBox2MSMapPlanar.setValue1(True)
        pm.optionVar["mapPlanarMS2BoxOptVar"] = True
        
        cBox3MSMapNormal.setValue1(True)
        pm.optionVar["mapPlanarMS3BoxOptVar"] = True
        
        cBoxSetMapPlanar.setValue1(False)
        pm.optionVar["mapPlanarSetBoxOptVar"] = False
        
        fieldSetMapPlanar.setText("uvSet1")
        fieldSetMapPlanar.setEnable(False)
        pm.optionVar["mapPlanarSetOptVar"] = "uvSet1"
        
        # Hide inactive
        mapPlanarSwitch()

        
    # Update optVar
    def mapPlanarUpdateOptVar(varType):
        
        if varType == 1:
            pm.optionVar["mapPlanarMS1RadGrpOptVar"] = radGrp1MSMapPlanar.getSelect()
            
            # Turn on/off UI controls
            if pm.optionVar["mapPlanarMS1RadGrpOptVar"] == 1:
                radGrp2MSMapPlanar.setEnable(False)
            else:
                radGrp2MSMapPlanar.setEnable(True)
            
        elif varType == 2:
            pm.optionVar["mapPlanarMS2RadGrpOptVar"] = radGrp2MSMapPlanar.getSelect()
            
        elif varType == 3:
            pm.optionVar["mapPlanarMS1BoxOptVar"] = cBox1MSMapPlanar.getValue1()
            
        elif varType == 4:
            pm.optionVar["mapPlanarMS2BoxOptVar"] = cBox2MSMapPlanar.getValue1()
            
        elif varType == 5:
            pm.optionVar["mapPlanarSetBoxOptVar"] = cBoxSetMapPlanar.getValue1()
            
            # Turn on/off UI controls
            if pm.optionVar["mapPlanarSetBoxOptVar"] == False:
                fieldSetMapPlanar.setEnable(False)
            else:
                fieldSetMapPlanar.setEnable(True)
            
            
        elif varType == 6:
            pm.optionVar["mapPlanarSetOptVar"] = fieldSetMapPlanar.getText()
            
        elif varType == 7:
            pm.optionVar["mapPlanarMS3BoxOptVar"] = cBox3MSMapNormal.getValue1()
            
            
    ## Create UI
    
    # Check for window duplicate
    if pm.window( winMapPlanar, exists=True ):
        pm.deleteUI( winMapPlanar )
        
    # Read UI control optVars - Set visibility states
    if pm.optionVar["mapPlanarMS1RadGrpOptVar"] == 2:    
        visState1 = True
        
    if pm.optionVar["mapPlanarSetBoxOptVar"] == True:    
        visState2 = True
        
    # Window 
    window = pm.window(
        winMapPlanar,
        minimizeButton=True, 
        maximizeButton=True, 
        sizeable=True, 
        title="UV Mapping: Planar Projection", 
        width=winWidth
    )
        
    # Create layouts
    form1MapPlanar = pm.formLayout()
    scrollMapPlanar = pm.scrollLayout( childResizable=True )
    form2MapPlanar = pm.formLayout( parent=scrollMapPlanar )
    
    frameMainMapPlanar = pm.frameLayout(
        borderVisible=False,
        collapsable=False, 
        label="Projection Options",
        parent=form2MapPlanar
    )
    
    # Method radioBtnGrp
    radGrpMethodMapPlanar = pm.radioButtonGrp(
        changeCommand=lambda *args: mapPlanarSwitch(),
        columnWidth2=[col1, col2],
        label="Method: ",
        labelArray2=["Custom", "Quick"],
        numberOfRadioButtons=2,
        parent=frameMainMapPlanar,
        select=pm.optionVar["mapPlanarMethodOptVar"],
        vertical=True,
    )
    
    ## Custom
    # Mapping Settings: Frame and column
    frameMSMapPlanar = pm.frameLayout(
        borderStyle="out",
        label="Mapping Settings",
        parent=form2MapPlanar
    )
    colMSMapPlanar = pm.columnLayout(
        parent=frameMSMapPlanar
    )
    
    # Mapping Settings: UI elements
    radGrp1MSMapPlanar = pm.radioButtonGrp(
        changeCommand=lambda *args: mapPlanarUpdateOptVar(1),
        columnWidth2=[col1, col2],
        label1="Best plane",
        label2="Bounding box",
        label="Fit projection to: ",
        numberOfRadioButtons=2,
        parent=colMSMapPlanar,
        select=pm.optionVar["mapPlanarMS1RadGrpOptVar"],
        vertical=True,
    )
    sep1MapPlanar = pm.separator(
        height=sepSpace,
        horizontal=True,
        parent=colMSMapPlanar,
        visible=True,
    )
    radGrp2MSMapPlanar = pm.radioButtonGrp(
        changeCommand=lambda *args: mapPlanarUpdateOptVar(2),
        columnWidth2=[col1, col2],
        enable=visState1,
        label1="X axis",
        label2="Y axis",
        label3="Z axis",
        label4="Camera",
        label="Projection from: ",
        numberOfRadioButtons=4,
        parent=colMSMapPlanar,
        select=pm.optionVar["mapPlanarMS2RadGrpOptVar"],
        vertical=True,
    )
    sep2MapPlanar = pm.separator(
        height=sepSpace,
        horizontal=True,
        parent=colMSMapPlanar,
        visible=True,
    )
    cBox1MSMapPlanar = pm.checkBoxGrp(
        changeCommand=lambda *args: mapPlanarUpdateOptVar(3),
        columnWidth2=[col1, col2],
        label="",
        label1="Keep width/height ratio",
        parent=colMSMapPlanar,
        value1=pm.optionVar["mapPlanarMS1BoxOptVar"],
    )
    cBox2MSMapPlanar = pm.checkBoxGrp(
        changeCommand=lambda *args: mapPlanarUpdateOptVar(4),
        columnWidth2=[col1, col2],
        label="",
        label1="Insert projection before deformers",
        parent=colMSMapPlanar,
        value1=pm.optionVar["mapPlanarMS2BoxOptVar"],
    )
    cBox3MSMapNormal = pm.checkBoxGrp(
        changeCommand=lambda *args: mapPlanarUpdateOptVar(7),
        columnWidth2=[col1, col2],
        label="",
        label1="Show projection manipulator(s)",
        parent=colMSMapPlanar,
        value1=pm.optionVar["mapPlanarMS3BoxOptVar"],
    )
    sep3MapPlanar = pm.separator(
        height=sepSpace,
        horizontal=True,
        parent=colMSMapPlanar,
        visible=True,
    )
    
    # UV Set: Frame and column
    frameSetMapPlanar = pm.frameLayout(
        borderStyle="out",
        label="UV Set",
        parent=form2MapPlanar
    )
    colSetMapPlanar = pm.columnLayout(
        parent=frameSetMapPlanar
    )
    
    # UV Set: UI elements
    cBoxSetMapPlanar = pm.checkBoxGrp(
        changeCommand=lambda *args: mapPlanarUpdateOptVar(5),
        columnWidth2=[col1, col2],
        label="",
        label1="Create new UV set",
        parent=colSetMapPlanar,
        value1=pm.optionVar["mapPlanarSetBoxOptVar"],
    )
    version = pm.about(version=True)
    if version.startswith("2012"): # Because the textChangedCommand didnt exist in Maya 2012...
        fieldSetMapPlanar = pm.textFieldGrp(
            changeCommand=lambda *args: mapPlanarUpdateOptVar(6),
            columnWidth2=[col1, (col2+col3)],
            enable=visState2,
            label="UV set name: ",
            parent=colSetMapPlanar,
            text=pm.optionVar["mapPlanarSetOptVar"],
        )
    else:
        fieldSetMapPlanar = pm.textFieldGrp(
            changeCommand=lambda *args: mapPlanarUpdateOptVar(6),
            columnWidth2=[col1, (col2+col3)],
            enable=visState2,
            label="UV set name: ",
            parent=colSetMapPlanar,
            text=pm.optionVar["mapPlanarSetOptVar"],
            textChangedCommand=lambda *args: mapPlanarUpdateOptVar(6),
        )
    sep4MapPlanar = pm.separator(
        height=sepSpace,
        horizontal=True,
        parent=colSetMapPlanar,
        visible=True,
    )
    
    
    ## Quick
    textQuickMapPlanar = pm.text(
        label="No options here - Things just get done!!",
        parent=form2MapPlanar
    )
    
    # Buttons
    btnApplyCloseMapPlanar = pm.button(
        command=lambda *args: core.mapping("plane", None, winMapPlanar), 
        label="Confirm",
        parent=form1MapPlanar,
    )
    btnApplyMapPlanar = pm.button(
        command=lambda *args: core.mapping("plane"), 
        label="Apply",
        parent=form1MapPlanar,
    )
    btnResetMapPlanar = pm.button( 
        command=lambda *args: mapPlanarReset(),
        label="Reset", 
        parent=form1MapPlanar,  
    )
    btnCloseMapPlanar = pm.button( 
        command=lambda *args: pm.deleteUI( winMapPlanar ),
        label="Close", 
        parent=form1MapPlanar,  
    )

    # Layout frames
    pm.formLayout(
        form2MapPlanar, edit=True, 
        attachForm=[
        
            (frameMainMapPlanar, "top", 0), 
            (frameMainMapPlanar, "left", 0), 
            (frameMainMapPlanar, "right", 0),  
        
            (frameMSMapPlanar, "left", 0), 
            (frameMSMapPlanar, "right", 0), 

            (frameSetMapPlanar, "left", 0), 
            (frameSetMapPlanar, "right", 0), 
            
            (textQuickMapPlanar, "left", 0), 
            (textQuickMapPlanar, "right", 0), 
        ], 
        attachControl=[            
            (frameMSMapPlanar, "top", 10, frameMainMapPlanar), 

            (frameSetMapPlanar, "top", 10, frameMSMapPlanar),
            
            (textQuickMapPlanar, "top", 0, frameSetMapPlanar), 
        ],
        attachNone=[
            (frameMSMapPlanar, "bottom"),
            
            (frameSetMapPlanar, "bottom"), 
            
            (textQuickMapPlanar, "bottom"), 
        ]
    )

    # Layout main frame
    pm.formLayout(
        form1MapPlanar, edit=True, 
        attachForm=[
            (scrollMapPlanar, "top", 0),
            (scrollMapPlanar, "left", 0),
            (scrollMapPlanar, "right", 0),

            (btnApplyCloseMapPlanar, "left", 5),         
            (btnApplyCloseMapPlanar, "bottom", 5),         
            (btnApplyMapPlanar, "bottom", 5),                
            (btnResetMapPlanar, "bottom", 5),         
            (btnCloseMapPlanar, "right", 5),         
            (btnCloseMapPlanar, "bottom", 5),     
        ], 
        attachControl=[
            (scrollMapPlanar, "bottom", 0, btnApplyCloseMapPlanar), 
        ],
        attachPosition=[
            (btnApplyCloseMapPlanar, "right", 3, 25),                   
            (btnApplyMapPlanar, "left", 2, 25),                   
            (btnApplyMapPlanar, "right", 3, 50),                   
            (btnResetMapPlanar, "right", 3, 75),                   
            (btnResetMapPlanar, "left", 2, 50),                   
            (btnCloseMapPlanar, "left", 2, 75),       
        ],
        attachNone=[
            (btnApplyCloseMapPlanar, "top"),    
            (btnApplyMapPlanar, "top"),    
            (btnResetMapPlanar, "top"),    
            (btnCloseMapPlanar, "top"),    
        ],
    )
    
    # Hide inactive
    mapPlanarSwitch()
    
    # Display the window
    pm.showWindow( window )  
    
    
# UI for changing the match UVs -tolerance value
def matchTolUI():

    # Vars
    btnRow = 274
    winHeight = 133
    winWidth = 300
    sliderMatchTol = "NSUV_matchTolSlider"

    # Internal method for updating field and optVar
    def update():    
        pm.optionVar["matchTolOptVar"] = sliderMatchTol.getValue()

    # Check for window duplicate
    if pm.window( winMatchTol, exists=True ):
        pm.deleteUI( winMatchTol )

    # Window
    window = pm.window(
        winMatchTol,
        height=winHeight, 
        minimizeButton=False, 
        maximizeButton=False, 
        resizeToFitChildren=True, 
        sizeable=True, 
        title="Match UVs", 
        width=winWidth 
    )
    
    # Layouts
    frameMatchTol = pm.frameLayout(
        borderStyle="etchedIn", 
        collapsable=False, 
        collapse=False, 
        height=winHeight, 
        label="Options", 
        marginHeight=10, 
        marginWidth=10, 
        width=winWidth 
    )
    colMatchTol = pm.columnLayout(
        adjustableColumn=False, 
        columnAlign="left", 
        rowSpacing=6
    )
    textMatchTol = pm.text(
        label="A higher value increases the likelyhood that UVs match to \ntheir neighboring UVs.")
        
    # Slider
    sliderMatchTol = pm.floatSliderGrp( 
        changeCommand=lambda *args: update(),
        columnAlign=[1, "left"], 
        columnWidth3=[115, 45, 110],
        field=True, 
        fieldMaxValue=0.05,    
        fieldMinValue=0.001,     
        label="Tolerance (UV units)", 
        maxValue=0.05, 
        minValue=0.001,     
        precision=3, 
        sliderStep=0.01, 
        value=pm.optionVar["matchTolOptVar"] 
    )
    
    # Buttons
    rowMatchTol = pm.rowLayout(
        columnAttach2=["both", "both"], 
        numberOfColumns=2, 
        parent=frameMatchTol     
    )
    btnOkMatchTol = pm.button(
        command=lambda *args: core.matchUVs(), 
        label="Match UVs",
        parent=rowMatchTol,
        width=(btnRow/2)
    )
    btnCancelMatchTol = pm.button( 
        command=lambda *args: pm.deleteUI(window),
        label="Close", 
        parent=rowMatchTol,  
        width=(btnRow/2) 
    )
    
    # Display the window
    pm.showWindow( window ) 
 

# UI for changing the match UVs -tolerance value
def orientShellsUI():

    # Vars
    btnRow=274
    radGrpOrient = "NSUV_orientShellsRadGrp"    

    # Internal method for updating optVar
    def update():
        pm.optionVar["orientShellsOptVar"] = radGrpOrient.getSelect()-1
    

    # Check for window duplicate
    if pm.window( winOrient, exists=True ):
        pm.deleteUI( winOrient )

    # Window
    window = pm.window(
        winOrient,
        height=150, 
        minimizeButton=False, 
        maximizeButton=False, 
        resizeToFitChildren=True, 
        sizeable=False, 
        title="Orient Shells", 
        width=300 
    )
    
    # Layouts
    frameOrient = pm.frameLayout(
        borderStyle="etchedIn", 
        collapsable=False, 
        collapse=False, 
        height=150, 
        label="Options", 
        marginHeight=10, 
        marginWidth=10, 
        width=300 
    )
    colOrient = pm.columnLayout(
        adjustableColumn=False, 
        columnAlign="left", 
        rowSpacing=6
    )
    
    # Radio collection and radio buttons
    radGrpOrient = pm.radioButtonGrp(
        changeCommand=lambda *args: update(radGrpOrient), 
        columnAlign=[1, "right"],
        columnWidth2=[80, 195],
        label1="Poor (Very fast)",
        label2="Default (Fast)",
        label3="Exceptional (Slow)",
        label4="Flawless (Very slow)",
        label="Accuracy: ", 
        numberOfRadioButtons=4,
        parent=colOrient,
        select=pm.optionVar["orientShellsOptVar"],
        vertical=True,
    )
    
    # Buttons
    rowOrient = pm.rowLayout(
        columnAttach2=["both", "both"], 
        numberOfColumns=2, 
        parent=frameOrient    
    )
    btnOkStrUVs = pm.button(
        command=lambda *args: core.orientShells(), 
        label="Orient Shells",
        parent=rowOrient,
        width=(btnRow/2)
    )
    btnCancelStrUVs = pm.button( 
        command=lambda *args: pm.deleteUI(window),
        label="Close", 
        parent=rowOrient,  
        width=(btnRow/2) 
    )
    
    # Display the window
    pm.showWindow( window ) 
 

# UI for randomizing shells
def randomizeUI():
 
    # Vars
    btnRow = 274
    cBox1Width = 40
    cBox2Width = 70
    rowHeight = 34
    textWidth = 90
    winHeight = 310
    winWidth = 300
    
    cBoxR1Rnd = None
    cBoxR2Rnd = None
    cBoxS1Rnd = None
    cBoxS2Rnd = None
    cBoxT1Rnd = None
    cBoxT2Rnd = None
    fSliderGrpRRnd = None
    fSliderGrpSRnd = None
    fSliderGrpTRnd = None
    
    ## Internal methods
    
    # Update optVar
    def randUpdateOptVar(varType):     
            
        if varType == 1:
            pm.optionVar["randTBox1OptVar"] = cBoxT1Rnd.getValue()
            
        elif varType == 2:
            pm.optionVar["randTBox2OptVar"] = cBoxT2Rnd.getValue()
            
        if varType == 3:
            pm.optionVar["randTOptVar"] = fSliderGrpTRnd.getValue()

        elif varType == 4:
            pm.optionVar["randRBox1OptVar"] = cBoxR1Rnd.getValue()
            
        elif varType == 5:
            pm.optionVar["randRBox2OptVar"] = cBoxR2Rnd.getValue()
            
        elif varType == 6:
            pm.optionVar["randROptVar"] = fSliderGrpRRnd.getValue()

        elif varType == 7:
            pm.optionVar["randSBox1OptVar"] = cBoxS1Rnd.getValue()
            
        elif varType == 8:
            pm.optionVar["randSBox2OptVar"] = cBoxS2Rnd.getValue()
            
        elif varType == 9:
            pm.optionVar["randSOptVar"] = fSliderGrpSRnd.getValue()
        
        else:
            print("Incorrect values specified for the UI.randomizeUI.randUpdateOptVar() -method")
    
    
    ## Create UI
    
    # Check for window duplicate
    if pm.window( winRandom, exists=True ):
        pm.deleteUI( winRandom )
    
    # Main window
    window = pm.window(
        winRandom,
        height=winHeight,
        maximizeButton=False,
        minimizeButton=False,
        resizeToFitChildren=True,
        sizeable=False,
        title="Randomize Shells", 
        width=winWidth,
    )
    
    # Main frame
    frameRnd = pm.frameLayout(
        borderStyle="etchedIn", 
        collapsable=False, 
        collapse=False, 
        height=135, 
        label="Options", 
        marginHeight=10, 
        marginWidth=10, 
        width=winWidth,
    )
    
    # The translate row - and it's components
    rowTRnd = pm.rowLayout(
        columnAttach3=["both", "both", "both"],
        numberOfColumns=3, 
        parent=frameRnd,
        width=btnRow
    )
    textTRnd = pm.text(
        align="right", 
        label="Translate: ", 
        parent=rowTRnd, 
        width=textWidth, 
    )
    cBoxT1Rnd = pm.checkBox(
        changeCommand=lambda *args: randUpdateOptVar(1), 
        label="U", 
        parent=rowTRnd, 
        value=pm.optionVar["randTBox1OptVar"],
        width=cBox1Width 
    )
    cBoxT2Rnd = pm.checkBox(
        changeCommand=lambda *args: randUpdateOptVar(2), 
        label="V", 
        parent=rowTRnd, 
        value=pm.optionVar["randTBox2OptVar"],
        width=cBox2Width 
    )
    fSliderGrpTRnd = pm.floatSliderGrp(
        changeCommand=lambda *args: randUpdateOptVar(3), 
        columnAlign=[1, "right"], 
        columnWidth3=[textWidth, 40, 100],
        field=True, 
        fieldMinValue=0.01, 
        fieldMaxValue=1.0, 
        label="Units (max): ", 
        maxValue=1.0, 
        minValue=0.01, 
        parent=frameRnd, 
        precision=3, 
        sliderStep=0.01, 
        value=pm.optionVar["randTOptVar"]
    )
    sep1Rnd = pm.separator(
        height=2,  
        parent=frameRnd, 
        style="in",
        width=btnRow
    )
    
    # The rotate row - and it's components
    rowRRnd = pm.rowLayout(
        columnAttach3=["both", "both", "both"],
        numberOfColumns=3, 
        parent=frameRnd,
        width=btnRow
    )
    textRRnd = pm.text(
        align="right", 
        label="Rotate: ", 
        parent=rowRRnd, 
        width=textWidth, 
    )
    cBoxR1Rnd = pm.checkBox(
        changeCommand=lambda *args: randUpdateOptVar(4), 
        label="CW", 
        parent=rowRRnd, 
        value=pm.optionVar["randRBox1OptVar"],
        width=cBox1Width 
    )
    cBoxR2Rnd = pm.checkBox(
        changeCommand=lambda *args: randUpdateOptVar(5), 
        label="CCW", 
        parent=rowRRnd, 
        value=pm.optionVar["randRBox2OptVar"],
        width=cBox2Width 
    )
    fSliderGrpRRnd = pm.floatSliderGrp(
        changeCommand=lambda *args: randUpdateOptVar(6), 
        columnAlign=[1, "right"], 
        columnWidth3=[textWidth, 40, 100],
        field=True, 
        fieldMinValue=1, 
        fieldMaxValue=180, 
        label="Degrees (max): ", 
        maxValue=180, 
        minValue=1, 
        parent=frameRnd, 
        value=pm.optionVar["randROptVar"]
    )
    sep2Rnd = pm.separator(
        height=2,  
        parent=frameRnd, 
        style="in",
        width=btnRow
    )

    # The scale row - and it's components
    rowSRnd = pm.rowLayout(
        columnAttach3=["both", "both", "both"],
        numberOfColumns=3, 
        parent=frameRnd,
        width=btnRow
    )
    textSRnd = pm.text(
        align="right", 
        label="Scale: ", 
        parent=rowSRnd, 
        width=textWidth, 
    )
    cBoxS1Rnd = pm.checkBox(
        changeCommand=lambda *args: randUpdateOptVar(7), 
        label="Up", 
        parent=rowSRnd, 
        value=pm.optionVar["randSBox1OptVar"],
        width=cBox1Width 
    )
    cBoxS2Rnd = pm.checkBox(
        changeCommand=lambda *args: randUpdateOptVar(8), 
        label="Down", 
        parent=rowSRnd, 
        value=pm.optionVar["randSBox2OptVar"],
        width=cBox2Width 
    )
    fSliderGrpSRnd = pm.floatSliderGrp(
        changeCommand=lambda *args: randUpdateOptVar(9), 
        columnAlign=[1, "right"], 
        columnWidth3=[textWidth, 40, 100],
        field=True, 
        fieldMinValue=1, 
        fieldMaxValue=180, 
        label="Percent (max): ", 
        maxValue=100, 
        minValue=0.1, 
        parent=frameRnd, 
        precision=1,
        sliderStep=1,
        value=pm.optionVar["randSOptVar"]
    )
    sep3Rnd = pm.separator(
        height=2,  
        parent=frameRnd, 
        style="in",
        width=btnRow
    ) 
    
    # Buttons
    rowBtnRnd = pm.rowLayout(
        columnAttach2=["both", "both"],  
        numberOfColumns=2, 
        parent=frameRnd
    )
    btnGoRnd = pm.button(
        command=lambda *args: core.randomizeUVs(), 
        label="Randomize", 
        parent=rowBtnRnd,
        width=(btnRow/2) 
    )
    buttonCloseRnd = pm.button(
        command=lambda *args: pm.deleteUI(winRandom), 
        label="Close", 
        parent=rowBtnRnd,
        width=(btnRow/2) 
    )    
    
    pm.showWindow( window ) # Display the window

    
# Options UI for the unfold feature
def relaxUI():

    # Vars
    col1 = 170
    col2 = 70
    col3 = 130
    visState1 = False
    sepSpace = 5
    
    radGrpRelax = None
    sliderItrRelax = None
    sliderAngleRelax = None
    sliderPowerRelax = None
    cBoxBorderRelax = None
    cBoxFlipsRelax = None
    menuRoomRelax = None
    sliderRoomRelax = None
    cBoxPin1Relax = None
    cBoxPin2Relax = None
    radGrpPinRelax = None
    radGrpWeightRelax = None
    sliderMaxItrRelax = None
    
    
    ## Internal methods
    
    # Switch relax method
    def relaxSwitch():

        # Unfold3D plugin loaded
        if pm.pluginInfo("Unfold3D", loaded=True, query=True) == True: 
        
            # Unfold3D. Hide Legacy frames
            if radGrpRelax.getSelect() == 1:    
                frameOptiRelax.setVisible(True)
                frameRoomRelax.setVisible(True)
                framePinningRelax.setVisible(False)
                frameOtherRelax.setVisible(False)
                textQuickRelax.setVisible(False)
                
            # Legacy. Hide Unfold3D frames
            elif radGrpRelax.getSelect() == 2 :  
                frameOptiRelax.setVisible(False)
                frameRoomRelax.setVisible(False)
                framePinningRelax.setVisible(True)
                frameOtherRelax.setVisible(True)
                textQuickRelax.setVisible(False)

            else: # Quick. Hide all frames   
                frameOptiRelax.setVisible(False)
                frameRoomRelax.setVisible(False)
                framePinningRelax.setVisible(False)
                frameOtherRelax.setVisible(False)
                textQuickRelax.setVisible(True)
                
        else: # Plugin not loaded   

            if radGrpRelax.getSelect() == 1:    
                frameOptiRelax.setVisible(False)
                frameRoomRelax.setVisible(False)
                framePinningRelax.setVisible(True)
                frameOtherRelax.setVisible(True)
                textQuickRelax.setVisible(False)
                
            else:
                frameOptiRelax.setVisible(False)
                frameRoomRelax.setVisible(False)
                framePinningRelax.setVisible(False)
                frameOtherRelax.setVisible(False)
                textQuickRelax.setVisible(True)        
     
        # Save optVar
        pm.optionVar["relaxMethodOptVar"] = radGrpRelax.getSelect()
    
    
    # Reset UI
    def relaxUIReset():

        # Update controls and optVars
        radGrpRelax.setSelect(1)
        pm.optionVar["relaxMethodOptVar"] = 1
        
        sliderItrRelax.setValue(1)
        pm.optionVar["relaxItrOptVar"] = 1
        
        sliderAngleRelax.setValue(1.0)
        pm.optionVar["relaxAngleOptVar"] = 1.0
        
        sliderPowerRelax.setValue(100)
        pm.optionVar["relaxPowerOptVar"] = 100
        
        cBoxBorderRelax.setValue1(True)
        pm.optionVar["relaxBorderOptVar"] = True
        
        cBoxFlipsRelax.setValue1(True)
        pm.optionVar["relaxFlipsOptVar"] = True 
        
        menuRoomRelax.setValue(1024)
        pm.optionVar["relaxSizeOptVar"] = 1024
        
        sliderRoomRelax.setValue(2)
        pm.optionVar["relaxRoomOptVar"] = 2
        
        cBoxPin1Relax.setValue1(True)
        pm.optionVar["relaxPinBorderOptVar"] = True
        
        cBoxPin2Relax.setValue1(False)
        pm.optionVar["relaxPinOptVar"] = False
        
        radGrpPinRelax.setSelect(1)
        pm.optionVar["relaxPinTypeOptVar"] = 1
        
        radGrpWeightRelax.setSelect(1)
        pm.optionVar["relaxEdgeOptVar"] = 1
        
        sliderMaxItrRelax.setValue(5)
        pm.optionVar["relaxMaxItrOptVar"] = 5
        
        # Hide inactive
        relaxSwitch()
        
    # Update optVar
    def relaxUpdateOptVar(varType, control=None, control2=None):
        
        if varType == 1:
            pm.optionVar["relaxItrOptVar"] = sliderItrRelax.getValue()
            
        elif varType == 2:
            pm.optionVar["relaxAngleOptVar"] = sliderAngleRelax.getValue()

        elif varType == 3:
            pm.optionVar["relaxPowerOptVar"] = sliderPowerRelax.getValue()
            
        elif varType == 4:
            pm.optionVar["relaxBorderOptVar"] = cBoxBorderRelax.getValue1()
            
        elif varType == 5:
            pm.optionVar["relaxFlipsOptVar"] = cBoxFlipsRelax.getValue1()
            
        elif varType == 6:
            pm.optionVar["relaxSizeOptVar"] = menuRoomRelax.getValue()

        elif varType == 7:
            pm.optionVar["relaxRoomOptVar"] = sliderRoomRelax.getValue()
            
        elif varType == 8:    
            pm.optionVar["relaxPinBorderOptVar"] = cBoxPin1Relax.getValue1()
            
        elif varType == 9:
        
            # Manipulate the other controls, then set optVar        
            if control.getValue1() == True:
                control2.setEnable(True) # Show 
            else:
                control2.setEnable(False) # Hide
            pm.optionVar["relaxPinOptVar"] = control.getValue1()
            
        elif varType == 10:    
            pm.optionVar["relaxPinTypeOptVar"] = radGrpPinRelax.getSelect()
            
        elif varType == 11:
            pm.optionVar["relaxEdgeOptVar"] = radGrpRelax.getSelect()
            
        elif varType == 12:
            pm.optionVar["relaxMaxItrOptVar"] = sliderMaxItrRelax.getValue()
            
        else: # Incorrect varType
            pm.error("Incorrect varType sent to UI.unfoldUI.relaxUpdateOptVar()")
    
    
    ## Create UI
    
    # Check for window duplicate
    if pm.window( winRelax, exists=True ):
        pm.deleteUI( winRelax )
    
    # Read UI control optVars - Het visibility states
    if pm.optionVar["relaxPinOptVar"] > 0:
        visState1 = True
        
    # Window
    window = pm.window(
        winRelax,
        minimizeButton=True, 
        maximizeButton=True, 
        sizeable=True, 
        title="Relax UVs", 
        width=500
    )
    
    # Create layouts
    form1Relax = pm.formLayout()
    scrollRelax = pm.scrollLayout( childResizable=True )
    form2Relax = pm.formLayout( parent=scrollRelax )
    
    frameMainRelax = pm.frameLayout(
        borderVisible=False,
        collapsable=False, 
        label="Relax Options",
        parent=form2Relax
    )
    
    # Method radioBtnGrp
    if pm.pluginInfo("Unfold3D", loaded=True, query=True) == True: # Unfold3D plugin -check
        radGrpRelax = pm.radioButtonGrp(
            changeCommand=lambda *args: relaxSwitch(),
            columnWidth2=[col1, col2+50],
            numberOfRadioButtons=3,
            label="Method: ",
            labelArray3=["Unfold3D (Optimize)", "Legacy", "Quick"],
            vertical=True,
            parent=frameMainRelax,
            select=pm.optionVar["relaxMethodOptVar"],
        )
    else: # Unfold3D not loaded
        radGrpRelax = pm.radioButtonGrp(
            changeCommand=lambda *args: relaxSwitch(),
            columnWidth2=[col1, col2],
            numberOfRadioButtons=2,
            label="Method: ",
            labelArray2=["Legacy", "Quick"],
            vertical=True,
            parent=frameMainRelax,
            select=pm.optionVar["relaxMethodOptVar"],
        )
    
    ## Unfold 3D
    # Unfold 3D: Optimize frame and column
    frameOptiRelax = pm.frameLayout(
        borderStyle="out",
        label="Optimize Options",
        parent=form2Relax
    )
    colSolver1Relax = pm.columnLayout(
        parent=frameOptiRelax
    )
    
    # Unfold3D: Solver elements
    sliderItrRelax = pm.intSliderGrp(
        adjustableColumn=3,
        columnAttach3=["both", "both", "both"],
        columnWidth3=[col1, col2, col3],
        changeCommand=lambda *args: relaxUpdateOptVar(1),
        field=True,
        fieldMaxValue=999,
        fieldMinValue=0,
        label="Iterations: ",
        maxValue=10,
        minValue=0,
        parent=colSolver1Relax, 
        value=pm.optionVar["relaxItrOptVar"], 
    )
    sliderAngleRelax = pm.floatSliderGrp(
        adjustableColumn=3,
        columnAttach3=["both", "both", "both"],
        columnWidth3=[col1, col2, col3],
        changeCommand=lambda *args: relaxUpdateOptVar(2),
        field=True,
        fieldMaxValue=1.0,
        fieldMinValue=0.0,
        label="Surfangle: ",
        maxValue=1.0,
        minValue=0.0,
        parent=colSolver1Relax, 
        value=pm.optionVar["relaxAngleOptVar"], 
    ) 
    sliderPowerRelax = pm.intSliderGrp(
        adjustableColumn=3,
        columnAttach3=["both", "both", "both"],
        columnWidth3=[col1, col2, col3],
        changeCommand=lambda *args: relaxUpdateOptVar(3),
        field=True,
        fieldMaxValue=100,
        fieldMinValue=1,
        label="Power: ",
        maxValue=100,
        minValue=1,
        parent=colSolver1Relax, 
        value=pm.optionVar["relaxPowerOptVar"], 
    ) 
    cBoxBorderRelax = pm.checkBoxGrp(
        changeCommand=lambda *args: relaxUpdateOptVar(4),
        columnWidth2=[col1, col2],
        label="",
        label1="Prevent self border intersections",
        parent=colSolver1Relax,
        value1=pm.optionVar["relaxBorderOptVar"],
    )
    cBoxFlipsRelax = pm.checkBoxGrp(
        changeCommand=lambda *args: relaxUpdateOptVar(5),
        columnWidth2=[col1, col2],
        label="",
        label1="Prevent triangle flips",
        parent=colSolver1Relax,
        value1=pm.optionVar["relaxFlipsOptVar"],
    )
    sep1Relax = pm.separator(
        height=sepSpace,
        horizontal=True,
        parent=colSolver1Relax,
        visible=True,
    )
    
    # Unfold3D: Room Space frame and column
    frameRoomRelax = pm.frameLayout(
        borderStyle="out",
        label="Room Space Options",
        parent=form2Relax
    )    
    colRoomRelax = pm.columnLayout(
        parent=frameRoomRelax,
    )
    
    # Unfold3D: Room Space elements
    menuRoomRelax = pm.optionMenuGrp(
        changeCommand=lambda *args: relaxUpdateOptVar(6),
        columnWidth2=[col1, col2],
        label="Map size (Pixels): ",
        parent=colRoomRelax,
    )    
    
    item8192 = pm.menuItem( label="8192")
    item4096 = pm.menuItem( label="4096")
    item2048 = pm.menuItem( label="2048")
    item1024 = pm.menuItem( label="1024")
    item512 = pm.menuItem( label="512")
    item256 = pm.menuItem( label="256")
    item128 = pm.menuItem( label="128")
    item64 = pm.menuItem( label="64")
    item32 = pm.menuItem( label="32")
    
    menuRoomRelax.setValue(pm.optionVar["relaxSizeOptVar"])
    
    sliderRoomRelax = pm.intSliderGrp(
        changeCommand=lambda *args: relaxUpdateOptVar(7),
        columnWidth3=[col1, col2, col3],
        field=True,
        fieldMaxValue=999,
        fieldMinValue=0,
        label="Room space (Pixels): ",
        maxValue=10,
        minValue=0,
        parent=colRoomRelax,
        value=pm.optionVar["relaxRoomOptVar"],
    )
    sep2Relax = pm.separator(
        height=sepSpace,
        horizontal=True,
        parent=colRoomRelax,
        visible=True,
    )
    
    ## Legacy    
    # Legacy: Pinning frame and column
    framePinningRelax = pm.frameLayout(
        borderStyle="out",
        label="Pinning",
        parent=form2Relax, 
    )
    colPinningRelax = pm.columnLayout(
        parent=framePinningRelax, 
    )
    
    # Legacy: Pinning elements
    cBoxPin1Relax = pm.checkBoxGrp(
        changeCommand=lambda *args: relaxUpdateOptVar(8),
        columnWidth2=[col1, col2],
        label="",
        label1="Pin UV Shell Border",
        parent=colPinningRelax, 
        value1=pm.optionVar["relaxPinBorderOptVar"],
    )
    cBoxPin2Relax = pm.checkBoxGrp(
        changeCommand=lambda *args: relaxUpdateOptVar(9, cBoxPin2Relax, radGrpPinRelax),    
        columnWidth2=[col1, col2],
        label="",
        label1="Pin UVs",
        parent=colPinningRelax,
        value1=pm.optionVar["relaxPinOptVar"],
    )
    radGrpPinRelax = pm.radioButtonGrp(
        changeCommand=lambda *args: relaxUpdateOptVar(10),
        columnWidth2=[( col1 + 15 ), ( col2 + 40 )],
        enable=visState1,
        label1="Pin selected UVs",
        label2="Pin unselected UVs",
        label="",
        numberOfRadioButtons=2,
        parent=colPinningRelax,
        select=pm.optionVar["relaxPinTypeOptVar"],
        vertical=True,
    )
    sep3Relax = pm.separator(
        height=sepSpace,
        horizontal=True,
        parent=colPinningRelax,
        visible=True,
    )
    
    # Legacy: Other frame and column
    frameOtherRelax = pm.frameLayout(
        borderStyle="out",
        label="Other Options",
        parent=form2Relax, 
    )
    colOtherRelax = pm.columnLayout(
        parent=frameOtherRelax, 
    )
    
    # Legacy: Other elements
    radGrpWeightRelax = pm.radioButtonGrp(
        changeCommand = lambda *args: relaxUpdateOptVar(11),
        columnWidth2=[col1, col2+20],
        numberOfRadioButtons = 2,
        label = "Edge weights: ",
        labelArray2 = ["Uniform", "World space"],
        vertical = True,
        parent=colOtherRelax,
        select=pm.optionVar["relaxEdgeOptVar"],
    )    
    sliderMaxItrRelax = pm.intSliderGrp(
        changeCommand=lambda *args: relaxUpdateOptVar(12),
        columnWidth3=[col1, col2, col3],
        field=True,
        fieldMaxValue=10000,
        fieldMinValue=1,
        label="Max iterations: ",
        maxValue=10000,
        minValue=1,
        parent=colOtherRelax, 
        value=pm.optionVar["relaxMaxItrOptVar"], 
    )
    sep4Relax = pm.separator(
        height=sepSpace,
        horizontal=True,
        parent=colOtherRelax,
        visible=True,
    )

    ## Quick
    textQuickRelax = pm.text(
        label="No options here - Things just get done!!",
        parent=form2Relax
    )
    
    # Buttons
    btnApplyCloseRelax = pm.button(
        command=lambda *args: core.relaxUVs(winRelax), 
        label="Confirm",
        parent=form1Relax,
    )
    btnApplyRelax = pm.button(
        command=lambda *args: core.relaxUVs(), 
        label="Apply",
        parent=form1Relax,
    )
    btnResetRelax = pm.button( 
        # command=lambda *args: ???,
        label="Reset", 
        parent=form1Relax,  
    )
    btnCloseRelax = pm.button( 
        command=lambda *args: pm.deleteUI( winRelax ),
        label="Close", 
        parent=form1Relax,  
    )
    
    # Layout frames
    pm.formLayout(
        form2Relax, edit=True, 
        attachForm=[
        
            (frameMainRelax, "top", 0), 
            (frameMainRelax, "left", 0), 
            (frameMainRelax, "right", 0),  
        
            (frameOptiRelax, "left", 0), 
            (frameOptiRelax, "right", 0), 

            (frameRoomRelax, "left", 0), 
            (frameRoomRelax, "right", 0), 
            
            (framePinningRelax, "left", 0), 
            (framePinningRelax, "right", 0), 
            
            (frameOtherRelax, "left", 0), 
            (frameOtherRelax, "right", 0), 
            
            (textQuickRelax, "left", 0), 
            (textQuickRelax, "right", 0), 
        ], 
        attachControl=[        
            (frameOptiRelax, "top", 10, frameMainRelax), 
            
            (frameRoomRelax, "top", 10, frameOptiRelax), 
            
            (framePinningRelax, "top", 0, frameRoomRelax), 
            
            (frameOtherRelax, "top", 10, framePinningRelax),
            
            (textQuickRelax, "top", 0, frameOtherRelax), 
        ],
        attachNone=[
            (frameOptiRelax, "bottom"),
            
            (frameRoomRelax, "bottom"), 
            
            (framePinningRelax, "bottom"), 
            
            (frameOtherRelax, "bottom"), 
            
            (textQuickRelax, "bottom"), 
        ]
    )
    
    # Layout main frame
    pm.formLayout(
        form1Relax, edit=True, 
        attachForm=[
            (scrollRelax, "top", 0),
            (scrollRelax, "left", 0),
            (scrollRelax, "right", 0),

            (btnApplyCloseRelax, "left", 5),         
            (btnApplyCloseRelax, "bottom", 5),         
            (btnApplyRelax, "bottom", 5),                
            (btnResetRelax, "bottom", 5),         
            (btnCloseRelax, "right", 5),         
            (btnCloseRelax, "bottom", 5),     
        ], 
        attachControl=[
            (scrollRelax, "bottom", 0, btnApplyCloseRelax), 
        ],
        attachPosition=[
            (btnApplyCloseRelax, "right", 3, 25),                   
            (btnApplyRelax, "left", 2, 25),                   
            (btnApplyRelax, "right", 3, 50),                   
            (btnResetRelax, "right", 3, 75),                   
            (btnResetRelax, "left", 2, 50),                   
            (btnCloseRelax, "left", 2, 75),       
        ],
        attachNone=[
            (btnApplyCloseRelax, "top"),    
            (btnApplyRelax, "top"),    
            (btnResetRelax, "top"),    
            (btnCloseRelax, "top"),    
        ],
    )
    
    # Hide inactive
    relaxSwitch()

    # Display the window
    pm.showWindow( window )

    
# UI for renaming a UV set
def renameSetUI(scrollList):

    # Check for window duplicate
    if pm.window( winRenameUVSet, exists=True ):
        pm.deleteUI( winRenameUVSet )
  
    # Get selected UV set
    selectedSet = scrollList.getSelectItem()
  
    # Main window
    window = pm.window(
        winRenameUVSet,
        maximizeButton=False, 
        sizeable=False,
        title="Rename UV Set", 
        width=240
    )
  
    # Create column layout
    colRenameUVSet = pm.columnLayout(
        columnAttach=["left", 10],
        rowSpacing=10
    )

    # Invisible separator
    sepRenameUVSet = pm.separator(
        height=1,
        isObscured=True,
    )

    # Create label and input field
    textRenameUVSet = pm.text(
        align="center", 
        label="Rename UV Set to..", 
        width=230
    )
    fieldRenameUVSet = pm.textField(
        alwaysInvokeEnterCommandOnReturn=True,
        annotation="Enter new name",
        enterCommand=lambda *args: core.renameSet(scrollList, fieldRenameUVSet, winRenameUVSet),
        text=str(selectedSet[0]),
        width=220
    )

    # Create row layout
    rowRenameUVSet = pm.rowLayout(numberOfColumns=2)
        
    # Create buttons
    btnOkRenameUVSet = pm.button(
        command=lambda *args: core.renameSet(scrollList, fieldRenameUVSet, winRenameUVSet),
        label="Rename", 
        width=108
    )
    btnCancelRenameUVSet = pm.button(
        command=lambda *args: pm.deleteUI(winRenameUVSet),
        label="Close",
        width=108
    )
    
    pm.showWindow( window ) # Display the window
 
    
# UI for changing working units
def setWorkingUnitsUI():

    btnRow = 276
    winWidth = 300

    # Check for window duplicate
    if pm.window( winTDwUnits, exists=True ):
        pm.deleteUI( winTDwUnits )
    
    # Window
    window = pm.window(
        winTDwUnits,
        height=140, 
        minimizeButton=False, 
        maximizeButton=False, 
        resizeToFitChildren=True, 
        sizeable=False, 
        title="Set working units", 
        width=winWidth 
    )
    
    # Frame
    frameTD = pm.frameLayout(
        borderStyle="etchedIn", 
        collapsable=False, 
        collapse=False, 
        height=140, 
        label="Options", 
        marginHeight=10, 
        marginWidth=10, 
        width=winWidth 
    )
    
    # Column
    colTD = pm.columnLayout(
        adjustableColumn=False, 
        columnAlign="left", 
        rowSpacing=6
    )
    
    # Label text
    textTD = pm.text(
        label=("NOTE: Changing the working units HERE is the same as \n"
           "changing it under the Maya preferences! Additionally, the\n"
           "viewport grid will be affected by a new setting!"
        )
    )
    
    # Units menu
    menuTD = pm.optionMenuGrp(
        columnWidth=[1, 40],
        label="Linear: "
    )      
    pm.menuItem(label="millimeter")
    pm.menuItem(label="centimeter")
    pm.menuItem(label="meter")
    pm.menuItem(label="kilometer")
    pm.menuItem(label="inch")
    pm.menuItem(label="foot")
    pm.menuItem(label="yard") 
    pm.menuItem(label="mile")

    # Get current linear unit and update the optionMenu
    menuVal = pm.currentUnit(query=True, linear=True)    
    
    if menuVal == "mm":
        menuVal = "millimeter"
    elif menuVal == "cm":
        menuVal = "centimeter"
    elif menuVal == "m":
        menuVal = "meter"
    elif menuVal == "km":
        menuVal = "kilometer"
    elif menuVal == "in":
        menuVal = "inch"
    elif menuVal == "ft":
        menuVal = "foot"
    elif menuVal == "yd":
        menuVal = "yard"
    elif menuVal == "mi":
        menuVal = "mile"

    menuTD.setValue(menuVal)
    
    
    # Buttons
    rowTD = pm.rowLayout(
        columnAttach2=["both", "both"], 
        numberOfColumns=2, 
        parent=frameTD    
    )
    btnOkTD = pm.button(
        command=lambda *args: core.setUnits(menuTD, winTDwUnits), 
        label="Okay",
        parent=rowTD,
        width=(btnRow/2)
    )
    btnCancelTD = pm.button(
        command=lambda *args: pm.deleteUI(window), 
        label="Cancel",
        parent=rowTD,
        width=(btnRow/2)
    )
    
    # Display the window
    pm.showWindow( window ) 
    

# UI for the UV snapshot window    
def snapshotUI():

    # Vars
    btn1SS = None
    btn2SS = None
    btn3SS = None
    btn4SS = None
    btn5SS = None
    btn6SS = None
    menuFormatSS = None
    menuRangeSS = None
    rad1SS = None
    rad2SS = None
    rad3SS = None
    rad4SS = None
    rad5SS = None
    rad6SS = None
    menuLabel1 = "Normal (0 to 1)"
    menuLabel2 = "User-specified"
    ssSpacing = 120 


    ## Internal methods
    
    # File path browser -method
    def ssBrowse():
        
        cleanPath = ""
        
        # Run file browser
        unicodePath = pm.fileDialog2(
            caption="Set output path",
            dialogStyle=1,
            fileMode=0,
            startingDirectory=pm.optionVar["shotUVpathOptVar"]
        )

        # Because fileDialog2 returns such a stupid data type, fix it!
        if unicodePath != None and unicodePath != "":
            cleanPath = str(unicodePath[0])

        # Update the file path -control
        if cleanPath != None and cleanPath != "":
            fieldSS.setText( cleanPath )
            
            # Update the optVar
            pm.optionVar["shotUVpathOptVar"] = cleanPath
            
    # Range toggle -method
    def ssRangeToggle():
        
        # Read menu value and update optVar
        range = pm.optionVar["shotUVrangeOptVar"] = menuRangeSS.getSelect()
        
        # Turn on/off UI parts
        if range != 1:
            btn1SS.setEnable(True)
            btn2SS.setEnable(True)
            btn3SS.setEnable(True)
            btn4SS.setEnable(True)
            btn5SS.setEnable(True)
            btn6SS.setEnable(True)
            rad1SS.setEnable(True)
            rad2SS.setEnable(True)
            rad3SS.setEnable(True)
            rad4SS.setEnable(True)
            rad5SS.setEnable(True)
            rad6SS.setEnable(True)
        
        else:
            btn1SS.setEnable(False)
            btn2SS.setEnable(False)
            btn3SS.setEnable(False)
            btn4SS.setEnable(False)
            btn5SS.setEnable(False)
            btn6SS.setEnable(False)
            rad1SS.setEnable(False)
            rad2SS.setEnable(False)
            rad3SS.setEnable(False)
            rad4SS.setEnable(False)
            rad5SS.setEnable(False)
            rad6SS.setEnable(False)   

    # "Reset to default" -method
    def ssReset():
        
        # Get root dir, set as default
        path = pm.workspace(query=True, rootDirectory=True) + "images/outUV"
        pm.optionVar["shotUVpathOptVar"] = path
        
        # Switch front slashes for back slashes in the path optVar if OS = windows
        if pm.about(ntOS=True) == True:
            pm.optionVar["shotUVpathOptVar"] = path = path.replace("/", "\\")
        
        # Reset UI controls to defaults
        cBoxAliasSS.setValue1(1)
        fieldSS.setText(path)
        menuFormatSS.setSelect(1)
        sliderColorSS.setRgbValue([1.0, 1.0, 1.0])
        sliderXSS.setValue(1024)
        sliderYSS.setValue(1024)
        menuRangeSS.setValue(menuLabel1)
        
        # And reset the associated optVars
        pm.optionVar["shotUVaaOptVar"] = 0
        pm.optionVar["shotUVratioOptVar"] = 1
        pm.optionVar["shotUVformatOptVar"] = 1
        pm.optionVar["shotUVxSizeOptVar"] = 1024
        pm.optionVar["shotUVySizeOptVar"] = 1024
        pm.optionVar["shotUVcolorOptVar"] = [ 1.0, 1.0, 1.0 ]
        pm.optionVar["shotUVrangeOptVar"] = 1
        
        # Toggle visibility
        ssRangeToggle()
        
    # Update optVar
    def ssUpdateOptVar(varType, control=None, radBtn=None):

        if varType == 1:
            pm.optionVar["shotUVpathOptVar"] = fieldSS.getText()
                
        elif varType == 2:
            
            # Query slider, round to power of two
            newVal = sliderXSS.getValue()
            newVal = core.powerOfTwo(newVal)
            sliderXSS.setValue(newVal)   
            
            pm.optionVar["shotUVxSizeOptVar"] = sliderXSS.getValue()

        elif varType == 3:
            
            # Query slider, round to power of two
            newVal = sliderYSS.getValue()
            newVal = core.powerOfTwo(newVal)
            sliderYSS.setValue(newVal)   
               
            pm.optionVar["shotUVySizeOptVar"] = sliderYSS.getValue()
            
        elif varType == 4:
            pm.optionVar["shotUVcolorOptVar"] = sliderColorSS.getRgbValue()
         
        elif varType == 5:
            pm.optionVar["shotUVaaOptVar"] = cBoxAliasSS.getValue1()
            
        elif varType == 6:
            pm.optionVar["shotUVformatOptVar"] = menuFormatSS.getValue()
            
        elif varType == 8:
            if radBtn == 1:
                pm.optionVar["shotUVtypeOptVar"] = 1
            elif radBtn == 2:
                pm.optionVar["shotUVtypeOptVar"] = 2
            elif radBtn == 3:
                pm.optionVar["shotUVtypeOptVar"] = 3
            elif radBtn == 4:
                pm.optionVar["shotUVtypeOptVar"] = 4
            elif radBtn == 5:
                pm.optionVar["shotUVtypeOptVar"] = 5
            elif radBtn == 6:
                pm.optionVar["shotUVtypeOptVar"] = 6
            else:
                pm.error("Incorrect radBtn sent to ss")
                
            control.setSelect()
                
        else: # Incorrect varType
            pm.error("Incorrect varType sent to UI.snapshotUI.ssUpdateOptVar()")

    
    ## Create UI

    # Check for window duplicate
    if pm.window( winSS, exists=True ):
        pm.deleteUI( winSS )
    
    # Create window
    window = pm.window(
        winSS,
        height=400,
        maximizeButton=True,
        minimizeButton=True,
        sizeable=True,
        title="Snapshot UVs", 
        width=500
    )
    
    # Create layouts
    form1SS = pm.formLayout()
    scrollSS = pm.scrollLayout( childResizable=True )
    form2SS = pm.formLayout( parent=scrollSS )
    
    frame1SS = pm.frameLayout(
        borderStyle="out", 
        collapsable=False, 
        label="Settings"  
    )
    col1SS = pm.columnLayout(parent=frame1SS)
    
    # File path field
    fieldSS = pm.textFieldButtonGrp(
        buttonCommand=lambda *args: ssBrowse(),
        buttonLabel="Browse...", 
        changeCommand=lambda *args: ssUpdateOptVar(1),
        columnWidth=( [1, ssSpacing], [3, 65] ),
        label="Path / File name: ",
        text=pm.optionVar["shotUVpathOptVar"],
    )
    
    # Size sliders
    sliderXSS = pm.intSliderGrp(
        changeCommand=lambda *args: ssUpdateOptVar(2),
        columnWidth=[1, ssSpacing],
        dragCommand=lambda *args: ssUpdateOptVar(2),
        field=True, 
        fieldStep=32,
        label="Size X (px): ", 
        max=8192, 
        min=32, 
        sliderStep=32,
        step=32,
        value=pm.optionVar["shotUVxSizeOptVar"]
    )    
    sliderYSS = pm.intSliderGrp(
        changeCommand=lambda *args: ssUpdateOptVar(3),
        columnWidth=[1, ssSpacing],
        dragCommand=lambda *args: ssUpdateOptVar(3),
        field=True, 
        fieldStep=32,
        label="Size Y (px): ", 
        max=8192, 
        min=32, 
        sliderStep=32,
        step=32,
        value=pm.optionVar["shotUVySizeOptVar"]
    )
    
    # Edge color slider
    redV, greenV, blueV = pm.optionVar["shotUVcolorOptVar"]    
    sliderColorSS = pm.colorSliderGrp(
        changeCommand=lambda *args: ssUpdateOptVar(4),
        columnWidth=[1, ssSpacing], 
        label="Edge color: ", 
        rgbValue=[redV, greenV, blueV]
    )
    
    # Anti-aliasing checkbox
    cBoxAliasSS = pm.checkBoxGrp( 
        changeCommand=lambda *args: ssUpdateOptVar(5),
        columnWidth=[1, ssSpacing], 
        label1="Anti-alias lines", 
        label="", 
        value1=pm.optionVar["shotUVaaOptVar"]
    )
    
    # File format menu
    menuFormatSS = pm.optionMenuGrp(
        changeCommand=lambda *args: ssUpdateOptVar(6),
        columnWidth=[1, ssSpacing],
        label="Image format: ",
        parent=col1SS
    )    
    
    # File format list on MacOS
    if pm.about(macOS=True):
        pm.menuItem(label="Maya IFF")
        pm.menuItem(label="JPEG")
        pm.menuItem(label="MacPaint")
        pm.menuItem(label="PSD")
        pm.menuItem(label="PNG")
        pm.menuItem(label="Quickdraw")
        pm.menuItem(label="Quickdraw Image")
        pm.menuItem(label="SGI")
        pm.menuItem(label="TGA")
        pm.menuItem(label="TIFF")
        pm.menuItem(label="BMP")
    
    else: # Windows
    
        # Query available image formats
        imfList = pm.imfPlugins(query=True)
    
        # Maya IFF is always available
        pm.menuItem(label="Maya IFF")
    
        # Create menuItem objects for all items in list
        counter = 0
        while counter < len(imfList):
        
            # Get keyword
            imfKey = pm.imfPlugins( imfList[counter], query=True, key=True )

            # Check for support types and make sure imfKey ain't "maya"
            wSupport = pm.imfPlugins(imfKey, query=True, writeSupport=True)
            mfSupport = pm.imfPlugins(imfKey, query=True, multiFrameSupport=True)
        
            if wSupport == True and mfSupport == False and imfKey != "maya":
                pm.menuItem( label=imfList[counter] ) # Create menuItem

            # Up the counter for the while loop
            counter += 1
    
        pm.setParent('..')
        
    # Select menuItem
    menuFormatSS.setValue(pm.optionVar["shotUVformatOptVar"])
    formatIndex = menuFormatSS.getSelect()
    
    # Layouts for the range section
    frame2SS = pm.frameLayout(
        borderStyle="out", 
        collapsable=True,
        label="UV Range Options",
        parent=form2SS
    )
    col2SS = pm.columnLayout(parent=frame2SS)
    
    # Range toggle menu
    if pm.optionVar["shotUVrangeOptVar"] == 1:
        rangeSelVar = str(menuLabel1)
    else:
        rangeSelVar = str(menuLabel2)
        
    menuRangeSS = pm.optionMenuGrp(
        changeCommand=lambda *args: ssRangeToggle(),
        columnWidth=[1, ssSpacing], 
        label="Range: ",
        parent=col2SS
    )
    
    # Create the menu items, select menuItem
    pm.menuItem(label=menuLabel1)
    pm.menuItem(label=menuLabel2)
    
    # formLayout for the range section
    form3SS = pm.formLayout(parent=col2SS)
    
    # Range buttons
    btn1SS = pm.iconTextButton( 
        annotation="Lying rectangle",
        command=lambda *args: ssUpdateOptVar(8, rad1SS, 1),
        height=iconSizeBig,
        image="NS_uvRange_a.bmp",
        label="Lying rectangle",
        width=iconSizeBig
    )
    btn2SS = pm.iconTextButton( 
        annotation="Standing rectangle",
        command=lambda *args: ssUpdateOptVar(8, rad2SS, 2),
        height=iconSizeBig,
        image="NS_uvRange_b.bmp",
        label="Standing rectangle",
        width=iconSizeBig
    )
    btn3SS = pm.iconTextButton( 
        annotation="-1 to 1",
        command=lambda *args: ssUpdateOptVar(8, rad3SS, 3),
        height=iconSizeBig,
        image="NS_uvRange_c.bmp",
        label="-1 to 1",
        width=iconSizeBig 
    )
    btn4SS = pm.iconTextButton( 
        annotation="Second quadrant",
        command=lambda *args: ssUpdateOptVar(8, rad4SS, 4),
        height=iconSizeBig,
        image="NS_uvRange_d.bmp",
        label="Second quadrant",
        width=iconSizeBig 
    )
    btn5SS = pm.iconTextButton( 
        annotation="Third quadrant",
        command=lambda *args: ssUpdateOptVar(8, rad5SS, 5),
        height=iconSizeBig,
        image="NS_uvRange_e.bmp",
        label="Third quadrant",
        width=iconSizeBig 
    )
    btn6SS = pm.iconTextButton( 
        annotation="Fourth quadrant",
        command=lambda *args: ssUpdateOptVar(8, rad6SS, 6),
        height=iconSizeBig,
        image="NS_uvRange_f.bmp",
        label="Fourth quadrant",
        width=iconSizeBig 
    )
    
    # Radio collection and radio buttons
    radColSS = pm.radioCollection(
        parent=form3SS
    )
    rad1SS = pm.radioButton(label="A", changeCommand=lambda *args: ssUpdateOptVar(8, rad1SS, 1))
    rad2SS = pm.radioButton(label="B", changeCommand=lambda *args: ssUpdateOptVar(8, rad2SS, 2))
    rad3SS = pm.radioButton(label="C", changeCommand=lambda *args: ssUpdateOptVar(8, rad3SS, 3))
    rad4SS = pm.radioButton(label="D", changeCommand=lambda *args: ssUpdateOptVar(8, rad4SS, 4))
    rad5SS = pm.radioButton(label="E", changeCommand=lambda *args: ssUpdateOptVar(8, rad5SS, 5))
    rad6SS = pm.radioButton(label="F", changeCommand=lambda *args: ssUpdateOptVar(8, rad6SS, 6))

    # Edit the radio collection and select item
    if pm.optionVar["shotUVtypeOptVar"] == 1:
        radColSS.setSelect(rad1SS)
    elif pm.optionVar["shotUVtypeOptVar"] == 2:
        radColSS.setSelect(rad2SS)
    elif pm.optionVar["shotUVtypeOptVar"] == 3:
        radColSS.setSelect(rad3SS)
    elif pm.optionVar["shotUVtypeOptVar"] == 4:
        radColSS.setSelect(rad4SS)
    elif pm.optionVar["shotUVtypeOptVar"] == 5:
        radColSS.setSelect(rad5SS)
    elif pm.optionVar["shotUVtypeOptVar"] == 6:
        radColSS.setSelect(rad6SS)

    # Layout elements in the range formLayout
    pm.formLayout(
        form3SS, edit=True, 
        attachForm=[
            (btn1SS, "top", 5), 
            (btn1SS, "left", ssSpacing),         
            (rad1SS, "top", 20), 
        
            (btn2SS, "top", 5), 
            (rad2SS, "top", 20), 
        
            (btn3SS, "top", 5), 
            (rad3SS, "top", 20), 
        
            (btn4SS, "left", ssSpacing), 
        ], 
        attachControl=[
            (rad1SS, "left", 2, btn1SS), 
        
            (btn2SS, "left", 12, rad1SS), 
            (rad2SS, "left", 2, btn2SS), 
        
            (btn3SS, "left", 12, rad2SS), 
            (rad3SS, "left", 2, btn3SS), 
            
            (btn4SS, "top", 20, btn1SS), 
            (rad4SS, "top", 50, rad1SS), 
            (rad4SS, "left", 2, btn4SS), 
            
            (btn5SS, "top", 20, btn2SS), 
            (btn5SS, "left", 12, rad4SS), 
            (rad5SS, "top", 50, rad2SS), 
            (rad5SS, "left", 2, btn5SS), 
            
            (btn6SS, "top", 20, btn3SS), 
            (btn6SS, "left", 12, rad5SS), 
            (rad6SS, "top", 50, rad3SS), 
            (rad6SS, "left", 2, btn6SS), 
        ]
    )
        
    # Separator
    sep1 = pm.separator(
        horizontal=True,
        style="none"
    )
    
    # Buttons
    btnOkSS = pm.button(  
        command=lambda *args: core.ssTakeShot(winSS),
        label="Ok",
        parent=form1SS
    )
    btnApply = pm.button(
        command=lambda *args: core.ssTakeShot(),
        label="Apply", 
        parent=form1SS
    )
    btnDefaultSS = pm.button(
        command=lambda *args: ssReset(),
        label="Reset", 
        parent=form1SS
    )
    btnCloseSS = pm.button(    
        command=lambda *args: pm.deleteUI(winSS),
        label="Close", 
        parent=form1SS
    )
    
    # Layout section frames
    pm.formLayout(
        form2SS, edit=True, 
        attachForm=[
            (frame1SS, "top", 0), 
            (frame1SS, "right", 0),       
            (frame1SS, "left", 0),
            
            (frame2SS, "right", 0), 
            (frame2SS, "left", 0), 
            (frame2SS, "bottom", 0),         
        ], 
        attachControl=[
            (frame2SS, "top", 10, frame1SS),         
        ], 
        attachNone=[
            (frame1SS, "bottom")            
        ]
    )
    
    # Layout main frame
    pm.formLayout(
        form1SS, edit=True, 
        attachForm=[
            (scrollSS, "top", 0),             
            (scrollSS, "right", 0),         
            (scrollSS, "left", 0), 
        
            (btnOkSS, "left", 5),         
            (btnOkSS, "bottom", 5),         
            (btnApply, "bottom", 5),         
            (btnDefaultSS, "bottom", 5),         
            (btnCloseSS, "right", 5),         
            (btnCloseSS, "bottom", 5),         
        ], 
        attachControl=[
            (scrollSS, "bottom", 5, btnOkSS),                   
        ], 
        attachPosition=[
            (btnOkSS, "right", 3, 25), 
            (btnApply, "right", 3, 50),
            (btnApply, "left", 2, 25),     
            (btnDefaultSS, "right", 3, 75),                                                   
            (btnDefaultSS, "left", 2, 50),                   
            (btnCloseSS, "left", 2, 75),                   
        ], 
        attachNone=[
            (btnOkSS, "top"),    
            (btnDefaultSS, "top"),    
            (btnCloseSS, "top"),    
        ]
    )
  
    # In case a plugin has been unloaded, reducing the number of FF...
    if formatIndex > menuFormatSS.getNumberOfItems():
        
        # ...just pick the file format at the end of the list
        formatIndex = menuFormatSS.getNumberOfItems()
        
    # Edit the file format menu
    menuFormatSS.setSelect(formatIndex)

    # Edit the range menu
    menuRangeSS.setSelect(pm.optionVar["shotUVrangeOptVar"])
    ssRangeToggle() # Toggle visibility
    
    # Display the window
    pm.showWindow( window )
    
    
# UI for changing the straighten UVs options
def strUVsUI():

    btnRow = 274
    winHeight = 200
    winWidth = 300

    ## Internal methods
    
    # Reset UI
    def strUVsReset():    
        pm.optionVar["strUVsAngleOptVar"] = 30
        pm.optionVar["strUVsTypeOptVar"] = 0
        radGrpStrUVs.setSelect(0)    
        sliderStrUVs.setValue(30)
    
    # Update optVar
    def strUVsUpdateOptVar(varType):  
        
        if varType == 0:
            pm.optionVar["strUVsAngleOptVar"] = sliderStrUVs.getValue()-1
        
        elif varType == 1:
            pm.optionVar["strUVsTypeOptVar"] = radGrpStrUVs.getSelect()-1   
            

    ## Create UI

    # Check for window duplicate
    if pm.window( winStrUVs, exists=True ):
        pm.deleteUI( winStrUVs )

    # Window
    window = pm.window(
        winStrUVs,
        height=winHeight, 
        minimizeButton=False, 
        maximizeButton=False, 
        resizeToFitChildren=True, 
        sizeable=False, 
        title="Straighten UVs", 
        width=winWidth 
    )
    
    # Layouts
    frameStrUVs = pm.frameLayout(
        borderStyle="etchedIn", 
        collapsable=False, 
        collapse=False, 
        height=winHeight, 
        label="Options", 
        marginHeight=10, 
        marginWidth=10, 
        width=winWidth 
    )
    colStrUVs = pm.columnLayout(
        adjustableColumn=False, 
        columnAlign="left", 
        rowSpacing=6
    )
    textStrUVs = pm.text(
        label="A higher value results in more aggressive straightening\nof the edge loops in the selection.")
        
    # Slider
    sliderStrUVs = pm.floatSliderGrp( 
        changeCommand=lambda *args: strUVsUpdateOptVar(0),
        columnAlign=[1, "right"], 
        columnWidth3=[90, 55, 126],
        field=True, 
        fieldMaxValue=44.99,    
        fieldMinValue=0.01,     
        label="Angle value: ", 
        maxValue=44.99, 
        minValue=0.01,     
        precision=2, 
        sliderStep=0.01, 
        value=pm.optionVar["strUVsAngleOptVar"]
    )
    
    # Radio collection and radio buttons
    radGrpStrUVs = pm.radioButtonGrp(
        changeCommand=lambda *args: strUVsUpdateOptVar(1), 
        columnAlign=[1, "right"],
        columnWidth2=[90, 185],
        label1="U and V",
        label2="U only",
        label3="V only",
        label="Straighten along: ", 
        numberOfRadioButtons=3,
        parent=colStrUVs,
        select=pm.optionVar["strUVsTypeOptVar"],
        vertical=True,
    )
    
    # Buttons
    rowStrUVs = pm.rowLayout(
        columnAttach3=["both", "both", "both"], 
        numberOfColumns=3, 
        parent=frameStrUVs    
    )
    btnOkStrUVs = pm.button(
        command=lambda *args: core.strUVs(), 
        label="Straighten",
        parent=rowStrUVs,
        width=(btnRow/3)
    )
    btnOkStrUVs = pm.button(
        command=lambda *args: strUVsReset(), 
        label="Reset",
        parent=rowStrUVs,
        width=(btnRow/3)
    )
    btnCancelStrUVs = pm.button( 
        command=lambda *args: pm.deleteUI(window),
        label="Close", 
        parent=rowStrUVs,  
        width=(btnRow/3) 
    )
    
    # Display the window
    pm.showWindow( window ) 
    
    
# Options UI for the unfold feature
def unfoldUI():

    # Vars
    col1 = 170
    col2 = 70
    col3 = 130
    visState1 = False
    visState2 = True
    visState2 = False
    sepSpace = 5
    
    cBoxBorderUnfold = None
    cBoxFlipsUnfold = None
    cBoxHistoryUnfold = None
    cBoxPackUnfold = None
    cBoxPin1Unfold = None
    cBoxPin2Unfold = None
    cBoxRescaleUnfold = None
    fieldAreaUnfold = None
    fieldOptUnfold = None
    fieldWeightUnfold = None
    menuRoomUnfold = None
    radGrpConstUnfold = None
    radGrpPinUnfold = None
    radGrpUnfold = None
    sliderAreaUnfold = None
    sliderItrUnfold = None
    sliderMaxItrUnfold = None
    sliderOptUnfold = None
    sliderRoomUnfold = None
    sliderScaleUnfold = None
    sliderStopUnfold = None
    sliderWeightUnfold = None
    
    
    ## Internal methods
   
    # Switch unfold method
    def unfoldSwitch():

        # Unfold3D plugin loaded
        if pm.pluginInfo("Unfold3D", loaded=True, query=True) == True: 
        
            # Unfold3D. Hide Legacy frames
            if radGrpUnfold.getSelect() == 1:    
                frameSolver1Unfold.setVisible(True)
                frameRoomUnfold.setVisible(True)
                frameSolver2Unfold.setVisible(False)
                framePinningUnfold.setVisible(False)
                frameOtherUnfold.setVisible(False)
                textQuickUnfold.setVisible(False)
        
            # Legacy. Hide Unfold3D frames
            elif radGrpUnfold.getSelect() == 2 :    
                frameSolver1Unfold.setVisible(False)
                frameRoomUnfold.setVisible(False)       
                frameSolver2Unfold.setVisible(True)
                framePinningUnfold.setVisible(True)
                frameOtherUnfold.setVisible(True)
                textQuickUnfold.setVisible(False)

            else: # Quick. Hide all frames    
                frameSolver1Unfold.setVisible(False)
                frameRoomUnfold.setVisible(False)
                frameSolver2Unfold.setVisible(False)
                framePinningUnfold.setVisible(False)
                frameOtherUnfold.setVisible(False)
                textQuickUnfold.setVisible(True)
                
        else: # Plugin not loaded       
            
            if radGrpUnfold.getSelect() == 1:    
                frameSolver1Unfold.setVisible(False)
                frameRoomUnfold.setVisible(False)
                frameSolver2Unfold.setVisible(True)
                framePinningUnfold.setVisible(True)
                frameOtherUnfold.setVisible(True)
                textQuickUnfold.setVisible(False)
                
            else:
                frameSolver1Unfold.setVisible(False)
                frameRoomUnfold.setVisible(False)
                frameSolver2Unfold.setVisible(False)
                framePinningUnfold.setVisible(False)
                frameOtherUnfold.setVisible(False)
                textQuickUnfold.setVisible(True)
        
     
        # Save optVar
        pm.optionVar["unfoldMethodOptVar"] = radGrpUnfold.getSelect()   

    # Reset UI
    def unfoldUIReset():
    
        # Update controls and optVars
        radGrpUnfold.setSelect(1)
        pm.optionVar["unfoldMethodOptVar"] = 1

        sliderItrUnfold.setValue(1)
        pm.optionVar["unfoldItrOptVar"] = 1

        cBoxPackUnfold.setValue1(True)
        pm.optionVar["unfoldPackOptVar"] = True

        cBoxBorderUnfold.setValue1(True)
        pm.optionVar["unfoldBorderOptVar"] = True 

        cBoxFlipsUnfold.setValue1(True)
        pm.optionVar["unfoldFlipsOptVar"] = True    

        menuRoomUnfold.setValue(2048)
        pm.optionVar["unfoldSizeOptVar"] = 2048    

        sliderRoomUnfold.setValue(2)
        pm.optionVar["unfoldRoomOptVar"] = 2    

        fieldWeightUnfold.setValue(0.0000)
        sliderWeightUnfold.setValue(0.0000)
        pm.optionVar["unfoldSolverOptVar"] = 0.0000    

        fieldOptUnfold.setValue(1)
        sliderOptUnfold.setValue(1)
        pm.optionVar["unfoldOtOOptVar"] = 0.5000

        fieldAreaUnfold.setValue(0.0)
        sliderAreaUnfold.setValue(0.0)
        pm.optionVar["unfoldAreaOptVar"] = 0.0    

        cBoxPin1Unfold.setValue1(False)
        pm.optionVar["unfoldPinBorderOptVar"] = False    

        cBoxPin2Unfold.setValue1(True)
        pm.optionVar["unfoldPinOptVar"] = True    

        radGrpPinUnfold.setSelect(1)
        pm.optionVar["unfoldPinTypeOptVar"] = 1    

        radGrpConstUnfold.setSelect(0)
        pm.optionVar["unfoldConstOptVar"] = 0

        sliderMaxItrUnfold.setValue(5000)
        pm.optionVar["unfoldMaxItrOptVar"] = 5000    

        sliderStopUnfold.setValue(0.0010)
        pm.optionVar["unfoldStopOptVar"] = 0.0010    

        cBoxRescaleUnfold.setValue1(False)
        pm.optionVar["unfoldRescaleOptVar"] = False    

        sliderScaleUnfold.setValue(0.0200)
        pm.optionVar["unfoldSFactOptVar"] = 0.0200    

        cBoxHistoryUnfold.setValue1(False)
        pm.optionVar["unfoldHistOptVar"] = False

        # Hide inactive
        unfoldSwitch()

    # Update optVar
    def unfoldUpdateOptVar(varType, control=None, control2=None):
        
        if varType == 1:
            pm.optionVar["unfoldItrOptVar"] = sliderItrUnfold.getValue()
            
        elif varType == 2:
            pm.optionVar["unfoldPackOptVar"] = cBoxPackUnfold.getValue1()

        elif varType == 3:
            pm.optionVar["unfoldBorderOptVar"] = cBoxBorderUnfold.getValue1()
            
        elif varType == 4:
            pm.optionVar["unfoldFlipsOptVar"] = cBoxFlipsUnfold.getValue1()
            
        elif varType == 5:
            pm.optionVar["unfoldSizeOptVar"] = menuRoomUnfold.getValue()
            
        elif varType == 6:
            pm.optionVar["unfoldRoomOptVar"] = sliderRoomUnfold.getValue()
            
        elif varType == 7:
            
            # Manipulate the other controls, then set optVar
            control2.setValue( control.getValue() )
            if control.getValue() == 0.0:
                fieldOptUnfold.setEnable(False) # Hide
                sliderOptUnfold.setEnable(False) # Hide
            else:
                fieldOptUnfold.setEnable(True) # Show
                sliderOptUnfold.setEnable(True) # Show
            pm.optionVar["unfoldSolverOptVar"] = control.getValue()        
            
        elif varType == 8:
        
            # Manipulate the other control, then set optVar
            control2.setValue( control.getValue() )
            pm.optionVar["unfoldOtOOptVar"] = control.getValue()
            
        elif varType == 9:
            pm.optionVar["unfoldPinBorderOptVar"] = cBoxPin1Unfold.getValue1()
            
        elif varType == 10:
        
            # Hide/Show other control, then set optVar
            if control2.getEnable() == True:
                control2.setEnable(False)
            else:    
                control2.setEnable(True)
            pm.optionVar["unfoldPinOptVar"] = control.getValue1()
            
        elif varType == 11:
            pm.optionVar["unfoldPinTypeOptVar"] = radGrpPinUnfold.getSelect()
            
        elif varType == 12:
            pm.optionVar["unfoldConstOptVar"] = radGrpConstUnfold.getSelect()
            
        elif varType == 13:
            pm.optionVar["unfoldMaxItrOptVar"] = sliderMaxItrUnfold.getValue()
            
        elif varType == 14:
            pm.optionVar["unfoldStopOptVar"] = sliderStopUnfold.getValue()
            
        elif varType == 15:
        
            # Hide/Show other control, then set optVar
            if control2.getEnable() == True:
                control2.setEnable(False)
            else:    
                control2.setEnable(True)    
            pm.optionVar["unfoldRescaleOptVar"] = control.getValue1()
            
        elif varType == 16:
            pm.optionVar["unfoldSFactOptVar"] = sliderScaleUnfold.getValue()
            
        elif varType == 17:
            pm.optionVar["unfoldHistOptVar"] = cBoxHistoryUnfold.getValue1()
            
        elif varType == 18:
        
            # Manipulate the other control, then set optVar
            control2.setValue( control.getValue() )
            pm.optionVar["unfoldAreaOptVar"] = control.getValue()
            
        else: # Incorrect varType
            pm.error("Incorrect varType sent to UI.unfoldUI.unfoldUpdateOptVar()")
        
        
    ## Create UI   
        
    # Check for window duplicate
    if pm.window( winUnfold, exists=True ):
        pm.deleteUI( winUnfold )
    
    # Read UI control optVars - Set visibility states
    if pm.optionVar["unfoldSolverOptVar"] > 0:
        visState1 = True
        
    if pm.optionVar["unfoldRescaleOptVar"] == True:
        visState2 = True
        
    # Window
    window = pm.window(
        winUnfold,
        minimizeButton=True, 
        maximizeButton=True, 
        sizeable=True, 
        title="Unfold UVs", 
        width=500
    )
    
    # Create layouts
    form1Unfold = pm.formLayout()
    scrollUnfold = pm.scrollLayout( childResizable=True )
    form2Unfold = pm.formLayout( parent=scrollUnfold )
    
    frameMainUnfold = pm.frameLayout(
        borderVisible=False,
        collapsable=False, 
        label="Unfold Options",
        parent=form2Unfold
    )
    
    # Method radioBtnGrp
    if pm.pluginInfo("Unfold3D", loaded=True, query=True) == True: # Unfold3D plugin -check
        radGrpUnfold = pm.radioButtonGrp(
            changeCommand=lambda *args: unfoldSwitch(),
            columnWidth2=[col1, col2],
            label="Method: ",
            labelArray3=["Unfold3D", "Legacy", "Quick"],
            numberOfRadioButtons=3,
            parent=frameMainUnfold,
            select=pm.optionVar["unfoldMethodOptVar"],
            vertical=True,
        )
    else: # Unfold3D not loaded
        radGrpUnfold = pm.radioButtonGrp(
            changeCommand=lambda *args: unfoldSwitch(),
            columnWidth2=[col1, col2],
            label="Method: ",
            labelArray2=["Legacy", "Quick"],
            numberOfRadioButtons=2,
            parent=frameMainUnfold,
            select=pm.optionVar["unfoldMethodOptVar"],
            vertical=True,
        )
    
    ## Unfold 3D
    # Unfold 3D: Solver frame and column
    frameSolver1Unfold = pm.frameLayout(
        borderStyle="out",
        label="Solver Options",
        parent=form2Unfold
    )
    colSolver1Unfold = pm.columnLayout(
        parent=frameSolver1Unfold
    )
    
    # Unfold3D: Solver elements
    sliderItrUnfold = pm.intSliderGrp(
        adjustableColumn=3,
        columnAttach3=["both", "both", "both"],
        columnWidth3=[col1, col2, col3],
        changeCommand=lambda *args: unfoldUpdateOptVar(1),
        field=True,
        fieldMaxValue=999,
        fieldMinValue=0,
        label="Iterations: ",
        maxValue=10,
        minValue=0,
        parent=colSolver1Unfold, 
        value=pm.optionVar["unfoldItrOptVar"], 
    )
    cBoxPackUnfold = pm.checkBoxGrp(
        changeCommand=lambda *args: unfoldUpdateOptVar(2),
        columnWidth2=[col1, col2],
        label="",
        label1="Pack",
        parent=colSolver1Unfold,
        value1=pm.optionVar["unfoldPackOptVar"],
    )
    cBoxBorderUnfold = pm.checkBoxGrp(
        changeCommand=lambda *args: unfoldUpdateOptVar(3),
        columnWidth2=[col1, col2],
        label="",
        label1="Prevent self border intersections",
        parent=colSolver1Unfold,
        value1=pm.optionVar["unfoldBorderOptVar"],
    )
    cBoxFlipsUnfold = pm.checkBoxGrp(
        changeCommand=lambda *args: unfoldUpdateOptVar(4),
        columnWidth2=[col1, col2],
        label="",
        label1="Prevent triangle flips",
        parent=colSolver1Unfold,
        value1=pm.optionVar["unfoldFlipsOptVar"],
    )
    sep1Unfold = pm.separator(
        height=sepSpace,
        horizontal=True,
        parent=colSolver1Unfold,
        visible=True,
    )
    
    # Unfold3D: Room Space frame and column
    frameRoomUnfold = pm.frameLayout(
        borderStyle="out",
        label="Room Space options",
        parent=form2Unfold
    )    
    colRoomUnfold = pm.columnLayout(
        parent=frameRoomUnfold,
    )
    
    # Unfold3D: Room Space elements
    menuRoomUnfold = pm.optionMenuGrp(
        changeCommand=lambda *args: unfoldUpdateOptVar(5),
        columnWidth2=[col1, col2],
        label="Map size (Pixels): ",
        parent=colRoomUnfold,
    )    
    
    item8192 = pm.menuItem( label="8192")
    item4096 = pm.menuItem( label="4096")
    item2048 = pm.menuItem( label="2048")
    item1024 = pm.menuItem( label="1024")
    item512 = pm.menuItem( label="512")
    item256 = pm.menuItem( label="256")
    item128 = pm.menuItem( label="128")
    item64 = pm.menuItem( label="64")
    item32 = pm.menuItem( label="32")
    
    menuRoomUnfold.setValue(pm.optionVar["unfoldSizeOptVar"])
    
    sliderRoomUnfold = pm.intSliderGrp(
        changeCommand=lambda *args: unfoldUpdateOptVar(6),
        columnWidth3=[col1, col2, col3],
        field=True,
        fieldMaxValue=999,
        fieldMinValue=0,
        label="Room space (Pixels): ",
        maxValue=10,
        minValue=0,
        parent=colRoomUnfold,
        value=pm.optionVar["unfoldRoomOptVar"],
    )
    sep2Unfold = pm.separator(
        height=sepSpace,
        horizontal=True,
        parent=colRoomUnfold,
        visible=True,
    )    
    
    ## Legacy
    # Legacy: Solver frame and column
    frameSolver2Unfold = pm.frameLayout(
        borderStyle="out",
        label="Solver Options",
        parent=form2Unfold
    )
    colSolver2Unfold = pm.columnLayout(
        parent=frameSolver2Unfold
    )
    
    # Legacy: Solver elements
    solverRowUnfold = pm.rowLayout(
        columnAttach=[1, "right", 0],
        columnWidth2=[col1, col2],
        numberOfColumns=2,
        parent=colSolver2Unfold, 
    )

    solverTextUnfold = pm.text( 
        label="Weight solver towards: ",
        parent=solverRowUnfold,
    )
    
    fieldWeightUnfold = pm.floatField(
        changeCommand=lambda *args: unfoldUpdateOptVar(7, fieldWeightUnfold, sliderWeightUnfold),
        maxValue=1.0,
        minValue=0.0,
        parent=solverRowUnfold, 
        value=pm.optionVar["unfoldSolverOptVar"],
    )
    
    sliderWeightUnfold = pm.floatSliderGrp(
        changeCommand=lambda *args: unfoldUpdateOptVar(7, sliderWeightUnfold, fieldWeightUnfold),
        columnWidth3=[col1, (col2+col3+2), 80],
        extraLabel=" Global solver",
        label="Local solver ",
        minValue=0.0,
        maxValue=1.0,
        parent=colSolver2Unfold,
        value=pm.optionVar["unfoldSolverOptVar"],
    )
    
    optRowUnfold = pm.rowLayout(
        numberOfColumns=2,
        columnAttach=[1, "right", 0],
        columnWidth2=[col1, col2],
        parent=colSolver2Unfold, 
    )
    
    optTextUnfold = pm.text( 
        label="Optimize to original: ",
        parent=optRowUnfold,
    )
    
    fieldOptUnfold = pm.floatField(
        changeCommand=lambda *args: unfoldUpdateOptVar(8, fieldOptUnfold, sliderOptUnfold),
        enable=visState1,
        maxValue=1.0,
        minValue=0.0,
        parent=optRowUnfold, 
        value=pm.optionVar["unfoldOtOOptVar"],
    )
    
    sliderOptUnfold = pm.floatSliderGrp(
        changeCommand=lambda *args: unfoldUpdateOptVar(8, sliderOptUnfold, fieldOptUnfold),
        columnWidth3=[col1, (col2+col3+2), 80],
        enable=visState1,
        extraLabel=" Face area",
        label="Edge length ",
        minValue=0.0,
        maxValue=1.0,
        parent=colSolver2Unfold,
        value=pm.optionVar["unfoldOtOOptVar"],
    )
    
    areaRowUnfold = pm.rowLayout(
        numberOfColumns=2,
        columnAttach=[1, "right", 0],
        columnWidth2=[col1, col2],
        parent=colSolver2Unfold, 
    )
    
    areaTextUnfold = pm.text( 
        label="Surface area weight: ",
        parent=areaRowUnfold,
    )
    
    fieldAreaUnfold = pm.floatField(
        changeCommand=lambda *args: unfoldUpdateOptVar(18, fieldAreaUnfold, sliderAreaUnfold),
        maxValue=1.0,
        minValue=0.0,
        parent=areaRowUnfold, 
        value=pm.optionVar["unfoldAreaOptVar"],
    )
    
    sliderAreaUnfold = pm.floatSliderGrp(
        changeCommand=lambda *args: unfoldUpdateOptVar(18, sliderAreaUnfold, fieldAreaUnfold),
        columnWidth3=[col1, (col2+col3+2), 80],
        extraLabel=" Prio large faces",
        label="All faces equal ",
        minValue=0.0,
        maxValue=1.0,
        parent=colSolver2Unfold,
        value=pm.optionVar["unfoldAreaOptVar"],
    )
        
    sep3Unfold = pm.separator(
        height=sepSpace,
        horizontal=True,
        parent=colSolver2Unfold,
        visible=True,
    )    
    
    # Legacy: Pinning frame and column
    framePinningUnfold = pm.frameLayout(
        borderStyle="out",
        label="Pinning",
        parent=form2Unfold, 
    )
    colPinningUnfold = pm.columnLayout(
        parent=framePinningUnfold, 
    )
    
    # Legacy: Pinning elements
    cBoxPin1Unfold = pm.checkBoxGrp(
        changeCommand=lambda *args: unfoldUpdateOptVar(9),
        columnWidth2=[col1, col2],
        label="",
        label1="Pin UV Shell Border",
        parent=colPinningUnfold, 
        value1=pm.optionVar["unfoldPinBorderOptVar"],
    )
    cBoxPin2Unfold = pm.checkBoxGrp(
        changeCommand=lambda *args: unfoldUpdateOptVar(10, cBoxPin2Unfold, radGrpPinUnfold),    
        columnWidth2=[col1, col2],
        label="",
        label1="Pin UVs",
        parent=colPinningUnfold,
        value1=pm.optionVar["unfoldPinOptVar"],
    )
    radGrpPinUnfold = pm.radioButtonGrp(
        changeCommand=lambda *args: unfoldUpdateOptVar(11),
        columnWidth2=[( col1 + 15 ), ( col2 + 40 )],
        enable=pm.optionVar["unfoldPinOptVar"],
        label1="Pin selected UVs",
        label2="Pin unselected UVs",
        label="",
        numberOfRadioButtons=2,
        parent=colPinningUnfold,
        select=pm.optionVar["unfoldPinTypeOptVar"],
        vertical=True,
    )
    radGrpConstUnfold = pm.radioButtonGrp(
        changeCommand=lambda *args: unfoldUpdateOptVar(12),
        columnWidth2=[col1, col2],
        label1="None",
        label2="Vertical",
        label3="Horizontal",
        label="Unfold constraint: ",
        numberOfRadioButtons=3,
        parent=colPinningUnfold,
        select=pm.optionVar["unfoldConstOptVar"],
        vertical=True,
    )
    sep4Unfold = pm.separator(
        height=sepSpace,
        horizontal=True,
        parent=colPinningUnfold,
        visible=True,
    )    
    
    # Legacy: Other frame and column
    frameOtherUnfold = pm.frameLayout(
        borderStyle="out",
        label="Other Options",
        parent=form2Unfold, 
    )
    colOtherUnfold = pm.columnLayout(
        parent=frameOtherUnfold, 
    )
    
    # Legacy: Other elements
    sliderMaxItrUnfold = pm.intSliderGrp(
        changeCommand=lambda *args: unfoldUpdateOptVar(13),
        columnWidth3=[col1, col2, col3],
        field=True,
        fieldMaxValue=10000,
        fieldMinValue=1,
        label="Max iterations: ",
        maxValue=10000,
        minValue=1,
        parent=colOtherUnfold, 
        value=pm.optionVar["unfoldMaxItrOptVar"], 
    )
    sliderStopUnfold = pm.floatSliderGrp(
        changeCommand=lambda *args: unfoldUpdateOptVar(14),
        columnWidth3=[col1, col2, col3],
        field=True,
        fieldMaxValue=100.0,
        fieldMinValue=0.0,
        label="Stopping threshold: ",
        maxValue=100.0,
        minValue=0.0,
        parent=colOtherUnfold, 
        value=pm.optionVar["unfoldStopOptVar"]
    )
    sep2Unfold = pm.separator(
        height=sepSpace,
        horizontal=True,
        parent=colOtherUnfold,
        visible=True,
    )
    cBoxRescaleUnfold = pm.checkBoxGrp(
        changeCommand=lambda *args: unfoldUpdateOptVar(15, cBoxRescaleUnfold, sliderScaleUnfold),
        columnWidth2=[col1, col2],
        label="",
        label1="Rescale",
        parent=colOtherUnfold, 
        value1=pm.optionVar["unfoldRescaleOptVar"],
    )
    sliderScaleUnfold = pm.floatSliderGrp(
        changeCommand=lambda *args: unfoldUpdateOptVar(16),
        columnWidth3=[col1, col2, col3],
        enable=visState2,
        field=True,
        fieldMaxValue=10000.0,
        fieldMinValue=0.00001,
        label="Scale factor: ",
        maxValue=10.0,
        minValue=0.00001,
        parent=colOtherUnfold, 
        value=pm.optionVar["unfoldSFactOptVar"],
    )
    sep3Unfold = pm.separator(
        height=sepSpace,
        horizontal=True,
        parent=colOtherUnfold,
        visible=True,
    )
    cBoxHistoryUnfold = pm.checkBoxGrp(
        changeCommand=lambda *args: unfoldUpdateOptVar(17),
        columnWidth2=[col1, col2],
        label="",
        label1="Keep history",
        parent=colOtherUnfold, 
        value1=pm.optionVar["unfoldHistOptVar"]
    )
    sep4Unfold = pm.separator(
        height=sepSpace,
        horizontal=True,
        parent=colOtherUnfold,
        visible=True,
    )
    
    ## Quick
    textQuickUnfold = pm.text(
        label="No options here - Things just get done!!",
        parent=form2Unfold
    )
    
    # Buttons
    btnApplyCloseUnfold = pm.button(
        command=lambda *args: core.unfoldUVs("both", winUnfold), 
        label="Confirm",
        parent=form1Unfold,
    )
    btnApplyUnfold = pm.button(
        command=lambda *args: core.unfoldUVs(), 
        label="Apply",
        parent=form1Unfold,
    )
    btnResetUnfold = pm.button( 
        command=lambda *args: unfoldUIReset(),
        label="Reset", 
        parent=form1Unfold,  
    )
    btnCloseUnfold = pm.button( 
        command=lambda *args: pm.deleteUI( winUnfold ),
        label="Close", 
        parent=form1Unfold,  
    )
    
    # Layout frames
    pm.formLayout(
        form2Unfold, edit=True, 
        attachForm=[
        
            (frameMainUnfold, "top", 0), 
            (frameMainUnfold, "left", 0), 
            (frameMainUnfold, "right", 0),  
        
            (frameSolver1Unfold, "left", 0), 
            (frameSolver1Unfold, "right", 0), 

            (frameRoomUnfold, "left", 0), 
            (frameRoomUnfold, "right", 0), 

            (frameSolver2Unfold, "left", 0), 
            (frameSolver2Unfold, "right", 0), 
            
            (framePinningUnfold, "left", 0), 
            (framePinningUnfold, "right", 0), 
            
            (frameOtherUnfold, "left", 0), 
            (frameOtherUnfold, "right", 0), 
            
            (textQuickUnfold, "left", 0), 
            (textQuickUnfold, "right", 0), 
        ], 
        attachControl=[            
            (frameSolver1Unfold, "top", 10, frameMainUnfold), 
            
            (frameRoomUnfold, "top", 10, frameSolver1Unfold), 
            
            (frameSolver2Unfold, "top", 0, frameRoomUnfold), 
            
            (framePinningUnfold, "top", 10, frameSolver2Unfold), 
            
            (frameOtherUnfold, "top", 10, framePinningUnfold),
            
            (textQuickUnfold, "top", 0, frameOtherUnfold), 
        ],
        attachNone=[
            (frameSolver1Unfold, "bottom"),
            
            (frameRoomUnfold, "bottom"), 
            
            (frameSolver2Unfold, "bottom"), 
            
            (framePinningUnfold, "bottom"), 
            
            (frameOtherUnfold, "bottom"), 
            
            (textQuickUnfold, "bottom"), 
        ]
    )
    
    # Layout main frame
    pm.formLayout(
        form1Unfold, edit=True, 
        attachForm=[
            (scrollUnfold, "top", 0),
            (scrollUnfold, "left", 0),
            (scrollUnfold, "right", 0),

            (btnApplyCloseUnfold, "left", 5),         
            (btnApplyCloseUnfold, "bottom", 5),         
            (btnApplyUnfold, "bottom", 5),                
            (btnResetUnfold, "bottom", 5),         
            (btnCloseUnfold, "right", 5),         
            (btnCloseUnfold, "bottom", 5),     
        ], 
        attachControl=[
            (scrollUnfold, "bottom", 0, btnApplyCloseUnfold), 
        ],
        attachPosition=[
            (btnApplyCloseUnfold, "right", 3, 25),                   
            (btnApplyUnfold, "left", 2, 25),                   
            (btnApplyUnfold, "right", 3, 50),                   
            (btnResetUnfold, "right", 3, 75),                   
            (btnResetUnfold, "left", 2, 50),                   
            (btnCloseUnfold, "left", 2, 75),       
        ],
        attachNone=[
            (btnApplyCloseUnfold, "top"),    
            (btnApplyUnfold, "top"),    
            (btnResetUnfold, "top"),    
            (btnCloseUnfold, "top"),    
        ],
    )
    
    # Hide inactive
    unfoldSwitch()

    # Display the window
    pm.showWindow( window )
    
    
# Update NSUV UI
def updateUI():

    # Vars
    btnRow = 317
    sepSpace = 5
    winHeight = 190
    winWidth = 340
    
    # Internal method for accessing the CC page    
    def NSUV_update(url):
        if url == 0:
            pm.launch(web="http://www.creativecrash.com/maya/script/nightshade-uv-editor")
        elif url == 1:
            pm.launch(web="https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=B8QYQ7RZDHP48")
         
    # Check for window duplicate
    if pm.window( winUpdate, exists=True ):
        pm.deleteUI( winUpdate )

    # Window
    window = pm.window(
        winUpdate,
        height=winHeight, 
        minimizeButton=False, 
        maximizeButton=False, 
        resizeToFitChildren=True, 
        sizeable=True, 
        title="Update NSUV", 
        width=winWidth 
    )
    
    # Layouts
    frameUpdate = pm.frameLayout(
        borderStyle="etchedIn", 
        collapsable=False, 
        collapse=False, 
        height=winHeight, 
        label="NSUV Information", 
        marginHeight=10, 
        marginWidth=10, 
        width=winWidth 
    )
    colUpdate = pm.columnLayout(
        adjustableColumn=False, 
        columnAlign="left", 
        rowSpacing=6
    )
    textUpdate = pm.text(
        label="Installed version: \n" + NSUV_title + "\n\n" + 
              "Click below to go and look for an update.\n" + 
              "If you find great use of NSUV, then please consider a donation.\n",
        parent=colUpdate,
    )
    
    sepUpdate = pm.separator(
        height=sepSpace,
        horizontal=True,
        parent=colUpdate,
        visible=True,
    )
        
    # Slider
    btnUpdate = pm.button( 
        command=lambda *args: NSUV_update(0),
        label="Update NSUV", 
        parent=colUpdate,  
        width=btnRow,
    )
    btnUpdate = pm.button( 
        command=lambda *args: NSUV_update(1),
        label="Donate", 
        parent=colUpdate,  
        width=btnRow,
    )

    # Buttons
    btnClose = pm.button( 
        command=lambda *args: pm.deleteUI(window),
        label="Close", 
        parent=colUpdate,  
        width=btnRow,
    )
   
    # Display the window
    pm.showWindow( window )
    
    
# Open pdf doc file, assuming it is in folder
def opendoc() :
    filename = 'Nightshade UV Editor 1.6 - User Manual.pdf'
    docpath = os.path.join( os.path.dirname(inspect.getfile(inspect.currentframe())) , filename)
    os.startfile(docpath, 'open')
