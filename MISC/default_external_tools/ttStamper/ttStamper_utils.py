import sys
import os
import time
import logging
from collections import namedtuple
from PySide2 import QtWidgets, QtCore
from pathlib import Path, PureWindowsPath

from PIL import Image, ImageDraw, ImageFont

logger = logging.getLogger(__name__)

from ttStamper_vars import *
from ttStamper_presets import StampingConfig


ttsListWdgData = namedtuple("ttsListWdgData", ['QUrls', 'StampConfig'])
#example: (list of QUrls, ('Metallic', 'btmMid'))

ttsCustomTxtData = namedtuple("ttsCustomTxtData", ['content', 'pos', 'override_size', 'size'])
# example: ((100, 200), 'hello World', 'topLeft')

_JPG_EXT = '.jpg'
_RGB_MODE = 'RGB'
_RGBA_MODES = ('RGBA',)
_ALPHA_CHANNEL = 'A'


def stamp_all(ui):
    """
    this is called by the 'STAMP ALL' button
    """

    # first processes the 'basic' stamping, i.e. for sources dropped into 'Sources' slot in 'Basic' tab

    basic_sources = get_list_wdg_items(ui.basicSrc_listWdg) 

    templates = get_list_wdg_items(ui.basicTemplate_listWdg)
    custom_texts = get_all_text_setups(ui)

    # if basic_sources.QUrls and (templates.QUrls or custom_texts):
    #     perform_stamp(ui, templates, custom_texts, basic_sources)
    # else:
    #     logger.info('No basic sources and (templates or custom texts) given.\n')
    
    # More relaxed rule, perform conversion even for no Auto-Date nor company logo
    if basic_sources.QUrls:
        perform_stamp(ui, templates, custom_texts, basic_sources)

    ####################################################################################################################

    # then processes the 'advanced' stamping, i.e. for sources dropped into 'ZBrush', 'Substance', etc., tabs 

    # gets all the QListWidget, filtering by whether it has valid 'advanced' stamping config
    adv_list_wdgs = (wdg for wdg in ui.centralWdg.findChildren(QtWidgets.QListWidget) if wdg.stampingConfig)

    # creates generator of tuple of [QUrls, stampingConfig value]
    adv_source_list = (get_list_wdg_items(adv_list_wdg) for adv_list_wdg in adv_list_wdgs)

    # filters by whether any valid file was dropped into
    adv_source_list = filter(lambda x: x[0], adv_source_list)

    for adv_sources in adv_source_list:
        perform_stamp(ui, templates, custom_texts, adv_sources)


def get_all_txt_cfg(ui):
    """
    Provide short-hand dicts and also some pre-made utilities
    """
    MASTER_CFG = ui.MasterConfig
    TXT_POS_CFG = MASTER_CFG[CUST_TXT_POS]
    
    margin = MASTER_CFG[CUST_TXT_MARGIN]

    # Pillow font
    txt_font = ImageFont.truetype(MASTER_CFG[CUST_TXT_FONT], MASTER_CFG[CUST_TXT_FONT_SIZE])
    txt_fill = MASTER_CFG[CUST_TXT_FONT_FILL]
    
    stroke_w = MASTER_CFG[CUST_TXT_STROKE_WIDTH]
    stroke_f = MASTER_CFG[CUST_TXT_STROKE_FILL]

    return MASTER_CFG, TXT_POS_CFG, margin, txt_font, txt_fill, stroke_w, stroke_f


