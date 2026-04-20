import pandas as pd


def cargar_datos(ruta_csv: str) -> pd.DataFrame:
    try:
        df = pd.read_csv(ruta_csv)
        return df
    except FileNotFoundError:
        return None


def manejar_valores_nulos(df: pd.DataFrame) -> pd.DataFrame:
    return df.dropna()


def estandarizar_texto(df: pd.DataFrame, columnas: list = None) -> pd.DataFrame:
    if columnas is None:
        columnas = df.select_dtypes(include=["object"]).columns

    for col in columnas:
        if col in df.columns:
            df[col] = df[col].str.strip().str.lower()

    return df


def eliminar_duplicados(df: pd.DataFrame) -> pd.DataFrame:
    return df.drop_duplicates()


def limpiar_genero(df: pd.DataFrame) -> pd.DataFrame:
    if "genero" in df.columns:
        generos_normalizados = {
            "pop": "Pop",
            "rock": "Rock",
            "synthwave": "Synthwave",
            "indie": "Indie",
            "synth-pop": "Synth-Pop",
            "heavy metal": "Heavy Metal",
            "grunge": "Grunge",
            "britpop": "Britpop",
            "alternative rock": "Alternative Rock",
            "country pop": "Country Pop",
            "alternative/indie pop": "Alternative/Indie Pop",
            "progressive rock": "Progressive Rock",
            "classic rock": "Classic Rock",
            "folk rock": "Folk Rock",
            "electronic": "Electronic",
            "industrial rock": "Industrial Rock",
            "hip hop": "Hip Hop",
            "rap": "Rap",
            "rap/pop": "Rap/Pop",
            "electronic dance": "Electronic Dance",
            "dubstep": "Dubstep",
            "electronic dance music": "Electronic Dance Music",
            "edm": "EDM",
            "disco": "Disco",
        }

        df["genero"] = df["genero"].str.strip().str.lower()
        df["genero"] = df["genero"].map(generos_normalizados).fillna(
            df["genero"].str.title()
        )

    return df


def validar_datos(df: pd.DataFrame) -> dict:
    return {
        "filas": len(df),
        "columnas": len(df.columns),
        "valores_nulos": df.isnull().sum().sum(),
        "duplicados": df.duplicated().sum(),
    }
