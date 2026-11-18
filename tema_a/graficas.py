"""
graficas.py
===========
Genera las gráficas del proyecto:

1. Gráfica de barras por integral: compara el error absoluto de cada método
   (escala logarítmica) para concluir cuál es más eficiente.
2. Gráfica de convergencia por integral: error vs. número de subintervalos/
   puntos para los métodos iterativos (Trapecio, Simpson 1/3, Gauss-Legendre).

Todas las figuras se guardan en la carpeta ``graficas/`` (PNG, 150 dpi) para
poder incluirlas en el informe, y además se muestran por pantalla.
"""

import os

import numpy as np
import matplotlib
import matplotlib.pyplot as plt

from metodos import trapecio, simpson13, gauss_legendre, integral_doble


# Colores consistentes para cada método
COLORES = {
    "Trapecio": "#1f77b4",
    "Simpson 1/3": "#2ca02c",
    "Simpson 3/8": "#ff7f0e",
    "Romberg": "#9467bd",
    "Gauss-Legendre": "#d62728",
}


def _color_de(nombre):
    """Devuelve el color asociado a un método a partir de su nombre completo."""
    for clave, color in COLORES.items():
        if nombre.startswith(clave):
            return color
    return "#888888"


def _carpeta_graficas():
    base = os.path.dirname(os.path.abspath(__file__))
    carpeta = os.path.join(base, "graficas")
    os.makedirs(carpeta, exist_ok=True)
    return carpeta


def graficar_barras(integral, resultados):
    """
    Gráfica de barras del error absoluto por método (escala logarítmica).

    Parámetros
    ----------
    integral   : dict de ``integrales.INTEGRALES``
    resultados : lista de tuplas (nombre_método, error_absoluto)
    """
    nombres = [r[0] for r in resultados]
    errores = [max(r[1], 1e-16) for r in resultados]  # evitar log(0)

    fig, ax = plt.subplots(figsize=(10, 5))
    barras = ax.bar(nombres, errores, color=[_color_de(n) for n in nombres])
    ax.set_yscale("log")
    ax.set_ylabel("Error absoluto (escala log)")
    ax.set_title(f"{integral['nombre']}: error absoluto por método\n{integral['formula']}", fontsize=10)
    ax.grid(axis="y", which="both", linestyle="--", alpha=0.5)
    plt.setp(ax.get_xticklabels(), rotation=30, ha="right", fontsize=8)

    # Etiqueta del valor sobre cada barra
    for b, e in zip(barras, errores):
        ax.text(b.get_x() + b.get_width() / 2, e, f"{e:.3e}",
                ha="center", va="bottom", fontsize=7, rotation=60)

    fig.tight_layout()
    archivo = os.path.join(_carpeta_graficas(), f"barras_{integral['nombre'].replace(' ', '_').lower()}.png")
    fig.savefig(archivo, dpi=150)
    plt.close(fig)
    return archivo


def graficar_convergencia(integral):
    """
    Gráfica de convergencia: error absoluto vs. n (subintervalos o puntos)
    para Trapecio, Simpson 1/3 y Gauss-Legendre (orden variable).
    """
    f = integral["f"]
    xa, xb = integral["xa"], integral["xb"]
    ya, yb = integral["ya"], integral["yb"]
    exacto = integral["exacto"]

    ns_trap = [4, 8, 16, 32, 64, 128]
    ns_simp = [4, 8, 16, 32, 64, 128]
    ns_gauss = [2, 3, 4, 5, 6, 7]

    err_trap = [abs(integral_doble(f, xa, xb, ya, yb, trapecio, n) - exacto) for n in ns_trap]
    err_simp = [abs(integral_doble(f, xa, xb, ya, yb, simpson13, n) - exacto) for n in ns_simp]
    err_gauss = [abs(integral_doble(f, xa, xb, ya, yb, gauss_legendre, n) - exacto) for n in ns_gauss]

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(ns_trap, err_trap, "o-", label="Trapecio", color=COLORES["Trapecio"])
    ax.plot(ns_simp, err_simp, "s-", label="Simpson 1/3", color=COLORES["Simpson 1/3"])
    ax.plot(ns_gauss, err_gauss, "^-", label="Gauss-Legendre", color=COLORES["Gauss-Legendre"])
    ax.set_yscale("log")
    ax.set_xlabel("n (subintervalos o puntos)")
    ax.set_ylabel("Error absoluto (escala log)")
    ax.set_title(f"{integral['nombre']}: convergencia de los métodos\n{integral['formula']}", fontsize=10)
    ax.grid(True, which="both", linestyle="--", alpha=0.5)
    ax.legend()

    fig.tight_layout()
    archivo = os.path.join(_carpeta_graficas(), f"convergencia_{integral['nombre'].replace(' ', '_').lower()}.png")
    fig.savefig(archivo, dpi=150)
    plt.close(fig)
    return archivo


def graficar_comparacion_global(integrales_resultados):
    """
    Gráfica conjunta (una sola figura) que compara, para TODAS las integrales,
    el error de cada método. Facilita la comparación "una gráfica sobre otra".
    """
    metodos_orden = []
    for _, resultados in integrales_resultados:
        for nombre, _ in resultados:
            if nombre not in metodos_orden:
                metodos_orden.append(nombre)

    fig, ax = plt.subplots(figsize=(10, 6))
    x = np.arange(len(integrales_resultados))
    ancho = 0.8 / max(len(metodos_orden), 1)

    for i, nombre in enumerate(metodos_orden):
        errores = []
        for _, resultados in integrales_resultados:
            d = dict(resultados)
            e = d.get(nombre, np.nan)
            errores.append(max(e, 1e-16) if e == e else 1e-16)
        ax.bar(x + (i - len(metodos_orden) / 2) * ancho, errores, ancho, label=nombre)

    ax.set_yscale("log")
    ax.set_xticks(x)
    ax.set_xticklabels([nombre for nombre, _ in integrales_resultados])
    ax.set_ylabel("Error absoluto (escala log)")
    ax.set_title("Comparación global de errores por método e integral")
    ax.grid(axis="y", which="both", linestyle="--", alpha=0.5)
    ax.legend(ncol=2, fontsize=8)

    fig.tight_layout()
    archivo = os.path.join(_carpeta_graficas(), "comparacion_global.png")
    fig.savefig(archivo, dpi=150)
    plt.close(fig)
    return archivo
