from flask import Flask, request, jsonify, render_template

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    exercises = [
        {
            "id": 1,
            "title": "Tres Compañías de Pasta Dental",
            "url": "/taller1-markov/ex1",
            "active": True,
        },
        {
            "id": 2,
            "title": "Industria de Bebidas de Cola",
            "url": "/taller1-markov/ex2",
            "active": True,
        },
        {
            "id": 3,
            "title": "¿Contratar la Agencia Publicitaria?",
            "url": "/taller1-markov/ex3",
            "active": True,
        },
        {
            "id": 4,
            "title": "Inventario de Vehículos (s=3, S=6)",
            "url": "/taller1-markov/ex4",
            "active": True,
        },
        {
            "id": 5,
            "title": "Industria del Café en Bogotá (5 Marcas)",
            "url": "/taller1-markov/ex5",
            "active": True,
        },
        {
            "id": 6,
            "title": "Movilidad Social (Padre → Hijo)",
            "url": "/taller1-markov/ex6",
            "active": True,
        },
    ]
    return render_template("index.html", exercises=exercises)


@app.route("/taller1-markov/ex1", methods=["GET"])
def get_exercise_1():
    response = {
        "problem": "Tres Compañías de Pasta Dental",
        "initial_state": {"C1": 0.40, "C2": 0.20, "C3": 0.40},
        "step_1": {
            "title": "Matriz de Transición P",
            "description": "Construcción de la matriz P (filas = destino, columnas = origen).",
            "matrix_standard": [
                [0.85, 0.15, 0.10],
                [0.10, 0.75, 0.10],
                [0.05, 0.10, 0.80],
            ],
            "note": "Se redistribuye el 5% restante de C2 a C3 para garantizar la matriz estocástica por columnas.",
        },
        "step_2": {
            "title": "Distribución Estacionaria (Largo Plazo) L",
            "description": "Se busca el vector pi tal que P * pi = pi, con suma de pi igual a 1.",
            "equations": [
                "pi1 = 0.85*pi1 + 0.15*pi2 + 0.10*pi3",
                "pi2 = 0.10*pi1 + 0.75*pi2 + 0.10*pi3",
                "pi3 = 0.05*pi1 + 0.10*pi2 + 0.80*pi3",
                "pi1 + pi2 + pi3 = 1",
            ],
            "calculations": [
                "De (1): 0.15*pi1 - 0.15*pi2 = 0.10*pi3  =>  pi3 = 1.5*pi1 - 1.5*pi2",
                "De (2): 0.25*pi2 = 0.10*pi1 + 0.10(1.5*pi1 - 1.5*pi2)  =>  0.40*pi2 = 0.25*pi1  =>  pi2 = 0.625*pi1",
                "Sustituyendo: pi3 = 1.5*pi1 - 1.5(0.625*pi1) = 0.5625*pi1",
                "Normalización: pi1 + 0.625*pi1 + 0.5625*pi1 = 1  =>  2.1875*pi1 = 1",
                "Resolviendo: pi1 = 0.4571",
            ],
            "results": {"pi1": 0.4571, "pi2": 0.2857, "pi3": 0.2571},
        },
        "step_3": {
            "title": "Decisiones Estratégicas",
            "analysis": {
                "C1": {
                    "initial": "40%",
                    "long_term": "45.71%",
                    "variation": "+5.71%",
                    "status": "Ganadora",
                },
                "C2": {
                    "initial": "20%",
                    "long_term": "28.57%",
                    "variation": "+8.57%",
                    "status": "Mayor ganancia relativa",
                },
                "C3": {
                    "initial": "40%",
                    "long_term": "25.71%",
                    "variation": "-14.29%",
                    "status": "Perdedora",
                },
            },
            "recommendations": [
                "C1 y C2: Mantener la estrategia actual, ambas crecen en participación.",
                "C3: Revisar urgentemente su estrategia de retención. Debe invertir en fidelización.",
            ],
        },
    }
    return render_template("ex1.html", data=response)


