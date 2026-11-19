# Proyecto-Análisis-Técnicas-Numéricas

Software de **resolución y análisis comparativo de integrales dobles** (Tema A) para
la asignatura *Análisis de Técnicas Numéricas* — Corporación Universitaria del
Caribe (CECAR).

## 📌 Descripción

El proyecto resuelve tres integrales dobles de forma **analítica** y **numérica**,
empleando todos los métodos vistos en clase, y compara la **eficiencia de cada
método** con base en su **error absoluto** y **relativo**.

| # | Integral | Límites | Valor exacto | Método más eficiente |
|---|----------|---------|--------------|----------------------|
| 1 | ∬ (1 − x² − y²) dx dy | −1 ≤ x ≤ 1, −1 ≤ y ≤ 1 | **4/3** | Gauss-Legendre (3 puntos) — error 0 |
| 2 | ∬ x² y² dx dy | 1 ≤ x ≤ 2, 1 ≤ y ≤ 3 | **182/9** | Romberg — error 0 |
| 3 | ∬ (x² + y²) dx dy | −1 ≤ x ≤ 1, −1 ≤ y ≤ 1 | **8/3** | Romberg — error 0 |

Incluye **cálculo manual**, **Excel** (con fórmulas vivas) y **software de
propósito general** (consola + interfaz gráfica + integral personalizada).

## 🧮 Métodos implementados

- **Trapecio compuesto**
- **Simpson 1/3 compuesta**
- **Simpson 3/8 compuesta**
- **Integración de Romberg**
- **Cuadratura de Gauss-Legendre** (orden 2, 3, 5 y variable)

Todos se aplican a la integral doble mediante **integración iterada** (primero en
`x`, luego en `y`), por lo que funcionan con cualquier `f(x, y)` sobre regiones
rectangulares.

## ⚙️ Requisitos

- Python 3.9+ (probado en 3.14)
- Dependencias: `numpy`, `matplotlib`, `openpyxl` (Tkinter viene con Python)

```powershell
cd tema_a
py -m pip install -r requirements.txt
```

## ▶️ Uso

```powershell
cd tema_a
py interfaz.py            # Interfaz gráfica (pestañas, gráficas, exportación)
py main.py                # Versión consola (tablas + gráficas por pantalla)
py main.py --solo-guardar # Solo guarda las PNG en ./graficas
py generar_excel.py       # Genera Tema_A_Excel.xlsx (con fórmulas vivas)
```

### Interfaz gráfica

- **Resultados** — tabla de resultados y errores por método + botón *Exportar a Excel*.
- **Gráficas** — barras (error por método), convergencia, **convergencia + R²**
  (ajuste log-log: orden de exactitud y coeficiente de determinación),
  comparación global y botón *Guardar gráfica (PNG)*.
- **Integral personalizada** — calcula cualquier `∬ f(x, y) dx dy` escrita por
  el usuario (ej.: `x**2 + y**2`, `sin(x)*cos(y)`).
- **Acerca de** — créditos y métodos.

## 📁 Estructura

```
.
├── Proyecto Final de Análisis de Técnicas Numéricas.pdf   # enunciado
├── README.md                                              # este archivo
├── informe/
│   └── Informe_Tema_A.tex     # informe LaTeX listo para Overleaf
└── tema_a/
    ├── interfaz.py         # GUI (Tkinter + Matplotlib)
    ├── main.py             # programa principal (consola)
    ├── metodos.py          # métodos numéricos (1D y 2D)
    ├── integrales.py       # definición de las integrales del Tema A
    ├── graficas.py         # generación de gráficas (PNG)
    ├── generar_excel.py    # genera el Excel con fórmulas
    ├── Tema_A_Excel.xlsx   # Excel generado
    ├── graficas/           # gráficas PNG generadas
    ├── requirements.txt    # dependencias
    └── README.md           # manual detallado del software
```

Documentación ampliada: [`tema_a/README.md`](tema_a/README.md).

## ℹ️ Autores

- **Asignatura:** Análisis de Técnicas Numéricas
- **Universidad:** Corporación Universitaria del Caribe (CECAR)
- **Facultad:** Ciencias Básicas, Ingeniería y Arquitectura
- **Docente:** Ing. Carlos Cohen M.
- **Autor:** Keiner Elías Beltrán Vergara

## ⚠️ Nota

Los límites de integración fueron interpretados de la imagen del enunciado.
El PDF menciona un valor de referencia de **2.230985** para el ejercicio de
Gauss-Legendre; si tus límites difieren, basta actualizar `exacto` en
`tema_a/integrales.py`.
