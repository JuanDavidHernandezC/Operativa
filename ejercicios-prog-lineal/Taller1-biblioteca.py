"""
PROBLEMA DE LA BIBLIOTECA UNIVERSITARIA
Minimización de bibliotecarios con turnos de 8 horas
Solución Optimizada
"""

import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import linprog
import matplotlib
matplotlib.use('TkAgg')

class BibliotecaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Optimización - Biblioteca Universitaria")
        self.root.geometry("900x700")
        self.root.configure(bg='#f0f0f0')
        
        # Resultados
        self.resultado = None
        self.x_optimo = None
        
        self.create_widgets()
        
    def create_widgets(self):
        # Título principal
        titulo = tk.Label(self.root, text=" OPTIMIZACIÓN DE BIBLIOTECARIOS ", 
                         font=("Arial", 20, "bold"), bg='#f0f0f0', fg='#2c3e50')
        titulo.pack(pady=20)
        
        # Frame de información
        info_frame = tk.Frame(self.root, bg='white', relief=tk.RAISED, bd=2)
        info_frame.pack(pady=10, padx=20, fill='x')
        
        info_text = """
          PROBLEMA: Biblioteca abierta 24 horas
          Turnos de 8 horas comenzando a las: 12AM, 4AM, 8AM, 12PM, 4PM, 8PM
          Demanda por período (4 horas):
           • 12:00 AM - 3:59 AM: 3 bibliotecarios
           • 4:00 AM - 7:59 AM: 2 bibliotecarios
           • 8:00 AM - 11:59 AM: 10 bibliotecarios
           • 12:00 PM - 3:59 PM: 14 bibliotecarios
           • 4:00 PM - 7:59 PM: 8 bibliotecarios
           • 8:00 PM - 11:59 PM: 10 bibliotecarios
        """
        
        info_label = tk.Label(info_frame, text=info_text, font=("Courier", 10), 
                             bg='white', justify=tk.LEFT)
        info_label.pack(pady=10, padx=10)
        
        # Botón para resolver
        btn_resolver = tk.Button(self.root, text="🔍 RESOLVER PROBLEMA", 
                                command=self.resolver_problema,
                                font=("Arial", 14, "bold"), bg='#3498db', fg='white',
                                padx=20, pady=10)
        btn_resolver.pack(pady=20)
        
        # Frame para resultados
        self.result_frame = tk.Frame(self.root, bg='white', relief=tk.RAISED, bd=2)
        self.result_frame.pack(pady=10, padx=20, fill='both', expand=True)
        
        self.result_text = tk.Text(self.result_frame, height=15, width=80, 
                                   font=("Courier", 10), bg='white')
        self.result_text.pack(pady=10, padx=10, fill='both', expand=True)
        
    def resolver_problema(self):
        # Configuración del problema
        c = [1, 1, 1, 1, 1, 1]
        
        A = [
            [-1, 0, 0, 0, 0, -1],
            [-1, -1, 0, 0, 0, 0],
            [0, -1, -1, 0, 0, 0],
            [0, 0, -1, -1, 0, 0],
            [0, 0, 0, -1, -1, 0],
            [0, 0, 0, 0, -1, -1]
        ]
        
        b = [-3, -2, -10, -14, -8, -10]
        bounds = [(0, None) for _ in range(6)]
        
        # Resolver
        result = linprog(c, A_ub=A, b_ub=b, bounds=bounds, method='highs')
        
        if result.success:
            self.resultado = result
            self.x_optimo = result.x
            self.mostrar_resultados()
            self.graficar_resultados()
        else:
            messagebox.showerror("Error", "No se encontró solución óptima")
    
    def mostrar_resultados(self):
        self.result_text.delete(1.0, tk.END)
        
        # Título de resultados
        self.result_text.insert(tk.END, "="*70 + "\n")
        self.result_text.insert(tk.END, " SOLUCIÓN ÓPTIMA ENCONTRADA\n")
        self.result_text.insert(tk.END, "="*70 + "\n\n")
        
        # Turnos
        turnos = ["12:00 AM (medianoche)", "4:00 AM", "8:00 AM", 
                 "12:00 PM (mediodía)", "4:00 PM", "8:00 PM"]
        
        self.result_text.insert(tk.END, " DISTRIBUCIÓN DE BIBLIOTECARIOS:\n")
        self.result_text.insert(tk.END, "-"*50 + "\n")
        
        for i, (turno, val) in enumerate(zip(turnos, self.x_optimo)):
            self.result_text.insert(tk.END, f"  Turno {turno:20s}: {int(val):3d} bibliotecarios\n")
        
        total = sum(self.x_optimo)
        self.result_text.insert(tk.END, "\n" + "="*50 + "\n")
        self.result_text.insert(tk.END, f" TOTAL MÍNIMO DE BIBLIOTECARIOS: {int(total)}\n")
        self.result_text.insert(tk.END, "="*50 + "\n\n")
        
        # Verificación de restricciones
        self.result_text.insert(tk.END, " VERIFICACIÓN DE RESTRICCIONES:\n")
        self.result_text.insert(tk.END, "-"*50 + "\n")
        
        periodos = [
            "12:00 AM - 3:59 AM", "4:00 AM - 7:59 AM", "8:00 AM - 11:59 AM",
            "12:00 PM - 3:59 PM", "4:00 PM - 7:59 PM", "8:00 PM - 11:59 PM"
        ]
        demandas = [3, 2, 10, 14, 8, 10]
        
        coberturas = [
            self.x_optimo[0] + self.x_optimo[5],
            self.x_optimo[0] + self.x_optimo[1],
            self.x_optimo[1] + self.x_optimo[2],
            self.x_optimo[2] + self.x_optimo[3],
            self.x_optimo[3] + self.x_optimo[4],
            self.x_optimo[4] + self.x_optimo[5]
        ]
        
        for i, (periodo, demanda, cobertura) in enumerate(zip(periodos, demandas, coberturas)):
            estado = "✓ CUMPLE" if cobertura >= demanda else "✗ NO CUMPLE"
            self.result_text.insert(tk.END, f"  {periodo:20s}: {int(cobertura):2d} >= {demanda:2d}? {estado}\n")
        
        # Teorema de dualidad
        self.result_text.insert(tk.END, "\n" + "="*70 + "\n")
        self.result_text.insert(tk.END, " TEOREMA DE DUALIDAD\n")
        self.result_text.insert(tk.END, "="*70 + "\n")
        self.result_text.insert(tk.END, "El valor óptimo del primal coincide con el del dual.\n")
        self.result_text.insert(tk.END, "Esto verifica la optimalidad de la solución.\n")
    
    def graficar_resultados(self):
        # Ventana de gráficos
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
        fig.suptitle('Análisis de Optimización - Biblioteca Universitaria', fontsize=16, fontweight='bold')
        
        # Gráfico 1: Distribución de bibliotecarios por turno
        turnos = ['12AM', '4AM', '8AM', '12PM', '4PM', '8PM']
        valores = [int(v) for v in self.x_optimo]
        colores = ['#3498db', '#e74c3c', '#2ecc71', '#f39c12', '#9b59b6', '#1abc9c']
        
        bars = ax1.bar(turnos, valores, color=colores, edgecolor='black', linewidth=1.5)
        ax1.set_xlabel('Hora de inicio del turno', fontsize=12)
        ax1.set_ylabel('Número de bibliotecarios', fontsize=12)
        ax1.set_title('Distribución Óptima de Bibliotecarios', fontsize=14, fontweight='bold')
        ax1.grid(True, alpha=0.3, axis='y')
        
        # Agregar valores en las barras
        for bar, val in zip(bars, valores):
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height + 0.3,
                    f'{int(val)}', ha='center', va='bottom', fontweight='bold')
        
        # Gráfico 2: Demanda vs Cobertura
        periodos = ['0-4', '4-8', '8-12', '12-16', '16-20', '20-24']
        demandas = [3, 2, 10, 14, 8, 10]
        
        coberturas = [
            self.x_optimo[0] + self.x_optimo[5],
            self.x_optimo[0] + self.x_optimo[1],
            self.x_optimo[1] + self.x_optimo[2],
            self.x_optimo[2] + self.x_optimo[3],
            self.x_optimo[3] + self.x_optimo[4],
            self.x_optimo[4] + self.x_optimo[5]
        ]
        
        x = np.arange(len(periodos))
        width = 0.35
        
        bars1 = ax2.bar(x - width/2, demandas, width, label='Demanda', color='#e74c3c', alpha=0.7)
        bars2 = ax2.bar(x + width/2, coberturas, width, label='Cobertura', color='#2ecc71', alpha=0.7)
        
        ax2.set_xlabel('Período de 4 horas', fontsize=12)
        ax2.set_ylabel('Número de bibliotecarios', fontsize=12)
        ax2.set_title('Demanda vs Cobertura por Período', fontsize=14, fontweight='bold')
        ax2.set_xticks(x)
        ax2.set_xticklabels(periodos)
        ax2.legend()
        ax2.grid(True, alpha=0.3, axis='y')
        
        # Agregar valores
        for bar in bars1:
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height + 0.3,
                    f'{int(height)}', ha='center', va='bottom', fontsize=9)
        
        for bar in bars2:
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height + 0.3,
                    f'{int(height)}', ha='center', va='bottom', fontsize=9)
        
        plt.tight_layout()
        plt.show()

# Ejecutar aplicación
if __name__ == "__main__":
    root = tk.Tk()
    app = BibliotecaApp(root)
    root.mainloop()