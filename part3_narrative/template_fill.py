def fill_prompt(
    category,
    previous_revenue,
    current_revenue,
    mom_pct,
    month,
    prev_month,
):
    """
    Deterministically fill the Part 3 narrative template.

    Uses only verified supplied values.
    No API, network, or external service is used.
    """

    return (
        f"Context: This update monitors {category} revenue "
        f"for {month} versus {prev_month}.\n"
        f"Insight: Fact: {category} changed by {mom_pct}% "
        f"month-on-month.\n"
        f"Implication: Action: Review regional and reseller-level "
        f"performance for {category} before deciding on the next action. "
        f"Hypothesis: The category-level figures alone do not prove "
        f"the cause of the change."
    )