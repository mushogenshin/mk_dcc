### See the file "LICENSE.txt" for the full license governing this code.
from flux.imports import *
import flux.core as fx
from flux.core import pix

from copy import deepcopy

class ListWidget(fx.ListButtonWidget):
    def dropEvent(self, event):
        index = self.indexAt(event.pos())
        item = self.itemFromIndex(index)
        qt.QListWidget.dropEvent(self, event)
        self.dataDelegate.dropEvent(event)

    def startDrag(self, supportedActions):
        self.drag_node = self.currentItem().text()
        self.drag_row = self.row(self.currentItem())
        fx.ListButtonWidget.startDrag(self, supportedActions)

    def mousePressEvent(self, event):
        index = self.indexAt(event.pos())

        if event.button() == qt.Qt.RightButton:
            self.actionButtonPressed = False
            qt.QListWidget.mousePressEvent(self,event)
            return

        row = index.row()
        if row < 0:
            self.actionButtonPressed = False
            qt.QListWidget.mousePressEvent(self, event)
            for i in xrange(self.count()):
                item = self.item(i)
                self.setItemSelected(item, False)
            return

        item = self.itemFromIndex(index)
        button = self.getButtonPressed(item, event.pos().x())

        if button is None or button=='dragIndicator' or button=='textField':
            self.actionButtonPressed = False
            qt.QListWidget.mousePressEvent(self,event)
            return

        self.actionButtonPressed = True

        if button=='toggleButton':
            item.setEnabled(not item.isOn)
            self.viewport().update()
            self.dataDelegate.buttonPressed(index, button)
        else:
            self.dataDelegate.buttonPressed(index, button)

    def mouseMoveEvent(self, event):
        fx.ListButtonWidget.mouseMoveEvent(self, event)
        self.setToolTip('')
        if self.hoverOver:
            if self.hoverOver[1] == 'boolType':
                self.setToolTip('Booleans')
            elif self.hoverOver[1] == 'visibility':
                self.setToolTip('Visibility')
            elif self.hoverOver[1] == 'toggleButton':
                self.setToolTip('Enable/Disable')

class BoolItem(fx.ListButtonItem):
    def __init__(self, text, parent, index=None):
        fx.ListButtonItem.__init__(self,text,parent,index)

        self.boolTypeIcons = ['Bool_Subtract', 'Bool_Union', 'Bool_Intersect']
        self.boolTypeNames = ['union', 'diff', 'intersection']
        self.wireframeIcons = ['Bool_Wireframe', 'Bool_Shaded', 'Bool_Hidden']

        icons = decoratedPixmap(self.boolTypeIcons[0])
        self.addButton(icons, 'boolType', alignRight=True)

        icons = decoratedPixmap(self.wireframeIcons[0])
        self.addButton(icons, 'visibility', alignRight=True)

        self.boolType = -1
        self.visibility = 0
        self.boolButtonsDisabled = False

        self.debugIcon = makeCircle(qt.QColor(0,0,0,0))

        shape = text
        self.updateVisibility()

    def setDebugIcon(self, iconId):
        if iconId == 0:
            self.debugIcon = makeCircle(qt.QColor(0,0,0,0))
        elif iconId == 1:
            self.debugIcon = makeCircle(qt.QColor('#7AF259'))
        elif iconId == 2:
            self.debugIcon = makeCircle(qt.QColor('#F2CC59'))

    def updateVisibility(self):
        import booltoolAPI as btapi
        self.setVisibility(btapi.nodeVisibility(self.text()))

    def setBoolType(self, boolType):
        self.boolType = boolType
        typeBtns = ['union', 'diff', 'intersection']
        btn = self.getButton('boolType')
        btn.icons = decoratedPixmap(self.boolTypeIcons[self.boolType])
        if self.boolButtonsDisabled:
            btn.icons = [dimPixmap(p) for p in btn.icons]

    def setVisibility(self, visibility):
        self.visibility = visibility
        btn = self.getButton('visibility')
        btn.icons = decoratedPixmap(self.wireframeIcons[self.visibility])

    def setBoolButtonsEnabled(self, enabled):
        self.boolButtonsDisabled = not enabled
        btn = self.getButton('boolType')
        icons = decoratedPixmap(self.boolTypeIcons[self.boolType])
        if not enabled:
            icons = [dimPixmap(p) for p in icons]
        btn.icons = icons
        btn.highlightable = enabled            

    def setEnabled(self, enabled):
        self.isOn = enabled