def perform_stamp(ui, templates, custom_texts, sources):
    """
    :parm ui:
    :parm sources, templates: namedtuple ttsListWdgData(QUrls, StampingConfig)
    :parm custom_texts: dict, where key: QPlainTextEdit object; 
                                    value: namedtuple ttsCustomTxtData
    
    """
    MASTER_CFG, TXT_POS_CFG, margin, txt_font, txt_fill, stroke_w, stroke_f = get_all_txt_cfg(ui)

    OVERWRITE_MODE = ui.srcOverwrite_checkBox.isChecked()
    OUTPUT_PATH = ui.browseOutput_btn.user_path  # Path object
    AS_JPG = ui.outputAsJPG_checkBox.isChecked()

    ADV_SOURCE_CFG = sources.StampConfig

    # Query the unify output dimension target
    UNIFY_TARGET_DIMENSIONS = get_target_dimensions_from_ui(ui=ui)
    performs_unify_dimensions = ui.unifyOutputs_checkBox.isChecked()

    # Reset the progress bar
    num_sources = len(sources.QUrls)
    ui.performStamp_progressBar.setValue(0)

    ####################################################################################################################
    # LOOPS OVER EACH SOURCE IMAGE

    for i, source_url in enumerate(sources.QUrls, 1):
        logger.info('--PROCESSING JOB {} OF {}...'.format(i, num_sources))

        source_url = Path(source_url.toLocalFile())

        # Pillow image open
        source_img = Image.open(source_url.as_posix())

        IS_RGBA = source_img.mode in _RGBA_MODES

        if IS_RGBA:
            source_img.load()

        # Get its size
        src_img_size = source_img.size

        # Pillow draw context
        draw_context = ImageDraw.Draw(source_img)

        ################################################################################################################
        # STAMPS ALL THE 'BASIC' TEXTS (CUSTOM + METADATA)
        for txt_wdg_info in custom_texts.values():

            # each txt_wdg_info is a ttsCustomTxtData namedtuple

            txt_pos = txt_wdg_info.pos
            override_font_size = txt_wdg_info.override_size

            if override_font_size != -1:
                # with font size override
                override_txt_font = ImageFont.truetype(MASTER_CFG[CUST_TXT_FONT], override_font_size)
                draw_context.multiline_text(calc_stamp_TopLeft_xy(src_img_size, txt_wdg_info.size, txt_pos, margin),
                                            txt_wdg_info.content, 
                                            font=override_txt_font, fill=txt_fill, 
                                            stroke_width=stroke_w,
                                            stroke_fill=stroke_f,
                                            align=TXT_POS_CFG[txt_pos][0])
            else:
                # no font size override
                draw_context.multiline_text(calc_stamp_TopLeft_xy(src_img_size, txt_wdg_info.size, txt_pos, margin),
                                            txt_wdg_info.content, 
                                            font=txt_font, fill=txt_fill, 
                                            stroke_width=stroke_w,
                                            stroke_fill=stroke_f,
                                            align=TXT_POS_CFG[txt_pos][0])

        ################################################################################################################
        # STAMPS THE 'ADVANCED' TEXT

        if ADV_SOURCE_CFG:
            subtitle_size = draw_context.multiline_textsize(text=ADV_SOURCE_CFG.content, 
                                                            font=txt_font, stroke_width=stroke_w)

            draw_context.multiline_text(calc_stamp_TopLeft_xy(src_img_size, subtitle_size, ADV_SOURCE_CFG.pos, margin),
                                        ADV_SOURCE_CFG.content, 
                                        font=txt_font, fill=txt_fill, 
                                        stroke_width=stroke_w,
                                        stroke_fill=stroke_f,
                                        align=ALIGN_CENTER)

        ################################################################################################################
        # PASTES THE TEMPLATES

        for template_file in templates.QUrls:

            template_file = template_file.toLocalFile()
            template_file = Image.open(template_file)

            # TODO: add support for gigantic templates versus tiny sources

            source_img.paste(template_file, (0, 0), template_file)  # third argv is mask


        ################################################################################################################
        # PASTES THE METADATA IMAGES

        for metadata_type, metadata_cfg in MASTER_CFG[METADATA_IMG].items():

            if metadata_cfg[-1].__call__():  # the QCheckBox

                # metadata_cfg[0]: StampingConfig namedtuple
                percentage = metadata_cfg[0].override_size / 100

                meta_img_path = str(PureWindowsPath(metadata_cfg[0].content))  # works around "PermissionError: [WinError 5] Access is denied"
                meta_img = Image.open(meta_img_path)  # original image

                meta_img_aspect_ratio = meta_img.size[0] / meta_img.size[1]  # width / height
                target_width = src_img_size[0] * percentage

                meta_img_new_size = (round(target_width), round(target_width / meta_img_aspect_ratio))

                meta_img = meta_img.resize(meta_img_new_size, resample=Image.LANCZOS)
                
                source_img.paste(meta_img, 
                                calc_stamp_TopLeft_xy(src_img_size, meta_img.size, metadata_cfg[0].pos, margin),
                                meta_img)  # third argv is mask

        
        ################################################################################################################
        # UNIFY OUTPUT DIMENSIONS
        if performs_unify_dimensions:
        
            if src_img_size != UNIFY_TARGET_DIMENSIONS:
                logger.info('Image dimensions are to be unified as specified.')
                source_img = unify_output_dimensions(source_img, UNIFY_TARGET_DIMENSIONS, IS_RGBA)
                # Update its size
                src_img_size = source_img.size
            else:
                logger.info('Image is already of proper output dimensions.')


        ################################################################################################################
        # SAVES FILE
        if not OVERWRITE_MODE:
            source_url = OUTPUT_PATH / source_url.name

        if AS_JPG:
            source_url = source_url.with_suffix(_JPG_EXT)
            
            # Support for input of RGBA formats
            if IS_RGBA:
                new_img = Image.new(_RGB_MODE, src_img_size, (255, 255, 255))
                new_img.paste(source_img, mask=source_img.getchannel(_ALPHA_CHANNEL))
                source_img = new_img

        try:
            source_img.save(source_url.as_posix())  # TODO: add support auto-incrementing name if file already exists
        except Exception as e:
            logger.warning('Unable to output processed image for file {}'.format())
        else:
            # updates the progress bar
            ui.performStamp_progressBar.setValue(round(i / num_sources * 100))

    # updates the progress bar
    ui.performStamp_progressBar.setValue(100)
    logger.info('***TT STAMPING COMPLETED.\n')


