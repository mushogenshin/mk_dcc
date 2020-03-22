"""
hoan.nguyen@virtuosgames.com

MARMOSET TURNTABLE PLUGIN

A copy of this script must reside in C:/Users/[username]/AppData/Local/Marmoset Toolbag 3/plugins

"""

import sys
import os
import subprocess
import json
import time
from pathlib import Path, PureWindowsPath
from functools import partial

import mset


class CUSTOM_CFG:

    _HUNTER_CUR_PROJ_ASSET_JSON_FP = Path('C:/Temp') / 'HUNTER_current_proj_asset.json'
    _VERSIONING_MODULE = Path('C:/vsTools2/SPD/python/asset/tools/default_external_tools/MarmoSmart/hunter_marmoset_tt_versioning.py')

    _TT_ROOT_KEY = 'marmoset_tt_root'
    _TT_WORKSPACE_KEY = 'marmoset_tt_workspace'

    # Toolbag PyTurntableObject
    _TT_OBJ_NAME = 'STWookiees_Turntable'
    _TT_OBJ_TYPE = 'turntable'
    _TT_OBJ_SPINRATE = -18.0  # spin degrees in each second,
    # Marmoset default timeline length is 20.0 seconds, so this spinrate equals one full turn
    # Negative value is to conform to Maya and Mari turntable spin directions
    
    # Toolbag Timeline
    _OUT_NUM_FRAMES = 60

    # Toolbag Video
    _TT_WIDTH = 1920
    _TT_HEIGHT = 1080
    _TT_SAMPLING = 100
    _TT_TRANSPARENCY = False

    _MOV_EXT = '.jpg'


class UI_CFG:
    # Toolbag UI
    _VERSION = '0.0.4'
    _TITLE = 'StoryTellingWOOKIEES*  Marmoset  Turntabler'

    _SETUP_BTN_LABEL = 'Step 1: Setup Turntable'
    _SETUP_BTN_TOOLTIP = '<<< Press the button'
    _SETUP_LABEL_TXT = '\nStep 2:  Please manually parent the group to\n\
the generated "{}"\n'

    _EXECUTE_BTN_LABEL = 'Step 3: Export Turntable'
    _OPEN_OUTPUT_LABEL = 'Open Output'
    _CLOSE_BTN_LABEL = 'Close  [  X  ]'
    
#######################################################################################################

def setup_timeline(cfg):

    current_totalFrames = _TIMELINE_SINGLETON.totalFrames
    current_framerate = _TIMELINE_SINGLETON.getFrameRate()  # Marmoset default is 30.0 fps

    _RESAMPLE_FPS_FACTOR = current_totalFrames / cfg._OUT_NUM_FRAMES  # n times smaller
    _RESAMPLE_FPS = current_framerate / _RESAMPLE_FPS_FACTOR  # n times smaller
    
    # Resample the FPS to reduce the amount of frames to render
    if current_framerate != _RESAMPLE_FPS:
        _TIMELINE_SINGLETON.resample(_RESAMPLE_FPS)

    return _RESAMPLE_FPS


def create_single_sceneObj(cfg, name, type):

    found = mset.findObject(name)  # only return first object it finds

    if not found:
        if type == cfg._TT_OBJ_TYPE:
            found = mset.PyTurntableObject(name=name, spinRate=cfg._TT_OBJ_SPINRATE)
    else:
        print('Object "{}"" already exists. Skipped.'.format(name))

    return found

def create_single_turntable(cfg):
    
    turntable = create_single_sceneObj(
        cfg=cfg, 
        name=cfg._TT_OBJ_NAME, 
        type=cfg._TT_OBJ_TYPE
    )

    # Conform the timeline setup
    resample_fps = setup_timeline(cfg)

    return turntable

def export_video(cfg, asset_token, tt_root):

    output_video_fp = tt_root / (asset_token['asset_name'] + cfg._MOV_EXT)

    mset.exportVideo(path=output_video_fp.as_posix(), 
                    width=cfg._TT_WIDTH,
                    height=cfg._TT_HEIGHT,
                    sampling=cfg._TT_SAMPLING,
                    transparency=cfg._TT_TRANSPARENCY)

    # return output_video_fp, resample_fps


