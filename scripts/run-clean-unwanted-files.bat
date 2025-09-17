@echo off
:START
set answer=
cls
echo Running script...
pushd "%~dp0"
python clean-unwanted-files.py
popd

echo.
set /p answer=Do you want to re-run the script? [Y/N] (default: N):

rem Normalize empty input to N
if "%answer%"=="" set answer=N

if /i "%answer%"=="Y" (
    goto START
)

exit
