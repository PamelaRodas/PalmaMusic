from pathlib import Path

from flask import Flask
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


app = Flask(__name__)
BASE_DIR = Path(__file__).resolve().parents[1]


def cargar_y_limpiar():
    usuarios_path = BASE_DIR / "data" / "usuarios.csv"
    canciones_path = BASE_DIR / "data" / "canciones.csv"

    df_usuarios = cargar_datos(str(usuarios_path))
    df_canciones = cargar_datos(str(canciones_path))

    if df_usuarios is None or df_canciones is None:
        return None, None

    df_usuarios = manejar_valores_nulos(df_usuarios)
    df_usuarios = estandarizar_texto(df_usuarios, columnas=["nombre", "email", "pais", "suscripcion"])
    df_usuarios = eliminar_duplicados(df_usuarios)

    df_canciones = manejar_valores_nulos(df_canciones)
    df_canciones = estandarizar_texto(df_canciones, columnas=["titulo", "artista", "genero"])
    df_canciones = limpiar_genero(df_canciones)
    df_canciones = eliminar_duplicados(df_canciones)

    return df_usuarios, df_canciones


def construir_resultados():
    df_usuarios, df_canciones = cargar_y_limpiar()
    if df_usuarios is None or df_canciones is None:
        return None

    generos_count = df_canciones["genero"].value_counts()
    genero_top = generos_count.idxmax()
    genero_top_total = int(generos_count.max())

    promedio_por_genero = (
        df_canciones.groupby("genero")["reproducciones"]
        .mean()
        .sort_values(ascending=False)
    )
    genero_promedio_top = promedio_por_genero.idxmax()
    promedio_top = float(promedio_por_genero.max())

    canciones_bien = df_canciones[df_canciones["calificacion"] > 4.6]
    canciones_bien_total = int(len(canciones_bien))
    canciones_bien_pct = round((canciones_bien_total / len(df_canciones)) * 100, 1)

    usuarios_merge = df_usuarios.copy()
    canciones_merge = df_canciones.copy()
    usuarios_merge["id"] = pd.to_numeric(usuarios_merge["id"], errors="coerce")
    canciones_merge["usuario_id"] = pd.to_numeric(canciones_merge["usuario_id"], errors="coerce")
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

    return {
        "usuarios_total": int(len(df_usuarios)),
        "canciones_total": int(len(df_canciones)),
        "pregunta_1": {
            "genero": genero_top,
            "cantidad": genero_top_total,
        },
        "pregunta_2": {
            "genero": genero_promedio_top,
            "promedio": f"{promedio_top:,.0f}",
        },
        "pregunta_3": {
            "cantidad": canciones_bien_total,
            "porcentaje": canciones_bien_pct,
        },
        "merge_total": int(len(merge)),
    }


@app.route("/")
def index():
    resultados = construir_resultados()
    if not resultados:
        return "No se pudieron cargar los datos."

    lineas = [
        f"Usuarios: {resultados['usuarios_total']}",
        f"Canciones: {resultados['canciones_total']}",
        f"Merge: {resultados['merge_total']}",
        (
            "Genero con mas canciones: "
            f"{resultados['pregunta_1']['genero']} "
            f"({resultados['pregunta_1']['cantidad']})"
        ),
        (
            "Mayor promedio de reproducciones: "
            f"{resultados['pregunta_2']['genero']} "
            f"({resultados['pregunta_2']['promedio']})"
        ),
        (
            "Calificacion > 4.6: "
            f"{resultados['pregunta_3']['cantidad']} "
            f"({resultados['pregunta_3']['porcentaje']}%)."
        ),
    ]
    return "\n".join(lineas)


if __name__ == "__main__":
    app.run(debug=True)
