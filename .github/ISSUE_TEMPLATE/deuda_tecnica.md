---
name: Deuda Técnica
about: Refactorización, optimización o actualización de dependencias sin cambio funcional.
title: '[TECH-DEBT] <Módulo afectado y problema estructural>'
labels: 'technical-debt'
assignees: ''
---

## 1. Módulo y Problema Estructural

_Indique el módulo afectado y qué problema de calidad presenta (complejidad, duplicación, dependencias, seguridad)._

## 2. Métricas de la Línea Base

_Pegue la salida de las herramientas de análisis estático que evidencian el problema (versión/commit analizado incluido)._

| Métrica | Valor actual | Umbral aceptable |
| :------ | -----------: | ---------------: |
|         |              |                  |

## 3. Riesgo o Impacto

_¿Qué puede fallar, qué cuesta mantenerlo así o qué vulnerabilidad expone?_

## 4. Estrategia Propuesta

_Técnicas de refactorización y versiones de dependencias objetivo._

## 5. Criterios de Aceptación

- [ ] El comportamiento observable no cambia (o los cambios deliberados están documentados).
- [ ] Las métricas quedan dentro de los umbrales.
- [ ] El pre-commit hook y el pipeline de CI pasan en verde.
- [ ] La cobertura cumple la DoD (≥ 80 % de líneas, ≥ 75 % de ramas).
