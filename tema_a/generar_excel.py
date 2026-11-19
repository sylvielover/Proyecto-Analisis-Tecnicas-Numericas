"""
generar_excel.py
================
Genera el archivo  Tema_A_Excel.xlsx  con los cálculos del Tema A.

El archivo contiene:
    - Resumen         : enunciado, comparación de métodos y errores
    - Metodos_1D      : integrales 1D (de x² / y²) con tablas demostrativas
                        con fórmulas de Excel en vivo (Trapecio y Simpson)
    - Gauss_Romberg   : nodos/pesos de Gauss-Legendre y tabla de Romberg
    - Metodologia     : explicación de la separabilidad y combinación 2D

Uso:
    py generar_excel.py
"""

import os

import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

import math

import numpy as np

from metodos import trapecio, simpson13, simpson38, romberg, gauss_legendre


# ---------------------------------------------------------------------------
# 1. Cálculos numéricos (reutiliza los métodos de metodos.py)
# ---------------------------------------------------------------------------

# Métodos a comparar
METODOS = [
    ("Trapecio (n=100)", trapecio, 100),
    ("Simpson 1/3 (n=100)", simpson13, 100),
    ("Simpson 3/8 (n=99)", simpson38, 99),
    ("Romberg (m=8)", romberg, 8),
    ("Gauss-Legendre (2 ptos)", gauss_legendre, 2),
    ("Gauss-Legendre (3 ptos)", gauss_legendre, 3),
    ("Gauss-Legendre (5 ptos)", gauss_legendre, 5),
]

# Integrales 1D necesarias (los tres integrandos son separables: f(x)·g(y))
# (nombre, función, a, b, valor exacto)
INTEGRALES_1D = [
    ("∫ (1−x²) dx  sobre [-1, 1]", lambda x: 1.0 - x ** 2, -1.0, 1.0, 4.0 / 3.0),
    ("∫ x² dx  sobre [0, 2]", lambda x: x ** 2, 0.0, 2.0, 8.0 / 3.0),
    ("∫ y² dy  sobre [0, 3]", lambda y: y ** 2, 0.0, 3.0, 9.0),
    ("∫ e^(−x²) dx  sobre [-1, 1]", lambda x: np.exp(-(x ** 2)), -1.0, 1.0,
     math.sqrt(math.pi) * math.erf(1.0)),
]

# Resultados 1D por método: resultados[método_idx][integral_1D_idx] = valor
RESULTADOS_1D = []
for nombre, metodo, n in METODOS:
    fila = []
    for _, f, a, b, _ in INTEGRALES_1D:
        fila.append(metodo(f, a, b, n))
    RESULTADOS_1D.append(fila)

# Índices de las cuatro integrales 1D
I_1MX2 = 0   # ∫ (1−x²) sobre [-1,1]  -> I1
I_X2_B = 1   # ∫ x² sobre [0,2]        -> I2
I_Y2_B = 2   # ∫ y² sobre [0,3]        -> I2
I_EXPX = 3   # ∫ e^(−x²) sobre [-1,1]  -> I3

# Combinación 2D -> integrales dobles del Tema A (todas separables)
#   I1 = ∫(1−x²) · ∫(1−y²)
#   I2 = ∫x² · ∫y²
#   I3 = ∫e^(−x²) · ∫e^(−y²)
def combinar(r):
    i1 = r[I_1MX2] * r[I_1MX2]   # (1−x²) y (1−y²) son la misma integral
    i2 = r[I_X2_B] * r[I_Y2_B]
    i3 = r[I_EXPX] * r[I_EXPX]   # e^(−x²) y e^(−y²) son la misma integral
    return i1, i2, i3

EXACTOS = (16.0 / 9.0, 24.0, math.pi * math.erf(1.0) ** 2)
RESULTADOS_2D = [combinar(r) for r in RESULTADOS_1D]

