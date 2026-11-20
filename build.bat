@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion
cd /d "%~dp0"

echo ==========================================
echo   Build books
echo ==========================================

set "PY="
where py >nul 2>nul
if not errorlevel 1 (
    py -3 -c "import sys" >nul 2>nul
    if not errorlevel 1 set "PY=py -3"
)
if not defined PY (
    where python >nul 2>nul
    if not errorlevel 1 set "PY=python"
)
if not defined PY (
    if exist "%LOCALAPPDATA%\Programs\Python\Python312\python.exe" set "PY=%LOCALAPPDATA%\Programs\Python\Python312\python.exe"
)
if not defined PY (
    echo [ERROR] Python not found. Install Python 3.10+ and add it to PATH.
    pause
    exit /b 1
)

%PY% -c "import markdown, pymupdf, PIL, matplotlib, typst" >nul 2>nul
if errorlevel 1 (
    echo Installing dependencies: markdown pymupdf pillow matplotlib
    %PY% -m pip install --quiet markdown pymupdf pillow matplotlib
)

set "TARGET=%~1"
if "%TARGET%"=="" set "TARGET=all"

if /i "%TARGET%"=="figures" (
    echo [1/2] Redraw figures
    %PY% books\build\build.py --all --figures --no-opt
    if errorlevel 1 goto fail
    echo [2/2] Build all books
    %PY% books\build\build.py --all
    if errorlevel 1 goto fail
    goto done
)

if /i "%TARGET%"=="all" (
    %PY% books\build\build.py --all
    if errorlevel 1 goto fail
    goto done
)

if exist "books\%TARGET%\book.json" (
    %PY% books\build\build.py --book books\%TARGET% %2 %3
    if errorlevel 1 goto fail
    goto done
)

echo [ERROR] Unknown target: %TARGET%
echo Usage: build.bat [all^|figures^|<book-name^>]
pause
exit /b 1

:fail
echo.
echo [ERROR] Build failed. See messages above.
pause
exit /b 1

:done
echo.
echo Done. PDF files are in the output folder.
pause
