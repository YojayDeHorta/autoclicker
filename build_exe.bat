@echo off
if not exist venv (
    echo El entorno virtual no existe. Ejecuta setup.bat primero.
    pause
    exit /b
)
echo Generando ejecutable...
call venv\Scripts\activate.bat
pip install pyinstaller
pyinstaller --noconsole --onefile --clean --name MinecraftAutoClickerV2 main.py
echo.
echo Ejecutable creado en la carpeta dist.
pause