@app.route("/taller1-markov/ex2", methods=["GET"])
def get_exercise_2():
    response = {
        "problem": "Problema 2: Industria de Bebidas de Cola",
        "steps": [
            {
                "title": "a) Matriz de Transición P",
                "matrix": {
                    "headers": ["Cola 1", "Cola 2"],
                    "row_headers": ["Cola 1", "Cola 2"],
                    "rows": [[0.90, 0.20], [0.10, 0.80]],
                },
            },
            {
                "title": "b) Distribución Estacionaria",
                "equations": [
                    "π1 = 0.90*π1 + 0.20*π2",
                    "π2 = 0.10*π1 + 0.80*π2",
                    "π1 + π2 = 1",
                ],
                "calculations": [
                    "De (1): 0.10*π1 = 0.20*π2  =>  π1 = 2*π2",
                    "Sustituyendo en (3): 2*π2 + π2 = 1  =>  3*π2 = 1  =>  π2 = 1/3 (≈33.33%)",
                    "Por lo tanto: π1 = 2*(1/3) = 2/3 (≈66.67%)",
                ],
                "results": {"Cola 1": "66.67% (Mejor Posicionada)", "Cola 2": "33.33%"},
            },
            {
                "title": "c) Matriz P^2 (Prob. a 2 pasos)",
                "matrix": {
                    "headers": ["Cola 1", "Cola 2"],
                    "row_headers": ["Cola 1", "Cola 2"],
                    "rows": [[0.82, 0.34], [0.18, 0.66]],
                },
                "calculations": [
                    "P^2[C1,C2] = P[C1,C1] * P[C1,C2] + P[C1,C2] * P[C2,C2]",
                    "= (0.90 * 0.20) + (0.20 * 0.80) = 0.18 + 0.16 = 0.34",
                ],
                "note": "Probabilidad de comprar Cola 1 dos veces dado que hoy compra Cola 2 es 34%.",
            },
            {
                "title": "d) Probabilidad a 3 pasos",
                "description": "La probabilidad de que alguien que hoy compra Cola 1 siga comprando Cola 1 en las próximas 3 compras es P^3[C1|C1].",
                "calculations": [
                    "P^3[C1,C1] = P^2[C1,C1] * P[C1,C1] + P^2[C1,C2] * P[C2,C1]",
                    "= (0.82 * 0.90) + (0.34 * 0.20) = 0.738 + 0.068 = 0.806",
                ],
                "results": {"P^3[C1,C1]": "80.6%"},
            },
        ],
    }
    return render_template("generic_ex.html", data=response)


@app.route("/taller1-markov/ex3", methods=["GET"])
def get_exercise_3():
    response = {
        "problem": "Problema 3: ¿Contratar la Agencia Publicitaria?",
        "steps": [
            {
                "title": "Análisis y Comparación de Ganancias",
                "calculations": [
                    "SIN AGENCIA: Clientes Cola 1 = 100M × (2/3) = 66.67 millones",
                    "SIN AGENCIA: Ganancia anual C1 = 66.67M × $52 = $3,466.67 millones",
                    "CON AGENCIA: Nuevo estado estacionario => 0.05*π1 = 0.20*π2 => π1 = 4*π2 => π1 = 0.80 (80%)",
                    "CON AGENCIA: Clientes Cola 1 = 100M × 0.80 = 80 millones",
                    "CON AGENCIA: Ganancia bruta = 80M × $52 = $4,160 millones",
                    "CON AGENCIA: Ganancia neta = $4,160M - $500M (Costo agencia) = $3,660 millones",
                ],
                "table": {
                    "headers": [
                        "Escenario",
                        "Clientes C1",
                        "Ingreso Bruto",
                        "Costo Agencia",
                        "Ganancia Neta",
                    ],
                    "rows": [
                        ["Sin agencia", "66.67M", "$3,466.67M", "$0", "$3,466.67M"],
                        ["Con agencia", "80.00M", "$4,160.00M", "$500M", "$3,660.00M"],
                        ["Diferencia", "+13.33M", "+$693.33M", "-$500M", "+$193.33M"],
                    ],
                },
                "note": "SÍ se debe contratar la agencia. Ganancia adicional neta de $193.33 millones.",
            }
        ],
    }
    return render_template("generic_ex.html", data=response)


