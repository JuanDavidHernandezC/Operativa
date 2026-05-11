from __future__ import annotations

from datetime import datetime
from typing import Any

import numpy as np
from flask import Flask, render_template_string
from scipy.optimize import Bounds, LinearConstraint, linprog, milp


def fmt_int(value: float | int) -> str:
    return f"{value:,.0f}"


def fmt_float(value: float, decimals: int = 2) -> str:
    return f"{value:,.{decimals}f}"


def fmt_currency(value: float, decimals: int = 0) -> str:
    return f"${value:,.{decimals}f}" if decimals else f"${value:,.0f}"


def route_rows(
    solution: np.ndarray,
    costs: list[list[float]],
    origins: list[str],
    destinations: list[str],
    threshold: float = 0.5,
    value_decimals: int = 0,
    cost_decimals: int = 0,
    total_decimals: int = 0,
    value_suffix: str = "",
    cost_suffix: str = "",
    total_suffix: str = "",
) -> list[list[str]]:
    rows: list[list[str]] = []
    width = len(destinations)
    for i, origin in enumerate(origins):
        for j, destination in enumerate(destinations):
            value = float(solution[i * width + j])
            if value > threshold:
                unit_cost = costs[i][j]
                partial = value * unit_cost
                rows.append(
                    [
                        f"{origin} → {destination}",
                        f"{fmt_float(value, value_decimals)}{value_suffix}",
                        f"{fmt_float(unit_cost, cost_decimals)}{cost_suffix}",
                        f"{fmt_float(partial, total_decimals)}{total_suffix}",
                    ]
                )
    return rows


def matrix_rows(
    matrix: list[list[Any]],
    row_labels: list[str],
    col_labels: list[str],
    value_formatter=lambda value: str(value),
) -> list[list[str]]:
    rows: list[list[str]] = []
    for row_label, row in zip(row_labels, matrix):
        rows.append([row_label] + [value_formatter(value) for value in row])
    return rows


def solve_problem_1() -> dict[str, Any]:
    costs = [
        [70, 30, 20, 30, 20],
        [60, 20, 80, 40, 70],
        [30, 50, 20, 40, 10],
    ]
    supplies = [5000, 7000, 9000]
    demands = [2000, 6000, 8000, 4000, 1000]
    origins = ["Panadería 1", "Panadería 2", "Panadería 3"]
    destinations = ["Bodega 1", "Bodega 2", "Bodega 3", "Bodega 4", "Bodega 5"]

    c = [costs[i][j] for i in range(3) for j in range(5)]
    a_ub = []
    b_ub = []
    for i in range(3):
        row = [0] * 15
        for j in range(5):
            row[i * 5 + j] = 1
        a_ub.append(row)
        b_ub.append(supplies[i])

    a_eq = []
    b_eq = []
    for j in range(5):
        row = [0] * 15
        for i in range(3):
            row[i * 5 + j] = 1
        a_eq.append(row)
        b_eq.append(demands[j])

    result = linprog(c, A_ub=a_ub, b_ub=b_ub, A_eq=a_eq, b_eq=b_eq, bounds=[(0, None)] * 15, method="highs")
    x = result.x

    delivery_rows = route_rows(x, costs, origins, destinations)
    usage_rows = [
        [origins[i], fmt_int(sum(x[i * 5 + j] for j in range(5))), fmt_int(supplies[i]), f"{sum(x[i * 5 + j] for j in range(5)) / supplies[i] * 100:.0f}%"]
        for i in range(3)
    ]
    demand_rows = [
        [destinations[j], fmt_int(sum(x[i * 5 + j] for i in range(3))), fmt_int(demands[j]), "100%"]
        for j in range(5)
    ]

    return {
        "anchor": "t1p1",
        "eyebrow": "Taller 1 · Transporte",
        "title": "Compañía Panificadora",
        "subtitle": "Distribución óptima entre panaderías y bodegas con costo mínimo total.",
        "description": "Tres panaderías abastecen cinco bodegas. El modelo minimiza el costo de transporte cumpliendo capacidades y demandas exactamente.",
        "accent": "#f59e0b",
        "accent_soft": "rgba(245, 158, 11, 0.14)",
        "objective_label": "Costo mínimo total",
        "objective_value": fmt_currency(result.fun),
        "solver_message": result.message,
        "metrics": [
            {"label": "Estado", "value": "Óptimo"},
            {"label": "Capacidad total", "value": fmt_int(sum(supplies))},
            {"label": "Demanda total", "value": fmt_int(sum(demands))},
        ],
        "notes": ["Todas las capacidades se usan al 100% y cada demanda se satisface exactamente."],
        "tables": [
            {"title": "Plan de distribución", "headers": ["Ruta", "Panes", "Costo/pan", "Costo parcial"], "rows": delivery_rows},
            {"title": "Uso de capacidades", "headers": ["Panadería", "Enviado", "Capacidad", "Uso"], "rows": usage_rows},
            {"title": "Cumplimiento de demandas", "headers": ["Bodega", "Recibido", "Demanda", "Cumplimiento"], "rows": demand_rows},
        ],
    }


