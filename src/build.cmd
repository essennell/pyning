@ECHO OFF
SETLOCAL

python %~dp0setup.py sdist bdist_wheel
twine upload dist/*
