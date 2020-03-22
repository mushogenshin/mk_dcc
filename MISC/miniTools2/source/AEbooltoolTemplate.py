### See the file "LICENSE.txt" for the full license governing this code.
from flux.ae.Template import Template
from flux.ae.Custom import Custom

from flux.imports import *
import flux.core as fx
from flux.core import pix

from copy import deepcopy
import booltoolUI as btui
import booltoolAPI as btapi
reload(btui)
reload(btapi)

from contextlib import contextmanager

@contextmanager
def skippable():
    try:
        yield
    except Exception as e:
        if e.message != 'skippable':
            raise
            
def skipContext():
    raise Exception('skippable')

@contextmanager
def runLocked(sLock):
    if sLock.locked():
        skipContext()
    sLock.lock()
    yield
    sLock.unlock()

class SimpleLock(object):
    def __init__(self):
        self.isLocked = False

    def locked(self):
        return self.isLocked

    def lock(self):
        self.isLocked = True

    def unlock(self):
        self.isLocked = False

class AEbooltoolTemplate(Template):
    def buildUI(self, nodeName):
        self.addCustom(MyCustom)

class MyCustom(Custom):
    def buildUI(self, nodeName):
        self.toolbar = fx.widgetWithLayout('H', pix(2), pix(5),pix(2),pix(5),pix(2))
        self.toolbar.setAutoFillBackground(True)
        self.toolbar.setFixedHeight(pix(30))
        fx.setWidgetBackgroundColor(self.toolbar, [73,73,73])
        self.mainIcon = qt.QLabel()
        self.mainIcon.setPixmap(fx.getPixmap('Bool_Logo'))
        self.toolbar.layout().addSpacing(pix(2))
        self.toolbar.layout().addWidget(self.mainIcon)
        self.toolbar.layout().addSpacing(pix(8))
        self.titleLabel = qt.QLabel('Bool')
        self.toolbar.layout().addWidget(self.titleLabel)

        self.toolbar.layout().addStretch()

        self.debugButton = fx.ImageButton('Bool_Debug')
        self.debugButton.setHighlighted(True)
        self.debugButton.setToolTip('Enable/Disable Debug')
        self.debugButton.clicked.connect(self.uiDebugClicked)
        self.toolbar.layout().addWidget(self.debugButton)

        self.toolbar.layout().addSpacing(pix(2))

        self.centerButton = fx.ImageButton('Bool_CentrePivot')
        self.centerButton.setToolTip('Center Pivot')
        self.centerButton.clicked.connect(self.uiCenterPivot)
        self.toolbar.layout().addWidget(self.centerButton)

        self.toolbar.layout().addSpacing(pix(2))

        self.boolModeSwitch = fx.ImageButton('Bool_Mode1')
        self.boolModeSwitch.setToolTip('Bool mode')
        self.boolModeSwitch.clicked.connect(self.uiBoolModeChanged)
        self.boolModeValue = 0
        self.toolbar.layout().addWidget(self.boolModeSwitch)

        self.toolbar.layout().addSpacing(pix(3))

        self.addWidget(self.toolbar)
        self.addSpacing(pix(5))

        self.dropWidget = btui.DropListWidget()
        self.dropWidget.dropped.connect(self.uiDroppedNode)
        self.dropWidget.reorder.connect(self.uiReorderNodes)
        self.dropWidget.deleted.connect(self.uiDeleteNode)
        self.dropWidget.buttonClicked.connect(self.uiButtonClicked)
        self.dropWidget.selected.connect(self.uiSelected)
        self.addWidget(self.dropWidget)

        self.addSpacing(pix(5))

        self.supportLabel = qt.QLabel('Thanks for purchasing Bool. Mainframe + your support = more tools!')
        self.supportLabel.setAlignment(qt.Qt.AlignCenter)
        self.addWidget(self.supportLabel)

        self.addSpacing(pix(10))

        self.createAttributeListener('booleanType', self.attrBooleanTypeChange)
        self.createAttributeListener('booleanMode', self.attrBooleanModeChange)
        self.createAttributeListener('elementEnabled', self.attrElementEnabledChange)
        self.createAttributeListener('inWorldMesh', self.attrInWorldMeshChange)
        self.createAttributeListener('boolDebugEnabled', self.updateDebug)
        self.createAttributeListener('boolDebugInfo', self.updateDebug)

        self.uiLock = SimpleLock()
        self.visJobs = []

        self.m_lockRepaint = False
        self.prevName = 0
        self.nodeChanged()

    def updateDebug(self):
        debugEnabled = cmds.getAttr(self.name + '.boolDebugEnabled')
        self.debugButton.setHighlighted(debugEnabled)
        debugInfo = cmds.getAttr(self.name + '.boolDebugInfo') or []
        enabled = cmds.getAttr(self.name + '.elementEnabled') or []
        booleanMode = cmds.getAttr(self.name + '.booleanMode')

        counter = 0
        for i in xrange(self.itemCount()):
            item = self.itemAt(i)
            item.setDebugIcon(0)
            if enabled[i]:
                if debugEnabled:
                    if booleanMode == 0:
                        if counter == 0:
                            item.setDebugIcon((1 in debugInfo) + 1)
                    else:
                        if counter != 0:
                            item.setDebugIcon((counter in debugInfo) + 1)
                counter += 1
        self.repaintList()

    def clearVisJobs(self):
        for v in self.visJobs:
            if cmds.scriptJob(exists=v):
                cmds.scriptJob(kill=v)
        self.visJobs = []

    def setupScriptJobs(self, nodes):
        self.clearVisJobs()
        for n in nodes:
            job = cmds.scriptJob(attributeChange=[n + '.visibility', self.attrVisibilityChange])
            self.visJobs.append(job)

    def attrVisibilityChange(self):
        with skippable(), runLocked(self.uiLock):
            self.updateShadeState()

    def nodeChanged(self):
        if self.prevName != cmds.ls(self.name, uuid=True):
            self.prevName = cmds.ls(self.name, uuid=True)
            self.resetView()

        shape = cmds.listConnections(self.name + '.shapeMessage') or []
        if shape:
            self.titleLabel.setText(shape[0])

        nodes = cmds.listConnections(self.name + '.inWorldMesh') or []

        if len(nodes) != self.itemCount():
            self.resetView()

        for i in xrange(self.itemCount()):
            item = self.itemAt(i)
            item.setText(nodes[i])

    def resetView(self):
        self.m_lockRepaint = True
        self.updateNodes()
        self.updateShadeState()
        self.attrBooleanModeChange()
        self.attrElementEnabledChange()
        self.updateRowButtons()
        self.updateDebug()
        self.m_lockRepaint = False

    def uiSelected(self):
        items = self.dropWidget.listWidget.selectedItems()
        if items:
            cmds.select(items[0].text(), self.name)
            fx.mayaViewport().setFocus()

    @fx.undoChunk('attrBooleanTypeChange')
    def attrBooleanTypeChange(self):
        with skippable(), runLocked(self.uiLock):
            checked = cmds.getAttr(self.name + '.booleanMode')
            types = cmds.getAttr(self.name + '.booleanType')

            for i in xrange(self.itemCount()):
                enabled = self.isRowBoolEnabled(i, checked)
                self.setIndividualMode(i, types[i])
            self.repaintList()

    @fx.undoChunk('attrBooleanModeChange')
    def attrBooleanModeChange(self):
        with skippable(), runLocked(self.uiLock):
            state = cmds.getAttr(self.name + '.booleanMode')
            self.boolModeValue = state

            self.updateRowButtons()
            self.updateBoolMode()

    @fx.undoChunk('attrElementEnabledChange')
    def attrElementEnabledChange(self):
        with skippable(), runLocked(self.uiLock):
            enabled = cmds.getAttr(self.name + '.elementEnabled') or []
            for i in xrange(self.itemCount()):
                item = self.itemAt(i)
                item.isOn = enabled[i] if i < len(enabled) else True
            self.repaintList()

    @fx.undoChunk('attrInWorldMeshChange')
    def attrInWorldMeshChange(self):
        with skippable(), runLocked(self.uiLock):
            conns = cmds.listConnections(self.name + '.inWorldMesh') or []
            items = [self.itemAt(i).text() for i in xrange(self.itemCount())]
            if conns == items:
                return
            self.resetView()

