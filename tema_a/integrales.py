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
Los límites fueron leídos de la imagen del enunciado. Verifica visualmente
los límites en tu PDF original. El enunciado además menciona un valor de
referencia "exacto" de 2.230985 para el problema de Gauss-Legendre de orden
dos y tres; si alguno de tus límites difiere, actualiza ``exacto``.

Solución analítica (verificación):
    ∫_{-1}^{1}∫_{-1}^{1} (1 - x² - y²) dx dy  = 4/3
    ∫_{1}^{2} ∫_{1}^{3}  x² y²         dx dy  = (7/3)(26/3) = 182/9
    ∫_{-1}^{1}∫_{-1}^{1} (x² + y²)     dx dy  = 8/3
"""


INTEGRALES = [
    {
        "nombre": "Integral 1",
        "formula": "∬ (1 - x² - y²) dx dy  sobre [-1, 1] × [-1, 1]",
        "f": lambda x, y: 1.0 - x ** 2 - y ** 2,
        "xa": -1.0, "xb": 1.0,
        "ya": -1.0, "yb": 1.0,
        "exacto": 4.0 / 3.0,
    },
    {
        "nombre": "Integral 2",
        "formula": "∬ x² y² dx dy  sobre [1, 2] × [1, 3]",
        "f": lambda x, y: (x ** 2) * (y ** 2),
        "xa": 1.0, "xb": 2.0,
        "ya": 1.0, "yb": 3.0,
        "exacto": 182.0 / 9.0,
    },
    {
        "nombre": "Integral 3",
        "formula": "∬ (x² + y²) dx dy  sobre [-1, 1] × [-1, 1]",
        "f": lambda x, y: x ** 2 + y ** 2,
        "xa": -1.0, "xb": 1.0,
        "ya": -1.0, "yb": 1.0,
        "exacto": 8.0 / 3.0,
    },
]
