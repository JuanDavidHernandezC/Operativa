from __future__ import annotations

from datetime import datetime
from typing import Any

import numpy as np
from flask import Flask, render_template_string


# ─── helpers ────────────────────────────────────────────────────────────────

def fmt_frac(num: int, den: int) -> str:
    from math import gcd
    g = gcd(abs(num), abs(den))
    n, d = num // g, den // g
    return f"{n}/{d}" if d != 1 else str(n)


def fmt_pct(value: float, decimals: int = 2) -> str:
    return f"{value * 100:.{decimals}f}%"


def fmt_prob(value: float, decimals: int = 5) -> str:
    return f"{value:.{decimals}f}"


def stationary_distribution(P: np.ndarray) -> np.ndarray:
    """Resolve π·P = π con Σπ = 1 via álgebra lineal."""
    n = P.shape[0]
    A = (P.T - np.eye(n))
    A = np.vstack([A, np.ones(n)])
    b = np.zeros(n + 1)
    b[-1] = 1.0
    pi, *_ = np.linalg.lstsq(A, b, rcond=None)
    pi = np.abs(pi)
    pi /= pi.sum()
    return pi


def verify_pi(pi: np.ndarray, P: np.ndarray) -> str:
    result = pi @ P
    ok = np.allclose(result, pi, atol=1e-6)
    return "π·P = π  ✓" if ok else "π·P ≠ π  ✗"


# ─── Problem 1: VoIP ─────────────────────────────────────────────────────────

def solve_problem_1() -> dict[str, Any]:
    states = ["H (Hablando)", "S (Silencio)"]
    P = np.array([
        [99/100,  1/100],
        [1/140,  139/140],
    ])

    pi = stationary_distribution(P)
    check = verify_pi(pi, P)

    matrix_rows = [
        [states[i]] + [fmt_prob(P[i][j], 5) for j in range(2)] + [fmt_prob(P[i].sum(), 3)]
        for i in range(2)
    ]
    pi_rows = [
        [states[i], fmt_frac(5 if i == 0 else 7, 12), fmt_pct(pi[i]), "Genera paquete de voz" if i == 0 else "No genera paquete"]
        for i in range(2)
    ]

    transitions = [
        ["H → H", "99/100 = 0.99000", "Permanece hablando"],
        ["H → S", "1/100 = 0.01000",  "Pasa a silencio"],
        ["S → H", "1/140 ≈ 0.00714",  "Pasa a hablar"],
        ["S → S", "139/140 ≈ 0.99286","Permanece en silencio"],
    ]

    return {
        "anchor": "p1",
        "eyebrow": "Problema 1 · VoIP",
        "title": "Sistema de Paquetes de Voz",
        "subtitle": "Cadena de Márkov de 2 estados: Hablando y Silencio.",
        "description": (
            "Sistema de voz digitalizada con intervalos de 10 ms. "
            "P(H→H) = 99/100, P(H→S) = 1/100, P(S→H) = 1/140. "
            "Se calcula la distribución estacionaria π para determinar el porcentaje del tiempo en cada estado."
        ),
        "accent": "#38bdf8",
        "accent_soft": "rgba(56, 189, 248, 0.14)",
        "objective_label": "Distribución estacionaria",
        "objective_value": f"πH = 5/12 ≈ {pi[0]:.4f}   ·   πS = 7/12 ≈ {pi[1]:.4f}",
        "solver_message": check,
        "metrics": [
            {"label": "Estados", "value": "2"},
            {"label": "% Hablando", "value": fmt_pct(pi[0])},
            {"label": "% Silencio", "value": fmt_pct(pi[1])},
        ],
        "notes": [
            "El hablante pasa el 41.67% del tiempo generando paquetes y el 58.33% en silencio. "
            "Σπ = 1 ✓ — cada fila de P también suma 1 ✓"
        ],
        "tables": [
            {
                "title": "Matriz de transición P",
                "headers": ["Estado \\ Siguiente", "H", "S", "Σ"],
                "rows": matrix_rows,
            },
            {
                "title": "Transiciones activas",
                "headers": ["Transición", "Probabilidad", "Descripción"],
                "rows": transitions,
            },
            {
                "title": "Distribución estacionaria π",
                "headers": ["Estado", "Fracción exacta", "Porcentaje", "Implicación"],
                "rows": pi_rows,
            },
        ],
    }