# Pivot button
    def uiCenterPivot(self):
        shape = cmds.listConnections(self.name + '.shapeMessage') or []
        if not shape: return
        cmds.select(shape)
        cmds.CenterPivot()

    @fx.undoChunk('enable debug')
    def uiDebugClicked(self):
        debugEnabled = cmds.getAttr(self.name + '.boolDebugEnabled')
        cmds.setAttr(self.name + '.boolDebugEnabled', not debugEnabled)
        self.updateDebug()

# Attr utilities    
    def updateBoolTypes(self):
        boolTypes = cmds.getAttr(self.name + '.booleanType')
        for i in xrange(self.itemCount()):
            self.setIndividualMode(i, boolTypes[i])
        self.repaintList()

    def updateRowButtons(self):
        checked = cmds.getAttr(self.name + '.booleanMode')
        types = cmds.getAttr(self.name + '.booleanType')

        for i in xrange(self.itemCount()):
            enabled = self.isRowBoolEnabled(i, checked)
            item = self.itemAt(i)
            item.setBoolType(types[i])
            item.setBoolButtonsEnabled(enabled)

        self.repaintList()

    def updateShadeState(self):
        for i in xrange(self.itemCount()):
            item = self.itemAt(i)
            item.setVisibility(btapi.nodeVisibility(item.text()))
        self.repaintList()

    def parentRow(self):
        enabled = cmds.getAttr(self.name + '.elementEnabled') or []
        for i in xrange(len(enabled)):
            if enabled[i]:
                return i
        return -1

    def isRowBoolEnabled(self, row, boolMode):
        if boolMode:
            return row > self.parentRow()
        else:
            return row == self.parentRow()

    def updateBoolMode(self):
        checked = cmds.getAttr(self.name + '.booleanMode')
        self.boolModeValue = checked
        if self.boolModeValue:
            self.boolModeSwitch.setImage(fx.getPixmap('Bool_Mode2'))
        else:
            self.boolModeSwitch.setImage(fx.getPixmap('Bool_Mode1'))
        self.updateRowButtons()
        self.repaintList()

    def setIndividualMode(self, row, mode):
        item = self.itemAt(row)
        item.setBoolType(mode)

