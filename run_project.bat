@echo off
cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
    echo Creando entorno virtual...
    py -3 -m venv .venv
)

echo Instalando dependencias...
.venv\Scripts\python.exe -m pip install -r requirements.txt

echo.
echo Ejecutando analisis...
.venv\Scripts\python.exe src\analisis.py
