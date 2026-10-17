@echo off
where py >nul 2>nul
if %errorlevel%==0 (py main.py) else (python main.py)
pause