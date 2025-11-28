import pandas as pd
import great_expectations as ge
from pathlib import Path
import pytest


# Paths
PROJECT_DIR = Path(".").resolve()
DATA_DIR = PROJECT_DIR / "data"


def build_validator(df: pd.DataFrame) -> ge.validator.validator.Validator:
    # Inicializar un DataContext efímero para evitar errores de contexto
    try:
        ge.get_context()
    except Exception:
        # Si falla, continuar: algunas instalaciones inicializan contexto bajo demanda
        pass

    # Un ExpectationSuite es un "contenedor" de las reglas de validación = expectativas
    suite = ge.core.ExpectationSuite("orders_suite")
    # Se arma un Batch en memoria con los datos (una fracción de los datos)
    batch = ge.core.batch.Batch(data=df)
    # Se instancia un validador que es lo que va a ejecutar las expectativas
    validator = ge.validator.validator.Validator(
        execution_engine=ge.execution_engine.PandasExecutionEngine(), # Con qué se van a ejecutar las validaciones
        batches=[batch], # Los datos a validar
        active_batch_id=batch.id, # El batch activo
        expectation_suite=suite, # La suite de expectativas
    )

    # Expectativas de formato >> Atributo de calidad a revisar: Exactitud sintáctica (formato general del dataset)
    validator.expect_column_values_to_match_regex("user_id", r"^U\d{6}$")
    validator.expect_column_values_to_match_regex("order_id", r"^O\d{6}$")

    # Expectativas de dominio >> Atributo de calidada revisar: Exactitud semántica (valores correctos en columnas específicas)
    validator.expect_column_values_to_be_in_set(
        "payment_method", ["Credit Card", "Debit Card", "PayPal", "UPI", "COD", "Gift Card"]
    )
    validator.expect_column_values_to_be_in_set(
        "order_status", ["processing", "shipped", "cancelled", "returned", "completed"]
    )
    # Expectativas de rango >> Atributo de calidad a revisar: Completitud (presencia de datos)
    validator.expect_column_values_to_be_between("num_items", min_value=1, max_value=10)
    validator.expect_column_values_to_be_between("total", min_value=0.01, max_value=10000.00)

    return validator


def _format_failed_expectations(results: dict, max_examples: int = 5) -> str:
    """ Formatea los resultados de expectativas fallidas para su presentación.
    Args:
        results (dict): Resultados de la validación de Great Expectations.
        max_examples (int): Número máximo de ejemplos inesperados a mostrar por expectativa.
    """
    lines = []
    for r in results.get("results", []):
        # Se itera en cada resultado de expectativa y se obtienen los detalles relevantes
        cfg = r.get("expectation_config", {})
        exp = cfg.get("expectation_type") # qué tipo de validación se hizo
        col = cfg.get("kwargs", {}).get("column")
        info = r.get("result", {}) or {} # detalles del resultado
        ucount = info.get("unexpected_count") # cuántos valores no cumplieron la expectativa
        total = info.get("element_count")
        examples = info.get("unexpected_list") or []
        examples = examples[:max_examples]
        # Formatear línea de salida por cada expectativa fallida
        line = f"- {exp} (col={col}) -> {ucount}/{total} valores inesperados"
        if examples:
            line += f" | Ejemplos: {examples}" # Se muestran algunos ejemplos de valores que no cumplieron la expectativa
        if r.get("exception_info", {}).get("raised_exception"):
            # En caso de que haya habido una excepción durante la validación, se agrega el mensaje
            line += f" | Excepción: {r['exception_info'].get('exception_message')}"
        lines.append(line)
    return "\n".join(lines) if lines else "(sin detalles)"


def test_orders_expectations():
    """Test de Great Expectations para el DataFrame de orders.
    Características objetivo:
        - Exactitud sintáctica (formato general del dataset).
        - Exactitud semántica (valores correctos en columnas específicas).
        - Completitud (presencia de datos).
    """
    # Cargar datos
    df = pd.read_csv(
        DATA_DIR / "orders.csv", 
        dtype={"order_id": "string", "user_id": "string"},
        sep=',', 
        header=0)

    # Construir validador
    validator = build_validator(df)

     # Devuelve solo fallos y con detalles completos
    results = validator.validate(
        only_return_failures=True,
        result_format="COMPLETE",
        catch_exceptions=True,
    )

    # Si hay fallos, se formatea el mensaje y se falla el test
    if not results.get("success", False):
        pytest.fail("Fallaron expectativas:\n" + _format_failed_expectations(results))

    assert results["success"]


