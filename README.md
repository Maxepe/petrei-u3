# petrei-u3

Trabajos prácticos de la Unidad 3 (Verificación y Validación) de Metodología de Sistemas II.
El paquete `tienda` reúne la lógica de descuentos, crédito y pedidos, con su suite de
pruebas y la cadena de calidad automatizada.

## Requisitos

- Python 3.14
- Git (en Windows, Git for Windows: el hook se ejecuta con su `sh`)
- Docker, solo para el análisis con SonarQube

## Instalación

```bash
python -m venv .venv
.venv/Scripts/python -m pip install -r requirements.txt -r requirements-dev.txt   # Windows
.venv/bin/python -m pip install -r requirements.txt -r requirements-dev.txt       # Linux/macOS
```

## Activar el pre-commit hook

Una vez por clon:

```bash
git config core.hooksPath .githooks
```

A partir de ahí cada `git commit` ejecuta, en orden y cortando en el primer fallo:

1. **Formatter:** `black --check --diff src tests`
2. **Linter:** `ruff check src tests`
3. **Pruebas:** `pytest`, con cobertura mínima del 80 % total y del 75 % de ramas

## Ejecutar los controles a mano

```bash
black --check src tests
ruff check src tests
pytest                              # reporte HTML en htmlcov/index.html
radon cc -s -a src                  # complejidad ciclomática
pip-audit -r requirements.txt       # vulnerabilidades en dependencias
```

## CI

`.github/workflows/calidad.yml` repite los mismos controles, más `pip-audit`, en cada push
a `main` y en cada Pull Request.

## Plantillas de issue

`.github/ISSUE_TEMPLATE/` contiene las plantillas de bug y de deuda técnica. Las etiquetas
del repositorio siguen la matriz de categorización del TP1: `bug`, `hotfix`, `feature`,
`release`, `technical-debt` y `documentation`.
