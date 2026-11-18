"""
metodos.py
==========
Módulo de métodos numéricos de integración.

Contiene los métodos vistos en clase (1D) y una función genérica que los
aplica a integrales dobles mediante integración iterada (integral en una
dirección y luego en la otra).

Todos los métodos tienen la firma:  metodo(f, a, b, n) -> float
donde:
    f : función de una variable (float -> float o array -> array)
    a : límite inferior
    b : límite superior
    n : número de subintervalos (o puntos, o niveles según el método)
"""

import numpy as np


# --------------------------------------------------------------------------
# Métodos de integración en 1D
# --------------------------------------------------------------------------

def trapecio(f, a, b, n):
    """Regla del trapecio compuesta con ``n`` subintervalos."""
    x = np.linspace(a, b, n + 1)
    y = np.asarray(f(x), dtype=float)
    h = (b - a) / n
    return h * (0.5 * y[0] + np.sum(y[1:-1]) + 0.5 * y[-1])


def simpson13(f, a, b, n):
    """Regla de Simpson 1/3 compuesta (``n`` debe ser par; se fuerza si no)."""
    if n % 2 == 1:
        n += 1
    x = np.linspace(a, b, n + 1)
    y = np.asarray(f(x), dtype=float)
    h = (b - a) / n
    return h / 3.0 * (y[0] + y[-1] + 4.0 * np.sum(y[1:-1:2]) + 2.0 * np.sum(y[2:-2:2]))


def simpson38(f, a, b, n):
    """Regla de Simpson 3/8 compuesta (``n`` debe ser múltiplo de 3; se fuerza)."""
    n = int(np.ceil(n / 3.0) * 3)
    x = np.linspace(a, b, n + 1)
    y = np.asarray(f(x), dtype=float)
    h = (b - a) / n
    s = y[0] + y[-1]
    for i in range(1, n):
        w = 3.0 if (i % 3 != 0) else 2.0
        s += w * y[i]
    return 3.0 * h / 8.0 * s


def romberg(f, a, b, m=8):
    """
    Integración de Romberg con ``m`` niveles (extrapolación de Richardson).

    Devuelve la mejor aproximación de la tabla de Romberg (último elemento).
    """
    R = np.zeros((m, m))
    h = float(b - a)
    R[0, 0] = 0.5 * h * (f(a) + f(b))
    for i in range(1, m):
        h *= 0.5
        # Suma de los puntos medios nuevos (índices impares)
        s = sum(f(a + (2 * k - 1) * h) for k in range(1, 2 ** (i - 1) + 1))
        R[i, 0] = 0.5 * R[i - 1, 0] + h * s
        for j in range(1, i + 1):
            R[i, j] = R[i, j - 1] + (R[i, j - 1] - R[i - 1, j - 1]) / (4.0 ** j - 1.0)
    return R[m - 1, m - 1]


def gauss_legendre(f, a, b, n):
    """
    Cuadratura de Gauss-Legendre con ``n`` puntos.

    Los nodos y pesos se obtienen de ``numpy.polynomial.legendre.leggauss``
    (raíces del polinomio de Legendre Pn en [-1, 1]) y se reescalan a [a, b].
    """
    x, w = np.polynomial.legendre.leggauss(n)
    t = 0.5 * (b - a) * x + 0.5 * (a + b)
    return 0.5 * (b - a) * np.sum(w * np.asarray(f(t), dtype=float))


# --------------------------------------------------------------------------
# Integración en 2D (integral doble iterada)
# --------------------------------------------------------------------------

def integral_doble(f, xa, xb, ya, yb, metodo, nx, ny=None):
    """
    Integral doble  ∫∫ f(x, y) dx dy  sobre [xa, xb] × [ya, yb].

    Usa ``metodo`` (cualquiera de los métodos 1D de arriba) tanto para la
    integración interior (en x) como para la exterior (en y).

    Parámetros
    ----------
    f      : función de dos variables  f(x, y)
    xa, xb : límites en x
    ya, yb : límites en y
    metodo : función 1D (trapecio, simpson13, simpson38, romberg, gauss_legendre)
    nx, ny : número de subintervalos/puntos/niveles en x y en y (ny = nx por defecto)
    """
    if ny is None:
        ny = nx

    def g_escalar(y):
        # Integra en x para un valor fijo de y
        return metodo(lambda x: f(x, y), xa, xb, nx)

    # Vectorizamos g para que los métodos exteriores puedan llamarla con
    # arreglos de valores de y (p. ej. np.linspace en Trapecio/Simpson/Gauss).
    g = np.vectorize(g_escalar, otypes=[float])

    # Integra en y
    return metodo(g, ya, yb, ny)
