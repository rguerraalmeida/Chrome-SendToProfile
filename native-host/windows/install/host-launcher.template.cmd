@echo off
setlocal
set "SCRIPT=__HOST_SCRIPT_PATH__"
if not exist "%SCRIPT%" exit /b 1
where py >nul 2>nul
if %ERRORLEVEL% EQU 0 (
  py -3 "%SCRIPT%"
  exit /b %ERRORLEVEL%
)
python "%SCRIPT%"
exit /b %ERRORLEVEL%
