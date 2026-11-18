"""
main.py
=======
Programa principal del Proyecto Final — Tema A (Análisis de Técnicas Numéricas).

Resuelve las tres integrales dobles del enunciado de forma:
    - analítica (valor exacto por integración iterada) y
    - numérica (Trapecio, Simpson 1/3, Simpson 3/8, Romberg y Gauss-Legendre),

calcula el error absoluto de cada método y genera las gráficas comparativas
y de convergencia.

Uso:
    py main.py                 -> ejecuta todo y muestra las gráficas por pantalla
    py main.py --solo-guardar  -> ejecuta todo y solo guarda las PNG en ./graficas
"""

import os
import sys

# Asegurar salida UTF-8 en consola (símbolos matemáticos: ∬, ∫, −, ², ×)
for _s in (sys.stdout, sys.stderr):
    if hasattr(_s, "reconfigure"):
        _s.reconfigure(encoding="utf-8", errors="replace")

from integrales import INTEGRALES
from metodos import (trapecio, simpson13, simpson38, romberg, gauss_legendre,
                     integral_doble)
from graficas import graficar_barras, graficar_convergencia, graficar_comparacion_global


# Métodos a comparar: (nombre, función 1D, n en cada dirección)
METODOS = [
    ("Trapecio (n=100)", trapecio, 100),
    ("Simpson 1/3 (n=100)", simpson13, 100),
    ("Simpson 3/8 (n=99)", simpson38, 99),
    ("Romberg (m=8)", romberg, 8),
    ("Gauss-Legendre (2 ptos)", gauss_legendre, 2),
    ("Gauss-Legendre (3 ptos)", gauss_legendre, 3),
    ("Gauss-Legendre (5 ptos)", gauss_legendre, 5),
]


def _formatear_tabla(resultados, exacto):
    """Devuelve una cadena con la tabla comparativa de resultados."""
    lineas = []
    lineas.append(f"{'Método':<26} {'Resultado':>18} {'Error absoluto':>20} {'Error rel.' :>14}")
    lineas.append("-" * 80)
    for nombre, valor in resultados:
        err = abs(valor - exacto)
        rel = err / abs(exacto) if exacto != 0 else float("nan")
        lineas.append(f"{nombre:<26} {valor:>18.10f} {err:>20.6e} {rel:>13.3e}")
    lineas.append("-" * 80)
    lineas.append(f"{'Valor exacto (analítico)':<26} {exacto:>18.10f}")
    return "\n".join(lineas)


def main():
    solo_guardar = "--solo-guardar" in sys.argv

    print("=" * 80)
    print("PROYECTO FINAL - ANÁLISIS DE TÉCNICAS NUMÉRICAS")
    print("Tema A: Resolución de integrales dobles (analítica y numérica)")
    print("=" * 80)

    global_results = []

    for integ in INTEGRALES:
        f = integ["f"]
        xa, xb = integ["xa"], integ["xb"]
        ya, yb = integ["ya"], integ["yb"]
        exacto = integ["exacto"]

        print("\n" + "=" * 80)
        print(f"{integ['nombre']}:  {integ['formula']}")
        print(f"Valor exacto (analítico) = {exacto:.10f}")
        print("=" * 80)

        resultados = []
        for nombre, metodo, n in METODOS:
            valor = integral_doble(f, xa, xb, ya, yb, metodo, n)
            resultados.append((nombre, valor))

        print(_formatear_tabla(resultados, exacto))

        # Mejor método (menor error absoluto)
        mejor = min(resultados, key=lambda r: abs(r[1] - exacto))
        print(f"\n>>> Método más eficiente para {integ['nombre']}: {mejor[0]} "
              f"(error = {abs(mejor[1] - exacto):.6e})")

        global_results.append((integ["nombre"], resultados))

    print("\n" + "=" * 80)
    print("GENERANDO GRÁFICAS ...")
    print("=" * 80)

    archivos = []
    for integ in INTEGRALES:
        resultados = dict(global_results)[integ["nombre"]]
        # para la gráfica de barras usamos el error
        resultados_err = [(n, abs(v - integ["exacto"])) for n, v in resultados]
        a1 = graficar_barras(integ, resultados_err)
        a2 = graficar_convergencia(integ)
        archivos += [a1, a2]
        print(f"  {integ['nombre']}: {os.path.basename(a1)}, {os.path.basename(a2)}")

    a3 = graficar_comparacion_global(global_results)
    archivos.append(a3)
    print(f"  Comparación global: {os.path.basename(a3)}")

    print("\nGráficas guardadas en la carpeta 'graficas/'.")

    if not solo_guardar:
        try:
            import matplotlib.pyplot as plt
            plt.show()
        except Exception as e:
            print(f"(No se pudo mostrar la ventana interactiva: {e})")


if __name__ == "__main__":
    main()