NOMBRES_INTEGRALES = ["Integral 1: ∬ (1 − x²)(1 − y²) dx dy",
                      "Integral 2: ∬ x² y² dx dy",
                      "Integral 3: ∬ e^(−(x² + y²)) dx dy"]


# ---------------------------------------------------------------------------
# 2. Utilidades de estilo
# ---------------------------------------------------------------------------

TITULO = Font(bold=True, size=14, color="FFFFFF")
SUBTITULO = Font(bold=True, size=11, color="1F4E79")
ENCABEZADO = Font(bold=True, size=10, color="FFFFFF")
TEXTO = Font(size=10)
NEGRITA = Font(bold=True, size=10)
RELLENO_TITULO = PatternFill("solid", fgColor="1F4E79")
RELLENO_ENC = PatternFill("solid", fgColor="4472C4")
RELLENO_ALT = PatternFill("solid", fgColor="D9E2F3")
RELLENO_VERDE = PatternFill("solid", fgColor="C6EFCE")
BORDE = Border(*[Side(style="thin", color="BFBFBF")] * 4)


def poner(ws, celda, valor, fuente=TEXTO, relleno=None, alineacion=None, formato=None):
    c = ws[celda]
    c.value = valor
    c.font = fuente
    if relleno:
        c.fill = relleno
    if alineacion:
        c.alignment = alineacion
    if formato:
        c.number_format = formato
    return c


def ancho_columnas(ws, anchos):
    for i, w in enumerate(anchos, start=1):
        ws.column_dimensions[get_column_letter(i)].width = w


# ---------------------------------------------------------------------------
# 3. Hoja "Resumen"
# ---------------------------------------------------------------------------

def hoja_resumen(wb):
    ws = wb.active
    ws.title = "Resumen"
    ancho_columnas(ws, [42, 18, 16, 18, 16, 18, 16])

    poner(ws, "A1", "PROYECTO FINAL — TEMA A", TITULO, RELLENO_TITULO)
    poner(ws, "A2", "Cálculos en Excel: integrales dobles (analítica y numérica)", SUBTITULO)
    ws.merge_cells("A1:G1")
    ws.merge_cells("A2:G2")

    r = 4
    poner(ws, f"A{r}", "ENUNCIADO", ENCABEZADO, RELLENO_ENC)
    r += 1
    for j, h in enumerate(["Integral", "Límites x", "Límites y", "Valor exacto"]):
        poner(ws, f"{get_column_letter(j+1)}{r}", h, ENCABEZADO, RELLENO_ENC)
    r += 1
    datos = [
        ("∬ (1 − x²)(1 − y²) dx dy", "[-1, 1]", "[-1, 1]", 16 / 9),
        ("∬ x² y² dx dy", "[0, 2]", "[0, 3]", 24),
        ("∬ e^(−(x² + y²)) dx dy", "[-1, 1]", "[-1, 1]", math.pi * math.erf(1.0) ** 2),
    ]
    for d in datos:
        poner(ws, f"A{r}", d[0], TEXTO)
        poner(ws, f"B{r}", d[1], TEXTO)
        poner(ws, f"C{r}", d[2], TEXTO)
        poner(ws, f"D{r}", d[3], TEXTO, formato="0.0000000000")
        r += 1

    r += 1
    poner(ws, f"A{r}", "COMPARACIÓN DE MÉTODOS (resultado y error absoluto)", ENCABEZADO, RELLENO_ENC)
    r += 1
    poner(ws, f"A{r}", "Método", ENCABEZADO, RELLENO_ENC)
    for j in range(3):
        col = 2 + 2 * j
        poner(ws, f"{get_column_letter(col)}{r}", f"I{j+1} (resultado)", ENCABEZADO, RELLENO_ENC)
        poner(ws, f"{get_column_letter(col+1)}{r}", f"I{j+1} (error abs.)", ENCABEZADO, RELLENO_ENC)
    r += 1
    for idx, (nombre, _, _) in enumerate(METODOS):
        relleno = RELLENO_ALT if idx % 2 else None
        poner(ws, f"A{r}", nombre, TEXTO, relleno)
        for j in range(3):
            col = 2 + 2 * j
            val = RESULTADOS_2D[idx][j]
            err = abs(val - EXACTOS[j])
            poner(ws, f"{get_column_letter(col)}{r}", val, TEXTO, relleno, formato="0.0000000000")
            poner(ws, f"{get_column_letter(col+1)}{r}", err, TEXTO, relleno, formato="0.0000E+00")
        r += 1
    poner(ws, f"A{r}", "Valor exacto", NEGRITA, RELLENO_VERDE)
    for j in range(3):
        col = 2 + 2 * j
        poner(ws, f"{get_column_letter(col)}{r}", EXACTOS[j], NEGRITA, RELLENO_VERDE, formato="0.0000000000")
        poner(ws, f"{get_column_letter(col+1)}{r}", "—", NEGRITA, RELLENO_VERDE)
    r += 1

    r += 1
    poner(ws, f"A{r}", "MÉTODO MÁS EFICIENTE POR INTEGRAL", ENCABEZADO, RELLENO_ENC)
    r += 1
    for j in range(3):
        mejor_idx = min(range(len(METODOS)), key=lambda i: abs(RESULTADOS_2D[i][j] - EXACTOS[j]))
        poner(ws, f"A{r}", NOMBRES_INTEGRALES[j], TEXTO)
        poner(ws, f"B{r}", METODOS[mejor_idx][0], TEXTO)
        poner(ws, f"C{r}", abs(RESULTADOS_2D[mejor_idx][j] - EXACTOS[j]), TEXTO, formato="0.0000E+00")
        r += 1
    return ws


