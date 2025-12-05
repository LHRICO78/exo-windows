@echo off
REM Script pour activer l'environnement virtuel et démarrer l'application exo

echo Activation de l'environnement virtuel...
call venv\Scripts\activate.bat

if errorlevel 0 (
    echo Lancement de l'application exo...
    exo
) else (
    echo Erreur lors de l'activation de l'environnement virtuel.
    pause
)

pause
