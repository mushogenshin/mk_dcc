from pathlib import Path
from PySide2 import QtCore, QtWidgets


class TTSListWidget_Video(QtWidgets.QListWidget):
	def __init__(self, parent):
		super(TTSListWidget_Video, self).__init__(parent)


	media_types = ['.mov', '.mp4']
	MEDIA_TYPES = [media_type.upper() for media_type in media_types]
	media_types.extend(MEDIA_TYPES)


	def dragEnterEvent(self, drag_event):

		if drag_event.mimeData().hasUrls():  # accepts URLs only
			drag_event.acceptProposedAction()


	def dragMoveEvent(self, drag_event):
		# MUST HAVE THIS FOR THE DROP TO WORK
		pass


	def dropEvent(self, drop_event):

		mime_data = drop_event.mimeData()

		if mime_data.hasUrls():
			drop_event.accept()

			for url in mime_data.urls():
				url_path = Path(url.toLocalFile())
				if url_path.is_file() and url_path.suffix in TTSListWidget_Video.media_types:
					
					list_wdg_item = QtWidgets.QListWidgetItem(url.fileName())
					list_wdg_item.setData(QtCore.Qt.UserRole, url)

					list_wdg_item.setToolTip(url.toLocalFile())

					self.addItem(list_wdg_item)