# ---------------------------------------------------------------------------
# 4. Hoja "Metodos_1D" (con tablas demostrativas en vivo)
# ---------------------------------------------------------------------------

def hoja_metodos_1d(wb):
    ws = wb.create_sheet("Metodos_1D")
    ancho_columnas(ws, [46, 14, 14, 12, 14])

    poner(ws, "A1", "MÉTODOS 1D APLICADOS A LAS INTEGRALES DEL TEMA A", TITULO, RELLENO_TITULO)
    poner(ws, "A2", "Los integrandos son separables; la integral doble se reduce a estas integrales 1D.", SUBTITULO)
    ws.merge_cells("A1:E1")
    ws.merge_cells("A2:E2")

    r = 4
    poner(ws, f"A{r}", "INTEGRALES 1D REQUERIDAS", ENCABEZADO, RELLENO_ENC)
    r += 1
    for j, h in enumerate(["Integral 1D", "a", "b", "Valor exacto"]):
        poner(ws, f"{get_column_letter(j+1)}{r}", h, ENCABEZADO, RELLENO_ENC)
    r += 1
    for nombre, _f, a, b, exacto in INTEGRALES_1D:
        poner(ws, f"A{r}", nombre, TEXTO)
        poner(ws, f"B{r}", a, TEXTO)
        poner(ws, f"C{r}", b, TEXTO)
        poner(ws, f"D{r}", exacto, TEXTO, formato="0.0000000000")
        r += 1

    # --- Tabla demostrativa Trapecio (n=8) ---
    r += 1
    poner(ws, f"A{r}", "DEMOSTRACIÓN — Trapecio compuesto (n=8) sobre ∫ e^(−x²) dx en [-1, 1]", ENCABEZADO, RELLENO_ENC)
    r += 1
    poner(ws, f"A{r}", "i", ENCABEZADO, RELLENO_ENC)
    poner(ws, f"B{r}", "x_i", ENCABEZADO, RELLENO_ENC)
    poner(ws, f"C{r}", "f(x_i) = e^(−x_i²)", ENCABEZADO, RELLENO_ENC)
    r += 1
    n_trap = 8
    h_trap = 2.0 / n_trap
    inicio = r
    for i in range(n_trap + 1):
        xi = -1.0 + i * h_trap
        poner(ws, f"A{r}", i, TEXTO)
        poner(ws, f"B{r}", xi, TEXTO, formato="0.00")
        poner(ws, f"C{r}", f"=EXP(-(B{r}^2))", TEXTO, formato="0.0000")
        r += 1
    fin = r - 1
    poner(ws, f"A{r}", "Trapecio =", NEGRITA)
    poner(ws, f"C{r}", f"={h_trap}*(0.5*C{inicio} + SUM(C{inicio+1}:C{fin-1}) + 0.5*C{fin})",
          NEGRITA, RELLENO_VERDE, formato="0.0000000000")
    poner(ws, f"D{r}", "(= h·(½f0 + Σfi + ½fn))", TEXTO)
    r += 2

    # --- Tabla demostrativa Simpson 1/3 (n=8) ---
    poner(ws, f"A{r}", "DEMOSTRACIÓN — Simpson 1/3 compuesta (n=8) sobre ∫ e^(−x²) dx en [-1, 1]", ENCABEZADO, RELLENO_ENC)
    r += 1
    for j, h in enumerate(["i", "x_i", "f(x_i) = e^(−x_i²)", "peso w_i", "w_i·f(x_i)"]):
        poner(ws, f"{get_column_letter(j+1)}{r}", h, ENCABEZADO, RELLENO_ENC)
    r += 1
    n_s13 = 8
    h_s13 = 2.0 / n_s13
    inicio = r
    for i in range(n_s13 + 1):
        xi = -1.0 + i * h_s13
        w = 1.0 if (i == 0 or i == n_s13) else (4.0 if i % 2 == 1 else 2.0)
        poner(ws, f"A{r}", i, TEXTO)
        poner(ws, f"B{r}", xi, TEXTO, formato="0.00")
        poner(ws, f"C{r}", f"=EXP(-(B{r}^2))", TEXTO, formato="0.0000")
        poner(ws, f"D{r}", w, TEXTO)
        poner(ws, f"E{r}", f"=C{r}*D{r}", TEXTO, formato="0.0000")
        r += 1
    fin = r - 1
    poner(ws, f"A{r}", "Simpson 1/3 =", NEGRITA)
    poner(ws, f"C{r}", f"=({h_s13}/3)*SUM(E{inicio}:E{fin})", NEGRITA, RELLENO_VERDE, formato="0.0000000000")
    poner(ws, f"D{r}", "(= (h/3)·Σ wᵢfᵢ)", TEXTO)
    r += 2

    # --- Tabla demostrativa Simpson 3/8 (n=9) ---
    poner(ws, f"A{r}", "DEMOSTRACIÓN — Simpson 3/8 compuesta (n=9) sobre ∫ e^(−x²) dx en [-1, 1]", ENCABEZADO, RELLENO_ENC)
    r += 1
    for j, h in enumerate(["i", "x_i", "f(x_i) = e^(−x_i²)", "peso w_i", "w_i·f(x_i)"]):
        poner(ws, f"{get_column_letter(j+1)}{r}", h, ENCABEZADO, RELLENO_ENC)
    r += 1
    n_s38 = 9
    h_s38 = 2.0 / n_s38
    inicio = r
    for i in range(n_s38 + 1):
        xi = -1.0 + i * h_s38
        w = 1.0 if (i == 0 or i == n_s38) else (2.0 if i % 3 == 0 else 3.0)
        poner(ws, f"A{r}", i, TEXTO)
        poner(ws, f"B{r}", xi, TEXTO, formato="0.0000")
        poner(ws, f"C{r}", f"=EXP(-(B{r}^2))", TEXTO, formato="0.0000")
        poner(ws, f"D{r}", w, TEXTO)
        poner(ws, f"E{r}", f"=C{r}*D{r}", TEXTO, formato="0.0000")
        r += 1
    fin = r - 1
    poner(ws, f"A{r}", "Simpson 3/8 =", NEGRITA)
    poner(ws, f"C{r}", f"=(3*{h_s38}/8)*SUM(E{inicio}:E{fin})", NEGRITA, RELLENO_VERDE, formato="0.0000000000")
    poner(ws, f"D{r}", "(= (3h/8)·Σ wᵢfᵢ)", TEXTO)
    r += 2

    # --- Resultados 1D por método (n grande) ---
    poner(ws, f"A{r}", "RESULTADOS 1D POR MÉTODO (n grande, calculados)", ENCABEZADO, RELLENO_ENC)
    r += 1
    poner(ws, f"A{r}", "Método", ENCABEZADO, RELLENO_ENC)
    for j, (nombre, _f, _a, _b, _e) in enumerate(INTEGRALES_1D):
        poner(ws, f"{get_column_letter(j+2)}{r}", nombre, ENCABEZADO, RELLENO_ENC)
    r += 1
    for idx, (nombre, _m, _n) in enumerate(METODOS):
        relleno = RELLENO_ALT if idx % 2 else None
        poner(ws, f"A{r}", nombre, TEXTO, relleno)
        for j in range(4):
            poner(ws, f"{get_column_letter(j+2)}{r}", RESULTADOS_1D[idx][j], TEXTO, relleno,
                  formato="0.0000000000")
        r += 1
    return ws


