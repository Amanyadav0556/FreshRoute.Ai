-- FreshRoute AI Supabase Seed Script
-- Populates Maharashtra perishable agri corridor: Nashik Central Hub -> Mumbai/Pune mandis

-- 1. Destinations
INSERT INTO destinations (id, name, city, state, latitude, longitude, market_type, unloading_handling_fee_per_kg, avg_selling_price_multiplier, daily_demand_capacity_kg, provenance, provenance_source, active_orders_count)
VALUES
('dest-vashi-01', 'Vashi APMC Mandi Hub', 'Navi Mumbai', 'Maharashtra', 19.0760, 72.9986, 'wholesale_mandi', 0.60, 1.15, 25000.0, 'real', 'APMC Market Board', 4),
('dest-dadar-02', 'Dadar Wholesale Flower & Produce Market', 'Mumbai', 'Maharashtra', 19.0178, 72.8478, 'wholesale_mandi', 0.75, 1.25, 15000.0, 'real', 'MCGM Directory', 3),
('dest-pune-03', 'Gultekdi Market Yard', 'Pune', 'Maharashtra', 18.4965, 73.8647, 'wholesale_mandi', 0.50, 1.08, 20000.0, 'real', 'Pune APMC', 3),
('dest-kalyan-04', 'Kalyan Regional Aggregation Market', 'Thane/Kalyan', 'Maharashtra', 19.2403, 73.1305, 'wholesale_mandi', 0.45, 1.02, 12000.0, 'real', 'Thane Portal', 2),
('dest-processor-05', 'Sahyadri Agro Processing Park', 'Dindori / Nashik', 'Maharashtra', 20.1580, 73.8340, 'processor', 0.25, 0.78, 35000.0, 'real', 'Sahyadri FPC', 2),
('dest-retail-06', 'Blinkit Dark Store Hub Kurla', 'Mumbai', 'Maharashtra', 19.0657, 72.8794, 'modern_retail', 0.85, 1.30, 8000.0, 'estimated', 'Quick Commerce Model', 3)
ON CONFLICT (id) DO UPDATE SET name = EXCLUDED.name;

-- 2. Vehicles
INSERT INTO vehicles (id, plate_number, model_type, vehicle_category, capacity_kg, is_refrigerated, fixed_booking_cost_inr, per_km_cost_inr, avg_speed_kmh, current_location, owner_role, status, provenance)
VALUES
('veh-001', 'MH 15 EF 3201', 'Tata Ace Gold', 'mini_truck', 750.0, FALSE, 350.0, 11.50, 42.0, 'Nashik Central Hub', 'owned', 'available', 'real'),
('veh-002', 'MH 15 GH 4892', 'Mahindra Bolero Maxi Truck', 'mini_truck', 1500.0, FALSE, 500.0, 14.00, 45.0, 'Nashik Central Hub', 'owned', 'available', 'real'),
('veh-003', 'MH 12 QW 8810', 'Eicher Pro 2049 Reefer', 'reefer', 2800.0, TRUE, 1200.0, 22.00, 50.0, 'Nashik Central Hub', 'rental', 'available', 'real'),
('veh-004', 'MH 15 AK 9923', 'Ashok Leyland Dost+', 'mini_truck', 1250.0, FALSE, 450.0, 13.00, 46.0, 'Nashik Central Hub', 'owned', 'available', 'real'),
('veh-005', 'MH 14 TY 5519', 'Tata 407 LPT Reefer', 'reefer', 3500.0, TRUE, 1500.0, 24.50, 48.0, 'Nashik Central Hub', 'rental', 'available', 'real'),
('veh-006', 'MH 15 BN 7711', 'Mahindra Bolero Maxi Truck', 'mini_truck', 1500.0, FALSE, 500.0, 14.00, 45.0, 'Sangamner Sub-Centre', 'contracted', 'available', 'real')
ON CONFLICT (id) DO UPDATE SET status = EXCLUDED.status;

-- 3. Routes
INSERT INTO routes (id, origin_name, destination_id, destination_name, distance_km, standard_travel_time_hours, toll_charges_inr, road_quality_factor, ambient_temp_celsius, effective_travel_time_hours, provenance)
VALUES
('route-nsk-vashi', 'Nashik Central Hub', 'dest-vashi-01', 'Vashi APMC Mandi Hub', 168.0, 3.8, 380.0, 1.05, 31.0, 4.0, 'real'),
('route-nsk-dadar', 'Nashik Central Hub', 'dest-dadar-02', 'Dadar Wholesale Flower & Produce Market', 175.0, 4.2, 420.0, 1.15, 32.5, 4.8, 'real'),
('route-nsk-pune', 'Nashik Central Hub', 'dest-pune-03', 'Gultekdi Market Yard', 210.0, 4.8, 310.0, 1.10, 29.0, 5.2, 'real'),
('route-nsk-kalyan', 'Nashik Central Hub', 'dest-kalyan-04', 'Kalyan Regional Aggregation Market', 135.0, 3.0, 290.0, 1.08, 30.5, 3.2, 'real'),
('route-nsk-processor', 'Nashik Central Hub', 'dest-processor-05', 'Sahyadri Agro Processing Park', 28.0, 0.75, 0.0, 1.00, 27.0, 0.75, 'real'),
('route-nsk-retail', 'Nashik Central Hub', 'dest-retail-06', 'Blinkit Dark Store Hub Kurla', 165.0, 3.9, 380.0, 1.12, 31.5, 4.4, 'estimated')
ON CONFLICT (id) DO UPDATE SET distance_km = EXCLUDED.distance_km;

