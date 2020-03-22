import maya.cmds as cmds
import maya.mel as mel

def nodeVisibility(node):
    isInvisible = not cmds.getAttr(node + '.visibility')
    if isInvisible:
        return 2

    if cmds.nodeType(node) == 'transform':
        node = cmds.listRelatives(node, s=True) or []
        if node:
            node = node[0]
        else:
            return

    isWireframe = cmds.getAttr(node + '.overrideEnabled')
    isWireframe = isWireframe and not cmds.getAttr(node + '.overrideShading')
    isWireframe = isWireframe and not cmds.getAttr(node + '.castsShadows')
    isWireframe = isWireframe and not cmds.getAttr(node + '.receiveShadows')
    isWireframe = isWireframe and not cmds.getAttr(node + '.primaryVisibility')
    isWireframe = isWireframe and not cmds.getAttr(node + '.visibleInReflections')
    isWireframe = isWireframe and not cmds.getAttr(node + '.visibleInRefractions')
    return not isWireframe

def setNodeVisibility(node, visibility):
    cmds.setAttr(node + '.visibility', visibility != 2)

    if visibility == 2: return

    if cmds.nodeType(node) == 'transform':
        node = cmds.listRelatives(node, s=True) or []
        if node:
            node = node[0]
        else:
            return

    if visibility == 0:
        cmds.setAttr(node + '.overrideEnabled', 1)

    cmds.setAttr(node + '.overrideShading', visibility)
    cmds.setAttr(node + '.castsShadows', visibility)
    cmds.setAttr(node + '.receiveShadows', visibility)
    cmds.setAttr(node + '.primaryVisibility', visibility)
    cmds.setAttr(node + '.visibleInReflections', visibility)
    cmds.setAttr(node + '.visibleInRefractions', visibility)

def addMeshToBool(boolNode, meshNode):
    i = mel.eval('getNextFreeMultiIndex %s 0;' % (boolNode + '.inWorldMesh'))

    if cmds.objExists(meshNode) and cmds.nodeType(meshNode) in ['transform', 'mesh']:
        existingConns = cmds.listConnections(meshNode + '.worldMesh') or []
        if cmds.ls(boolNode, uuid=True) in [cmds.ls(x, uuid=True) for x in existingConns]:
            return
        cmds.connectAttr(meshNode + '.worldMesh', boolNode + '.inWorldMesh[%d]' % i)
        setNodeVisibility(meshNode, 0)

def setNodeOverrideColor(node, color):
    try:
        color = [x / 255.0 for x in color]
        cmds.setAttr(node + '.overrideRGBColors', 1)
        cmds.setAttr(node + '.overrideColorRGB', *color, typ='float3')
    except: pass

def setBoolMode(node, mode):
    cmds.setAttr(node + '.booleanMode', mode)

def setBoolType(node, types):
    cmds.setAttr(node + '.booleanType', types, typ='Int32Array')

def setElementEnabled(node, elements):
    cmds.setAttr(node + '.elementEnabled', elements, typ='Int32Array')




