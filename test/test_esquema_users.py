import pandas as pd
from pandera.pandas import DataFrameSchema, Column
import pytest
from pathlib import Path

# Paths
PROJECT_DIR = Path(".").resolve()
DATA_DIR = PROJECT_DIR / "data"

@pytest.fixture
def datos_users():
    """Fixture para cargar los datos del banco desde un archivo CSV.
    Returns:
        pd.DataFrame: DataFrame que contiene los datos del banco.
    """
    df = pd.read_csv(DATA_DIR / "users.csv", sep=',', header=0)
    return df


def test_esquema_users(datos_users):
    """Test de esquema para el DataFrame de datos_users.
    Característica objetivo: Exactitud sintáctica (formato general del dataset).

    Args:
        datos_users (pd.DataFrame): DataFrame que contiene los datos del dataset de usuarios.
    """
    df = datos_users
    """
    Columnas:
        user_id,first_name,last_name,email,
        signup_date,country,city,postal_code,
        age,gender,loyalty_tier
    """ 
    esquema = DataFrameSchema({
        "user_id": Column(str, nullable=False),
        "first_name": Column(str, nullable=False),
        "last_name": Column(str, nullable=False),
        "email": Column(str, nullable=False),
        "signup_date": Column(str, nullable=False),
        "country": Column(str, nullable=False),
        "city": Column(str, nullable=False),
        "postal_code": Column(int, nullable=False),
        "age": Column(int, nullable=False),
        "gender": Column(str, nullable=False),
        "loyalty_tier": Column(str, nullable=True),
    })

    esquema.validate(df)


def test_basico_users(datos_users):
    """Test básico para verificar que el DataFrame de users no está vacío
    y contiene las columnas esperadas.
    Característica objetivo: Completitud (presencia de datos).

    Args:
        datos_users (pd.DataFrame): DataFrame que contiene los datos de los usuarios.
    """
    df = datos_users
    # Verificar que el DataFrame no está vacío
    assert not df.empty, "El DataFrame está vacío." 
    # Verificar cantidad de columnas
    assert df.shape[1] == 11, f"El DataFrame debería tener 11 columnas, pero tiene {df.shape[1]}."
