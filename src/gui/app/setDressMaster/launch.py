import sys
from src.gui.dcc import StandAlone

py2 = True if sys.version_info.major < 3 else False

if not py2:
    from pathlib import Path
else:
    from pathlib2 import Path
    
app_name = Path(__file__).parent.stem

if __name__ == '__main__':
    base_app = StandAlone(app_name)
    pass
