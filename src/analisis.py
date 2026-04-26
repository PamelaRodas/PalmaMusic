try:
    from src import cargar_y_preparar_datos, construir_merge_usuarios_canciones
except ModuleNotFoundError:
    from __init__ import cargar_y_preparar_datos, construir_merge_usuarios_canciones


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
    merge = construir_merge_usuarios_canciones(df_usuarios, df_canciones)

    print(f"Registros relacionados: {len(merge)}")
    suscripciones = df_usuarios["suscripcion"].value_counts()
    print(
        "Suscripciones: "
        f"Premium={int(suscripciones.get('premium', 0))}, "
        f"Free={int(suscripciones.get('free', 0))}"
    )


def main():
    df_usuarios, df_canciones = cargar_y_preparar_datos()

    if df_usuarios is None or df_canciones is None:
        return

    pregunta_1_genero_popular(df_canciones)
    pregunta_2_reproducciones_genero(df_canciones)
    pregunta_3_canciones_calificadas(df_canciones)
    analisis_merge(df_usuarios, df_canciones)

    print("\nAnalisis completado")


if __name__ == "__main__":
    main()
