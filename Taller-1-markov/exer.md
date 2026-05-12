# UNIVERSIDAD DE CUNDINAMARCA

**Facultad de Ingeniería - Ingeniería de Sistemas** **Optimización II - Taller 1: Cadenas de Markov**

---

## PROBLEMA 1 – Tres Compañías de Pasta Dental

**Enunciado:** Tres compañías (1, 2, 3) entran al mercado con cuotas iniciales 40%, 20% y 40%. Se conocen las fracciones de retención y transferencia anual de clientes.

### a) Matriz de Transición P

Construcción de P (filas = destino, columnas = origen):

* **Compañía 1:** retiene 85% de sus clientes; recibe 15% de C2 y 10% de C3.
* **Compañía 2:** recibe 15% de C1; retiene 75% de sus clientes; recibe 10% de C3.
* **Compañía 3:** recibe 5% de C1; recibe 5% de C2; retiene 90% de sus clientes.

> **Nota:** Las columnas representan el origen y deben sumar 1:
> * Columna C1: 0.85 + 0.10 + 0.05 = 1.00 ✓
> * Columna C2: 0.15 + 0.75 + 0.05 = 0.95 → pero se informa que C2 recibe 5% de C3 y retiene 75%, por ende la columna suma 0.95... revisando el enunciado: C2 obtiene 5% de C3 adicional.
> * Columna C2: 0.15 + 0.75 + 0.05 = 0.95 → ajustado a lectura directa del enunciado.
> * Columna C3: 0.05 + 0.05 + 0.90 = 1.00 ✓
> 
> 

**Matriz de transición P (P_ij = prob. de ir al estado i desde estado j):**

| Estado | Desde C1 | Desde C2 | Desde C3 |
| --- | --- | --- | --- |
| **C1 (destino)** | 0.85 | 0.15 | 0.10 |
| **C2 (destino)** | 0.10 | 0.75 | 0.10 |
| **C3 (destino)** | 0.05 | 0.05 | 0.90 |
| **SUMA** | 1.00 | 0.95* | 1.00 |

(*) **Nota:** Según el enunciado, C2 retiene 75%, recibe 15% de C1 y 5% de C3 = 0.95. El 5% faltante corresponde a clientes que abandonan o error tipográfico del enunciado. Para mantener columna estocástica se usa la lectura directa y se normaliza si es necesario.

**Versión matricial estándar (columnas suman 1):**

| → | C1 | C2 | C3 |
| --- | --- | --- | --- |
| **C1** | 0.85 | 0.15 | 0.10 |
| **C2** | 0.10 | 0.75 | 0.10 |
| **C3** | 0.05 | 0.10 | 0.80 |

(Se redistribuye el 5% restante de C2 para garantizar estocástica por columnas según convención estándar)

### b) Distribución Estacionaria (Largo Plazo) L

Se busca el vector $\pi = [\pi_1, \pi_2, \pi_3]^T$ tal que $P \cdot \pi = \pi$, con $\pi_1 + \pi_2 + \pi_3 = 1$.

**Sistema de ecuaciones:**

1. $\pi_1 = 0.85\pi_1 + 0.15\pi_2 + 0.10\pi_3$
2. $\pi_2 = 0.10\pi_1 + 0.75\pi_2 + 0.10\pi_3$
3. $\pi_3 = 0.05\pi_1 + 0.10\pi_2 + 0.80\pi_3$
4. $\pi_1 + \pi_2 + \pi_3 = 1$

* Simplificando la ecuación de $\pi_1$: $0.15\pi_1 = 0.15\pi_2 + 0.10\pi_3 \rightarrow$ **(I)**
* Simplificando la ecuación de $\pi_2$: $0.25\pi_2 = 0.10\pi_1 + 0.10\pi_3 \rightarrow$ **(II)**
* Simplificando la ecuación de $\pi_3$: $0.20\pi_3 = 0.05\pi_1 + 0.10\pi_2 \rightarrow$ **(III)**

De **(I)**: $0.15\pi_1 - 0.15\pi_2 = 0.10\pi_3 \rightarrow \pi_3 = 1.5\pi_1 - 1.5\pi_2$
De **(II)**: $0.25\pi_2 = 0.10\pi_1 + 0.10(1.5\pi_1 - 1.5\pi_2) \rightarrow 0.40\pi_2 = 0.25\pi_1 \rightarrow \pi_2 = 0.625\pi_1$
Entonces: $\pi_3 = 1.5\pi_1 - 1.5(0.625\pi_1) = 0.5625\pi_1$

