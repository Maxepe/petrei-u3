def evaluar_solicitud_credito(edad: int, ingresos: float, posee_garantia: bool) -> str:
    """
    Evalúa la aprobación de una solicitud de crédito.

    Estructura condicional compleja que requiere evaluación de ramas.
    """
    if (edad >= 18 and ingresos >= 150000) or posee_garantia:
        return "CRÉDITO APROBADO"
    else:
        return "CRÉDITO RECHAZADO"
