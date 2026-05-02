# =============================================================================
#  INVESTIGACIÓN DE OPERACIONES I  —  Universidad de Cundinamarca
#  Grupos 601N y 603N
#
#  SOLUCIÓN COMPLETA DE PROBLEMAS DE PROGRAMACIÓN LINEAL
#  Y TRANSPORTE EN PYTHON
#
#  Librerías utilizadas:
#    - scipy.optimize.linprog  : programación lineal continua
#    - scipy.optimize.milp     : programación entera / binaria
#    - numpy                   : manejo de matrices y vectores
#
#  Instalación (si es necesario):
#    pip install scipy numpy
# =============================================================================

import numpy as np
from scipy.optimize import linprog, milp, LinearConstraint, Bounds

# ─────────────────────────────────────────────────────────────────────────────
#  UTILIDADES DE IMPRESIÓN
# ─────────────────────────────────────────────────────────────────────────────

def titulo(texto):
    """Imprime un encabezado principal con líneas de separación."""
    linea = "=" * 70
    print(f"\n{linea}")
    print(f"  {texto}")
    print(linea)

def subtitulo(texto):
    """Imprime un subtítulo secundario."""
    print(f"\n{'─' * 60}")
    print(f"  {texto}")
    print(f"{'─' * 60}")

def imprimir_tabla(encabezados, filas, anchos=None):
    """
    Imprime una tabla con encabezados y filas.
    encabezados : lista de strings
    filas       : lista de listas
    anchos      : lista de anchos por columna (opcional)
    """
    if anchos is None:
        anchos = [max(len(str(encabezados[i])),
                      max(len(str(f[i])) for f in filas)) + 2
                  for i in range(len(encabezados))]
    sep = "+" + "+".join("-" * a for a in anchos) + "+"
    fmt = "|" + "|".join(f"{{:^{a}}}" for a in anchos) + "|"
    print(sep)
    print(fmt.format(*encabezados))
    print(sep)
    for fila in filas:
        print(fmt.format(*[str(v) for v in fila]))
    print(sep)


# =============================================================================
#  TALLER 1 — PROBLEMA 1
#  Distribución de Panes: Compañía Panificadora
#  Tipo: Modelo de Transporte (PL)
# =============================================================================

titulo("TALLER 1 — PROBLEMA 1: Compañía Panificadora (Transporte)")

print("""
ENUNCIADO:
  Tres panaderías (P1, P2, P3) con capacidades 5000, 7000 y 9000 panes/día
  deben abastecer cinco bodegas (B1..B5) con demandas 2000, 6000, 8000, 4000
  y 1000 panes. Minimizar el costo total de transporte.

VARIABLES:
  x[i][j] = panes enviados de panadería i a bodega j
  i = 1,2,3   j = 1,2,3,4,5   → 15 variables en total

  Se ordenan linealmente: x11, x12, x13, x14, x15,
                           x21, x22, x23, x24, x25,
                           x31, x32, x33, x34, x35
""")

# ── Datos del problema ──────────────────────────────────────────────────────
costos = [
    [70, 30, 20, 30, 20],   # Panadería 1
    [60, 20, 80, 40, 70],   # Panadería 2
    [30, 50, 20, 40, 10],   # Panadería 3
]
capacidades = [5000, 7000, 9000]   # oferta de cada panadería
demandas    = [2000, 6000, 8000, 4000, 1000]  # demanda de cada bodega

n_origen  = 3   # panaderías
n_destino = 5   # bodegas
n_vars    = n_origen * n_destino  # 15 variables

# ── Vector de costos (función objetivo) ─────────────────────────────────────
c = []
for fila in costos:
    c.extend(fila)
print("Vector de costos c (orden: x11..x35):")
print(f"  {c}\n")

# ── Restricciones de capacidad (desigualdad <=) ──────────────────────────────
# Panadería i: suma de todas sus entregas <= capacidad[i]
A_ub = []
b_ub = []
for i in range(n_origen):
    fila = [0] * n_vars
    for j in range(n_destino):
        fila[i * n_destino + j] = 1
    A_ub.append(fila)
    b_ub.append(capacidades[i])

print("Restricciones de capacidad (A_ub · x <= b_ub):")
for i, (fila, cap) in enumerate(zip(A_ub, b_ub)):
    vars_activas = " + ".join(f"x{i+1}{j+1}" for j in range(n_destino))
    print(f"  {vars_activas} <= {cap}")

