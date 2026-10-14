-- FreshRoute AI Database Schema Migration 02
-- Row-Level Security (RLS) Policies for 5 User Roles

-- Enable RLS on all tables
ALTER TABLE produce_batches ENABLE ROW LEVEL SECURITY;
ALTER TABLE destinations ENABLE ROW LEVEL SECURITY;
ALTER TABLE vehicles ENABLE ROW LEVEL SECURITY;
ALTER TABLE routes ENABLE ROW LEVEL SECURITY;
ALTER TABLE orders ENABLE ROW LEVEL SECURITY;
ALTER TABLE dispatch_plans ENABLE ROW LEVEL SECURITY;
ALTER TABLE audit_logs ENABLE ROW LEVEL SECURITY;

-- Helper function to extract user role from auth JWT
CREATE OR REPLACE FUNCTION auth.get_user_role()
RETURNS TEXT AS $$
    SELECT coalesce(
        current_setting('request.jwt.claims', true)::jsonb->'app_metadata'->>'role',
        current_setting('request.jwt.claims', true)::jsonb->'user_metadata'->>'role',
        'distributor' -- Default fallback during public demonstration
    );
$$ LANGUAGE sql STABLE;

-- 1. Produce Batches Policies
CREATE POLICY "Public Read Access for Produce Batches"
ON produce_batches FOR SELECT
TO authenticated, anon
USING (true);

CREATE POLICY "Distributor Full Write on Batches"
ON produce_batches FOR ALL
TO authenticated
USING (auth.get_user_role() IN ('distributor', 'collection_centre_worker'))
WITH CHECK (auth.get_user_role() IN ('distributor', 'collection_centre_worker'));

-- 2. Destinations Policies
CREATE POLICY "Public Read Access for Destinations"
ON destinations FOR SELECT
TO authenticated, anon
USING (true);

CREATE POLICY "Distributor Manage Destinations"
ON destinations FOR ALL
TO authenticated
USING (auth.get_user_role() = 'distributor')
WITH CHECK (auth.get_user_role() = 'distributor');

-- 3. Vehicles Policies
CREATE POLICY "Public Read Access for Vehicles"
ON vehicles FOR SELECT
TO authenticated, anon
USING (true);

CREATE POLICY "Fleet Write Access"
ON vehicles FOR ALL
TO authenticated
USING (auth.get_user_role() IN ('distributor', 'rental_vehicle_owner'))
WITH CHECK (auth.get_user_role() IN ('distributor', 'rental_vehicle_owner'));

-- 4. Routes Policies
CREATE POLICY "Public Read Access for Routes"
ON routes FOR SELECT
TO authenticated, anon
USING (true);

CREATE POLICY "Distributor Manage Routes"
ON routes FOR ALL
TO authenticated
USING (auth.get_user_role() = 'distributor')
WITH CHECK (auth.get_user_role() = 'distributor');

-- 5. Orders Policies
CREATE POLICY "Public Read Access for Orders"
ON orders FOR SELECT
TO authenticated, anon
USING (true);

CREATE POLICY "Seller and Distributor Manage Orders"
ON orders FOR ALL
TO authenticated
USING (auth.get_user_role() IN ('distributor', 'seller'))
WITH CHECK (auth.get_user_role() IN ('distributor', 'seller'));

-- 6. Dispatch Plans Policies
CREATE POLICY "Public Read Access for Dispatch Plans"
ON dispatch_plans FOR SELECT
TO authenticated, anon
USING (true);

CREATE POLICY "Distributor Manage Dispatch Plans"
ON dispatch_plans FOR ALL
TO authenticated
USING (auth.get_user_role() = 'distributor')
WITH CHECK (auth.get_user_role() = 'distributor');

-- 7. Audit Logs Policies
CREATE POLICY "Audit Logs Insert Access"
ON audit_logs FOR INSERT
TO authenticated, anon
WITH CHECK (true);

CREATE POLICY "Distributor View Audit Logs"
ON audit_logs FOR SELECT
TO authenticated
USING (auth.get_user_role() = 'distributor');
