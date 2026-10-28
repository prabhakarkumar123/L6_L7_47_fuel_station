import pytest

from fuel_station import fuel_bill, pump_allowed, session_status


# Test fuel bill branches
@pytest.mark.parametrize(
    "grade, litres, loyalty_tier, expected",
    [
        ("regular", 8, "silver", 0),
        ("premium", 20, "gold", 0),
        ("regular", 20, "silver", 1050),
        ("premium", 25, "gold", 525),
        ("diesel", 25, "silver", 450),
        ("diesel", 25, "gold", 450),
        ("regular", 41, "silver", 31 * 99),
        ("regular", 46, "gold", 31 * 95),
        ("diesel", 55, "silver", 35 * 84),
        ("diesel", 55, "gold", 35 * 80),
    ],
)
def test_fuel_bill_branches(grade, litres, loyalty_tier, expected):
    assert fuel_bill(grade, litres, loyalty_tier) == expected


# Test invalid inputs
@pytest.mark.parametrize(
    "grade, litres, loyalty_tier, error",
    [
        ("electric", 10, "silver", "unknown fuel grade"),
        ("regular", -1, "silver", "invalid litres"),
    ],
)
def test_fuel_bill_errors(grade, litres, loyalty_tier, error):
    with pytest.raises(ValueError, match=error):
        fuel_bill(grade, litres, loyalty_tier)


# Test pump restrictions
@pytest.mark.parametrize(
    "litres, containers, is_fleet, expected",
    [
        (200, 4, True, True),
        (201, 1, True, False),
        (60, 1, False, True),
        (61, 1, False, False),
        (60, 2, False, False),
    ],
)
def test_pump_allowed_branches(litres, containers, is_fleet, expected):
    assert pump_allowed(litres, containers, is_fleet) is expected


# Test session-status branches
@pytest.mark.parametrize(
    "seconds, card, night, expected",
    [
        (60, True, False, "active"),
        (45, True, False, "warning"),
        (44, True, False, "timed_out"),
        (30, False, False, "active"),
        (15, False, False, "warning"),
        (14, False, False, "timed_out"),
        (90, True, True, "active"),
        (75, True, True, "warning"),
        (74, True, True, "timed_out"),
        (60, False, True, "active"),
        (45, False, True, "warning"),
        (44, False, True, "timed_out"),
    ],
)
def test_session_status_branches(seconds, card, night, expected):
    assert session_status(seconds, card, night) == expected