def unify_output_dimensions(orig_img, target_img_size, src_is_rgba=False):

    _BCKGRD_CLR = (0, 0, 0)  # full black
    _BCKGRD_CLR_ALPHA = (0, 0, 0, 255)

    # Start a new img of target_img_size
    if not src_is_rgba:
        new_img = Image.new(_RGB_MODE, target_img_size, _BCKGRD_CLR)
    else:
        new_img = Image.new(_RGBA_MODES[0], target_img_size, _BCKGRD_CLR_ALPHA)
        new_img.load()

    # Paste the orig_img on top
    if not src_is_rgba:
        new_img.paste(orig_img, box=calc_paste_TopLeft_xy(orig_img.size, target_img_size))  # box flag works with negative values
    else:
        dest_offset, source_offset = calc_paste_TopLeft_xy_alpha(orig_img.size, target_img_size)
        new_img.alpha_composite(orig_img, dest_offset, source_offset)

    return new_img


def get_target_dimensions_from_ui(ui):
    return (ui.unifyOutputs_width_spinBox.value(), ui.unifyOutputs_height_spinBox.value())


def calc_paste_TopLeft_xy(src_img_size, target_img_size):
    return round((target_img_size[0] - src_img_size[0]) / 2), round((target_img_size[1] - src_img_size[1]) / 2)


def calc_paste_TopLeft_xy_alpha(src_img_size, target_img_size):
    # Since "dest" and "source" flags of alpha_composite don't work with negative values

    box = calc_paste_TopLeft_xy(src_img_size, target_img_size)
    
    # Width
    if target_img_size[0] >= src_img_size[0]:
        dest_x = box[0]
        source_x = 0
    else:
        dest_x = 0
        source_x = -box[0]
    # Height
    if target_img_size[1] >= src_img_size[1]:
        dest_y = box[1]
        source_y = 0
    else:
        dest_y = 0
        source_y = -box[1]

    return (dest_x, dest_y), (source_x, source_y)


