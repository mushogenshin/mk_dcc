import sys
import os
import time
from pathlib import Path
from functools import partial
import subprocess
import logging as logger

try:
    from PySide2 import QtWidgets, QtCore, QtGui
except ImportError:
    _PYSIDE2_PATH = 'C:/vsTools2/library/python_module/PySide2-5.11.1'
    sys.path.append(_PYSIDE2_PATH)
    from PySide2 import QtWidgets, QtCore, QtGui

_SVN_PILLOW_PATH = 'C:/vsTools2/library/python_module/Pillow-6.2.0/'
sys.path.append(_SVN_PILLOW_PATH)
from PIL import Image, ImageDraw, ImageFont

########################################################################################################################
logger.basicConfig(format='%(levelname)s: %(message)s: %(funcName)s: %(name)s',
    level=logger.DEBUG
)

from ttStamper_presets import TTStamperMainWindow
from ttStamper_vars import *
import ttStamper_utils

import ttStamper_before_after as ttSt_bvsa
import ttStamper_videos as ttSt_videos


def TTStamper_launch():

    TTStamperApp = QtWidgets.QApplication(sys.argv)

    if len(sys.argv) > 1:
        asset_token = eval(sys.argv[-1])  # a dict
    else:
        asset_token = {}
    
    logger.info('Asset token received from Hunter: {}'.format(asset_token))

    TTStamperWin = TTStamperMainWindow()

    ui_init(TTStamperWin.ui, asset_token)
    create_all_connections(TTStamperWin.ui, TTStamperWin)
            
    TTStamperWin.show()    
    sys.exit(TTStamperApp.exec_())


def parse_asset_token_to_ui(ui, asset_token):

    if asset_token:
        ui.text1_plainTextEdit.setPlainText(asset_token.get('asset_name', ''))
        # ui.text1_comboBox.setCurrentIndex()  # by default the first index is already TopLeft


def ui_init(ui, asset_token):

    populate_combo_boxes(ui)
    get_ui_settings(ui)
    parse_asset_token_to_ui(ui, asset_token)
    # print_config_as_plain_text(ui)

    # "Before vs. After" tab
    ttSt_bvsa.ui_init(ui, asset_token)

    ui.bvsa_bckgrd_color_btn.user_color = QtGui.QColor(189, 28, 70)
    ui.bvsa_bckgrd_color_btn.setStyleSheet('background-color: {}'.format(
        ui.bvsa_bckgrd_color_btn.user_color.name()
    ))

    # # "Clamp Video Size" tab
    # ttSt_videos.ui_init(ui, asset_token)


def create_all_connections(ui, win):

    create_grpBx_connections(ui)

    ui.basicTemplate_removeBtn.clicked.connect(partial(
        remove_list_wdg_items, 
        list_wdg=ui.basicTemplate_listWdg
    ))

    ui.theme_comboBox.currentIndexChanged.connect(partial(
        select_theme, 
        win=win
    ))

    ui.browseOutput_btn.clicked.connect(partial(
        browse_output, 
        ui=ui, 
        parent=ui.centralWdg, 
        btn=ui.browseOutput_btn
    ))

    ui.stampAll_btn.clicked.connect(partial(
        get_setting_n_stamp_all,
        ui=ui
    ))

    ui.srcOverwrite_checkBox.toggled.connect(partial(
        disable_browse_output, 
        ui=ui
    ))

    # "Before vs. After" tab
    ui.mainTabWidget.currentChanged.connect(partial(
        disable_normal_stamp_btns,
        ui=ui
    ))

    ttSt_bvsa.create_connections(ui, win)
    
    # "Videos" tab
    ttSt_videos.create_connections(ui, win)

    # Unify Output Dimensions controls
    ui.unifyOutputs_checkBox.toggled.connect(partial(
        enable_unify_output_dimensions,
        ui=ui
    ))

    # "Config" tab
    ui.bvsa_bckgrd_color_btn.clicked.connect(partial(
        bvsa_set_bckgrd_color,
        ui=ui
    ))


def disable_normal_stamp_btns(tab_index, ui):
    disabled = False
    
    if tab_index in (3, 4):  # "Before vs. After" and "Clamp" tabs
        disabled = True
    
    # Disable all widgets in the Execute GrpBx
    for widget in ui.execute_grpBx.findChildren(QtWidgets.QWidget):
        if not isinstance(widget, QtWidgets.QProgressBar):
            widget.setDisabled(disabled)

    # Manually update the Browse Output btn
    overwrite_mode = ui.srcOverwrite_checkBox.isChecked()
    if overwrite_mode:
        disable_browse_output(overwrite_mode, ui=ui)


def populate_combo_boxes(ui):
    for pos in ui.MasterConfig[CUST_TXT_POS].keys():
        ui.text1_comboBox.addItem(pos)
        ui.text2_comboBox.addItem(pos)
        ui.text3_comboBox.addItem(pos)
        ui.text4_comboBox.addItem(pos)

    # helper for setting position at 4 corners of an image
    ui.text1_comboBox.setCurrentIndex(0)
    ui.text2_comboBox.setCurrentIndex(1)
    ui.text3_comboBox.setCurrentIndex(3)
    ui.text4_comboBox.setCurrentIndex(5)


