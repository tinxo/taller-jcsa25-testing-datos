import pandas as pd
from pandera.pandas import DataFrameSchema, Column
import pytest
from pathlib import Path

# Paths
PROJECT_DIR = Path(".").resolve()
DATA_DIR = PROJECT_DIR / "data"

@pytest.fixture
def datos_orders():
    """Fixture para cargar los datos del banco desde un archivo CSV.
    Returns:
        pd.DataFrame: DataFrame que contiene los datos del banco.
    """
    df = pd.read_csv(DATA_DIR / "orders.csv", sep=',', header=0)
    return df


def test_esquema_orders(datos_orders):
    """Test de esquema para el DataFrame de datos_orders.
    Característica objetivo: Exactitud sintáctica (formato general del dataset).

    Args:
        datos_orders (pd.DataFrame): DataFrame que contiene los datos del dataset de ordenes.
    """
    df = datos_orders
    """
    Columnas:
        order_id,user_id,order_datetime,num_items,
        subtotal,shipping_fee,tax,discount_total,
        total,payment_method,order_status,
        shipping_city,shipping_country
    """ 
    esquema = DataFrameSchema({
        "user_id": Column(str, nullable=False),
        "order_id": Column(str, nullable=False),
        "order_datetime": Column(str, nullable=False),
        "num_items": Column(int, nullable=False),
        "subtotal": Column(float, nullable=False),
        "shipping_fee": Column(float, nullable=False),
        "tax": Column(float, nullable=False),
        "discount_total": Column(float, nullable=False),
        "total": Column(float, nullable=False),
        "payment_method": Column(str, nullable=False),
        "order_status": Column(str, nullable=False),
        "shipping_city": Column(str, nullable=False),
        "shipping_country": Column(str, nullable=False),
    })

    esquema.validate(df)


def test_basico_orders(datos_orders):
    """Test básico para verificar que el DataFrame de orders no está vacío
    y contiene las columnas esperadas.
    Característica objetivo: Completitud (presencia de datos).

    Args:
        datos_orders (pd.DataFrame): DataFrame que contiene los datos de las ordenes.
    """
    df = datos_orders
    # Verificar que el DataFrame no está vacío
    assert not df.empty, "El DataFrame está vacío." 
    # Verificar cantidad de columnas
    assert df.shape[1] == 13, f"El DataFrame debería tener 13 columnas, pero tiene {df.shape[1]}."