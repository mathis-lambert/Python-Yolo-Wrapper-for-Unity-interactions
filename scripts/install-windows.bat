@echo off
setlocal
cd /d "%~dp0.."

echo Installation process...

echo Installing package and dependencies...
pip install -e .

echo Done.
pause
