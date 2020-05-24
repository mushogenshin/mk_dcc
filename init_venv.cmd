REM First, make sure Python2.7 and 3.8 install dir are correct

set PY27_DIR=C:\Python\Python27
set PY38_DIR=C:\Python\Python38

"%PY27_DIR%/python" -m pip install virtualenv
"%PY27_DIR%/python" -m virtualenv venv27
"venv27/Scripts/pip" install -e .[dev27]

"%PY38_DIR%/python" -m venv venv38
"venv38/Scripts/pip" install -e .[dev38]
