import math
import maya.OpenMaya as om
import maya.cmds as cmds
# For Using in script editor
#import ilmUDIMTool
#reload(ilmUDIMTool)
#ilmUDIMTool.ilmCombineMeshByUDIMs()
#
def name2DagPath(aNodeName):
    selectionList = om.MSelectionList()
    try:
        selectionList.add(aNodeName)
    except:
        return None
    dagPath = om.MDagPath()
    selectionList.getDagPath( 0, dagPath )
    return dagPath
def getUVShells(shape, uvSet=None):
    '''
        return a dict of UVshell in format
        uvShells{shelllId:UVlist,...}
    '''
    meshFn = om.MFnMesh(shape)
    
    uvShellArray = om.MIntArray()
    # uvShellArray is a list of Shell Indices sorted by UV Id.
    # [0, 0, 0, 1, 1, 1, 0] translates to UVs  0, 1, 2, 6 belong to a shell, while 3, 4, 5 belong to another
    
    shells = om.MScriptUtil()
    shellsPtr = shells.asUintPtr()
    meshFn.getUvShellsIds(uvShellArray, shellsPtr, uvSet)
    
    uvShells = {}
    for i, shellId in enumerate(uvShellArray):
        comp = '{0}.map[{1}]'.format(shape.fullPathName(), i)
        #see if can optimise later, because if else could be slow for a very big array
        if uvShells.has_key(shellId):
            uvShells[shellId].append(comp)
        else:
            uvShells[shellId] = [comp]
    return uvShells
    
def mergeDict(dict1, dict2):
    result = dict1
    if not result:
        return dict2
    for k in dict2:
        if k in result:
            result[k].extend(dict2[k])
        else:
            result[k] = dict2[k]
    return result

def getRectUDIM(uvList):
    cmds.select(uvList)
    shellBB = cmds.polyEvaluate(bc2=1)
    return (abs(shellBB[0][1] - shellBB[0][0]), abs(shellBB[1][1] - shellBB[1][0]), shellBB[0][0], shellBB[1][0])
def getValueUDIM(uvList):
    """
        Calculate UDIM number base on Bounding Box
        UDIM num = 1001 + v*10 + u
    """
    cmds.select(uvList)
    shellBB = cmds.polyEvaluate(bc2=1)
    xMinFloat = shellBB[0][0]
    xMinInt = int(xMinFloat)
    xMaxInt = int(shellBB[0][1])
    yMinFloat = shellBB[1][0]
    yMinInt = int(yMinFloat)
    yMaxInt = int(shellBB[1][1])
    retVal = 0
    #print xMinInt, xMaxInt, yMinInt, yMaxInt
    if xMinInt == xMaxInt and yMinInt == yMaxInt and xMinFloat > 0 and xMinInt < 10 and yMinFloat > 0:
        return 1001 + yMinInt*10 + xMinInt
    return retVal
def ilmCombineMeshByUDIMs(byMesh='all'):
    """
        Combine all meshes or selected meshes) which have the same UDIM
        assume: 1 mesh has only 1 UDIM
    """
    selection = cmds.ls(sl=1)
    meshes = []
    if not selection:
        meshes = cmds.ls(type='mesh')
    else:
        for aS in selection:
            slMesh = cmds.listRelatives(aS, s=1)
            if slMesh and len(slMesh) == 1:
                meshes.append(slMesh[0])
            else:
                print 'Error: %s should have 1 and only 1 shapeNode'%aS
    uvShellsByUVList = {}
    numItem = len(uvShellsByUVList)
    for aM in meshes:
        if cmds.getAttr('%s.intermediateObject'%aM) or cmds.ls(aM, ro=1):
            #it's intermediateObject or readOnly node, just ignore
            continue
        uvShells = getUVShells(name2DagPath(aM), uvSet='map1')
        for k in uvShells:
            if not uvShells[k]:
                continue
            if k in uvShellsByUVList:
                uvShellsByUVList[k+numItem] = uvShells[k]
            else:
                uvShellsByUVList[k] = uvShells[k]
        numItem = len(uvShellsByUVList)
    meshesByUDIM = {}
    for k in uvShellsByUVList:
        udimValue = getValueUDIM(uvShellsByUVList[k])
        meshName = uvShellsByUVList[k][0].split('.')[0]
        if udimValue:
            if udimValue in meshesByUDIM:
                if not meshName in meshesByUDIM[udimValue]:
                    meshesByUDIM[udimValue].append(meshName)
            else:
                meshesByUDIM[udimValue] = [meshName]
        else:
            print '\t>>> Error UDIM:', meshName
            
    solvedMesh = []
    for k in meshesByUDIM:
        print 'Combine...', 'combineUDIM%s'%k, meshesByUDIM[k]
        uniqueList = set(meshesByUDIM[k]) - set(solvedMesh)
        if len(uniqueList) > 1:
            cmds.polyUnite(list(uniqueList), ch=0, mergeUVSets=1, name='combineUDIM%s'%k)
            solvedMesh.extend(list(uniqueList))
        elif uniqueList and not list(uniqueList)[0] in solvedMesh:
            cmds.rename(cmds.listRelatives(list(uniqueList)[0], p=1, f=1), 'combineUDIM%s'%k)
            solvedMesh.append(list(uniqueList)[0])
