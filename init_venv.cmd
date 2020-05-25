REM First, make sure Python install dirs are correct

set PY27_DIR=C:\Python\Python2.7.18
set PY38_DIR=C:\Python\Python3.8.3

"%PY27_DIR%/python" -m pip install virtualenv
"%PY27_DIR%/python" -m virtualenv venv27
"venv27/Scripts/pip" install -e .[dev27]

"%PY38_DIR%/python" -m venv venv38
"venv38/Scripts/pip" install -e .[dev38]