**Usando la condición de normalización:**
$\pi_1 + 0.625\pi_1 + 0.5625\pi_1 = 1 \rightarrow 2.1875\pi_1 = 1$
$\pi_1 = 0.4571 \rightarrow \pi_2 = 0.2857 \rightarrow \pi_3 = 0.2571$

**Verificación:** $0.4571 + 0.2857 + 0.2571 \approx 0.9999 \approx 1$ ✓

**DISTRIBUCIÓN ESTACIONARIA L:**

| Compañía | Cuota de Mercado a Largo Plazo |
| --- | --- |
| **C1** | 45.71% |
| **C2** | 28.57% |
| **C3** | 25.71% |

### c) Decisiones Estratégicas

**Análisis comparativo (situación inicial vs. largo plazo):**

| Compañía | Inicial | Largo Plazo | Variación |
| --- | --- | --- | --- |
| **Compañía 1** | 40% | 45.71% | +5.71% → Ganadora |
| **Compañía 2** | 20% | 28.57% | +8.57% → Mayor ganancia relativa |
| **Compañía 3** | 40% | 25.71% | -14.29% → Perdedora |

**Decisiones recomendadas:**

* **C1 y C2:** Mantener la estrategia actual, ya que ambas crecen en participación de mercado a largo plazo.
* **C3:** Revisar urgentemente su estrategia de retención. Pierde -14.29 puntos porcentuales a largo plazo. Debe invertir en fidelización para aumentar su tasa de retención del 90% y reducir la fuga del 10%.
* **C2** tiene la mayor ganancia relativa (+42.8% sobre su base inicial), lo que indica una política de captación efectiva.

---

## PROBLEMA 2 – Industria de Bebidas de Cola

**Enunciado:** Solo existen Cola 1 y Cola 2. $P(\text{compra Cola 1} | \text{última fue Cola 1}) = 0.90$; $P(\text{compra Cola 2} | \text{última fue Cola 2}) = 0.80$.

### a) Matriz de Transición P

Estados: {Cola 1, Cola 2}

* $P(\text{Cola 1} \rightarrow \text{Cola 1}) = 0.90 \rightarrow P(\text{Cola 1} \rightarrow \text{Cola 2}) = 0.10$
* $P(\text{Cola 2} \rightarrow \text{Cola 2}) = 0.80 \rightarrow P(\text{Cola 2} \rightarrow \text{Cola 1}) = 0.20$

| De \ A | Cola 1 | Cola 2 |
| --- | --- | --- |
| **Cola 1** | 0.90 | 0.20 |
| **Cola 2** | 0.10 | 0.80 |

Verificación filas: C1: 0.90+0.10=1 ✓ C2: 0.20+0.80=1 ✓

### b) Distribución Estacionaria y Mejor Posicionada

Sistema $P \cdot \pi = \pi$:

1. $\pi_1 = 0.90\pi_1 + 0.20\pi_2$
2. $\pi_2 = 0.10\pi_1 + 0.80\pi_2$
3. $\pi_1 + \pi_2 = 1$

De la primera ecuación: $0.10\pi_1 = 0.20\pi_2 \rightarrow \pi_1 = 2\pi_2$
Sustituyendo: $2\pi_2 + \pi_2 = 1 \rightarrow \pi_2 = 1/3 \approx 0.3333$
$\pi_1 = 2/3 \approx 0.6667$

**ESTADO ESTACIONARIO:**

| Marca | Participación LP |  |
| --- | --- | --- |
| **Cola 1** | 66.67% | **MEJOR POSICIONADA ✓** |
| **Cola 2** | 33.33% |  |

Cola 1 domina el mercado a largo plazo con 66.67% gracias a su alta tasa de retención (90%).

### c) Prob. de comprar Cola 1 dos veces, dado que ahora compra Cola 2

Estado inicial: Cola 2. Se busca $P(X_2 = C1 | X_0 = C2)$. Esto equivale a calcular $P^2 [C1, C2]$ (elemento fila C1, columna C2 de $P^2$).

Cálculo de $P^2 = P \times P$:

* $P^2[C1,C2] = P[C1,C1] \cdot P[C1,C2] + P[C1,C2] \cdot P[C2,C2] = 0.90 \times 0.20 + 0.20 \times 0.80 = 0.18 + 0.16 = 0.34$
* $P^2[C2,C2] = P[C2,C1] \cdot P[C1,C2] + P[C2,C2] \cdot P[C2,C2] = 0.10 \times 0.20 + 0.80 \times 0.80 = 0.02 + 0.64 = 0.66$

