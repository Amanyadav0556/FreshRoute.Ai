"""Evaluation and multi-strategy benchmark comparison schemas."""
from pydantic import Field
from typing import Optional, List, Dict
from datetime import datetime
from app.schemas.common import BaseDomainModel


class StrategyMetrics(BaseDomainModel):
    strategy_name: str
    strategy_label: str
    is_optimizer: bool = False
    net_economic_value_inr: float
    total_revenue_inr: float
    total_transport_cost_inr: float
    spoilage_quantity_kg: float
    spoilage_rate_percent: float
    order_fulfillment_rate_percent: float
    avg_delivery_freshness_hours: float
    fleet_utilization_percent: float
    computation_time_ms: float


class MetricComparison(BaseDomainModel):
    metric_key: str
    metric_label: str
    unit: str
    fefo_baseline: float
    highest_price_baseline: float
    greedy_baseline: float
    freshroute_optimizer: float
    improvement_vs_fefo_percent: float
    interpretation: str


class BenchmarkResult(BaseDomainModel):
    scenario_id: str
    scenario_name: str
    total_batch_volume_kg: float
    total_market_demand_kg: float
    strategies: List[StrategyMetrics]
    comparisons: List[MetricComparison]
    evaluated_at: datetime
    notes: str = "Benchmark runs simulated simultaneously on identical produce inventory, vehicle fleets, and demand orders."