# ─── Problem 2: Stock ticks ──────────────────────────────────────────────────

def solve_problem_2() -> dict[str, Any]:
    states = ["PAR (=)", "BAJA (↓)", "REPUNTE (↑)"]
    P = np.array([
        [0.6, 0.2, 0.2],
        [0.6, 0.4, 0.0],
        [0.6, 0.0, 0.4],
    ])

    pi = stationary_distribution(P)
    check = verify_pi(pi, P)

    matrix_rows = [
        [states[i]] + [fmt_prob(P[i][j], 3) for j in range(3)] + [fmt_prob(P[i].sum(), 1)]
        for i in range(3)
    ]
    pi_rows = [
        [states[0], "3/5 = 0.60", fmt_pct(pi[0])],
        [states[1], "1/5 = 0.20", fmt_pct(pi[1])],
        [states[2], "1/5 = 0.20", fmt_pct(pi[2])],
    ]
    verify_rows = [
        ["πPAR'",  "0.6(0.6)+0.2(0.6)+0.2(0.6)", "= 0.60", "✓"],
        ["πBAJA'", "0.6(0.2)+0.2(0.4)+0.2(0.0)", "= 0.20", "✓"],
        ["πREP'",  "0.6(0.2)+0.2(0.0)+0.2(0.4)", "= 0.20", "✓"],
    ]

    return {
        "anchor": "p2",
        "eyebrow": "Problema 2 · Acciones",
        "title": "Acciones Bursátiles",
        "subtitle": "Tick PAR / BAJA / REPUNTE — cadena de 3 estados.",
        "description": (
            "Una acción puede estar en tick PAR (=), BAJA (↓) o REPUNTE (↑). "
            "Desde PAR se bifurca simétricamente; BAJA y REPUNTE solo retornan a PAR. "
            "La simetría del modelo produce una distribución estacionaria muy limpia."
        ),
        "accent": "#a855f7",
        "accent_soft": "rgba(168, 85, 247, 0.14)",
        "objective_label": "Distribución estacionaria",
        "objective_value": f"πPAR = 0.60   ·   πBAJA = 0.20   ·   πREP = 0.20",
        "solver_message": check,
        "metrics": [
            {"label": "Estados", "value": "3"},
            {"label": "% PAR",    "value": fmt_pct(pi[0])},
            {"label": "% BAJA / REP.", "value": fmt_pct(pi[1])},
        ],
        "notes": [
            "El tick PAR ocurre el 60% del tiempo. BAJA y REPUNTE son igualmente probables (20% c/u) "
            "por la simetría del modelo: PAR recibe 0.6 desde cualquier estado."
        ],
        "tables": [
            {
                "title": "Matriz de transición P",
                "headers": ["Estado \\ Siguiente", "PAR", "BAJA", "REPUNTE", "Σ"],
                "rows": matrix_rows,
            },
            {
                "title": "Distribución estacionaria π",
                "headers": ["Estado", "Valor exacto", "Porcentaje"],
                "rows": pi_rows,
            },
            {
                "title": "Verificación π·P = π",
                "headers": ["Componente", "Cálculo", "Resultado", "Ok"],
                "rows": verify_rows,
            },
        ],
    }


# ─── Problem 3: Digital phone with timeout ───────────────────────────────────

