@echo off
REM Create a virtual environment in the "venv" directory
python -m venv venv

REM Activate the virtual environment
call venv\Scripts\activate

REM Install required packages from requirements.txt
pip install -r requirements.txt

echo Installation complete. Press any key to exit.
pause