def get_ui_settings(ui):

    margin_size = ui.marginSize_spinBox.value()
    ui.MasterConfig[CUST_TXT_MARGIN] = (margin_size, margin_size)

    ui.MasterConfig[CUST_TXT_FONT_SIZE] = ui.customTxtFontSize_spinBox.value()
    ui.MasterConfig[CUST_TXT_STROKE_WIDTH] = ui.strokeWidth_spinBox.value()

    ui.MasterConfig[METADATA_TXT][AUTO_DATE][0][2] = ui.autoDateFrontSize_spinBox.value()


def get_setting_n_stamp_all(ui):
    get_ui_settings(ui=ui)
    ttStamper_utils.stamp_all(ui=ui)


def print_config_as_plain_text(ui):
    for k, v in ui.MasterConfig.items():
        ui.configPlainTextEdit.insertPlainText("{0} = {1}\n\n".format(k, v))


def create_grpBx_connections(ui):

    all_group_boxes = ui.centralWdg.findChildren(QtWidgets.QGroupBox)
    basicTemplate_grpBx = ui.centralWdg.findChild(QtWidgets.QGroupBox, "basicTemplate_grpBx")

    # all_group_boxes = [grpBx for grpBx in all_group_boxes if grpBx not in (basicTemplate_grpBx,)]
    all_group_boxes.remove(basicTemplate_grpBx)

    for grp_box in all_group_boxes:
        connect_list_wdg_reset_btn(grp_box)
           

def connect_list_wdg_reset_btn(grpBx):
    reset_btn = grpBx.findChild(QtWidgets.QPushButton)
    list_wdg = grpBx.findChild(QtWidgets.QListWidget)

    if list_wdg and reset_btn:
        reset_btn.clicked.connect(list_wdg.clear)

        return reset_btn, list_wdg
    else:
        return None, None


def remove_list_wdg_items(list_wdg):

    selected_items = list_wdg.selectedItems()

    for item in selected_items:
        item_index = list_wdg.indexFromItem(item)
        list_wdg.takeItem(item_index.row())


def select_theme(index, win):
    _REPO_path = Path(__file__).parent
    _QDARKSTYLE_PATH = 'C:/vsTools2/GFP2/python/asset/frontend/desktop_gui/style'
    _GTRONICK_PATH = 'stylesheets/gtronick/{}.qss'

    sys.path.append(_QDARKSTYLE_PATH)
    import qdarkstyle

    def get_qss_path(style):
        return (_REPO_path / _GTRONICK_PATH.format(style)).as_posix()

    if index==0:
        win.setStyleSheet('')
    elif index==1:
        win.setStyleSheet('')
        win.setStyleSheet(qdarkstyle.load_stylesheet())
    elif index==2:
        qss_file = QtCore.QFile(get_qss_path('Aqua'))
        qss_file.open(QtCore.QFile.ReadOnly | QtCore.QFile.Text)
        qss_stream = QtCore.QTextStream(qss_file)
        win.setStyleSheet('')
        win.setStyleSheet(qss_stream.readAll())
        qss_file.close()
    elif index==3:
        qss_file = QtCore.QFile(get_qss_path('ConsoleStyle'))
        qss_file.open(QtCore.QFile.ReadOnly | QtCore.QFile.Text)
        qss_stream = QtCore.QTextStream(qss_file)
        win.setStyleSheet('')
        win.setStyleSheet(qss_stream.readAll())
        qss_file.close()
    elif index==4:
        qss_file = QtCore.QFile(get_qss_path('Ubuntu'))
        qss_file.open(QtCore.QFile.ReadOnly | QtCore.QFile.Text)
        qss_stream = QtCore.QTextStream(qss_file)
        win.setStyleSheet('')
        win.setStyleSheet(qss_stream.readAll())
        qss_file.close()


def browse_output(ui, parent, btn):

    output_path = QtWidgets.QFileDialog.getExistingDirectory(parent, 'Select output folder:', 
                                                                ui.MasterConfig[DEFAULT_OUTPUT_DIR])
    
    if output_path:
        btn.user_path = Path(output_path)
        logger.info('Output images will be saved to {}'.format(btn.user_path.as_posix()))


def disable_browse_output(checked, ui):
    ui.browseOutput_btn.setDisabled(checked)


def enable_unify_output_dimensions(checked, ui):
    ui.unifyOutputs_width_spinBox.setEnabled(checked)
    ui.unifyOutputs_height_spinBox.setEnabled(checked)


def bvsa_set_bckgrd_color(ui):
    ui.bvsa_bckgrd_color_btn.user_color = QtWidgets.QColorDialog.getColor()

    if ui.bvsa_bckgrd_color_btn.user_color.isValid():
    
        logger.debug('Background color for "Before vs. After" image set to: {}'.format(
            ui.bvsa_bckgrd_color_btn.user_color.name()
        ))

        # Update the button background color
        ui.bvsa_bckgrd_color_btn.setStyleSheet('background-color: {}'.format(
            ui.bvsa_bckgrd_color_btn.user_color.name()
        ))


if __name__ == '__main__':
    TTStamper_launch()
