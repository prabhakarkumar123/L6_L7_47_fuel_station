import pytest

from fuel_station import fuel_bill, pump_allowed, session_status


# Test invalid inputs
def test_fuel_bill_unknown_grade():
    with pytest.raises(ValueError, match="unknown fuel grade"):
        fuel_bill("electric", 10, "silver")


def test_fuel_bill_negative_litres():
    with pytest.raises(ValueError, match="invalid litres"):
        fuel_bill("regular", -1, "silver")


# Test fuel bill calculations
def test_fuel_bill_covered_regular():
    assert fuel_bill("regular", 8, "silver") == 0


def test_fuel_bill_gold_regular_bonus():
    assert fuel_bill("regular", 15, "gold") == 0


def test_fuel_bill_regular_positive_extra():
    assert fuel_bill("regular", 20, "silver") == 1050


def test_fuel_bill_diesel_rate():
    assert fuel_bill("diesel", 25, "silver") == 450


def test_fuel_bill_large_extra_regular():
    assert fuel_bill("regular", 45, "silver") == 35 * 99


def test_fuel_bill_large_extra_gold():
    assert fuel_bill("regular", 50, "gold") == 35 * 95


def test_fuel_bill_gold_diesel_gets_no_bonus():
    assert fuel_bill("diesel", 25, "gold") == 450


# Test pump restrictions
def test_pump_allowed_fleet_within_limit():
    assert pump_allowed(200, 4, True) is True


def test_pump_allowed_fleet_over_limit():
    assert pump_allowed(201, 1, True) is False


def test_pump_allowed_non_fleet_over_litres():
    assert pump_allowed(61, 1, False) is False


def test_pump_allowed_non_fleet_multiple_containers():
    assert pump_allowed(50, 2, False) is False


def test_pump_allowed_non_fleet_valid_request():
    assert pump_allowed(30, 1, False) is True


# Test pump session status
def test_session_card_active_day():
    assert session_status(60, True, False) == "active"


def test_session_card_warning_day():
    assert session_status(45, True, False) == "warning"


def test_session_card_timed_out_day():
    assert session_status(44, True, False) == "timed_out"


def test_session_cash_active_day():
    assert session_status(30, False, False) == "active"


def test_session_night_active():
    assert session_status(90, True, True) == "active"


def test_session_night_warning():
    assert session_status(75, True, True) == "warning"


def test_session_night_timed_out():
    assert session_status(74, True, True) == "timed_out"