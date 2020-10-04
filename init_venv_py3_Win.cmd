REM First, make sure Python install dir are correct

set PY3_DIR=C:\Python\Python3.7.9

"%PY3_DIR%/python" -m venv .venv3
"./.venv3/Scripts/pip" install -e .
