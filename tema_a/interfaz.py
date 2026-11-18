"""
interfaz.py
===========
Interfaz gráfica (Tkinter + Matplotlib) del software del Tema A.

Incluye:
    - Pestaña "Resultados": tablas de resultados y errores por integral.
    - Pestaña "Gráficas": gráficas comparativas y de convergencia (embebidas).
    - Pestaña "Integral personalizada": cálculo de cualquier ∬ f(x,y) dx dy
      (software de propósito general).
    - Pestaña "Acerca de": créditos (autores, asignatura, universidad).

Uso:
    py interfaz.py
"""

import os
import tkinter as tk
from tkinter import ttk, messagebox

import numpy as np
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from metodos import (trapecio, simpson13, simpson38, romberg, gauss_legendre,
                     integral_doble)
from integrales import INTEGRALES


# Métodos disponibles (nombre, función 1D, n por defecto)
METODOS = [
    ("Trapecio", trapecio, 100),
    ("Simpson 1/3", simpson13, 100),
    ("Simpson 3/8", simpson38, 99),
    ("Romberg", romberg, 8),
    ("Gauss-Legendre (2 ptos)", gauss_legendre, 2),
    ("Gauss-Legendre (3 ptos)", gauss_legendre, 3),
    ("Gauss-Legendre (5 ptos)", gauss_legendre, 5),
]

COLORES = {
    "Trapecio": "#1f77b4",
    "Simpson 1/3": "#2ca02c",
    "Simpson 3/8": "#ff7f0e",
    "Romberg": "#9467bd",
    "Gauss-Legendre": "#d62728",
}


def _color_de(nombre):
    for clave, color in COLORES.items():
        if nombre.startswith(clave):
            return color
    return "#888888"