# ---------------------------------------------------------------------------
# 5. Hoja "Gauss_Romberg"
# ---------------------------------------------------------------------------

def _tabla_romberg(f, a, b, m):
    """Devuelve la tabla de Romberg completa (lista de listas)."""
    R = [[0.0] * m for _ in range(m)]
    h = b - a
    R[0][0] = 0.5 * h * (f(a) + f(b))
    for i in range(1, m):
        h /= 2.0
        s = sum(f(a + (2 * k - 1) * h) for k in range(1, 2 ** (i - 1) + 1))
        R[i][0] = 0.5 * R[i - 1][0] + h * s
        for j in range(1, i + 1):
            R[i][j] = R[i][j - 1] + (R[i][j - 1] - R[i - 1][j - 1]) / (4.0 ** j - 1.0)
    return R


def hoja_gauss_romberg(wb):
    from numpy.polynomial.legendre import leggauss

    ws = wb.create_sheet("Gauss_Romberg")
    ancho_columnas(ws, [52, 16, 16, 16, 16, 16])

    poner(ws, "A1", "CUADRATURA DE GAUSS-LEGENDRE  Y  ROMBERG", TITULO, RELLENO_TITULO)
    ws.merge_cells("A1:F1")

    r = 3
    # --- Nodos y pesos de Gauss-Legendre (n=2, 3, 5) ---
    for n in (2, 3, 5):
        x, w = leggauss(n)
        poner(ws, f"A{r}", f"Gauss-Legendre: n = {n} puntos (nodos xᵢ y pesos wᵢ en [-1, 1])",
              ENCABEZADO, RELLENO_ENC)
        r += 1
        poner(ws, f"A{r}", "Nodo xᵢ", ENCABEZADO, RELLENO_ENC)
        poner(ws, f"B{r}", "Peso wᵢ", ENCABEZADO, RELLENO_ENC)
        r += 1
        for i in range(n):
            poner(ws, f"A{r}", x[i], TEXTO, formato="0.0000000000")
            poner(ws, f"B{r}", w[i], TEXTO, formato="0.0000000000")
            r += 1
        r += 1

    # --- Demostración en vivo: Gauss n=2 sobre ∫ e^(−x²) dx en [-1,1] ---
    poner(ws, f"A{r}", "DEMOSTRACIÓN — Gauss-Legendre (n=2) sobre ∫ e^(−x²) dx en [-1, 1]", ENCABEZADO, RELLENO_ENC)
    r += 1
    for j, h in enumerate(["xᵢ (nodo en [-1,1])", "tᵢ (mapeado a [a,b])", "f(tᵢ) = e^(−tᵢ²)", "wᵢ", "wᵢ·f(tᵢ)"]):
        poner(ws, f"{get_column_letter(j+1)}{r}", h, ENCABEZADO, RELLENO_ENC)
    r += 1
    x2, w2 = leggauss(2)
    a, b = -1.0, 1.0
    inicio = r
    for xi, wi in zip(x2, w2):
        ti = 0.5 * (b - a) * xi + 0.5 * (a + b)
        poner(ws, f"A{r}", xi, TEXTO, formato="0.0000000000")
        poner(ws, f"B{r}", ti, TEXTO, formato="0.0000000000")
        poner(ws, f"C{r}", f"=EXP(-(B{r}^2))", TEXTO, formato="0.0000000000")
        poner(ws, f"D{r}", wi, TEXTO, formato="0.0000000000")
        poner(ws, f"E{r}", f"=C{r}*D{r}", TEXTO, formato="0.0000000000")
        r += 1
    fin = r - 1
    poner(ws, f"A{r}", "Gauss-Legendre (n=2) =", NEGRITA)
    poner(ws, f"C{r}", f"={0.5*(b-a)}*SUM(E{inicio}:E{fin})", NEGRITA, RELLENO_VERDE, formato="0.0000000000")
    poner(ws, f"D{r}", "(= (b−a)/2 · Σ wᵢf(tᵢ))", TEXTO)
    r += 2

    # --- Tabla de Romberg (valores) para ∫ e^(−x²) dx en [-1,1] ---
    poner(ws, f"A{r}", "TABLA DE ROMBERG — ∫ e^(−x²) dx en [-1, 1]  (m = 8 niveles)", ENCABEZADO, RELLENO_ENC)
    r += 1
    poner(ws, f"A{r}", "Nivel (trapecios)", ENCABEZADO, RELLENO_ENC)
    for j in range(8):
        poner(ws, f"{get_column_letter(j+2)}{r}", f"Extrap. {j}", ENCABEZADO, RELLENO_ENC)
    r += 1
    R = _tabla_romberg(lambda x: np.exp(-(x ** 2)), -1.0, 1.0, 8)
    for i in range(8):
        poner(ws, f"A{r}", f"h/2^{i}", TEXTO)
        for j in range(8):
            if j <= i:
                poner(ws, f"{get_column_letter(j+2)}{r}", R[i][j], TEXTO, formato="0.0000000000")
        r += 1
    poner(ws, f"A{r}", "Mejor aproximación (R88):", NEGRITA)
    poner(ws, f"B{r}", R[7][7], NEGRITA, RELLENO_VERDE, formato="0.0000000000")
    r += 1
    poner(ws, f"A{r}", "Nota: R[i,j] = R[i,j-1] + (R[i,j-1] − R[i-1,j-1]) / (4^j − 1)", TEXTO)
    r += 2

    # --- Resultados Gauss y Romberg para las 4 integrales 1D ---
    poner(ws, f"A{r}", "RESULTADOS 1D (Gauss-Legendre n=2,3,5 y Romberg)", ENCABEZADO, RELLENO_ENC)
    r += 1
    poner(ws, f"A{r}", "Método", ENCABEZADO, RELLENO_ENC)
    for j, (nombre, _f, _a, _b, _e) in enumerate(INTEGRALES_1D):
        poner(ws, f"{get_column_letter(j+2)}{r}", nombre, ENCABEZADO, RELLENO_ENC)
    r += 1
    filas = [i for i, (n, _m, _nn) in enumerate(METODOS) if n.startswith("Gauss") or n.startswith("Romberg")]
    for idx in filas:
        relleno = RELLENO_ALT if idx % 2 else None
        poner(ws, f"A{r}", METODOS[idx][0], TEXTO, relleno)
        for j in range(4):
            poner(ws, f"{get_column_letter(j+2)}{r}", RESULTADOS_1D[idx][j], TEXTO, relleno,
                  formato="0.0000000000")
        r += 1
    return ws


