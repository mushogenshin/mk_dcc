### See the file "LICENSE.txt" for the full license governing this code.
import booltoolAPI as btapi

import maya.cmds as cmds
import maya.mel as mel
import maya.OpenMaya as om
import flux.ae.loader as loader

def registerTemplates():
    loader.registerTemplate('AEbooltoolTemplate.AEbooltoolTemplate', 'booltool')

nodeCallbacks = []

class MCallbackIdWrapper:
    def __init__(self, callbackId):
        self.callbackId = callbackId

    def __del__(self):
        om.MMessage.removeCallback(self.callbackId)

def isInBatch():
    return (om.MGlobal.mayaState() == om.MGlobal.kBatch or om.MGlobal.mayaState() == om.MGlobal.kLibraryApp)

def register():
    # Registers node created callbacks to manage all required connections
    try:
        global nodeCallbacks
        nodeCallbackId = om.MDGMessage.addNodeAddedCallback(onBoolToolCreated, "booltool", None)
        nodeCallbacks.append(MCallbackIdWrapper(nodeCallbackId))

        if not isInBatch():
            setupUI()
    except Exception, e:
        print str(e)

def deregister():
    # Clear up callbacks
    global nodeCallbacks
    nodeCallbacks = []
    if not isInBatch():
        tearDownUI()

def onBoolToolRemoved(mobj, dgmodifier, clientData):
    dep = om.MFnDependencyNode(mobj)
    pname = dep.name()
    nodes = cmds.listConnections(pname + '.inWorldMesh') or []
    for n in nodes:
        btapi.setNodeVisibility(n, 1)

def onBoolToolCreated(mobj, clientData):
    nodeCallbackId = om.MNodeMessage.addNodeAboutToDeleteCallback(mobj, onBoolToolRemoved, None)
    nodeCallbacks.append(MCallbackIdWrapper(nodeCallbackId))
    
def getShelfButton():
    children = cmds.shelfLayout('Polygons', childArray=True, q=True)

    for c in children:
        docTag = ''
        try:
            docTag = cmds.shelfButton(c, dtg=True, q=True)
        except: pass
        if docTag and docTag == 'BoolTool/Create':
            return c

def setupUI():
    registerTemplates()
    if not getShelfButton():
        cmds.shelfButton('BoolToolCreate', annotation='Bool',
            image1='Bool_Logo_Shelf.png', command='import booltoolUtils; booltoolUtils.createBoolTool()',
            p='Polygons', dtg='BoolTool/Create', label='Bool')

def tearDownUI():
    shelfBtn = getShelfButton()
    if shelfBtn:
        fullPath = cmds.shelfButton(shelfBtn, fullPathName=True, q=True)
        cmds.deleteUI(fullPath)

def createBoolTool():
    meshes = cmds.ls(sl=True, dag=True, type="mesh", long=True) or []

    boolNode = cmds.createNode("booltool", n="boolTool#")
    cmds.select(boolNode)
    if not cmds.attributeQuery('shapeMessage', node=boolNode, exists=True):
        cmds.addAttr(longName='shapeMessage', at='message')
    name = cmds.createNode('transform', n='Bool#')
    shapeName = cmds.createNode('mesh', n='BoolShape#', p=name)
    cmds.select(shapeName)
    cmds.addAttr(longName='shapeMessage', at='message')
    cmds.connectAttr(boolNode + '.outMesh', shapeName + '.inMesh')
    cmds.connectAttr(boolNode + '.shapeMessage', shapeName + '.shapeMessage')

    polySoftName = cmds.polySoftEdge(name)[0]
    cmds.sets(shapeName, edit=True, forceElement="initialShadingGroup")
    cmds.select(name)

    for m in meshes:
        btapi.addMeshToBool(boolNode, m)