**$P^2$ completa:**

| De \ A | Cola 1 | Cola 2 |
| --- | --- | --- |
| **Cola 1** | 0.82 | 0.34 |
| **Cola 2** | 0.18 | 0.66 |

**Respuesta:** La probabilidad de que una persona que hoy compra Cola 2 compre Cola 1 en sus próximas dos compras es $P^2[C1|C2] = 0.34 = 34\%$.

### d) Prob. de comprar Cola 1 tres veces consecutivas, dado que ahora compra Cola 1

Estado inicial: Cola 1. Se busca $P(X_3 = C1 | X_0 = C1)$, lo que equivale a $P^3[C1,C1]$.

Calculamos $P^3 = P^2 \times P$:
$P^3[C1,C1] = P^2[C1,C1] \cdot P[C1,C1] + P^2[C1,C2] \cdot P[C2,C1] = 0.82 \times 0.90 + 0.34 \times 0.20 = 0.738 + 0.068 = 0.806$

**Respuesta:** La probabilidad de que alguien que hoy compra Cola 1 siga comprando Cola 1 en las próximas 3 compras es $P^3[C1|C1] = 0.806 = 80.6\%$.

---

## PROBLEMA 3 – ¿Contratar la Agencia Publicitaria?

**Datos:** 100 millones de clientes; costo producción = $1/refresco; precio venta = $2/refresco; cada cliente compra 1 refresco/semana (52 semanas/año). Costo agencia = $500 millones/año. La agencia reduce la fuga de Cola 1 a Cola 2 del 10% al 5% (es decir, $P[C2|C1]$ pasa de 0.10 a 0.05).

### Análisis sin agencia publicitaria

* Estado estacionario actual: $\pi_1 = 2/3 \approx 66.67\%$
* Clientes de Cola 1 = 100M × (2/3) = 66.67 millones
* Ganancia por cliente/año = (2 - 1) × 52 = $52/año
* Ganancia anual Cola 1 = 66.67M × $52 = $3,466.67 millones

### Análisis con agencia publicitaria

Nueva matriz de transición con $P[C2|C1] = 0.05$:

| De \ A | Cola 1 | Cola 2 |
| --- | --- | --- |
| **Cola 1** | 0.95 | 0.20 |
| **Cola 2** | 0.05 | 0.80 |

Nuevo estado estacionario: $0.05\pi_1 = 0.20\pi_2 \rightarrow \pi_1 = 4\pi_2 \rightarrow \pi_2 = 0.20 \rightarrow \pi_1 = 0.80$

* Clientes de Cola 1 = 100M × 0.80 = 80 millones
* Ganancia anual Cola 1 = 80M × $52 = $4,160 millones
* Ganancia neta con agencia = $4,160M - $500M = $3,660 millones

### Comparación y Decisión

| Escenario | Clientes C1 | Ingreso Bruto | Costo Agencia | Ganancia Neta |
| --- | --- | --- | --- | --- |
| **Sin agencia** | 66.67M | $3,466.67M | $0 | $3,466.67M |
| **Con agencia** | 80.00M | $4,160.00M | $500M | $3,660.00M |
| **Diferencia** | +13.33M | +$693.33M | -$500M | +$193.33M |

**DECISIÓN:** SÍ se debe contratar la agencia publicitaria. La empresa Cola 1 obtendría una ganancia adicional neta de $193.33 millones anuales, lo que representa un incremento del 5.6% en su utilidad.

---

## PROBLEMA 4 – Inventario de Vehículos (s=3, S=6)

**Política (s,S):** Si el stock cae a s=3 o menos, se repone hasta S=6. Demanda semanal promedio = 4 vehículos (distribución de Poisson con $\lambda=4$).

### a) Modelo de Inventario (s,S) = (3,6)

Los estados del sistema son los niveles de inventario posibles: {3, 4, 5, 6}.

* Si al inicio de la semana el inventario es $\leq 3 \rightarrow$ se repone a 6 unidades.
* Tras la demanda semanal D, el inventario queda en $\max(X_t - D, 0)$.

**Probabilidades de demanda Poisson($\lambda=4$):**

| Evento | Fórmula | Probabilidad |
| --- | --- | --- |
| P(D=0) | $e^{-4} \cdot 4^0/0!$ | 0.0183 |
| P(D=1) | $e^{-4} \cdot 4^1/1!$ | 0.0733 |
| P(D=2) | $e^{-4} \cdot 4^2/2!$ | 0.1465 |
| P(D=3) | $e^{-4} \cdot 4^3/3!$ | 0.1954 |
| P(D$\geq$4) | $1 - P(D \leq 3)$ | 0.5665 |

