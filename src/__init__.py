from pathlib import Path

import pandas as pd

try:
    from data_processing import (
        cargar_datos,
        manejar_valores_nulos,
        estandarizar_texto,
        eliminar_duplicados,
        limpiar_genero,
    )
except ModuleNotFoundError:
    from src.data_processing import (
        cargar_datos,
        manejar_valores_nulos,
        estandarizar_texto,
        eliminar_duplicados,
        limpiar_genero,
    )


def cargar_y_preparar_datos(base_dir: Path | None = None):
    if base_dir is None:
        base_dir = Path(__file__).resolve().parents[1]

    usuarios_path = base_dir / "data" / "usuarios.csv"
    canciones_path = base_dir / "data" / "canciones.csv"

    df_usuarios = cargar_datos(str(usuarios_path))
    df_canciones = cargar_datos(str(canciones_path))

    if df_usuarios is None or df_canciones is None:
        return None, None

    df_usuarios = manejar_valores_nulos(df_usuarios)
    df_usuarios = estandarizar_texto(
        df_usuarios,
        columnas=["nombre", "email", "pais", "suscripcion"],
    )
    df_usuarios = eliminar_duplicados(df_usuarios)
    df_usuarios["id"] = pd.to_numeric(df_usuarios["id"], errors="coerce")
    df_usuarios = df_usuarios.dropna(subset=["id"])
    df_usuarios["id"] = df_usuarios["id"].astype(int)

    df_canciones = manejar_valores_nulos(df_canciones)
    df_canciones = estandarizar_texto(
        df_canciones,
        columnas=["titulo", "artista", "genero"],
    )
    df_canciones = limpiar_genero(df_canciones)
    df_canciones = eliminar_duplicados(df_canciones)
    df_canciones["reproducciones"] = pd.to_numeric(
        df_canciones["reproducciones"],
        errors="coerce",
    )
    df_canciones["calificacion"] = pd.to_numeric(
        df_canciones["calificacion"],
        errors="coerce",
    )
    df_canciones["usuario_id"] = pd.to_numeric(df_canciones["usuario_id"], errors="coerce")
    df_canciones = df_canciones.dropna(subset=["reproducciones", "calificacion", "usuario_id"])
    df_canciones["usuario_id"] = df_canciones["usuario_id"].astype(int)

    return df_usuarios, df_canciones


def construir_merge_usuarios_canciones(df_usuarios: pd.DataFrame, df_canciones: pd.DataFrame):
    return df_canciones.merge(
        df_usuarios[["id", "nombre"]],
        left_on="usuario_id",
        right_on="id",
        how="inner",
    )


__all__ = ["cargar_y_preparar_datos", "construir_merge_usuarios_canciones"]