def solve_problem_3() -> dict[str, Any]:
    states = ["0 (OK)", "E1", "E2", "E3", "E4", "TE"]
    n = 6
    # Columns = current state, rows = next state (transpose convention)
    # Build row-stochastic P (row = current state)
    P = np.array([
        [0.9,  0.9,  0.9,  0.9,  0.9,  0.01],
        [0.1,  0.0,  0.0,  0.0,  0.0,  0.0 ],
        [0.0,  0.1,  0.0,  0.0,  0.0,  0.0 ],
        [0.0,  0.0,  0.1,  0.0,  0.0,  0.0 ],
        [0.0,  0.0,  0.0,  0.1,  0.0,  0.0 ],
        [0.0,  0.0,  0.0,  0.0,  0.1,  0.99],
    ]).T  # Transpose so rows = current state

    pi = stationary_distribution(P)
    check = verify_pi(pi, P)

    # Analytical values
    pi0_analytic = 1 / (1 + 0.1 + 0.01 + 0.001 + 0.0001 + 0.001)
    pi_analytic = [
        pi0_analytic,
        0.1   * pi0_analytic,
        0.01  * pi0_analytic,
        0.001 * pi0_analytic,
        0.0001* pi0_analytic,
        0.001 * pi0_analytic,
    ]

    matrix_rows_data = [
        [states[i]] + [fmt_prob(P[i][j], 2) for j in range(n)] + [fmt_prob(P[i].sum(), 1)]
        for i in range(n)
    ]
    pi_rows = [
        [states[i], f"{pi_analytic[i]:.4f}", fmt_pct(pi_analytic[i], 3)]
        for i in range(n)
    ]

    return {
        "anchor": "p3",
        "eyebrow": "Problema 3 · Teléfono Digital",
        "title": "Teléfono Digital con Tiempo de Espera",
        "subtitle": "6 estados: OK, E1–E4 y Tiempo de Espera (TE).",
        "description": (
            "Intervalo de 20 ms. P(error) = 0.1 por paquete. Tras 5 errores consecutivos el sistema "
            "entra en Tiempo de Espera (TE). Durante TE la recuperación es Bernoulli con p=0.01. "
            "Los estados son {0, E1, E2, E3, E4, TE}."
        ),
        "accent": "#22c55e",
        "accent_soft": "rgba(34, 197, 94, 0.14)",
        "objective_label": "π₀ (estado OK)",
        "objective_value": f"{pi_analytic[0]:.4f}  ≈  89.92%  del tiempo en transmisión normal",
        "solver_message": check,
        "metrics": [
            {"label": "Estados", "value": "6"},
            {"label": "% Tiempo OK",  "value": fmt_pct(pi_analytic[0], 2)},
            {"label": "% Tiempo TE",  "value": fmt_pct(pi_analytic[5], 3)},
        ],
        "notes": [
            "El sistema opera normalmente el 89.92% del tiempo. "
            "Entra en tiempo de espera solo el 0.090% — el mecanismo de 5 errores consecutivos es muy robusto para P(error)=0.1."
        ],
        "tables": [
            {
                "title": "Matriz de transición P (fila = estado actual)",
                "headers": ["Estado \\ Siguiente"] + states + ["Σ"],
                "rows": matrix_rows_data,
            },
            {
                "title": "Distribución estacionaria π",
                "headers": ["Estado", "Probabilidad", "Porcentaje"],
                "rows": pi_rows,
            },
        ],
    }


# ─── Problem 4: Urn (balls) ──────────────────────────────────────────────────

