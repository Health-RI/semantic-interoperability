@echo off
setlocal EnableExtensions EnableDelayedExpansion

REM ------------------------------------------------------------
REM Usage:
REM   make-json-diff.bat [OLD.json] [NEW.json]
REM Defaults (if args omitted):
REM   OLD = "Health-RI Ontology-v0.4.0.json"
REM   NEW = "Health-RI Ontology-v0.5.0.json"
REM Output:
REM   diff.txt in the current directory (unified diff, -U0, -w, --minimal)
REM Requires:
REM   - jq in PATH (jq.exe)
REM   - EITHER diff (GNU diffutils) in PATH OR git in PATH (for fallback)
REM ------------------------------------------------------------

set "OLD=%~1"
set "NEW=%~2"
if not defined OLD set "OLD=Health-RI Ontology-v0.4.0.json"
if not defined NEW set "NEW=Health-RI Ontology-v0.5.0.json"

set "TMPDIR=%TEMP%\sssomdiff_%RANDOM%%RANDOM%"
mkdir "%TMPDIR%" >nul 2>&1
set "OLD_DEL=%TMPDIR%\old.del"
set "NEW_DEL=%TMPDIR%\new.del"
set "OUT=diff.txt"

REM --- Check jq availability ---
where jq >nul 2>&1
if errorlevel 1 (
  echo ERROR: 'jq' not found in PATH. Please install jq for Windows and try again. 1>&2
  goto :fail
)

REM --- Check input files exist ---
if not exist "%OLD%" (
  echo ERROR: File not found: "%OLD%". 1>&2
  goto :fail
)
if not exist "%NEW%" (
  echo ERROR: File not found: "%NEW%". 1>&2
  goto :fail
)

REM --- Produce reduced JSONs (strip .shape and *View objects) ---
jq "del(.. | .shape?, .. | select(type == \"object\" and (.type | type == \"string\") and (.type | endswith(\"View\"))))" "%OLD%" > "%OLD_DEL%"
if errorlevel 1 (
  echo ERROR: jq failed on "%OLD%". 1>&2
  goto :fail
)
jq "del(.. | .shape?, .. | select(type == \"object\" and (.type | type == \"string\") and (.type | endswith(\"View\"))))" "%NEW%" > "%NEW_DEL%"
if errorlevel 1 (
  echo ERROR: jq failed on "%NEW%". 1>&2
  goto :fail
)

REM --- Prefer diff if available; otherwise fallback to git diff ---
where diff >nul 2>&1
if not errorlevel 1 (
  diff -U0 --minimal -w "%OLD_DEL%" "%NEW_DEL%" > "%OUT%"
  set "DIFF_EXIT=!ERRORLEVEL!"
) else (
  where git >nul 2>&1
  if errorlevel 1 (
    echo ERROR: Neither 'diff' nor 'git' found in PATH. Install GNU diffutils or Git for Windows. 1>&2
    goto :fail
  )
  git --no-pager diff --no-index --unified=0 --minimal -w "%OLD_DEL%" "%NEW_DEL%" > "%OUT%"
  set "DIFF_EXIT=!ERRORLEVEL!"
)


REM --- Interpret exit code: 0=no diffs, 1=diffs (OK), >=2=error ---
if %DIFF_EXIT% GEQ 2 (
  echo ERROR: diff encountered an error. 1>&2
  goto :fail
) else if %DIFF_EXIT% EQU 0 (
  echo No differences found. Empty "%OUT%".
  REM Optional: delete empty diff
  REM del /q "%OUT%" >nul 2>&1
) else (
  echo Differences found. Wrote "%OUT%".
)

:cleanup
del /q "%OLD_DEL%" "%NEW_DEL%" >nul 2>&1
rmdir "%TMPDIR%" >nul 2>&1
endlocal
exit /b 0

:fail
del /q "%OLD_DEL%" "%NEW_DEL%" >nul 2>&1
rmdir "%TMPDIR%" >nul 2>&1
endlocal
exit /b 1
