@echo off
if not exist venv (
    echo El entorno virtual no existe. Ejecuta setup.bat primero.
    pause
    exit /b
)
start "Minecraft Autoclicker" venv\Scripts\pythonw.exe main.py
