"""
integrales.py
=============
Definición de los tres ejercicios del Tema A (integrales dobles).

Cada integral incluye:
    - nombre       : descripción breve
    - f            : función de dos variables f(x, y)
    - xa, xb       : límites de integración en x
    - ya, yb       : límites de integración en y
    - exacto       : valor exacto (solución analítica por integración iterada)
    - formula      : texto de la fórmula (para la salida por pantalla)

IMPORTANTE
----------
Los integrandos corresponden al problema de cuadratura de Gauss-Legendre del
enunciado. El valor de referencia "exacto" 2.230985 coincide con la Integral 3:
    ∫∫ e^-(x²+y²) dx dy = (√π · erf(1))² = π · erf(1)² ≈ 2.230985

Solución analítica (verificación):
    ∫_{-1}^{1}∫_{-1}^{1} (1-x²)(1-y²) dx dy = (4/3)(4/3) = 16/9
    ∫_{0}^{2} ∫_{0}^{3}  x² y²        dx dy = (8/3)(9) = 24
    ∫_{-1}^{1}∫_{-1}^{1} e^-(x²+y²)   dx dy = (√π · erf(1))² ≈ 2.230985
"""


import math

import numpy as np


INTEGRALES = [
    {
        "nombre": "Integral 1",
        "formula": "∬ (1 - x²)(1 - y²) dx dy  sobre [-1, 1] × [-1, 1]",
        "f": lambda x, y: (1.0 - x ** 2) * (1.0 - y ** 2),
        "xa": -1.0, "xb": 1.0,
        "ya": -1.0, "yb": 1.0,
        "exacto": 16.0 / 9.0,
    },
    {
        "nombre": "Integral 2",
        "formula": "∬ x² y² dx dy  sobre [0, 2] × [0, 3]",
        "f": lambda x, y: (x ** 2) * (y ** 2),
        "xa": 0.0, "xb": 2.0,
        "ya": 0.0, "yb": 3.0,
        "exacto": 24.0,
    },
    {
        "nombre": "Integral 3",
        "formula": "∬ exp(-(x² + y²)) dx dy  sobre [-1, 1] × [-1, 1]",
        "f": lambda x, y: np.exp(-(x ** 2 + y ** 2)),
        "xa": -1.0, "xb": 1.0,
        "ya": -1.0, "yb": 1.0,
        "exacto": math.pi * math.erf(1.0) ** 2,
    },
]