def solve_problem_4() -> dict[str, Any]:
    states = ["SS", "RS", "NS", "RN", "RR", "NN"]
    n = 6
    # Row-stochastic P (row = current state, col = next state)
    P = np.array([
        [0,    1/2,  1/2,  0,    0,   0  ],   # SS
        [0,    0,    1/2,  1/4,  1/4, 0  ],   # RS
        [0,    1/2,  0,    1/4,  0,   1/4],   # NS
        [0,    0,    0,    0,    1/2, 1/2],   # RN
        [0,    0,    0,    1,    0,   0  ],   # RR
        [0,    0,    0,    1,    0,   0  ],   # NN
    ])

    # Recurrent subchain {RN, RR, NN}
    P_rec = np.array([
        [0,   1/2, 1/2],   # RN
        [1,   0,   0  ],   # RR
        [1,   0,   0  ],   # NN
    ])
    pi_rec = stationary_distribution(P_rec)
    check_rec = verify_pi(pi_rec, P_rec)

    pi_full = np.array([0, 0, 0, pi_rec[0], pi_rec[1], pi_rec[2]])
    pi_fracs = ["0", "0", "0", "1/2", "1/4", "1/4"]

    matrix_rows_data = [
        [states[i]] + [fmt_prob(P[i][j], 3) for j in range(n)] + [fmt_prob(P[i].sum(), 1)]
        for i in range(n)
    ]
    pi_rows = [
        [states[i], pi_fracs[i], fmt_pct(pi_full[i]), "Transiente" if i < 3 else "Recurrente ✓"]
        for i in range(n)
    ]
    verify_rows = [
        ["πRN'", "πRR + πNN", "1/4+1/4 = 1/2", "✓"],
        ["πRR'", "(1/2)·πRN", "(1/2)·(1/2) = 1/4", "✓"],
        ["πNN'", "(1/2)·πRN", "(1/2)·(1/2) = 1/4", "✓"],
    ]

    return {
        "anchor": "p4",
        "eyebrow": "Problema 4 · Urna",
        "title": "Urna con Bolas (Roja / Negra / Sin Pintar)",
        "subtitle": "6 estados — 3 transientes + 3 recurrentes.",
        "description": (
            "Urna con 2 bolas. Se selecciona 1 al azar y se lanza una moneda. Si no está pintada: "
            "Cara → Rojo, Sello → Negro. Si ya está pintada: cambia de color. "
            "Los estados SS, RS, NS son transientes; el proceso se absorbe en {RN, RR, NN}."
        ),
        "accent": "#f59e0b",
        "accent_soft": "rgba(245, 158, 11, 0.14)",
        "objective_label": "Distribución estacionaria (estados recurrentes)",
        "objective_value": "πRN = 1/2   ·   πRR = 1/4   ·   πNN = 1/4",
        "solver_message": check_rec,
        "metrics": [
            {"label": "Estados totales",    "value": "6"},
            {"label": "Recurrentes",         "value": "3"},
            {"label": "% Conf. mixta (RN)",  "value": "50.00%"},
        ],
        "notes": [
            "Los estados SS, RS, NS son transientes — la cadena los abandona permanentemente. "
            "A largo plazo: RN (una roja + una negra) ocurre el 50% del tiempo, RR y NN el 25% c/u, "
            "gracias a la simetría perfecta del mecanismo de cambio de color."
        ],
        "tables": [
            {
                "title": "Matriz de transición P completa (6×6)",
                "headers": ["Estado \\ Siguiente"] + states + ["Σ"],
                "rows": matrix_rows_data,
            },
            {
                "title": "Distribución estacionaria π",
                "headers": ["Estado", "Fracción exacta", "Porcentaje", "Tipo"],
                "rows": pi_rows,
            },
            {
                "title": "Verificación π·P = π (submatriz recurrente)",
                "headers": ["Componente", "Expresión", "Resultado", "Ok"],
                "rows": verify_rows,
            },
        ],
    }


# ─── All problems ────────────────────────────────────────────────────────────

PROBLEMS = [
    solve_problem_1(),
    solve_problem_2(),
    solve_problem_3(),
    solve_problem_4(),
]


# ─── HTML Template ───────────────────────────────────────────────────────────

