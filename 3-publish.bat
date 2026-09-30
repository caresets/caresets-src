@echo off
rem 3-publish.bat - build the public site into the caresets/caresets clone and
rem push it. That push IS the publication: GitHub Pages serves that repository's
rem main branch at https://caresets.github.io/caresets/
rem
rem The clone is expected at %PUBLISH_CLONE%, default c:\work\caresets\caresets,
rem and is created if it is missing. The build runs the content step first, so
rem 1-preprocess.bat is not required before this; 2-commit.bat is, if you want
rem the source on GitHub to match what you publish.
setlocal
cd /d "%~dp0"
if "%PUBLISH_CLONE%"=="" set "PUBLISH_CLONE=c:\work\caresets\caresets"

if not exist "%PUBLISH_CLONE%\.git" (
  echo No clone at %PUBLISH_CLONE% - cloning caresets/caresets there.
  git clone https://github.com/caresets/caresets.git "%PUBLISH_CLONE%"
  if errorlevel 1 exit /b 1
)

echo Bringing the clone up to date...
git -C "%PUBLISH_CLONE%" pull --ff-only
if errorlevel 1 (
  echo Pull FAILED - the clone has local changes or diverged. Fix it by hand first.
  exit /b 1
)

echo.
echo Building the site into %PUBLISH_CLONE% ...
python build_package.py --publish-to "%PUBLISH_CLONE%"
if errorlevel 1 (
  echo Build FAILED - nothing published.
  exit /b 1
)

echo.
echo Changes in the publication clone:
git -C "%PUBLISH_CLONE%" status --short
git -C "%PUBLISH_CLONE%" add -A
git -C "%PUBLISH_CLONE%" diff --cached --quiet
if not errorlevel 1 (
  echo Nothing changed - the published site is already current.
  exit /b 0
)

echo.
choice /c YN /m "Commit and push these to GitHub Pages"
if errorlevel 2 (
  echo Left uncommitted in %PUBLISH_CLONE%. Nothing published.
  exit /b 0
)

git -C "%PUBLISH_CLONE%" commit -m "Publish site %date% %time:~0,5%"
if errorlevel 1 exit /b 1
git -C "%PUBLISH_CLONE%" push
if errorlevel 1 (
  echo Push FAILED. Nothing published.
  exit /b 1
)
echo.
echo Published. Pages picks it up within a minute or two; the site is cached for
echo ten minutes, so hard-refresh if the old version still shows.
endlocal
