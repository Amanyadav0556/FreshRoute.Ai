-- FreshRoute AI Database Schema Migration 01
-- Tables: produce_batches, destinations, vehicles, routes, orders, dispatch_plans, plan_allocations, discount_recommendations, disruption_scenarios, audit_logs

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 1. Produce Batches
CREATE TABLE IF NOT EXISTS produce_batches (
    id TEXT PRIMARY KEY DEFAULT ('batch-' || substr(md5(random()::text), 1, 8)),
    batch_code TEXT UNIQUE NOT NULL,
    commodity TEXT NOT NULL,
    variety TEXT,
    collection_centre_id TEXT NOT NULL,
    initial_quantity_kg NUMERIC(10, 2) NOT NULL CHECK (initial_quantity_kg > 0),
    current_quantity_kg NUMERIC(10, 2) NOT NULL CHECK (current_quantity_kg >= 0),
    harvest_date TIMESTAMPTZ NOT NULL,
    initial_shelf_life_hours NUMERIC(8, 2) NOT NULL CHECK (initial_shelf_life_hours > 0),
    remaining_shelf_life_hours NUMERIC(8, 2) NOT NULL CHECK (remaining_shelf_life_hours >= 0),
    storage_condition TEXT NOT NULL DEFAULT 'ambient',
    procurement_cost_per_kg NUMERIC(10, 2) NOT NULL CHECK (procurement_cost_per_kg >= 0),
    min_selling_price_per_kg NUMERIC(10, 2) NOT NULL CHECK (min_selling_price_per_kg >= 0),
    quality_grade TEXT NOT NULL DEFAULT 'Grade A',
    urgency_level TEXT NOT NULL DEFAULT 'normal',
    spoilage_risk_percent NUMERIC(5, 2) NOT NULL DEFAULT 0.0,
    provenance TEXT NOT NULL DEFAULT 'real',
    provenance_source TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 2. Destinations (APMC Mandis & Retail Hubs)
CREATE TABLE IF NOT EXISTS destinations (
    id TEXT PRIMARY KEY DEFAULT ('dest-' || substr(md5(random()::text), 1, 8)),
    name TEXT NOT NULL,
    city TEXT NOT NULL,
    state TEXT NOT NULL DEFAULT 'Maharashtra',
    latitude NUMERIC(9, 6) NOT NULL,
    longitude NUMERIC(9, 6) NOT NULL,
    market_type TEXT NOT NULL DEFAULT 'wholesale_mandi',
    unloading_handling_fee_per_kg NUMERIC(10, 2) NOT NULL DEFAULT 0.50,
    avg_selling_price_multiplier NUMERIC(6, 3) NOT NULL DEFAULT 1.000,
    daily_demand_capacity_kg NUMERIC(10, 2) NOT NULL DEFAULT 10000.0,
    provenance TEXT NOT NULL DEFAULT 'real',
    provenance_source TEXT,
    active_orders_count INT NOT NULL DEFAULT 0,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 3. Vehicles (Fleet & Rental Logistics)
CREATE TABLE IF NOT EXISTS vehicles (
    id TEXT PRIMARY KEY DEFAULT ('veh-' || substr(md5(random()::text), 1, 8)),
    plate_number TEXT UNIQUE NOT NULL,
    model_type TEXT NOT NULL,
    vehicle_category TEXT NOT NULL DEFAULT 'mini_truck',
    capacity_kg NUMERIC(10, 2) NOT NULL CHECK (capacity_kg > 0),
    is_refrigerated BOOLEAN NOT NULL DEFAULT FALSE,
    fixed_booking_cost_inr NUMERIC(10, 2) NOT NULL DEFAULT 400.0,
    per_km_cost_inr NUMERIC(10, 2) NOT NULL DEFAULT 14.0,
    avg_speed_kmh NUMERIC(6, 2) NOT NULL DEFAULT 45.0,
    current_location TEXT NOT NULL DEFAULT 'Nashik Central Hub',
    owner_role TEXT NOT NULL DEFAULT 'owned',
    status TEXT NOT NULL DEFAULT 'available',
    provenance TEXT NOT NULL DEFAULT 'real',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 4. Routes (Transit Matrix & Road Conditions)
CREATE TABLE IF NOT EXISTS routes (
    id TEXT PRIMARY KEY DEFAULT ('route-' || substr(md5(random()::text), 1, 8)),
    origin_name TEXT NOT NULL,
    destination_id TEXT NOT NULL REFERENCES destinations(id) ON DELETE CASCADE,
    destination_name TEXT NOT NULL,
    distance_km NUMERIC(8, 2) NOT NULL CHECK (distance_km > 0),
    standard_travel_time_hours NUMERIC(6, 2) NOT NULL CHECK (standard_travel_time_hours > 0),
    toll_charges_inr NUMERIC(10, 2) NOT NULL DEFAULT 0.0,
    road_quality_factor NUMERIC(4, 2) NOT NULL DEFAULT 1.0,
    ambient_temp_celsius NUMERIC(5, 2) NOT NULL DEFAULT 28.0,
    effective_travel_time_hours NUMERIC(6, 2) NOT NULL,
    provenance TEXT NOT NULL DEFAULT 'real',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 5. Orders (Market Buyer Demand)
CREATE TABLE IF NOT EXISTS orders (
    id TEXT PRIMARY KEY DEFAULT ('ord-' || substr(md5(random()::text), 1, 8)),
    order_code TEXT UNIQUE NOT NULL,
    destination_id TEXT NOT NULL REFERENCES destinations(id) ON DELETE CASCADE,
    destination_name TEXT NOT NULL,
    commodity TEXT NOT NULL,
    variety TEXT,
    demanded_quantity_kg NUMERIC(10, 2) NOT NULL CHECK (demanded_quantity_kg > 0),
    offered_price_per_kg NUMERIC(10, 2) NOT NULL CHECK (offered_price_per_kg > 0),
    delivery_deadline TIMESTAMPTZ NOT NULL,
    min_acceptable_grade TEXT NOT NULL DEFAULT 'Grade B',
    min_shelf_life_upon_arrival_hours NUMERIC(6, 2) NOT NULL DEFAULT 12.0,
    penalty_per_kg_unfulfilled NUMERIC(10, 2) NOT NULL DEFAULT 2.0,
    allocated_quantity_kg NUMERIC(10, 2) NOT NULL DEFAULT 0.0,
    fulfillment_rate_percent NUMERIC(5, 2) NOT NULL DEFAULT 0.0,
    status TEXT NOT NULL DEFAULT 'pending',
    provenance TEXT NOT NULL DEFAULT 'real',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 6. Dispatch Plans
CREATE TABLE IF NOT EXISTS dispatch_plans (
    id TEXT PRIMARY KEY,
    strategy TEXT NOT NULL,
    scenario_name TEXT NOT NULL DEFAULT 'Normal Operation',
    solver_used TEXT NOT NULL,
    solver_duration_ms NUMERIC(8, 2) NOT NULL,
    status TEXT NOT NULL DEFAULT 'optimized',
    total_allocated_kg NUMERIC(10, 2) NOT NULL DEFAULT 0.0,
    total_revenue_inr NUMERIC(12, 2) NOT NULL DEFAULT 0.0,
    total_transport_cost_inr NUMERIC(12, 2) NOT NULL DEFAULT 0.0,
    total_discount_loss_inr NUMERIC(12, 2) NOT NULL DEFAULT 0.0,
    net_economic_value_inr NUMERIC(12, 2) NOT NULL DEFAULT 0.0,
    spoilage_prevented_kg NUMERIC(10, 2) NOT NULL DEFAULT 0.0,
    average_spoilage_risk_percent NUMERIC(5, 2) NOT NULL DEFAULT 0.0,
    total_dispatches INT NOT NULL DEFAULT 0,
    allocations JSONB NOT NULL DEFAULT '[]'::jsonb,
    validation JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 7. Audit Logs
CREATE TABLE IF NOT EXISTS audit_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID,
    user_role TEXT,
    action TEXT NOT NULL,
    entity_type TEXT NOT NULL,
    entity_id TEXT,
    metadata JSONB DEFAULT '{}'::jsonb,
    ip_address TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