# ── Restricciones de demanda (igualdad =) ────────────────────────────────────
# Bodega j: suma de recibos de todas las panaderías = demanda[j]
A_eq = []
b_eq = []
for j in range(n_destino):
    fila = [0] * n_vars
    for i in range(n_origen):
        fila[i * n_destino + j] = 1
    A_eq.append(fila)
    b_eq.append(demandas[j])

print("\nRestricciones de demanda (A_eq · x = b_eq):")
for j, (fila, dem) in enumerate(zip(A_eq, b_eq)):
    vars_activas = " + ".join(f"x{i+1}{j+1}" for i in range(n_origen))
    print(f"  {vars_activas} = {dem}")

# ── No negatividad ─────────────────────────────────────────────────────────
bounds = [(0, None)] * n_vars  # xij >= 0 para todo i,j

# ── Resolución con linprog (Simplex / HiGHS) ─────────────────────────────────
print("\nResolviendo con scipy.optimize.linprog (método HiGHS)...")
resultado = linprog(c, A_ub=A_ub, b_ub=b_ub,
                    A_eq=A_eq, b_eq=b_eq,
                    bounds=bounds, method='highs')

# ── Presentación de resultados ───────────────────────────────────────────────
subtitulo("SOLUCIÓN ÓPTIMA — Problema 1")
print(f"  Estado del solver : {resultado.message}")
print(f"  Costo mínimo total: ${resultado.fun:,.0f}")

x = resultado.x
print("\n  Plan de distribución:")
filas_tabla = []
costo_total_check = 0
for i in range(n_origen):
    for j in range(n_destino):
        val = x[i * n_destino + j]
        if val > 0.5:  # solo rutas activas
            cp = val * costos[i][j]
            costo_total_check += cp
            filas_tabla.append([
                f"P{i+1} → B{j+1}",
                f"{val:,.0f}",
                f"{costos[i][j]}",
                f"${cp:,.0f}"
            ])
imprimir_tabla(
    ["Ruta", "Panes", "Costo/pan", "Costo parcial"],
    filas_tabla, [20, 10, 12, 16]
)
print(f"\n  Verificación costo total: ${costo_total_check:,.0f}")

print("\n  Uso de capacidades:")
for i in range(n_origen):
    uso = sum(x[i * n_destino + j] for j in range(n_destino))
    print(f"    Panadería {i+1}: {uso:,.0f} / {capacidades[i]:,} panes enviados")

print("\n  Cumplimiento de demandas:")
for j in range(n_destino):
    recibido = sum(x[i * n_destino + j] for i in range(n_origen))
    print(f"    Bodega {j+1}: {recibido:,.0f} / {demandas[j]:,} panes recibidos")


# =============================================================================
#  TALLER 1 — PROBLEMA 3
#  Producción en Dos Plantas
#  Tipo: Programación Lineal (minimización de costos)
# =============================================================================

titulo("TALLER 1 — PROBLEMA 3: Producción en Dos Plantas")

print("""
ENUNCIADO:
  Dos plantas fabrican tres productos. Cada planta tiene capacidad máxima
  de 10,000 unidades en total. Se requieren mínimo 6,000 del producto 1,
  8,000 del producto 2 y 5,000 del producto 3. Minimizar el costo de producción.

VARIABLES:
  x[i][j] = unidades del producto j fabricadas en la planta i
  i = 1,2  (plantas)   j = 1,2,3  (productos)

  Orden lineal: x11, x12, x13, x21, x22, x23

FUNCIÓN OBJETIVO:
  Min z = 5·x11 + 6·x12 + 18·x13 + 8·x21 + 7·x22 + 10·x23

RESTRICCIONES:
  x11 + x12 + x13 <= 10,000   (capacidad planta 1)
  x21 + x22 + x23 <= 10,000   (capacidad planta 2)
  x11 + x21 >= 6,000           (demanda producto 1)
  x12 + x22 >= 8,000           (demanda producto 2)
  x13 + x23 >= 5,000           (demanda producto 3)
  xij >= 0
""")

# ── Datos ────────────────────────────────────────────────────────────────────
costos_p3 = [5, 6, 18, 8, 7, 10]   # c = [x11,x12,x13,x21,x22,x23]
cap_planta = 10000
demanda_prod = [6000, 8000, 5000]

