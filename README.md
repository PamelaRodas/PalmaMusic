# Analisis de Datos - Streaming Musical

Integrantes:
- Alma
- Pamela

## Conceptos clave

- Un DataFrame es una tabla de datos en memoria (filas y columnas) que permite filtrar, limpiar, agrupar y combinar informacion con Pandas.
- Un entorno virtual (venv) aisla las librerias del proyecto para que no se mezclen con otros trabajos y la ejecucion sea reproducible.

## Archivos

- `data/usuarios.csv`
- `data/canciones.csv`
- `src/data_processing.py`
- `src/analisis.py`
- `src/web_app.py`
- `run_project.bat`

## Comandos definitivos

### Opcion 1: ejecutar analisis en terminal (Windows CMD/PowerShell)

En `cmd`, desde la carpeta del proyecto:

```cmd
run_project.bat
```

### Opcion 2: ejecutar paso por paso

En `cmd`, desde la carpeta del proyecto:

```cmd
python -m venv .venv
.venv\Scripts\activate.bat
python -m pip install -r requirements.txt
python src\analisis.py
```

## Opcional: ver la pagina web

Si tambien quieres levantar Flask:

```text
python src\web_app.py
http://127.0.0.1:5000
```
