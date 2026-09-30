@echo off
rem 1-preprocess.bat - rebuild everything the site serves from input/.
rem
rem Runs build_content.py: workbook -> ClinicalGlossary.csv, input/models ->
rem _resources/models (without the inherited id/extension/modifierExtension
rem elements), the glossary CodeSystems, and the model-to-glossary ConceptMap
rem from the confirmed rows of input/glossary_mappings.csv.
rem
rem Safe to run any time. Nothing is committed; run 2-commit.bat next.
setlocal
cd /d "%~dp0"

python build_content.py
if errorlevel 1 (
  echo.
  echo Content build FAILED - nothing further done.
  exit /b 1
)

echo.
echo Inherited elements still served (should be none):
python preprocess_models.py | findstr /c:"Inherited elements found"
echo.
echo Changed files:
git status --short
echo.
echo Done. Review the changes, then run 2-commit.bat.
endlocal
