"""
hoan.nguyen@virtuosgames.com

_VERSION CONTROL THE OUTPUT ZBRUSH TT

_THIS MODULE GETS CALLED FROM THE ACCOMPANIED "ZINITOOLS" ZPLUGIN, AND

WORKS BY READING THE GENERATED JSON FILE, WHICH CONTAINS ASSET_TOKEN INFO

_MUST BE USING ZBRUSH LAUNCHED FROM HUNTER TO MAKE IT WORK

"""

import sys
import time
import re
import subprocess
import logging
from pathlib import Path, PureWindowsPath

logger = logging.getLogger(__name__)

from hunter_zbrush_talk import app_tt_cfg

def hold_cmd_win(wait_time=15):
    print("\n------------Python called from ZBrush!------------\n\n")
    time.sleep(wait_time)

try:
    from asset.wrangler import common
    from asset.tools.default_external_tools.common import external_tool_utils as ext_utils

    _SVN_PILLOW_PATH = 'C:/vsTools2/library/python_module/Pillow-6.2.0/'
    sys.path.append(_SVN_PILLOW_PATH)
    import PIL.Image

except ImportError:
    logger.warning('Cannot import essential modules. Aborted.')
    hold_cmd_win()
    raise

_IMG_EXT = '.jpg'
_PADDING = 4


def PIL_convert_all_images(working_dir, input_extension='.tif', output_extension=_IMG_EXT):
    """
    :parm Path working_dir:
    :parm Path output_folder: custom output folder, or None
    """
    logger.info('<<< Entering PILLOW land >>>\n***Converting all images found in {}\n'.format(working_dir))

    for orig_image in working_dir.glob('*' + input_extension):

        # opens the image
        pil_orig_img = PIL.Image.open(orig_image.as_posix())
        # writes the output
        output_path = orig_image.with_name(orig_image.stem + output_extension)
        try:
            pil_orig_img.save(output_path.as_posix())
        except Exception as e:
            logger.warning('Unable to convert image "{}" due to: {}.\n'.format(orig_image.name, e))
        # deletes the original image
        orig_image.unlink()

    logger.info('Image conversion is done.\n<<< Leaving PILLOW land >>>\n')


def reverse_spin_direction(working_dir, file_name):
    '''
    :param Path working_dir:
    '''
    # Query all files
    all_files = list(working_dir.glob('*' + _IMG_EXT))

    logging.info('Reversing ZBrush spin direction by reversing file names')

    all_files.reverse()

    for i, current_file in enumerate(all_files):
        current_file.rename(
            current_file.with_name('_'.join([file_name, str(i).zfill(_PADDING)]) + _IMG_EXT)
        )


def do_tt_commit_and_checkout(cfg, do_versioning=True):

    # Load the versioning config from JSON file
    logger.info('***Loading versioning config from JSON file...')
    ASSET_TOKEN = common.load_json(cfg._HUNTER_CUR_PROJ_ASSET_JSON_FP.as_posix())

    tt_output_root_dir = Path(ASSET_TOKEN[cfg._APP_TT_OUTPUT_ROOT_KEY])

    # Do the Pillow conversion
    logger.info('***Performing PILLOW conversion.')
    try:
        PIL_convert_all_images(tt_output_root_dir)
    except:
        pass

    # Reverse spin direction
    try:
        reverse_spin_direction(tt_output_root_dir, ASSET_TOKEN['asset_name'])
    except:
        pass

    if do_versioning:
        # queries the workspace and checkout paths
        logger.info('***PERFORMING VERSIONING...\nQuerying Workspace and Checkout paths...')
        WORKSPACE_PATH = Path(ASSET_TOKEN[cfg._APP_TT_OUTPUT_ROOT_KEY])
        CHECKOUT_PATH = WORKSPACE_PATH.parent

        logger.info('***Committing latest files to repo...')
        ext_utils.do_tt_commit(
            WORKSPACE_PATH, 
            common.REVIEW_SESS, 
            ext_utils._ASSET_FILE_PATTERN
        )
        
        logger.info('***Checking out latest files from repo...')
        ext_utils.do_tt_checkout(
            WORKSPACE_PATH, 
            common.REVIEW_SESS, 
            ext_utils._ASSET_FILE_PATTERN, 
            CHECKOUT_PATH
        )

    
if __name__ == "__main__":
    do_tt_commit_and_checkout(cfg=app_tt_cfg)
    hold_cmd_win()
