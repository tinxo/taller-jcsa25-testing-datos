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
    suite = ge.core.ExpectationSuite("users_suite")
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
    validator.expect_column_values_to_match_regex("email", r"^[\w\.-]+@[\w\.-]+\.\w+$")

    # Expectativas de dominio >> Atributo de calidada revisar: Exactitud semántica (valores correctos en columnas específicas)
    validator.expect_column_values_to_be_in_set(
        "gender", ["Male", "Female", "Other", "Prefer not to say"]
    )
    validator.expect_column_values_to_be_in_set(
        "loyalty_tier", ["Bronze", "Silver", "Gold", "Platinum", None]
    )
    # Expectativas de rango >> Atributo de calidad a revisar: Completitud (presencia de datos)
    validator.expect_column_values_to_be_between("age", min_value=15, max_value=100)

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


def test_users_expectations():
    """Test de Great Expectations para el DataFrame de users.
    Características objetivo:
        - Exactitud sintáctica (formato general del dataset).
        - Exactitud semántica (valores correctos en columnas específicas).
        - Completitud (presencia de datos).
    """
    # Cargar datos
    df = pd.read_csv(
        DATA_DIR / "users.csv", 
        dtype={"user_id": "string"},
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
