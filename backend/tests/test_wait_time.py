import pytest
from app.routers.wait_time import calculate_wait_time


def test_empty_queue():
    """Test wait time with no orders."""
    orders = []
    wait_time = calculate_wait_time(orders, baristas_available=3)
    assert wait_time == 0


def test_single_order():
    """Test wait time with one order of 2 items."""
    orders = [{"status": "queued", "items": ["latte", "cappuccino"]}]
    wait_time = calculate_wait_time(orders, baristas_available=1)
    # 2 items * 3 min per item = 6 minutes
    assert wait_time == 6


def test_multiple_orders():
    """Test wait time with multiple orders."""
    orders = [
        {"status": "queued", "items": ["espresso"]},
        {"status": "queued", "items": ["latte", "cappuccino"]},
        {"status": "in_progress", "items": ["americano"]},
    ]
    # Total: 1 + 2 + 1 = 4 items * 3 min = 12 minutes total
    wait_time = calculate_wait_time(orders, baristas_available=2)
    # 12 / 2 = 6 minutes
    assert wait_time == 6


def test_zero_baristas():
    """Test wait time with no baristas (edge case)."""
    orders = [{"status": "queued", "items": ["latte"]}]
    wait_time = calculate_wait_time(orders, baristas_available=0)
    # 1 item * 3 min = 3 minutes (no division by baristas)
    assert wait_time == 3


def test_ignores_ready_orders():
    """Test that ready/completed orders are not counted."""
    orders = [
        {"status": "ready", "items": ["espresso"]},
        {"status": "completed", "items": ["latte"]},
        {"status": "queued", "items": ["cappuccino"]},
    ]
    wait_time = calculate_wait_time(orders, baristas_available=1)
    # Only cappuccino counted: 1 * 3 = 3 minutes
    assert wait_time == 3
