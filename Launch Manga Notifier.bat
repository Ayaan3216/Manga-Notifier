@echo off
cd /d "%~dp0"
echo Starting Manga Notifier...
pythonw main.py
if errorlevel 1 (
    echo.
    echo Error starting app. Trying with python instead...
    python main.py
    pause
)
