-- FreshRoute AI Database Schema Migration 03
-- Performance Indexes, Auto-updating Triggers, and Analytical Views

-- 1. Performance Indexes
CREATE INDEX IF NOT EXISTS idx_batches_commodity ON produce_batches(commodity);
CREATE INDEX IF NOT EXISTS idx_batches_rsl ON produce_batches(remaining_shelf_life_hours);
CREATE INDEX IF NOT EXISTS idx_batches_urgency ON produce_batches(urgency_level);
CREATE INDEX IF NOT EXISTS idx_batches_current_qty ON produce_batches(current_quantity_kg) WHERE current_quantity_kg > 0;

CREATE INDEX IF NOT EXISTS idx_orders_destination ON orders(destination_id);
CREATE INDEX IF NOT EXISTS idx_orders_commodity ON orders(commodity);
CREATE INDEX IF NOT EXISTS idx_orders_status ON orders(status);

CREATE INDEX IF NOT EXISTS idx_vehicles_status ON vehicles(status);
CREATE INDEX IF NOT EXISTS idx_vehicles_reefer ON vehicles(is_refrigerated);

CREATE INDEX IF NOT EXISTS idx_routes_dest_origin ON routes(origin_name, destination_id);

-- 2. Auto-update updated_at timestamp trigger function
CREATE OR REPLACE FUNCTION trigger_set_timestamp()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Apply triggers
DROP TRIGGER IF EXISTS set_timestamp_batches ON produce_batches;
CREATE TRIGGER set_timestamp_batches
BEFORE UPDATE ON produce_batches
FOR EACH ROW EXECUTE PROCEDURE trigger_set_timestamp();

DROP TRIGGER IF EXISTS set_timestamp_destinations ON destinations;
CREATE TRIGGER set_timestamp_destinations
BEFORE UPDATE ON destinations
FOR EACH ROW EXECUTE PROCEDURE trigger_set_timestamp();

DROP TRIGGER IF EXISTS set_timestamp_vehicles ON vehicles;
CREATE TRIGGER set_timestamp_vehicles
BEFORE UPDATE ON vehicles
FOR EACH ROW EXECUTE PROCEDURE trigger_set_timestamp();

DROP TRIGGER IF EXISTS set_timestamp_routes ON routes;
CREATE TRIGGER set_timestamp_routes
BEFORE UPDATE ON routes
FOR EACH ROW EXECUTE PROCEDURE trigger_set_timestamp();

DROP TRIGGER IF EXISTS set_timestamp_orders ON orders;
CREATE TRIGGER set_timestamp_orders
BEFORE UPDATE ON orders
FOR EACH ROW EXECUTE PROCEDURE trigger_set_timestamp();

-- 3. Analytical View: At-Risk Inventory Monitor
CREATE OR REPLACE VIEW v_at_risk_batches AS
SELECT 
    id,
    batch_code,
    commodity,
    variety,
    current_quantity_kg,
    remaining_shelf_life_hours,
    storage_condition,
    procurement_cost_per_kg,
    (current_quantity_kg * procurement_cost_per_kg) AS financial_exposure_inr,
    CASE 
        WHEN remaining_shelf_life_hours < 12.0 THEN 'critical'
        WHEN remaining_shelf_life_hours < 24.0 THEN 'high'
        WHEN remaining_shelf_life_hours < 48.0 THEN 'normal'
        ELSE 'low'
    END AS computed_urgency
FROM produce_batches
WHERE current_quantity_kg > 0 AND remaining_shelf_life_hours < 36.0
ORDER BY remaining_shelf_life_hours ASC;
