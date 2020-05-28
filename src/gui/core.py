import sys
from os.path import dirname
from functools import partial
import logging


logger = logging.getLogger(__name__)
PYTHON2 = True if sys.version_info.major < 3 else False


try:
    from PySide2 import QtCore
    from PySide2.QtWidgets import QMainWindow
except ImportError:
    from PySide import QtCore
    from PySide.QtGui import QMainWindow


if not PYTHON2:
    from pathlib import Path
else:
    import src.utils
    scandir = src.utils.load_scandir_from_venv()
    pathlib2 = src.utils.load_pathlib2_from_venv()
    import scandir
    from pathlib2 import Path


class MK_DCC_AbstractMainWindow(QMainWindow):
    '''
    The base QMainWindow class that will wrap the uic-generated class which is fed into it.

    :param class uic_main_window: the Ui_MainWindow class dependent on version of uic used (PySide of PySide2)
    '''
    def __init__(self, uic_main_window, app_register_info=('MK DCC', 'Base App')):
        '''
        '''
        super(MK_DCC_AbstractMainWindow, self).__init__()

        self.ui = uic_main_window()
        self.ui.setupUi(self)

        self._app_register_info = app_register_info

        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        # Load the QSettings
        self.read_settings()

        self.create_connections(self.ui)

    def write_settings(self):
        settings = QtCore.QSettings(*self._app_register_info)

        settings.setValue('window_pos', self.pos())  # Window geometry

    def read_settings(self):
        settings = QtCore.QSettings(*self._app_register_info)

        self.move(settings.value('window_pos', QtCore.QPoint(400, 300)))  # Window geometry

    def create_connections(self, ui):
        # logger.info('TODO: create UI connections via Qt signals and slots mechanism')
        # ui.theme_comboBox.currentIndexChanged.connect(partial(self.select_theme))
        pass

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

    def closeEvent(self, event):
        super(MK_DCC_AbstractMainWindow, self).closeEvent(event)

        logger.debug('Saving QSettings of the widget')
        self.write_settings()


# if __name__ == '__main__':
#     pass