# ---------------------------------------------------------------------------
# 6. Hoja "Metodologia"
# ---------------------------------------------------------------------------

def hoja_metodologia(wb):
    ws = wb.create_sheet("Metodologia")
    ws.column_dimensions["A"].width = 110

    poner(ws, "A1", "METODOLOGÍA — DE LAS INTEGRALES 1D A LA INTEGRAL DOBLE", TITULO, RELLENO_TITULO)

    lineas = [
        "",
        "1) SEPARABILIDAD DE LOS INTEGRANDOS",
        "   Los tres integrandos son separables en x e y: f(x,y) = g(x)·h(y). Por eso la integral",
        "   doble sobre el rectángulo [xa,xb]×[ya,yb] se reduce al PRODUCTO de dos integrales 1D:",
        "",
        "     ∬ (1−x²)(1−y²) dx dy = ∫(1−x²)dx · ∫(1−y²)dy",
        "     ∬ x² y²       dx dy = ∫x²dx · ∫y²dy",
        "     ∬ e^(−(x²+y²)) dx dy = ∫e^(−x²)dx · ∫e^(−y²)dy",
        "",
        "2) INTEGRALES 1D NECESARIAS (calculadas con cada método en la hoja 'Metodos_1D')",
        "     ∫ (1−x²) dx en [-1,1] = 4/3          ∫ x² dx en [0,2] = 8/3",
        "     ∫ y² dy en [0,3] = 9                ∫ e^(−x²) dx en [-1,1] = √π·erf(1) ≈ 1.493648",
        "",
        "3) COMPROBACIÓN ANALÍTICA",
        "     I1 = (4/3)·(4/3) = 16/9",
        "     I2 = (8/3)·(9) = 24",
        "     I3 = (√π·erf(1))² = π·erf(1)² ≈ 2.230985   (= valor de referencia del enunciado)",
        "",
        "4) ¿POR QUÉ GAUSS-LEGENDRE ES EXACTO EN I1 E I2 PERO NO EN I3?",
        "     Una cuadratura de Gauss-Legendre de n puntos integra EXACTAMENTE cualquier polinomio",
        "     de grado ≤ 2n−1. En I1 e I2 los integrandos son polinomios de grado bajo (2 y 4),",
        "     por lo que n=2 y n=3 ya son exactos. En I3 el integrando e^(−(x²+y²)) NO es un",
        "     polinomio, así que Gauss-Legendre solo aproxima: con n=2,3,5 puntos da errores de",
        "     1.77e-1, 1.51e-2 y 4.68e-5 respectivamente. Ahí Romberg (m=8) alcanza error ~1e-15,",
        "     siendo el más eficiente.",
        "",
        "5) COMPARACIÓN DE EFICIENCIA (criterio: error absoluto)",
        "     Ver la tabla de la hoja 'Resumen'. Para integrandos polinomiales, Gauss-Legendre y",
        "     Romberg son los más eficientes; para la exponencial, Romberg supera a Gauss-Legendre",
        "     de pocos puntos. El trapecio es siempre el menos preciso (error O(h²)).",
    ]
    r = 3
    for ln in lineas:
        poner(ws, f"A{r}", ln, TEXTO)
        r += 1
    return ws


# ---------------------------------------------------------------------------
# 7. Programa principal
# ---------------------------------------------------------------------------

def main():
    wb = openpyxl.Workbook()
    hoja_resumen(wb)
    hoja_metodos_1d(wb)
    hoja_gauss_romberg(wb)
    hoja_metodologia(wb)

    salida = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Tema_A_Excel.xlsx")
    wb.save(salida)
    print(f"Excel generado: {salida}")


if __name__ == "__main__":
    main()
