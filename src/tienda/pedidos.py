"""Pedidos: subtotal por categoría, descuento de cliente, cupón y envío."""

import logging
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

import requests
import yaml

from tienda.descuentos import calcular_descuento

logger = logging.getLogger(__name__)

Notificador = Callable[[dict], None]

PROVINCIA_LOCAL = "Buenos Aires"


@dataclass(frozen=True)
class ReglaVolumen:
    cantidad_minima: int
    factor: float


@dataclass(frozen=True)
class TarifaEnvio:
    umbral_bonificacion: float
    costo_bonificado: float
    costo_estandar: float

    def costo(self, total: float) -> float:
        if total > self.umbral_bonificacion:
            return self.costo_bonificado
        return self.costo_estandar


@dataclass(frozen=True)
class Cupon:
    porcentaje: float
    total_minimo: float = 0


REGLAS_POR_CATEGORIA = {
    "electronica": ReglaVolumen(cantidad_minima=10, factor=0.90),
    "ropa": ReglaVolumen(cantidad_minima=5, factor=0.85),
}

# Clave: (tipo de envío, ¿destino en la provincia local?)
TARIFAS_ENVIO = {
    ("express", True): TarifaEnvio(100_000, 0, 3_000),
    ("express", False): TarifaEnvio(100_000, 2_000, 5_000),
    ("normal", True): TarifaEnvio(50_000, 0, 1_500),
    ("normal", False): TarifaEnvio(50_000, 1_000, 2_500),
}

CUPONES = {
    "DESC10": Cupon(porcentaje=0.10),
    "DESC20": Cupon(porcentaje=0.20, total_minimo=20_000),
}


def calcular_importe_item(item: dict) -> float:
    importe = item["precio"] * item["cantidad"]
    regla = REGLAS_POR_CATEGORIA.get(item["categoria"])
    if regla and item["cantidad"] >= regla.cantidad_minima:
        return importe * regla.factor
    return importe


def calcular_subtotal(items: list[dict]) -> float:
    return sum(calcular_importe_item(item) for item in items)


def calcular_envio(total: float, tipo_envio: str, provincia: str) -> float:
    tarifa = TARIFAS_ENVIO.get((tipo_envio, provincia == PROVINCIA_LOCAL))
    return tarifa.costo(total) if tarifa else 0


def aplicar_cupon(total: float, codigo: str | None) -> float:
    cupon = CUPONES.get(codigo)
    if cupon is None or total <= cupon.total_minimo:
        return total
    return total - total * cupon.porcentaje


def _total_con_descuento_de_cliente(pedido: dict, cliente: dict) -> float:
    subtotal = calcular_subtotal(pedido["items"])
    return subtotal - calcular_descuento(subtotal, cliente["es_vip"])


def calcular_presupuesto(pedido: dict, cliente: dict, tipo_envio: str) -> float:
    total = _total_con_descuento_de_cliente(pedido, cliente)
    return total + calcular_envio(total, tipo_envio, cliente["provincia"])


def procesar_pedido(
    pedido: dict,
    cliente: dict,
    tipo_envio: str,
    cupon: str | None,
    notificar: Notificador,
) -> float:
    total = _total_con_descuento_de_cliente(pedido, cliente)
    envio = calcular_envio(total, tipo_envio, cliente["provincia"])
    total = aplicar_cupon(total, cupon) + envio
    notificar({"cliente": cliente["id"], "total": total})
    return total


def crear_notificador_webhook(ruta_config: Path, timeout: float = 5) -> Notificador:
    with ruta_config.open(encoding="utf-8") as archivo:
        url = yaml.safe_load(archivo)["webhook_url"]

    def notificar(datos: dict) -> None:
        try:
            requests.post(url, json=datos, timeout=timeout).raise_for_status()
        except requests.RequestException as error:
            logger.warning("No se pudo notificar el pedido: %s", error)

    return notificar