# Utilities
    def repaintList(self):
        if self.m_lockRepaint: return
        self.dropWidget.listWidget.viewport().repaint()

    def itemAt(self, index):
        return self.dropWidget.listWidget.item(index)

    def itemCount(self):
        return self.dropWidget.listWidget.count()

    def clearItems(self):
        self.dropWidget.listWidget.clear()

    def addItem(self, item):
        self.dropWidget.listWidget.addItem(item)

    def draggedNode(self):
        return self.dropWidget.listWidget.drag_node
        
    def dragStartIndex(self):
        return self.dropWidget.listWidget.drag_row

# UI Events
    @fx.undoChunk('bool mode')
    def uiBoolModeChanged(self):
        with skippable(), runLocked(self.uiLock):
            self.boolModeValue = not self.boolModeValue
            btapi.setBoolMode(self.name, self.boolModeValue)

    @fx.undoChunk('bool edit')
    def uiButtonClicked(self, row, btnName):
        with skippable(), runLocked(self.uiLock):
            if btnName == 'boolType':
                checked = cmds.getAttr(self.name + '.booleanMode')
                boolEnabled = self.isRowBoolEnabled(row, checked)
                if not boolEnabled:
                    return

                parent = self.dropWidget.listWidget
                pos = qt.QCursor.pos()
                pos = qt.QPoint(parent.width() - 48 - 8, 30 * row + 8)
                pos = parent.mapToGlobal(pos)
                selected = 0
                icons = [fx.getPixmap(x) for x in ['Bool_Union', 'Bool_Subtract', 'Bool_Intersect']]

                btn = self.itemAt(row).getButton('boolType')
                highlightable = btn.highlightable
                original = btn.icons[0]

                btn.icons = [btui.depressPixmap(original)]
                btn.highlightable = False
                self.repaintList()

                def choiceSelected(choice):
                    btn.icons = [original]
                    btn.highlightable = highlightable
                    self.repaintList()

                    if choice != -1:
                        if choice == 1: 
                            choice = 0
                        elif choice == 0: 
                            choice = 1
                        checked = cmds.getAttr(self.name + '.booleanMode')
                        boolEnabled = self.isRowBoolEnabled(row, checked)

                        if not boolEnabled: return

                        self.setIndividualMode(row, choice)
                        boolTypes = cmds.getAttr(self.name + '.booleanType')
                        boolTypes[row] = choice
                        btapi.setBoolType(self.name, boolTypes)
                        self.repaintList()  

                btui.ChoiceDropdown.getChoice(parent, pos, 0, icons, choiceSelected)

            elif btnName == 'visibility':
                parent = self.dropWidget.listWidget
                pos = qt.QCursor.pos()
                pos = qt.QPoint(parent.width() - 24 - 8, 30 * row + 8)
                pos = parent.mapToGlobal(pos)
                selected = 0
                icons = [fx.getPixmap(x) for x in ['Bool_Wireframe', 'Bool_Shaded', 'Bool_Hidden']]

                btn = self.itemAt(row).getButton('visibility')
                highlightable = btn.highlightable
                original = btn.icons[0]

                btn.icons = [btui.depressPixmap(original)]
                btn.highlightable = False
                self.repaintList()

                def choiceSelected(choice):
                    btn.icons = [original]
                    btn.highlightable = highlightable
                    self.repaintList()

                    if choice != -1:
                        item = self.itemAt(row)
                        item.setVisibility(choice)
                        btapi.setNodeVisibility(item.text(), choice)
                        self.repaintList()
                    
                btui.ChoiceDropdown.getChoice(parent, pos, 0, icons, choiceSelected)

            elif btnName == 'toggleButton':
                checked = cmds.getAttr(self.name + '.booleanMode')
                boolEnabled = self.isRowBoolEnabled(row, checked)

                item = self.itemAt(row)
                enabled = cmds.getAttr(self.name + '.elementEnabled')
                enabled[row] = item.isOn
                btapi.setElementEnabled(self.name, enabled)
                if item.isOn:
                    if boolEnabled:
                        boolTypes = cmds.getAttr(self.name + '.booleanType')
                        item.setBoolType(boolTypes[row])
                        item.setBoolButtonsEnabled(True)
                else:
                    boolTypes = cmds.getAttr(self.name + '.booleanType')
                    item.setBoolType(boolTypes[row])
                    item.setBoolButtonsEnabled(False)
                self.resetView()            

    @fx.undoChunk('remove bool')
    def uiDeleteNode(self, node):
        with skippable(), runLocked(self.uiLock):
            cmds.select(self.name)
            nodes = []
            count = self.itemCount()
            for i in xrange(count):
                nodes.append(self.itemAt(i).text())

            nodes.remove(node)
            btapi.setNodeVisibility(node, 1)

            conns = cmds.listConnections(self.name + '.inWorldMesh', p=True, c=True)
            if not conns: return
            for i in xrange(len(conns) / 2):
                outconn = conns[i*2 + 1]
                inconn = conns[i*2]

                cmds.disconnectAttr(outconn, inconn)

            for n in nodes:
                i = mel.eval('getNextFreeMultiIndex %s 0;' % (self.name + '.inWorldMesh'))
                cmds.connectAttr(n + '.worldMesh', self.name + '.inWorldMesh[%d]' % i)

            self.resetView()

    @fx.undoChunk('reorder bool')
    def uiReorderNodes(self):
        with skippable(), runLocked(self.uiLock):
            dragNode = self.draggedNode()
            dragStartIndex = self.dragStartIndex()

            nodes = [self.itemAt(i).text() for i in xrange(self.itemCount())]
            newRow = nodes.index(dragNode)

            oldTypes = cmds.getAttr(self.name + '.booleanType')
            oldTypes.insert(newRow, oldTypes.pop(dragStartIndex))
            btapi.setBoolType(self.name, oldTypes)

            oldEnabled = cmds.getAttr(self.name + '.elementEnabled')
            oldEnabled.insert(newRow, oldEnabled.pop(dragStartIndex))
            btapi.setElementEnabled(self.name, oldEnabled)

            conns = cmds.listConnections(self.name + '.inWorldMesh', p=True, c=True)
            if not conns: return

            for i in xrange(len(conns) / 2):
                outconn = conns[i*2 + 1]
                inconn = conns[i*2]

                cmds.disconnectAttr(outconn, inconn)

            for n in nodes:
                i = mel.eval('getNextFreeMultiIndex %s 0;' % (self.name + '.inWorldMesh'))
                cmds.connectAttr(n + '.worldMesh', self.name + '.inWorldMesh[%d]' % i)

            self.resetView()

    @fx.undoChunk('add bool')
    def uiDroppedNode(self, data):
        with skippable(), runLocked(self.uiLock):
            nodes = [x.strip() for x in data.split('\n')]
            if not nodes: return

            node = nodes[0]

            btapi.addMeshToBool(self.name, node)

            self.resetView()

    def fixElementEnabled(self, count):
        '''Update elementEnabled to match number of connected nodes
        '''
        elementEnabled = cmds.getAttr(self.name + '.elementEnabled') or []
        if len(elementEnabled) > count:
            elementEnabled = elementEnabled[:count]
        else:
            elementEnabled += [1 for x in xrange(count - len(elementEnabled))]

        btapi.setElementEnabled(self.name, elementEnabled)
        return elementEnabled

    
    def fixBooleanTypes(self, count):
        '''Update booleanTypes to match number of connected nodes
        '''
        boolTypes = cmds.getAttr(self.name + '.booleanType') or []
        if len(boolTypes) > count:
            boolTypes = boolTypes[:count]
        else:
            boolTypes += [0 for x in xrange(count - len(boolTypes))]

        btapi.setBoolType(self.name, boolTypes)
        return boolTypes

    def updateNodes(self):
        nodes = cmds.listConnections(self.name + '.inWorldMesh')
        self.clearItems()

        if not nodes: return

        count = len(nodes)
        elementEnabled = self.fixElementEnabled(count)
        self.fixBooleanTypes(count)
        
        # Fill widget with items
        for i, n in enumerate(nodes):
            item = btui.BoolItem(n, self.dropWidget.listWidget)
            nodeColor = None
            rowColor = None

            if not elementEnabled[i]:
                nodeColor = [89, 89, 89]
                rowColor = self.dropWidget.listWidget.rowBGColor
            elif i == self.parentRow():
                nodeColor = [241, 90, 91]
                rowColor = qt.QColor(94, 94, 94)
            else:
                nodeColor = [189, 189, 189]
                rowColor = self.dropWidget.listWidget.rowBGColor

            item.color = qt.QColor(*nodeColor)
            item.rowBGColor = rowColor
            btapi.setNodeOverrideColor(n, nodeColor)

            self.addItem(item)

        self.setupScriptJobs(nodes)
