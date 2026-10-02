def alias_for(reseller_id: str) -> str:
    """Convert a reseller ID into an external-facing alias."""
    return f"ALIAS-{reseller_id[3:]}"


def assert_no_raw_names_leak(
    text: str,
    reseller_names: list[str],
) -> bool:
    """Return False if any raw reseller name appears in the text."""
    return not any(name in text for name in reseller_names)


# Required acceptance checks
assert alias_for("RS019") == "ALIAS-19"
assert alias_for("RS006") == "ALIAS-06"

top_reseller_names = [
    "Mumbai Reseller 1",
    "Mumbai Reseller 4",
    "Hyderabad Reseller 6",
    "Lucknow Reseller 6",
    "Jaipur Reseller 5",
]

safe_text = """
ALIAS-19 — Mumbai region
ALIAS-22 — Mumbai region
ALIAS-12 — Hyderabad region
ALIAS-06 — Lucknow region
ALIAS-05 — Jaipur region
"""

leaking_text = "Mumbai Reseller 1 had the highest total spend."

assert assert_no_raw_names_leak(
    safe_text,
    top_reseller_names,
) is True

assert assert_no_raw_names_leak(
    leaking_text,
    top_reseller_names,
) is False