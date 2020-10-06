import sys
import src.gui.dcc

is_py2 = True if sys.version_info.major < 3 else False

if not is_py2:
    from pathlib import Path
else:
    from pathlib2 import Path
    
app_name = Path(__file__).parent.stem

# from src.utils import uic_rebuild
# uic_rebuild(app_name)

if __name__ == '__main__':
    base_app = src.gui.dcc.StandAlone(app_name)
    base_app.show()
    pass
