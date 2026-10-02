import pytest

from tienda.descuentos import calcular_descuento


def test_calcular_descuento_cliente_vip():
    # Arrange (Configuración del escenario)
    monto_total = 1000.0
    es_vip = True
    resultado_esperado = 200.0

    # Act (Ejecución de la lógica bajo prueba)
    resultado_obtenido = calcular_descuento(monto_total, es_vip)

    # Assert (Verificación y aseveración de resultados)
    assert resultado_obtenido == resultado_esperado


def test_calcular_descuento_cliente_regular():
    # Arrange
    monto_total = 1000.0
    es_vip = False
    resultado_esperado = 50.0

    # Act
    resultado_obtenido = calcular_descuento(monto_total, es_vip)

    # Assert
    assert resultado_obtenido == resultado_esperado


def test_calcular_descuento_monto_invalido_lanza_excepcion():
    # Arrange
    monto_total = -50.0
    es_vip = False

    # Act & Assert
    with pytest.raises(ValueError) as exc_info:
        calcular_descuento(monto_total, es_vip)

    assert str(exc_info.value) == "El monto total debe ser mayor a cero."
