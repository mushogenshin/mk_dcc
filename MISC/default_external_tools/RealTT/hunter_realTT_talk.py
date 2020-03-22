"""
hoan.nguyen@virtuosgames.com

LAUNCH "SMART" UNREAL EDITOR - TO WORK WITH ASSET HUNTER

UNREAL EDITOR REQUIRED

"""
import os
import subprocess
from pathlib import Path

from asset.tools.default_external_tools.common import external_tool_utils as ext_utils


app_tt_cfg = ext_utils.APP_TT_CFG('RealTT', 'unreal', 'Python', __file__)
# Overrides
# C:\Epic Games\UE_4.24\Engine\Content\Python
app_tt_cfg._DST_PLUGIN_DIR = app_tt_cfg._APP_EXE.parent.parent.parent / 'Content' / app_tt_cfg._PLUGIN_SUBDIR_NAME 


def launch_app(asset_token, cfg=app_tt_cfg):

    # \\vnnas\projects\S26\data\review\image\asset\unreal\prop\SM_Car_Max_Radio\medRes\last\jpg
    ext_utils.prep_launch_app(asset_token, cfg, 'unreal_footage')

    # calls the executable
    # subprocess.Popen([str(cfg._APP_EXE)])

    return {
        'status': 1,
        'data': {},
        'message': 'Performed "{0}" Tool on "{1}" successfully.\n\n \
        Please manually launch Unreal Editor now.'.format(cfg._APP_NAME, asset_token['asset_name']),
    }

if __name__ == "__main__":

    # asset_token_test = {
    #                     'asset_name': "AtollaJellyfish",
    #                     'category': {
    #                         'main_type': "char"
    #                     },
    #                     'version': "last",
    #                     'lod': "medRes",
    #                     }

    # launch_app(asset_token_test)
    pass