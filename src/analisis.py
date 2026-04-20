from pathlib import Path

import pandas as pd

from data_processing import (
    cargar_datos,
    manejar_valores_nulos,
    estandarizar_texto,
    eliminar_duplicados,
    limpiar_genero,
)


BASE_DIR = Path(__file__).resolve().parents[1]
USUARIOS_PATH = BASE_DIR / "data" / "usuarios.csv"
CANCIONES_PATH = BASE_DIR / "data" / "canciones.csv"


def procesar_datos():
    df_usuarios = cargar_datos(str(USUARIOS_PATH))
    df_canciones = cargar_datos(str(CANCIONES_PATH))

    if df_usuarios is None or df_canciones is None:
        return None, None

    df_usuarios = manejar_valores_nulos(df_usuarios)
    df_usuarios = estandarizar_texto(
        df_usuarios,
        columnas=["nombre", "email", "pais", "suscripcion"],
    )
    df_usuarios = eliminar_duplicados(df_usuarios)

    df_canciones = manejar_valores_nulos(df_canciones)
    df_canciones = estandarizar_texto(
        df_canciones,
        columnas=["titulo", "artista", "genero"],
    )
    df_canciones = limpiar_genero(df_canciones)
    df_canciones = eliminar_duplicados(df_canciones)

    return df_usuarios, df_canciones


def pregunta_1_genero_popular(df_canciones):
    generos_count = df_canciones["genero"].value_counts()
    genero = generos_count.idxmax()
    cantidad = generos_count.max()

    print(f"Genero con mas canciones: {genero} ({cantidad})")


def pregunta_2_reproducciones_genero(df_canciones):
    reproduccion_promedio = (
        df_canciones.groupby("genero")["reproducciones"]
        .mean()
        .sort_values(ascending=False)
    )
    genero_mayor = reproduccion_promedio.idxmax()
    promedio = reproduccion_promedio.max()

    print(f"Mayor promedio de reproducciones: {genero_mayor} ({promedio:,.0f})")


def pregunta_3_canciones_calificadas(df_canciones):
    canciones_bien = df_canciones[df_canciones["calificacion"] > 4.6]
    cantidad = len(canciones_bien)
    porcentaje = (cantidad / len(df_canciones)) * 100

    print(f"Calificacion > 4.6: {cantidad} ({porcentaje:.1f}%)")


def analisis_merge(df_usuarios, df_canciones):
    usuarios_merge = df_usuarios.copy()
    canciones_merge = df_canciones.copy()

    usuarios_merge["id"] = pd.to_numeric(usuarios_merge["id"], errors="coerce")
    canciones_merge["usuario_id"] = pd.to_numeric(
        canciones_merge["usuario_id"],
        errors="coerce",
    )

    usuarios_merge = usuarios_merge.dropna(subset=["id"])
    canciones_merge = canciones_merge.dropna(subset=["usuario_id"])
    usuarios_merge["id"] = usuarios_merge["id"].astype(int)
    canciones_merge["usuario_id"] = canciones_merge["usuario_id"].astype(int)

    merge = canciones_merge.merge(
        usuarios_merge[["id", "nombre"]],
        left_on="usuario_id",
        right_on="id",
        how="inner",
    )

    print(f"Registros relacionados: {len(merge)}")
    suscripciones = df_usuarios["suscripcion"].value_counts()
    print(
        "Suscripciones: "
        f"Premium={int(suscripciones.get('premium', 0))}, "
        f"Free={int(suscripciones.get('free', 0))}"
    )


def main():
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
