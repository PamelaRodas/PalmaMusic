from flask import Flask

try:
    from src import cargar_y_preparar_datos, construir_merge_usuarios_canciones
except ModuleNotFoundError:
    from __init__ import cargar_y_preparar_datos, construir_merge_usuarios_canciones


app = Flask(__name__)


def construir_resultados():
    df_usuarios, df_canciones = cargar_y_preparar_datos()
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

    merge = construir_merge_usuarios_canciones(df_usuarios, df_canciones)

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
