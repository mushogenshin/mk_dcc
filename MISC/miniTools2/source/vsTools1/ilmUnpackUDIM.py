import maya.cmds as cmds

uMin = 0
uMax = 9 
vMin = 0

def doUnpackUDIM(meshes, uMin = uMin, uMax = uMax, vMin = vMin):
    """
        for each mesh in a list of selected meshes do
            arrange UV side-by-side in U and V direction, starting from U = 1, V = 1
        Assume:
            each mesh have all UVs located within (0,1)
    """
    currSl = cmds.ls(sl=1)
    uMin += 1
    for i in range(1, len(meshes)):
        if uMin > uMax:
            uMin = 0
            vMin += 1
        toUV = cmds.polyListComponentConversion(meshes[i], tuv=1)
        try:
            cmds.polyEditUV(toUV, r=1, u=uMin, v=vMin)
        except:
            pass
        uMin += 1
def ilmUnpackUDIM():
    """
        prepare mesh list from selected objects to unpack UDIM
    """
    slMeshes = []
    for anObj in cmds.ls(sl=1, l=1):
        #check object is a mesh
        meshShape = cmds.listRelatives(anObj, s=1)
        if meshShape and cmds.nodeType(meshShape[0]) == 'mesh':
            slMeshes.append(anObj) 
    
    if len(slMeshes) > 1:
        doUnpackUDIM(slMeshes, uMin = uMin, uMax = uMax, vMin = vMin)
    else:
        cmds.confirmDialog(m='Please select at least 2 meshes to unpack UDIM')
            