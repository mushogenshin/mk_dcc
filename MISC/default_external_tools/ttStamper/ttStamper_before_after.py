import time
import subprocess
import shutil
from pathlib import Path, PureWindowsPath
from functools import partial
from PySide2 import QtWidgets
from PySide2 import QtCore
from PySide2 import QtGui
import logging

from PIL import Image, ImageDraw, ImageFont

logger = logging.getLogger(__name__)

import ttStamper_utils
from ttStamper_vars import *

# No longer needed as receiving subtitles from user inputs
# _LEFT_SUBTITLE = 'before'
# _RIGHT_SUBTITLE = 'after'

_CONCAT_FILE_SUFFIX = '_bvsa'

_SUBTITLE_HEIGHT_PERCENT = 8
_SUBTITLE_FONT = 'arial.ttf'

_MARGIN_PERCENT = 2

_SCREENSHOT_TEMP_FOLDER = 'C:/Temp/ttStamper'
_SCREENSHOT_TEMP_PREFIX = 'ttStamp'
_SCREENSHOT_TEMP_BEFORE_FILENAME = '_'.join([_SCREENSHOT_TEMP_PREFIX, 'A'])
_SCREENSHOT_TEMP_AFTER_FILENAME = '_'.join([_SCREENSHOT_TEMP_PREFIX, 'B'])
_SCREENSHOT_EXT = '.png'


def ui_init(ui, asset_token):
    hunter_snapshot = import_hunter_snapshot()
    # logger.debug('HUNTER SNAPSHOT:', hunter_snapshot)

    if not hunter_snapshot:
        ui.bvsa_before_screenshot_btn.setDisabled(True)
        ui.bvsa_after_screenshot_btn.setDisabled(True)
        ui.bvsa_before_load_img_btn.setDisabled(True)
        ui.bvsa_after_load_img_btn.setDisabled(True)
    
def create_connections(ui, win):

    graphics_views = (ui.before_graphicsView, ui.after_graphicsView)

    ui.bvsa_clearAll_btn.clicked.connect(partial(
        clear_all,
        graphics_views=graphics_views
    ))

    ui.bvsa_execute_btn.clicked.connect(partial(
        concat_before_vs_after_imgs,
        ui=ui,
        graphics_views=graphics_views
    ))

    ui.bvsa_showResult_btn.clicked.connect(partial(
        show_result,
        graphics_view=ui.before_graphicsView
    ))

    # Screenshot support
    ui.bvsa_before_screenshot_btn.clicked.connect(partial(
        perform_screenshot,
        temp_file_location=_SCREENSHOT_TEMP_FOLDER,
        temp_file_name=_SCREENSHOT_TEMP_BEFORE_FILENAME
    ))
    ui.bvsa_after_screenshot_btn.clicked.connect(partial(
        perform_screenshot,
        temp_file_location=_SCREENSHOT_TEMP_FOLDER,
        temp_file_name=_SCREENSHOT_TEMP_AFTER_FILENAME
    ))

    ui.bvsa_before_load_img_btn.clicked.connect(partial(
        load_img_to_graphics_view,
        graphics_view=ui.before_graphicsView,
        img=(Path(_SCREENSHOT_TEMP_FOLDER) / _SCREENSHOT_TEMP_BEFORE_FILENAME).with_suffix(_SCREENSHOT_EXT)
    ))

    ui.bvsa_after_load_img_btn.clicked.connect(partial(
        load_img_to_graphics_view,
        graphics_view=ui.after_graphicsView,
        img=(Path(_SCREENSHOT_TEMP_FOLDER) / _SCREENSHOT_TEMP_AFTER_FILENAME).with_suffix(_SCREENSHOT_EXT)
    ))

def import_hunter_snapshot():
    try:
        import asset.tools.snapshot as hunter_snapshot
    except ImportError as e:
        logger.error('{}: Opening TT Stamper from Hunter is recommended'.format(e))
        return False
    else:
        logger.debug(hunter_snapshot)
        return hunter_snapshot
        
def perform_screenshot(temp_file_location, temp_file_name):
    hunter_snapshot = import_hunter_snapshot()

    # Prepare output folder
    Path(temp_file_location).mkdir(parents=True, exist_ok=True)

    # Prepare Greenshot
    hunter_snapshot.kill_greenshot()
    update_greenshot_config(
        hunter_snapshot, 
        temp_file_location,
        temp_file_name
    )
    hunter_snapshot.launch_greenshot()

    # time.sleep(2)
    hunter_snapshot.press_print_screen()