# ── Restricciones de capacidad (<=) ─────────────────────────────────────────
A_ub_p3 = [
    [1, 1, 1, 0, 0, 0],   # planta 1 <= 10000
    [0, 0, 0, 1, 1, 1],   # planta 2 <= 10000
]
b_ub_p3 = [cap_planta, cap_planta]

# ── Restricciones de demanda (>= se convierte a <= negando) ─────────────────
# xj_planta1 + xj_planta2 >= dem[j]  ↔  -xj_p1 - xj_p2 <= -dem[j]
A_ub_dem = [
    [-1, 0, 0, -1, 0, 0],   # prod 1 >= 6000
    [0, -1, 0, 0, -1, 0],   # prod 2 >= 8000
    [0, 0, -1, 0, 0, -1],   # prod 3 >= 5000
]
b_ub_dem = [-d for d in demanda_prod]

A_ub_total = A_ub_p3 + A_ub_dem
b_ub_total = b_ub_p3 + b_ub_dem

bounds_p3 = [(0, None)] * 6

print("Resolviendo...")
res_p3 = linprog(costos_p3,
                 A_ub=A_ub_total, b_ub=b_ub_total,
                 bounds=bounds_p3, method='highs')

subtitulo("SOLUCIÓN ÓPTIMA — Problema 3")
print(f"  Estado : {res_p3.message}")
print(f"  Costo mínimo total: ${res_p3.fun:,.0f}")

x3 = res_p3.x
nombres_prod = ["Producto 1", "Producto 2", "Producto 3"]
costos_unitarios = [[5,6,18],[8,7,10]]
filas_p3 = []
for i in range(2):
    for j in range(3):
        val = x3[i*3+j]
        if val > 0.5:
            cp = val * costos_unitarios[i][j]
            filas_p3.append([f"Planta {i+1} → {nombres_prod[j]}",
                              f"{val:,.0f}", f"${costos_unitarios[i][j]}",
                              f"${cp:,.0f}"])
imprimir_tabla(
    ["Asignación", "Unidades", "Costo/u", "Costo parcial"],
    filas_p3, [30, 12, 10, 16]
)

print("\n  Uso de capacidades:")
for i in range(2):
    uso = sum(x3[i*3+j] for j in range(3))
    print(f"    Planta {i+1}: {uso:,.0f} / {cap_planta:,}")

print("\n  Cumplimiento de demandas mínimas:")
for j in range(3):
    prod_total = sum(x3[i*3+j] for i in range(2))
    print(f"    {nombres_prod[j]}: {prod_total:,.0f} unidades (mín {demanda_prod[j]:,})")


# =============================================================================
#  TALLER 2 — PROBLEMA 4
#  Transporte Fábricas–Detallistas
#  Tipo: Modelo de Transporte (PL)
# =============================================================================

titulo("TALLER 2 — PROBLEMA 4: Fabricante de Plásticos (Transporte)")

print("""
ENUNCIADO:
  Dos fábricas tienen inventarios de 1,200 y 1,000 cajas de envoltura.
  Tres detallistas demandan 1,000, 700 y 500 cajas respectivamente.
  Minimizar el costo total de envío.

VARIABLES:
  x[i][j] = cajas enviadas de fábrica i a detallista j
  i=1,2  j=1,2,3  → 6 variables: x11, x12, x13, x21, x22, x23

COSTOS DE ENVÍO ($/caja):
         D1   D2   D3
  F1:    14   13   11
  F2:    13   13   12

FUNCIÓN OBJETIVO:
  Min z = 14·x11 + 13·x12 + 11·x13 + 13·x21 + 13·x22 + 12·x23

RESTRICCIONES:
  x11+x12+x13 <= 1200   (inventario fábrica 1)
  x21+x22+x23 <= 1000   (inventario fábrica 2)
  x11+x21 = 1000        (demanda detallista 1)
  x12+x22 = 700         (demanda detallista 2)
  x13+x23 = 500         (demanda detallista 3)
  xij >= 0
""")

# ── Datos ────────────────────────────────────────────────────────────────────
c_t2 = [14, 13, 11, 13, 13, 12]
inventarios = [1200, 1000]
demandas_t2 = [1000, 700, 500]
costos_t2   = [[14,13,11],[13,13,12]]

A_ub_t2 = [
    [1,1,1, 0,0,0],   # fábrica 1
    [0,0,0, 1,1,1],   # fábrica 2
]
b_ub_t2 = inventarios

