import sys

is_py2 = True if sys.version_info.major < 3 else False

# if not is_py2:
#     from pathlib import Path
# else:
#     import src.utils
#     scandir = src.utils.load_scandir_from_venv()
#     pathlib2 = src.utils.load_pathlib2_from_venv()
#     import scandir
#     from pathlib2 import Path

class Control(object):
    def __init__(self):
        super(Control, self).__init__()
