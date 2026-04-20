# Analisis de Datos - Streaming Musical

Integrantes:
- Alma
- Pamela

## Archivos

- `data/usuarios.csv`
- `data/canciones.csv`
- `src/data_processing.py`
- `src/analisis.py`
- `src/web_app.py`
- `run_project.bat`

## Comandos definitivos

### Opcion 1: ejecutar todo con un solo archivo

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
python src\web_app.py
```

## Ver la pagina

Con la terminal abierta, entrar en:

```text
http://127.0.0.1:5000
```