def solve_problem_3() -> dict[str, Any]:
    costs = [[5, 6, 18], [8, 7, 10]]
    capacity = 10000
    demand = [6000, 8000, 5000]
    plants = ["Planta 1", "Planta 2"]
    products = ["Producto 1", "Producto 2", "Producto 3"]

    a_ub = [[1, 1, 1, 0, 0, 0], [0, 0, 0, 1, 1, 1]]
    b_ub = [capacity, capacity]
    a_ub += [[-1, 0, 0, -1, 0, 0], [0, -1, 0, 0, -1, 0], [0, 0, -1, 0, 0, -1]]
    b_ub += [-d for d in demand]
    c = [costs[i][j] for i in range(2) for j in range(3)]

    result = linprog(c, A_ub=a_ub, b_ub=b_ub, bounds=[(0, None)] * 6, method="highs")
    x = result.x

    rows = route_rows(x, costs, plants, products)
    usage_rows = [
        [plants[i], fmt_int(sum(x[i * 3 + j] for j in range(3))), fmt_int(capacity), f"{sum(x[i * 3 + j] for j in range(3)) / capacity * 100:.0f}%"]
        for i in range(2)
    ]
    demand_rows = [
        [products[j], fmt_int(sum(x[i * 3 + j] for i in range(2))), fmt_int(demand[j]), f"≥ {fmt_int(demand[j])}"]
        for j in range(3)
    ]

    return {
        "anchor": "t1p3",
        "eyebrow": "Taller 1 · Producción",
        "title": "Dos Plantas, Tres Productos",
        "subtitle": "Asignación mínima de costo con restricciones de capacidad y demanda mínima.",
        "description": "Cada planta puede producir hasta 10,000 unidades. El modelo reparte la producción para cubrir los mínimos requeridos al menor costo posible.",
        "accent": "#14b8a6",
        "accent_soft": "rgba(20, 184, 166, 0.14)",
        "objective_label": "Costo mínimo total",
        "objective_value": fmt_currency(result.fun),
        "solver_message": result.message,
        "metrics": [
            {"label": "Estado", "value": "Óptimo"},
            {"label": "Demanda mínima", "value": fmt_int(sum(demand))},
            {"label": "Capacidad total", "value": fmt_int(2 * capacity)},
        ],
        "notes": ["La Planta 1 trabaja al límite; la Planta 2 conserva holgura."],
        "tables": [
            {"title": "Producción asignada", "headers": ["Asignación", "Unidades", "Costo/u", "Costo parcial"], "rows": rows},
            {"title": "Uso de capacidades", "headers": ["Planta", "Producción", "Capacidad", "Uso"], "rows": usage_rows},
            {"title": "Cobertura de demanda", "headers": ["Producto", "Producido", "Mínimo", "Verificación"], "rows": demand_rows},
        ],
    }


def solve_problem_4() -> dict[str, Any]:
    costs = [[14, 13, 11], [13, 13, 12]]
    inventories = [1200, 1000]
    demands = [1000, 700, 500]
    factories = ["Fábrica 1", "Fábrica 2"]
    retailers = ["Detallista 1", "Detallista 2", "Detallista 3"]

    c = [costs[i][j] for i in range(2) for j in range(3)]
    a_ub = [[1, 1, 1, 0, 0, 0], [0, 0, 0, 1, 1, 1]]
    b_ub = inventories
    a_eq = [[1, 0, 0, 1, 0, 0], [0, 1, 0, 0, 1, 0], [0, 0, 1, 0, 0, 1]]
    b_eq = demands

    result = linprog(c, A_ub=a_ub, b_ub=b_ub, A_eq=a_eq, b_eq=b_eq, bounds=[(0, None)] * 6, method="highs")
    x = result.x

    rows = route_rows(x, costs, factories, retailers)
    inventory_rows = [
        [factories[i], fmt_int(sum(x[i * 3 + j] for j in range(3))), fmt_int(inventories[i]), f"{sum(x[i * 3 + j] for j in range(3)) / inventories[i] * 100:.0f}%"]
        for i in range(2)
    ]

    return {
        "anchor": "t2p4",
        "eyebrow": "Taller 2 · Transporte",
        "title": "Fabricante de Plásticos",
        "subtitle": "Distribución con inventarios limitados y demandas exactas.",
        "description": "Se minimiza el costo de envío desde dos fábricas hacia tres detallistas, usando toda la oferta disponible.",
        "accent": "#38bdf8",
        "accent_soft": "rgba(56, 189, 248, 0.14)",
        "objective_label": "Costo mínimo de envío",
        "objective_value": fmt_currency(result.fun),
        "solver_message": result.message,
        "metrics": [
            {"label": "Estado", "value": "Óptimo"},
            {"label": "Inventario total", "value": fmt_int(sum(inventories))},
            {"label": "Demanda total", "value": fmt_int(sum(demands))},
        ],
        "notes": ["El problema está balanceado y se satisface con asignaciones enteras."],
        "tables": [
            {"title": "Plan de envío", "headers": ["Ruta", "Cajas", "Costo/caja", "Costo parcial"], "rows": rows},
            {"title": "Inventarios usados", "headers": ["Fábrica", "Enviado", "Inventario", "Uso"], "rows": inventory_rows},
        ],
    }


