% filepath: /d:/Projets/Alibi/Memory/compile.bat
@echo off

echo Compilation du mémoire avec XeLaTeX...

REM Compilation avec XeLaTeX au lieu de PDFLaTeX
xelatex -interaction=nonstopmode memoire.tex
bibtex memoire
xelatex -interaction=nonstopmode memoire.tex
xelatex -interaction=nonstopmode memoire.tex

echo.
if errorlevel 1 (
    echo Des erreurs de compilation ont été détectées. Veuillez consulter le fichier memoire.log pour plus d'informations.
) else ( 
    echo Compilation terminée avec succès!
)

REM Pause pour voir les messages
pause