class Aplicacion(tk.Tk):
    """Ventana principal de la aplicación."""

    def __init__(self):
        super().__init__()
        self.title("Proyecto Final — Tema A · Análisis de Técnicas Numéricas")
        self.geometry("1080x720")
        self.minsize(900, 600)

        self.tablas = {}           # nombre_integral -> ttk.Treeview
        self.etiquetas_mejor = {}  # nombre_integral -> ttk.Label
        self.datos_resultados = {}  # nombre_integral -> [(metodo, valor, err, rel)]
        self.canvas = None
        self.fig = None

        self._construir()
        self._calcular_todo()

    # ------------------------------------------------------------------
    # Construcción de la interfaz
    # ------------------------------------------------------------------
    def _construir(self):
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=6, pady=6)

        self.tab_resultados = ttk.Frame(self.notebook)
        self.tab_graficas = ttk.Frame(self.notebook)
        self.tab_custom = ttk.Frame(self.notebook)
        self.tab_acerca = ttk.Frame(self.notebook)

        self.notebook.add(self.tab_resultados, text="  Resultados  ")
        self.notebook.add(self.tab_graficas, text="  Gráficas  ")
        self.notebook.add(self.tab_custom, text="  Integral personalizada  ")
        self.notebook.add(self.tab_acerca, text="  Acerca de  ")

        self._construir_resultados()
        self._construir_graficas()
        self._construir_custom()
        self._construir_acerca()

    def _construir_resultados(self):
        ttk.Label(self.tab_resultados,
                  text="Resolución de las integrales dobles (analítica y numérica)\n"
                       "Resultados de cada método, error absoluto y error relativo.",
                  justify="center").pack(pady=(8, 4))

        fila_botones = ttk.Frame(self.tab_resultados)
        fila_botones.pack(pady=(0, 8))
        ttk.Button(fila_botones, text="⟳ Recalcular todo",
                   command=self._calcular_todo).pack(side="left", padx=4)
        ttk.Button(fila_botones, text="⤓ Exportar a Excel",
                   command=self._exportar_resultados).pack(side="left", padx=4)

        contenedor = ttk.Frame(self.tab_resultados)
        contenedor.pack(fill="both", expand=True, padx=8, pady=4)

        for integ in INTEGRALES:
            marco = ttk.LabelFrame(contenedor, text=f"{integ['nombre']}:  {integ['formula']}")
            marco.pack(fill="x", pady=4)

            ttk.Label(marco, text=f"Valor exacto (analítico) = {integ['exacto']:.10f}").pack(
                anchor="w", padx=6, pady=(2, 0))

            columnas = ("metodo", "resultado", "error", "rel")
            tabla = ttk.Treeview(marco, columns=columnas, show="headings", height=7)
            tabla.heading("metodo", text="Método")
            tabla.heading("resultado", text="Resultado")
            tabla.heading("error", text="Error absoluto")
            tabla.heading("rel", text="Error relativo")
            tabla.column("metodo", width=200, anchor="w")
            tabla.column("resultado", width=180, anchor="e")
            tabla.column("error", width=160, anchor="e")
            tabla.column("rel", width=140, anchor="e")
            tabla.pack(fill="x", padx=6, pady=2)
            self.tablas[integ["nombre"]] = tabla

            etiqueta = ttk.Label(marco, text="", foreground="#1a7a1a")
            etiqueta.pack(anchor="w", padx=6, pady=(0, 4))
            self.etiquetas_mejor[integ["nombre"]] = etiqueta

    def _construir_graficas(self):
        marco_botones = ttk.Frame(self.tab_graficas)
        marco_botones.pack(fill="x", padx=8, pady=6)

        for integ in INTEGRALES:
            ttk.Button(marco_botones, text=f"Barras · {integ['nombre']}",
                       command=lambda i=integ: self._mostrar_barras(i)).pack(side="left", padx=3)
            ttk.Button(marco_botones, text=f"Convergencia · {integ['nombre']}",
                       command=lambda i=integ: self._mostrar_convergencia(i)).pack(side="left", padx=3)

        ttk.Button(marco_botones, text="Comparación global",
                   command=self._mostrar_global).pack(side="left", padx=(12, 3))

        # Fila adicional: convergencia con R² y exportar gráfica
        marco_botones2 = ttk.Frame(self.tab_graficas)
        marco_botones2.pack(fill="x", padx=8, pady=(0, 6))
        for integ in INTEGRALES:
            ttk.Button(marco_botones2, text=f"Convergencia + R² · {integ['nombre']}",
                       command=lambda i=integ: self._mostrar_convergencia_r2(i)).pack(
                side="left", padx=3)
        ttk.Button(marco_botones2, text="💾 Guardar gráfica (PNG)",
                   command=self._exportar_grafica).pack(side="left", padx=(12, 3))

        self.contenedor_grafica = ttk.Frame(self.tab_graficas)
        self.contenedor_grafica.pack(fill="both", expand=True, padx=8, pady=4)

        ttk.Label(self.tab_graficas,
                  text="Haz clic en un botón para generar la gráfica correspondiente.").pack(
            side="bottom", pady=4)

    def _construir_custom(self):
        ttk.Label(self.tab_custom,
                  text="Integral personalizada  ∬ f(x, y) dx dy  (propósito general)",
                  font=("Segoe UI", 11, "bold")).pack(pady=(10, 4))

        ttk.Label(self.tab_custom,
                  text="Escribe f(x,y) usando x, y y funciones: sin, cos, exp, log, sqrt, pi, abs.\n"
                       "Ejemplo:  x**2 + y**2",
                  justify="center").pack(pady=(0, 6))

        self.var_f = tk.StringVar(value="x**2 + y**2")
        self.var_xa = tk.StringVar(value="-1")
        self.var_xb = tk.StringVar(value="1")
        self.var_ya = tk.StringVar(value="-1")
        self.var_yb = tk.StringVar(value="1")
        self.var_metodo = tk.StringVar(value="Simpson 1/3")
        self.var_n = tk.StringVar(value="100")

        ttk.Label(self.tab_custom, text="f(x, y) =").pack()
        ttk.Entry(self.tab_custom, textvariable=self.var_f, width=44).pack(pady=2)

        fila_limites = ttk.Frame(self.tab_custom)
        fila_limites.pack(pady=4)
        for texto, var in [("xa", self.var_xa), ("xb", self.var_xb),
                           ("ya", self.var_ya), ("yb", self.var_yb)]:
            ttk.Label(fila_limites, text=texto + "=").pack(side="left", padx=(6, 1))
            ttk.Entry(fila_limites, textvariable=var, width=7).pack(side="left")

        fila_metodo = ttk.Frame(self.tab_custom)
        fila_metodo.pack(pady=4)
        ttk.Label(fila_metodo, text="Método:").pack(side="left", padx=(0, 4))
        combo = ttk.Combobox(fila_metodo, textvariable=self.var_metodo, state="readonly",
                             values=[m[0] for m in METODOS], width=22)
        combo.pack(side="left")
        ttk.Label(fila_metodo, text="   n:").pack(side="left", padx=(10, 4))
        ttk.Entry(fila_metodo, textvariable=self.var_n, width=8).pack(side="left")

        ttk.Button(self.tab_custom, text="Calcular integral",
                   command=self._calcular_custom).pack(pady=8)

        self.etiqueta_custom = ttk.Label(self.tab_custom, text="", font=("Segoe UI", 10))
        self.etiqueta_custom.pack(pady=6)

    def _construir_acerca(self):
        texto = (
            "\n\nPROYECTO FINAL — ANÁLISIS DE TÉCNICAS NUMÉRICAS\n"
            "Tema A: Resolución de integrales dobles (analítica y numérica)\n\n"
            "Métodos implementados:\n"
            "  • Regla del Trapecio compuesta\n"
            "  • Simpson 1/3 compuesta\n"
            "  • Simpson 3/8 compuesta\n"
            "  • Integración de Romberg\n"
            "  • Cuadratura de Gauss-Legendre (orden 2, 3 y 5)\n\n"
            "Asignatura:  Análisis de Técnicas Numéricas\n"
            "Universidad: Corporación Universitaria del Caribe (CECAR)\n"
            "Facultad:    Ciencias Básicas, Ingeniería y Arquitectura\n"
            "Docente:     Ing. Carlos Cohen M.\n\n"
            "Autores:     (completar con los nombres del grupo)\n\n"
            "Nota: verifica los límites de las integrales en el enunciado original;\n"
            "el docente menciona un valor de referencia \"exacto\" de 2.230985 para\n"
            "el ejercicio de Gauss-Legendre de orden dos y tres."
        )
        tk.Label(self.tab_acerca, text=texto, justify="left", font=("Segoe UI", 10)).pack(
            padx=20, pady=10, anchor="w")

    # ------------------------------------------------------------------
    # Cálculo de las integrales del Tema A
    # ------------------------------------------------------------------
    def _calcular_todo(self):
        for integ in INTEGRALES:
            resultados = []
            for nombre, metodo, n in METODOS:
                valor = integral_doble(integ["f"], integ["xa"], integ["xb"],
                                       integ["ya"], integ["yb"], metodo, n)
                err = abs(valor - integ["exacto"])
                rel = err / abs(integ["exacto"])
                resultados.append((nombre, valor, err, rel))

            self.datos_resultados[integ["nombre"]] = resultados

            tabla = self.tablas[integ["nombre"]]
            for fila in tabla.get_children():
                tabla.delete(fila)
            for nombre, valor, err, rel in resultados:
                tabla.insert("", "end", values=(nombre, f"{valor:.10f}",
                                                f"{err:.4e}", f"{rel:.3e}"))

            mejor = min(resultados, key=lambda r: r[2])
            self.etiquetas_mejor[integ["nombre"]].config(
                text=f"✓ Método más eficiente: {mejor[0]}  (error = {mejor[2]:.4e})")

    # ------------------------------------------------------------------
    # Gráficas
    # ------------------------------------------------------------------
    def _dibujar_figura(self, fig):
        if self.canvas is not None:
            self.canvas.get_tk_widget().destroy()
        self.canvas = FigureCanvasTkAgg(fig, master=self.contenedor_grafica)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill="both", expand=True)
        self.fig = fig

    def _mostrar_barras(self, integ):
        fig = Figure(figsize=(8, 4.6), dpi=100)
        ax = fig.add_subplot(111)
        nombres = [m[0] for m in METODOS]
        errores = []
        for nombre, metodo, n in METODOS:
            v = integral_doble(integ["f"], integ["xa"], integ["xb"],
                               integ["ya"], integ["yb"], metodo, n)
            errores.append(max(abs(v - integ["exacto"]), 1e-16))
        ax.bar(nombres, errores, color=[_color_de(n) for n in nombres])
        ax.set_yscale("log")
        ax.set_ylabel("Error absoluto (escala log)")
        ax.set_title(f"{integ['nombre']}: error absoluto por método\n{integ['formula']}", fontsize=9)
        ax.tick_params(axis="x", labelsize=7, rotation=25)
        ax.grid(axis="y", which="both", linestyle="--", alpha=0.5)
        fig.tight_layout()
        self._dibujar_figura(fig)

    def _mostrar_convergencia(self, integ):
        fig = Figure(figsize=(8, 4.6), dpi=100)
        ax = fig.add_subplot(111)
        f = integ["f"]
        xa, xb, ya, yb = integ["xa"], integ["xb"], integ["ya"], integ["yb"]
        exacto = integ["exacto"]
        ns = [4, 8, 16, 32, 64, 128]
        for nombre, metodo, _ in METODOS:
            if nombre in ("Trapecio", "Simpson 1/3"):
                errs = [abs(integral_doble(f, xa, xb, ya, yb, metodo, n) - exacto) for n in ns]
                ax.plot(ns, errs, "o-", label=nombre, color=_color_de(nombre))
        gns = [2, 3, 4, 5, 6, 7]
        gerrs = [abs(integral_doble(f, xa, xb, ya, yb, gauss_legendre, n) - exacto) for n in gns]
        ax.plot(gns, gerrs, "^-", label="Gauss-Legendre", color=_color_de("Gauss-Legendre"))
        ax.set_yscale("log")
        ax.set_xlabel("n (subintervalos o puntos)")
        ax.set_ylabel("Error absoluto (escala log)")
        ax.set_title(f"{integ['nombre']}: convergencia\n{integ['formula']}", fontsize=9)
        ax.grid(True, which="both", linestyle="--", alpha=0.5)
        ax.legend(fontsize=8)
        fig.tight_layout()
        self._dibujar_figura(fig)

    def _mostrar_global(self):
        fig = Figure(figsize=(8, 4.6), dpi=100)
        ax = fig.add_subplot(111)
        x = np.arange(len(INTEGRALES))
        ancho = 0.8 / len(METODOS)
        for i, (nombre, metodo, n) in enumerate(METODOS):
            errores = []
            for integ in INTEGRALES:
                v = integral_doble(integ["f"], integ["xa"], integ["xb"],
                                   integ["ya"], integ["yb"], metodo, n)
                errores.append(max(abs(v - integ["exacto"]), 1e-16))
            ax.bar(x + (i - len(METODOS) / 2) * ancho, errores, ancho,
                   label=nombre, color=_color_de(nombre))
        ax.set_yscale("log")
        ax.set_xticks(x)
        ax.set_xticklabels([integ["nombre"] for integ in INTEGRALES])
        ax.set_ylabel("Error absoluto (escala log)")
        ax.set_title("Comparación global de errores por método e integral")
        ax.grid(axis="y", which="both", linestyle="--", alpha=0.5)
        ax.legend(ncol=2, fontsize=7)
        fig.tight_layout()
        self._dibujar_figura(fig)

    # ------------------------------------------------------------------
    # Integral personalizada
    # ------------------------------------------------------------------
    def _calcular_custom(self):
        try:
            expr = self.var_f.get().strip()
            xa = float(self.var_xa.get())
            xb = float(self.var_xb.get())
            ya = float(self.var_ya.get())
            yb = float(self.var_yb.get())
            n = int(float(self.var_n.get()))
            nombre_metodo = self.var_metodo.get()
        except ValueError:
            messagebox.showerror("Error", "Revisa los límites y el valor de n (deben ser números).")
            return

        metodo = next((m[1] for m in METODOS if m[0] == nombre_metodo), simpson13)

        entorno = {"__builtins__": {}}
        entorno.update({
            "sin": np.sin, "cos": np.cos, "tan": np.tan,
            "exp": np.exp, "log": np.log, "sqrt": np.sqrt,
            "abs": np.abs, "pi": np.pi, "e": np.e, "np": np,
        })
        try:
            f = eval(f"lambda x, y: ({expr})", entorno, {})
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo interpretar f(x,y):\n{e}")
            return

        try:
            valor = integral_doble(f, xa, xb, ya, yb, metodo, n)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo calcular la integral:\n{e}")
            return

        self.etiqueta_custom.config(
            text=f"∬ f(x,y) dx dy ≈ {valor:.10f}\n"
                 f"(método: {nombre_metodo}, n = {n})")

    # ------------------------------------------------------------------
    # Convergencia con ajuste (R²) y exportación
    # ------------------------------------------------------------------
    def _mostrar_convergencia_r2(self, integ):
        """Gráfica log-log del error vs. n con ajuste lineal, mostrando el
        orden de convergencia y el coeficiente R² del ajuste."""
        fig = Figure(figsize=(8, 4.6), dpi=100)
        ax = fig.add_subplot(111)
        f = integ["f"]
        xa, xb, ya, yb = integ["xa"], integ["xb"], integ["ya"], integ["yb"]
        exacto = integ["exacto"]
        ns = [4, 8, 16, 32, 64, 128]

        for nombre, metodo, _ in METODOS:
            if nombre not in ("Trapecio", "Simpson 1/3", "Simpson 3/8"):
                continue
            errs = [max(abs(integral_doble(f, xa, xb, ya, yb, metodo, n) - exacto), 1e-16)
                    for n in ns]
            logn = np.log10(ns)
            loge = np.log10(errs)

            # Si el error ya está a nivel de precisión de máquina, no hay
            # tendencia polinomial que ajustar (el método es "exacto").
            if max(errs) < 1e-14:
                ax.plot(logn, loge, "o", color=_color_de(nombre))
                ax.plot(logn, loge, "--", color=_color_de(nombre),
                        label=f"{nombre}: exacto (error ~1e-15, precisión de máquina)")
                continue

            coef = np.polyfit(logn, loge, 1)
            pred = coef[0] * logn + coef[1]
            ss_res = float(np.sum((loge - pred) ** 2))
            ss_tot = float(np.sum((loge - loge.mean()) ** 2))
            r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else 1.0
            orden = -coef[0]
            ax.plot(logn, loge, "o", color=_color_de(nombre))
            ax.plot(logn, pred, "--", color=_color_de(nombre),
                    label=f"{nombre}: orden ≈ {orden:.2f}, R² = {r2:.4f}")

        ax.set_xlabel("log10(n)")
        ax.set_ylabel("log10(error absoluto)")
        ax.set_title(f"{integ['nombre']}: convergencia y ajuste (R²)\n{integ['formula']}",
                     fontsize=9)
        ax.grid(True, which="both", linestyle="--", alpha=0.5)
        ax.legend(fontsize=8)
        fig.tight_layout()
        self._dibujar_figura(fig)

    def _exportar_grafica(self):
        if self.fig is None:
            messagebox.showwarning("Sin gráfica", "Primero genera una gráfica.")
            return
        import datetime
        nombre = "grafica_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S") + ".png"
        ruta = os.path.join(os.path.dirname(os.path.abspath(__file__)), nombre)
        self.fig.savefig(ruta, dpi=150)
        messagebox.showinfo("Exportado", f"Gráfica guardada en:\n{ruta}")

    def _exportar_resultados(self):
        ruta = os.path.join(os.path.dirname(os.path.abspath(__file__)), "resultados_TemaA.xlsx")
        try:
            import openpyxl
            wb = openpyxl.Workbook()
            ws = wb.active
            ws.title = "Resultados"
            ws.append(["Integral", "Método", "Resultado", "Error absoluto",
                       "Error relativo", "Valor exacto"])
            for integ in INTEGRALES:
                nombre = integ["nombre"]
                for metodo, valor, err, rel in self.datos_resultados.get(nombre, []):
                    ws.append([nombre, metodo, valor, err, rel, integ["exacto"]])
            wb.save(ruta)
        except ImportError:
            import csv
            ruta = os.path.splitext(ruta)[0] + ".csv"
            with open(ruta, "w", newline="", encoding="utf-8-sig") as fh:
                w = csv.writer(fh)
                w.writerow(["Integral", "Método", "Resultado", "Error absoluto",
                            "Error relativo", "Valor exacto"])
                for integ in INTEGRALES:
                    for metodo, valor, err, rel in self.datos_resultados.get(integ["nombre"], []):
                        w.writerow([integ["nombre"], metodo, valor, err, rel, integ["exacto"]])
        messagebox.showinfo("Exportado", f"Resultados guardados en:\n{ruta}")


def main():
    app = Aplicacion()
    app.mainloop()


if __name__ == "__main__":
    main()


