"""
hoan.nguyen@virtuosgames.com

_VERSION CONTROL THE OUTPUT MARMOSET TT - TO WORK WITH VSRUNNER.BAT

"""
import sys
import time
from pathlib import Path

from asset.wrangler import common
from asset.tools.default_external_tools.common import external_tool_utils as ext_utils

#######################################################################################################

_ASSET_TT_WORKSPACE = sys.argv[-1]  # unable to pass a str(dict) as argv to VSRunner.bat without having it broken down
print('***Binary VCS Lite Workspace:', _ASSET_TT_WORKSPACE)

#######################################################################################################

def do_tt_commit_and_checkout(workspace_path):

    workspace_path = Path(workspace_path)

    try:
        ext_utils.do_tt_commit(workspace_path, common.REVIEW_SESS, ext_utils._ASSET_FILE_PATTERN)
        ext_utils.do_tt_checkout(workspace_path, common.REVIEW_SESS, ext_utils._ASSET_FILE_PATTERN, workspace_path.parent)
    except Exception as e:
        print('Unable to perform version control for turntable images due to: {}'.format(e))
    else:
        print('Performed version control successfully.')


#######################################################################################################

if __name__ == '__main__':
    do_tt_commit_and_checkout(_ASSET_TT_WORKSPACE)
    time.sleep(5)
    pass
