import math


def _to_finite_float(value):
    """Convert text to a finite, non-negative float. Return None if invalid."""
    try:
        number = float(value)
    except (ValueError, TypeError, OverflowError):
        return None
    if not math.isfinite(number) or number < 0:   # rejects nan, inf, negatives
        return None
    return number


def parse_purchase(text):
    """Parse 'grade:litres' (e.g. 'diesel:25').

    Returns (Grade, litres) or None if the input is invalid.
    """
    if not isinstance(text, str):                 # None, int, list ...
        return None
    parts = text.split(':')
    if len(parts) != 2:                           # missing or extra ':'
        return None
    grade = parts[0].strip()
    litres = _to_finite_float(parts[1])
    if grade == "" or litres is None:             # empty grade / bad number
        return None
    return grade.title(), litres


def volume_average(volumes_csv):
    """Average of comma-separated pump volumes (e.g. '10,25,40').

    Returns a float, or None if the input is invalid.
    """
    if not isinstance(volumes_csv, str):
        return None
    values = []
    for item in volumes_csv.split(','):
        number = _to_finite_float(item)
        if number is None:                        # empty item, text, nan, negative
            return None
        values.append(number)
    if not values:                                # defensive: avoid ZeroDivisionError
        return None
    average = sum(values) / len(values)           # true average (not floor division)
    return average if math.isfinite(average) else None


def payable_bill(text):
    """Compute bill * 1.18 (GST) - discount from 'bill|discount'.

    Returns a float >= 0, or None if the input is invalid.
    """
    if not isinstance(text, str):
        return None
    parts = text.split('|')
    if len(parts) != 2:
        return None
    bill = _to_finite_float(parts[0])
    discount = _to_finite_float(parts[1])
    if bill is None or discount is None:
        return None
    total = bill * 1.18 - discount
    if not math.isfinite(total):
        return None
    return max(total, 0)


def _ask(prompt, func):
    """Run func on user input and print a friendly message if invalid."""
    result = func(input(prompt))
    return "Invalid input - please follow the format shown." if result is None else result


def main():
    print("==== Running parse_purchase ====")
    result = _ask("Enter grade:litres (e.g. diesel:25): ", parse_purchase)
    print("Grade and Litres:", result)

    print("\n==== Running volume_average ====")
    result = _ask("Enter pump volumes in litres as CSV (e.g. 10,25,40): ", volume_average)
    print("Average Volume:", result)

    print("\n==== Running payable_bill ====")
    result = _ask("Enter bill|discount (e.g. 2500|100): ", payable_bill)
    print("Payable Bill:", result)


if __name__ == "__main__":
    main()