A_eq_t2 = [
    [1,0,0, 1,0,0],   # detallista 1
    [0,1,0, 0,1,0],   # detallista 2
    [0,0,1, 0,0,1],   # detallista 3
]
b_eq_t2 = demandas_t2

print("Resolviendo...")
res_t2 = linprog(c_t2, A_ub=A_ub_t2, b_ub=b_ub_t2,
                 A_eq=A_eq_t2, b_eq=b_eq_t2,
                 bounds=[(0,None)]*6, method='highs')

subtitulo("SOLUCIÓN ÓPTIMA — Taller 2 Problema 4")
print(f"  Estado : {res_t2.message}")
print(f"  Costo mínimo de envío: ${res_t2.fun:,.0f}")

x_t2 = res_t2.x
filas_t2 = []
for i in range(2):
    for j in range(3):
        val = x_t2[i*3+j]
        if val > 0.5:
            cp = val * costos_t2[i][j]
            filas_t2.append([f"Fábrica {i+1} → Detallista {j+1}",
                              f"{val:,.0f}", f"${costos_t2[i][j]}", f"${cp:,.0f}"])
imprimir_tabla(
    ["Ruta", "Cajas", "Costo/caja", "Costo parcial"],
    filas_t2, [28, 8, 12, 16]
)
print("\n  Inventarios usados:")
for i in range(2):
    uso = sum(x_t2[i*3+j] for j in range(3))
    print(f"    Fábrica {i+1}: {uso:,.0f} / {inventarios[i]:,} cajas enviadas")


# =============================================================================
#  PROGRAMACIÓN BINARIA — PROBLEMA 1
#  Semiconductores: Producción y Distribución
#  Tipo: Modelo de Transporte con costo combinado (producción + envío)
# =============================================================================

titulo("PROGRAMACIÓN BINARIA — PROBLEMA 1: Semiconductores")

print("""
ENUNCIADO:
  Tres plantas producen módulos electrónicos para cuatro fabricantes de TV.
  El costo total por módulo = costo de producción + costo de envío.
  Capacidades: A=7500, B=10000, C=8100 módulos/mes.
  Demandas: I=4200, II=8300, III=6300, IV=2700 módulos.

VARIABLES:
  x[i][j] = módulos enviados de planta i a fabricante j
  i ∈ {A,B,C}   j ∈ {I,II,III,IV}   → 12 variables

COSTOS TOTALES (producción + envío por módulo, en $):
  Planta A: prod=1.10 → [1.21, 1.23, 1.19, 1.29]
  Planta B: prod=0.95 → [1.07, 1.11, 1.05, 1.09]
  Planta C: prod=1.03 → [1.17, 1.16, 1.15, 1.18]
""")

# ── Datos ────────────────────────────────────────────────────────────────────
costo_prod  = [1.10, 0.95, 1.03]
costo_envio = [
    [0.11, 0.13, 0.09, 0.19],   # planta A
    [0.12, 0.16, 0.10, 0.14],   # planta B
    [0.14, 0.13, 0.12, 0.15],   # planta C
]
capacidades_sem = [7500, 10000, 8100]
demandas_sem    = [4200, 8300, 6300, 2700]
plantas_sem     = ['A', 'B', 'C']
fabricantes_sem = ['I', 'II', 'III', 'IV']

# Costo total por módulo (producción + envío)
c_sem = []
costos_totales = []
for i in range(3):
    fila = []
    for j in range(4):
        ct = costo_prod[i] + costo_envio[i][j]
        c_sem.append(ct)
        fila.append(ct)
    costos_totales.append(fila)

print("Matriz de costos totales ($):")
imprimir_tabla(
    [" "] + fabricantes_sem,
    [[plantas_sem[i]] + [f"${costos_totales[i][j]:.2f}" for j in range(4)]
     for i in range(3)],
    [10, 10, 10, 10, 10]
)

# ── Restricciones de capacidad ───────────────────────────────────────────────
A_ub_sem = []
b_ub_sem = []
for i in range(3):
    fila = [0]*12
    for j in range(4):
        fila[i*4+j] = 1
    A_ub_sem.append(fila)
    b_ub_sem.append(capacidades_sem[i])