class DropListDelegate(fx.ListButtonDelegate):
    def _drawIcon(self, offset, icon, highlighted):
        w = icon.width() / icon.devicePixelRatio()
        h = icon.height() / icon.devicePixelRatio()

        newRect = deepcopy(self._rect)
        newRect.setLeft(self._rect.left() + offset)
        newRect.setTop(self._rect.top() + (newRect.height() - h) / 2.0)
        newRect.setWidth(w)
        newRect.setHeight(h)
        if highlighted: icon = fx.highlightPixmap(icon)
        self._painter.drawPixmap(newRect, icon)

    def paint(self, painter, option, index):
        """ Main entry point of drawing the cell """
        if not index.isValid(): return

        item = self.parent().itemFromIndex(index)
        self._rect = deepcopy(option.rect)
        self._painter = painter

        selected = option.state & qt.QStyle.State_Selected
        bgcolor = None
        if selected:
            bgcolor = option.palette.color(qt.QPalette.Highlight)
        else:
            bgcolor = item.rowBGColor

        self._drawBackground(index.row(), bgcolor, selected, item.isOn)
        self._drawColorBar(item.color)

        buttonName = ''
        if self.parent().hoverOver:
            row, button = self.parent().hoverOver
            if index.row()==row and button is not None:
                buttonName = button

        offset = self.parent().colorBarWidth
        self._drawIcon(offset, fx.fluxIcons['OutlinerDrag'], buttonName=='dragIndicator')
        
        for i, button in enumerate(item._leftButtons):
            self._drawIcon(offset, button.icons[button.state], (buttonName==button.name and button.highlightable))
            offset += self.parent().iconWidth
        
        offset2 = offset + pix(11)
        self._drawIcon(offset2, item.debugIcon, False)
        offset += self.parent().iconWidth
        offset += pix(5)

        self._drawText(offset, item.text(), self.parent().palette().text().color())

        toggleOffset = pix(24) if self.parent().showToggleButton else pix(4)


        offset = self._rect.width() -toggleOffset -len(item._rightButtons) * self.parent().iconWidth
        for i, button in enumerate(item._rightButtons):
            self._drawIcon(offset, button.icons[button.state], (buttonName==button.name and button.highlightable))
            offset += self.parent().iconWidth

        if self.parent().showToggleButton:
            icon = None
            if item.isOn and selected:
                icon = fx.fluxIcons['Enable_Selected']
            elif item.isOn:
                icon = fx.fluxIcons['Enable']
            else:
                icon = fx.fluxIcons['Disable']
            self._drawIcon(self._rect.width()-pix(24), icon, buttonName=='toggleButton')

        self._rect = None

class DropListWidget(qt.QWidget):
    dropped = qt.Signal(str)
    reorder = qt.Signal()
    deleted = qt.Signal(str)
    buttonClicked = qt.Signal(int, str)
    selected = qt.Signal()

    def __init__(self):
        qt.QWidget.__init__(self)
        fx.setVLayout(self)
        self.listWidget = ListWidget()
        self.listWidget.objectName = "MASH_ListWidget"
        self.listWidget.dataDelegate = self
        self.listWidget.setFixedHeight(pix(250))
        self.listWidget.setDefaultDropAction(qt.Qt.MoveAction)
        self.listWidget.setDropIndicatorShown(True)
        self.listWidget.showDropIndicator = True
        self.listWidget.setSelectionMode(qt.QAbstractItemView.SingleSelection)
        self.listWidget.setItemDelegate(DropListDelegate(self.listWidget))
        self.listWidget.iconWidth = pix(24)
        self.layout().addWidget(self.listWidget)

    def dropEvent(self, e):
        if e.mimeData().hasFormat('text/plain'):
            self.dropped.emit(e.mimeData().text())
        else:
            self.reorder.emit()

    def setupTreeMenu(self, treeMenu, position):
        if self.listWidget.currentItem():
            treeMenu.addAction(fx.getIconFromName('trash'), 'Delete', self.deleteNode)

    def deleteNode(self):
        if self.listWidget.currentItem():
            self.deleted.emit(self.listWidget.currentItem().text())

    def selectionChanged(self):
        self.selected.emit()

    def buttonPressed(self, index, buttonName):
        self.buttonClicked.emit(index.row(), buttonName)

    def doubleClick(self, index, buttonName):
        self.buttonClicked.emit(index.row(), buttonName)

    def itemTextChangedAtIndex(self, index, oldValue, newValue):
        return newName

class ToggleButton(fx.ImageButton):
    def __init__(self, imageName, text=''):
        fx.ImageButton.__init__(self, imageName, text, 'right', False)
        self.hasHoverBackground = True
        self.layout().setContentsMargins(0,0,0,0)
        self.hoverBackgroundColor = qt.QColor(90,90,90,255)
        pixmap = fx.getPixmap(imageName)
        self.setImage(pixmap)
        self.setFixedHeight(pix(20))
        self.setFixedWidth(pix(20))
        self.isBtnOn = False

    def setBtnOn(self):
        self.isBtnOn = True
        p = self.palette()
        p.setColor(self.backgroundRole(), qt.QColor(51, 114, 152))
        self.setPalette(p)
        self.hoverBackgroundColor = qt.QColor(qt.QColor(51, 114, 152))

    def setBtnOff(self):
        self.isBtnOn = False
        p = self.palette()
        p.setColor(self.backgroundRole(), qt.QColor(0, 0, 0, 0))
        self.setPalette(p)
        self.hoverBackgroundColor = qt.QColor(90,90,90,255)

    def enterEvent(self, e):
        result = fx.ImageButton.enterEvent(self,e)
        if self.isBtnOn:
            self.setBtnOn()
        else:
            self.setBtnOff()

        return result

    def leaveEvent(self, e):
        result = fx.ImageButton.leaveEvent(self,e)
        if self.isBtnOn:
            self.setBtnOn()
        else:
            self.setBtnOff()
        return result

