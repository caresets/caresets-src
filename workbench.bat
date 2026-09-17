@echo off
REM Double-click to open the CareSets workbench.
REM Python is the only requirement; the page runs the same scripts a developer
REM would run from the command line.
cd /d "%~dp0"
python workbench.py
pause
