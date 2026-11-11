import math

from hypothesis import given, strategies as st
from fuel_station import parse_purchase, volume_average, payable_bill


# ---------------------------------------------------------------
# 1. parse_purchase
# ---------------------------------------------------------------
@given(st.text() | st.none())
def test_parse_purchase_no_crash(s):
    try:
        parse_purchase(s)
    except Exception as e:
        assert False, f"parse_purchase crashed with: {type(e).__name__}: {e}"


@given(st.text() | st.none())
def test_parse_purchase_output_is_valid(s):
    """Result must be None, or a (non-empty grade, finite litres >= 0) tuple."""
    result = parse_purchase(s)
    if result is not None:
        grade, litres = result
        assert isinstance(grade, str) and grade != ""
        assert math.isfinite(litres) and litres >= 0


@given(st.text(alphabet="abcdefghijklmnopqrstuvwxyz", min_size=1),
       st.floats(min_value=0, max_value=1e6, allow_nan=False, allow_infinity=False))
def test_parse_purchase_valid_input_roundtrip(grade, litres):
    """Well-formed input must always be parsed correctly."""
    result = parse_purchase(f"{grade}:{litres}")
    assert result == (grade.title(), litres)


# ---------------------------------------------------------------
# 2. volume_average
# ---------------------------------------------------------------
@given(st.text() | st.none())
def test_volume_average_no_crash(s):
    try:
        volume_average(s)
    except Exception as e:
        assert False, f"volume_average crashed with: {type(e).__name__}: {e}"


@given(st.text() | st.none())
def test_volume_average_output_is_valid(s):
    result = volume_average(s)
    assert result is None or (math.isfinite(result) and result >= 0)


@given(st.lists(st.integers(min_value=0, max_value=100000), min_size=1))
def test_volume_average_valid_list_is_between_min_and_max(nums):
    """The average of valid volumes must lie between the min and the max."""
    result = volume_average(",".join(map(str, nums)))
    assert min(nums) <= result <= max(nums)


# ---------------------------------------------------------------
# 3. payable_bill
# ---------------------------------------------------------------
@given(st.text() | st.none())
def test_payable_bill_no_crash(s):
    try:
        payable_bill(s)
    except Exception as e:
        assert False, f"payable_bill crashed with: {type(e).__name__}: {e}"


@given(st.text() | st.none())
def test_payable_bill_output_is_valid(s):
    result = payable_bill(s)
    assert result is None or (math.isfinite(result) and result >= 0)


@given(st.floats(min_value=0, max_value=1e7, allow_nan=False, allow_infinity=False),
       st.floats(min_value=0, max_value=1e7, allow_nan=False, allow_infinity=False))
def test_payable_bill_valid_input_never_negative(bill, discount):
    result = payable_bill(f"{bill}|{discount}")
    assert result is not None and result >= 0