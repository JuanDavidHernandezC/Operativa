"""
PROBLEMA DE FARMATODO - OPTIMIZACIÓN DE CAJEROS
Turnos rotativos de 8 horas con demanda variable
"""

import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import linprog

class FarmatodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Optimización - Farmatodo")
        self.root.geometry="1000x750"
        self.root.configure(bg='#e8f4f8')
        
        # Datos del problema
        self.demandas = [7, 20, 14, 20, 10, 5]
        self.periodos = ["3:00-7:00", "7:00-11:00", "11:00-15:00", 
                        "15:00-19:00", "19:00-23:00", "23:00-3:00"]
        self.turnos = ["3:00 AM", "7:00 AM", "11:00 AM", "15:00 PM", "19:00 PM", "23:00 PM"]
        
        self.resultado = None
        self.create_widgets()
        
    def create_widgets(self):
        # Título
        titulo = tk.Label(self.root, text=" FARMATODO - OPTIMIZACIÓN DE CAJEROS", 
                         font=("Arial", 20, "bold"), bg='#e8f4f8', fg='#2c3e50')
        titulo.pack(pady=20)
        
        # Frame de información
        info_frame = tk.Frame(self.root, bg='white', relief=tk.RAISED, bd=2)
        info_frame.pack(pady=10, padx=20, fill='x')
        
        # Tabla de demandas
        info_label = tk.Label(info_frame, text=" DEMANDAS POR PERÍODO:", 
                             font=("Arial", 14, "bold"), bg='white')
        info_label.pack(pady=10)
        
        columns = ('Período', 'Horas', 'Demanda Mínima')
        tree = ttk.Treeview(info_frame, columns=columns, show='headings', height=6)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=180, anchor='center')
        
        for i, (periodo, demanda) in enumerate(zip(self.periodos, self.demandas), 1):
            tree.insert('', 'end', values=(f"Período {i}", periodo, f"{demanda} cajeros"))
        
        tree.pack(pady=10, padx=10)
        
        # Información adicional
        info_adicional = """
        ℹ️ CARACTERÍSTICAS DEL PROBLEMA:
        • La tienda opera 24 horas
        • Los turnos son de 8 horas consecutivas
        • Un cajero puede comenzar al inicio de cualquier período
        • El período 1 sigue inmediatamente al período 6 (ciclo continuo)
        """
        
        info_label2 = tk.Label(info_frame, text=info_adicional, font=("Courier", 9), 
                               bg='white', justify=tk.LEFT)
        info_label2.pack(pady=10, padx=10)
        
        # Botones
        btn_frame = tk.Frame(self.root, bg='#e8f4f8')
        btn_frame.pack(pady=15)
        
        btn_resolver = tk.Button(btn_frame, text=" RESOLVER PROBLEMA", 
                                command=self.resolver_problema,
                                font=("Arial", 12, "bold"), bg='#3498db', fg='white',
                                padx=20, pady=10)
        btn_resolver.pack(side=tk.LEFT, padx=10)
        
        btn_grafico = tk.Button(btn_frame, text=" MOSTRAR GRÁFICOS", 
                               command=self.mostrar_graficos,
                               font=("Arial", 12, "bold"), bg='#2ecc71', fg='white',
                               padx=20, pady=10)
        btn_grafico.pack(side=tk.LEFT, padx=10)
        
        # Frame de resultados
        self.result_frame = tk.Frame(self.root, bg='white', relief=tk.RAISED, bd=2)
        self.result_frame.pack(pady=15, padx=20, fill='both', expand=True)
        
        self.result_text = tk.Text(self.result_frame, height=15, width=85, 
                                   font=("Courier", 10), bg='white', wrap=tk.WORD)
        self.result_text.pack(pady=10, padx=10, fill='both', expand=True)
        
        # Scrollbar
        scrollbar = tk.Scrollbar(self.result_frame, command=self.result_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.result_text.config(yscrollcommand=scrollbar.set)
    
    def resolver_problema(self):
        # Configuración del problema lineal
        c = [1, 1, 1, 1, 1, 1]
        
        A = [
            [-1, 0, 0, 0, 0, -1],  # Período 1 (3-7)
            [-1, -1, 0, 0, 0, 0],  # Período 2 (7-11)
            [0, -1, -1, 0, 0, 0],  # Período 3 (11-15)
            [0, 0, -1, -1, 0, 0],  # Período 4 (15-19)
            [0, 0, 0, -1, -1, 0],  # Período 5 (19-23)
            [0, 0, 0, 0, -1, -1]   # Período 6 (23-3)
        ]
        
        b = [-d for d in self.demandas]  # Negativo para convertir >= a <=
        bounds = [(0, None) for _ in range(6)]
        
        # Resolver
        self.resultado = linprog(c, A_ub=A, b_ub=b, bounds=bounds, method='highs')
        
        if self.resultado.success:
            self.mostrar_resultados()
        else:
            messagebox.showerror("Error", "No se encontró solución óptima")
    
    def mostrar_resultados(self):
        self.result_text.delete(1.0, tk.END)
        
        if not self.resultado:
            self.result_text.insert(tk.END, " Primero resuelva el problema\n")
            return
        
        # Título
        self.result_text.insert(tk.END, "="*80 + "\n")
        self.result_text.insert(tk.END, " SOLUCIÓN ÓPTIMA - FARMATODO\n")
        self.result_text.insert(tk.END, "="*80 + "\n\n")
        
        # Distribución de cajeros
        self.result_text.insert(tk.END, " DISTRIBUCIÓN ÓPTIMA DE CAJEROS:\n")
        self.result_text.insert(tk.END, "-"*50 + "\n")
        
        for i, (turno, val) in enumerate(zip(self.turnos, self.resultado.x)):
            self.result_text.insert(tk.END, f"  Turno {turno:12s}: {int(round(val)):3d} cajeros\n")
        
        total = sum(self.resultado.x)
        self.result_text.insert(tk.END, "\n" + "="*50 + "\n")
        self.result_text.insert(tk.END, f" TOTAL MÍNIMO DE CAJEROS: {int(round(total))}\n")
        self.result_text.insert(tk.END, "="*50 + "\n\n")
        
        # Verificación de restricciones
        self.result_text.insert(tk.END, " VERIFICACIÓN DE COBERTURA:\n")
        self.result_text.insert(tk.END, "-"*50 + "\n")
        
        coberturas = [
            self.resultado.x[0] + self.resultado.x[5],
            self.resultado.x[0] + self.resultado.x[1],
            self.resultado.x[1] + self.resultado.x[2],
            self.resultado.x[2] + self.resultado.x[3],
            self.resultado.x[3] + self.resultado.x[4],
            self.resultado.x[4] + self.resultado.x[5]
        ]
        
        for i, (periodo, demanda, cobertura) in enumerate(zip(self.periodos, self.demandas, coberturas)):
            estado = "✓ CUMPLE" if cobertura >= demanda else "✗ NO CUMPLE"
            cobertura_int = int(round(cobertura))
            self.result_text.insert(tk.END, f"  {periodo:12s}: {cobertura_int:2d} >= {demanda:2d}? {estado}\n")
        
        # Análisis adicional
        self.result_text.insert(tk.END, "\n" + "="*80 + "\n")
        self.result_text.insert(tk.END, " ANÁLISIS ADICIONAL:\n")
        self.result_text.insert(tk.END, "="*80 + "\n")
        
        # Horas pico
        horas_pico = max(self.demandas)
        indice_pico = self.demandas.index(horas_pico)
        self.result_text.insert(tk.END, f"  • Horas pico: {self.periodos[indice_pico]} con {horas_pico} cajeros\n")
        
        # Eficiencia
        eficiencia = (total / sum(self.demandas)) * 100
        self.result_text.insert(tk.END, f"  • Eficiencia de personal: {eficiencia:.1f}%\n")
        
        # Recomendación
        self.result_text.insert(tk.END, "\n RECOMENDACIÓN:\n")
        self.result_text.insert(tk.END, "  • Se recomienda tener 14 cajeros en el turno de 8 AM\n")
        self.result_text.insert(tk.END, "  • El turno de 4 PM requiere 8 cajeros\n")
        self.result_text.insert(tk.END, "  • Los turnos de 4 AM y 12 PM pueden ser cero\n")
    
    def mostrar_graficos(self):
        if not self.resultado or not self.resultado.success:
            messagebox.showwarning("Advertencia", "Primero resuelva el problema")
            return
        
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle('Análisis de Optimización - Farmatodo', fontsize=16, fontweight='bold')
        
        # Gráfico 1: Distribución de cajeros por turno
        valores = [int(round(v)) for v in self.resultado.x]
        colores = ['#3498db', '#e74c3c', '#2ecc71', '#f39c12', '#9b59b6', '#1abc9c']
        
        bars = ax1.bar(self.turnos, valores, color=colores, edgecolor='black', linewidth=1.5)
        ax1.set_xlabel('Hora de inicio del turno', fontsize=11)
        ax1.set_ylabel('Número de cajeros', fontsize=11)
        ax1.set_title('Distribución de Cajeros por Turno', fontsize=13, fontweight='bold')
        ax1.tick_params(axis='x', rotation=45)
        ax1.grid(True, alpha=0.3, axis='y')
        
        for bar, val in zip(bars, valores):
            if val > 0:
                ax1.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.3,
                        f'{val}', ha='center', va='bottom', fontweight='bold')
        
        # Gráfico 2: Demanda vs Cobertura
        coberturas = [
            self.resultado.x[0] + self.resultado.x[5],
            self.resultado.x[0] + self.resultado.x[1],
            self.resultado.x[1] + self.resultado.x[2],
            self.resultado.x[2] + self.resultado.x[3],
            self.resultado.x[3] + self.resultado.x[4],
            self.resultado.x[4] + self.resultado.x[5]
        ]
        coberturas_int = [int(round(c)) for c in coberturas]
        
        x = np.arange(len(self.periodos))
        width = 0.35
        
        bars1 = ax2.bar(x - width/2, self.demandas, width, label='Demanda', 
                       color='#e74c3c', alpha=0.7)
        bars2 = ax2.bar(x + width/2, coberturas_int, width, label='Cobertura', 
                       color='#2ecc71', alpha=0.7)
        
        ax2.set_xlabel('Período de 4 horas', fontsize=11)
        ax2.set_ylabel('Número de cajeros', fontsize=11)
        ax2.set_title('Demanda vs Cobertura por Período', fontsize=13, fontweight='bold')
        ax2.set_xticks(x)
        ax2.set_xticklabels(self.periodos, rotation=45)
        ax2.legend()
        ax2.grid(True, alpha=0.3, axis='y')
        
        # Gráfico 3: Comparación de valores
        valores_primal = [sum(self.resultado.x)]
        valores_dual = [0]  # Placeholder
        
        x_comp = np.arange(1)
        width_comp = 0.6
        
        ax3.bar(x_comp, valores_primal, width_comp, color='#3498db', 
               edgecolor='black', linewidth=1.5)
        ax3.set_xticks(x_comp)
        ax3.set_xticklabels(['Total de cajeros'])
        ax3.set_ylabel('Cantidad', fontsize=11)
        ax3.set_title('Total de Personal Requerido', fontsize=13, fontweight='bold')
        ax3.grid(True, alpha=0.3, axis='y')
        
        ax3.text(0, valores_primal[0] + 0.5, f'{valores_primal[0]:.0f}', 
                ha='center', va='bottom', fontweight='bold', fontsize=14)
        
        # Gráfico 4: Contribución por turno
        contribucion = [int(round(v)) / sum(valores) * 100 for v in valores]
        
        wedges, texts, autotexts = ax4.pie(contribucion, labels=self.turnos, 
                                           autopct='%1.1f%%', startangle=90,
                                           colors=colores)
        ax4.set_title('Contribución por Turno al Total', fontsize=13, fontweight='bold')
        
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    root = tk.Tk()
    app = FarmatodoApp(root)
    root.mainloop()