import os
from pathlib import Path
import subprocess
import svn.library


_DEPENDENCIES = {'python_module/Pillow-6.2.0/': 'C:/vsTools2/library/python_module/Pillow-6.2.0'}


def open_hunter_ttStamper(asset_token):

    # SVN get dependencies
    for module, module_path in _DEPENDENCIES.items():
        if not Path(module_path).exists():
            print('--Adding module {} from SVN...'.format(module))
            svn.library.addsitedir(module_path)

    #####################################################################################################

    _PYTHON3 = 'C:/python3.7.0/python.exe'

    _TT_STAMPER_MAIN_MODULE_NAME = 'ttStamper.pyw'
    _TT_STAMPER_MAIN_MODULE_PATH = Path(__file__).with_name(_TT_STAMPER_MAIN_MODULE_NAME)

    # print(_TT_STAMPER_MAIN_MODULE_PATH)
    # print('FOUND _TT_STAMPER_MAIN_MODULE_NAME:', _TT_STAMPER_MAIN_MODULE_PATH.exists())

    subprocess.Popen([_PYTHON3, _TT_STAMPER_MAIN_MODULE_PATH.as_posix(), str(asset_token)])

    return {
        'status': 1,
        'data': {},
        'message': 'Called "TT Stamper" Tool on "{}" successfully'.format(asset_token['asset_name']),
    }
