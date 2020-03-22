"""
hoan.nguyen@virtuosgames.com

LAUNCH "SMART" MARMOSET - TO WORK WITH ASSET HUNTER

MARMOSET TOOLBAG REQUIRED

"""
import os
import subprocess
from pathlib import Path

from asset.tools.default_external_tools.common import external_tool_utils as ext_utils


app_tt_cfg = ext_utils.APP_TT_CFG('MarmoSmart', 'marmoset', 'plugins', __file__)
# Overrides
# C:\Users\hoan.nguyen\AppData\Local\Marmoset Toolbag 3\plugins
mset_version = 'Marmoset {}'.format(app_tt_cfg._APP_EXE.parent.name)  # abstracting 'Toolbag 3'
app_tt_cfg._DST_PLUGIN_DIR = Path(os.environ['LOCALAPPDATA']) / mset_version / app_tt_cfg._PLUGIN_SUBDIR_NAME


def launch_app(asset_token, cfg=app_tt_cfg):

    # \\vnnas\projects\S26\data\review\image\asset\substance\prop\SM_Car_Max_Radio\medRes\last\jpg
    ext_utils.prep_launch_app(asset_token, cfg, 'substance_footage')

    # calls the executable
    subprocess.Popen([str(cfg._APP_EXE)])

    return {
        'status': 1,
        'data': {},
        'message': 'Called "Launch {0}" Tool on "{1}" successfully'.format(cfg._APP_NAME, asset_token['asset_name']),
    }

if __name__ == "__main__":

    # asset_token_test = {
    #                     'asset_name': "AndeanCondor",
    #                     'category': {
    #                         'main_type': "char"
    #                     },
    #                     'version': "last",
    #                     'lod': "medRes",
    #                     }

    # launch_app(asset_token_test)
    pass