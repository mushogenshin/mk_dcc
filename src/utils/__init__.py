from os.path import dirname

MK_DCC_ROOT = dirname(dirname(dirname(__file__)))

def load_pathlib2_from_venv():
    import imp
    pathlib2 = MK_DCC_ROOT + '/venv27/Lib/site-packages/pathlib2/__init__.py'
    return imp.load_source('pathlib2', pathlib2)

def load_scandir_from_venv():
    import imp
    scandir = MK_DCC_ROOT + '/venv27/Lib/site-packages/scandir.py'
    return imp.load_source('scandir', scandir)

# if __name__ == '__main__':
#     pass