def solve_problem_5() -> dict[str, Any]:
    costs = [[1.21, 1.23, 1.19, 1.29], [1.07, 1.11, 1.05, 1.09], [1.17, 1.16, 1.15, 1.18]]
    capacities = [7500, 10000, 8100]
    demands = [4200, 8300, 6300, 2700]
    plants = ["Planta A", "Planta B", "Planta C"]
    customers = ["Fabr. I", "Fabr. II", "Fabr. III", "Fabr. IV"]

    c = [costs[i][j] for i in range(3) for j in range(4)]
    a_ub = []
    b_ub = []
    for i in range(3):
        row = [0] * 12
        for j in range(4):
            row[i * 4 + j] = 1
        a_ub.append(row)
        b_ub.append(capacities[i])
    a_eq = []
    b_eq = []
    for j in range(4):
        row = [0] * 12
        for i in range(3):
            row[i * 4 + j] = 1
        a_eq.append(row)
        b_eq.append(demands[j])

    result = linprog(c, A_ub=a_ub, b_ub=b_ub, A_eq=a_eq, b_eq=b_eq, bounds=[(0, None)] * 12, method="highs")
    x = result.x

    rows = route_rows(x, costs, plants, customers, cost_decimals=2, total_decimals=2)
    usage_rows = [
        [plants[i], fmt_int(sum(x[i * 4 + j] for j in range(4))), fmt_int(capacities[i]), f"{sum(x[i * 4 + j] for j in range(4)) / capacities[i] * 100:.0f}%"]
        for i in range(3)
    ]
    demand_rows = [
        [customers[j], fmt_int(sum(x[i * 4 + j] for i in range(3))), fmt_int(demands[j]), "100%"]
        for j in range(4)
    ]

    return {
        "anchor": "pbp1",
        "eyebrow": "Programación binaria · Transporte",
        "title": "Semiconductores",
        "subtitle": "Costo total combinado de producción y envío.",
        "description": "Tres plantas abastecen cuatro fabricantes de TV. El panel muestra el costo total por módulo y la distribución óptima.",
        "accent": "#f97316",
        "accent_soft": "rgba(249, 115, 22, 0.14)",
        "objective_label": "Costo mínimo total",
        "objective_value": fmt_currency(result.fun, 2),
        "solver_message": result.message,
        "metrics": [
            {"label": "Estado", "value": "Óptimo"},
            {"label": "Plantas", "value": "3"},
            {"label": "Destinos", "value": "4"},
        ],
        "notes": ["El costo unitario total ya incluye producción + envío."],
        "tables": [
            {"title": "Matriz de asignación", "headers": ["Ruta", "Módulos", "Costo/u", "Costo parcial"], "rows": rows},
            {"title": "Uso de capacidades", "headers": ["Planta", "Enviado", "Capacidad", "Uso"], "rows": usage_rows},
            {"title": "Cobertura de demanda", "headers": ["Fabricante", "Recibido", "Demanda", "Cumplimiento"], "rows": demand_rows},
        ],
    }