"""
padding = 0.02
uStart, vStart = (padding, padding)
shellIDParsed = []
xUDIM = 0
yUDIM = 0
for k1 in uvShellsByUVList:
    
        #init uStart, vStart = 0.02 (pading percent)
        #arrange 1 shell at (uStart, vStart)
        #update (uStart, max(vStart))
        #if uStart + shell.u < 1 - 0.02 then (arrange next shell at (uStart + shell.u/2 + 0.02, vStart), update uStart, max(vStart))
        #else:
        #    update((uStart = 0.02, vStart = max(vStart) + 0.02))
        #    arrange shell at (uStart, vStart)
    
    
    if k1 in shellIDParsed:
        continue
    shellIDParsed.append(k1)
    uu, vv, uMinBB, vMinBB = getRectUDIM(uvShellsByUVList[k])
    cmds.polyEditUV(uvShellsByUVList[k], r=1, u=xUDIM - int(uMinBB), v=yUDIM - int(vMinBB))
    for k2 in uvShellsByUVList:
        if k2 in shellIDParsed:
            continue
        if (udimCompass + uvShellsByCompass[cnt2][1]) < 0.98 :
        shellIDParsed.append(k1)

print uvShellsByUVList
uvShellsByCompass = []

for shellID in uvShellsByUVList:
    cmds.select(uvShellsByUVList[shellID])
    shellBB = cmds.polyEvaluate(bc2=1)
    uvCompass = abs(shellBB[0][1] - shellBB[0][0])*abs(shellBB[1][1] - shellBB[1][0])
    uvShellsByCompass.append([shellID,uvCompass])

cmds.select(cl=1)
arrUDIM = []
shellIDParsed = []
for cnt1 in range(len(uvShellsByCompass)):
    if cnt1 in shellIDParsed:
            continue
    shellIDParsed.append(cnt1)
    udimCompass = uvShellsByCompass[cnt1][1]
    aUDIM = uvShellsByUVList[uvShellsByCompass[cnt1][0]]
    for cnt2 in range(cnt1 + 1, len(uvShellsByCompass)):
        if cnt2 in shellIDParsed:
            continue
        if (udimCompass + uvShellsByCompass[cnt2][1]) < 0.98 :
            udimCompass += uvShellsByCompass[cnt2][1]
            aUDIM.extend(uvShellsByUVList[uvShellsByCompass[cnt2][0]])
            shellIDParsed.append(cnt2)
    arrUDIM.append(aUDIM)

xUDIM = 0
yUDIM = 0
for anU in arrUDIM:
    print anU
    
    #cmds.polyLayoutUV(anU, lm=0, sc=0, se=0, rbf=0, fr=0, ps=0.2, l=2)
    #cmds.polyLayoutUV(anU, lm=0, sc=1, se=0, rbf=0, fr=0, ps=0.2, l=2)
    cmds.polyMultiLayoutUV(anU, lm=0, sc=1, rbf=0, fr=0, ps=0.2, l=2)
    cmds.polyEditUV(anU, r=1, u = xUDIM, v=yUDIM)
    if xUDIM == 9:
        xUDIM = 0
        yUDIM += 1
    else:
        xUDIM += 1
print len(arrUDIM)
"""