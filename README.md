# Analisis de Datos - Streaming Musical

Integrantes:
- Alma
- Pamela

## Objetivo

Limpiar y analizar datos con pandas usando dos archivos CSV relacionados.

## Ejecucion (PowerShell) - pasos probados

1. Verificar que estas en la carpeta del proyecto
```powershell
Get-Location
```

2. Activar entorno virtual
```powershell
.\.venv\Scripts\Activate.ps1
```

3. Instalar dependencias
```powershell
python -m pip install -r requirements.txt
```

4. Ejecutar analisis
```powershell
python src\analisis.py
```

5. Verificar web sin abrir navegador
```powershell
python -c "from src.web_app import app; c=app.test_client(); r=c.get('/'); print(r.status_code)"
```

Resultado esperado:
- El analisis termina con "Analisis completado".
- El comando web imprime 200.

## Abrir la web

```powershell
python src\web_app.py
```

Luego abrir: http://127.0.0.1:5000

## Estructura esencial

- data/usuarios.csv
- data/canciones.csv
- src/data_processing.py
- src/analisis.py
- src/web_app.py
- requirements.txt
- .gitignore

## Git para entrega (release)

```bash
git checkout develop
git pull
git checkout -b release/analisis-v1
git push origin release/analisis-v1
```
