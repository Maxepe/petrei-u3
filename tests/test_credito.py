import pytest

from tienda.credito import evaluar_solicitud_credito


@pytest.mark.parametrize(
    ("edad", "ingresos", "posee_garantia", "resultado_esperado"),
    [
        # #1: (True and True) or False -> rama if
        (25, 200000, False, "CRÉDITO APROBADO"),
        # #2: (False and False) or False -> rama else
        (17, 100000, False, "CRÉDITO RECHAZADO"),
        # #3: (False and False) or True -> rama if por garantía
        (17, 100000, True, "CRÉDITO APROBADO"),
        # #4: (True and False) or False -> rama else por ingresos
        (25, 100000, False, "CRÉDITO RECHAZADO"),
        # #5: (False and True) or False -> rama else por edad
        (17, 200000, False, "CRÉDITO RECHAZADO"),
    ],
)
def test_evaluar_solicitud_credito(edad, ingresos, posee_garantia, resultado_esperado):
    # Arrange: datos de entrada provistos por la parametrización

    # Act
    resultado_obtenido = evaluar_solicitud_credito(edad, ingresos, posee_garantia)

    # Assert
    assert resultado_obtenido == resultado_esperado
