import sys
import os
from functools import partial
import logging as logger

try:
    from PySide2 import QtCore
    from PySide2.QtWidgets import QMainWindow, QWidget
    # from shiboken2 import wrapInstance
except ImportError:
    from PySide import QtCore
    from PySide.QtGui import QMainWindow, QWidget
    # from shiboken import wrapInstance


PYTHON2 = True if sys.version_info.major < 3 else False

if not PYTHON2:
    from pathlib import Path
else:
    LIB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'lib')
    sys.path.append(LIB_PATH)
    from pathlib2 import Path


class MK_DCC(QMainWindow):
    '''
    Main UI
    '''
    def __init__(self, Ui_MK_DCC):
        '''
        :param module Ui_MK_DCC: generated uic module, dependent on version of uic used (PySide of PySide2)
        '''
        super(MK_DCC, self).__init__()

        self.ui = Ui_MK_DCC()
        self.ui.setupUi(self)

        self.create_connections(self.ui)

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