# ── Restricciones de demanda (=) ─────────────────────────────────────────────
A_eq_sem = []
b_eq_sem = []
for j in range(4):
    fila = [0]*12
    for i in range(3):
        fila[i*4+j] = 1
    A_eq_sem.append(fila)
    b_eq_sem.append(demandas_sem[j])

print("\nResolviendo...")
res_sem = linprog(c_sem, A_ub=A_ub_sem, b_ub=b_ub_sem,
                  A_eq=A_eq_sem, b_eq=b_eq_sem,
                  bounds=[(0,None)]*12, method='highs')

subtitulo("SOLUCIÓN ÓPTIMA — Prob. Binaria 1: Semiconductores")
print(f"  Estado : {res_sem.message}")
print(f"  Costo mínimo total: ${res_sem.fun:,.2f}")

x_sem = res_sem.x
filas_sem = []
for i in range(3):
    for j in range(4):
        val = x_sem[i*4+j]
        if val > 0.5:
            cp = val * costos_totales[i][j]
            filas_sem.append([
                f"Planta {plantas_sem[i]} → Fabr. {fabricantes_sem[j]}",
                f"{val:,.0f}",
                f"${costos_totales[i][j]:.2f}",
                f"${cp:,.2f}"
            ])
imprimir_tabla(
    ["Ruta", "Módulos", "Costo/u ($)", "Costo parcial ($)"],
    filas_sem, [30, 10, 12, 18]
)


# =============================================================================
#  PROGRAMACIÓN BINARIA — PROBLEMA 2
#  Asignación de Programadores a Desarrollos
#  Tipo: Programación Entera Binaria (Problema de Asignación)
# =============================================================================

titulo("PROGRAMACIÓN BINARIA — PROBLEMA 2: Asignación de Programadores")

print("""
ENUNCIADO:
  Cinco programadores deben ser asignados a cinco desarrollos, uno cada uno.
  Se minimiza el tiempo total. Cada variable es binaria:
    x[i][j] = 1  si el programador i realiza el desarrollo j
    x[i][j] = 0  en caso contrario

FUNCIÓN OBJETIVO:
  Min z = Σᵢ Σⱼ t[i][j] · x[i][j]

RESTRICCIONES:
  Σⱼ x[i][j] = 1   ∀i  (cada programador a exactamente 1 desarrollo)
  Σᵢ x[i][j] = 1   ∀j  (cada desarrollo asignado a exactamente 1 programador)
  x[i][j] ∈ {0, 1}

TABLA DE TIEMPOS (horas):
""")

tiempos = [
    [145, 122, 130,  95, 115],  # programador 1
    [ 80,  63,  85,  48,  78],  # programador 2
    [121, 107,  93,  69,  95],  # programador 3
    [118,  83, 116,  80, 105],  # programador 4
    [ 97,  75, 120,  80, 111],  # programador 5
]

imprimir_tabla(
    [" ", "Des.1", "Des.2", "Des.3", "Des.4", "Des.5"],
    [[f"Prog.{i+1}"] + tiempos[i] for i in range(5)],
    [9, 7, 7, 7, 7, 7]
)

# ── Aplanar la matriz de tiempos en vector de costos (25 variables) ──────────
n = 5
c_asig = np.array([tiempos[i][j] for i in range(n) for j in range(n)],
                   dtype=float)

# ── Restricciones de igualdad ────────────────────────────────────────────────
# Cada programador asignado a exactamente 1 desarrollo: Σⱼ x[i][j] = 1
# Cada desarrollo a exactamente 1 programador: Σᵢ x[i][j] = 1
filas_eq = []
rhs_eq   = []

for i in range(n):  # una ecuación por programador
    fila = [0] * (n*n)
    for j in range(n):
        fila[i*n + j] = 1
    filas_eq.append(fila)
    rhs_eq.append(1)

for j in range(n):  # una ecuación por desarrollo
    fila = [0] * (n*n)
    for i in range(n):
        fila[i*n + j] = 1
    filas_eq.append(fila)
    rhs_eq.append(1)

A_asig = np.array(filas_eq, dtype=float)
b_asig = np.array(rhs_eq, dtype=float)

# ── Resolver con MILP (variables binarias) ───────────────────────────────────
print("\nResolviendo con scipy.optimize.milp (variables enteras binarias)...")
restricciones = LinearConstraint(A_asig, b_asig, b_asig)  # lb == ub → igualdad
integrality   = np.ones(n*n)                               # 1 = entera (binaria con bounds 0-1)
bounds_asig   = Bounds(lb=0, ub=1)

