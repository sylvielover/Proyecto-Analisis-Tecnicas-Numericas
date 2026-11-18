# Proyecto Final — Tema A
## Análisis de Técnicas Numéricas

Software de resolución de integrales dobles (analítica y numérica) para el
**Tema A** del Proyecto Final.

---

## 📌 Enunciado (Tema A)

> Resuelva las siguientes integrales de forma analítica (matemática) y numérica,
> empleando todos los métodos vistos en clase. Realice los cálculos manualmente,
> en Excel y mediante software de propósito general; finalmente, compare la
> eficiencia de cada método con base en su error absoluto.

### Integrales

| # | Integral | Límites | Valor exacto |
|---|----------|---------|--------------|
| 1 | ∬ (1 − x² − y²) dx dy | −1 ≤ x ≤ 1, −1 ≤ y ≤ 1 | 4/3 |
| 2 | ∬ x² y² dx dy | 1 ≤ x ≤ 2, 1 ≤ y ≤ 3 | 182/9 |
| 3 | ∬ (x² + y²) dx dy | −1 ≤ x ≤ 1, −1 ≤ y ≤ 1 | 8/3 |

> ⚠️ Los límites fueron interpretados de la imagen del enunciado; verifícalos
> en tu PDF. El enunciado menciona además un valor de referencia "exacto" de
> **2.230985** para el ejercicio de Gauss-Legendre de orden dos y tres.

---

## 🧮 Métodos implementados

- **Trapecio compuesto**
- **Simpson 1/3 compuesta**
- **Simpson 3/8 compuesta**
- **Integración de Romberg**
- **Cuadratura de Gauss-Legendre** (orden 2, 3, 5 y variable)

Todos se aplican a la **integral doble** mediante integración iterada
(primero en `x`, luego en `y`), de modo que también funcionan como un
"software de propósito general" para cualquier `f(x, y)` y cualquier región
rectangular.

---

## ⚙️ Requisitos e instalación

1. Tener **Python 3.9+** instalado (descarga en https://www.python.org/).
2. Instalar las dependencias:

   ```powershell
   py -m pip install -r requirements.txt
   ```

   (equivale a `pip install numpy matplotlib`)

---

## ▶️ Uso

Desde la carpeta `tema_a`:

```powershell
py interfaz.py            # INTERFAZ GRÁFICA (ventana con pestañas y gráficas)
py main.py                # versión de consola: tablas + gráficas por pantalla
py main.py --solo-guardar # versión de consola: solo guarda las PNG en ./graficas
py generar_excel.py       # genera el archivo Tema_A_Excel.xlsx
```

### Interfaz gráfica (`py interfaz.py`)

La aplicación abre una ventana con 4 pestañas:

- **Resultados**: tabla por integral con el resultado de cada método, su error
  absoluto y relativo, y el método más eficiente. Incluye botón
  **"Exportar a Excel"** (genera `resultados_TemaA.xlsx`).
- **Gráficas**: botones para generar (embebidas en la ventana) las gráficas de
  barras, de convergencia, **convergencia + R²** (ajuste log-log con el orden
  de exactitud) y la comparación global. Incluye botón **"Guardar gráfica (PNG)"**.
- **Integral personalizada**: calcula cualquier `∬ f(x, y) dx dy` que escribas
  (software de propósito general). Ej.: `x**2 + y**2`, `sin(x)*cos(y)`, etc.
- **Acerca de**: créditos y métodos implementados.

**Salida que genera el programa:**

- Tabla por integral con el resultado de cada método, su **error absoluto** y
  **error relativo** frente al valor exacto (analítico).
- Indicación del **método más eficiente** por integral.
- Gráficas (guardadas en `./graficas/`):
  - `barras_integral_N.png` — error absoluto por método (escala log).
  - `convergencia_integral_N.png` — error vs. número de puntos/subintervalos.
  - `comparacion_global.png` — comparación de todos los métodos y todas las integrales.

---

## 📁 Estructura

```
tema_a/
├── interfaz.py         # interfaz gráfica (Tkinter + Matplotlib)
├── main.py             # programa principal (consola)
├── metodos.py          # métodos numéricos (1D y 2D)
├── integrales.py       # definición de las integrales del Tema A
├── graficas.py         # generación de gráficas (PNG)
├── generar_excel.py    # genera el Excel con los cálculos
├── Tema_A_Excel.xlsx   # Excel generado
├── graficas/           # gráficas PNG generadas
├── requirements.txt    # dependencias
└── README.md           # este manual
```

---

## ℹ️ Acerca de

- **Asignatura:** Análisis de Técnicas Numéricas
- **Proyecto:** Proyecto Final — Tema A
- **Universidad:** Corporación Universitaria del Caribe (CECAR)
- **Facultad:** Ciencias Básicas, Ingeniería y Arquitectura
- **Docente:** Ing. Carlos Cohen M.
- **Autores:** *(completar con los nombres del grupo)*

---

## 📝 Notas para el informe (Overleaf)

- Incluir la **identificación** del grupo.
- Describir cada método usado.
- Explicar la **metodología** (integración iterada para integrales dobles).
- Mostrar las tablas de errores y las gráficas generadas.
- Redactar **conclusiones** (¿qué método converge más rápido? ¿por qué
  Gauss-Legendre es exacto para polinomios de bajo grado?).
- Añadir **recomendaciones** y **referencias bibliográficas**.

### ¿Por qué Gauss-Legendre es "exacto" en estos casos?

Los tres integrandos son polinomios de grado bajo:

- `1 − x² − y²`: grado 2 en cada variable.
- `x² y²`: grado 4.
- `x² + y²`: grado 2.

Una cuadratura de Gauss-Legendre de `n` puntos integra *exactamente* cualquier
polinomio de grado ≤ `2n − 1`. Por eso, con 2 puntos (grado ≤ 3) la integral 1
y 3 ya salen exactas, y con 3 puntos (grado ≤ 5) la integral 2 sale exacta.
Este es un punto clave para justificar la **eficiencia** en las conclusiones.
