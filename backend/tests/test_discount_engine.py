"""Unit tests for the 7-strategy discount pricing engine."""
import pytest
from app.services.discount_engine import evaluate_discount_strategies
from app.db.sample_data import SAMPLE_BATCHES


def test_discount_engine_generates_all_seven_options():
    batch = SAMPLE_BATCHES[0]  # Tomato batch
    rec = evaluate_discount_strategies(batch)

    assert rec.batch_id == batch["id"]
    assert rec.commodity == batch["commodity"]
    assert len(rec.options) == 7

    keys = {opt.strategy_key for opt in rec.options}
    expected_keys = {
        "no_discount",
        "dynamic_10",
        "clearance_20",
        "salvage_35",
        "elasticity_based",
        "auction_processor",
        "donation_tax",
    }
    assert keys == expected_keys


def test_discount_engine_sets_single_recommended_option():
    batch = SAMPLE_BATCHES[1]  # Critical spinach batch
    rec = evaluate_discount_strategies(batch)

    recommended_opts = [opt for opt in rec.options if opt.is_recommended]
    assert len(recommended_opts) == 1
    assert recommended_opts[0].strategy_key == rec.recommended_strategy


def test_processor_option_eliminates_spoilage():
    batch = SAMPLE_BATCHES[0]
    rec = evaluate_discount_strategies(batch)

    proc_opt = next(opt for opt in rec.options if opt.strategy_key == "auction_processor")
    assert proc_opt.expected_spoilage_kg == 0.0
    assert proc_opt.expected_clearance_kg == float(batch["current_quantity_kg"])
