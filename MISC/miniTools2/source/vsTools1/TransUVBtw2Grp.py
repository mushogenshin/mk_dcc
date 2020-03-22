import maya.cmds as cmds

import TransUV2MultipleObjects as tUV

def getSrcMesh(grpNode):
    """
        return a dictionary of meshes under grpNode
    """
    meshDict = {}
    childMesh = cmds.listRelatives(grpNode, ad=1, f=1, type='mesh')
    for aC in childMesh:
        transNode = cmds.listRelatives(aC, p=1, f=1)
        transLeafNode = transNode[0].split('|')[-1]
        if transLeafNode in meshDict:
            print 'Duplicated mesh found: %s'%transNode[0]
        else:
            meshDict[transLeafNode] = transNode[0]
    return meshDict

def TransUVBtw2Grp():
    """
        Transfer UV between two selected group of meshes
        First selected group is the source
        The second one is the destination
    """
    grpSl = cmds.ls(sl=1)
    if len(grpSl) != 2:
        print 'Please select only 2 groups, first is SouRCe and the second is DeSTination.'
        return
    
    srcMesh = getSrcMesh(grpSl[0])
    dstMesh = getSrcMesh(grpSl[1])
    print srcMesh, dstMesh
    for aN in srcMesh:
        if aN in dstMesh:
            #first select is soruce and the rest of selecton is destination
            cmds.select(srcMesh[aN], dstMesh[aN])
            tUV.TransUV2MultipleObjects()
    print "DONE: transferUV Group"
