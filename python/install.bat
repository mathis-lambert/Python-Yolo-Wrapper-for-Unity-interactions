@echo off
echo Installation process...

echo Installing dependencies from requirements.txt...
pip install --force-reinstall -r requirements.txt

echo Installing package...
pip install -e .

echo Done.
pause