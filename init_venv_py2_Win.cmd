REM First, make sure Python install dir are correct

set PY2_DIR=C:\Python\Python2.7.18

"%PY2_DIR%/python" -m pip install virtualenv
"%PY2_DIR%/python" -m virtualenv .venv2
".venv2/Scripts/pip" install -e .
