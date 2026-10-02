from unittest.mock import Mock

import pytest
import requests

from tienda import pedidos
from tienda.pedidos import (
    aplicar_cupon,
    calcular_envio,
    calcular_importe_item,
    calcular_presupuesto,
    crear_notificador_webhook,
    procesar_pedido,
)

CLIENTE_VIP_LOCAL = {"id": 7, "es_vip": True, "provincia": "Buenos Aires"}
CLIENTE_REGULAR_INTERIOR = {"id": 8, "es_vip": False, "provincia": "Córdoba"}


def item(categoria, precio, cantidad):
    return {"categoria": categoria, "precio": precio, "cantidad": cantidad}


@pytest.mark.parametrize(
    ("categoria", "cantidad", "importe_esperado"),
    [
        ("electronica", 9, 900.0),  # por debajo del mínimo: sin descuento
        ("electronica", 10, 900.0),  # 1000 x 0.90
        ("ropa", 4, 400.0),
        ("ropa", 5, 425.0),  # 500 x 0.85
        ("alimentos", 50, 5000.0),  # categoría sin regla de volumen
    ],
)
def test_calcular_importe_item_aplica_descuento_por_volumen(
    categoria, cantidad, importe_esperado
):
    # Arrange
    linea = item(categoria, 100, cantidad)

    # Act
    importe = calcular_importe_item(linea)

    # Assert
    assert importe == pytest.approx(importe_esperado)


@pytest.mark.parametrize(
    ("total", "tipo_envio", "provincia", "costo_esperado"),
    [
        (100_000, "express", "Buenos Aires", 3_000),  # umbral exacto: no bonifica
        (100_001, "express", "Buenos Aires", 0),
        (100_001, "express", "Córdoba", 2_000),
        (50_001, "normal", "Buenos Aires", 0),
        (50_000, "normal", "Córdoba", 2_500),
        (999_999, "retiro", "Córdoba", 0),  # tipo sin tarifa: no cobra envío
    ],
)
def test_calcular_envio_segun_tipo_provincia_y_monto(
    total, tipo_envio, provincia, costo_esperado
):
    # Act
    costo = calcular_envio(total, tipo_envio, provincia)

    # Assert
    assert costo == costo_esperado


@pytest.mark.parametrize(
    ("total", "codigo", "total_esperado"),
    [
        (10_000, "DESC10", 9_000),
        (30_000, "DESC20", 24_000),
        (20_000, "DESC20", 20_000),  # no supera el mínimo del cupón
        (10_000, "INEXISTENTE", 10_000),
        (10_000, None, 10_000),
    ],
)
def test_aplicar_cupon(total, codigo, total_esperado):
    # Act
    resultado = aplicar_cupon(total, codigo)

    # Assert
    assert resultado == pytest.approx(total_esperado)


def test_calcular_presupuesto_cliente_vip_local():
    # Arrange: 10 x 7000 de electrónica = 63000 con volumen; VIP -20% = 50400
    pedido = {"items": [item("electronica", 7_000, 10)]}

    # Act
    presupuesto = calcular_presupuesto(pedido, CLIENTE_VIP_LOCAL, "normal")

    # Assert: 50400 supera 50000, el envío normal local es gratis
    assert presupuesto == pytest.approx(50_400)


def test_procesar_pedido_calcula_envio_antes_del_cupon_y_notifica_una_vez():
    # Arrange: 60000 de alimentos; regular -5% = 57000; envío normal interior
    # sobre 57000 (> 50000) = 1000; DESC20 sobre 57000 = 45600; total 46600
    pedido = {"items": [item("alimentos", 60_000, 1)]}
    notificar = Mock()

    # Act
    total = procesar_pedido(
        pedido, CLIENTE_REGULAR_INTERIOR, "normal", "DESC20", notificar
    )

    # Assert
    assert total == pytest.approx(46_600)
    notificar.assert_called_once_with({"cliente": 8, "total": total})


def test_procesar_pedido_sin_items_es_rechazado():
    # Arrange
    pedido = {"items": []}
    notificar = Mock()

    # Act & Assert
    with pytest.raises(ValueError, match="mayor a cero"):
        procesar_pedido(pedido, CLIENTE_VIP_LOCAL, "express", None, notificar)
    notificar.assert_not_called()


@pytest.fixture
def ruta_config(tmp_path):
    ruta = tmp_path / "config.yaml"
    ruta.write_text("webhook_url: https://hooks.ejemplo.com/pedidos\n")
    return ruta


def test_notificador_webhook_envia_json_con_timeout_y_tls(ruta_config, monkeypatch):
    # Arrange
    post = Mock()
    monkeypatch.setattr(pedidos.requests, "post", post)
    notificar = crear_notificador_webhook(ruta_config, timeout=3)

    # Act
    notificar({"cliente": 7, "total": 100.0})

    # Assert
    post.assert_called_once_with(
        "https://hooks.ejemplo.com/pedidos",
        json={"cliente": 7, "total": 100.0},
        timeout=3,
    )
    post.return_value.raise_for_status.assert_called_once()


def test_notificador_webhook_registra_el_fallo_sin_interrumpir(
    ruta_config, monkeypatch, caplog
):
    # Arrange: stub que simula la caída del servicio
    caida = requests.ConnectionError("servicio caído")
    monkeypatch.setattr(pedidos.requests, "post", Mock(side_effect=caida))
    notificar = crear_notificador_webhook(ruta_config)

    # Act
    notificar({"cliente": 7, "total": 100.0})

    # Assert
    assert "No se pudo notificar el pedido: servicio caído" in caplog.text
