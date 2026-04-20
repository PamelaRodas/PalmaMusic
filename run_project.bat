@echo off
cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
    echo Creando entorno virtual...
    python -m venv .venv
)

call .venv\Scripts\activate.bat

echo Instalando dependencias...
python -m pip install -r requirements.txt

echo.
echo Ejecutando analisis...
python src\analisis.py

echo.
echo Iniciando aplicacion...
echo Abre http://127.0.0.1:5000
python src\web_app.py
