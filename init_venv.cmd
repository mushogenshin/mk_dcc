REM First, make sure Python2.7 and 3.6 install dir are correct

set PY27_DIR=C:\Python27
set PY36_DIR=C:\Python36

"%PY27_DIR%/python" -m pip install virtualenv
"%PY27_DIR%/python" -m virtualenv venv27
"venv27/Scripts/pip" install -e .[dev27]

"%PY36_DIR%/python" -m venv venv36
"venv36/Scripts/pip" install -e .[dev36]
