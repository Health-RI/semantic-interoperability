@echo off
setlocal enabledelayedexpansion

REM Create output folder if it doesn't exist
if not exist processed (
    mkdir processed
)

REM Loop over image files
for %%F in (*.png *.jpg *.jpeg) do (
    echo Processing %%F...
    magick "%%F" ^
        -background white ^
        -alpha remove -alpha off ^
        -gravity center ^
        -extent %%[fx:w*1.1]x%%[fx:h*1.1] ^
        -bordercolor "#F7AD2C" ^
        -border 10 ^
        "processed\%%F"
)

echo.
echo Processing complete. Files saved in the 'processed' folder.
pause
