import maya.api.OpenMaya as om2
import maya.cmds as cmds
from collections import defaultdict

def getUVShells(mesh, uvSet=None):
    """ Return UVs per shell ID for a given mesh.
    
    :return: list(list)
    :rtype: Return a list of UVs per shell.
    """
    
    # define which uvSet to process
    uvSets = cmds.polyUVSet(mesh, q=True, allUVSets=True)
    if not uvSet or uvSet not in uvSets:
        uvSet = cmds.polyUVSet(mesh, q=True, cuv=True)[0]

    # get the api dag path
    sel = om2.MSelectionList()
    sel.add(mesh)
    dagPath = sel.getDagPath(0)
    dagPath.extendToShape()
    
    # Note:
    # Maya returns the .map[id] on the transform instead of shape if you select it.
    # For convenience for now let's do the same (whether you want this is up to you)
    mesh = cmds.ls(dagPath.fullPathName(), long=True, o=True)[0]
    mesh = mesh.rsplit('|', 1)[0] # get the parent transform
    
    # get shell uv ids
    fnMesh = om2.MFnMesh(dagPath)
    uvCount, uvShellArray = fnMesh.getUvShellsIds(uvSet)
    
    # convert to a format we like it (per shell)
    uvShells = defaultdict(list)
    for i, shellId in enumerate(uvShellArray):
        uv = '{0}.map[{1}]'.format(mesh, i)
        uvShells[shellId].append(uv)
    
    # return a list per shell
    return uvShells.values()
    
if __name__ == '__main__':
    
    # create test
    sphere = cmds.polySphere()[0]
    cmds.polyAutoProjection()
    cmds.select('{0}.map[1]'.format(sphere), r=1)
    sel = cmds.ls(sl=1)
    shells = getUVShells(sel[0])
    
    # test: print each shell
    for shell in shells:
        print shell
    
    # test: convert each selected uv component to uv shell
    sel = cmds.ls(sl=1, flatten=True, long=True)
    selected_shells = []  
    for shell in shells:
        for component in sel:
            if component in shell:
                selected_shells.extend(shell)
                
    cmds.select(selected_shells, r=1)
    
from see import see

see(pm.general.MeshUV)

myNode = pm.selected()[0]

myNode.getIndex()

pm.polyEditUV(myNode, q=True, u=True)
pm.select(shells[3], r=True)
pm.polyEditUV(u=-1, v=-2)