res_asig = milp(c_asig,
                constraints=restricciones,
                integrality=integrality,
                bounds=bounds_asig)

subtitulo("SOLUCIÓN ÓPTIMA — Prob. Binaria 2: Asignación")
print(f"  Estado : {res_asig.message}")
print(f"  Tiempo mínimo total: {res_asig.fun:.0f} horas")

x_asig = np.round(res_asig.x).astype(int)
filas_asig = []
for i in range(n):
    for j in range(n):
        if x_asig[i*n + j] == 1:
            filas_asig.append([
                f"Programador {i+1}",
                f"Desarrollo {j+1}",
                f"{tiempos[i][j]} horas"
            ])
imprimir_tabla(
    ["Programador", "Desarrollo", "Tiempo"],
    filas_asig, [16, 14, 12]
)

print("\n  Matriz de asignación final (1 = asignado):")
print("       Des1 Des2 Des3 Des4 Des5")
for i in range(n):
    fila_str = "  ".join(str(x_asig[i*n+j]) for j in range(n))
    print(f"  Prog{i+1}  {fila_str}")


# =============================================================================
#  PROGRAMACIÓN BINARIA — PROBLEMA 3
#  Compra de Software — Empresa Latinoamericana
#  Tipo: Modelo de Transporte (PL)
# =============================================================================

titulo("PROGRAMACIÓN BINARIA — PROBLEMA 3: Compra de Software")

print("""
ENUNCIADO:
  Una empresa puede comprar aplicaciones de software a tres proveedores
  para tres sucursales. Minimizar el costo total respetando capacidades
  de los proveedores y demandas de las sucursales.

CAPACIDADES: P1=320, P2=270, P3=190 aplicaciones/año
DEMANDAS:    S1=100, S2=180, S3=350 aplicaciones/año

COSTOS ($/aplicación):
         S1   S2   S3
  P1:    92   89   90
  P2:    91   91   95
  P3:    87   90   92

VARIABLES: x[i][j] = aplicaciones compradas de proveedor i para sucursal j
""")

costos_sw = [[92,89,90],[91,91,95],[87,90,92]]
cap_sw    = [320, 270, 190]
dem_sw    = [100, 180, 350]

c_sw = [costos_sw[i][j] for i in range(3) for j in range(3)]

A_ub_sw = []
b_ub_sw = []
for i in range(3):  # restricciones de capacidad
    fila = [0]*9
    for j in range(3):
        fila[i*3+j] = 1
    A_ub_sw.append(fila)
    b_ub_sw.append(cap_sw[i])

A_eq_sw = []
b_eq_sw = []
for j in range(3):  # restricciones de demanda exacta
    fila = [0]*9
    for i in range(3):
        fila[i*3+j] = 1
    A_eq_sw.append(fila)
    b_eq_sw.append(dem_sw[j])

print("Resolviendo...")
res_sw = linprog(c_sw, A_ub=A_ub_sw, b_ub=b_ub_sw,
                 A_eq=A_eq_sw, b_eq=b_eq_sw,
                 bounds=[(0,None)]*9, method='highs')

subtitulo("SOLUCIÓN ÓPTIMA — Prob. Binaria 3: Software")
print(f"  Estado : {res_sw.message}")
print(f"  Costo mínimo total: ${res_sw.fun:,.0f}")

x_sw = res_sw.x
filas_sw = []
for i in range(3):
    for j in range(3):
        val = x_sw[i*3+j]
        if val > 0.5:
            cp = val * costos_sw[i][j]
            filas_sw.append([f"P{i+1} → S{j+1}", f"{val:,.0f}",
                              f"${costos_sw[i][j]}", f"${cp:,.0f}"])
imprimir_tabla(
    ["Ruta", "Aplicaciones", "Precio/u", "Costo parcial"],
    filas_sw, [12, 14, 10, 16]
)


# =============================================================================
#  PROGRAMACIÓN BINARIA — PROBLEMA 4
#  Compañía Panificadora — Maximizar Ganancia
#  Tipo: PL (maximización de beneficio neto)
# =============================================================================

titulo("PROGRAMACIÓN BINARIA — PROBLEMA 4: Panificadora (Maximizar Ganancia)")