class ChoiceDropdown(qt.QDialog):
    choiceSelected = qt.Signal(int)
    def __init__(self, parent, pos, selected, icons, callback):
        qt.QDialog.__init__(self, parent=parent)
        self.setWindowFlags(self.windowFlags() | qt.Qt.FramelessWindowHint)
        self.resize(fx.pix(20), fx.pix(60))
        self.setFixedHeight(self.height())
        self.choice = -1
        fx.setVLayout(self, 0,0,0,0,0)
        choices = range(len(icons))
        self.choiceSelected.connect(callback)

        for i in xrange(len(icons)):
            btn = fx.ImageButton(icons[choices[i]])
            btn.clicked.connect(lambda a=choices[i]: self.setChoice(a))
            btn.setFixedHeight(pix(20))
            btn.setFixedWidth(pix(20))
            self.layout().addWidget(btn)

    def showEvent(self, e):
        qt.QDialog.showEvent(self, e)

    def closeWindow(self):
        self.choiceSelected.emit(self.choice)
        self.close()

    def setChoice(self,choice):
        self.choice = choice
        self.closeWindow()

    def focusOutEvent(self, event):
        self.closeWindow()

    @staticmethod
    def getChoice(parent, pos,selected,icons,callback):
        dialog = ChoiceDropdown(parent, pos, selected, icons,callback)
        dialog.move(pos)
        result = dialog.show()
        dialog.setFocus()

def dimPixmap(pixmap):
    img = qt.QImage(pixmap.toImage().convertToFormat(qt.QImage.Format_ARGB32))
    imgh = img.height()
    imgw = img.width()

    for y in range (0, imgh, 1):
        for x in range (0, imgw, 1):
            pixel = img.pixel(x, y);
            highLimit = 205 # value above this limit will just max up to 255
            lowLimit = 70 # value below this limit will not be adjusted
            adjustment = -lowLimit;
            color = qt.QColor(pixel);
            v = color.value()
            s = color.saturation()
            h = color.hue()
            if(v > lowLimit):
                v = v + adjustment
            else:
                v = 0
            v = color.setHsv(h, s, v)
            img.setPixel(x, y, qt.qRgba(color.red(), color.green(), color.blue(), qt.qAlpha(pixel)));

    return qt.QPixmap(img)

def decoratePixmap(original):
    pixmap2 = qt.QPixmap(fx.dpi(20), fx.dpi(20))
    pixmap2.setDevicePixelRatio(original.devicePixelRatio())
    pixmap2.fill(qt.QColor(0, 0, 0, 0))
    painter = qt.QPainter(pixmap2)
    painter.setRenderHint(qt.QPainter.Antialiasing, True)
    painter.setPen(qt.QColor(0, 0, 0, 0))
    painter.setBrush(qt.QColor(0,0,0,0))

    w = original.width() / original.devicePixelRatio()
    h = original.height() / original.devicePixelRatio()

    painter.drawPixmap(0, 0, original)
    painter.drawPixmap(0, 0, fx.getPixmap('Bool_Dropdown'))

    painter.end()

    return pixmap2

def depressPixmap(original):
    pixmap = qt.QPixmap(fx.dpi(20), fx.dpi(20))
    pixmap.setDevicePixelRatio(original.devicePixelRatio())
    pixmap.fill(qt.QColor(42, 42, 42))

    painter = qt.QPainter(pixmap)
    painter.setRenderHint(qt.QPainter.Antialiasing, True)
    painter.setPen(qt.QColor(0, 0, 0, 0))
    painter.setBrush(qt.QColor(0,0,0,0))

    w = original.width() / original.devicePixelRatio()
    h = original.height() / original.devicePixelRatio()

    painter.drawPixmap(0, 0, original)
    painter.end()
    return pixmap

def decoratedPixmap(name):
    original = fx.getPixmap(name)
    original = decoratePixmap(original)

    return [original]

def makeCircle(color):
    pixmap = qt.QPixmap(pix(100),pix(100))
    pixmap.fill(qt.QColor(0,0,0,0))
    painter = qt.QPainter(pixmap)
    painter.setPen(qt.QColor(0,0,0,0))
    painter.setBrush(color)
    painter.drawEllipse(pix(35),pix(35),pix(30),pix(30))
    painter.end()
    return qt.QIcon(pixmap).pixmap(pix(20),pix(20))