def load_img_to_graphics_view(graphics_view, img):
    # Load image to corresponding graphicsView
    # logger.debug('Screenshot will be loaded into {}'.format(graphics_view))
    logger.debug('Attempting to load image: {}'.format(img))
    if img.is_file():
        graphics_view.load_new_img_to_graphic_view(img)

def update_greenshot_config(snapshot, output_folder, output_file_name):

    if not snapshot.GREENSHOT_CFG_PATH.exists():
        shutil.copyfile(snapshot._SNAPSHOT_CFG['DEFAULT_GREENSHOT_CFG'], snapshot.GREENSHOT_CFG_PATH.as_posix())

    cfg = snapshot._read_config(snapshot.GREENSHOT_CFG_PATH)

    # Setting the options
    snapshot._set_cfg_option(cfg, 'Core', 'OutputFilePath', str(PureWindowsPath(output_folder)))
    snapshot._set_cfg_option(cfg, 'Core', 'OutputFileFilenamePattern', output_file_name)
    snapshot._set_cfg_option(cfg, 'Core', 'RegionHotkey', snapshot._SNAPSHOT_CFG['REGION_HOTKEY'])

    with open(snapshot.GREENSHOT_CFG_PATH.as_posix(), 'w') as f:
        cfg.write(f, space_around_delimiters=0)
        logger.info('Updated Greenshot settings for TT Stamper Before vs. After tool.')
        return True

def qrect_to_confined_PIL_box(qrect, img_size):
    '''
    Convert Qt (x, y, width, height) system to Pillow (left, upper, right, lower) system
    '''
    x, y, width, height = qrect.getRect()
    x = max(0, x)
    y = max(0, y)
    return x, y, x + min(width, img_size[0]), y + min(height, img_size[1])

