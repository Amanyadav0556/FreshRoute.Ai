# FreshRoute AI 🥬🚚

**Intelligent Perishable Produce Distribution & Discount Optimization**

FreshRoute AI is a decision-support platform for perishable produce distribution. It recommends optimal dispatch plans to minimize spoilage and maximize net economic value.

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React + Vite + TypeScript + Tailwind CSS + shadcn/ui |
| Charts | Recharts |
| Forms | React Hook Form + Zod |
| Server State | TanStack Query |
| Backend | Python + FastAPI + Pydantic |
| Optimization | SciPy (HiGHS) + greedy fallback |
| Database | Supabase PostgreSQL |
| Auth | Supabase Auth + RLS |

---

## Project Structure

```
freshroute.ai/
├── frontend/          # React + Vite + TypeScript app
├── backend/           # Python FastAPI optimization engine
├── supabase/
│   ├── migrations/    # SQL migrations
│   └── seed.sql       # Demo seed data
├── data/
│   ├── sample/        # Sample datasets
│   └── scenarios/     # Scenario definitions
├── scripts/           # Setup and utility scripts
├── docs/              # API and architecture docs
├── .env.example       # Environment variable template
└── README.md
```

---

## Quick Start (Windows PowerShell)

### Prerequisites
- Node.js >= 18
- Python >= 3.11
- Git

### 1. Clone & Setup Environment

```powershell
git clone https://github.com/Amanyadav0556/FreshRoute.Ai.git
cd FreshRoute.Ai
Copy-Item .env.example .env
# Edit .env with your Supabase credentials
```

### 2. Frontend

```powershell
cd frontend
npm install
npm run dev
# Runs at http://localhost:5173
```

### 3. Backend

```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
# API at http://localhost:8000
# Docs at http://localhost:8000/docs
```

### 4. Database (Supabase)

```powershell
# Install Supabase CLI
npm install -g supabase
supabase login
supabase link --project-ref YOUR_PROJECT_REF
supabase db push          # Apply migrations
psql $DATABASE_URL -f supabase/seed.sql  # Load seed data
```

---

## Environment Variables

See [.env.example](.env.example) for all required variables.

**Frontend** (prefix with `VITE_`):
- `VITE_SUPABASE_URL` — Supabase project URL
- `VITE_SUPABASE_ANON_KEY` — Supabase publishable anon key
- `VITE_API_BASE_URL` — FastAPI backend URL

**Backend**:
- `SUPABASE_URL` — Supabase project URL
- `SUPABASE_SERVICE_ROLE_KEY` — Service-role key (never expose to browser)
- `DATABASE_URL` — Direct PostgreSQL connection string

---

## Running Tests

```powershell
# Backend tests
cd backend
.\venv\Scripts\Activate.ps1
pytest tests/ -v

# Frontend build check
cd frontend
npm run build
```

---

## Key Features

- 📦 **Inventory Management** — Track produce batches with shelf-life monitoring
- 🗺️ **Dispatch Optimization** — SciPy/HiGHS LP solver with greedy fallback
- 💰 **Discount Engine** — Compare 7 pricing strategies per at-risk batch
- 🚨 **Spoilage Alerts** — Real-time risk flagging with emergency redistribution
- 📊 **Evaluation Scoreboard** — Compare FEFO, highest-price, greedy and FreshRoute optimizer
- 🎭 **Scenario Analysis** — 8 configurable disruption scenarios
- 🔒 **Role-Based Access** — Supabase RLS with 5 user roles
- 📋 **Audit Trail** — Complete action history

---

## Roles

| Role | Access |
|------|--------|
| Distributor | Full planning, all data |
| Collection Centre Worker | Own centre batches |
| Seller | Destination/order data |
| Driver | Assigned dispatches |
| Rental Vehicle Owner | Own vehicle data |

---

## Data Provenance

All inputs are clearly labelled as `real`, `estimated` or `simulated`. Demand-response assumptions are explicitly disclosed. No fabricated optimization results.

---

## License

MIT — Built for hackathon demonstration purposes.
