# FreshRoute AI — Mathematical Optimization & Biological Decay Model

## 1. Mathematical Formulation

FreshRoute AI formulates produce distribution as a Linear/Mixed-Integer Program (LP/MILP) designed to maximize Net Economic Value while adhering to physical supply, transit shelf-life viability, vehicle payload capacities, and destination market intake constraints.

---

### Sets & Indices
- $b \in B$: Perishable produce batches in inventory.
- $d \in D$: Target destination markets (APMC mandis, retail hubs, processors).
- $v \in V$: Transport fleet vehicles (ambient trucks, reefers).
- $k \in K$: Produce commodity types (Tomatoes, Spinach, Grapes, Onions, Mangoes).

---

### Parameters
- $Q_b$: Available quantity of batch $b$ in stock (kg).
- $C_{proc, b}$: Unit procurement cost paid to farmer for batch $b$ (₹/kg).
- $RSL_b$: Current remaining shelf-life of batch $b$ (hours).
- $Cap_v$: Maximum legal payload capacity of vehicle $v$ (kg).
- $F_v$: Fixed vehicle dispatch/booking cost (₹).
- $c_{km, v}$: Per-kilometer operating cost of vehicle $v$ (₹/km).
- $Dist_d$: Transit road distance from origin collection hub to destination $d$ (km).
- $Toll_d$: Highway toll fees on corridor to destination $d$ (₹).
- $T_{transit, d, v}$: Estimated transit duration to destination $d$ (hours).
- $H_d$: Unloading and handling fee at destination market $d$ (₹/kg).
- $P_{b, d}$: Effective market selling price for commodity of batch $b$ at destination $d$ (₹/kg).
- $D_{d, k}$: Demand ceiling for commodity $k$ at destination $d$ (kg).
- $\Pi_{spoil, b, d, v}$: Estimated probability of spoilage decay during transit and handling buffer.

---

### Decision Variables
- $x_{b, d, v} \ge 0$: Continuous weight of batch $b$ allocated to destination $d$ via vehicle $v$ (kg).
- $y_{v, d} \in \{0, 1\}$: Binary variable indicating if vehicle $v$ is dispatched to destination $d$.

---

### Objective Function: Maximize Net Economic Value ($Z$)

$$\max Z = \sum_{b \in B} \sum_{d \in D} \sum_{v \in V} \left[ \Big( P_{b, d} - C_{proc, b} - H_d \Big) x_{b, d, v} - \Pi_{spoil, b, d, v} \cdot C_{proc, b} \cdot x_{b, d, v} \right] - \sum_{v \in V} \sum_{d \in D} \Big( F_v + c_{km, v} \cdot Dist_d + Toll_d \Big) y_{v, d}$$

---

### Physical Constraints

#### 1. Batch Stock Conservation
Total allocated volume cannot exceed harvested inventory:
$$\sum_{d \in D} \sum_{v \in V} x_{b, d, v} \le Q_b \quad \forall b \in B$$

#### 2. Vehicle Payload Capacity
Cargo loaded on vehicle $v$ bound for destination $d$ cannot exceed vehicle rated capacity:
$$\sum_{b \in B} x_{b, d, v} \le Cap_v \cdot y_{v, d} \quad \forall v \in V, \forall d \in D$$

#### 3. Single Destination Assignment per Shift
Each active vehicle can service at most one target destination per dispatch run:
$$\sum_{d \in D} y_{v, d} \le 1 \quad \forall v \in V$$

#### 4. Market Demand Ceilings
Deliveries to destination $d$ must respect buyer order caps:
$$\sum_{b \in B, comm(b) = k} \sum_{v \in V} x_{b, d, v} \le D_{d, k} \quad \forall d \in D, \forall k \in K$$

#### 5. Shelf-Life Transit Feasibility (Hard Cutoff)
Produce cannot be assigned to routes where transit plus handling exceeds remaining shelf-life:
$$x_{b, d, v} = 0 \quad \text{if } T_{transit, d, v} + \text{Buffer} \ge RSL_b$$

---

## 2. Biological Respiration & Thermal Decay Model

Produce respiration and senescence accelerate non-linearly with temperature following the Arrhenius relationship:

$$\text{Decay Multiplier } \mu(T) = Q_{10}^{\frac{T_{ambient} - T_{ref}}{10}}$$

Where:
- $T_{ref} = 20^\circ\text{C}$ (Standard reference temperature)
- $Q_{10} \in [2.0, 2.8]$ (Commodity respiration coefficient)
- For refrigerated transport (reefers), $\mu(T) = 0.35$ (temperature maintained at $4^\circ\text{C}$).

---

## 3. Dynamic Discounting & Price Elasticity

Clearance velocity for at-risk batches uses calibrated constant elasticity:

$$\frac{\Delta Q}{Q} = \varepsilon \cdot \frac{\Delta P}{P}$$

The optimal marginal revenue markdown satisfies:

$$P^* = \frac{C_{proc}}{1 + \frac{1}{\varepsilon}}$$