print("""
ENUNCIADO:
  Dos plantas producen hogazas para cuatro cadenas de restaurantes.
  Maximizar la ganancia total = precio_venta - costo_producción - costo_envío.

  Planta A: cap=2500, costo_prod=23¢
  Planta B: cap=2100, costo_prod=25¢

  Cadenas y precios ofrecidos (¢/hogaza):
    C1: dem_máx=1800, precio=39¢
    C2: dem_máx=2300, precio=37¢
    C3: dem_máx=550,  precio=40¢
    C4: dem_máx=1750, precio=36¢

  Costos de envío (¢/hogaza):
          C1  C2  C3  C4
  PA:      6   8  11   9
  PB:     12   6   8   5

VARIABLES: x[i][j] = hogazas de planta i enviadas a cadena j
  i = A,B   j = 1,2,3,4   → 8 variables
""")

costo_prod_pan = [23, 25]  # A, B
precio_cadena  = [39, 37, 40, 36]
costo_env_pan  = [[6,8,11,9],[12,6,8,5]]
cap_planta_pan = [2500, 2100]
dem_max_pan    = [1800, 2300, 550, 1750]

# Ganancia neta por hogaza: precio - costo_prod - costo_envío
ganancia = []
matriz_ganancia = []
for i in range(2):
    fila = []
    for j in range(4):
        g = precio_cadena[j] - costo_prod_pan[i] - costo_env_pan[i][j]
        ganancia.append(g)
        fila.append(g)
    matriz_ganancia.append(fila)

print("Ganancia neta por hogaza (¢):")
imprimir_tabla(
    [" ", "C1", "C2", "C3", "C4"],
    [["Planta A"] + matriz_ganancia[0],
     ["Planta B"] + matriz_ganancia[1]],
    [10, 8, 8, 8, 8]
)

# Maximizar → minimizar negativo de la ganancia
c_pan = [-g for g in ganancia]

A_ub_pan = [
    [1,1,1,1, 0,0,0,0],   # Planta A <= 2500
    [0,0,0,0, 1,1,1,1],   # Planta B <= 2100
    [1,0,0,0, 1,0,0,0],   # Cadena 1 <= 1800
    [0,1,0,0, 0,1,0,0],   # Cadena 2 <= 2300
    [0,0,1,0, 0,0,1,0],   # Cadena 3 <= 550
    [0,0,0,1, 0,0,0,1],   # Cadena 4 <= 1750
]
b_ub_pan = [2500, 2100, 1800, 2300, 550, 1750]

print("\nResolviendo (maximización → negamos la FO)...")
res_pan = linprog(c_pan, A_ub=A_ub_pan, b_ub=b_ub_pan,
                  bounds=[(0,None)]*8, method='highs')

subtitulo("SOLUCIÓN ÓPTIMA — Prob. Binaria 4: Panificadora")
print(f"  Estado : {res_pan.message}")
print(f"  Ganancia máxima: {-res_pan.fun:,.0f} centavos = ${-res_pan.fun/100:.2f}")

x_pan = res_pan.x
cadenas_pan = ['C1','C2','C3','C4']
filas_pan = []
for i, planta in enumerate(['A','B']):
    for j in range(4):
        val = x_pan[i*4+j]
        if val > 0.5:
            gp = val * matriz_ganancia[i][j]
            filas_pan.append([f"Planta {planta} → {cadenas_pan[j]}",
                               f"{val:,.0f}", f"{matriz_ganancia[i][j]}¢",
                               f"{gp:,.0f}¢"])
imprimir_tabla(
    ["Ruta", "Hogazas", "Ganancia/u", "Ganancia parcial"],
    filas_pan, [22, 10, 12, 18]
)


# =============================================================================
#  PROGRAMACIÓN BINARIA — PROBLEMA 5
#  Vacunas COVIG-19
#  Tipo: Modelo de Transporte con demanda mínima garantizada
# =============================================================================

titulo("PROGRAMACIÓN BINARIA — PROBLEMA 5: Distribución de Vacunas COVIG-19")

print("""
ENUNCIADO:
  Dos compañías farmacéuticas (C1=1.1M, C2=0.9M dosis) deben enviar vacunas
  a tres ciudades. Cada ciudad debe recibir AL MENOS las dosis para ancianos.
  Minimizar el costo total de envío.

  Dosis mínimas para ancianos (millones):
    Ciudad 1: 0.325   Ciudad 2: 0.260   Ciudad 3: 0.195

  Capacidad máxima de administración (ancianos + otros, en millones):
    Ciudad 1: 1.075   Ciudad 2: 1.060   Ciudad 3: 0.845

  Costos de envío (¢/dosis):
          C1  C2  C3
  Comp1:   3   3   6
  Comp2:   1   4   7

VARIABLES: x[i][j] = millones de dosis enviadas de compañía i a ciudad j
""")