def calc_stamp_TopLeft_xy(src_img_size, stamp_size, stamp_pos, margin):

    # P_TOP_LEFT = 'topLeft'
    # P_TOP_MID = 'topMid'
    # P_TOP_RIGHT = 'topRight'
    # P_BTM_LEFT = 'btmLeft'
    # P_BTM_MID = 'btmMid'
    # P_BTM_RIGHT = 'btmRight'
    # logger.debug('Stamp size: {}'.format(stamp_size))

    x = margin[0]
    y = margin[1]

    # calculates x
    if stamp_pos in (P_TOP_MID, P_BTM_MID):  # dealing if MID
        x = (src_img_size[0] - stamp_size[0]) / 2
    elif stamp_pos in (P_TOP_RIGHT, P_BTM_RIGHT):  # dealing if RIGHT
        x = src_img_size[0] - stamp_size[0] - x

    # calculates y
    if stamp_pos in (P_BTM_LEFT, P_BTM_MID, P_BTM_RIGHT):  # dealing if BTM only
        y = src_img_size[1] - stamp_size[1] - y

    return x, y


def get_all_text_setups(ui, include_meta_txts=True):
    """return: dict{QPlainTextEdit: a namedtuple, ttsCustomTxtData}"""

    MASTER_CFG, TXT_POS_CFG, margin, txt_font, txt_fill, stroke_w, stroke_f = get_all_txt_cfg(ui)

    # image = Image.open(ui.MasterConfig[OWN_LOGO_PATH])  # opens a dummy image
    # draw_context = ImageDraw.Draw(image)

    ####################################################################################################################
    # ACTUAL CUSTOM TEXTS

    all_text_setups = {}

    all_child_grp_boxes = ui.custom_grpBx.findChildren(QtWidgets.QGroupBox)

    # queries all text edits and their combo box
    for grpBx in all_child_grp_boxes:
        text_wdg = grpBx.findChild(QtWidgets.QPlainTextEdit)
        combo_bx = grpBx.findChild(QtWidgets.QComboBox)

        custom_txt = text_wdg.toPlainText()

        if custom_txt:
            logger.debug('Stamping custom text: {}'.format(custom_txt))
            # txt_size = draw_context.multiline_textsize(text=custom_txt, font=txt_font, stroke_width=stroke_w)
            txt_size = txt_font.getsize_multiline(text=custom_txt, stroke_width=stroke_w)
            all_text_setups[text_wdg] = ttsCustomTxtData(custom_txt, combo_bx.currentText(), -1, txt_size)

    ####################################################################################################################
    # METADATA TEXTS

    if include_meta_txts:
        METADATA_TXT_CFG = MASTER_CFG[METADATA_TXT]

        for metadata_type, metadata_cfg in METADATA_TXT_CFG.items():

            if metadata_cfg[-1].__call__():  # the QCheckBox

                # metadata_cfg[0]: a list that needs to be converted to StampingConfig namedtuple
                metadata_cfg_ntuple = StampingConfig._make(metadata_cfg[0])

                meta_txt = metadata_cfg_ntuple.content
                logger.debug('Stamping metadata text: {}'.format(meta_txt))
                meta_override_font_size = metadata_cfg_ntuple.override_size

                if meta_override_font_size != -1:
                    override_txt_font = ImageFont.truetype(MASTER_CFG[CUST_TXT_FONT], meta_override_font_size)
                    meta_txt_size = override_txt_font.getsize_multiline(text=meta_txt, stroke_width=stroke_w)
                else:
                    meta_txt_size = txt_font.getsize(text=meta_txt, stroke_width=stroke_w)

                all_text_setups[metadata_type] = ttsCustomTxtData(meta_txt, metadata_cfg_ntuple.pos, 
                                                                    meta_override_font_size, meta_txt_size)

    return all_text_setups


def get_list_wdg_items(list_wdg):
    """
    :parm list_wdg: QListWidget
    :return: a namedtuple, ttsListWdgData: (list of QUrls, stampingConfig value),
    where stampingConfig=None for basic sources
    """
    return ttsListWdgData([list_wdg.item(i).data(QtCore.Qt.UserRole) 
                                for i in range(list_wdg.count())], list_wdg.stampingConfig)