-- 4. Produce Batches
INSERT INTO produce_batches (id, batch_code, commodity, variety, collection_centre_id, initial_quantity_kg, current_quantity_kg, harvest_date, initial_shelf_life_hours, remaining_shelf_life_hours, storage_condition, procurement_cost_per_kg, min_selling_price_per_kg, quality_grade, urgency_level, spoilage_risk_percent, provenance)
VALUES
('batch-tom-001', 'BATCH-NSK-TOM-01', 'Tomatoes', 'Hybrid Abhinav', 'hub-nashik-01', 2500.0, 2500.0, NOW() - INTERVAL '34 hours', 72.0, 14.5, 'ambient', 18.0, 22.0, 'Grade A', 'high', 35.0, 'real'),
('batch-spin-002', 'BATCH-NSK-SPN-02', 'Spinach (Palak)', 'All Green Desi', 'hub-nashik-01', 950.0, 950.0, NOW() - INTERVAL '18 hours', 28.0, 9.2, 'ambient', 12.0, 16.0, 'Grade A', 'critical', 68.0, 'real'),
('batch-grp-003', 'BATCH-NSK-GRP-03', 'Grapes', 'Thomson Seedless Export Cull', 'hub-nashik-01', 3200.0, 3200.0, NOW() - INTERVAL '24 hours', 120.0, 78.0, 'precool', 45.0, 55.0, 'Grade A', 'low', 8.0, 'real'),
('batch-oni-004', 'BATCH-NSK-ONI-04', 'Onions', 'Nashik Garva Red', 'hub-nashik-01', 5000.0, 5000.0, NOW() - INTERVAL '4 days', 480.0, 384.0, 'ambient', 20.0, 25.0, 'Grade A', 'low', 4.0, 'real'),
('batch-mng-005', 'BATCH-NSK-MNG-05', 'Mangoes', 'Kesar Semi-Ripe', 'hub-nashik-01', 1800.0, 1800.0, NOW() - INTERVAL '48 hours', 96.0, 26.0, 'ambient', 65.0, 85.0, 'Grade B', 'normal', 22.0, 'real'),
('batch-cap-006', 'BATCH-NSK-CAP-06', 'Capsicum (Bell Pepper)', 'Green Wonder', 'hub-nashik-01', 1400.0, 1400.0, NOW() - INTERVAL '30 hours', 60.0, 16.5, 'ambient', 28.0, 36.0, 'Grade A', 'high', 38.0, 'real')
ON CONFLICT (id) DO UPDATE SET current_quantity_kg = EXCLUDED.current_quantity_kg;

-- 5. Orders
INSERT INTO orders (id, order_code, destination_id, destination_name, commodity, variety, demanded_quantity_kg, offered_price_per_kg, delivery_deadline, min_acceptable_grade, min_shelf_life_upon_arrival_hours, penalty_per_kg_unfulfilled, allocated_quantity_kg, fulfillment_rate_percent, status, provenance)
VALUES
('ord-vashi-01', 'ORD-VSH-TOM-01', 'dest-vashi-01', 'Vashi APMC Mandi Hub', 'Tomatoes', 'Hybrid Abhinav', 2000.0, 28.50, NOW() + INTERVAL '10 hours', 'Grade B', 8.0, 3.0, 0.0, 0.0, 'pending', 'real'),
('ord-dadar-02', 'ORD-DDR-SPN-02', 'dest-dadar-02', 'Dadar Wholesale Flower & Produce Market', 'Spinach (Palak)', 'All Green Desi', 800.0, 24.00, NOW() + INTERVAL '7 hours', 'Grade A', 4.0, 4.5, 0.0, 0.0, 'pending', 'real'),
('ord-retail-03', 'ORD-BLK-MNG-03', 'dest-retail-06', 'Blinkit Dark Store Hub Kurla', 'Mangoes', 'Kesar Semi-Ripe', 1200.0, 110.00, NOW() + INTERVAL '12 hours', 'Grade A', 18.0, 12.0, 0.0, 0.0, 'pending', 'estimated'),
('ord-pune-04', 'ORD-PUN-GRP-04', 'dest-pune-03', 'Gultekdi Market Yard', 'Grapes', 'Thomson Seedless Export Cull', 2500.0, 68.00, NOW() + INTERVAL '18 hours', 'Grade B', 24.0, 5.0, 0.0, 0.0, 'pending', 'real'),
('ord-proc-05', 'ORD-PRC-TOM-05', 'dest-processor-05', 'Sahyadri Agro Processing Park', 'Tomatoes', 'Hybrid Abhinav', 4000.0, 19.50, NOW() + INTERVAL '24 hours', 'Grade C', 3.0, 1.0, 0.0, 0.0, 'pending', 'real')
ON CONFLICT (id) DO UPDATE SET status = EXCLUDED.status;