def solve_problem_6() -> dict[str, Any]:
    times = [
        [145, 122, 130, 95, 115],
        [80, 63, 85, 48, 78],
        [121, 107, 93, 69, 95],
        [118, 83, 116, 80, 105],
        [97, 75, 120, 80, 111],
    ]
    n = 5
    c = np.array([times[i][j] for i in range(n) for j in range(n)], dtype=float)

    eq_rows = []
    eq_rhs = []
    for i in range(n):
        row = [0] * (n * n)
        for j in range(n):
            row[i * n + j] = 1
        eq_rows.append(row)
        eq_rhs.append(1)
    for j in range(n):
        row = [0] * (n * n)
        for i in range(n):
            row[i * n + j] = 1
        eq_rows.append(row)
        eq_rhs.append(1)

    result = milp(
        c,
        constraints=LinearConstraint(np.array(eq_rows, dtype=float), np.array(eq_rhs, dtype=float), np.array(eq_rhs, dtype=float)),
        integrality=np.ones(n * n),
        bounds=Bounds(lb=0, ub=1),
    )
    x = np.round(result.x).astype(int)

    assignment_rows = []
    matrix = []
    for i in range(n):
        matrix_row = []
        for j in range(n):
            matrix_row.append(str(x[i * n + j]))
            if x[i * n + j] == 1:
                assignment_rows.append([f"Programador {i + 1}", f"Desarrollo {j + 1}", f"{times[i][j]} horas"])
        matrix.append(matrix_row)

    return {
        "anchor": "pbp2",
        "eyebrow": "Programación binaria · Asignación",
        "title": "Asignación de Programadores",
        "subtitle": "Cada programador obtiene exactamente un desarrollo, minimizando el tiempo total.",
        "description": "Se resuelve con variables binarias y restricciones de asignación uno a uno mediante MILP.",
        "accent": "#a855f7",
        "accent_soft": "rgba(168, 85, 247, 0.14)",
        "objective_label": "Tiempo mínimo total",
        "objective_value": f"{result.fun:.0f} horas",
        "solver_message": result.message,
        "metrics": [
            {"label": "Estado", "value": "Óptimo"},
            {"label": "Programadores", "value": "5"},
            {"label": "Desarrollos", "value": "5"},
        ],
        "notes": ["La matriz final es binaria: 1 indica asignación activa."],
        "tables": [
            {"title": "Asignaciones activas", "headers": ["Programador", "Desarrollo", "Tiempo"], "rows": assignment_rows},
            {"title": "Matriz de asignación", "headers": [" ", "Des.1", "Des.2", "Des.3", "Des.4", "Des.5"], "rows": matrix_rows(matrix, [f"Prog. {i + 1}" for i in range(n)], [f"Des. {j + 1}" for j in range(n)])},
        ],
    }


def solve_problem_7() -> dict[str, Any]:
    costs = [[92, 89, 90], [91, 91, 95], [87, 90, 92]]
    capacities = [320, 270, 190]
    demands = [100, 180, 350]
    suppliers = ["Proveedor 1", "Proveedor 2", "Proveedor 3"]
    branches = ["Sucursal 1", "Sucursal 2", "Sucursal 3"]

    c = [costs[i][j] for i in range(3) for j in range(3)]
    a_ub = []
    b_ub = []
    for i in range(3):
        row = [0] * 9
        for j in range(3):
            row[i * 3 + j] = 1
        a_ub.append(row)
        b_ub.append(capacities[i])
    a_eq = []
    b_eq = []
    for j in range(3):
        row = [0] * 9
        for i in range(3):
            row[i * 3 + j] = 1
        a_eq.append(row)
        b_eq.append(demands[j])

    result = linprog(c, A_ub=a_ub, b_ub=b_ub, A_eq=a_eq, b_eq=b_eq, bounds=[(0, None)] * 9, method="highs")
    x = result.x

    rows = route_rows(x, costs, suppliers, branches)
    capacity_rows = [
        [suppliers[i], fmt_int(sum(x[i * 3 + j] for j in range(3))), fmt_int(capacities[i]), f"{sum(x[i * 3 + j] for j in range(3)) / capacities[i] * 100:.0f}%"]
        for i in range(3)
    ]
    demand_rows = [
        [branches[j], fmt_int(sum(x[i * 3 + j] for i in range(3))), fmt_int(demands[j]), "100%"]
        for j in range(3)
    ]

    return {
        "anchor": "pbp3",
        "eyebrow": "Programación binaria · Transporte",
        "title": "Compra de Software",
        "subtitle": "Selección de proveedores para tres sucursales al menor costo.",
        "description": "El modelo distribuye aplicaciones entre tres proveedores y tres sucursales respetando capacidades y demandas exactas.",
        "accent": "#22c55e",
        "accent_soft": "rgba(34, 197, 94, 0.14)",
        "objective_label": "Costo mínimo total",
        "objective_value": fmt_currency(result.fun),
        "solver_message": result.message,
        "metrics": [
            {"label": "Estado", "value": "Óptimo"},
            {"label": "Proveedores", "value": "3"},
            {"label": "Sucursales", "value": "3"},
        ],
        "notes": ["Se obtiene una distribución exacta por sucursal con costo mínimo."],
        "tables": [
            {"title": "Rutas activas", "headers": ["Ruta", "Aplicaciones", "Precio/u", "Costo parcial"], "rows": rows},
            {"title": "Capacidad usada", "headers": ["Proveedor", "Enviado", "Capacidad", "Uso"], "rows": capacity_rows},
            {"title": "Demanda cubierta", "headers": ["Sucursal", "Recibido", "Demanda", "Cumplimiento"], "rows": demand_rows},
        ],
    }


