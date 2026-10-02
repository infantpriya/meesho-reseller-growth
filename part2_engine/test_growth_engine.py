from growth_engine import mom_growth, is_flagged, validate_feed


# Test 1:
# April → May Ethnic Wear
previous = 104520.77
current = 185107.61

growth = mom_growth(previous, current)

assert growth == 77.1
assert is_flagged(growth) == "flagged"


# Test 2:
# May → June Beauty & Personal Care
previous = 35542.11
current = 37559.07

growth = mom_growth(previous, current)

assert growth == 5.67
assert is_flagged(growth) == "not_flagged"


# Test 3:
# Exact 8% threshold boundary
growth = mom_growth(100000, 108000)

assert growth == 8.0
assert is_flagged(growth) == "escalate_exact_boundary"


# Test 4:
# Corrupted feed validation
is_valid, errors = validate_feed(
    "part2_engine/fixtures/corrupted_feed.csv"
)

assert is_valid is False

assert errors == [
    "line 3: negative revenue (-4200.0) for category=Western Wear",
    "line 4: missing category (month=July)",
    "line 6: missing revenue (category=Home & Kitchen)",
]