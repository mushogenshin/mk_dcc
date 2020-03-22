from pathlib import Path
from PySide2 import QtCore
from PySide2 import QtWidgets
from PySide2 import QtGui


class TTSGraphicsView(QtWidgets.QGraphicsView):
    '''
    Inherit QGraphicsView to support natural zoom and pan images
    '''
    img_types = ['.jpg', '.jpeg', '.png', '.bmp', '.tga', '.tif']
    IMG_TYPES = [img_typ.upper() for img_typ in img_types]
    img_types.extend(IMG_TYPES)

    def __init__(self, parent):
        super(TTSGraphicsView, self).__init__(parent)

        self._IMG_PATH = None  # placeholder to the image path
        self._PIXMAP = None

        self.setBackgroundBrush(QtGui.QBrush(QtGui.QColor(191, 191, 191)))

        # Create QGraphicsScene to add graphic items into
        self._GRAPHICS_SCENE = QtWidgets.QGraphicsScene(self)
        self.setScene(self._GRAPHICS_SCENE)

        # these are already set in the .ui file
        # self.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)
        # self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        # self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        # self.setTransformationAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        # self.setResizeAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)

    def wheelEvent(self, wheel_event):
        angle_delta = wheel_event.angleDelta().y()
        zoom_factor = 1.1 if angle_delta > 0 else .909

        self.scale(zoom_factor, zoom_factor)

    def dragEnterEvent(self, drag_event):
        if drag_event.mimeData().hasUrls():  # accept URLs only
            drag_event.acceptProposedAction()

    # MUST HAVE THIS FOR THE DROP TO WORK
    def dragMoveEvent(self, drag_move_event):
        # super(TTSGraphicsView, self).dragMoveEvent(drag_move_event)
        pass

    def dragLeaveEvent(self, drag_leave_event):
        # super(TTSGraphicsView, self).dragLeaveEvent(drag_leave_event)
        pass

    def dropEvent(self, drop_event):
        mime_data = drop_event.mimeData()

        if mime_data.hasUrls():
            drop_event.accept()

            for url in mime_data.urls():
                url_path = Path(url.toLocalFile())
                if url_path.is_file() and url_path.suffix in TTSGraphicsView.img_types:
                    self.load_new_img_to_graphic_view(url_path)
                # Just accept the first dropped item
                break
    
    def clear_scene(self):
        self._GRAPHICS_SCENE.clear()

    def load_new_img_to_graphic_view(self, url_path):
        self._IMG_PATH = url_path
        
        self.clear_scene()
        # Add the dropped image into scene
        new_pixmap_item = QtWidgets.QGraphicsPixmapItem(QtGui.QPixmap(url_path.as_posix()))
        self._GRAPHICS_SCENE.addItem(new_pixmap_item)
        self._GRAPHICS_SCENE.update()

        self._PIXMAP = new_pixmap_item.pixmap()

        self.fit_view()
        return self._PIXMAP

    def fit_view(self):

        viewport_rect = self.viewport().geometry()
        img_rect_scaled = self.transform().mapRect(self._PIXMAP.rect())

        scale_factor  = max(
            img_rect_scaled.width() / viewport_rect.width(),
            img_rect_scaled.height() / viewport_rect.height()
        )

        self.scale(1 / scale_factor, 1 / scale_factor)

        self._GRAPHICS_SCENE.setSceneRect(self._PIXMAP.rect())
