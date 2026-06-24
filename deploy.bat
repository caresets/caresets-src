@echo off
REM Batch script to build with preview config and encrypt for deployment
REM Builds with _config.yml + _config_preview.yml, then encrypts
REM Usage: deploy.bat [password]

setlocal enabledelayedexpansion

REM Configuration
set "PASSWORD=25caresets"
set "SITE_DIR=_site"

REM Override password if provided as argument
if not "%~1"=="" set "PASSWORD=%~1"

echo ========================================
echo Build and Encrypt - PREVIEW
echo ========================================
echo.

REM Check if staticrypt is installed
where staticrypt >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo ERROR: StatiCrypt is not installed!
    echo Please install it with: npm install -g staticrypt
    exit /b 1
)

echo Building Jekyll site with preview config...
echo   Config: _config.yml,_config_preview.yml
echo.
call bundle exec jekyll build --config _config.yml,_config_preview.yml
if %ERRORLEVEL% neq 0 (
    echo ERROR: Jekyll build failed!
    exit /b 1
)

echo Creating .nojekyll file to disable GitHub Pages Jekyll processing...
echo. > "%SITE_DIR%\.nojekyll"

echo.
echo Encrypting HTML files in %SITE_DIR%...
echo Using password: %PASSWORD%
echo.

REM Counter for encrypted files
set /a COUNT=0

REM Find and encrypt all HTML files except index.html in root
for /r "%SITE_DIR%" %%f in (*.html) do (
    set "FILE=%%f"
    set "REL_PATH=!FILE:%CD%\%SITE_DIR%\=!"

    REM Skip root index.html (you may want it public)
    if /i not "!REL_PATH!"=="index.html" (
        echo Encrypting: !REL_PATH!

        REM Get directory of the file
        for %%d in ("%%~dpf.") do set "FILEDIR=%%~fd"

        REM Encrypt to same directory, then move back
        call staticrypt "%%f" -p "%PASSWORD%" -d "!FILEDIR!" --short --template-title "Protected Content" --template-instructions "Enter password to access this page" --template-color-primary "#5c5962" --template-color-secondary "#f5f6fa"

        if errorlevel 1 (
            echo WARNING: Failed to encrypt: !REL_PATH!
        ) else (
            set /a COUNT+=1
        )
    )
)

echo.
echo ========================================
echo Build and Encryption complete!
echo Total files encrypted: %COUNT%
echo ========================================
echo.
echo Your encrypted site is ready in: %SITE_DIR%
echo Password: %PASSWORD%
echo.
echo Build used: _config.yml + _config_preview.yml
echo.
echo To deploy to GitHub Pages:
echo   1. Copy contents of %SITE_DIR% to your gh-pages branch
echo   2. Or push and GitHub Actions will handle deployment
echo.

endlocal
