EDAD_MINIMA = 18
INGRESOS_MINIMOS = 150000


def evaluar_solicitud_credito(edad: int, ingresos: float, posee_garantia: bool) -> str:
    """
    Evalúa la aprobación de una solicitud de crédito.

    Estructura condicional compleja que requiere evaluación de ramas.
    """
    if (edad >= EDAD_MINIMA and ingresos >= INGRESOS_MINIMOS) or posee_garantia:
        return "CRÉDITO APROBADO"
    else:
        return "CRÉDITO RECHAZADO"