def call_versioning(cfg, asset_token):

    cmd = 'C:/vsTools2/VsRunner.bat {} python3.7.0 {} {}'.format(asset_token['vsproject'],
                                                                cfg._VERSIONING_MODULE.as_posix(),
                                                                asset_token[cfg._TT_WORKSPACE_KEY])
    
    try:
        subprocess.call(cmd)
    except Exception as e:
        print('Failed to call versioning module due to {}'.format(e))
    else:
        print('Called versioning module successfully.')


def load_json(json_path, verbose=0):
    if not os.path.exists(json_path):
        json_dir = os.path.dirname(json_path)
        if not os.path.exists(json_dir):
            os.makedirs(json_dir)
        with open(json_path, 'w') as file:
            data = {}
            json.dump(data, file, indent=4, sort_keys=True)
    data_dict = {}

    with open(json_path) as file:
        data_dict = json.loads(file.read())
        if verbose:
            print('Loaded data from JSON successfully : {}'.format(json_path))
    return data_dict


def reread_json(cfg):

    asset_token = load_json(cfg._HUNTER_CUR_PROJ_ASSET_JSON_FP.as_posix())
    tt_root_dir = Path(asset_token[cfg._TT_ROOT_KEY])

    if not tt_root_dir.exists():
        try:
            tt_root_dir.mkdir(parents=True)
        except Exception as e:
            print('Unable to create folder {} due to: {}'.format(tt_root_dir, e))

    return asset_token, tt_root_dir


def do_tt(cfg):

    _HUNTER_ASSET_TOKEN, _MARMOSET_TT_ROOT = reread_json(cfg)

    export_video(cfg, _HUNTER_ASSET_TOKEN, _MARMOSET_TT_ROOT)
    call_versioning(cfg, _HUNTER_ASSET_TOKEN)

    return True


def open_output(cfg):

    _HUNTER_ASSET_TOKEN, _MARMOSET_TT_ROOT = reread_json(cfg)

    output_dir = str(PureWindowsPath(_MARMOSET_TT_ROOT))
    subprocess.Popen(['explorer', output_dir])


#######################################################################################################
# ENTRY

# Get the Singleton Timeline
_TIMELINE_SINGLETON = mset.getTimeline()

# Partial functions for UI
do_create_turntable = partial(create_single_turntable, cfg=CUSTOM_CFG)
do_make_turntable = partial(do_tt, cfg=CUSTOM_CFG)
do_open_output = partial(open_output, cfg=CUSTOM_CFG)

#######################################################################################################
# MARMOSET UI

# Create the UI
tbtt_window = mset.UIWindow(name='{}  v{}'.format(UI_CFG._TITLE, UI_CFG._VERSION))

# Buttons
setup_btn = mset.UIButton(name=UI_CFG._SETUP_BTN_LABEL)
setup_btn_tooltip = mset.UILabel(name=UI_CFG._SETUP_BTN_TOOLTIP)
setup_btn_label = mset.UILabel(name=UI_CFG._SETUP_LABEL_TXT.format(CUSTOM_CFG._TT_OBJ_NAME))

export_btn = mset.UIButton(name=UI_CFG._EXECUTE_BTN_LABEL)
open_output_btn = mset.UIButton(name=UI_CFG._OPEN_OUTPUT_LABEL)

close_btn = mset.UIButton(name=UI_CFG._CLOSE_BTN_LABEL)

# Layout
tbtt_window.addReturn()
tbtt_window.addReturn()
tbtt_window.addElement(setup_btn)
tbtt_window.addElement(setup_btn_tooltip)
tbtt_window.addReturn()

tbtt_window.addElement(setup_btn_label)
tbtt_window.addReturn()

tbtt_window.addElement(export_btn)
tbtt_window.addElement(open_output_btn)
tbtt_window.addReturn()

tbtt_window.addReturn()
tbtt_window.addReturn()
tbtt_window.addSpace(tbtt_window.width * 2 / 3)
tbtt_window.addElement(close_btn)
tbtt_window.addReturn()

# Create the connections
setup_btn.onClick = do_create_turntable
export_btn.onClick = do_make_turntable
open_output_btn.onClick = do_open_output

close_btn.onClick = mset.shutdownPlugin
