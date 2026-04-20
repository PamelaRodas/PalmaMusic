"""
Módulo de limpieza de datos
Autor: Alma
"""

import pandas as pd


def cargar_datos(ruta_csv: str) -> pd.DataFrame:
    """Carga un archivo CSV."""
    try:
        df = pd.read_csv(ruta_csv)
        print(f"✓ Datos cargados desde {ruta_csv} ({df.shape[0]} filas)")
        return df
    except FileNotFoundError:
        print(f"✗ Error: {ruta_csv} no encontrado")
        return None


def manejar_valores_nulos(df: pd.DataFrame) -> pd.DataFrame:
    """Elimina filas con valores nulos."""
    filas_antes = len(df)
    df = df.dropna()
    filas_despues = len(df)
    print(f"✓ {filas_antes - filas_despues} filas con NaN eliminadas")
    return df


def estandarizar_texto(df: pd.DataFrame, columnas: list = None) -> pd.DataFrame:
    """Convierte a minúsculas y elimina espacios extra."""
    if columnas is None:
        columnas = df.select_dtypes(include=['object']).columns
    
    for col in columnas:
        if col in df.columns:
            df[col] = df[col].str.strip().str.lower()
    
    print(f"✓ Texto estandarizado en {len(columnas)} columnas")
    return df


def eliminar_duplicados(df: pd.DataFrame) -> pd.DataFrame:
    """Elimina filas duplicadas."""
    antes = len(df)
    df = df.drop_duplicates()
    print(f"✓ {antes - len(df)} duplicados eliminados")
    return df


def limpiar_genero(df: pd.DataFrame) -> pd.DataFrame:
    """Normaliza nombres de géneros."""
    if 'genero' in df.columns:
        generos_normalizados = {
            'pop': 'Pop', 'rock': 'Rock', 'synthwave': 'Synthwave',
            'indie': 'Indie', 'synth-pop': 'Synth-Pop', 'heavy metal': 'Heavy Metal',
            'grunge': 'Grunge', 'britpop': 'Britpop', 'alternative rock': 'Alternative Rock',
            'country pop': 'Country Pop', 'alternative/indie pop': 'Alternative/Indie Pop',
            'progressive rock': 'Progressive Rock', 'classic rock': 'Classic Rock',
            'folk rock': 'Folk Rock', 'electronic': 'Electronic', 'industrial rock': 'Industrial Rock',
            'hip hop': 'Hip Hop', 'rap': 'Rap', 'rap/pop': 'Rap/Pop',
            'electronic dance': 'Electronic Dance', 'dubstep': 'Dubstep',
            'electronic dance music': 'Electronic Dance Music', 'edm': 'EDM', 'disco': 'Disco'
        }
        
        df['genero'] = df['genero'].str.strip().str.lower()
        df['genero'] = df['genero'].map(generos_normalizados).fillna(df['genero'].str.title())
        print(f"✓ Géneros normalizados")
    
    return df


def validar_datos(df: pd.DataFrame) -> dict:
    """Retorna reporte de calidad de datos."""
    return {
        'filas': len(df),
        'columnas': len(df.columns),
        'valores_nulos': df.isnull().sum().sum(),
        'duplicados': df.duplicated().sum()
    }

