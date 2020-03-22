"""
hoan.nguyen@virtuosgames.com

_LAUNCH "SMART" ZBRUSH - TO WORK WITH ASSET HUNTER

_PIXOLOGIC ZBRUSH REQUIRED

"""
import subprocess
from pathlib import Path, PureWindowsPath
import logging as logger

from asset.wrangler import workflow, common
from asset.tools.default_external_tools.common import external_tool_utils as ext_utils


app_tt_cfg = ext_utils.APP_TT_CFG('SmartZ', 'zbrush', 'ZStartup/ZPlugs64', __file__)
# Overrides
app_tt_cfg._SVN_DEPENDENCIES = {'python_module/Pillow-6.2.0/': 'C:/vsTools2/library/python_module/Pillow-6.2.0'}
# C:\Program Files\Pixologic\ZBrush 2018\ZStartup\ZPlugs64
app_tt_cfg._DST_PLUGIN_DIR = app_tt_cfg._APP_EXE.parent / app_tt_cfg._PLUGIN_SUBDIR_NAME
# Specific to ZBrush
app_tt_cfg._SZ_ZSCRIPT_FILE_PATH = app_tt_cfg._JSON_ROOT_DIR / "HUNTER_create_ZBrush_var.txt"  
app_tt_cfg._HUNTER_TT_PATH_ZVAR_NAME = "HUNTER_asset_ttable_path"


def write_zscript_file(asset_token, asset_tt_path, zvar, zscript_file_path):
    """
    """
    _ZVAR_EXT = ".zvr"

    logger.info('***Writing the ZScript instruction file.')

    # Create ZScript file content
    ZSCRIPT_FILE_CONTENT = """\
[VarSet, {0}, "{1}"]
[VarSave, {0}, "{2}"]"""\
.format(zvar, asset_tt_path, zvar + _ZVAR_EXT)
    
    try:
        # Write the ZScript text file at C:/Temp using the content above 
        with open(zscript_file_path, "w") as hunter_zscript_file:
            hunter_zscript_file.write(ZSCRIPT_FILE_CONTENT)
    except Exception as e:
        logger.warning('--Cannot write ZScript instruction file due to: {}.\n'.format(e))
    else:
        logger.info('--ZScript instruction file written successfully.\n')
        return True


def launch_app(asset_token, cfg=app_tt_cfg):
    """
    """
    # \\vnnas\projects\S26\data\review\image\asset\zbrush\prop\SM_Car_Max_Radio\medRes\last\jpg
    tt_root_dir = ext_utils.prep_launch_app(asset_token, cfg, 'zbrush_footage')

    # Prepare the text file to pass to ZBrush
    write_zscript_file(
            asset_token, 
            tt_root_dir, 
            cfg._HUNTER_TT_PATH_ZVAR_NAME,  
            cfg._SZ_ZSCRIPT_FILE_PATH
        )

    # Launch ZBrush with the ZScript as the second argument
    subprocess.Popen([str(PureWindowsPath(cfg._APP_EXE)), cfg._SZ_ZSCRIPT_FILE_PATH.as_posix()])
    
    return {
        'status': 1,
        'data': {},
        'message': 'Called "Launch {0}" Tool on "{1}" successfully'.format(cfg._APP_NAME, asset_token['asset_name']),
    }


if __name__ == "__main__":
    # asset_token_test = {
    #                     'asset_name': "BlueWhale",
    #                     'category': {
    #                         'main_type': "char"
    #                     },
    #                     'version': "last",
    #                     'lod': "medRes",
    #                     }
    # launch_app(asset_token_test)
    pass