def test_orders_num_items_matches_order_items_sum():
    """ Test para verificar que la columna num_items en orders coincide con la suma de cantidades en order_items.
    Característica objetivo: Consistencia (cumplimiento de reglas de negocio entre los datasets).
    """
    # Cargar órdenes e ítems
    df_orders = pd.read_csv(
        DATA_DIR / "orders.csv",
        dtype={"order_id": "string", "user_id": "string"},
        sep=",",
        header=0,
    )
    df_items = pd.read_csv(
        DATA_DIR / "order_items.csv",
        dtype={"order_id": "string", "product_id": "string"},
        sep=",",
        header=0,
    )

    # Sumar cantidades por order_id (si no hay ítems, suma=0)
    sums = (
        df_items.groupby("order_id", as_index=False)["quantity"]
        .sum()
        .rename(columns={"quantity": "sum_items"})
    )

    # DataFrame de comparación
    df_check = (
        df_orders[["order_id", "num_items"]]
        .merge(sums, on="order_id", how="left")
        .fillna({"sum_items": 0})
    )

    # Validador específico para esta verificación
    suite = ge.core.ExpectationSuite("orders_items_consistency_suite")
    batch = ge.core.batch.Batch(data=df_check)
    validator = ge.validator.validator.Validator(
        execution_engine=ge.execution_engine.PandasExecutionEngine(),
        batches=[batch],
        active_batch_id=batch.id,
        expectation_suite=suite,
    )

    # Regla: num_items debe igualar sum_items
    validator.expect_column_pair_values_to_be_equal("num_items", "sum_items")

    results = validator.validate(
        only_return_failures=True,
        result_format="COMPLETE",
        catch_exceptions=True,
    )

    if not results.get("success", False):
        # Mostrar algunas órdenes con discrepancias como ayuda de depuración
        bad = df_check[df_check["num_items"] != df_check["sum_items"]]
        examples = bad.head(10).to_dict(orient="records")
        pytest.fail("Inconsistencias num_items vs sum_items:\n" + str(examples))

    assert results["success"]


def test_orders_amounts_consistency():
    """ Test para verificar reglas de consistencia de montos en orders.
    Característica objetivo: Consistencia (cumplimiento de reglas de negocio en uno y entre los datasets). 

    Verifica:
    1) subtotal == suma de importes de items (quantity * unit_price) por order_id.
    2) total == subtotal + shipping_fee + tax - discount_total.
    """
    # Cargar datasets
    df_orders = pd.read_csv(
        DATA_DIR / "orders.csv",
        dtype={"order_id": "string", "user_id": "string"},
        sep=",",
        header=0,
    )
    df_items = pd.read_csv(
        DATA_DIR / "order_items.csv",
        dtype={"order_id": "string", "product_id": "string"},
        sep=",",
        header=0,
    )

    # Detectar columna de precio por ítem (ajusta según tu schema)
    price_cols = [c for c in ["unit_price", "price", "item_price"] if c in df_items.columns]
    if not price_cols:
        pytest.fail("No se encontró columna de precio en order_items (unit_price/price/item_price).")
    unit_price_col = price_cols[0]

    # Calcular importe por ítem y sumar por order_id
    df_items["__item_amount__"] = df_items["quantity"] * df_items[unit_price_col]
    sums = (
        df_items.groupby("order_id", as_index=False)["__item_amount__"]
        .sum()
        .rename(columns={"__item_amount__": "items_sum_amount"})
    )

    # Preparar dataframe de verificación con columnas esperadas
    df_check = (
        df_orders[
            ["order_id", "subtotal", "shipping_fee", "tax", "discount_total", "total"]
        ]
        .merge(sums, on="order_id", how="left")
        .fillna({"items_sum_amount": 0.0})
    )
    # Calcular total esperado por fórmula de negocio
    df_check["expected_total"] = (
        df_check["subtotal"] + df_check["shipping_fee"] + df_check["tax"] - df_check["discount_total"]
    )

    # Validador gx
    suite = ge.core.ExpectationSuite("orders_amounts_consistency_suite")
    batch = ge.core.batch.Batch(data=df_check)
    validator = ge.validator.validator.Validator(
        execution_engine=ge.execution_engine.PandasExecutionEngine(),
        batches=[batch],
        active_batch_id=batch.id,
        expectation_suite=suite,
    )

    # Expectativas:
    # 1) subtotal == suma de importes de ítems
    validator.expect_column_pair_values_to_be_equal("subtotal", "items_sum_amount")
    # 2) total == subtotal + shipping_fee + tax - discount_total
    validator.expect_column_pair_values_to_be_equal("total", "expected_total")

    # Ejecutar y reportar fallos con ejemplos
    results = validator.validate(
        only_return_failures=True,
        result_format="COMPLETE",
        catch_exceptions=True,
    )

    if not results.get("success", False):
        bad = df_check[
            (df_check["subtotal"] != df_check["items_sum_amount"]) |
            (df_check["total"] != df_check["expected_total"])
        ][["order_id", "subtotal", "items_sum_amount", "shipping_fee", "tax", "discount_total", "total", "expected_total"]]
        examples = bad.head(10).to_dict(orient="records")
        pytest.fail("Inconsistencias de montos en orders:\n" + str(examples))

    assert results["success"]