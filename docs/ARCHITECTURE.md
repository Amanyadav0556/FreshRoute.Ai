# FreshRoute AI — System Architecture Document

## Overview

FreshRoute AI is an intelligent decision-support and dispatch-optimization platform designed for the perishable produce supply chain. It addresses post-harvest loss in fresh fruit and vegetable (FFV) logistics through real-time mathematical optimization and dynamic discount pricing.

---

## 1. High-Level Architecture Topology

```
+-----------------------------------------------------------------------------------+
|                                  USER BROWSER                                     |
|  React 18 + Vite + TypeScript + Tailwind CSS (Custom Dark Glassmorphic Design)   |
|  TanStack Query + Recharts + Lucide Icons + React Hook Form + Zod                 |
+-----------------------------------------------------------------------------------+
                                  |                     |
                   Supabase Auth  |                     |  REST API Calls
                  (JWT Sessions)  |                     |  (/api/*)
                                  v                     v
+-------------------------------+      +--------------------------------------------+
|         SUPABASE CLOUD        |      |              FASTAPI BACKEND               |
|  - PostgreSQL Database        |      |  - Python 3.11+ ASGI Web Engine            |
|  - Row-Level Security (5 Roles|      |  - SciPy HiGHS LP/MILP Solver Engine       |
|  - Storage & Realtime Triggers|      |  - Arrhenius Shelf-Life Thermal Model      |
|  - Analytical Views           |      |  - 7-Strategy Dynamic Discount Calculator  |
+-------------------------------+      |  - 6-Point Physical Constraint Validator   |
               ^                       +--------------------------------------------+
               |                                              |
               +----------------------------------------------+
                         Database Sync & Fallback Engine
```

---

## 2. Core Functional Modules

### A. Frontend Layer (`frontend/src/`)
- **`pages/OverviewPage.tsx`**: High-level KPI command center, emergency risk counters, shelf-life distribution bars.
- **`pages/InventoryPage.tsx`**: Searchable produce inventory table with color-coded shelf-life degradation progress bars.
- **`pages/PlannerPage.tsx`**: Interactive dispatch optimizer cockpit; allows selecting strategies (Balanced, Max Margin, Min Spoilage) and running the solver.
- **`pages/DiscountsPage.tsx`**: 7-option comparison table with price elasticity and recovery projections.
- **`pages/AlertsPage.tsx`**: Real-time spoilage warning center with emergency alternative redistribution feasibility analysis.
- **`pages/EvaluationPage.tsx`**: Multi-strategy scoreboard with Recharts bar & radar comparisons.
- **`pages/ScenariosPage.tsx`**: 8 real-world disruption scenarios with toggleable parameter overrides.
- **`pages/AssumptionsPage.tsx`**: Transparent scientific and economic assumption disclosure with provenance badges.

### B. Optimization & Algorithmic Core (`backend/app/services/`)
- **HiGHS Simplex/Interior-Point Solver (`highs_solver.py`)**: Uses SciPy's HiGHS C++ linear programming engine for optimal dispatch assignment.
- **Greedy Priority Dispatcher (`greedy_solver.py`)**: Multi-attribute ranking fallback solver.
- **Arrhenius Shelf-Life Model (`shelf_life.py`)**: Biological decay acceleration with Q10 temperature modeling and road vibration penalty.
- **Plan Validator (`validator.py`)**: 6-point verification auditing vehicle capacity, produce supply, travel time, and market demand caps.
- **Dynamic Discount Engine (`discount_engine.py`)**: 7-strategy pricing matrix integrating price elasticity curves.

---

## 3. Data Flow

1. **Harvest Logging**: Fresh batch registered at Nashik hub with initial shelf-life and ambient temperature.
2. **Thermal Degradation**: Respiration rate adjusted dynamically based on route temperature and road vibration.
3. **Trip Formulation**: Viable (batch, destination, vehicle) triplets evaluated for transit feasibility.
4. **LP Matrix Assembly**: Objective function assembled; HiGHS solver solves continuous/mixed-integer allocation.
5. **Constraint Validation**: Plan verified against 6 physical boundaries before committing.
6. **Execution & Audit**: Vehicle dispatched, inventory deducted, and audit trail logged.