costo_vac = [3,3,6, 1,4,7]
cap_vac    = [1.1, 0.9]
min_anc    = [0.325, 0.260, 0.195]  # mínimo para ancianos
max_total  = [1.075, 1.060, 0.845] # capacidad máx por ciudad

# Restricciones de capacidad (<= disponible)
A_ub_vac = [
    [1,1,1, 0,0,0],   # Compañía 1 <= 1.1
    [0,0,0, 1,1,1],   # Compañía 2 <= 0.9
]
b_ub_vac = cap_vac

# Restricciones de demanda mínima (>= → negar)
for j in range(3):
    fila = [0]*6
    fila[j] = -1       # compañía 1 a ciudad j
    fila[3+j] = -1     # compañía 2 a ciudad j
    A_ub_vac.append(fila)
    b_ub_vac.append(-min_anc[j])

# Restricciones de capacidad máxima por ciudad
for j in range(3):
    fila = [0]*6
    fila[j] = 1
    fila[3+j] = 1
    A_ub_vac.append(fila)
    b_ub_vac.append(max_total[j])

print("Resolviendo...")
res_vac = linprog(costo_vac, A_ub=A_ub_vac, b_ub=b_ub_vac,
                  bounds=[(0,None)]*6, method='highs')

subtitulo("SOLUCIÓN ÓPTIMA — Prob. Binaria 5: Vacunas")
print(f"  Estado : {res_vac.message}")
# costo en centavos × millones de dosis × 1,000,000 dosis/millón ÷ 100 (¢→$)
costo_dolares = res_vac.fun * 1_000_000 / 100
print(f"  Costo mínimo: {res_vac.fun:.4f} M·¢  =  ${costo_dolares:,.2f}")

x_vac = res_vac.x
ciudades_vac = ['Ciudad 1', 'Ciudad 2', 'Ciudad 3']
filas_vac = []
for i in range(2):
    for j in range(3):
        val = x_vac[i*3+j]
        if val > 0.001:
            filas_vac.append([f"Compañía {i+1} → {ciudades_vac[j]}",
                               f"{val:.3f} M dosis",
                               f"{costo_vac[i*3+j]}¢/dosis"])
imprimir_tabla(
    ["Ruta", "Dosis (millones)", "Costo envío"],
    filas_vac, [28, 18, 14]
)
print("\n  Verificación — dosis recibidas por ciudad:")
for j in range(3):
    total = sum(x_vac[i*3+j] for i in range(2))
    print(f"    {ciudades_vac[j]}: {total:.3f} M dosis "
          f"(mín ancianos = {min_anc[j]} M)  ✔" if total >= min_anc[j]-1e-6
          else f"    {ciudades_vac[j]}: {total:.3f} M  ✗ INCUMPLE")

# ─── Resumen general ────────────────────────────────────────────────────────
titulo("RESUMEN DE RESULTADOS")
print("""
  ┌─────────────────────────────────────────────────────────────┬──────────────────┐
  │ Problema                                                    │ Resultado óptimo │
  ├─────────────────────────────────────────────────────────────┼──────────────────┤
  │ T1-P1  Panificadora (transporte, min costo)                 │  $  480,000      │
  │ T1-P3  Dos plantas, tres productos (min costo)              │  $  132,000      │
  │ T2-P4  Fábricas–Detallistas (min costo envío)               │  $   27,600      │
  │ PB-P1  Semiconductores (min costo total)                    │  $   24,142      │
  │ PB-P2  Asignación programadores (min horas, binaria)        │    436 horas     │
  │ PB-P3  Compra de software (min costo)                       │  $   56,580      │
  │ PB-P4  Panificadora ganancia (max ganancia)                 │  $      353.50   │
  │ PB-P5  Vacunas COVIG-19 (min costo envío)                   │  $   22,750      │
  └─────────────────────────────────────────────────────────────┴──────────────────┘
""")

print("  Todos los problemas resueltos exitosamente con scipy.optimize.")
print("  Método utilizado: HiGHS (Simplex + Programación Entera)\n")