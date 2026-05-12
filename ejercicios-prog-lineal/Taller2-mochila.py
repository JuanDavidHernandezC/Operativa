"""
PROBLEMA DE LA MOCHILA DEL EXCURSIONISTA
Optimización de selección de artículos con capacidad limitada
"""

import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib
matplotlib.use('TkAgg')  # Forzar backend TkAgg para mejor compatibilidad
import matplotlib.pyplot as plt
import numpy as np
from itertools import combinations

# Configurar estilo de matplotlib para mejor visualización
plt.style.use('seaborn-v0_8-darkgrid')
plt.rcParams['font.size'] = 10
plt.rcParams['axes.titlesize'] = 12
plt.rcParams['axes.labelsize'] = 10

class MochilaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Problema de la Mochila - Excursionista")
        self.root.geometry("1100x800")
        self.root.configure(bg='#f0f2f5')
        
        # Datos del problema
        self.articulos = [
            {"nombre": "Artículo 1", "peso": 52, "valor": 100},
            {"nombre": "Artículo 2", "peso": 23, "valor": 60},
            {"nombre": "Artículo 3", "peso": 35, "valor": 70},
            {"nombre": "Artículo 4", "peso": 15, "valor": 15},
            {"nombre": "Artículo 5", "peso": 7, "valor": 15}
        ]
        self.capacidad = 60
        self.mejor_solucion = None
        
        self.create_widgets()
        
    def create_widgets(self):
        # Frame principal
        main_frame = tk.Frame(self.root, bg='#f0f2f5')
        main_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Título
        titulo = tk.Label(main_frame, text=" PROBLEMA DE LA MOCHILA", 
                         font=("Arial", 24, "bold"), bg='#f0f2f5', fg='#2c3e50')
        titulo.pack(pady=10)
        
        # Subtítulo
        subtitulo = tk.Label(main_frame, text="Optimización de selección de artículos para excursionismo", 
                            font=("Arial", 11), bg='#f0f2f5', fg='#7f8c8d')
        subtitulo.pack(pady=5)
        
        # Frame de tabla de artículos
        table_frame = tk.LabelFrame(main_frame, text=" DATOS DE LOS ARTÍCULOS", 
                                    font=("Arial", 11, "bold"), bg='white', fg='#2c3e50',
                                    relief=tk.RAISED, bd=2, padx=10, pady=10)
        table_frame.pack(pady=15, fill='x')
        
        # Tabla de artículos
        columns = ('Artículo', 'Peso (lb)', 'Valor', 'Valor/Peso', 'Eficiencia')
        tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=5)
        
        column_widths = {'Artículo': 120, 'Peso (lb)': 100, 'Valor': 100, 
                        'Valor/Peso': 120, 'Eficiencia': 120}
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=column_widths.get(col, 100), anchor='center')
        
        # Colores para la tabla
        for i, art in enumerate(self.articulos, 1):
            valor_peso = art['valor'] / art['peso']
            # Determinar eficiencia
            if valor_peso >= 2.0:
                eficiencia = "🟢 Alta"
            elif valor_peso >= 1.5:
                eficiencia = "🟡 Media"
            else:
                eficiencia = "🔴 Baja"
            
            tree.insert('', 'end', values=(f"Artículo {i}", art['peso'], 
                                          art['valor'], f"{valor_peso:.2f}", eficiencia))
        
        tree.pack(pady=5, padx=5)
        
        # Etiqueta de capacidad
        cap_label = tk.Label(table_frame, text=f" Capacidad máxima de la mochila: {self.capacidad} libras", 
                            font=("Arial", 11, "bold"), fg='#e74c3c', bg='white')
        cap_label.pack(pady=8)
        
        # Frame de botones
        btn_frame = tk.Frame(main_frame, bg='#f0f2f5')
        btn_frame.pack(pady=15)
        
        btn_resolver = tk.Button(btn_frame, text=" RESOLVER POR FUERZA BRUTA", 
                                command=self.resolver_fuerza_bruta,
                                font=("Arial", 11, "bold"), bg='#3498db', fg='white',
                                padx=15, pady=8, cursor='hand2')
        btn_resolver.pack(side=tk.LEFT, padx=8)
        
        btn_grafico = tk.Button(btn_frame, text=" MOSTRAR GRÁFICOS", 
                               command=self.mostrar_graficos,
                               font=("Arial", 11, "bold"), bg='#2ecc71', fg='white',
                               padx=15, pady=8, cursor='hand2')
        btn_grafico.pack(side=tk.LEFT, padx=8)
        
        btn_analisis = tk.Button(btn_frame, text=" ANÁLISIS DE SENSIBILIDAD", 
                                command=self.analisis_sensibilidad,
                                font=("Arial", 11, "bold"), bg='#e67e22', fg='white',
                                padx=15, pady=8, cursor='hand2')
        btn_analisis.pack(side=tk.LEFT, padx=8)
        
        btn_limpiar = tk.Button(btn_frame, text=" LIMPIAR", 
                               command=self.limpiar_resultados,
                               font=("Arial", 11, "bold"), bg='#95a5a6', fg='white',
                               padx=15, pady=8, cursor='hand2')
        btn_limpiar.pack(side=tk.LEFT, padx=8)
        
        # Frame de resultados
        result_frame = tk.LabelFrame(main_frame, text=" RESULTADOS", 
                                     font=("Arial", 11, "bold"), bg='#f0f2f5',
                                     fg='#2c3e50', relief=tk.RAISED, bd=2)
        result_frame.pack(pady=15, fill='both', expand=True)
        
        # Text widget con scrollbar
        text_frame = tk.Frame(result_frame, bg='white')
        text_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.result_text = tk.Text(text_frame, height=15, width=90, 
                                   font=("Consolas", 10), bg='white', 
                                   fg='#2c3e50', wrap=tk.WORD)
        self.result_text.pack(side=tk.LEFT, fill='both', expand=True)
        
        scrollbar = tk.Scrollbar(text_frame, command=self.result_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.result_text.config(yscrollcommand=scrollbar.set)
        
        # Configurar colores de tags
        self.result_text.tag_configure('titulo', font=('Arial', 12, 'bold'), foreground='#2c3e50')
        self.result_text.tag_configure('subtitulo', font=('Arial', 10, 'bold'), foreground='#3498db')
        self.result_text.tag_configure('exito', foreground='#27ae60')
        self.result_text.tag_configure('warning', foreground='#e67e22')
    
    def resolver_fuerza_bruta(self):
        """Resuelve el problema por fuerza bruta"""
        n = len(self.articulos)
        mejor_valor = 0
        mejor_combinacion = []
        todas_combinaciones = []
        
        # Probar todas las combinaciones posibles
        for r in range(1, n + 1):
            for comb in combinations(range(n), r):
                peso_total = sum(self.articulos[i]['peso'] for i in comb)
                valor_total = sum(self.articulos[i]['valor'] for i in comb)
                todas_combinaciones.append((comb, peso_total, valor_total))
                
                if peso_total <= self.capacidad and valor_total > mejor_valor:
                    mejor_valor = valor_total
                    mejor_combinacion = comb
        
        self.mejor_solucion = {
            'combinacion': mejor_combinacion,
            'valor': mejor_valor,
            'peso': sum(self.articulos[i]['peso'] for i in mejor_combinacion),
            'todas': todas_combinaciones
        }
        
        self.mostrar_resultados()
        messagebox.showinfo("Éxito", "¡Problema resuelto correctamente!")
    
    def limpiar_resultados(self):
        self.result_text.delete(1.0, tk.END)
        self.mejor_solucion = None
    
    def mostrar_resultados(self):
        self.result_text.delete(1.0, tk.END)
        
        if not self.mejor_solucion:
            self.result_text.insert(tk.END, " Primero resuelva el problema usando el botón 'RESOLVER'\n", 'warning')
            return
        
        # Título
        self.result_text.insert(tk.END, "="*85 + "\n", 'titulo')
        self.result_text.insert(tk.END, " SOLUCIÓN ÓPTIMA DEL PROBLEMA DE LA MOCHILA\n", 'titulo')
        self.result_text.insert(tk.END, "="*85 + "\n\n", 'titulo')
        
        # Mejor combinación
        self.result_text.insert(tk.END, " MEJOR SELECCIÓN DE ARTÍCULOS:\n", 'subtitulo')
        self.result_text.insert(tk.END, "-"*50 + "\n")
        
        for idx in self.mejor_solucion['combinacion']:
            art = self.articulos[idx]
            self.result_text.insert(tk.END, f"   {art['nombre']:12s} → Peso: {art['peso']:2d} lb | Valor: {art['valor']:3d} pts\n")
        
        self.result_text.insert(tk.END, "\n" + "="*50 + "\n")
        self.result_text.insert(tk.END, f" PESO TOTAL: {self.mejor_solucion['peso']} / {self.capacidad} libras\n")
        self.result_text.insert(tk.END, f" VALOR TOTAL: {self.mejor_solucion['valor']} puntos\n")
        self.result_text.insert(tk.END, f" EFICIENCIA: {self.mejor_solucion['peso']/self.capacidad*100:.1f}% de capacidad utilizada\n")
        self.result_text.insert(tk.END, "="*50 + "\n\n")
        
        # Top 5 mejores combinaciones
        self.result_text.insert(tk.END, " TOP 5 MEJORES COMBINACIONES:\n", 'subtitulo')
        self.result_text.insert(tk.END, "-"*50 + "\n")
        
        combinaciones_ordenadas = sorted([c for c in self.mejor_solucion['todas'] if c[1] <= self.capacidad],
                                        key=lambda x: x[2], reverse=True)[:5]
        
        for i, (comb, peso, valor) in enumerate(combinaciones_ordenadas, 1):
            articulos_str = ", ".join([self.articulos[j]['nombre'] for j in comb])
            if len(articulos_str) > 35:
                articulos_str = articulos_str[:32] + "..."
            medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else "  "
            self.result_text.insert(tk.END, f"  {medal} {i}. {articulos_str:<35} → Peso: {peso:2d} lb | Valor: {valor:3d}\n")
    
    def mostrar_graficos(self):
        if not self.mejor_solucion:
            messagebox.showwarning("Advertencia", "Primero resuelva el problema")
            return
        
        # Crear figura con tamaño adecuado
        fig = plt.figure(figsize=(16, 10), facecolor='white')
        fig.suptitle(' ANÁLISIS DEL PROBLEMA DE LA MOCHILA', fontsize=16, fontweight='bold', y=0.98)
        
        # Gráfico 1: Peso vs Valor
        ax1 = fig.add_subplot(2, 2, 1)
        pesos = [x[1] for x in self.mejor_solucion['todas']]
        valores = [x[2] for x in self.mejor_solucion['todas']]
        
        # Separar soluciones factibles e infactibles
        factibles = [(p, v) for p, v in zip(pesos, valores) if p <= self.capacidad]
        infactibles = [(p, v) for p, v in zip(pesos, valores) if p > self.capacidad]
        
        if factibles:
            p_f, v_f = zip(*factibles)
            ax1.scatter(p_f, v_f, c='#2ecc71', alpha=0.6, s=60, label='✅ Factibles', edgecolors='black', linewidth=0.5)
        
        if infactibles:
            p_i, v_i = zip(*infactibles)
            ax1.scatter(p_i, v_i, c='#e74c3c', alpha=0.6, s=60, label='❌ Infactibles', edgecolors='black', linewidth=0.5)
        
        # Marcar solución óptima
        ax1.scatter(self.mejor_solucion['peso'], self.mejor_solucion['valor'], 
                   c='gold', s=300, marker='*', edgecolors='black', 
                   linewidths=2, label=' SOLUCIÓN ÓPTIMA', zorder=5)
        
        ax1.axvline(x=self.capacidad, color='#3498db', linestyle='--', linewidth=2,
                   label=f' Capacidad ({self.capacidad} lb)')
        ax1.set_xlabel('Peso (libras)', fontsize=11, fontweight='bold')
        ax1.set_ylabel('Valor (puntos)', fontsize=11, fontweight='bold')
        ax1.set_title(' Espacio de Búsqueda: Peso vs Valor', fontsize=13, fontweight='bold')
        ax1.legend(loc='upper left', fontsize=9)
        ax1.grid(True, alpha=0.3, linestyle='--')
        ax1.set_facecolor('#f8f9fa')
        
        # Gráfico 2: Valor por artículo
        ax2 = fig.add_subplot(2, 2, 2)
        nombres = [f'Art{i+1}' for i in range(len(self.articulos))]
        valores_art = [art['valor'] for art in self.articulos]
        colores = ['#2ecc71' if i in self.mejor_solucion['combinacion'] else '#bdc3c7' 
                  for i in range(len(self.articulos))]
        
        bars = ax2.bar(nombres, valores_art, color=colores, edgecolor='black', linewidth=1.5)
        ax2.set_xlabel('Artículo', fontsize=11, fontweight='bold')
        ax2.set_ylabel('Valor', fontsize=11, fontweight='bold')
        ax2.set_title(' Valor por Artículo', fontsize=13, fontweight='bold')
        ax2.grid(True, alpha=0.3, axis='y', linestyle='--')
        ax2.set_facecolor('#f8f9fa')
        
        for bar, val in zip(bars, valores_art):
            ax2.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 2,
                    f'{val}', ha='center', va='bottom', fontweight='bold', fontsize=10)
        
        # Gráfico 3: Pastel de capacidad
        ax3 = fig.add_subplot(2, 2, 3)
        capacidad_usada = self.mejor_solucion['peso']
        capacidad_libre = self.capacidad - capacidad_usada
        
        sizes = [capacidad_usada, capacidad_libre]
        labels = [f'Usada\n{capacidad_usada} lb', f'Libre\n{capacidad_libre} lb']
        colors_pie = ['#2ecc71', '#e74c3c']
        explode = (0.05, 0)
        
        wedges, texts, autotexts = ax3.pie(sizes, explode=explode, labels=labels, colors=colors_pie,
                                           autopct='%1.1f%%', shadow=True, startangle=90,
                                           textprops={'fontsize': 11, 'fontweight': 'bold'})
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
            autotext.set_fontsize(10)
        ax3.set_title(' Utilización de Capacidad', fontsize=13, fontweight='bold')
        
        # Gráfico 4: Eficiencia
        ax4 = fig.add_subplot(2, 2, 4)
        densidad = [art['valor']/art['peso'] for art in self.articulos]
        colores_densidad = ['#e67e22' if i in self.mejor_solucion['combinacion'] else '#95a5a6' 
                           for i in range(len(self.articulos))]
        
        bars = ax4.bar(nombres, densidad, color=colores_densidad, edgecolor='black', linewidth=1.5)
        ax4.set_xlabel('Artículo', fontsize=11, fontweight='bold')
        ax4.set_ylabel('Valor/Peso', fontsize=11, fontweight='bold')
        ax4.set_title(' Eficiencia por Artículo', fontsize=13, fontweight='bold')
        ax4.grid(True, alpha=0.3, axis='y', linestyle='--')
        ax4.set_facecolor('#f8f9fa')
        
        for bar, val in zip(bars, densidad):
            ax4.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.05,
                    f'{val:.2f}', ha='center', va='bottom', fontsize=9, fontweight='bold')
        
        # Añadir línea de referencia de eficiencia
        ax4.axhline(y=2.0, color='#e74c3c', linestyle='--', alpha=0.7, label='Eficiencia alta (2.0)')
        ax4.legend(loc='upper right', fontsize=8)
        
        plt.tight_layout()
        plt.subplots_adjust(top=0.93, hspace=0.3, wspace=0.3)
        plt.show()
    
    def analisis_sensibilidad(self):
        """Análisis de sensibilidad variando la capacidad"""
        if not self.mejor_solucion:
            messagebox.showwarning("Advertencia", "Primero resuelva el problema")
            return
        
        # Calcular para diferentes capacidades
        capacidades = list(range(10, 101, 5))
        valores_optimos = []
        
        for cap in capacidades:
            mejor_valor = 0
            for comb in self.mejor_solucion['todas']:
                if comb[1] <= cap and comb[2] > mejor_valor:
                    mejor_valor = comb[2]
            valores_optimos.append(mejor_valor)
        
        # Crear gráfico de sensibilidad
        fig, ax = plt.subplots(figsize=(12, 7), facecolor='white')
        
        # Área bajo la curva
        ax.fill_between(capacidades, valores_optimos, alpha=0.3, color='#3498db')
        
        # Línea principal
        ax.plot(capacidades, valores_optimos, 'b-o', linewidth=2.5, markersize=8, 
               markerfacecolor='#2ecc71', markeredgecolor='white', markeredgewidth=1.5)
        
        # Línea de capacidad original
        ax.axvline(x=self.capacidad, color='#e74c3c', linestyle='--', linewidth=2.5,
                  label=f' Capacidad original ({self.capacidad} lb)')
        
        # Línea de valor original
        ax.axhline(y=self.mejor_solucion['valor'], color='#e67e22', linestyle='--', 
                  alpha=0.7, linewidth=2, label=f' Valor óptimo original ({self.mejor_solucion["valor"]})')
        
        # Punto de la solución actual
        ax.scatter([self.capacidad], [self.mejor_solucion['valor']], 
                  s=200, c='gold', marker='*', edgecolors='black', 
                  linewidths=2, zorder=5, label=' Solución actual')
        
        ax.set_xlabel('Capacidad de la mochila (libras)', fontsize=12, fontweight='bold')
        ax.set_ylabel('Valor óptimo alcanzable', fontsize=12, fontweight='bold')
        ax.set_title(' Análisis de Sensibilidad: Valor Óptimo vs Capacidad', 
                    fontsize=14, fontweight='bold')
        ax.legend(loc='upper left', fontsize=10)
        ax.grid(True, alpha=0.3, linestyle='--')
        ax.set_facecolor('#f8f9fa')
        
        # Añadir anotaciones
        for cap, val in zip(capacidades[::2], valores_optimos[::2]):
            ax.annotate(f'{val}', xy=(cap, val), xytext=(5, 5), 
                       textcoords='offset points', fontsize=8, alpha=0.7)
        
        plt.tight_layout()
        plt.show()
        
        # Mostrar análisis en texto
        messagebox.showinfo("Análisis de Sensibilidad", 
                           f" RESULTADOS DEL ANÁLISIS:\n\n"
                           f"• Capacidad actual: {self.capacidad} lb\n"
                           f"• Valor actual: {self.mejor_solucion['valor']} pts\n"
                           f"• Si aumentas a 70 lb, obtendrías: {max(valores_optimos[capacidades.index(70)])} pts\n"
                           f"• Si reduces a 50 lb, obtendrías: {max(valores_optimos[capacidades.index(50)])} pts\n\n"
                           f" La capacidad óptima es de 58 lb con valor 130 pts")

if __name__ == "__main__":
    root = tk.Tk()
    # Configurar icono (opcional)
    try:
        root.iconbitmap('icon.ico')
    except:
        pass
    app = MochilaApp(root)
    root.mainloop()