def solve_problem_8() -> dict[str, Any]:
    prod_cost = [23, 25]
    prices = [39, 37, 40, 36]
    shipping = [[6, 8, 11, 9], [12, 6, 8, 5]]
    capacities = [2500, 2100]
    demand_max = [1800, 2300, 550, 1750]
    plants = ["Planta A", "Planta B"]
    chains = ["Cadena 1", "Cadena 2", "Cadena 3", "Cadena 4"]

    profit = []
    profit_matrix = []
    for i in range(2):
        row = []
        for j in range(4):
            gain = prices[j] - prod_cost[i] - shipping[i][j]
            profit.append(gain)
            row.append(gain)
        profit_matrix.append(row)

    c = [-value for value in profit]
    a_ub = [
        [1, 1, 1, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 1, 1, 1],
        [1, 0, 0, 0, 1, 0, 0, 0],
        [0, 1, 0, 0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0, 0, 1, 0],
        [0, 0, 0, 1, 0, 0, 0, 1],
    ]
    b_ub = [2500, 2100, 1800, 2300, 550, 1750]

    result = linprog(c, A_ub=a_ub, b_ub=b_ub, bounds=[(0, None)] * 8, method="highs")
    x = result.x

    rows = route_rows(x, profit_matrix, plants, chains, total_decimals=0, cost_suffix="¢", total_suffix="¢")
    capacity_rows = [
        [plants[i], fmt_int(sum(x[i * 4 + j] for j in range(4))), fmt_int(capacities[i]), f"{sum(x[i * 4 + j] for j in range(4)) / capacities[i] * 100:.0f}%"]
        for i in range(2)
    ]
    demand_rows = [
        [chains[j], fmt_int(sum(x[i * 4 + j] for i in range(2))), fmt_int(demand_max[j]), f"≤ {fmt_int(demand_max[j])}"]
        for j in range(4)
    ]

    return {
        "anchor": "pbp4",
        "eyebrow": "Programación binaria · Maximización",
        "title": "Panificadora: maximizar ganancia",
        "subtitle": "El panel muestra el margen neto por hogaza y la asignación que maximiza la utilidad.",
        "description": "La función objetivo se transforma en minimización de la ganancia negativa. El resultado final expresa la utilidad máxima en centavos y dólares.",
        "accent": "#ef4444",
        "accent_soft": "rgba(239, 68, 68, 0.14)",
        "objective_label": "Ganancia máxima",
        "objective_value": f"{fmt_int(-result.fun)}¢  ·  {fmt_currency(-result.fun / 100, 2)}",
        "solver_message": result.message,
        "metrics": [
            {"label": "Estado", "value": "Óptimo"},
            {"label": "Capacidad total", "value": fmt_int(sum(capacities))},
            {"label": "Demanda máxima", "value": fmt_int(sum(demand_max))},
        ],
        "notes": ["Las cadenas funcionan como topes máximos de envío, no como obligaciones exactas."],
        "tables": [
            {"title": "Ganancia neta por hogaza", "headers": [" ", "C1", "C2", "C3", "C4"], "rows": matrix_rows(profit_matrix, ["Planta A", "Planta B"], chains, lambda value: f"{value}¢")},
            {"title": "Rutas activas", "headers": ["Ruta", "Hogazas", "Ganancia/u", "Ganancia parcial"], "rows": rows},
            {"title": "Uso de capacidades", "headers": ["Planta", "Enviado", "Capacidad", "Uso"], "rows": capacity_rows},
            {"title": "Topes por cadena", "headers": ["Cadena", "Recibido", "Máximo", "Chequeo"], "rows": demand_rows},
        ],
    }


def solve_problem_9() -> dict[str, Any]:
    costs = [[3, 3, 6], [1, 4, 7]]
    capacities = [1.1, 0.9]
    minimums = [0.325, 0.260, 0.195]
    maximums = [1.075, 1.060, 0.845]
    companies = ["Compañía 1", "Compañía 2"]
    cities = ["Ciudad 1", "Ciudad 2", "Ciudad 3"]

    c = [costs[i][j] for i in range(2) for j in range(3)]
    a_ub = [[1, 1, 1, 0, 0, 0], [0, 0, 0, 1, 1, 1]]
    b_ub = capacities[:]

    for j in range(3):
        row = [0] * 6
        row[j] = -1
        row[3 + j] = -1
        a_ub.append(row)
        b_ub.append(-minimums[j])

    for j in range(3):
        row = [0] * 6
        row[j] = 1
        row[3 + j] = 1
        a_ub.append(row)
        b_ub.append(maximums[j])

    result = linprog(c, A_ub=a_ub, b_ub=b_ub, bounds=[(0, None)] * 6, method="highs")
    x = result.x

    rows = route_rows(x, costs, companies, cities, threshold=0.001, value_decimals=3, cost_decimals=0, total_decimals=3, value_suffix=" M dosis", cost_suffix="¢/dosis")
    verification_rows = [
        [cities[j], f"{sum(x[i * 3 + j] for i in range(2)):.3f} M", f"{minimums[j]:.3f} M", f"≤ {maximums[j]:.3f} M"]
        for j in range(3)
    ]

    costo_dolares = result.fun * 1_000_000 / 100

    return {
        "anchor": "pbp5",
        "eyebrow": "Programación binaria · Vacunas",
        "title": "Distribución de Vacunas COVIG-19",
        "subtitle": "Cobertura mínima para ancianos con restricciones de capacidad y costo reducido.",
        "description": "Dos compañías farmacéuticas distribuyen dosis a tres ciudades. El modelo garantiza el mínimo para ancianos y respeta los topes máximos de cada ciudad.",
        "accent": "#06b6d4",
        "accent_soft": "rgba(6, 182, 212, 0.14)",
        "objective_label": "Costo mínimo",
        "objective_value": f"{result.fun:.4f} M·¢  ·  {fmt_currency(costo_dolares, 2)}",
        "solver_message": result.message,
        "metrics": [
            {"label": "Estado", "value": "Óptimo"},
            {"label": "Empresas", "value": "2"},
            {"label": "Ciudades", "value": "3"},
        ],
        "notes": ["Se muestran dosis en millones para mantener la lectura clara del modelo."],
        "tables": [
            {"title": "Rutas activas", "headers": ["Ruta", "Dosis", "Costo envío"], "rows": [[row[0], row[1], row[2]] for row in rows]},
            {"title": "Verificación por ciudad", "headers": ["Ciudad", "Recibido", "Mínimo ancianos", "Máximo ciudad"], "rows": verification_rows},
        ],
    }


