import sys
from os.path import dirname
from functools import partial
import logging

try:
    from PySide2 import QtCore
    from PySide2.QtWidgets import QMainWindow
except ImportError:
    from PySide import QtCore
    from PySide.QtGui import QMainWindow

logger = logging.getLogger(__name__)


class AbstractMainWindow(QMainWindow):
    '''
    The base QMainWindow class that will wrap the uic-generated class which is fed into it.

    :param class uic_main_window: the Ui_MainWindow class dependent on version of uic used (PySide of PySide2)
    '''
    def __init__(self, uic_main_window, control, app_register_info=('MK DCC', 'Generic App')):
        super(AbstractMainWindow, self).__init__()

        self.ui = uic_main_window()
        self.ui.setupUi(self)

        self._control = control
        self._app_register_info = app_register_info

        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        # Load the QSettings
        self.read_settings()

    def write_settings(self):
        settings = QtCore.QSettings(*self._app_register_info)
        settings.setValue('window_pos', self.pos())  # Window geometry

    def read_settings(self):
        settings = QtCore.QSettings(*self._app_register_info)
        self.move(settings.value('window_pos', QtCore.QPoint(400, 300)))  # Window geometry

    def closeEvent(self, event):
        super(AbstractMainWindow, self).closeEvent(event)

        logger.debug('Saving QSettings of the widget')
        self.write_settings()

    # def select_theme(self, index):
    #     _REPO_path = Path(__file__).parent
    #     _GTRONICK_PATH = 'stylesheets/gtronick/{}.qss'

    #     def get_qss_path(style):
    #         return (_REPO_path / _GTRONICK_PATH.format(style)).as_posix()

    #     if index==0:
    #         self.setStyleSheet('')
    #     elif index==1:
    #         qss_file = QtCore.QFile(get_qss_path('Aqua'))
    #         qss_file.open(QtCore.QFile.ReadOnly | QtCore.QFile.Text)
    #         qss_stream = QtCore.QTextStream(qss_file)
    #         self.setStyleSheet('')
    #         self.setStyleSheet(qss_stream.readAll())
    #         qss_file.close()
    #     elif index==2:
    #         qss_file = QtCore.QFile(get_qss_path('ConsoleStyle'))
    #         qss_file.open(QtCore.QFile.ReadOnly | QtCore.QFile.Text)
    #         qss_stream = QtCore.QTextStream(qss_file)
    #         self.setStyleSheet('')
    #         self.setStyleSheet(qss_stream.readAll())
    #         qss_file.close()
    #     elif index==3:
    #         qss_file = QtCore.QFile(get_qss_path('Ubuntu'))
    #         qss_file.open(QtCore.QFile.ReadOnly | QtCore.QFile.Text)
    #         qss_stream = QtCore.QTextStream(qss_file)
    #         self.setStyleSheet('')
    #         self.setStyleSheet(qss_stream.readAll())
    #         qss_file.close()