def concat_before_vs_after_imgs(ui, graphics_views, gap_width=5):
    '''
    :param int gap_width: gap width between two images
    '''
    MASTER_CFG = ui.MasterConfig

    _SUBTITLE_FILL = MASTER_CFG[CUST_TXT_FONT_FILL]
    _SUBTITLE_STROKE_WIDTH = MASTER_CFG[CUST_TXT_STROKE_WIDTH]
    _SUBTITLE_STROKE_FILL = MASTER_CFG[CUST_TXT_STROKE_FILL]

    _CONCAT_BCKGRD_COLOR = ui.bvsa_bckgrd_color_btn.user_color  # QColor

    # Unpack the viewports' metadata
    before_url, before_rect = get_viewport_metadata(graphics_views[0])
    after_url, after_rect = get_viewport_metadata(graphics_views[1])

    # Perform the concat using Pillow
    if before_url and after_url:

        # Source images open
        before_img = Image.open(before_url.as_posix())
        after_img = Image.open(after_url.as_posix())

        is_before_rgba = before_img.mode in ttStamper_utils._RGBA_MODES
        is_after_rgba = after_img.mode in ttStamper_utils._RGBA_MODES

        if is_before_rgba:
            before_img.load()

        if is_after_rgba:
            after_img.load()

        # Overwrite with crop specs
        before_img = before_img.crop(qrect_to_confined_PIL_box(before_rect, before_img.size))
        after_img = after_img.crop(qrect_to_confined_PIL_box(after_rect, after_img.size))

        # Apply height matching to the smaller image
        cropped_height_ratio = before_img.height / after_img.height
        if cropped_height_ratio < 1:
            # Scale the first image
            before_img = before_img.resize(
                (round(before_img.width / cropped_height_ratio), after_img.height), 
                resample=Image.LANCZOS
            )
            concat_height = after_img.height
        else:
            # Scale the second image
            after_img = after_img.resize(
                (round(after_img.width * cropped_height_ratio), before_img.height), 
                resample=Image.LANCZOS
            )
            concat_height = before_img.height

        # Prepare final image
        concat_size = (
            before_img.width + after_img.width + gap_width, 
            concat_height
        )

        concat_img = Image.new(
            ttStamper_utils._RGB_MODE, 
            concat_size, 
            (_CONCAT_BCKGRD_COLOR.red(), _CONCAT_BCKGRD_COLOR.green(), _CONCAT_BCKGRD_COLOR.blue())
        )

        # Paste the source images
        if not is_before_rgba:
            concat_img.paste(before_img, (0, 0))
        else:
            concat_img.paste(before_img, (0, 0), before_img)

        if not is_after_rgba:
            concat_img.paste(after_img, (before_img.width + gap_width, 0))
        else:
            concat_img.paste(after_img, (before_img.width + gap_width, 0), after_img)

        ################################################################################################
        # Add the subtitles

        subtitle_font = ImageFont.truetype(
            _SUBTITLE_FONT, 
            round(concat_height * _SUBTITLE_HEIGHT_PERCENT / 100)
        )

        _CAPTION_MARGIN = round(concat_height * _MARGIN_PERCENT / 100)

        left_img_text = ui.bvsa_before_plainTextEdit.toPlainText()
        right_img_text = ui.bvsa_after_plainTextEdit.toPlainText()

        left_img_text_size = subtitle_font.getsize_multiline(
            text=left_img_text, 
            stroke_width=_SUBTITLE_STROKE_WIDTH
        )

        right_img_text_size = subtitle_font.getsize_multiline(
            text=right_img_text, 
            stroke_width=_SUBTITLE_STROKE_WIDTH
        )

        def get_subtitles_hpos_offset(align='center'):
            if align == 'center':
                # incorporating subtitle contents
                before_subtitle_hpos = (before_img.width - left_img_text_size[0]) / 2
                after_subtitle_hpos = (after_img.width - right_img_text_size[0]) / 2 + before_img.width + gap_width
                return before_subtitle_hpos, after_subtitle_hpos
            elif align == 'left':
                return _CAPTION_MARGIN, before_img.width + gap_width + _CAPTION_MARGIN

        subtitles_hpos = get_subtitles_hpos_offset(align=ui.bvsa_caption_align_comboBox.currentText())

        # Support for Top Banner
        if ui.bvsa_caption_banner_checkBox.isChecked():
            # Create new PIL image where text height and margin are added to its height
            additional_height = max(left_img_text_size[1], right_img_text_size[1]) + 2 * _CAPTION_MARGIN
            img_w_banner = Image.new(
                ttStamper_utils._RGB_MODE, 
                (concat_size[0], concat_height + additional_height), 
                (_CONCAT_BCKGRD_COLOR.red(), _CONCAT_BCKGRD_COLOR.green(), _CONCAT_BCKGRD_COLOR.blue())
            )
            # Paste the concatenated images below the additional height
            img_w_banner.paste(concat_img, (0, additional_height))
            # Overwrite the old one
            concat_img = img_w_banner

        # Pillow draw context
        draw_context = ImageDraw.Draw(concat_img)

        # Draw left subtitle
        draw_context.multiline_text(
            (subtitles_hpos[0], _CAPTION_MARGIN), 
            left_img_text,
            font=subtitle_font,
            fill=_SUBTITLE_FILL,
            stroke_width=_SUBTITLE_STROKE_WIDTH,
            stroke_fill=_SUBTITLE_STROKE_FILL,
            align=ALIGN_CENTER
        )

        # Draw right subtitle
        draw_context.multiline_text(
            (subtitles_hpos[1], _CAPTION_MARGIN), 
            right_img_text,
            font=subtitle_font,
            fill=_SUBTITLE_FILL,
            stroke_width=_SUBTITLE_STROKE_WIDTH,
            stroke_fill=_SUBTITLE_STROKE_FILL,
            align=ALIGN_CENTER
        )

        # DEBUG
        # concat_img.show()

        # # TODO: clamp final image to certain size

        # Output the concat image
        output_url = before_url.with_name(before_url.stem + _CONCAT_FILE_SUFFIX + ttStamper_utils._JPG_EXT)

        try:
            concat_img.save(output_url.as_posix())
        except Exception as e:
            print('Unable to output image due to: {}'.format(e))
        else:
            # updates the progress bar
            ui.performStamp_progressBar.setValue(100)
            print('Concatenating before vs. after images successfully')

def get_viewport_metadata(graphics_view):
    return graphics_view._IMG_PATH, get_viewport_rect(graphics_view)

def get_viewport_rect(graphics_view):
    viewport_rect = graphics_view.viewport().geometry()  # return QRect of viewport QWidget
    # Map to scene
    viewport_polygon = graphics_view.mapToScene(viewport_rect).toPolygon()  # has 4 QPoint
    return viewport_polygon.boundingRect()

def show_result(graphics_view):
    output_path = graphics_view._IMG_PATH

    if output_path:
        subprocess.Popen(['explorer', str(PureWindowsPath(output_path.parent))])

def clear_all(graphics_views):
    for graphics_view in graphics_views:
        graphics_view.clear_scene()
