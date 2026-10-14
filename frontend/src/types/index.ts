// ─── Core domain types ─────────────────────────────────────────────────────

export type QualityGrade = 'A' | 'B' | 'C';
export type ProvenanceType = 'real' | 'estimated' | 'simulated';
export type RiskLevel = 'low' | 'medium' | 'high' | 'expired';
export type VehicleStatus = 'available' | 'in_transit' | 'maintenance' | 'unavailable';
export type VehicleType = 'normal' | 'refrigerated';
export type PlanStatus = 'draft' | 'validating' | 'valid' | 'invalid' | 'executed';
export type ValidationStatus = 'pending' | 'valid' | 'invalid';
export type OrderStatus = 'pending' | 'confirmed' | 'dispatched' | 'delivered' | 'cancelled';
export type UserRole = 'distributor' | 'collection_centre_worker' | 'seller' | 'driver' | 'rental_vehicle_owner';

// ─── User / Profile ─────────────────────────────────────────────────────────

export interface Profile {
  id: string;
  display_name: string;
  role: UserRole;
  created_at: string;
}

// ─── Commodities ─────────────────────────────────────────────────────────────

export interface Commodity {
  id: string;
  name: string;
  base_shelf_life_hours: number;
  reference_temperature_c?: number;
  provenance: ProvenanceType;
}

// ─── Collection Centres ──────────────────────────────────────────────────────

export interface CollectionCentre {
  id: string;
  name: string;
  location_description: string;
  latitude?: number;
  longitude?: number;
  created_at: string;
}

// ─── Batches ─────────────────────────────────────────────────────────────────

export interface Batch {
  id: string;
  batch_code: string;
  commodity_id: string;
  commodity?: Commodity;
  collection_centre_id: string;
  collection_centre?: CollectionCentre;
  quantity_kg: number;
  remaining_shelf_life_hours: number;
  quality_grade: QualityGrade;
  arrival_time: string;
  shelf_life_low_hours?: number;
  shelf_life_high_hours?: number;
  provenance: ProvenanceType;
  risk_level?: RiskLevel;
  created_at: string;
  updated_at: string;
}

// ─── Destinations ─────────────────────────────────────────────────────────────

export interface Destination {
  id: string;
  name: string;
  location_description: string;
  latitude?: number;
  longitude?: number;
  demand_kg: number;
  confirmed_order_kg: number;
  predicted_demand_kg: number;
  base_price_inr_per_kg: number;
  handling_time_hours: number;
  handling_cost_inr_per_kg: number;
  delivery_window_start?: string;
  delivery_window_end?: string;
  provenance: ProvenanceType;
}

// ─── Orders ──────────────────────────────────────────────────────────────────

export interface Order {
  id: string;
  destination_id: string;
  destination?: Destination;
  commodity_id: string;
  commodity?: Commodity;
  quantity_kg: number;
  confirmed: boolean;
  due_time?: string;
  status: OrderStatus;
  created_at: string;
}

// ─── Vehicles ────────────────────────────────────────────────────────────────

export interface Vehicle {
  id: string;
  vehicle_code: string;
  vehicle_type: VehicleType;
  capacity_kg: number;
  cost_per_trip_inr: number;
  availability_start?: string;
  availability_end?: string;
  cabin_temperature_c?: number;
  status: VehicleStatus;
}

// ─── Routes ──────────────────────────────────────────────────────────────────

export interface Route {
  id: string;
  origin_id: string;
  origin?: CollectionCentre;
  destination_id: string;
  destination?: Destination;
  travel_time_hours: number;
  transport_cost_inr: number;
  travel_time_low_hours?: number;
  travel_time_high_hours?: number;
}

// ─── Dispatch Recommendations ────────────────────────────────────────────────

export interface DispatchRecommendation {
  id: string;
  plan_id: string;
  batch_id: string;
  batch?: Batch;
  destination_id: string;
  destination?: Destination;
  vehicle_id: string;
  vehicle?: Vehicle;
  quantity_kg: number;
  discount_percent: number;
  original_price_inr_per_kg: number;
  recommended_price_inr_per_kg: number;
  estimated_revenue_inr: number;
  estimated_cost_inr: number;
  estimated_net_value_inr: number;
  explanation: string;
  confidence_label?: string;
  validation_status: ValidationStatus;
}

// ─── Plans ───────────────────────────────────────────────────────────────────

export interface Plan {
  id: string;
  created_by: string;
  strategy: PlanStrategy;
  scenario_id?: string;
  status: PlanStatus;
  objective_value_inr: number;
  optimizer_method: string;
  solver_status: string;
  recommendations?: DispatchRecommendation[];
  violations?: ConstraintViolation[];
  created_at: string;
}

export type PlanStrategy = 'freshroute' | 'fefo' | 'highest_price' | 'greedy';

// ─── Constraint Violations ───────────────────────────────────────────────────

export interface ConstraintViolation {
  constraint_id: string;
  affected_entity: string;
  actual_value: number;
  allowed_value: number;
  reason: string;
}

// ─── Evaluations ─────────────────────────────────────────────────────────────

export interface Evaluation {
  id: string;
  plan_id: string;
  strategy: PlanStrategy;
  scenario_id?: string;
  spoilage_percent: number;
  demand_fulfilment_percent: number;
  unmet_demand_kg: number;
  net_value_inr: number;
  transport_cost_inr: number;
  discount_cost_inr: number;
  violation_count: number;
  runtime_seconds: number;
  created_at: string;
}

// ─── Scenarios ───────────────────────────────────────────────────────────────

export type ScenarioType =
  | 'normal'
  | 'shelf_life_reduced'
  | 'demand_increased'
  | 'demand_decreased'
  | 'travel_time_increased'
  | 'vehicle_unavailable'
  | 'new_order'
  | 'custom';

export interface Scenario {
  id: string;
  name: string;
  description: string;
  scenario_type: ScenarioType;
  parameter_overrides: Record<string, unknown>;
  is_held_out: boolean;
  provenance: ProvenanceType;
}

// ─── Discount ────────────────────────────────────────────────────────────────

export interface DiscountOption {
  discount_percent: number;
  recommended_price_inr_per_kg: number;
  expected_quantity_kg: number;
  estimated_revenue_inr: number;
  transport_cost_inr: number;
  handling_cost_inr: number;
  net_value_inr: number;
  demand_response_assumption: string;
}

export interface DiscountRecommendation {
  batch_id: string;
  batch?: Batch;
  destination_id: string;
  destination?: Destination;
  recommended_action: 'sell_full' | 'discount' | 'redirect' | 'salvage' | 'no_option';
  recommended_discount_percent: number;
  options: DiscountOption[];
  explanation: string;
  assumptions: string[];
  uncertainty_note: string;
  walk_away_price_available: boolean;
}

// ─── Dashboard Summary ───────────────────────────────────────────────────────

export interface DashboardSummary {
  total_inventory_kg: number;
  high_risk_batch_count: number;
  expired_batch_count: number;
  planned_dispatch_count: number;
  demand_fulfilment_percent: number;
  spoilage_percent: number;
  net_economic_value_inr: number;
  constraint_violations: number;
  data_mode: 'live' | 'sample';
}

// ─── API helpers ─────────────────────────────────────────────────────────────

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  size: number;
}

export interface ApiError {
  detail: string;
  status?: number;
}

export interface AssumptionItem {
  category: string;
  parameter: string;
  value: string | number;
  source: ProvenanceType;
  note: string;
}
