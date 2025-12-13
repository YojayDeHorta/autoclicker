@echo off
echo Creando entorno virtual...
python -m venv venv
echo Activando entorno virtual e instalando dependencias...
call venv\Scripts\activate.bat
pip install -r requirements.txt
echo.
echo Listo! Ahora puedes usar run.bat para iniciar el autoclicker.
pause
