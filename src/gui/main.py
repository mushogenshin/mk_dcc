import sys
from os.path import dirname
from functools import partial
import logging as logger

PYTHON2 = True if sys.version_info.major < 3 else False
QT_VERSION = 4

try:
    from PySide2 import QtCore
    from PySide2.QtWidgets import QMainWindow, QWidget
except ImportError:
    from PySide import QtCore
    from PySide.QtGui import QMainWindow, QWidget
else:
    QT_VERSION = 5


MK_DCC_ROOT = dirname(dirname(dirname(__file__)))

VIEW_QT_FILE = 'view_qt5.py' if QT_VERSION > 4 else 'view_qt4.py'
VIEW_QT_FILE = MK_DCC_ROOT + '/src/gui/' + VIEW_QT_FILE

if not PYTHON2:
    from importlib.machinery import SourceFileLoader
    view_qt = SourceFileLoader('mk_dcc_view_qt', VIEW_QT_FILE).load_module()

    from pathlib import Path
else:
    import imp
    view_qt = imp.load_source('mk_dcc_view_qt', VIEW_QT_FILE)

    import src.utils
    scandir = src.utils.load_scandir_from_venv()
    pathlib2 = src.utils.load_pathlib2_from_venv()
    import scandir
    from pathlib2 import Path


class MK_DCC(QMainWindow):
    '''
    Main UI
    '''
    def __init__(self):
        '''
        :param class Ui_MK_DCC: generated uic module, dependent on version of uic used (PySide of PySide2)
        '''
        super(MK_DCC, self).__init__()

        self.ui = view_qt.Ui_MK_DCC()
        self.ui.setupUi(self)

        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        # Load the QSettings
        self.read_settings()

        self.create_connections(self.ui)

    def write_settings(self):
        settings = QtCore.QSettings('Virtuos_SPARX', 'MK_DCC')

        # Window geometry
        settings.setValue('window_pos', self.pos())

    def read_settings(self):
        settings = QtCore.QSettings('Virtuos_SPARX', 'MK_DCC')

        # Window geometry
        self.move(settings.value('window_pos', QtCore.QPoint(400, 300)))

    def create_connections(self, ui):

        # logger.info('TODO: create UI connections via Qt signals and slots mechanism')

        ui.theme_comboBox.currentIndexChanged.connect(partial(self.select_theme))

    def select_theme(self, index):
        _REPO_path = Path(__file__).parent
        _GTRONICK_PATH = 'stylesheets/gtronick/{}.qss'

        def get_qss_path(style):
            return (_REPO_path / _GTRONICK_PATH.format(style)).as_posix()

        if index==0:
            self.setStyleSheet('')
        elif index==1:
            qss_file = QtCore.QFile(get_qss_path('Aqua'))
            qss_file.open(QtCore.QFile.ReadOnly | QtCore.QFile.Text)
            qss_stream = QtCore.QTextStream(qss_file)
            self.setStyleSheet('')
            self.setStyleSheet(qss_stream.readAll())
            qss_file.close()
        elif index==2:
            qss_file = QtCore.QFile(get_qss_path('ConsoleStyle'))
            qss_file.open(QtCore.QFile.ReadOnly | QtCore.QFile.Text)
            qss_stream = QtCore.QTextStream(qss_file)
            self.setStyleSheet('')
            self.setStyleSheet(qss_stream.readAll())
            qss_file.close()
        elif index==3:
            qss_file = QtCore.QFile(get_qss_path('Ubuntu'))
            qss_file.open(QtCore.QFile.ReadOnly | QtCore.QFile.Text)
            qss_stream = QtCore.QTextStream(qss_file)
            self.setStyleSheet('')
            self.setStyleSheet(qss_stream.readAll())
            qss_file.close()

    def closeEvent(self, event):
        super(MK_DCC, self).closeEvent(event)

        logger.debug('Saving QSettings of the widget')
        self.write_settings()


# if __name__ == '__main__':
#     pass