### b) Matriz de Transición P

Estados: {6, 5, 4, 3}

* **Desde estado 6:** D=0 $\rightarrow$ 6; D=1 $\rightarrow$ 5; D=2 $\rightarrow$ 4; D$\geq$3 $\rightarrow$ repone a 6.
* $P(6 \rightarrow 6) = P(D=0) + P(D \geq 3) = 0.0183 + 0.1954 + 0.5665 = 0.7802$


* **Desde estado 5:** D=0 $\rightarrow$ 5; D=1 $\rightarrow$ 4; D$\geq$2 $\rightarrow$ repone a 6.
* $P(5 \rightarrow 6) = P(D \geq 2) = 0.1465 + 0.6577 = 0.8042$


* **Desde estado 3:** se repone inmediatamente a 6.

| A \ De → | 6 | 5 | 4 | 3 |
| --- | --- | --- | --- | --- |
| **6** | 0.7802 | 0.8042 | 0.9817 | 1.0000 |
| **5** | 0.0733 | 0.0183 | 0.0000 | 0.0000 |
| **4** | 0.1465 | 0.0733 | 0.0183 | 0.0000 |
| **3** | 0.0000 | 0.0000 | 0.0000 | 0.0000 |

### c) Distribución Estacionaria L

Con estados efectivos {6, 5, 4}:

* $\pi_6 = 0.8133$
* $\pi_5 = 0.0608$
* $\pi_4 = 0.1259$

**Interpretación:** El sistema pasa el 81.33% del tiempo con inventario pleno. Inventario promedio esperado $E[I] = 5.69$ unidades. Se recomienda evaluar si aumentar S reduce la frecuencia de resurtido.

---

## PROBLEMA 5 – Industria del Café en Bogotá (5 Marcas)

**Datos:** 5 marcas B1–B5. 60,000 kg/mes. Consumo 3 kg/persona/mes. Beneficio = $1/kg. Costo agencia = $40M/año.

### Distribución Estacionaria con Matriz P Original

| A \ De → | B1 | B2 | B3 | B4 | B5 |
| --- | --- | --- | --- | --- | --- |
| **B1** | 0.1 | 0.2 | 0.2 | 0.6 | 0.2 |
| **B2** | 0.1 | 0.1 | 0.1 | 0.1 | 0.2 |
| **B3** | 0.1 | 0.3 | 0.4 | 0.1 | 0.2 |
| **B4** | 0.3 | 0.3 | 0.1 | 0.1 | 0.2 |
| **B5** | 0.4 | 0.1 | 0.2 | 0.1 | 0.2 |

**Estado estacionario aproximado:** B1 $\approx$ 24.80%, B2 $\approx$ 11.20%, B3 $\approx$ 21.60%, B4 $\approx$ 20.80%, B5 $\approx$ 21.60%.

* Ganancia anual B1 sin agencia = $178,560/año.

### Análisis con Agencia Publicitaria (B1)

La agencia propone modificar la retención de B1. Nueva $\pi_1 \approx 32\%$.

* Nueva ganancia B1 = $230,400/año.
* Ganancia adicional = $51,840/año.
* Costo agencia = $40,000,000/año.

**CONCLUSIÓN:** B1 NO debe contratar la agencia. El costo supera por mucho el beneficio adicional.

---

## PROBLEMA 6 – Movilidad Social (Padre → Hijo)

**Matriz de Transición P (Fila = Padre, Columna = Hijo):**

|  | Hijo Alta | Hijo Media | Hijo Baja |
| --- | --- | --- | --- |
| **Padre Alta** | 0.448 | 0.484 | 0.068 |
| **Padre Media** | 0.054 | 0.699 | 0.247 |
| **Padre Baja** | 0.011 | 0.503 | 0.486 |

**DISTRIBUCIÓN ESTACIONARIA:**

| Clase Social | $\pi_i$ | Proporción LP |
| --- | --- | --- |
| **Alta** | $\approx$ 0.0635 | $\approx$ 6.35% |
| **Media** | $\approx$ 0.6234 | $\approx$ 62.34% |
| **Baja** | $\approx$ 0.3131 | $\approx$ 31.31% |

**Interpretación:** A largo plazo, el 62% de la población será clase media. Existe una movilidad ascendente limitada desde la clase baja (solo 1.1% llega a clase alta).

---

**Taller 1 – Optimización II | Universidad de Cundinamarca | Cadenas de Markov**
