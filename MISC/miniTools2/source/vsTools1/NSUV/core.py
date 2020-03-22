"""
    Core functionality for Nightshade UV editor (NSUV) v1.6.1

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
import pymel.core.datatypes as dt
import os.path
import math
import random
import re

# Vars
pointLeft = [0.0, 0.0]
uvSets = []


## Initialization

# ScriptJobs
def createScriptJobs(win, UVSetsList, cBox):

    # Update the compSpace toggle on tool change
    pm.scriptJob(
        event=["ToolChanged", lambda *args: compSpaceToggle(cBox, 2)],
        parent=win
    )
    
    # Update the uvSetEditor on undo/redo and selection change
    pm.scriptJob(
        event=["SelectionChanged", lambda *args: updateUVSetEditor(UVSetsList)],
        parent=win
    )
    pm.scriptJob(
        event=["SelectTypeChanged", lambda *args: updateUVSetEditor(UVSetsList)],
        parent=win
    )
    pm.scriptJob(
        event=["SelectModeChanged", lambda *args: updateUVSetEditor(UVSetsList)],
        parent=win
    )
    pm.scriptJob(
        event=["Undo", lambda *args: updateUVSetEditor(UVSetsList)],
        parent=win
    )
    pm.scriptJob(
        event=["Redo", lambda *args: updateUVSetEditor(UVSetsList)],
        parent=win
    )
    
    
######## Core methods ########

# Absolute/Relative -toggle for the manipulator
def absToggle(state):    
    if state == True:
        pm.optionVar["absToggleOptVar"] = True
    else:
        pm.optionVar["absToggleOptVar"] = False

    
# Align shells
def alignShells(action):
    
    # Removes the "WARNING: some items cannot be moved in the 3d view" -error message
    pm.mel.eval("setToolTo $gSelect")
    
    # Validate UV selection
    checkSel("UV")
    
    # Turn off undo queue
    pm.undoInfo(stateWithoutFlush=False)
    
    # Store the original selection, get bounds and store the shells in a separate list
    selOrg = pm.ls(selection=True)
    uvBox = pm.polyEvaluate(boundingBoxComponent2d=True)
    shells = convertToShell()
    
    shellsTotal = shellsRemain = len(shells) # Shell count
    
    # Calculate uMin/uMax
    centerU = 0.5 * ( uvBox[0][0] + uvBox[0][1] )
    centerV = 0.5 * ( uvBox[1][0] + uvBox[1][1] )
   
    # Create progress window
    pm.progressWindow(
        isInterruptable=True, 
        maxValue=len(shells), 
        title="Aligning UV shells", 
        progress=0
    )
    
    # Loop through each shell
    for item in shells:
    
        # Break if cancelled by user
        if pm.progressWindow(query=True, isCancelled=True) == True:
            pm.warning("Interupted by user")
            break
        
        # Edit the progress window
        pm.progressWindow(
            edit=True, 
            progress=(shellsTotal - shellsRemain),
            status="Aligning UV shells. %s shells remaining."%shellsRemain        
        )
        
        # Select the shell and calculate new bounds
        pm.select(item)
        shellBox = pm.polyEvaluate(boundingBoxComponent2d=True)
        
        # Turn on the undo queue for the actual shell xform
        pm.undoInfo(stateWithoutFlush=True)
    
        # Move the shell
        if action == "uMax":
            offset = uvBox[0][1] - shellBox[0][1]
            pm.polyEditUV(relative=True, uValue=offset)
        
        if action == "uMin":
            offset = uvBox[0][0] - shellBox[0][0]
            pm.polyEditUV(relative=True, uValue=offset)
        
        if action == "uAvg":       
            offset = centerU - ( 0.5 * (shellBox[0][0] + shellBox[0][1]) )
            pm.polyEditUV(relative=True, uValue=offset)
        
        if action == "vMax":
            offset = uvBox[1][1] - shellBox[1][1]
            pm.polyEditUV(relative=True, vValue=offset)
        
        if action == "vMin":
            offset = uvBox[1][0] - shellBox[1][0]
            pm.polyEditUV(relative=True, vValue=offset)
        
        if action == "vAvg":
            offset = centerV - ( 0.5 * (shellBox[1][0] + shellBox[1][1]) )
            pm.polyEditUV(relative=True, vValue=offset)
            
        # Turn off undo queue
        pm.undoInfo(stateWithoutFlush=False)
    
        # Decrease the shells remaining -counter
        shellsRemain -= 1
    
    # Close the progress window
    pm.progressWindow(endProgress=True)

    # Reselect the original selection
    pm.select(selOrg)
    
    # Turn on undo queue
    pm.undoInfo(stateWithoutFlush=True)
    
    # Activate the move tool
    pm.mel.eval("setToolTo $gMove")
    
    
# Align UVs
def alignUVs(action):
    
    # Original selection
    selOrg = pm.ls(selection=True)
    
    # Poly UVs filter
    selUV = pm.filterExpand(selectionMask=35)    
    if selUV == []:
        return # Stop execution without a warning
        
    # Get bounds
    uvBox = pm.polyEvaluate(boundingBoxComponent2d=True)
        
    # Calculate U and V centers
    centerU = 0.5 * ( uvBox[0][0] + uvBox[0][1] )
    centerV = 0.5 * ( uvBox[1][0] + uvBox[1][1] )
   
    # Removes the "WARNING: some items cannot be moved in the 3d view" -error message
    pm.mel.eval("setToolTo $gSelect")
    pm.select(selUV, replace=True)

    # Align to max U
    if action == "maxU":
        pm.polyEditUV(
            relative=False,
            uValue=uvBox[0][1]
        )
    
    # Align to min U
    if action == "minU":    
        pm.polyEditUV(
            relative=False,
            uValue=uvBox[0][0]
        )
    
    # Align to average U
    if action == "avgU":    
        pm.polyEditUV(
            relative=False,
            uValue=centerU
        )
    
    # Align to max V
    if action == "maxV":
        pm.polyEditUV(
            relative=False,
            vValue=uvBox[1][1]
        )
    
    # Align to min V
    if action == "minV":
        pm.polyEditUV(
            relative=False,
            vValue=uvBox[1][0]
        )
    
    # Align to average V
    if action == "avgV":     
        pm.polyEditUV(
            relative=False,
            vValue=centerV
        )
        
    if action == "singularity":
        pm.polyEditUV(
            relative=False,
            uValue=centerU,
            vValue=centerV,
        )
    
    # Select original selection
    pm.select(selOrg)
    
    # Activate the move tool
    pm.mel.eval("setToolTo $gMove")
    
    
# Calculate arctangent and return the angle
def calcArctanAngle(uv1, uv2):
    
    # Store coordinates
    pointA = pm.polyEditUV(uv1, query=True)
    pointB = pm.polyEditUV(uv2, query=True)
    
    # Results can be both positive and negative, so calc both
    if pointA[0] >= pointB[0]:
        distU = (pointA[0] - pointB[0])
        distV = (pointA[1] - pointB[1])
    else:
        distU = (pointB[0] - pointA[0])
        distV = (pointB[1] - pointA[1])
        
    # Use arctangent to calculate angle
    angle = math.degrees( math.atan2(distV, distU) )
    return angle
    
 
# Calculate pixel distance between two UVs
def calcPxDist():
    
    # Validate UV selection
    checkSel("UV")
    
    # Get bounds and calculate distances
    uvBox = pm.polyEvaluate(boundingBoxComponent2d=True)
    distU = abs(uvBox[0][1] - uvBox[0][0])
    distV = abs(uvBox[1][0] - uvBox[1][1])
    
    # Calculate hypotenuse using trig
    distUV = math.hypot(distU, distV)
    
    # Return distances
    return (distU, distV, distUV)
    

# Calculate UV utilization
def calcUVStats():

    # Validate selection
    checkSel("any")
    
    # Store original selection
    selOrg = pm.ls(selection=True)
    
    # Run script
    calcUVStats.calcUVStats() # WARN - make my own version of this. Script fails too easily as a user
    
    # Reselct the original selection
    pm.select(selOrg)
  
  
# Selection checker
def checkSel(selType):
    
    # Check for any selection
    if selType == "any":
        selection = pm.filterExpand( selectionMask=(12, 31, 32, 34, 35) )
        if selection == [] or selection == None:
            errorCode(0)
        
    # Check for valid mesh selection 
    if selType == "mesh":
        selection = pm.filterExpand( selectionMask=12 )
        if selection == [] or selection == None:
            errorCode(9)  
    
    # Check for valid face selection
    if selType == "face":
        selection = pm.filterExpand( selectionMask=34 )
        if selection == [] or selection == None:
            errorCode(1)
            
    # Check for valid edge selection
    if selType == "edge":
        selection = pm.filterExpand( selectionMask=32 )
        if selection == [] or selection == None:
            errorCode(14)            
        
    # Check for valid UV selection
    if selType == "UV":
        selection = pm.filterExpand( selectionMask=35 )
        if selection == [] or selection == None:
            errorCode(2)  
        
    # Check for valid UV selection (Two points only)
    if selType == "UV2":
        selection = pm.filterExpand( selectionMask=35 )
        if len(selection) != 2:
            errorCode(8)
        
    # Check for valid edge or UV selection
    if selType == "edgeUV":
        selection = pm.filterExpand( selectionMask=(32, 35) )
        if selection == [] or selection == None:
            errorCode(3)
                        
    # Check for valid face or mesh selection
    if selType == "faceMesh":
        selection = pm.filterExpand( selectionMask=(12, 34) )
        if selection == [] or selection == None:
            errorCode(11)
        
    # Check for valid face or UV selection
    if selType == "faceUV":
        selection = pm.filterExpand( selectionMask=(34, 35) )
        if selection == [] or selection == None:
            errorCode(4)    
        
    # Check for valid mesh or UV selection 
    if selType == "meshUV":
        selection = pm.filterExpand( selectionMask=(12, 35) )
        if selection == [] or selection == None:
            errorCode(5)
        
    # Check for valid selection for the Stitch together -tool
    if selType == "stitch":
        if pm.filterExpand( selectionMask=35 ) != None:
            if len(pm.filterExpand( selectionMask=35 )) != 2:
                errorCode(15)
        elif pm.filterExpand( selectionMask=32 ) != None:
            if len(pm.filterExpand( selectionMask=32 )) != 1:
                errorCode(16)
        else: # Incorrect select
            errorCode(17)
    
    # Check if selection spans over multiple shells
    if selType == "multi":
    
        # Store original selection and the UVs of it
        selOrg = pm.ls(selection=True)
        selOrgUVs = pm.polyListComponentConversion(toUV=True)
        
        # Expand to entire shells
        shellsAll = pm.polySelectConstraint(
            mode=2,
            shell=1,
            type=0x0010
        )
        pm.polySelectConstraint(disable=True)
        
        # Store all shell(s) UVs
        selUVs = pm.ls(selection=True, flatten=True)
        
        # Get one single UV from selOrgUVs and convert to just ONE shell
        pm.select(selOrgUVs[0])
        shellSingle = pm.polySelectConstraint(
            mode=2, 
            shell=1, 
            type=0x0010
        )
        pm.polySelectConstraint(disable=True)
        
        # This if-statement will only be true if the original selection
        # could be expanded to cover multiple UV shells.
        if shellSingle != shellsAll:
            pm.select(selOrg)
            errorCode(6) 
            
            
# Comp space toggle
def compSpaceToggle(cBox, mode):
  
    # Query optVar - not used atm
    if mode == 2:
        return pm.optionVar["compSpaceOptVar"] 
        
    # Check for UV selection (necessary for scriptJob to bypass Maya bug)
    selection = pm.filterExpand(selectionMask=35)
    if selection != [] or selection != None:
    
        # Toggle and update UI component
        pm.texMoveContext(
            "texMoveContext",
            edit=True,
            snapComponentsRelative=mode
        )
        cBox.setValue(mode)
 
        # Update optVar 
        pm.optionVar["compSpaceOptVar"] = mode
        
    else:
        pass
        
        
# Returns list with each shell in it. Used for orienting/randomizing shells
def convertToShell():
    
    listFinal = []
    
    # Store coords and check count
    selCoords = pm.filterExpand(selectionMask=35) # Poly UVs
    uvRemain = uvCount = len(selCoords)
    
    # Progress window
    pm.progressWindow(
        isInterruptable=True,  
        maxValue=uvCount, 
        progress=0, 
        status="Pre-processing UV shells", 
        title="Pre-processing UV shells" 
    )
    
    # Do for every shell
    while uvRemain != 0:
        
        # Break if cancelled by user
        if pm.progressWindow(query=True, isCancelled=True) == True:
            pm.warning("Interupted by user")
            break
        
        # Edit the progress window
        pm.progressWindow(
            edit=True, 
                progress=(uvCount - uvRemain),
                status=("Pre-processing shells.\n%s UVs left")%uvRemain
        )
    
        # Select the first and current coord of selCoords
        pm.select(selCoords[0], replace=True)
        
        # Expand selection to entire shell and store in var
        pm.polySelectConstraint(type=0x0010, shell=True, border=False, mode=2)
        pm.polySelectConstraint(shell=False, border=False, mode=0)
        selShell = pm.ls(selection=True, flatten=True)
        
        # Go back to original single-UV selection (replace)
        pm.select(selCoords, replace=True)
        
        # Reduce that selection by deselecting previous shell
        pm.select(selShell, deselect=True)
        selCoords = pm.ls(selection=True, flatten=True)
        
        # Recalculate number of UVs left
        uvRemain = len(selCoords)
        
        # Add shell to list
        listFinal.append(selShell)
        pm.select(clear=True)
        
    # Close progress window
    pm.progressWindow(endProgress=True)
    
    # Return shell list
    return listFinal
    
  
# Copy UV Set
def copySet(scrollList, copyFrom, copyTo, win=None):

    # Get selection type
    selection = pm.filterExpand(selectionMask=12) # Mesh
    if selection == [] or selection == None:
        selection = pm.filterExpand(selectionMask=(31, 32, 34, 35)) # Edges, Faces, Verts or UVs

    # Copy selected
    if selection != [] or selection != None:
        pm.polyCopyUV(
            selection,
            constructionHistory=True,
            uvSetName=copyTo,
        ) 

    else: # Copy entire set
        pm.polyUVSet(
            copy=True,
            newUVSet=copyTo,
            uvSet=copyFrom,
        ) 

    # Update the UV set editor
    updateUVSetEditor(scrollList)
    
    # Close the copySetUI window
    if win != None:
        pm.deleteUI(win)

    # Go to mesh selection mode
    pm.mel.eval("toggleSelMode")
    pm.selectMode(object=True)
 

# Create new UV set
def createSet(scrollList, closeWin=None, noClose=False):

    # Selection check
    checkSel("mesh")

    instVar = False
    unShareVar = False
    
    # Check optVars
    if pm.optionVar["newUVSetShareOptVar"] > 1:
        instVar = True
        if pm.optionVar["newUVSetShareOptVar"] == 3:
            unShareVar = True
    
    # Create the UV set
    if instVar == True:
        pm.polyUVSet(
            create=True,
            perInstance=instVar,
            unshared=unShareVar,
            uvSet=pm.optionVar["newUVSetOptVar"]
        )
    else: # discarding perInstance -flag in order to avoid [0] -suffix
        pm.polyUVSet(
            create=True,
            uvSet=pm.optionVar["newUVSetOptVar"]
        )

    # Update the UV Set list
    updateUVSetEditor(scrollList)

    # Close the "Create New UV Set" -window if necessary
    if closeWin != None and noClose == False:
        pm.deleteUI(closeWin)
        
        
# Create new UV set - store optVars
def createSetOptVars(optVar, ctrlName):

    if optVar == 0:
        pm.optionVar["newUVSetOptVar"] = ctrlName.getText()
    else:
        pm.optionVar["newUVSetShareOptVar"] = ctrlName.getSelect()-1
   
    
# Create shell
def createShell():

    # Validate face selection
    checkSel("face")
    
    # Original selection
    selOrg = pm.ls(selection=True)
    
    # Convert to border selection
    selBorders = pm.polyListComponentConversion(
        selOrg,
        border=True,
        fromFace=True,
        toEdge=True,    
    )  

    # Select the borders, cut them up, reselect original selection as UVs
    pm.select(selBorders)    
    pm.polyMapCut()
    pm.select(selOrg)
    newSel = pm.polyListComponentConversion(toUV=True)
    pm.select(newSel)
    
    # Activate the move tool
    pm.mel.eval("setToolTo $gMove")

    
# Switches back to the native UV Texture Editor
def defaultUV(win):

    # Close down NSUV
    pm.deleteUI(win)
    
    # This row below is in case you need to source a custom in-house script.
    # path = pm.util.getEnv("MAYA_LOCATION") + "/scripts/others/textureWindowCreateToolBar.mel"
    
    # Re-source the native toolbar
    pm.mel.source("textureWindowCreateToolBar.mel") # Change this to pm.mel.source(path) if you are using a custom script

    # Open up the native UV Texture Editor
    pm.runtime.TextureViewWindow()
    
    
def deleteSet(scrollList):
    
    # Get UV sets from scrollList
    uvSets = scrollList.getSelectItem()
    
    # Delete all selected sets from the current mesh selection
    for item in uvSets:
        pm.polyUVSet(
            delete=True,
            uvSet=item,
        )
        
    # Update the UV set editor
    updateUVSetEditor(scrollList)
    
    
# Duplicate current UV set
def dupeSet(scrollList, nameFromOptVar=False, window=None ):

    # Selection check
    checkSel("mesh")
    
    # Get selection
    selOrg = pm.ls(selection=True)

    if nameFromOptVar == False:
    
        # Dupe the active UV set of each mesh
        for item in selOrg:   
            pm.select(item)        
            uvSetActive = pm.polyUVSet(currentUVSet=True, query=True)
            pm.polyCopyUV(
                item,
                constructionHistory=True,
                uvSetNameInput=str(uvSetActive[0]),
                uvSetName=str(uvSetActive[0]),
                createNewMap=True
            ) 
    else:
        # Copy into new UV set (with name)
        for item in selOrg:   
            pm.select(item)        
            uvSetActive = pm.polyUVSet(currentUVSet=True, query=True)
            pm.polyCopyUV(
                item,
                constructionHistory=True,
                uvSetNameInput=str(uvSetActive[0]),
                uvSetName=pm.optionVar["copyNewUVSetOptVar"],
                createNewMap=True
            ) 
            
        # Close window
        pm.deleteUI(window)

    # Reselect the original selection
    pm.select(selOrg)
    
    # Update the UV set editor
    updateUVSetEditor(scrollList)
    

# Cycles edge color
def edgeColor(dir):
    
    # Display color
    dispCol = pm.displayColor("polyEdge", query=True, active=True)
    
    # Set the color variable
    if dir == "forward":
        if dispCol == 31:
            dispCol = 1 # Cycle around
        else:
            dispCol += 1        
        
    elif dir == "backward":
        if dispCol == 1:
            dispCol = 31 # Cycle around
        else:
            dispCol -= 1
    
    # Change the edge color    
    pm.displayColor("polyEdge", dispCol , active=True)
    
    
# Flips a UV selection
def flipUVs(direction):
    
    # Update and get pivot coords
    updateManipCoords()
    manipCoords = pm.optionVar["manipCoordsOptVar"]
    
    # Flip
    if direction == "U":
        pm.polyEditUV(
            pivotU=manipCoords[0],
            scaleU = -1
        )        
    if direction == "V":
        pm.polyEditUV(
            pivotV=manipCoords[1],
            scaleV = -1
        )

        
# Offset back all shells into the default UV range
def gatherShells():
    
    # Selection check
    checkSel("mesh")
    
    # Store selection
    orgSel = pm.ls(flatten=True, selection=True)
    uvSel = pm.polyListComponentConversion(toUV=True)
    uvSel = pm.ls(uvSel, flatten=True)
    
    # Progress window
    pm.progressWindow(
        isInterruptable=True,  
        maxValue=len(uvSel), 
        minValue=0,
        status="Gathering shells", 
        title="Gather UVs" 
    )
    
    # Go through each UV
    for uvCoord in uvSel:
        
        # Break if cancelled by user
        if pm.progressWindow(query=True, isCancelled=True) == True:
            pm.warning("Interupted by user")
            break

        move = False
        offsetU = 0.0
        offsetV = 0.0
        position = pm.polyEditUV(uvCoord, query=True)
        
        # Get U offset distance as whole 0-1 -steps
        if position[0] < 0:
            offsetU = 1 - math.trunc(position[0])
            move = True          
        elif position[0] > 1:
            offsetU = 0 - math.trunc(position[0])
            move = True
            
        # Get V offset distance as whole 0-1 -steps
        if position[1] < 0:
            offsetV = 1 - math.trunc(position[1])
            move = True          
        elif position[1] > 1:
            offsetV = 0 - math.trunc(position[1])
            move = True
        
        # Move the shell
        if move == True:
            pm.select(uvCoord, replace=True)
            pm.polyEditUVShell(
                relative=True, 
                uValue=offsetU, 
                vValue=offsetV
            )
            
        # Update the progress window
        pm.progressWindow(edit=True, step=1)
        
    # Close the progress window and reselect original selection
    pm.progressWindow(endProgress=True)
    pm.select(orgSel, replace=True)

    
# Method for fetching UV sets
def getSet(mode, object, objUVSet=None):

    if mode == "all":
        results = pm.polyUVSet(
            object, 
            allUVSets=True,
            perInstance=True, 
            query=True 
        )   
    
    elif mode == "current":
        results = pm.polyUVSet(
            object,
            currentUVSet=True, 
            query=True
        )

        # Make unicode list to single item string
        if results != None:            
            results = str(results[0])
    
    elif mode == "instanced":
        results = pm.polyUVSet(
            object,
            uvSet=objUVSet,
            query=True,
            perInstance=True,
        )
    
    else:
        print("NSUV.core.getSet() was used with an incorrect mode -flag")
        
    return results
  
  
# Get and return meshes from selection
def getShapes():
    
    # From selection
    shapes = pm.listRelatives(
        shapes=True, 
        fullPath=True, 
        type="mesh"
    )

    # From selected group
    if shapes == None or shapes == []:
        # shapes = pm.ls(selection=True, type="transform") - OLD
        pass # We do NOT want to return a group's transform node - causes errors in updateUVSetEditor()
        
    # From components
    if shapes == None or shapes == []:
        shapes = pm.listRelatives(fullPath=True, parent=True, type="mesh")
        
    return shapes
  
  
# Splits up a shared edge into two uvEdges - Returns a tuple with the uvEdges
def getUVEdgePairs(selUVs):   
    i = 0
    
    # Find uvEdge pairs by first finding a face that is shared by 2 UVs in selUVs
    while i != 4:
        try:
            uvA_faceList = pm.ls(pm.polyListComponentConversion(selUVs[0], fromUV=True, toFace=True), flatten=True, long=True)
            uvB_faceList = pm.ls(pm.polyListComponentConversion(selUVs[i], fromUV=True, toFace=True), flatten=True, long=True)
        except IndexError: # Will occur if the UVs are not on the same shared edge
            errorCode(18)
        
        # Conv. face lists to sets and get the intersecting face
        intersection = list(set(uvA_faceList) & set(uvB_faceList))
        
        # Might get more than one face. If so, check each face's UVs against selUVs
        if len(intersection) != 1:
            for face in intersection:
                faceUVs = pm.ls(pm.polyListComponentConversion(face, fromFace=True, toUV=True), flatten=True, long=True)
                uvCount = 0
                for uv in faceUVs:
                    if uv in selUVs:
                        uvCount += 1
                if uvCount == 2:
                    intersection = face
                    break

        if intersection != []: 
        
            # Now get the UVs of the intersecting face
            if type(intersection) is list: # as it might be a list 
                faceUVs = pm.ls(pm.polyListComponentConversion(intersection[0], fromFace=True, toUV=True), flatten=True, long=True)
            else:
                faceUVs = pm.ls(pm.polyListComponentConversion(intersection, fromFace=True, toUV=True), flatten=True, long=True)
            
            # Match the UVs of the intersecting face towards the original UV selection
            j = 0
            removeList = []
            while j != len(faceUVs):
                if faceUVs[j] not in selUVs:
                    removeList.append(faceUVs[j])
                j += 1
                
            # Remove UVs that weren't found in the original UV selection
            for uv in removeList:
                if uv in faceUVs:
                    faceUVs.remove(uv)

            # Store in logical var, break out...
            uvEdgeA = faceUVs
            break
            
        else:
            i += 1
            
    # Get the final uvEdge by exclusion and store in a logical var
    removeList = []
    for uv in selUVs:
        if uv in uvEdgeA:
            removeList.append(uv)        
    for uv in removeList:
        selUVs.remove(uv)
    uvEdgeB = selUVs
    
    # Return the pairs
    uvEdgePairs = (uvEdgeA, uvEdgeB)
    return uvEdgePairs
  
  
# Layout U/V strip
def layoutStrip(dir):
        
    # Layout U strip
    pm.polyLayoutUV(
        flipReversed=False,
        layout=1,
        layoutMethod=1,
        percentageSpace=0.2,
        rotateForBestFit=True,
        scale=0,
    )
        
    # Convert selection to UVs and select it
    selUV = pm.polyListComponentConversion(toUV=True)
    pm.select(selUV)
    
    # Rearrange if user wants a V-strip
    if dir == "V":
        
        # Rotate and align shells
        pm.polyEditUV(
            angle=90,
            pivotU=0.0,
            pivotV=0.0
        )
        alignShells("uMin")
        
        # Get selection bounds, calculate distance to U=0 and translate
        uvBox = pm.polyEvaluate(boundingBoxComponent2d=True)
        offset = uvBox[0][1] - uvBox[0][0]
        pm.polyEditUV(uValue=offset)
    
    # Activate the move tool
    pm.mel.eval("setToolTo $gMove")   
    
    
# Reset or get value from the manipulation field
def manipField(field, action):

    # Update the optionVar
    pm.optionVar["manipAmtOptVar"] = field.getValue()
 
    # Reset to 0
    if action == 0:
        field.setValue(0.0)
        pm.optionVar["manipAmtOptVar"] = 0.0
    
    # Reset to 1
    elif action == 1:
        field.setValue(1.0)
        pm.optionVar["manipAmtOptVar"] = 1.0
    
    # Get value
    elif action == "get":
        pm.optionVar["manipAmtOptVar"] = field.getValue()
        
    # Double value
    elif action == "double":
        newVal = pm.optionVar["manipAmtOptVar"] = pm.optionVar["manipAmtOptVar"] * 2
        field.setValue(newVal)
        
    # Split value
    elif action == "split":
        newVal = pm.optionVar["manipAmtOptVar"] = pm.optionVar["manipAmtOptVar"] / 2
        field.setValue(newVal)
        
    # U-distance
    elif action == "distU":
        
        # Get bounding box coords, and absolute distance between
        uvBBox = pm.polyEvaluate(boundingBoxComponent2d=True)
        newVal = abs(uvBBox[0][1] - uvBBox[0][0])

        pm.optionVar["manipAmtOptVar"] = newVal
        field.setValue(newVal)
        
    # U-distance
    elif action == "distV":
        
        # Get bounding box coords, and absolute distance between
        uvBBox = pm.polyEvaluate(boundingBoxComponent2d=True)
        newVal = abs(uvBBox[1][1] - uvBBox[1][0])
        
        pm.optionVar["manipAmtOptVar"] = newVal
        field.setValue(newVal)
        
    # Store value into var A
    elif action == "setA":    
        newVal = pm.optionVar["manipVarAOptVar"] = field.getValue()
        pm.optionVar["manipAmtOptVar"] = newVal
        
    # Load value from var A
    elif action == "getA":
        newVal = pm.optionVar["manipAmtOptVar"] = pm.optionVar["manipVarAOptVar"]
        field.setValue(newVal)
    
    # Store value into var B
    elif action == "setB":    
        newVal = pm.optionVar["manipVarBOptVar"] = field.getValue()
        pm.optionVar["manipAmtOptVar"] = newVal
        
    # Load value from var B
    elif action == "getB":
        newVal = pm.optionVar["manipAmtOptVar"] = pm.optionVar["manipVarBOptVar"]
        field.setValue(newVal)
    
    
# UV mapping
def mapping(projection, planarAxis=None, win=None):

    # Vars
    layoutVar = 0
    methodVar = 0
    optimizeVar = 0
    orgSel = None
    projList = []
    scaleVar = 0
    ssVar = False
    
    
    ## Internal methods
    
    # Method for creating meshFace -groups from a selection containing both meshes and faces
    # Returned list contains meshes on the first index number and meshFace -groups on the second
    def mappingCreateFaceGrpList():

        # Make sure we have faces and not meshes
        pm.mel.ConvertSelectionToFaces()
        selection = pm.ls(selection=True)
    
        # Create set and loop through selection
        shapeSet = set()
        for item in selection:
            shapeSet.add(item.node()) # Get shape node and add to set
            
        # Convert set to list
        shapeSet = list(shapeSet)

        # Create main list - populate with null objects. One None per shape node
        mainList = [None] * len(shapeSet)

        # Loop through every shape node, one index at a time
        for item in range(len(shapeSet)):      
        
            meshFaceList = []        
            for meshFaceGrp in selection:
               
                # Create sub list with all meshFace -groups belonging to each shape node
                if meshFaceGrp.node() == shapeSet[item]:
                    meshFaceList.append(meshFaceGrp)
                    # selection.remove(meshFaceGrp) # Reduces unneccessary scanning - but breaks script

            # Add meshFace -sub list to main list
            mainList[item] = meshFaceList
        
        # Return cleaned meshFace -group list    
        return mainList
        
    
    # Method for setting the projection attribs of an automatic projection
    def mappingSetAttr(meshFaceGrp, projType):
        
        proj = None
        
        # Get bounding box, store center points (which is where the manipulator is)
        bounds = pm.exactWorldBoundingBox(meshFaceGrp)
        manipX = (bounds[0] + bounds[3]) / 2.0
        manipY = (bounds[1] + bounds[4]) / 2.0
        manipZ = (bounds[2] + bounds[5]) / 2.0
        
        # Calculate XYZ distances of the bounding box, and get scale value
        distX = abs(bounds[3] - bounds[0])
        distY = abs(bounds[4] - bounds[1])
        distZ = abs(bounds[5] - bounds[2])
        scaleVal = max(max(distX, distY), distZ)
        
        # Get shape node and projection node from incomming meshFaceGrp
        if projType == "auto":
            proj = pm.listConnections( meshFaceGrp[0].node() , destination=True, type="polyAutoProj")[0]
        elif projType == "cyl":
            proj = pm.listConnections( meshFaceGrp[0].node() , destination=True, type="polyCylProj")[0]
        elif projType == "plane":
            proj = pm.listConnections( meshFaceGrp[0].node() , destination=True, type="polyPlanarProj")[0]
        elif projType == "sphere":
            proj = pm.listConnections( meshFaceGrp[0].node() , destination=True, type="polySphProj")[0]
        
        # Editor projection node
        if projType == "auto": 
        
            # World space
            if pm.optionVar["mapAutoMS2RadGrpOptVar"] == 1:
                pm.setAttr(proj + ".pivotX", manipX)
                pm.setAttr(proj + ".pivotY", manipY)
                pm.setAttr(proj + ".pivotZ", manipZ)

                pm.setAttr(proj + ".translateX", manipX)
                pm.setAttr(proj + ".translateY", manipY)
                pm.setAttr(proj + ".translateZ", manipZ)
                
            # Local space
            else: 
                pm.setAttr(proj + ".pivotX", 0.0)
                pm.setAttr(proj + ".pivotY", 0.0)
                pm.setAttr(proj + ".pivotZ", 0.0)

                pm.setAttr(proj + ".translateX", 0.0)
                pm.setAttr(proj + ".translateY", 0.0)
                pm.setAttr(proj + ".translateZ", 0.0)

            pm.setAttr(proj + ".scaleX", scaleVal)
            pm.setAttr(proj + ".scaleY", scaleVal)
            pm.setAttr(proj + ".scaleZ", scaleVal)

            # Add projection node to projList...
            if pm.optionVar["mapAutoMSBox2OptVar"] == True:
                projList.append(proj)
                
                
        elif projType == "cyl":
            pm.setAttr(proj + ".projectionHorizontalSweep", pm.optionVar["mapCylindricalSweepOptVar"])   

            # Add projection node to projList...
            if pm.optionVar["mapCylindricalMS2BoxOptVar"] == True:
                projList.append(proj)
                
        
        elif projType == "plane":
        
            # Add projection node to projList...
            if pm.optionVar["mapPlanarMS3BoxOptVar"] == True:
                projList.append(proj)
                
        
        elif projType == "sphere":
            pm.setAttr(proj + ".projectionHorizontalSweep", pm.optionVar["mapSphericalSweep1OptVar"])   
            pm.setAttr(proj + ".projectionVerticalSweep", pm.optionVar["mapSphericalSweep2OptVar"])   
        
            # Add projection node to projList...
            if pm.optionVar["mapSphericalMS2BoxOptVar"] == True:
                projList.append(proj)  

        else:
            print("Unknown projection type sent to core.mapping.mappingSetAttr()")
        
    
    ## Project UVs
    
    # Check for valid face or mesh selection
    checkSel("faceMesh")

    # Store original selection
    orgSel = pm.ls(selection=True)
    
    
    ## Automatic projection
    if projection == "auto":
  
        # Eval optVars
        if pm.optionVar["mapAutoMS1RadGrpOptVar"] == 2:
            optimizeVar = 1
        
        if pm.optionVar["mapAutoSSRadGrpOptVar"] == 1:
            ssVar = True

        if pm.optionVar["mapAutoLayoutMenuOptVar"] == "Along U":
            layoutVar = 1
        elif pm.optionVar["mapAutoLayoutMenuOptVar"] == "Into Square":
            layoutVar = 2
        elif pm.optionVar["mapAutoLayoutMenuOptVar"] == "Tile":
            layoutVar = 3
            
        if pm.optionVar["mapAutoLayoutRadGrp1OptVar"] == 2:
            scaleVar = 1
        elif pm.optionVar["mapAutoLayoutRadGrp1OptVar"] == 3:
            scaleVar = 3
            
        if pm.optionVar["mapAutoLayoutRadGrp2OptVar"] == 2:
            methodVar = 1
    
        # Create meshFace group -list
        meshFaceGrpList = mappingCreateFaceGrpList()
        
        # Start projecting - one meshFaceGrp at a time
        for meshFaceGrp in meshFaceGrpList:
    
            # Project with custom settings
            if pm.optionVar["mapAutoMethodOptVar"] == 1:
            
                # Custom UV set name
                if pm.optionVar["mapAutoSetBoxOptVar"] == True:
                    pm.polyAutoProjection(
                        meshFaceGrp,
                        constructionHistory=True,
                        createNewMap=pm.optionVar["mapAutoSetBoxOptVar"],
                        layout=layoutVar,
                        layoutMethod=methodVar,
                        optimize=optimizeVar,
                        percentageSpace=pm.optionVar["mapAutoSpaceValOptVar"],
                        planes=int(pm.optionVar["mapAutoMSMenuOptVar"]),
                        scaleMode=scaleVar,
                        uvSetName=pm.optionVar["mapAutoSetOptVar"],
                        worldSpace=ssVar,
                    )
                else: # No custom UV set name
                    pm.polyAutoProjection(
                        meshFaceGrp,
                        constructionHistory=True,
                        createNewMap=pm.optionVar["mapAutoSetBoxOptVar"],
                        layout=layoutVar,
                        layoutMethod=methodVar,
                        optimize=optimizeVar,
                        percentageSpace=pm.optionVar["mapAutoSpaceValOptVar"],
                        planes=int(pm.optionVar["mapAutoMSMenuOptVar"]),
                        scaleMode=scaleVar,
                        worldSpace=ssVar,
                    )
                
                # Set projection node attributes
                mappingSetAttr(meshFaceGrp, "auto")
            
                # Normalize results
                if pm.optionVar["mapAutoNormBoxOptVar"] == True:    

                    # Convert to UVs            
                    priorSel = pm.ls(selection=True)     
                    pm.select( pm.polyListComponentConversion(orgSel, toUV=True) )
                    
                    # Normalize
                    normalizeShells(0)
                    
                    # Reselect selection
                    pm.select(priorSel)
                    
                
            # Project with quick settings
            else:            
                pm.polyAutoProjection(
                    orgSel,
                    constructionHistory=True,
                    createNewMap=False,
                    layout=2,
                    layoutMethod=0,
                    optimize=0,
                    percentageSpace=0.2,
                    scaleMode=1,
                    worldSpace=True,
                )
                
        # Select original selection
        pm.select(orgSel)
        
        # If the user wants the projection manipulators visible...
        if pm.optionVar["mapAutoMSBox2OptVar"] == True:
            for item in projList:
                pm.select(item, add=True)
            pm.setToolTo("ShowManips")
    
    
    ## Cylindrical projection
    elif projection == "cyl":
    
        # Create meshFace group -list
        meshFaceGrpList = mappingCreateFaceGrpList()
        
        # Start projecting - one meshFaceGrp at a time
        for meshFaceGrp in meshFaceGrpList:

            # Custom UV set name
            if pm.optionVar["mapCylindricalSetBoxOptVar"] == True:
                pm.polyProjection(
                    meshFaceGrp,
                    constructionHistory=True,
                    createNewMap=pm.optionVar["mapCylindricalSetBoxOptVar"],
                    insertBeforeDeformers=pm.optionVar["mapCylindricalMS1BoxOptVar"],
                    smartFit=True,
                    type="cylindrical",
                    uvSetName=pm.optionVar["mapCylindricalSetOptVar"],
                )
            else: # No custom UV set name
                pm.polyProjection(
                    meshFaceGrp,
                    constructionHistory=True,
                    insertBeforeDeformers=pm.optionVar["mapCylindricalMS1BoxOptVar"],
                    smartFit=True,
                    type="cylindrical",
                )
                
            # Set projection node attributes
            mappingSetAttr(meshFaceGrp, "cyl")
            
        # Select original selection
        pm.select(orgSel)
        
        # If the user wants the projection manipulators visible...
        if pm.optionVar["mapCylindricalMS2BoxOptVar"] == True:
            for item in projList:
                pm.select(item, add=True)
            pm.setToolTo("ShowManips")

    
    ## Normal based projection
    elif projection == "normal":
    
        # Vars
        vectorMean = []
        vectorCount = 0

        # Create meshFace group -list
        meshFaceGrpList = mappingCreateFaceGrpList()
        
        # Start projecting - one meshFaceGrp at a time
        for meshFaceGrp in meshFaceGrpList:
        
            pm.select(meshFaceGrp)
            meshFaceGrpFlat = pm.ls(selection=True, flatten=True)
        
            # Calculate mean vector, then invert it
            for face in meshFaceGrpFlat:
                vectorMean.append( face.getNormal() )

            vectorMean = sum(vectorMean) / len(vectorMean)
            if vectorMean[0] != 0:
                vectorMean[0] = -vectorMean[0]
            if vectorMean[1] != 0:
                vectorMean[1] = -vectorMean[1]
            if vectorMean[2] != 0:
                vectorMean[2] = -vectorMean[2]

            # Create new tempCamera (by cloning the persp camera)
            camTemp = pm.duplicate("persp")
            camTemp = camTemp[0] # list to single object

            # Get current active modelling panel and switch the camera there to camTemp
            panel = pm.getPanel(withFocus=True)
            pm.lookThru(camTemp, panel)

            # Get camera vector and calculate angle between vectors - return as 3 Euler angles
            vectorCam = camTemp.viewDirection(space="world")
            camAngles = pm.angleBetween( euler=True, vector1=vectorCam, vector2=vectorMean )

            # Rotate camera, focus on the selection
            pm.xform(camTemp, relative=True, rotation=[ camAngles[0], camAngles[1], camAngles[2] ])
            pm.viewFit()
        
            # Make projection
            if pm.optionVar["mapNormalSetBoxOptVar"] == True:
                pm.polyProjection(
                    meshFaceGrp,
                    constructionHistory=True,
                    createNewMap=pm.optionVar["mapNormalSetBoxOptVar"],
                    insertBeforeDeformers=pm.optionVar["mapNormalMS2OptVar"],
                    keepImageRatio=pm.optionVar["mapNormalMS1OptVar"],
                    mapDirection="c",
                    type="planar",
                    uvSetName=pm.optionVar["mapNormalSetOptVar"],
                )
            else:
                pm.polyProjection(
                    meshFaceGrp,
                    constructionHistory=True,
                    createNewMap=pm.optionVar["mapNormalSetBoxOptVar"],
                    insertBeforeDeformers=pm.optionVar["mapNormalMS2OptVar"],
                    keepImageRatio=pm.optionVar["mapNormalMS1OptVar"],
                    mapDirection="c",
                    type="planar",
                )
            
            # Switch back to perspective camera
            pm.lookThru("persp", panel)
            
            # Remove tempCamera
            pm.delete(camTemp)
            
        # Select original selection
        pm.select(orgSel)
    
    
    ## Planar projection
    elif projection == "plane":
    
        # Eval direction var
        if planarAxis == None:
        
            if pm.optionVar["mapPlanarMS1RadGrpOptVar"] == 1:
                planarAxis = "bestPlane"
                
            else:
                if pm.optionVar["mapPlanarMS2RadGrpOptVar"] == 1:
                    planarAxis = "x"
                elif pm.optionVar["mapPlanarMS2RadGrpOptVar"] == 2:
                    planarAxis = "y"
                elif pm.optionVar["mapPlanarMS2RadGrpOptVar"] == 3:
                    planarAxis = "z"
                elif pm.optionVar["mapPlanarMS2RadGrpOptVar"] == 4:
                    planarAxis = "c"

        # Create meshFace group -list
        meshFaceGrpList = mappingCreateFaceGrpList()
        
        # Start projecting - one meshFaceGrp at a time
        for meshFaceGrp in meshFaceGrpList:
    
            # Custom settings
            if pm.optionVar["mapPlanarMethodOptVar"] == 1:     
            
                # Custom UV set name
                if pm.optionVar["mapPlanarSetBoxOptVar"] == True:
                    pm.polyProjection(
                        meshFaceGrp,
                        constructionHistory=True,
                        createNewMap=pm.optionVar["mapPlanarSetBoxOptVar"],
                        insertBeforeDeformers=pm.optionVar["mapPlanarMS2BoxOptVar"],
                        keepImageRatio=pm.optionVar["mapPlanarMS1BoxOptVar"],
                        mapDirection=planarAxis,
                        type="planar",
                        uvSetName=pm.optionVar["mapPlanarSetOptVar"],
                    )
                else: # No custom UV set name
                    pm.polyProjection(
                        meshFaceGrp,
                        constructionHistory=True,
                        createNewMap=pm.optionVar["mapPlanarSetBoxOptVar"],
                        insertBeforeDeformers=pm.optionVar["mapPlanarMS2BoxOptVar"],
                        keepImageRatio=pm.optionVar["mapPlanarMS1BoxOptVar"],
                        mapDirection=planarAxis,
                        type="planar",
                    )
                    
                # Set projection node attributes
                mappingSetAttr(meshFaceGrp, "plane")

            # Quick settings
            else:               
                pm.polyProjection(
                    meshFaceGrp[0],
                    constructionHistory=True,
                    insertBeforeDeformers=True,
                    keepImageRatio=True,
                    mapDirection=planarAxis,
                    type="planar",
                )
                
        # Select original selection
        pm.select(orgSel)
        
        # If the user wants the projection manipulators visible...
        if pm.optionVar["mapPlanarMS3BoxOptVar"] == True:
            for item in projList:
                pm.select(item, add=True)
            pm.setToolTo("ShowManips")    
        

    ## Spherical projection
    elif projection == "sphere":
    
        # Create meshFace group -list
        meshFaceGrpList = mappingCreateFaceGrpList()
        
        # Start projecting - one meshFaceGrp at a time
        for meshFaceGrp in meshFaceGrpList:
    
            # Custom UV set name
            if pm.optionVar["mapSphericalSetBoxOptVar"] == True:
                pm.polyProjection(
                    meshFaceGrp,
                    constructionHistory=True,
                    createNewMap=pm.optionVar["mapSphericalSetBoxOptVar"],
                    insertBeforeDeformers=pm.optionVar["mapSphericalMS1BoxOptVar"],
                    smartFit=True,
                    type="spherical",
                    uvSetName=pm.optionVar["mapSphericalSetOptVar"],
                )
            else: # No custom UV set name
                pm.polyProjection(
                    meshFaceGrp,
                    constructionHistory=True,
                    insertBeforeDeformers=pm.optionVar["mapSphericalMS1BoxOptVar"],
                    smartFit=True,
                    type="spherical",
                )
                
            # Set projection node attributes
            mappingSetAttr(meshFaceGrp, "sphere")

        # Select original selection
        pm.select(orgSel)
        
        # If the user wants the projection manipulators visible...
        if pm.optionVar["mapSphericalMS2BoxOptVar"] == True:
            for item in projList:
                pm.select(item, add=True)
            pm.setToolTo("ShowManips")


    else:
        print("Incorrect projection type specified for core.mapping()")
    
    # Delete window if necessary
    if win != None:
        pm.deleteUI(win)

  
# Match UVs
def matchUVs():

    # Check for valid UV selection
    checkSel("UV")
    
    # Var
    matchTol = pm.optionVar["matchTolOptVar"]
    
    # Store original selection as flattened list
    selUVs = pm.ls(selection=True, flatten=True)
    
    # Get mesh name from component
    mesh = str(selUVs[0])
    mesh = re.findall("([^.]+)[.]", mesh )[0]    
    
    # Count number of UVs
    uvCount = pm.polyEvaluate(uvcoord=True) # All UVs on all affected shells
    uvCountSel = pm.polyEvaluate(uvComponent=True) # UVs on selection only
    
    # Progress window
    pm.progressWindow(
        isInterruptable=True,  
        maxValue=uvCount, 
        progress=0, 
        status="Matching UVs", 
        title="Matching UVs" 
    )
    
    # Loop through every UV in the selection
    counter1 = 0
    while counter1 < uvCountSel:
        
        # Break if cancelled by user
        if pm.progressWindow(query=True, isCancelled=True) == True:
            pm.warning("Interupted by user")
            break
 
        # Update progress window
        pm.progressWindow(
            edit=True,  
            progress=(uvCount - counter1), 
            status="Matching UVs. %s UVs remaining."%counter1 
        )
        
        # Get current UV coords, as specified by the loop counter
        uvCurrent = pm.polyEditUV(selUVs[counter1], query=True)
        
        # And for all UVs on all selected shells...
        counter2 = 0
        while counter2 < uvCount:
            
            # Get full name of this UV
            fullName = mesh + (".map[%s]"%counter2)
            
            # ...and the coords of that UV
            uvCoords = pm.polyEditUV(fullName, query=True)
            
            # Then match if is in range as specified by the tolerance value
            if (uvCoords[0] < (uvCurrent[0] + matchTol) and uvCoords[0] > (uvCurrent[0] - matchTol)):
                if (uvCoords[1] < (uvCurrent[1] + matchTol) and uvCoords[1] > (uvCurrent[1] - matchTol)):
                    pm.polyEditUV(
                        selUVs[counter1],
                        relative=False,
                        uValue=uvCoords[0],
                        vValue=uvCoords[1]
                    )
            counter2 += 1
        counter1 += 1
  
    # Close the progress window
    pm.progressWindow(endProgress=True)
    
    
# Normalize shells
def normalizeShells(action):
    
    # Validate selection
    checkSel("any")
    
    # Store original selection
    selOrg = pm.ls(selection=True)
  
    # Snap to bottom left
    snapShells(6)
    
    # Normalize UV - preserve aspect ratio
    if action == 0:
        pm.polyNormalizeUV(
            normalizeType=1,
            preserveAspectRatio=True
        )
    
    # Normalize UV - DON'T preserve aspect ratio
    elif action == 1:
        pm.polyNormalizeUV(
            normalizeType=1,
            preserveAspectRatio=False
        )
  
    # Normalize U only
    elif action == 3:
    
        # Get bounding box
        uvBox = pm.polyEvaluate(boundingBoxComponent2d=True)
    
        # Normalize
        scaleDist = (1 / uvBox[0][1])
        pm.polyEditUV(
            pivotU=0,
            pivotV=0,
            scaleU=scaleDist,
            scaleV=scaleDist
        )
    
    # Normalize V only
    elif action == 4:
    
        # Get bounding box
        uvBox = pm.polyEvaluate(boundingBoxComponent2d=True)
    
        # Normalize
        scaleDist = (1 / uvBox[1][1])
        pm.polyEditUV(
            pivotU=0,
            pivotV=0,
            scaleU=scaleDist,
            scaleV=scaleDist
        )
    
    else:
        print("Error: Invalid action -flag passed to normalizeShells() - expected 0, 1, 3 or 4")
        
    # Reselect original selection
    pm.select(selOrg)
  
    
# Orient edge
def orientEdge():
    
    ## Internal orientation method
    def orient(coords):
    
        # Calculate arctangent (returns degrees) - round down to 4 decimals
        angleVal = round( calcArctanAngle(coords[0], coords[1]), 4)
        invertVal = 0
        
        # Determine how much to rotate. Arctangent range is -90 to +90 degrees
        if angleVal == 0.0000 or angleVal == 90.0000 or angleVal == -90.0000:
            # Type 0 - No rotation
            angleVal = 0
        
        elif angleVal >= -44.9999 and angleVal <= 44.9999:
            # Type A - Invert
            invertVal = 1
            
        elif angleVal >= 45.0001 and angleVal <= 89.9999:
            # Type B - Subtract angle from 90
            angleVal = 90 - angleVal
            invertVal = 0
            
        elif angleVal <= -45.0001 and angleVal >= -89.9999:
            # Type C - Add 45 degrees to angle and invert
            angleVal = 90 + angleVal
            invertVal = 1
            
        else:
            # Type D - Angle is 45 degrees
            angleVal = 45
            invertVal = 0
            
        if invertVal == 1:
            angleVal = -angleVal
            
        # Convert to uv shell
        pm.polySelectConstraint(
            mode=2,
            shell=True,
        )
        pm.polySelectConstraint(
            border=0,
            mode=0,
            shell=False,
        )
        
        # Calculate bounding box pivot (center point) then rotate
        uvBox = pm.polyEvaluate(boundingBoxComponent2d=True)
        centerU = 0.5 * ( uvBox[0][0] + uvBox[0][1] )
        centerV = 0.5 * ( uvBox[1][0] + uvBox[1][1] )    
        pm.polyEditUV(
            angle=angleVal,
            pivotU=centerU,
            pivotV=centerV,
        )
 
    # Validate selection
    checkSel("edgeUV")
    
    # Store selection
    selOrg = pm.ls(selection=True)
    pm.mel.ConvertSelectionToUVs()
    selUVs = pm.ls(selection=True, flatten=True)
    
    # Single UV selection?
    if len(selUVs) == 1:
        errorCode(13)
  
    # Convert selection to shells -list
    shellList = convertToShell()
    
    # Edit progress window created by convertToShell()
    pm.progressWindow(
        edit=True, 
            maxValue=len(shellList),
    )
    
    # Loop through each shell
    counter = 0
    while len(shellList) > counter:
    
        # Break if cancelled by user
        if pm.progressWindow(query=True, isCancelled=True) == True:
            pm.warning("Interupted by user")
            break
    
        # Update progress window
        pm.progressWindow(
            edit=True,
                progress=(counter + 1),
                status=("Orienting: %s / %s"%( counter+1, len(shellList) ))
        )
    
        # Loop through shell UVs
        shellComps = []
        for uv in selUVs:
        
            # Create shell components -list
            if uv in shellList[counter]:
                shellComps.append(uv)
                
                # As we only need two UVs...
                if len(shellComps) <= 2:
                    continue # Move on to next, eventually breaking out
                 
        # Select shell, run orientation method and up the counter
        pm.select(shellComps)    
        orient(shellComps)
        counter += 1
    
    # Close the progress window and reselect original selection
    pm.progressWindow(endProgress=True)
    pm.select(selOrg)
    
    # Go to edge selection tool if the original selection was an edge
    if pm.filterExpand(selectionMask=32) != [] and pm.filterExpand(selectionMask=32) != None:
        pm.mel.SelectEdgeMask()
    
    
# Orient shells
def orientShells():
    
    # Actual shell orientation method
    def orient():
        
        # Method variables
        iteration = pm.optionVar["orientShellsOptVar"] + 3 # Accuracy
        scans = 8 # How many times the bBox area is calculated
        scanRange = 90.0 # Max rotation
        scanAngle = scanRange / scans
        
        # Get bounding box coordinates and calculate pivots
        uvBox = pm.polyEvaluate(boundingBoxComponent2d=True)
        centerU = 0.5 * ( uvBox[0][0] + uvBox[0][1] )
        centerV = 0.5 * ( uvBox[1][0] + uvBox[1][1] )
        
        # Iteration loop       
        for x in xrange(1, iteration):
            angleBest = 0 # Reset
            
            # Calculate area of the bounding box
            uvBox = pm.polyEvaluate(boundingBoxComponent2d=True)
            uvBoxOld = (uvBox[0][1] - uvBox[0][0]) + (uvBox[1][1] - uvBox[1][0])
            
            # Rotate shell
            for y in xrange(1, scans):
                pm.polyEditUV(
                    angle=scanAngle,
                    pivotU=centerU,
                    pivotV=centerV
                )
                
                # Calculate area of the NEW bounding box
                uvBox = pm.polyEvaluate(boundingBoxComponent2d=True)
                uvBoxNew = (uvBox[0][1] - uvBox[0][0]) + (uvBox[1][1] - uvBox[1][0])
                
                # If the new bounds have a smaller area than the old...
                if uvBoxNew < uvBoxOld:
                    uvBoxOld = uvBoxNew
                
                    # Rotation angle FOR this position
                    angleBest = (y * scanAngle)
                    
            # Angle to ROTATE for this position
            angleCorrection = angleBest - ( scanAngle * (scans-1) )
                
            # Narrow down scan
            if x != iteration:
                scanRange = scanAngle
                scanAngle = scanRange / scans
                angleCorrection -= scanRange * 0.5
                
            # Actual shell rotation
            pm.polyEditUV(
                angle=angleCorrection,
                pivotU=centerU,
                pivotV=centerV
            )

            
    ## End of the orientation internal method
        
    # Removes the "WARNING: some items cannot be moved in the 3d view" -error message
    pm.mel.eval("setToolTo $gSelect")
    
    # Validate selection
    checkSel("UV")
    
    # Store selection
    selOrg = pm.ls(selection=True)
    
    # Convert to individual shells, store as list
    shellList = convertToShell()
    
    # Edit progress window created by convertToShell()
    pm.progressWindow(
        edit=True, 
            maxValue=len(shellList),
    )
    
    # Loop through each shell
    counter = 0
    while len(shellList) > counter:
        
        # Break if cancelled by user
        if pm.progressWindow(query=True, isCancelled=True) == True:
            pm.warning("Interupted by user")
            break
        
        # Update progress window
        pm.progressWindow(
            edit=True,
                progress=(counter + 1),
                status=("Orienting: %s / %s"%( counter+1, len(shellList) ))
        )
        
        # Select shell, run orientation method and up the counter
        pm.select( shellList[counter], replace=True )
        orient()
        counter += 1
        
    # Close the progress window and reselect original selection
    pm.progressWindow(endProgress=True)
    pm.select(selOrg, replace=True)
 
    
# Rounds a value to the power of two
def powerOfTwo(val):
    
    nextSize = 1
    newSize = 0
    prevSize = 0
    
    while nextSize < val:
        prevSize = nextSize
        nextSize = nextSize * 2
    
    if (val - prevSize) < (nextSize - val):
        newSize = prevSize
    else:
        newSize = nextSize
        
    return newSize
    
    
# Propagate UV set
def propagateSets(scrollList):

    # Selection check
    checkSel("mesh")
    
    # Get long names (mesh and shape node) from selection
    objects = pm.listRelatives(
        shapes=True,
        noIntermediate=True,
        fullPath=True,
        type="mesh",
    )
    if objects == None or objects == []:
        objects = pm.ls(selection=True, type="mesh")
    if objects == None or objects == []:
        objects = pm.listRelatives(
            parent=True,
            noIntermediate=True,
            fullPath=True, 
            type="mesh"
    )
    
    # Can't propagate with a single mesh only
    if len(objects) < 2:
        errorCode(12)

    # Get active UV set
    setName = pm.polyUVSet(
        objects[0],
        currentUVSet=True,
        query=True,
    )
    
    # Go through each set/object and propagate accordingly
    for mesh in objects:    
        baseSetName = str(setName[0])
        perInstance = False
        setExists = False
        
        # If the name ends with the suffix (*) where * is a digit between 0-99...
        if re.match("^[a-z]+?\([0-9]{1,2}\)$", baseSetName, re.IGNORECASE):
        
            # ...remove said prefix from the baseSetName, set bool
            baseSetName = re.findall("([^.]+)[(]", baseSetName, re.IGNORECASE )[0]
            perInstance = True

        
        # Get all sets from mesh object and check for a match
        uvSets = pm.polyUVSet(
            mesh,
            allUVSets=True,
            perInstance=True,
            query=True,
        )        
        if baseSetName in uvSets:
            setExists = True
        
        # If we have a per-instance case
        if perInstance == True:
        
            # Set exists...
            if setExists == True:
            
                # ..but does it exist on this instance?
                perInstanceExists = pm.polyUVSet(
                    mesh,
                    perInstance=True,
                    query=True,
                    uvSet=baseSetName,
                )

                if perInstanceExists == None or perInstanceExists == []:
                    meshParent = pm.listRelatives(
                        mesh,
                        parent=True, 
                        path=True,
                    )
                    newSet = pm.polyUVSet(
                        mesh,
                        create=True,
                        perInstance=True,
                        uvSet=baseSetName,                
                    )
                    pm.polyUVSet(
                        meshParent[0],
                        currentUVSet=True,
                        uvSet=newSet[0],
                    )
            
            # Set doesn't exist at all   
            else: 
                pm.polyUVSet(
                    mesh, 
                    create=True,
                    perInstance=True,
                    uvSet=baseSetName
                )
                pm.polyUVSet(
                    mesh,
                    currentUVSet=True,
                    uvSet=baseSetName,
                ) 
 
        # Set does not exist and is not per-instance
        elif (setExists == False): 

            pm.polyUVSet(
                mesh,
                create=True,
                uvSet=baseSetName,            
            )
            pm.polyUVSet(
                mesh,
                currentUVSet=True,
                uvSet=baseSetName,            
            )        

        else: # Set exists already, do nothing!
            pass

    # Update the editor
    updateUVSetEditor(scrollList)
    
        
# Method for randomizing a single shell
def randomizeShell():
    
    # optVars to short notation vars
    boxTU = pm.optionVar["randTBox1OptVar"]
    boxTV = pm.optionVar["randTBox2OptVar"]
    boxRCW = pm.optionVar["randRBox1OptVar"]
    boxRCCW = pm.optionVar["randRBox2OptVar"]
    boxSU = pm.optionVar["randSBox1OptVar"]
    boxSD = pm.optionVar["randSBox2OptVar"]
    
    # Translation
    if boxTU == 1 or boxTV == 1:
        valT = pm.optionVar["randTOptVar"]
        
        # Along U
        if boxTU == 1:
            translateVal = random.uniform(-valT, valT)
            pm.polyEditUV(uValue=translateVal)
        
        # Along V
        if boxTV == 1:
            translateVal = random.uniform(-valT, valT)
            pm.polyEditUV(vValue=translateVal)

        
    # Rotation
    if boxRCW == 1 or boxRCCW == 1:
        valR = pm.optionVar["randROptVar"]
    
        # Both directions
        if boxRCW and boxRCCW:
            rotateVal = random.uniform(-valR, valR)
            updateManipCoords()
            manipCoords = pm.optionVar["manipCoordsOptVar"]
            pm.polyEditUV( pivotU=manipCoords[0], pivotV=manipCoords[1], angle=rotateVal )
    
        # Clockwise
        elif boxRCW == 1:
            rotateVal = random.uniform(0, valR)
            updateManipCoords()
            manipCoords = pm.optionVar["manipCoordsOptVar"]
            pm.polyEditUV( pivotU=manipCoords[0], pivotV=manipCoords[1], angle=rotateVal )
        
        # Counter-clockwise
        elif boxRCCW == 1:
            rotateVal = random.uniform(-valR, 0)
            updateManipCoords()
            manipCoords = pm.optionVar["manipCoordsOptVar"]
            pm.polyEditUV( pivotU=manipCoords[0], pivotV=manipCoords[1], angle=rotateVal )

    
    # Scaling
    if boxSU == 1 or boxSD == 1:
        valS = pm.optionVar["randSOptVar"]
        
        # Both up and down
        if boxSU == 1 and boxSD == 1:
        
            # Convert percentage to decimal number
            tempUp = (valS/100) + 1
            tempDown = 1 - (valS/100)
            
            scaleVal = random.uniform(tempDown, tempUp)
            updateManipCoords()
            manipCoords = pm.optionVar["manipCoordsOptVar"]
            pm.polyEditUV( pivotU=manipCoords[0], pivotV=manipCoords[1], scaleU=scaleVal, scaleV=scaleVal )
        
        # Up
        elif boxSU == 1:
        
            # Convert percentage to decimal number
            tempUp = (valS/100) + 1
            
            scaleVal = random.uniform(1.0, tempUp)
            updateManipCoords()
            manipCoords = pm.optionVar["manipCoordsOptVar"]
            pm.polyEditUV( pivotU=manipCoords[0], pivotV=manipCoords[1], scaleU=scaleVal, scaleV=scaleVal )
            
        # Down
        elif boxSD == 1:
        
            # Convert percentage to decimal number
            tempDown = 1 - (valS/100)
            
            scaleVal = random.uniform(tempDown, 1.0)
            updateManipCoords()
            manipCoords = pm.optionVar["manipCoordsOptVar"]
            pm.polyEditUV( pivotU=manipCoords[0], pivotV=manipCoords[1], scaleU=scaleVal, scaleV=scaleVal )
    

# Randomize UVs
def randomizeUVs():

    # Removes the "WARNING: some items cannot be moved in the 3d view" -error message
    pm.mel.eval("setToolTo $gSelect")
    
    # Check the selection
    checkSel("UV")
    
    # Get the selection
    selOrg = pm.ls(selection=True)
    
    # Convert the selection to individual shells; store in a list
    selShells = convertToShell()
    
    # Count shells
    countShells = len(selShells)
    
    # Edit the progress window created by convertToShell
    pm.progressWindow(
        edit=True,
        maxValue=countShells
    )
    
    progCount = 0
    
    # Randomization loop
    for item in selShells:
    
        progCount += 1
        
        # Break if cancelled by user
        if pm.progressWindow(query=True, isCancelled=True) == True:
            pm.warning("Interupted by user\n")
            break
        
        # Edit the progress window
        pm.progressWindow(
            edit=True,
            progress=(progCount),
            status=("Randomizing shell %s / %s")%(progCount, countShells)
        )
        
        # Select shell and run randomize
        pm.select(selShells[progCount-1], replace=True) # WARN: eval at runtime?
        pm.mel.eval("setToolTo $gMove")
        randomizeShell()
        
    # End progress window and reselect original selection
    pm.progressWindow(endProgress=True)
    pm.select(selOrg, replace=True)

    
# Relax UVs        
def relaxUVs(win=None):

    # Vars
    pluginLoaded = False
    methodVar = 1
    
    # Check for Unfold3D plugin - correct optVar if it isnt
    if pm.pluginInfo("Unfold3D", loaded=True, query=True) == True:
        pluginLoaded = True
    
    # Manage optVars
    if pm.optionVar["relaxEdgeOptVar"] == 1:
        relaxType = "uniform"
    else:
        relaxType = "harmonic"

    if pm.optionVar["relaxPinTypeOptVar"] == 1:
        pinTypeSel = True
        pinTypeUnsel = False
    else:
        pinTypeSel = False
        pinTypeUnsel = True
    
    if pluginLoaded == True:
        methodVar = pm.optionVar["relaxMethodOptVar"]
    else:
        if pm.optionVar["relaxMethodOptVar"] == 1:
            methodVar = 2
        elif pm.optionVar["relaxMethodOptVar"] == 2:
            methodVar = 3
    
    # Validate selection
    checkSel("UV")
    
    # Store selection
    orgSel = pm.ls(selection=True, flatten=True)
    
    # Convert to individual shells, store as list
    shellList = convertToShell() 

    # Begin relaxing
    for item in shellList:
        relaxSel = []
        
        # Get UVs from whole shell (item) and compare to original selection
        for uv in item:
            if uv in orgSel:
                relaxSel.append(uv)
    
        # Method: Unfold3D
        if methodVar == 1:        
            pm.Unfold3D(
                relaxSel, 
                borderintersection=pm.optionVar["relaxBorderOptVar"],            
                iterations=pm.optionVar["relaxItrOptVar"],
                mapsize=int(pm.optionVar["relaxSizeOptVar"]),            
                optimize=True,  
                power=pm.optionVar["relaxPowerOptVar"],
                roomspace=pm.optionVar["relaxRoomOptVar"],
                surfangle=pm.optionVar["relaxAngleOptVar"],
                triangleflip=pm.optionVar["relaxFlipsOptVar"],            
            )        
            
        # Method: Legacy
        elif methodVar == 2:
            pm.untangleUV(
                relaxSel,
                relax=relaxType,
                pinBorder=pm.optionVar["relaxPinBorderOptVar"], 
                pinSelected=pinTypeSel,
                pinUnselected=pinTypeUnsel,
                maxRelaxIterations=pm.optionVar["relaxMaxItrOptVar"], 
            )
     
        # Method: Quick
        elif methodVar == 3:
            pm.untangleUV(
                relaxSel,
                relax=relaxType,
                pinBorder=False,
                pinSelected=False,
                pinUnselected=True,
                relaxTolerance=0.0,
                maxRelaxIterations=10,
            )
        
    # Reselect original selection
    pm.select(orgSel)

    # Close relax window
    if win != None:
        pm.deleteUI( win )


# Rename UV set
def renameSet(scrollList, renameField, renameUI):
    
    # Get UV Set names
    nameNew = renameField.getText()
    nameOld = scrollList.getSelectItem()
    
    # Rename UV Set and set it to the current set
    pm.polyUVSet(
        newUVSet=nameNew,
        rename=True,
        uvSet=str(nameOld[0]),
    )
    pm.polyUVSet(
        currentUVSet=True,
        uvSet=nameNew
    )
    
    # Update UV Set list
    updateUVSetEditor(scrollList)
    
    # Select the correct set
    scrollList.setSelectItem(nameNew)
    
    # Close down the rename UV Set window. Eval at runtime.
    pm.evalDeferred(lambda: pm.deleteUI( renameUI ))
    

# Rotates a UV selectio
def rotateUVs(dir):
    
    # Update coords and read from optVars
    updateManipCoords()
    manipCoords = pm.optionVar["manipCoordsOptVar"]
    manipAmt = pm.optionVar["manipAmtOptVar"]
    
    # Rotate
    if dir == "90":
        pm.polyEditUV(
            angle=90,
            pivotU=manipCoords[0],
            pivotV=manipCoords[1]         
        )        
    if dir == "-90":
        pm.polyEditUV(
            angle = -90,
            pivotU=manipCoords[0],
            pivotV=manipCoords[1]         
        )    
    if dir == "180":
        pm.polyEditUV(
            angle=180,
            pivotU=manipCoords[0],
            pivotV=manipCoords[1]          
        )
    if dir == "CW":
        pm.polyEditUV(
            angle=(manipAmt * -1),
            pivotU=manipCoords[0],
            pivotV=manipCoords[1]        
        )        
    if dir == "CCW":
        pm.polyEditUV(
            angle=manipAmt,
            pivotU=manipCoords[0],
            pivotV=manipCoords[1]         
        )
    

# Scales a UV selection
def scaleUVs(scaleType):

    manipAmt = pm.optionVar["manipAmtOptVar"]

    # Scale as group
    if scaleType == "U" or scaleType == "V" or scaleType == "UV":
    
        # Update coords
        updateManipCoords()
        manipCoords = pm.optionVar["manipCoordsOptVar"]
        
        # Scale
        if scaleType == "U":   
            pm.polyEditUV(
            pivotU=manipCoords[0],
            pivotV=manipCoords[1],
            scaleU=manipAmt
            )        
        if scaleType == "V":
            pm.polyEditUV(
            pivotU=manipCoords[0],
            pivotV=manipCoords[1],
            scaleV=manipAmt
            )        
        if scaleType == "UV":
            pm.polyEditUV(
            pivotU=manipCoords[0],
            pivotV=manipCoords[1],
            scaleU=manipAmt,
            scaleV=manipAmt
            )
            
    # Scale every shell
    else:
       
        # Save original selection and create shell list
        selOrg = pm.ls(selection=True)
        shellList = convertToShell()
        
        # Select shell, update manip coords, then scale
        for shell in shellList:
            pm.select(shell)
            updateManipCoords()
            manipCoords = pm.optionVar["manipCoordsOptVar"]
            
            if scaleType == "relU":
                pm.polyEditUV(
                pivotU=manipCoords[0],
                pivotV=manipCoords[1],
                scaleU=manipAmt
                ) 
            
            elif scaleType == "relV":
                pm.polyEditUV(
                pivotU=manipCoords[0],
                pivotV=manipCoords[1],
                scaleV=manipAmt
                ) 
            
            else: # scaleType == "relUV"
                pm.polyEditUV(
                pivotU=manipCoords[0],
                pivotV=manipCoords[1],
                scaleU=manipAmt,
                scaleV=manipAmt
                )
        
        # Reselect original selection
        pm.select(selOrg)
        
        
# Select unmapped faces
def selectUnmapped():
    pm.polySelectConstraint( mode=3, type=0x0008, textured=2 )
    
    
# Set the selected UV set to the current
def setCurrent(scrollList):

    # Get UV sets from scrollList and change currentUVSet
    setCurrent = scrollList.getSelectItem()
    pm.polyUVSet(
        currentUVSet=True,
        uvSet=str(setCurrent[0])
    )


# Method for setting working units via the setWorkingUnits -UI
def setUnits(menu, deleteWin):
    newUnit = menu.getValue() # Read value
    pm.currentUnit(linear=newUnit) # Set working units

    # Reload grid
    currentGridSpacing = pm.grid(query=True, spacing=True)
    currentGridSize = pm.grid(query=True, size=True)
    if currentGridSize < 1.0:
        currentGridSize = 1.0
    pm.grid(spacing=currentGridSpacing, size=currentGridSize)
    
    pm.deleteUI(deleteWin)
  
  
# Set texel density
def setTD(field1, field2):
    
    # Validate selection
    checkSel("meshUV")
    
    # Read TD and map size values from fields
    tdVal = pm.optionVar["tdOptVar"] = field1.getValue1()
    mapVal = pm.optionVar["tdSizeOptVar"] = field2.getValue1()
    
    # Calculate scalar
    scalar = tdVal / mapVal
    
    # Get selection
    selection = pm.ls(flatten=True, selection=True)
    
    # Run unfold on every shell
    for item in selection:
        pm.unfold(
            item,
            globalBlend=0, 
            globalMethodBlend=1, 
            iterations=0, 
            optimizeAxis=0, 
            pinSelected=0, 
            pinUvBorder=0, 
            scale=scalar,
            stoppingThreshold=0.001, 
            useScale=True,
        )
        
    # Re-center the manipulator
    pm.mel.eval("setToolTo $gMove")
  
  
# Snap point A to point B
def snapPoints(snapSel):
    
    # Validate selection (only two UVs)
    checkSel("UV2")
    
    # Store original selection as flattened list
    selOrg = pm.ls(selection=True, flatten=True)
    
    # Get U and V distances
    uvBox = pm.polyEvaluate(boundingBoxComponent2d=True)
    distU = abs(uvBox[0][1] - uvBox[0][0])
    distV = abs(uvBox[1][1] - uvBox[1][0])
    
    # Store coordinate info
    pointA = pm.polyEditUV(selOrg[0], query=True)
    pointB = pm.polyEditUV(selOrg[1], query=True)
    
    # Snap A to B
    if snapSel == 0:
    
        # Shell position correction
        if pointA[1] > pointB[1]:
            distV = -distV
        if pointA[0] > pointB[0]:
            distU = -distU
        
        # Select UV from first shell
        pm.select(selOrg[0])
    
    # Snap B to A 
    elif snapSel == 1:
    
        # Shell position correction
        if pointA[0] < pointB[0]:
            distU = -distU
        if pointA[1] < pointB[1]:
            distV = -distV
        
        # Select UV from second shell
        pm.select(selOrg[1])
        
    else: # Error
        print("Error: Invalid snapSel -flag passed to snapPointS() - expected 0 or 1")
      
    # Expand selection to entire shell, then move the shell
    pm.polySelectConstraint(
        type=0x0010,
        shell=False,
        border=True,
        mode=2
    )
    pm.polySelectConstraint(
        type=0x0010,
        shell=True,
        border=False,
        mode=0
    )
    pm.polySelectConstraint(
        shell=False,
        border=False,
        mode=0
    )    
    pm.polyEditUV(
        uValue=distU, 
        vValue=distV
    )
  
  
# Snap shells
def snapShells(dir):
    
    # Validate UV selection
    checkSel("UV")

    # Get bounding box
    uvBox = pm.polyEvaluate(boundingBoxComponent2d=True)
    
    # Calc distances
    distCenterU = 0.5 - (uvBox[0][0] + uvBox[0][1]) * 0.5
    distCenterV = 0.5 - (uvBox[1][0] + uvBox[1][1]) * 0.5
    distRight = 1 - uvBox[0][1]
    distLeft = -uvBox[0][0]
    distBottom = -uvBox[1][0]
    distTop = 1 - uvBox[1][1]
    
    # Center
    if dir == 0:
        pm.polyEditUV(
            uValue=distCenterU,
            vValue=distCenterV
        )
    
    # Top left
    elif dir == 1:
        pm.polyEditUV(
            uValue=distLeft,
            vValue=distTop
        )
    
    # Top
    elif dir == 2:
        pm.polyEditUV(
            uValue=distCenterU,
            vValue=distTop
        )
    
    # Top right
    elif dir == 3:
        pm.polyEditUV(
            uValue=distRight,
            vValue=distTop
        )
    
    # Left
    elif dir == 4:
        pm.polyEditUV(
            uValue=distLeft,
            vValue=distCenterV
        )
    
    # Right
    elif dir == 5:
        pm.polyEditUV(
            uValue=distRight,
            vValue=distCenterV
        )
    
    # Bottom left
    elif dir == 6:
        pm.polyEditUV(
            uValue=distLeft,
            vValue=distBottom
        )
    
    # Bottom
    elif dir == 7:
        pm.polyEditUV(
            uValue=distCenterU,
            vValue=distBottom
        )
    
    # Bottom right
    elif dir == 8:
        pm.polyEditUV(
            uValue=distRight,
            vValue=distBottom
        )
        
    # Activate the move tool
    pm.mel.eval("setToolTo $gMove")

  
# Spread out shells
def spreadOutShells():
    
    # Validate selection
    checkSel("any")
    
    # Save original selection
    selOrg = pm.ls(selection=True)
    
    # Go to mesh selection mode
    pm.mel.eval("toggleSelMode")
    pm.selectMode(object=True)
    
    # Spread out for every shell...
    meshList = pm.filterExpand(selectionMask=12) # Convert selection to mesh    
    for item in meshList:

        # Select mesh, convert selection to UVs
        pm.select(item)
        selOrgUV = pm.polyListComponentConversion(toUV=True)
        pm.select(selOrgUV)
        
        # Calculate center point from UV bounding box
        uvBox = pm.polyEvaluate(boundingBoxComponent2d=True)
        oldCenterU = 0.5 * ( uvBox[0][0] + uvBox[0][1] )
        oldCenterV = 0.5 * ( uvBox[1][0] + uvBox[1][1] )
        
        # Layout/(order) UV shells
        pm.polyLayoutUV(
            flipReversed=True,
            layout=2,
            layoutMethod=1,
            percentageSpace=0.2,
            rotateForBestFit=True,
            scale=0,
            separate=False,
        )
        
        # Calculate new center point from UV bounding box
        uvBox = pm.polyEvaluate(boundingBoxComponent2d=True)
        newCenterU = 0.5 * ( uvBox[0][0] + uvBox[0][1] )
        newCenterV = 0.5 * ( uvBox[1][0] + uvBox[1][1] )
        
        # Get proper translation distance, then move back the shell package
        distU = oldCenterU - newCenterU
        distV = oldCenterV - newCenterV
        
        if oldCenterU <= newCenterU:        
            pm.polyEditUV(
                uValue=distU,
                vValue=distV
            )

        else:
            pm.polyEditUV(
                uValue=distU,
                vValue=distV
            )
        
    # Select the original selection
    pm.select(selOrg)

    
# UV Snapshot: Take snapshot
def ssTakeShot(win=None):
    
    # Method vars
    imfExt = ".iff"
    imfKey = "iff"
    
    # Check for valid mesh selection
    checkSel("mesh")
  
    # Get file format from control, insert into optVar
    format = pm.optionVar["shotUVformatOptVar"]
    
    # Get ff names (keyword and extensions) if OS is macintosh
    if pm.about(macOS=True) == True:
        extList = ["iff", "jpg", "pntg", "ps", "png", "pict", "qtif", "sgi", "tga", "tif", "bmp"]
        imfKey = extList[format-1]
        imfExt = "." + extList[format-1]
        
    else: # Else get for Windows        
        if format != "Maya IFF":
            imfKey = pm.imfPlugins(format, query=True, keyword=True)
            imfExt = pm.imfPlugins(format, query=True, extension=True)
    
    # Read optVars, store in convenient vars
    rgb = pm.optionVar["shotUVcolorOptVar"]
    sizeX = pm.optionVar["shotUVxSizeOptVar"]
    sizeY = pm.optionVar["shotUVySizeOptVar"]
    
    # Check if file path is blank - execution is halted
    path = pm.optionVar["shotUVpathOptVar"]
    if path == "":
        errorCode(10)
    
    # Correct the file path if the user left the file extension blank in the file browser
    # make a regex - make sure that path ends with imfExt
    if not path.endswith(imfExt):
        path = path + imfExt

    # Check if file already exists
    if os.path.isfile(path) == True:
        
        # Warn the user about it
        result = pm.confirmDialog(
            button=["Yes", "Cancel"],
            cancelButton="Cancel",
            defaultButton="Cancel",
            dismissString="Cancel",
            message="File exists. Overwrite?", 
            # parent=win, No window is active when running ssTakeShot() standalone 
        )
        
    # Double all the backslashes in case we have an NT-like path
    path = path.replace("\\", "\\\\")
    
    # Custom range: Read radioButton from radioCollection and set optVar
    if pm.optionVar["shotUVrangeOptVar"] == 2:
    
        # Do the xform
        rangeType = pm.optionVar["shotUVtypeOptVar"]
        
        if rangeType == 1:
            ssXform(0)
        
        elif rangeType == 2:
            ssXform(2)
        
        elif rangeType == 3:
            ssXform(4)
        
        elif rangeType == 4:
            ssXform(6)
        
        elif rangeType == 5:
            ssXform(8)
        
        elif rangeType == 6:
            ssXform(10)    

    # Run snapshot command
    pm.uvSnapshot(
        antiAliased=pm.optionVar["shotUVaaOptVar"],
        entireUVRange=False,
        fileFormat=imfKey,
        name=path,
        overwrite=True,
        redColor=(rgb[0] * 255),
        greenColor=(rgb[1] * 255),
        blueColor=(rgb[2] * 255),
        xResolution=sizeX,
        yResolution=sizeY,
    )
    
    # Custom range: Then move back shells to original position
    if pm.optionVar["shotUVrangeOptVar"] == 2:
    
        # Do the xform
        rangeType = pm.optionVar["shotUVtypeOptVar"]
        
        if rangeType == 1:
            ssXform(1)
        
        elif rangeType == 2:
            ssXform(3)
        
        elif rangeType == 3:
            ssXform(5)
        
        elif rangeType == 4:
            ssXform(7)
        
        elif rangeType == 5:
            ssXform(9)
        
        elif rangeType == 6:
            ssXform(11)  
            
    # Delete window if necessary
    if win != None:
        pm.deleteUI(win)
        
        
# UV Snapshot: Transforms shells into 0->1 range
def ssXform(action):

    # Convert mesh to UV selection and store in list
    selOrg = pm.ls(selection=True)
    selOrgUVs = pm.polyListComponentConversion(toUV=True)
    
    # Transformation switch below
    
    # Lying rectangle
    if action == 0:
        pm.polyEditUV(
            selOrgUVs, 
            pivotU=0,
            pivotV=0,
            scaleV=2
        )
    
    # Lying rectangle - undo
    elif action == 1:
        pm.polyEditUV(
            selOrgUVs, 
            pivotU=0,
            pivotV=0,
            scaleV=0.5
        )
    
    # Standing rectangle
    elif action == 2:
        pm.polyEditUV(
            selOrgUVs, 
            pivotU=0,
            pivotV=0,
            scaleU=2
        )
    
    # Standing rectangle - undo
    elif action == 3:
        pm.polyEditUV(
            selOrgUVs, 
            pivotU=0,
            pivotV=0,
            scaleU=0.5
        )
    
    # -1 to 1
    elif action == 4:
        pm.polyEditUV(
            selOrgUVs, 
            pivotU=1,
            pivotV=1,
            scaleU=0.5,
            scaleV=0.5
        )
    
    # -1 to 1 - undo
    elif action == 5:
        pm.polyEditUV(
            selOrgUVs, 
            pivotU=1,
            pivotV=1,
            scaleU=2,
            scaleV=2
        )
    
    # Second quadrant
    elif action == 6:
        pm.polyEditUV(
            selOrgUVs, 
            pivotU=1,
            pivotV=1,
            uValue=1
        )
    
    # Second quadrant - undo
    elif action == 7:
        pm.polyEditUV(
            selOrgUVs, 
            pivotU=1,
            pivotV=1,
            uValue=-1
        )
    
    # Third quadrant
    elif action == 8:
        pm.polyEditUV(
            selOrgUVs, 
            pivotU=1,
            pivotV=1,
            uValue=1,
            vValue=1
        )
    
    # Third quadrant - undo
    elif action == 9:
        pm.polyEditUV(
            selOrgUVs, 
            pivotU=1,
            pivotV=1,
            uValue=-1,
            vValue=-1
        )
    
    # Fourth quadrant
    elif action == 10:
        pm.polyEditUV(
            selOrgUVs, 
            pivotU=1,
            pivotV=1,
            vValue=1
        )
    
    # Fourth quadrant - undo
    elif action == 11:
        pm.polyEditUV(
            selOrgUVs, 
            pivotU=1,
            pivotV=1,
            vValue=-1
        )
   
   
# Stack shells
def stackShells():

    # Validate selection
    checkSel("UV")
    
    selOrg = pm.ls(selection=True, flatten=False)
    
    # Removes the "WARNING: some items cannot be moved in the 3d view" -error message
    pm.mel.eval("setToolTo $gMove")
    
    # Run shell alignment
    alignShells("uAvg")
    alignShells("vAvg")
    
    # Expand selection to entire shell
    pm.runtime.SelectUVShell()
    

# Stitch edges - moving, rotating and scaling the connected UV shells    
def stitchTogether(order=0):

    # Vars
    uvBool = False
    selUVs = None
    uvEdgeA = []
    uvEdgeB = []

    # Validate selection
    checkSel("stitch")
    
    # Get original selection
    selOrg = pm.ls(selection=True, flatten=True)

    # Check if we have UVs or an edge
    if pm.filterExpand( selectionMask=35 ) != None: # UVs
    
        # Get shared edge
        tempSel = pm.ls(selection=True, flatten=True)
        uvA_edgeList = pm.ls(pm.polyListComponentConversion(selOrg[0], fromUV=True, toEdge=True), flatten=True, long=True)
        uvB_edgeList = pm.ls(pm.polyListComponentConversion(selOrg[1], fromUV=True, toEdge=True), flatten=True, long=True)
        intersection = list(set(uvA_edgeList) & set(uvB_edgeList))
        selUVs = pm.ls(pm.polyListComponentConversion(intersection, fromEdge=True, toUV=True), flatten=True, long=True)
        uvBool = True # UV selection bool
    
    elif pm.filterExpand( selectionMask=32 ) != None: # Edge
        selUVs = pm.ls( pm.polyListComponentConversion(selOrg, fromEdge=True, toUV=True), flatten=True )

    # Get correct uvEdge pairs from the UV selection
    uvEdgePairs = getUVEdgePairs(selUVs)
    if order == 0:
        uvEdgeA = uvEdgePairs[0]
        uvEdgeB = uvEdgePairs[1]
    elif order == 1:
        uvEdgeA = uvEdgePairs[1]
        uvEdgeB = uvEdgePairs[0]
    
    # Create/calc vectors and calc angle, offset and ratio between the uvEdge pairs
    targetP0 = pm.polyEditUV(uvEdgeA[0], query=True)
    targetP1 = pm.polyEditUV(uvEdgeA[1], query=True)
    targetVector = dt.Vector(targetP0[0] - targetP1[0], targetP0[1] - targetP1[1] , 0.0)
    
    sourceP0 = pm.polyEditUV(uvEdgeB[0], query=True)
    sourceP1 = pm.polyEditUV(uvEdgeB[1], query=True)
    sourceVector = dt.Vector(sourceP1[0] - sourceP0[0], sourceP1[1] - sourceP0[1] , 0.0)
    
    offsetVector = dt.Vector(targetP1[0] - sourceP0[0], targetP1[1] - sourceP0[1], 0.0)
    angle = math.degrees(sourceVector.angle(targetVector)) # Returned unsigned angle in degrees
    ratio = targetVector.length() / sourceVector.length()
    temp = (sourceVector.x * targetVector.y) - (sourceVector.y * targetVector.x)
    if temp > 0:
        sign = 1
    elif temp < 0:
        sign = -1
    else:
        sign = 0
    
    # Move, rotate, scale and sew together
    pm.select(uvEdgeB)
    pm.mel.SelectUVShell()
    sourceShell = pm.filterExpand(selectionMask=35, expand=0, fullPath=1)
    pivot = dt.Vector( targetP1[0], targetP1[1] )
    
    # Move
    pm.polyEditUV(
        sourceShell, 
            relative=True, 
            uValue=(offsetVector.x), 
            vValue=(offsetVector.y),
    )

    # Rotate
    pm.polyEditUV(
        sourceShell, 
            angle=(angle * sign),
            pivotU=(pivot.x), 
            pivotV=(pivot.y),
            relative=True, 
    ) 

    # Scale
    pm.polyEditUV(
        sourceShell, 
            pivotU=(pivot.x),
            pivotV=(pivot.y),
            relative=True, 
            scaleU=ratio,
            scaleV=ratio,
    )
    
    # Sew
    pm.select(uvEdgeA)
    pm.select(uvEdgeB, add=True)
    pm.mel.ConvertSelectionToContainedEdges()
    pm.polyMapSewMove()    
    

# Straighten shell
def strShell():
    
    # Validate selection
    checkSel("edgeUV")
    
    # Store original selection in various formats
    selOrg = pm.ls(selection=True)
    pm.select( pm.polyListComponentConversion(toUV=True) ) # selOrg as UVs
    selOrgUVs = pm.ls(selection=True, flatten=True) # selOrg as UVs (flattened)
    
    # Check if selection spans multiple shells
    checkSel("multi")
    
    # Get border UVs selection
    selBorderUVs = pm.polySelectConstraint(
        border=1, 
        mode=2, 
        shell=0, 
        type=0x0010
    )
    pm.polySelectConstraint(disable=True)
    selBorderUVs = pm.ls(selection=True, flatten=True)
    
    # Loops for counting border UVs in the original UV selection
    countUV = 0
    counter1 = 0

    while counter1 < len(selOrgUVs):
        counter2 = 0
        
        # Check for match against every border UV - count matching UVs
        while counter2 < len(selBorderUVs):
            if selOrgUVs[counter1] == selBorderUVs[counter2]:
                countUV += 1
            counter2 += 1    
        counter1 += 1 
    
    # Border edge UV count collected. Select original UV selection
    pm.select(selOrgUVs)
    
    # Selection contains only border UVs
    if len(selOrgUVs) == countUV:

        # Straighten map border
        pm.polyStraightenUVBorder(
            blendOriginal=0.0,
            curvature=0.0,
            gapTolerance=5,
            preserveLength=1.0
        )
        
        # Unfold unselected UVs
        unfoldUVs("unselected")
    
    # Selection contains two border UVs
    elif countUV == 2:
        
        # Convert to contained edges, cut, convert back, straighten
        pm.select( pm.polyListComponentConversion(toEdge=True, internal=True) )
        pm.polyMapCut()
        pm.select( pm.polyListComponentConversion(toUV=True) )
        pm.polyStraightenUVBorder(
            blendOriginal=0.0,
            curvature=0.0,
            gapTolerance=5,
            preserveLength=1.0
        )
 
        # Convert to contained edges, sew, convert back    
        pm.select( pm.polyListComponentConversion(toEdge=True, internal=True) )
        pm.polyMapSewMove(
            constructionHistory=True,
            limitPieceSize=False,
            numberFaces=10
        )    
        pm.select(selOrgUVs) # Because the sew command deselects
        
        # Unfold unselected UVs
        unfoldUVs("unselected")
        
    # Faulty UV selection. This one should never execute actually
    else:
        errorCode(7)
    
    # Time to straighten the shell!
    # Select two random UVs. Since they are all on a line now, it doesn't matter
    pm.select(selOrgUVs[0])
    pm.select(selOrgUVs[1], add=True)
    
    # Orient straight
    orientEdge()
    
    # Find shell direction by calculating arctangent. It's either 0 or 90
    angleVal = int( round( calcArctanAngle(selOrgUVs[0], selOrgUVs[1]) ) )
    
    # Unfold
    if angleVal == 0:
        unfoldUVs("U")
    else:
        unfoldUVs("V")
    
    pm.select(selOrg)

    
# Straighten UV selection
def strUVs():

    # Check the selection
    checkSel("UV")

    # Store selection
    selOrg = pm.ls(selection=True, flatten=True)
    
    # Create shell list
    shellList = convertToShell()
    
    # Read optionVars
    rotAngleTol = pm.optionVar["strUVsAngleOptVar"]
    strType = pm.optionVar["strUVsTypeOptVar"]
    
    # Perform straighten for every individual shell
    for shell in shellList:
    
        edgeList = []
        uvEdgeListU = []
        uvEdgeListV = []
        shellUVList = []
        
        # Collect the shell UVs into a list
        for uv in shell:
            if uv not in shellUVList:
                shellUVList.append(uv)
    
        # Convert selection to edges
        if len(selOrg) < len(shellUVList):
            edgeList = pm.polyListComponentConversion(selOrg, toEdge=True)
        else:
            edgeList = pm.polyListComponentConversion(shellUVList, toEdge=True)
        
        # Make sure the list is flattened
        edgeList = pm.ls(edgeList, flatten=True)
        
        # Divide edges into two straighten groups (horizontal and vertical)
        for edge in edgeList:
        
            # Convert edge to UVs and flatten
            edgeToUV = pm.polyListComponentConversion(edge, toUV=True)
            edgeToUV = pm.ls(edgeToUV, flatten=True)
            
            # Check if the UVs of the uvEdge belong to selOrg AND the current UV shell
            uvEdge = []
            for uvCoord in edgeToUV:
                
                # Add UV to list - Need this because an edge can be on two shells
                if uvCoord in selOrg and uvCoord in shellUVList:
                    uvEdge.insert(0, uvCoord)
            
            # Check uv count in uvEdge. 1 = single coord, 2 = uvEdge, 4 = shared edge
            if len(uvEdge) == 4:
                uvEdgePairs = getUVEdgePairs(edgeToUV)
            elif len(uvEdge) == 2:
                uvEdgePairs = []
                uvEdgePairs.append(uvEdge)
            
            # Insert the uvEdgePair(s) into either the uvEdgeListU/V by checking its arctan angle
            for uvEdge in uvEdgePairs:
                # Get absolute value of the uvEdge angle (to nearest 90 deg)
                rotAngle = math.fabs( calcArctanAngle(uvEdge[0], uvEdge[1]) )

                # Determine where to insert the uvEdge (U or V list)
                if rotAngle >= 0 and rotAngle <= rotAngleTol:
                    
                    # Create uvEdge tuple and insert into V list
                    uvEdgeTuple = (uvEdge[0], uvEdge[1])
                    uvEdgeListU.insert(0, uvEdgeTuple)

                elif rotAngle <= 90 and rotAngle >= (90 - rotAngleTol):
                    
                    # Create uvEdge tuple and insert into U list
                    uvEdgeTuple = (uvEdge[0], uvEdge[1])
                    uvEdgeListV.insert(0, uvEdgeTuple)
                    
                else:
                    pass # uvEdge is already straight
        
        # Straighten edges: edge loops along U
        if strType == 0 or strType == 1:
            
            while len(uvEdgeListU) != 0:
                
                # Clear lists and get coords from first edgeUV. Use as start for edge loop
                edgeLoop = []
                removeList = []
                scannedEdges = []
                stopLoop = False
                edgeLoop.insert(0, uvEdgeListU[0][0])
                edgeLoop.insert(1, uvEdgeListU[0][1])
                removeList.insert(0, uvEdgeListU[0])            
                startingEdge = uvEdgeListU[0] 
                
                # Keep running the upcomming for-loop until no more components are added
                # to the current edgeLoop. When that happens, exit and straighten.
                while stopLoop == False:
                
                    compAdded = False
                
                    # Scan all uvEdges (tuples) and look for connections forming the edgeLoop
                    for x in range(len(uvEdgeListU)):
                        
                        # Check if we've worked on the current tuple
                        if uvEdgeListU[x] not in scannedEdges:

                            # Split up the current tuple into a list with it's edgeUV components
                            singleEdge = []
                            singleEdge.append(uvEdgeListU[x][0])
                            singleEdge.append(uvEdgeListU[x][1])
          
                            # Check if the edgeUV exist in the edgeLoop list
                            if singleEdge[0] in edgeLoop or singleEdge[1] in edgeLoop:
                                
                                # Check every individual UV component of the current uvEdge
                                for uv in singleEdge:
                                    if uv not in edgeLoop:

                                        # Add components to lists
                                        compAdded = True
                                        edgeLoop.append(uv)
                                        scannedEdges.append(uvEdgeListU[x])
                                        removeList.append(uvEdgeListU[x])

                            else:
                                pass # It doesn't exist in the edgeLoop
                                
                        else:
                            pass # uvEdge has been scanned already
                            
                    # Entire edgeLoop gathered. Stop the while-loop running the for-loop scanner
                    if compAdded == False:
                        stopLoop = True
                    
                # Remove processed edgeUVs (tuples)
                for item in removeList:
                    if item in uvEdgeListU:
                        uvEdgeListU.remove(item)

                # Select the edgeLoop and straighten it
                pm.select(edgeLoop)
                alignUVs("avgV")
           
        # Straighten edges: edge loops along V
        if strType == 0 or strType == 2:  

            while len(uvEdgeListV) != 0:
                
                # Clear lists and get coords from first edgeUV. Use as start for edge loop
                edgeLoop = []
                removeList = []
                scannedEdges = []
                stopLoop = False
                edgeLoop.insert(0, uvEdgeListV[0][0])
                edgeLoop.insert(1, uvEdgeListV[0][1])
                removeList.insert(0, uvEdgeListV[0])            
                startingEdge = uvEdgeListV[0] 
                
                # Keep running the upcomming for-loop until no more components are added
                # to the current edgeLoop. When that happens, exit and straighten.
                while stopLoop == False:
                
                    compAdded = False
                
                    # Scan all uvEdges (tuples) and look for connections forming the edgeLoop
                    for x in range(len(uvEdgeListV)):
                        
                        # Check if we've worked on the current tuple
                        if uvEdgeListV[x] not in scannedEdges:

                            # Split up the current tuple into a list with it's edgeUV components
                            singleEdge = []
                            singleEdge.append(uvEdgeListV[x][0])
                            singleEdge.append(uvEdgeListV[x][1])
          
                            # Check if the edgeUV exist in the edgeLoop list
                            if singleEdge[0] in edgeLoop or singleEdge[1] in edgeLoop:
                                
                                # Check every individual UV component of the current uvEdge
                                for uv in singleEdge:
                                    if uv not in edgeLoop:

                                        # Add components to lists
                                        compAdded = True
                                        edgeLoop.append(uv)
                                        scannedEdges.append(uvEdgeListV[x])
                                        removeList.append(uvEdgeListV[x])

                            else:
                                pass # It doesn't exist in the edgeLoop
                                
                        else:
                            pass # uvEdge has been scanned already
                            
                    # Entire edgeLoop gathered. Stop the while-loop running the for-loop scanner
                    if compAdded == False:
                        stopLoop = True
                    
                # Remove processed edgeUVs (tuples)
                for item in removeList:
                    if item in uvEdgeListV:
                        uvEdgeListV.remove(item)

                # Select the edgeLoop and straighten it
                pm.select(edgeLoop)
                alignUVs("avgU")
            
    # Select the original selection
    pm.select(selOrg)
 

# Load/Store field values to a variable
def tdVar(mode, field1, field2=None):

    if mode == "getA":
        varTD = pm.optionVar["manipVarTDA1OptVar"]
        varMap = pm.optionVar["manipVarTDA2OptVar"]
        field1.setValue1(varTD)
        field2.setValue1(varMap)
    
    if mode == "getB":
        varTD = pm.optionVar["manipVarTDB1OptVar"]
        varMap = pm.optionVar["manipVarTDB2OptVar"]
        field1.setValue1(varTD)
        field2.setValue1(varMap)
    
    if mode == "setA":
        varTD = field1.getValue1()
        varMap = field2.getValue1()
        pm.optionVar["manipVarTDA1OptVar"] = varTD
        pm.optionVar["manipVarTDA2OptVar"] = varMap
    
    if mode == "setB":
        varTD = field1.getValue1()
        varMap = field2.getValue1()
        pm.optionVar["manipVarTDB1OptVar"] = varTD
        pm.optionVar["manipVarTDB2OptVar"] = varMap
        
    if mode == "updateTD":
        pm.optionVar["tdOptVar"] = field1.getValue1()
    
    if mode == "updateSize":
        pm.optionVar["tdSizeOptVar"] = field1.getValue1()
    

# Translates a UV selection    
def translateUVs(dir):
    
    # Update coords and read from optVars
    updateManipCoords()
    manipAmt = pm.optionVar["manipAmtOptVar"]
    
    # If the absolute toggle is active
    if pm.optionVar["absToggleOptVar"] == True:
    
        # Get bounding box
        uvBox = pm.polyEvaluate(boundingBoxComponent2d=True)
        
        # Calc distances
        distCenterU = 0.5 * (uvBox[0][0] + uvBox[0][1])
        distCenterV = 0.5 * (uvBox[1][0] + uvBox[1][1])
        distU = distCenterU - manipAmt
        distV = distCenterV - manipAmt

        # Get proper translation distance
        if distU < 0:
            distU = math.fabs(distU)
            distV = math.fabs(distV)
        else:
            distU = -distU
            distV = -distV
    
    # Move switch
    if dir == "left" or dir == "upLeft" or dir == "downLeft":
        if pm.optionVar["absToggleOptVar"] == False:
            pm.polyEditUV(
                uValue=(manipAmt * -1),
                vValue=0
            )
        else: # Absolute position
            pm.polyEditUV(
                uValue=distU
            )
    
    if dir == "right" or dir == "upRight" or dir == "downRight":
        if pm.optionVar["absToggleOptVar"] == False:
            pm.polyEditUV(
                uValue=manipAmt,
                vValue=0
            )
        else: # Absolute position
            pm.polyEditUV(
                uValue=distU
            )
    
    if dir == "up" or dir == "upRight" or dir == "upLeft":
        if pm.optionVar["absToggleOptVar"] == False:
            pm.polyEditUV(
                uValue=0,
                vValue=manipAmt
            )
        else: # Absolute position
            pm.polyEditUV(
                vValue=distV
            )
    
    if dir == "down" or dir == "downRight" or dir == "downLeft":
        if pm.optionVar["absToggleOptVar"] == False:
            pm.polyEditUV(
                uValue=0,
                vValue=(manipAmt * -1)
            )
        else: # Absolute position
            pm.polyEditUV(
                vValue=distV
            )
      
        
def unfoldUVs(unfoldType="both", win=None):

    # Vars
    methodVar = 1
    pinVar = False
    pluginLoaded = False
    
    # Check for Unfold3D plugin - correct optVar if it isnt
    if pm.pluginInfo("Unfold3D", loaded=True, query=True) == True:
        pluginLoaded = True

    # Manage optVars
    if pm.optionVar["unfoldPinOptVar"] == True and pm.optionVar["unfoldPinTypeOptVar"] == 1:
        pinVar = True
    
    if pluginLoaded == True:
        methodVar = pm.optionVar["unfoldMethodOptVar"]
    else:
        if pm.optionVar["unfoldMethodOptVar"] == 1:
            methodVar = 2
        elif pm.optionVar["unfoldMethodOptVar"] == 2:
            methodVar = 3
        
    # Validate selection
    checkSel("UV")
    
    # Store selection
    orgSel = pm.ls(selection=True, flatten=True)
    
    # Convert to individual shells, store as list
    shellList = convertToShell()
    
    # Begin unfolding
    for item in shellList:
        unfoldSel = []
        
        # Get UVs from whole shell (item) and compare to original selection
        for uv in item:
            if uv in orgSel:
                unfoldSel.append(uv)
                
        ## Standard unfold cases
    
        if unfoldType == "both":
        
            # Method: Unfold3D
            if methodVar == 1:
                pm.Unfold3D(
                    unfoldSel,
                    unfold=True, 
                    iterations=pm.optionVar["unfoldItrOptVar"],
                    pack=pm.optionVar["unfoldPackOptVar"],
                    borderintersection=pm.optionVar["unfoldBorderOptVar"],
                    triangleflip=pm.optionVar["unfoldFlipsOptVar"],
                    mapsize=int(pm.optionVar["unfoldSizeOptVar"]),
                    roomspace=pm.optionVar["unfoldRoomOptVar"],
                )
            
            # Method: Legacy
            elif methodVar == 2:
                pm.polyOptUvs( # Local solver
                    unfoldSel,
                    areaWeight=pm.optionVar["unfoldAreaOptVar"],
                    constructionHistory=pm.optionVar["unfoldHistOptVar"], 
                    globalBlend=pm.optionVar["unfoldSolverOptVar"], 
                    globalMethodBlend=pm.optionVar["unfoldOtOOptVar"], 
                    iterations=pm.optionVar["unfoldMaxItrOptVar"],
                    optimizeAxis=pm.optionVar["unfoldConstOptVar"],
                    pinSelected=pinVar,
                    pinUvBorder=pm.optionVar["unfoldPinBorderOptVar"],
                    scale=pm.optionVar["unfoldSFactOptVar"],
                    stoppingThreshold=pm.optionVar["unfoldStopOptVar"], 
                    useScale=pm.optionVar["unfoldRescaleOptVar"],
                )
            
            # Method: Quick
            elif methodVar == 3:
                pm.polyOptUvs( # Local solver
                    unfoldSel,
                    constructionHistory=True,
                    globalBlend=0.0, 
                    globalMethodBlend=1.0, 
                    iterations=25,
                    optimizeAxis=0,
                    pinSelected=False,
                    stoppingThreshold=0.001, 
                    useScale=False,
                )
                pm.polyOptUvs( # Global solver
                    unfoldSel,
                    constructionHistory=True,
                    globalBlend=0.25, 
                    globalMethodBlend=1.0, 
                    iterations=5,
                    optimizeAxis=0,
                    pinSelected=False,
                    stoppingThreshold=0.001, 
                    useScale=False,
                )
                
        ## Special unfold cases

        # Legacy unselected
        elif unfoldType == "unselected":    
            pm.polyOptUvs( # Local solver
                unfoldSel,
                constructionHistory=True,
                globalBlend=0.0, 
                globalMethodBlend=1.0, 
                iterations=25,
                optimizeAxis=0,
                pinSelected=True,
                stoppingThreshold=0.001, 
                useScale=False,
            )
            pm.polyOptUvs( # Global solver
                unfoldSel,
                constructionHistory=True,
                globalBlend=0.25, 
                globalMethodBlend=1.0, 
                iterations=5,
                optimizeAxis=0,
                pinSelected=True,
                stoppingThreshold=0.001, 
                useScale=False,
            )

        
        # Legacy U
        elif unfoldType == "U":   
            pm.polyOptUvs( # Global solver
                unfoldSel,
                constructionHistory=True,
                globalBlend=0.25, 
                globalMethodBlend=1.0, 
                iterations=5,
                optimizeAxis=2,
                pinSelected=False,
                stoppingThreshold=0.001, 
                useScale=False,
            )
        
        # Legacy V
        elif unfoldType == "V":
            pm.polyOptUvs( # Global solver
                unfoldSel,
                constructionHistory=True,
                globalBlend=0.25, 
                globalMethodBlend=1.0, 
                iterations=5,
                optimizeAxis=1,
                pinSelected=False,
                stoppingThreshold=0.001, 
                useScale=False,
            )
        
        else: # Unknown type
            print("Unknown unfoldType sent to core.unfoldUVs")
        
    # Reselect original selection
    pm.select(orgSel)
        
    # Close unfold window
    if win != None:
        pm.deleteUI( win )


# Updates the pivot of the move/rotate/scale -contexts
def updateManipCoords():
    
    # Get current tool
    cTool = pm.currentCtx()
    
    if cTool == "moveSuperContext":
        pm.optionVar["manipCoordsOptVar"] = pm.texMoveContext( "texMoveContext", query=True, position=True ) 
    
    elif cTool == "RotateSuperContext":
        pm.optionVar["manipCoordsOptVar"] = pm.texRotateContext( "texRotateContext", query=True, position=True ) 
    
    elif cTool == "scaleSuperContext":
        pm.optionVar["manipCoordsOptVar"] = pm.texScaleContext( "texScaleContext", query=True, position=True )
        
    elif cTool == "ModelingToolkitSuperCtx":
        pm.optionVar["manipCoordsOptVar"] = pm.texWinToolCtx( "ModelingToolkitSuperCtx", query=True, position=True )
    
    else: # Some other tool - pass
        pass
        
        
# Saves optVars for the frames
def updateFrame(frame, state):

    if frame == 1:
        pm.optionVar["frameManipOptVar"] = state
    elif frame == 2:
        pm.optionVar["frameAlignOptVar"] = state
    elif frame == 3:
        pm.optionVar["frameSetOptVar"] = state
    elif frame == 4:
        pm.optionVar["frameMappingOptVar"] = state
    elif frame == 5:
        pm.optionVar["frameTDOptVar"] = state
        
        
        
# Updates the UV set editor
def updateUVSetEditor(scrollList):
    
    # Clear the UV set editor
    scrollList.removeAll()
    
    # Get mesh from the current selection
    mesh = getShapes()
    
    # How do we differentiate from a group?=?????
    
    # If we have a selection, only get the first object in the queue
    if mesh != None and mesh != []:
        mesh = mesh[0]

    # If a mesh is selected, get all and the current UV-set(s)
    if mesh != None and mesh != []:
        
        uvSets = getSet("all", mesh)
        
        # Prevent # TypeError: 'NoneType' object is not iterable # when exporting a group
        if uvSets != None:

            # Rebuild the textScrollList
            for item in uvSets:
            
                # Check UV set for instance identifiers
                uvSetPerInst = getSet("instanced", mesh, item)
            
                # If instance identifier was found, continue to next uv-set in the loop
                if len(uvSetPerInst[0]) > 0:
                    uvSetInst = uvSetPerInst[0]
                else:
                    continue
                    
                # Add UV set to list
                scrollList.append(uvSetInst) 
            
                # In case the default UV set editor is also open...
                if pm.window("uvSetEditor", exists=True):
                    pm.textScrollList(
                    "uvSetList", edit=True,
                        append=uvSetInst
                    )
          
        # Get the current (first) UV-set
        uvSetCurrent = getSet("current", mesh)
        
        # ...and highlight it in the editor
        scrollList.setSelectItem(uvSetCurrent)
        
        # Also highlight it in the native UV set editor if it's open
        if pm.window("uvSetEditor", exists=True):
            pm.textScrollList(
                "uvSetList", edit=True,
                selectItem=uvSetCurrent
            )
            
    else:
        # No selection on the UI - clear the list
        scrollList.deselectAll()
        scrollList.removeAll()


########## Error codes ##########

def errorCode(code):
    
    # No selection at all
    if code == 0:
        pm.confirmDialog(
            button="Ok",
            cancelButton="Ok",
            defaultButton="Ok",
            dismissString="Ok",
            message="You must select something before performing this operation.",
            title="Error!"
        )
        pm.error("You must select something before performing this operation.")
    
    # No valid face selection
    if code == 1:
        pm.confirmDialog(
            button="Ok",
            cancelButton="Ok",
            defaultButton="Ok",
            dismissString="Ok",
            message="You must select some faces before performing this operation.",
            title="Error!"
        )
        pm.error("You must select some faces before performing this operation.")
    
    # No valid UV selection
    if code == 2:
        pm.confirmDialog(
            button="Ok",
            cancelButton="Ok",
            defaultButton="Ok",
            dismissString="Ok",
            message="You must select some UVs before performing this operation.",
            title="Error!"
        )
        pm.error("You must select some UVs before performing this operation.")
    
    # No valid edge or UV selection
    if code == 3:
        pm.confirmDialog(
            button="Ok",
            cancelButton="Ok",
            defaultButton="Ok",
            dismissString="Ok",
            message="You must select some edges or UVs before performing this operation.",
            title="Error!"
        )
        pm.error("You must select some edges or UVs before performing this operation.")
            
    # No valid face or UV selection
    if code == 4:
        pm.confirmDialog(
            button="Ok",
            cancelButton="Ok",
            defaultButton="Ok",
            dismissString="Ok",
            message="You must select some faces or UVs before performing this operation.",
            title="Error!"
        )
        pm.error("You must select some faces or UVs before performing this operation.")
        
    # No valid mesh or UV selection
    if code == 5:
        pm.confirmDialog(
            button="Ok",
            cancelButton="Ok",
            defaultButton="Ok",
            dismissString="Ok",
            message="You must select a mesh or some UVs before performing this operation.",
            title="Error!"
        )
        pm.error("You must select a mesh or some UVs before performing this operation.")
        
    # Selection spans over multiple shells
    if code == 6:
        pm.confirmDialog(
            button="Ok",
            cancelButton="Ok",
            defaultButton="Ok",
            dismissString="Ok",
            message="This tool doesn't work if the selection spans over multiple UV shells.",
            title="Error!"
        )
        pm.error("This tool doesn't work if the selection spans over multiple UV shells.")
        
    # Straighten UV shell failed
    if code == 7:
        pm.confirmDialog(
            button="Ok",
            cancelButton="Ok",
            defaultButton="Ok",
            dismissString="Ok",
            message=("The straighten shell -tool only works on -one- UV shell and only on -one- "
                 "edge loop -or- edge ring at a time. Center or shell border selection does "
                 "not matter."
                     ),
            title="Error!"
        )
        pm.error("Incorrect selection for the straighten shell tool")
        
    # Didn't select exactly two UVs
    if code == 8:
        pm.confirmDialog(
            button="Ok",
            cancelButton="Ok",
            defaultButton="Ok",
            dismissString="Ok",
            message=("You must select exactly two UVs before performing this operation."),
            title="Error!"
        )
        pm.error("You must select exactly two UVs before performing this operation.")  
        
    # No valid mesh selection
    if code == 9:
        pm.confirmDialog(
            button="Ok",
            cancelButton="Ok",
            defaultButton="Ok",
            dismissString="Ok",
            message=("You must select a mesh before performing this operation."),
            title="Error!"
        )
        pm.error("You must select a mesh before performing this operation.")  
        
    # File path is blank
    if code == 10:
        pm.confirmDialog(
            button="Ok",
            cancelButton="Ok",
            defaultButton="Ok",
            dismissString="Ok",
            message=("You must enter a file path."),
            title="Error!"
        )
        pm.error("You must enter a file path.")  
        
    # No valid face or mesh selection
    if code == 11:
        pm.confirmDialog(
            button="Ok",
            cancelButton="Ok",
            defaultButton="Ok",
            dismissString="Ok",
            message=("You must select some face(s) or a mesh before performing this operation."),
            title="Error!"
        )
        pm.error("You must select some face(s) or a mesh before performing this operation.")  
    
    # Invalid selection for UV Set: Propagate
    if code == 12:
        pm.confirmDialog(
            button="Ok",
            cancelButton="Ok",
            defaultButton="Ok",
            dismissString="Ok",
            message=("Propagate requires more than one object to be selected."),
            title="Error!"
        )
        pm.error("Propagate requires more than one object to be selected.")  
        
    if code == 13:
        pm.confirmDialog(
            button="Ok",
            cancelButton="Ok",
            defaultButton="Ok",
            dismissString="Ok",
            message=("This operation requires at least 2 UVs or an edge."),
            title="Error!"
        )
        pm.error("You must select exactly two UVs or one edge before performing this operation.")  
        
    if code == 14:
        pm.confirmDialog(
            button="Ok",
            cancelButton="Ok",
            defaultButton="Ok",
            dismissString="Ok",
            message=("This operation requires an edge selection."),
            title="Error!"
        )
        pm.error("This operation requires an edge selection.")  
        
    if code == 15:
        pm.confirmDialog(
            button="Ok",
            cancelButton="Ok",
            defaultButton="Ok",
            dismissString="Ok",
            message=("Using this feature on a UV selection requires exactly 2 UVs!"),
            title="Using this feature on a UV selection requires exactly 2 UVs!"
        )
        pm.error("")

    if code == 17:
        pm.confirmDialog(
            button="Ok",
            cancelButton="Ok",
            defaultButton="Ok",
            dismissString="Ok",
            message=("This feature requires one selected edge OR two selected UVs to execute."),
            title="Error!"
        )
        pm.error("This feature requires one selected edge OR two selected UVs to execute.") 
        
    if code == 18:
        pm.confirmDialog(
            button="Ok",
            cancelButton="Ok",
            defaultButton="Ok",
            dismissString="Ok",
            message=("The selected UVs are not located on the same shared edge."),
            title="Error!"
        )
        pm.error("The selected UVs are not located on the same shared edge.") 