"""
Script de análisis de datos
Autor: Pamela
"""

from pathlib import Path
import pandas as pd

from data_processing import (
    cargar_datos, manejar_valores_nulos, estandarizar_texto,
    eliminar_duplicados, limpiar_genero
)


BASE_DIR = Path(__file__).resolve().parents[1]
USUARIOS_PATH = BASE_DIR / "data" / "usuarios.csv"
CANCIONES_PATH = BASE_DIR / "data" / "canciones.csv"


def procesar_datos():
    """Carga y limpia datos."""
    print("\nProyecto: analisis de streaming musical (equipo de 2)\n")
    
    # Cargar datos
    df_usuarios = cargar_datos(str(USUARIOS_PATH))
    df_canciones = cargar_datos(str(CANCIONES_PATH))
    
    if df_usuarios is None or df_canciones is None:
        return None, None
    
    # Limpiar usuarios
    print("\nLimpiando usuarios...")
    df_usuarios = manejar_valores_nulos(df_usuarios)
    df_usuarios = estandarizar_texto(df_usuarios, columnas=['nombre', 'email', 'pais', 'suscripcion'])
    df_usuarios = eliminar_duplicados(df_usuarios)
    
    # Limpiar canciones
    print("\nLimpiando canciones...")
    df_canciones = manejar_valores_nulos(df_canciones)
    df_canciones = estandarizar_texto(df_canciones, columnas=['titulo', 'artista', 'genero'])
    df_canciones = limpiar_genero(df_canciones)
    df_canciones = eliminar_duplicados(df_canciones)
    
    print(f"\nDatos limpios: {len(df_usuarios)} usuarios, {len(df_canciones)} canciones")
    return df_usuarios, df_canciones


def pregunta_1_genero_popular(df_canciones):
    """Género con más canciones."""
    print("\n1) Genero con mas canciones")
    
    generos_count = df_canciones['genero'].value_counts()
    genero = generos_count.idxmax()
    cantidad = generos_count.max()
    
    print(f"   Respuesta: '{genero}' con {cantidad} canciones")
    print(f"   Distribucion general: {dict(generos_count.head())}")


def pregunta_2_reproducciones_genero(df_canciones):
    """Promedio de reproducciones por género."""
    print("\n2) Promedio de reproducciones por genero")
    
    reproduccion_promedio = df_canciones.groupby('genero')['reproducciones'].mean().sort_values(ascending=False)
    genero_mayor = reproduccion_promedio.idxmax()
    promedio = reproduccion_promedio.max()
    
    print(f"   Respuesta: '{genero_mayor}' con {promedio:,.0f} reproducciones promedio")
    print(f"   Top 3: {dict(reproduccion_promedio.head(3))}")


def pregunta_3_canciones_calificadas(df_canciones):
    """Canciones con calificación > 4.6."""
    print("\n3) Canciones con calificacion mayor a 4.6")
    
    canciones_bien = df_canciones[df_canciones['calificacion'] > 4.6]
    cantidad = len(canciones_bien)
    porcentaje = (cantidad / len(df_canciones)) * 100
    
    print(f"   Respuesta: {cantidad} canciones ({porcentaje:.1f}%)")
    print(f"   Promedio de calificación: {canciones_bien['calificacion'].mean():.2f}")


def analisis_merge(df_usuarios, df_canciones):
    """Merge entre usuarios y canciones."""
    print("\n4) Cruce de usuarios con canciones (merge)")

    # Convierte claves a numérico para tolerar datos sucios (espacios, strings, vacíos)
    usuarios_merge = df_usuarios.copy()
    canciones_merge = df_canciones.copy()
    usuarios_merge['id'] = pd.to_numeric(usuarios_merge['id'], errors='coerce')
    canciones_merge['usuario_id'] = pd.to_numeric(canciones_merge['usuario_id'], errors='coerce')
    usuarios_merge = usuarios_merge.dropna(subset=['id'])
    canciones_merge = canciones_merge.dropna(subset=['usuario_id'])
    usuarios_merge['id'] = usuarios_merge['id'].astype(int)
    canciones_merge['usuario_id'] = canciones_merge['usuario_id'].astype(int)
    
    merge = canciones_merge.merge(
        usuarios_merge[['id', 'nombre']],
        left_on='usuario_id',
        right_on='id',
        how='inner'
    )
    
    print(f"   Total de registros: {len(merge)}")
    suscripciones = df_usuarios['suscripcion'].value_counts()
    print(f"   Suscripciones: Premium={int(suscripciones.get('premium', 0))}, Free={int(suscripciones.get('free', 0))}")


def main():
    """Ejecuta el análisis."""
    df_usuarios, df_canciones = procesar_datos()
    
    if df_usuarios is None or df_canciones is None:
        return
    
    pregunta_1_genero_popular(df_canciones)
    pregunta_2_reproducciones_genero(df_canciones)
    pregunta_3_canciones_calificadas(df_canciones)
    analisis_merge(df_usuarios, df_canciones)
    
    print("\nAnalisis completado")


if __name__ == "__main__":
    main()