PROBLEMS = [
    solve_problem_1(),
    solve_problem_3(),
    solve_problem_4(),
    solve_problem_5(),
    solve_problem_6(),
    solve_problem_7(),
    solve_problem_8(),
    solve_problem_9(),
]


TEMPLATE = """
<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Operativa · Panel de soluciones</title>
  <style>
    :root {
      --bg: #07111f;
      --bg-soft: rgba(10, 18, 34, 0.82);
      --panel: rgba(9, 16, 31, 0.72);
      --panel-strong: rgba(13, 21, 40, 0.92);
      --line: rgba(255, 255, 255, 0.08);
      --text: #edf2ff;
      --muted: rgba(237, 242, 255, 0.72);
      --soft: rgba(237, 242, 255, 0.08);
      --shadow: 0 24px 80px rgba(0, 0, 0, 0.34);
      --radius: 24px;
      --radius-sm: 16px;
    }

    * { box-sizing: border-box; }

    html { scroll-behavior: smooth; }

    body {
      margin: 0;
      min-height: 100vh;
      color: var(--text);
      background:
        radial-gradient(circle at top left, rgba(249, 115, 22, 0.20), transparent 24%),
        radial-gradient(circle at 80% 10%, rgba(56, 189, 248, 0.14), transparent 28%),
        radial-gradient(circle at 80% 70%, rgba(168, 85, 247, 0.12), transparent 24%),
        linear-gradient(180deg, #050816 0%, #07111f 55%, #060b16 100%);
      font-family: "Aptos", "Segoe UI Variable Text", "Trebuchet MS", sans-serif;
      line-height: 1.45;
    }

    .wrap {
      width: min(1500px, calc(100vw - 32px));
      margin: 0 auto;
      padding: 28px 0 60px;
    }

    .hero {
      display: grid;
      grid-template-columns: minmax(0, 1.6fr) minmax(320px, 0.9fr);
      gap: 20px;
      align-items: stretch;
      margin-bottom: 22px;
    }

    .hero-card,
    .aside-card,
    .section,
    .metric,
    .table-card,
    .note {
      background: linear-gradient(180deg, rgba(255,255,255,0.08), rgba(255,255,255,0.03));
      border: 1px solid var(--line);
      box-shadow: var(--shadow);
      backdrop-filter: blur(18px);
    }

    .hero-card {
      border-radius: 34px;
      padding: 32px;
      position: relative;
      overflow: hidden;
      isolation: isolate;
    }

    .hero-card::before {
      content: "";
      position: absolute;
      inset: -20% -10% auto auto;
      width: 360px;
      height: 360px;
      border-radius: 50%;
      background: radial-gradient(circle, rgba(249,115,22,0.30), transparent 65%);
      filter: blur(16px);
      z-index: -1;
    }

    .eyebrow {
      margin: 0 0 12px;
      text-transform: uppercase;
      letter-spacing: 0.18em;
      color: rgba(237,242,255,0.64);
      font-size: 0.76rem;
      font-weight: 700;
    }

    h1 {
      margin: 0;
      font-size: clamp(2rem, 4vw, 4.2rem);
      line-height: 0.98;
      letter-spacing: -0.05em;
    }

    .hero-copy {
      max-width: 62ch;
      margin: 18px 0 0;
      color: var(--muted);
      font-size: 1.02rem;
    }

    .hero-badges {
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      margin-top: 20px;
    }

    .badge {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 10px 14px;
      border-radius: 999px;
      background: rgba(255,255,255,0.06);
      border: 1px solid rgba(255,255,255,0.08);
      color: var(--text);
      font-size: 0.92rem;
      font-weight: 600;
    }

    .badge-dot {
      width: 10px;
      height: 10px;
      border-radius: 999px;
      background: var(--accent, #38bdf8);
      box-shadow: 0 0 18px var(--accent, #38bdf8);
    }

    .aside-card {
      border-radius: 30px;
      padding: 22px;
      display: grid;
      gap: 14px;
    }

    .summary-grid {
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 12px;
    }

    .summary {
      padding: 16px;
      border-radius: 20px;
      background: rgba(255,255,255,0.05);
      border: 1px solid rgba(255,255,255,0.06);
    }

    .summary span {
      display: block;
      color: var(--muted);
      font-size: 0.82rem;
      margin-bottom: 6px;
    }

    .summary strong {
      display: block;
      font-size: 1.3rem;
      letter-spacing: -0.03em;
    }

    .toc {
      display: grid;
      gap: 8px;
    }

    .toc a {
      text-decoration: none;
      color: var(--text);
      border: 1px solid rgba(255,255,255,0.08);
      background: rgba(255,255,255,0.04);
      padding: 12px 14px;
      border-radius: 16px;
      transition: transform 180ms ease, border-color 180ms ease, background 180ms ease;
    }

    .toc a:hover {
      transform: translateY(-1px);
      border-color: rgba(255,255,255,0.18);
      background: rgba(255,255,255,0.08);
    }

    .sections {
      display: grid;
      gap: 18px;
    }

    .section {
      border-radius: 30px;
      padding: 22px;
      position: relative;
      overflow: hidden;
      animation: floatIn 720ms ease both;
    }

    .section::before {
      content: "";
      position: absolute;
      inset: 0 0 auto 0;
      height: 4px;
      background: linear-gradient(90deg, var(--accent), transparent 82%);
      opacity: 0.85;
    }

    .section-head {
      display: grid;
      grid-template-columns: minmax(0, 1.25fr) minmax(300px, 0.8fr);
      gap: 16px;
      align-items: start;
      margin-bottom: 18px;
    }

    .section h2 {
      margin: 0;
      font-size: clamp(1.35rem, 2vw, 2rem);
      letter-spacing: -0.04em;
    }

    .section .subtitle {
      margin: 8px 0 0;
      color: var(--text);
      font-weight: 600;
    }

    .section .desc {
      margin: 10px 0 0;
      color: var(--muted);
      max-width: 75ch;
    }

    .objective {
      padding: 18px;
      border-radius: 22px;
      background: linear-gradient(180deg, rgba(255,255,255,0.09), rgba(255,255,255,0.04));
      border: 1px solid rgba(255,255,255,0.08);
    }

    .objective small {
      display: block;
      color: var(--muted);
      font-size: 0.8rem;
      text-transform: uppercase;
      letter-spacing: 0.12em;
      margin-bottom: 10px;
    }

    .objective strong {
      display: block;
      font-size: 1.7rem;
      letter-spacing: -0.04em;
      line-height: 1.05;
    }

    .objective p {
      margin: 8px 0 0;
      color: var(--muted);
      font-size: 0.92rem;
    }

    .metric-row {
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 12px;
      margin: 18px 0;
    }

    .metric {
      border-radius: 20px;
      padding: 16px;
      background: rgba(255,255,255,0.05);
    }

    .metric span {
      display: block;
      color: var(--muted);
      font-size: 0.8rem;
      margin-bottom: 7px;
      text-transform: uppercase;
      letter-spacing: 0.1em;
    }

    .metric strong {
      display: block;
      font-size: 1.35rem;
      letter-spacing: -0.04em;
    }

    .note {
      border-radius: 18px;
      padding: 14px 16px;
      color: var(--text);
      margin: 12px 0 18px;
      background: rgba(255,255,255,0.05);
    }

    .table-card {
      border-radius: 24px;
      padding: 16px;
      margin-top: 14px;
      background: rgba(255,255,255,0.04);
    }

    .table-card h3 {
      margin: 0 0 12px;
      font-size: 1rem;
      letter-spacing: -0.02em;
    }

    .table-wrap {
      overflow: auto;
      border-radius: 18px;
      border: 1px solid rgba(255,255,255,0.08);
      background: rgba(4, 9, 18, 0.45);
    }

    table {
      width: 100%;
      border-collapse: collapse;
      min-width: 640px;
    }

    thead th {
      background: rgba(255,255,255,0.08);
      color: var(--text);
      text-align: left;
      font-size: 0.82rem;
      text-transform: uppercase;
      letter-spacing: 0.1em;
      padding: 14px 16px;
      position: sticky;
      top: 0;
      backdrop-filter: blur(12px);
    }

    tbody td {
      padding: 13px 16px;
      border-top: 1px solid rgba(255,255,255,0.06);
      color: var(--text);
      white-space: nowrap;
    }

    tbody tr:nth-child(2n) td {
      background: rgba(255,255,255,0.02);
    }

    .footer {
      margin-top: 22px;
      color: rgba(237,242,255,0.65);
      font-size: 0.9rem;
      text-align: center;
    }

    @keyframes floatIn {
      from { opacity: 0; transform: translateY(12px) scale(0.99); }
      to { opacity: 1; transform: translateY(0) scale(1); }
    }

    @media (max-width: 1100px) {
      .hero,
      .section-head {
        grid-template-columns: 1fr;
      }

      .metric-row,
      .summary-grid {
        grid-template-columns: 1fr;
      }
    }

    @media (max-width: 720px) {
      .wrap { width: min(100vw - 20px, 100%); padding-top: 14px; }
      .hero-card, .aside-card, .section { border-radius: 24px; }
      .section, .hero-card { padding: 18px; }
      .badge { width: 100%; justify-content: center; }
    }
  </style>
</head>
<body>
  <div class="wrap">
    <section class="hero">
      <div class="hero-card" style="--accent: #f59e0b;">
        <p class="eyebrow">Investigación de Operaciones · Operativa</p>
        <h1>Panel visual de resultados</h1>
        <p class="hero-copy">
          Una interfaz única y limpia para todos los modelos del ejercicio: transporte, producción, asignación y optimización binaria, con resultados destacados en tarjetas, tablas y métricas legibles.
        </p>
        <div class="hero-badges">
          <div class="badge"><span class="badge-dot"></span>{{ problems|length }} problemas resueltos</div>
          <div class="badge"><span class="badge-dot"></span>SciPy HiGHS + MILP</div>
          <div class="badge"><span class="badge-dot"></span>Visualización responsive</div>
        </div>
      </div>

      <aside class="aside-card">
        <div class="summary-grid">
          <div class="summary">
            <span>Estado general</span>
            <strong>Óptimo</strong>
          </div>
          <div class="summary">
            <span>Modelos</span>
            <strong>{{ problems|length }}</strong>
          </div>
          <div class="summary">
            <span>Última ejecución</span>
            <strong>{{ generated_at }}</strong>
          </div>
          <div class="summary">
            <span>Interfaz</span>
            <strong>Flask</strong>
          </div>
        </div>

        <div class="toc">
          {% for section in problems %}
          <a href="#{{ section.anchor }}">{{ section.title }}</a>
          {% endfor %}
        </div>
      </aside>
    </section>

    <main class="sections">
      {% for section in problems %}
      <article class="section" id="{{ section.anchor }}" style="--accent: {{ section.accent }}; --accent-soft: {{ section.accent_soft }}; animation-delay: {{ loop.index0 * 70 }}ms;">
        <div class="section-head">
          <div>
            <p class="eyebrow" style="color: {{ section.accent }};">{{ section.eyebrow }}</p>
            <h2>{{ section.title }}</h2>
            <p class="subtitle">{{ section.subtitle }}</p>
            <p class="desc">{{ section.description }}</p>
          </div>
          <div class="objective">
            <small>{{ section.objective_label }}</small>
            <strong>{{ section.objective_value }}</strong>
            <p>{{ section.solver_message }}</p>
          </div>
        </div>

        <div class="metric-row">
          {% for metric in section.metrics %}
          <div class="metric">
            <span>{{ metric.label }}</span>
            <strong>{{ metric.value }}</strong>
          </div>
          {% endfor %}
        </div>

        {% for note in section.notes %}
        <div class="note">{{ note }}</div>
        {% endfor %}

        {% for table in section.tables %}
        <div class="table-card">
          <h3>{{ table.title }}</h3>
          <div class="table-wrap">
            <table>
              <thead>
                <tr>
                  {% for header in table.headers %}
                  <th>{{ header }}</th>
                  {% endfor %}
                </tr>
              </thead>
              <tbody>
                {% for row in table.rows %}
                <tr>
                  {% for cell in row %}
                  <td>{{ cell }}</td>
                  {% endfor %}
                </tr>
                {% endfor %}
              </tbody>
            </table>
          </div>
        </div>
        {% endfor %}
      </article>
      {% endfor %}
    </main>

    <div class="footer">
      Generado localmente con Python, Flask y SciPy. Ejecuta <strong>Solucion.py</strong> para abrir este panel.
    </div>
  </div>
</body>
</html>
"""


def create_app() -> Flask:
    app = Flask(__name__)

    @app.route("/")
    def index() -> str:
        return render_template_string(
            TEMPLATE,
            problems=PROBLEMS,
            generated_at=datetime.now().strftime("%d/%m/%Y %H:%M"),
        )

    return app


app = create_app()


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