TEMPLATE = """
<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Taller 2 · Cadenas de Márkov</title>
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
        radial-gradient(circle at top left,  rgba(56,189,248,0.18), transparent 26%),
        radial-gradient(circle at 80% 10%,   rgba(168,85,247,0.14), transparent 28%),
        radial-gradient(circle at 80% 70%,   rgba(34,197,94,0.10),  transparent 24%),
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

    .hero-card, .aside-card, .section, .metric, .table-card, .note {
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
      width: 360px; height: 360px;
      border-radius: 50%;
      background: radial-gradient(circle, rgba(56,189,248,0.28), transparent 65%);
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
      width: 10px; height: 10px;
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
      grid-template-columns: repeat(2, minmax(0,1fr));
      gap: 12px;
    }

    .summary {
      padding: 16px;
      border-radius: 20px;
      background: rgba(255,255,255,0.05);
      border: 1px solid rgba(255,255,255,0.06);
    }

    .summary span { display:block; color:var(--muted); font-size:0.82rem; margin-bottom:6px; }
    .summary strong { display:block; font-size:1.3rem; letter-spacing:-0.03em; }

    .toc { display: grid; gap: 8px; }

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

    .sections { display: grid; gap: 18px; }

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
      grid-template-columns: minmax(0,1.25fr) minmax(300px,0.8fr);
      gap: 16px;
      align-items: start;
      margin-bottom: 18px;
    }

    .section h2 { margin:0; font-size: clamp(1.35rem, 2vw, 2rem); letter-spacing:-0.04em; }
    .section .subtitle { margin:8px 0 0; color:var(--text); font-weight:600; }
    .section .desc { margin:10px 0 0; color:var(--muted); max-width:75ch; }

    .objective {
      padding: 18px;
      border-radius: 22px;
      background: linear-gradient(180deg, rgba(255,255,255,0.09), rgba(255,255,255,0.04));
      border: 1px solid rgba(255,255,255,0.08);
    }

    .objective small {
      display:block; color:var(--muted); font-size:0.8rem;
      text-transform:uppercase; letter-spacing:0.12em; margin-bottom:10px;
    }

    .objective strong { display:block; font-size:1.5rem; letter-spacing:-0.04em; line-height:1.1; }
    .objective p { margin:8px 0 0; color:var(--muted); font-size:0.92rem; }

    .metric-row {
      display: grid;
      grid-template-columns: repeat(3, minmax(0,1fr));
      gap: 12px;
      margin: 18px 0;
    }

    .metric {
      border-radius: 20px;
      padding: 16px;
      background: rgba(255,255,255,0.05);
    }

    .metric span { display:block; color:var(--muted); font-size:0.8rem; margin-bottom:7px; text-transform:uppercase; letter-spacing:0.1em; }
    .metric strong { display:block; font-size:1.35rem; letter-spacing:-0.04em; }

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

    .table-card h3 { margin:0 0 12px; font-size:1rem; letter-spacing:-0.02em; }

    .table-wrap {
      overflow: auto;
      border-radius: 18px;
      border: 1px solid rgba(255,255,255,0.08);
      background: rgba(4,9,18,0.45);
    }

    table { width:100%; border-collapse:collapse; min-width: 520px; }

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

    tbody tr:nth-child(2n) td { background: rgba(255,255,255,0.02); }

    .footer {
      margin-top: 22px;
      color: rgba(237,242,255,0.65);
      font-size: 0.9rem;
      text-align: center;
    }

    @keyframes floatIn {
      from { opacity:0; transform:translateY(12px) scale(0.99); }
      to   { opacity:1; transform:translateY(0) scale(1); }
    }

    @media (max-width: 1100px) {
      .hero, .section-head { grid-template-columns: 1fr; }
      .metric-row, .summary-grid { grid-template-columns: 1fr; }
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
      <div class="hero-card" style="--accent: #38bdf8;">
        <p class="eyebrow">Investigación de Operaciones II · Universidad de Cundinamarca · 701T</p>
        <h1>Taller 2 — Cadenas de Márkov</h1>
        <p class="hero-copy">
          Solución computacional de los cuatro problemas del taller: distribuciones estacionarias,
          matrices de transición, verificación algebraica y análisis de estados transientes vs. recurrentes.
        </p>
        <div class="hero-badges">
          <div class="badge"><span class="badge-dot"></span>{{ problems|length }} problemas resueltos</div>
          <div class="badge"><span class="badge-dot" style="background:#a855f7;box-shadow:0 0 18px #a855f7;"></span>NumPy + SciPy</div>
          <div class="badge"><span class="badge-dot" style="background:#22c55e;box-shadow:0 0 18px #22c55e;"></span>Distribución estacionaria exacta</div>
        </div>
      </div>

      <aside class="aside-card">
        <div class="summary-grid">
          <div class="summary">
            <span>Estado general</span>
            <strong>Óptimo ✓</strong>
          </div>
          <div class="summary">
            <span>Problemas</span>
            <strong>{{ problems|length }}</strong>
          </div>
          <div class="summary">
            <span>Última ejecución</span>
            <strong>{{ generated_at }}</strong>
          </div>
          <div class="summary">
            <span>Método</span>
            <strong>π·P = π</strong>
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
      <article class="section" id="{{ section.anchor }}"
               style="--accent: {{ section.accent }}; --accent-soft: {{ section.accent_soft }};
                      animation-delay: {{ loop.index0 * 70 }}ms;">
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
                <tr>{% for header in table.headers %}<th>{{ header }}</th>{% endfor %}</tr>
              </thead>
              <tbody>
                {% for row in table.rows %}
                <tr>{% for cell in row %}<td>{{ cell }}</td>{% endfor %}</tr>
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
      Generado con Python, Flask y NumPy &mdash;
      Taller 2: Cadenas de Márkov &mdash; Investigación de Operaciones II &mdash;
      Universidad de Cundinamarca.
      Ejecuta <strong>Solucion_Markov.py</strong> para abrir este panel.
    </div>
  </div>
</body>
</html>
"""


# ─── Flask app ───────────────────────────────────────────────────────────────

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