"""
PROBLEMA DUAL DE LA BIBLIOTECA UNIVERSITARIA
Verificación del teorema de dualidad fuerte
"""

import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import linprog

class DualApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Análisis de Dualidad - Biblioteca")
        self.root.geometry("900x700")
        self.root.configure(bg='#ecf0f1')
        
        self.resultado_dual = None
        self.create_widgets()
        
    def create_widgets(self):
        # Título
        titulo = tk.Label(self.root, text=" ANÁLISIS DE DUALIDAD FUERTE", 
                         font=("Arial", 20, "bold"), bg='#ecf0f1', fg='#2c3e50')
        titulo.pack(pady=20)
        
        # Marco de explicación
        expl_frame = tk.Frame(self.root, bg='white', relief=tk.RAISED, bd=2)
        expl_frame.pack(pady=10, padx=20, fill='x')
        
        explicacion = """
         TEOREMA DE DUALIDAD FUERTE:
        
        El problema dual proporciona una cota superior para el problema primal.
        En optimalidad, los valores de las funciones objetivo son iguales.
        
        PRIMAL (Original):      DUAL (Transformado):
        Minimizar c^T x         Maximizar b^T y
        Sujeto a: Ax ≥ b        Sujeto a: A^T y ≤ c
                  x ≥ 0                    y ≥ 0
        """
        
        expl_label = tk.Label(expl_frame, text=explicacion, font=("Courier", 10), 
                             bg='white', justify=tk.LEFT)
        expl_label.pack(pady=10, padx=10)
        
        # Botón resolver
        btn_resolver = tk.Button(self.root, text="🔬 RESOLVER PROBLEMA DUAL", 
                                command=self.resolver_dual,
                                font=("Arial", 14, "bold"), bg='#9b59b6', fg='white',
                                padx=20, pady=10)
        btn_resolver.pack(pady=20)
        
        # Frame resultados
        self.result_frame = tk.Frame(self.root, bg='white', relief=tk.RAISED, bd=2)
        self.result_frame.pack(pady=10, padx=20, fill='both', expand=True)
        
        self.result_text = tk.Text(self.result_frame, height=20, width=80, 
                                   font=("Courier", 10), bg='white')
        self.result_text.pack(pady=10, padx=10, fill='both', expand=True)
    
    def resolver_dual(self):
        # Configuración del dual
        c_dual = [-3, -2, -10, -14, -8, -10]
        
        A_dual = [
            [1, 1, 0, 0, 0, 0],
            [0, 1, 1, 0, 0, 0],
            [0, 0, 1, 1, 0, 0],
            [0, 0, 0, 1, 1, 0],
            [0, 0, 0, 0, 1, 1],
            [1, 0, 0, 0, 0, 1]
        ]
        
        b_dual = [1, 1, 1, 1, 1, 1]
        bounds_dual = [(0, None) for _ in range(6)]
        
        result_dual = linprog(c_dual, A_ub=A_dual, b_ub=b_dual, 
                             bounds=bounds_dual, method='highs')
        
        if result_dual.success:
            self.resultado_dual = result_dual
            self.mostrar_resultados()
            self.graficar_dualidad()
        else:
            messagebox.showerror("Error", "No se encontró solución óptima para el dual")
    
    def mostrar_resultados(self):
        self.result_text.delete(1.0, tk.END)
        
        # Título
        self.result_text.insert(tk.END, "="*80 + "\n")
        self.result_text.insert(tk.END, " SOLUCIÓN DEL PROBLEMA DUAL\n")
        self.result_text.insert(tk.END, "="*80 + "\n\n")
        
        # Variables duales
        self.result_text.insert(tk.END, " VARIABLES DUALES (Precios sombra):\n")
        self.result_text.insert(tk.END, "-"*50 + "\n")
        
        periodos = [
            "Período 1 (12-4 AM)", "Período 2 (4-8 AM)", "Período 3 (8-12 PM)",
            "Período 4 (12-4 PM)", "Período 5 (4-8 PM)", "Período 6 (8-12 PM)"
        ]
        
        for i, (periodo, val) in enumerate(zip(periodos, self.resultado_dual.x)):
            self.result_text.insert(tk.END, f"  y{i+1} ({periodo:20s}): {val:.4f}\n")
        
        # Valor óptimo
        valor_dual = -self.resultado_dual.fun
        self.result_text.insert(tk.END, "\n" + "="*50 + "\n")
        self.result_text.insert(tk.END, f" VALOR ÓPTIMO DEL DUAL: {valor_dual:.2f}\n")
        self.result_text.insert(tk.END, "="*50 + "\n\n")
        
        # Verificación del teorema
        self.result_text.insert(tk.END, " VERIFICACIÓN DEL TEOREMA DE DUALIDAD:\n")
        self.result_text.insert(tk.END, "-"*50 + "\n")
        self.result_text.insert(tk.END, "Valor óptimo del PRIMAL (bibliotecarios): 26.00\n")
        self.result_text.insert(tk.END, f"Valor óptimo del DUAL: {valor_dual:.2f}\n\n")
        
        if abs(26 - valor_dual) < 0.001:
            self.result_text.insert(tk.END, " ¡LOS VALORES COINCIDEN! Dualidad fuerte verificada.\n")
            self.result_text.insert(tk.END, "Esto confirma que la solución es óptima global.\n")
        else:
            self.result_text.insert(tk.END, " Los valores no coinciden. Revisar formulación.\n")
        
        # Interpretación económica
        self.result_text.insert(tk.END, "\n" + "="*80 + "\n")
        self.result_text.insert(tk.END, " INTERPRETACIÓN ECONÓMICA:\n")
        self.result_text.insert(tk.END, "="*80 + "\n")
        self.result_text.insert(tk.END, "Las variables duales representan el valor marginal\n")
        self.result_text.insert(tk.END, "de relajar cada restricción (precio sombra).\n\n")
        
        for i, val in enumerate(self.resultado_dual.x):
            if val > 0:
                self.result_text.insert(tk.END, f"  • Período {i+1}: Aumentar la demanda en 1 unidad\n")
                self.result_text.insert(tk.END, f"    incrementaría el costo en {val:.1f} bibliotecarios.\n\n")
    
    def graficar_dualidad(self):
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
        fig.suptitle('Análisis de Dualidad - Biblioteca Universitaria', 
                    fontsize=16, fontweight='bold')
        
        # Gráfico 1: Variables duales (precios sombra)
        periodos = ['P1\n(0-4h)', 'P2\n(4-8h)', 'P3\n(8-12h)', 
                   'P4\n(12-16h)', 'P5\n(16-20h)', 'P6\n(20-24h)']
        valores_dual = self.resultado_dual.x
        
        ax1.bar(periodos, valores_dual, color='#9b59b6', edgecolor='black', linewidth=1.5)
        ax1.set_xlabel('Período de 4 horas', fontsize=12)
        ax1.set_ylabel('Precio sombra', fontsize=12)
        ax1.set_title('Variables Duales (Precios Sombra)', fontsize=14, fontweight='bold')
        ax1.grid(True, alpha=0.3, axis='y')
        
        # Gráfico 2: Comparación primal vs dual
        valores_primal = [26]  # Valor óptimo primal
        valores_dual_opt = [-self.resultado_dual.fun]
        
        x = np.arange(2)
        width = 0.6
        
        bars = ax2.bar(x, [valores_primal[0], valores_dual_opt[0]], width, 
                      color=['#2ecc71', '#e74c3c'], edgecolor='black', linewidth=1.5)
        ax2.set_xticks(x)
        ax2.set_xticklabels(['Primal\n(Bibliotecarios)', 'Dual\n(Precios sombra)'])
        ax2.set_ylabel('Valor óptimo', fontsize=12)
        ax2.set_title('Comparación Primal vs Dual', fontsize=14, fontweight='bold')
        ax2.grid(True, alpha=0.3, axis='y')
        
        # Agregar valores
        for bar, val in zip(bars, [valores_primal[0], valores_dual_opt[0]]):
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                    f'{val:.2f}', ha='center', va='bottom', fontweight='bold', fontsize=12)
        
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    root = tk.Tk()
    app = DualApp(root)
    root.mainloop()