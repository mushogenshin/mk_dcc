import os
from pathlib import Path
from ruamel import yaml

import svn.library
from asset.wrangler import workflow, common
from asset.frontend.desktop_gui import external_tool_socket
from binary_vcs_lite.vcs_interface import LocalVersioning

# Object to parse all needed paths
_RESOURCE_PARSER = workflow._RESOURCE_PARSER

_CENTRAL_TURNTABLE = 'CENTRAL_TURNTABLE'
_EXCLUDE_EXTS = ('.db',)  # excludes the thumbs.db files

_ASSET_FILE_PATTERN = {
    'INCLUDE': ['**/*'],
    'EXCLUDE': ['[.]vcs_lite', 'Thumbs.db']
}


def get_dependencies(dependencies):
    # SVN get dependencies
    for module, module_path in dependencies.items():
        if not Path(module_path).exists():
            print('--Adding module {} from SVN...'.format(module))
            svn.library.addsitedir(module_path)


def write_asset_versioning_json_cfg(asset_token, tt_root_dir, json_output_fp, root_key, workspace_key):

    print('***Writing the JSON versioning config.')

    asset_token['vsproject'] = os.environ.get('VSPROJECT', '')
    asset_token[root_key] = tt_root_dir.as_posix()
    asset_token[workspace_key] = tt_root_dir.parent.as_posix()

    try:
        common.save_json(asset_token, json_output_fp.as_posix())
    except Exception as e:
        print('--Unable to write versioning JSON config due to: {}.\n'.format(e))
    else:
        print('--Versioning JSON config written successfully.\n')


def parse_yaml(config_file):
    """
    Parse the config file
    :parm Path config_file:
    """
    with open(config_file.as_posix(), 'r') as stream:
        yaml_data = {}
        try:
            yaml_data = yaml.safe_load(stream) # a dict
        except yaml.YAMLError as e:
            print('Cannot parse config file due to: {}.'.format(e))

    return yaml_data


def update_plugin(_SRC_PLUGIN_DIR, _DST_PLUGIN_DIR):

    if _SRC_PLUGIN_DIR and _DST_PLUGIN_DIR:
        common.flexible_copy_dir(_SRC_PLUGIN_DIR.as_posix(), _DST_PLUGIN_DIR.as_posix())


def prep_launch_app(asset_token, cfg, tt_key):

    get_dependencies(cfg._SVN_DEPENDENCIES)

    asset_token['image_version'] = 'last'

    # \\vnnas\projects\S26\data\review\image\asset\[tt_key]\prop\SM_Car_Max_Radio\medRes\last\jpg
    tt_root_dir = Path(_RESOURCE_PARSER.get_path(_CENTRAL_TURNTABLE, tt_key, asset_token))

    # checks if folder exists, and make it otherwise
    if not tt_root_dir.exists():
        try:
            Path.mkdir(tt_root_dir, parents=True)
        except:
            pass

    write_asset_versioning_json_cfg(
        asset_token, 
        tt_root_dir,
        cfg._HUNTER_CUR_PROJ_ASSET_JSON_FP,
        cfg._APP_TT_OUTPUT_ROOT_KEY,
        cfg._APP_TT_OUTPUT_WORKSPACE_KEY
    )

    update_plugin(cfg._SRC_PLUGIN_DIR, cfg._DST_PLUGIN_DIR)

    return tt_root_dir


def do_tt_commit(workspace_path, session, pattern):
    workspace = LocalVersioning(workspace_path, session)
    workspace.set_file_pattern(pattern)

    workspace.commit(
        [session], 
        data={'message': 'workspace 1, local commit 1'}, 
        add_only=0, 
        fast_forward=1
    )


def do_tt_checkout(workspace_path, session, pattern, checkout_path):
    workspace = LocalVersioning(workspace_path, session)
    workspace.set_file_pattern(pattern)

    workspace.checkout(
        session, 
        workspace.latest_revision(session), 
        checkout_dir=Path(checkout_path, 
        str(workspace.latest_revision(session)).zfill(3))
    )

class APP_TT_CFG(object):

    # _EXE_CFG_FP = Path(__file__).parent.parent.parent.parent / 'frontend/desktop_gui/project_config/external_tool_exe.yaml'

    def __init__(self, app_name, app_exe_key, plugin_dir_name, src_plugin_dir, json_root_dir="C:/Temp"):

        self._APP_NAME = app_name
        # self._APP_EXE = Path(parse_yaml(APP_TT_CFG._EXE_CFG_FP)[app_exe_key])  # doesn't work with override
        self._APP_EXE = Path(external_tool_socket.EXECUTABLES[app_exe_key])  # using the helper object in Duy's module

        self._SVN_DEPENDENCIES = {}

        # PLUGIN SOURCE & DESTINATION PATHS CONFIG
        
        self._PLUGIN_SUBDIR_NAME = plugin_dir_name
        self._SRC_PLUGIN_DIR = Path(src_plugin_dir).parent / self._PLUGIN_SUBDIR_NAME
        self._DST_PLUGIN_DIR = None  # this varies depending on softwares

        # ASSET TOKEN JSON FILE PATH CONFIG

        self._JSON_ROOT_DIR = Path(json_root_dir)
        self._HUNTER_CUR_PROJ_ASSET_JSON_FP = self._JSON_ROOT_DIR / "HUNTER_current_proj_asset.json"

        self._APP_TT_OUTPUT_ROOT_KEY = '{}_tt_root'.format(app_exe_key)
        self._APP_TT_OUTPUT_WORKSPACE_KEY = '{}_tt_workspace'.format(app_exe_key)
