def calcular_descuento(monto_total: float, es_vip: bool) -> float:
    """
    Calcula el monto de descuento aplicable a una orden de compra.

    Reglas de negocio:
    - Si el monto es menor o igual a 0, lanza ValueError.
    - Si el cliente es VIP, aplica un 20% de descuento.
    - Si el cliente no es VIP, aplica un 5% de descuento.
    """
    if monto_total <= 0:
        raise ValueError("El monto total debe ser mayor a cero.")
    if es_vip:
        return monto_total * 0.20
    return monto_total * 0.05
