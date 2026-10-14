"""Unit tests for HiGHS LP and Greedy heuristic optimization solvers."""
import pytest
from app.services.optimizer.highs_solver import solve_with_highs
from app.services.optimizer.greedy_solver import solve_with_greedy
from app.db.sample_data import (
    SAMPLE_BATCHES,
    SAMPLE_DESTINATIONS,
    SAMPLE_VEHICLES,
    SAMPLE_ROUTES,
    SAMPLE_ORDERS,
)


def test_highs_solver_generates_valid_allocations():
    plan = solve_with_highs(
        batches=SAMPLE_BATCHES,
        destinations=SAMPLE_DESTINATIONS,
        vehicles=SAMPLE_VEHICLES,
        routes=SAMPLE_ROUTES,
        orders=SAMPLE_ORDERS,
        strategy="balanced",
    )

    assert plan is not None
    assert len(plan.allocations) > 0
    assert plan.total_allocated_kg > 0
    assert plan.net_economic_value_inr > 0
    assert plan.validation.is_valid is True
    assert plan.validation.passed_checks == 6


def test_greedy_solver_fallback_behavior():
    plan = solve_with_greedy(
        batches=SAMPLE_BATCHES,
        destinations=SAMPLE_DESTINATIONS,
        vehicles=SAMPLE_VEHICLES,
        routes=SAMPLE_ROUTES,
        orders=SAMPLE_ORDERS,
        strategy="max_margin",
    )

    assert plan is not None
    assert len(plan.allocations) > 0
    assert plan.total_revenue_inr > 0
    assert plan.validation.is_valid is True


def test_different_strategies_affect_allocations():
    plan_margin = solve_with_greedy(
        batches=SAMPLE_BATCHES,
        destinations=SAMPLE_DESTINATIONS,
        vehicles=SAMPLE_VEHICLES,
        routes=SAMPLE_ROUTES,
        orders=SAMPLE_ORDERS,
        strategy="max_margin",
    )
    plan_spoil = solve_with_greedy(
        batches=SAMPLE_BATCHES,
        destinations=SAMPLE_DESTINATIONS,
        vehicles=SAMPLE_VEHICLES,
        routes=SAMPLE_ROUTES,
        orders=SAMPLE_ORDERS,
        strategy="min_spoilage",
    )

    assert plan_margin.strategy == "max_margin"
    assert plan_spoil.strategy == "min_spoilage"
