"""Unit tests for plan validator and constraint boundary checks."""
import pytest
from app.services.optimizer.validator import validate_dispatch_plan
from app.schemas.plan import PlanItem
from app.db.sample_data import SAMPLE_BATCHES, SAMPLE_VEHICLES, SAMPLE_DESTINATIONS


def test_validator_passes_compliant_allocation():
    allocations = [
        PlanItem(
            batch_id=SAMPLE_BATCHES[0]["id"],
            batch_code=SAMPLE_BATCHES[0]["batch_code"],
            commodity="Tomatoes",
            destination_id=SAMPLE_DESTINATIONS[0]["id"],
            destination_name=SAMPLE_DESTINATIONS[0]["name"],
            vehicle_id=SAMPLE_VEHICLES[0]["id"],
            vehicle_plate=SAMPLE_VEHICLES[0]["plate_number"],
            allocated_quantity_kg=500.0,
            offered_price_per_kg=28.0,
            effective_selling_price_per_kg=28.0,
            estimated_revenue_inr=14000.0,
            estimated_transport_cost_inr=2200.0,
            estimated_spoilage_risk_percent=12.0,
            remaining_shelf_life_on_arrival_hours=10.5,
            net_economic_value_inr=2800.0,
            dispatch_explanation="Valid sample allocation.",
        )
    ]

    result = validate_dispatch_plan(allocations, SAMPLE_BATCHES, SAMPLE_VEHICLES, SAMPLE_DESTINATIONS)
    assert result.is_valid is True
    assert result.failed_checks == 0


def test_validator_fails_on_vehicle_overload():
    # Attempt to allocate 5000kg on Tata Ace (750kg capacity)
    overloaded_allocations = [
        PlanItem(
            batch_id=SAMPLE_BATCHES[0]["id"],
            batch_code=SAMPLE_BATCHES[0]["batch_code"],
            commodity="Tomatoes",
            destination_id=SAMPLE_DESTINATIONS[0]["id"],
            destination_name=SAMPLE_DESTINATIONS[0]["name"],
            vehicle_id="veh-001",
            vehicle_plate="MH 15 EF 3201",
            allocated_quantity_kg=5000.0,
            offered_price_per_kg=28.0,
            effective_selling_price_per_kg=28.0,
            estimated_revenue_inr=140000.0,
            estimated_transport_cost_inr=2200.0,
            estimated_spoilage_risk_percent=12.0,
            remaining_shelf_life_on_arrival_hours=10.5,
            net_economic_value_inr=28000.0,
            dispatch_explanation="Overloaded vehicle test.",
        )
    ]

    result = validate_dispatch_plan(overloaded_allocations, SAMPLE_BATCHES, SAMPLE_VEHICLES, SAMPLE_DESTINATIONS)
    assert result.is_valid is False
    assert result.failed_checks > 0
    cap_check = next(c for c in result.checks if c.rule_name == "Capacity Non-Exceedance")
    assert cap_check.passed is False