@app.route("/taller1-markov/ex4", methods=["GET"])
def get_exercise_4():
    response = {
        "problem": "Problema 4: Inventario de Vehículos (s=3, S=6)",
        "steps": [
            {
                "title": "a) Probabilidades de Demanda (Poisson)",
                "equations": [
                    "Fórmula Poisson: P(D=x) = (e^-λ * λ^x) / x!",
                    "Dado λ=4 vehículos por semana:",
                ],
                "calculations": [
                    "P(D=0) = e^-4 * 4^0 / 0! = 0.0183",
                    "P(D=1) = e^-4 * 4^1 / 1! = 0.0733",
                    "P(D=2) = e^-4 * 4^2 / 2! = 0.1465",
                    "P(D=3) = e^-4 * 4^3 / 3! = 0.1954",
                    "P(D≥4) = 1 - P(D≤3) = 0.5665",
                ],
            },
            {
                "title": "b) Matriz de Transición P",
                "matrix": {
                    "headers": ["6", "5", "4", "3"],
                    "row_headers": ["6", "5", "4", "3"],
                    "rows": [
                        [0.7802, 0.8042, 0.9817, 1.0000],
                        [0.0733, 0.0183, 0.0000, 0.0000],
                        [0.1465, 0.0733, 0.0183, 0.0000],
                        [0.0000, 0.0000, 0.0000, 0.0000],
                    ],
                },
            },
            {
                "title": "c) Distribución Estacionaria L",
                "results": {"π_6": "81.33%", "π_5": "6.08%", "π_4": "12.59%"},
            },
        ],
    }
    return render_template("generic_ex.html", data=response)


@app.route("/taller1-markov/ex5", methods=["GET"])
def get_exercise_5():
    response = {
        "problem": "Problema 5: Industria del Café en Bogotá",
        "steps": [
            {
                "title": "Distribución Estacionaria y Decisión",
                "description": "Comparación del estado estacionario y decisión respecto a la agencia.",
                "calculations": [
                    "Mercado total: 60,000 kg/mes. Beneficio = $1/kg",
                    "Ganancia Original B1 = (60,000 * 0.2480) * 12 meses * $1 = $178,560",
                    "Ganancia con Agencia B1 = (60,000 * 0.3200) * 12 meses * $1 = $230,400",
                    "Ganancia adicional bruta = $230,400 - $178,560 = $51,840 / año",
                    "Costo de la agencia = $40,000,000 / año",
                ],
                "results": {
                    "B1 Original": "24.80% (Ganancia: $178,560)",
                    "B1 con Agencia": "32.00% (Ganancia: $230,400)",
                    "Ganancia Adicional": "$51,840",
                    "Costo Agencia": "$40,000,000",
                },
                "note": "CONCLUSIÓN: B1 NO debe contratar la agencia porque el costo supera por mucho el beneficio.",
            }
        ],
    }
    return render_template("generic_ex.html", data=response)


@app.route("/taller1-markov/ex6", methods=["GET"])
def get_exercise_6():
    response = {
        "problem": "Problema 6: Movilidad Social",
        "steps": [
            {
                "title": "Matriz de Transición P (Padre a Hijo)",
                "matrix": {
                    "headers": ["Hijo Alta", "Hijo Media", "Hijo Baja"],
                    "row_headers": ["Padre Alta", "Padre Media", "Padre Baja"],
                    "rows": [
                        [0.448, 0.484, 0.068],
                        [0.054, 0.699, 0.247],
                        [0.011, 0.503, 0.486],
                    ],
                },
            },
            {
                "title": "Distribución Estacionaria",
                "equations": [
                    "π_A = 0.448*π_A + 0.054*π_M + 0.011*π_B",
                    "π_M = 0.484*π_A + 0.699*π_M + 0.503*π_B",
                    "π_B = 0.068*π_A + 0.247*π_M + 0.486*π_B",
                    "π_A + π_M + π_B = 1",
                ],
                "calculations": [
                    "Resolviendo el sistema de ecuaciones lineales se obtiene la proporción de clases a largo plazo:"
                ],
                "results": {
                    "Clase Alta": "6.35%",
                    "Clase Media": "62.34%",
                    "Clase Baja": "31.31%",
                },
                "note": "A largo plazo, el 62% de la población será clase media.",
            },
        ],
    }
    return render_template("generic_ex.html", data=response)


if __name__ == "__main__":
    app.run(debug=True)
