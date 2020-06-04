REM First, make sure Python install dirs are correct

set PY27_DIR=C:\Python\Python2.7.18
set PY37_DIR=C:\Python\Python3.7.7

"%PY27_DIR%/python" -m pip install virtualenv
"%PY27_DIR%/python" -m virtualenv venv27
"venv27/Scripts/pip" install -e .[dev27]

"%PY37_DIR%/python" -m venv venv37
"venv37/Scripts/pip" install -e .[dev37]
