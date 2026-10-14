"""Perishable produce shelf-life degradation and spoilage modeling service.
Incorporates Arrhenius temperature acceleration, road vibration stress,
and refrigerated cold-chain deceleration.
"""
import math
from typing import Dict, Any


COMMODITY_BASE_Q10 = {
    "tomatoes": 2.2,
    "spinach (palak)": 2.8,
    "grapes": 2.0,
    "onions": 1.5,
    "mangoes": 2.4,
    "capsicum (bell pepper)": 2.1,
}

COMMODITY_REF_TEMP_C = 20.0  # Reference baseline temperature in Celsius


def get_q10_factor(commodity: str) -> float:
    for k, v in COMMODITY_BASE_Q10.items():
        if k in commodity.lower():
            return v
    return 2.2


def calculate_temperature_acceleration(temp_celsius: float, commodity: str) -> float:
    """Calculates thermal degradation multiplier using Q10 formula:
    Rate(T) / Rate(T_ref) = Q10 ^ ((T - T_ref) / 10)
    """
    q10 = get_q10_factor(commodity)
    delta_t = temp_celsius - COMMODITY_REF_TEMP_C
    exponent = delta_t / 10.0
    return float(math.pow(q10, exponent))


def calculate_transit_shelf_life_consumption(
    transit_hours: float,
    ambient_temp_celsius: float,
    commodity: str,
    is_refrigerated: bool,
    road_quality_factor: float = 1.0,
) -> float:
    """Estimates the effective hours of shelf life consumed during transit.
    If refrigerated, effective transit temp is held at ~4-6°C, decelerating degradation.
    Road vibration factor multiplies physical bruising stress.
    """
    if is_refrigerated:
        # Refrigerated transport maintains optimal produce temperature
        thermal_factor = 0.35
        vibration_factor = max(1.0, road_quality_factor * 0.8)
    else:
        thermal_factor = calculate_temperature_acceleration(ambient_temp_celsius, commodity)
        vibration_factor = max(1.0, road_quality_factor)

    effective_consumption_hours = transit_hours * thermal_factor * vibration_factor
    return round(effective_consumption_hours, 2)


def estimate_spoilage_risk(
    remaining_shelf_life_hours: float,
    transit_hours: float,
    ambient_temp_celsius: float,
    commodity: str,
    is_refrigerated: bool,
    road_quality_factor: float = 1.0,
    handling_buffer_hours: float = 2.0,
) -> Dict[str, Any]:
    """Calculates arrival shelf life and estimated spoilage probability percentage."""
    consumed_hours = calculate_transit_shelf_life_consumption(
        transit_hours=transit_hours,
        ambient_temp_celsius=ambient_temp_celsius,
        commodity=commodity,
        is_refrigerated=is_refrigerated,
        road_quality_factor=road_quality_factor,
    )

    remaining_on_arrival = remaining_shelf_life_hours - consumed_hours - handling_buffer_hours

    if remaining_on_arrival <= 0:
        spoilage_risk = 100.0
        is_feasible = False
        urgency = "critical"
    elif remaining_on_arrival < 8.0:
        spoilage_risk = round(70.0 + (8.0 - remaining_on_arrival) * 3.75, 1)
        is_feasible = True
        urgency = "high"
    elif remaining_on_arrival < 24.0:
        spoilage_risk = round(20.0 + (24.0 - remaining_on_arrival) * 2.5, 1)
        is_feasible = True
        urgency = "normal"
    else:
        spoilage_risk = round(max(2.0, 15.0 - (remaining_on_arrival - 24.0) * 0.2), 1)
        is_feasible = True
        urgency = "low"

    return {
        "consumed_hours": consumed_hours,
        "remaining_on_arrival_hours": max(0.0, round(remaining_on_arrival, 2)),
        "spoilage_risk_percent": min(100.0, spoilage_risk),
        "is_feasible": is_feasible,
        "urgency_level": urgency,
    }
