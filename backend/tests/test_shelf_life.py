"""Unit tests for shelf life degradation and Arrhenius respiration physics."""
import pytest
from app.services.shelf_life import (
    calculate_temperature_acceleration,
    calculate_transit_shelf_life_consumption,
    estimate_spoilage_risk,
)


def test_temperature_acceleration():
    # At 20C (reference temp), acceleration factor must be exactly 1.0
    accel_20 = calculate_temperature_acceleration(20.0, "tomatoes")
    assert round(accel_20, 3) == 1.0

    # At 30C (+10C), acceleration factor must equal Q10 (~2.2 for tomatoes)
    accel_30 = calculate_temperature_acceleration(30.0, "tomatoes")
    assert round(accel_30, 2) == 2.20

    # At 10C (-10C), acceleration factor should be 1/2.2 ~ 0.455
    accel_10 = calculate_temperature_acceleration(10.0, "tomatoes")
    assert round(accel_10, 3) == round(1.0 / 2.2, 3)


def test_transit_consumption_refrigerated_vs_ambient():
    ambient_consumed = calculate_transit_shelf_life_consumption(
        transit_hours=4.0,
        ambient_temp_celsius=32.0,
        commodity="spinach (palak)",
        is_refrigerated=False,
    )
    reefer_consumed = calculate_transit_shelf_life_consumption(
        transit_hours=4.0,
        ambient_temp_celsius=32.0,
        commodity="spinach (palak)",
        is_refrigerated=True,
    )
    # Cold chain should preserve significantly more shelf life
    assert reefer_consumed < ambient_consumed
    assert reefer_consumed <= ambient_consumed * 0.40


def test_spoilage_risk_feasible_and_infeasible():
    # Plenty of shelf life remaining
    safe_risk = estimate_spoilage_risk(
        remaining_shelf_life_hours=48.0,
        transit_hours=3.5,
        ambient_temp_celsius=28.0,
        commodity="tomatoes",
        is_refrigerated=False,
    )
    assert safe_risk["is_feasible"] is True
    assert safe_risk["urgency_level"] == "low"
    assert safe_risk["spoilage_risk_percent"] <= 15.0

    # Batch that expires in transit
    expired_risk = estimate_spoilage_risk(
        remaining_shelf_life_hours=4.0,
        transit_hours=5.0,
        ambient_temp_celsius=35.0,
        commodity="spinach (palak)",
        is_refrigerated=False,
    )
    assert expired_risk["is_feasible"] is False
    assert expired_risk["spoilage_risk_percent"] == 100.0
    assert expired_risk["urgency_level"] == "critical"
