@echo off
REM Définit l'encodage de la console en UTF-8 pour un affichage correct des logs
chcp 65001 > nul

echo Lancement du script Python tout-en-un...
python cleaner.py

echo.
echo Processus termine. Verifiez le fichier 'execution_log.txt' pour les details.
pause