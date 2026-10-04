import csv
import json
import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from part2_engine.growth_engine import (
    validate_feed,
    mom_growth,
    is_flagged,
)

from part3_narrative.template_fill import fill_prompt

MONTH_ORDER = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
]


def load_rows(csv_path):
    """Load a CSV file into a list of dictionaries."""
    with open(csv_path, "r", newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def get_previous_month(month):
    """Return the month immediately before the supplied month."""
    index = MONTH_ORDER.index(month)

    if index == 0:
        raise ValueError(
            "January does not have a previous month in this project."
        )

    return MONTH_ORDER[index - 1]


def get_month_rows(rows, month):
    """Get rows for one month from a CSV feed."""
    return [
        row
        for row in rows
        if row.get("month", "").strip() == month
    ]





def run(month, previous_month_csv, current_month_csv):
    """
    Run the complete Part 4 mock agent workflow.

    Returns the required structured JSON-compatible dictionary.
    """

    # ---------------------------------------------------------
    # 1. Load current feed
    # ---------------------------------------------------------
    current_rows = load_rows(current_month_csv)

    # ---------------------------------------------------------
    # 2. Validate before doing any calculations
    # ---------------------------------------------------------
    is_valid, validation_errors = validate_feed(current_month_csv)

    if not is_valid:
        return {
            "run_month": month,
            "validation_status": "invalid",
            "validation_errors": validation_errors,
            "flagged_categories": [],
            "suppressed_categories": [],
            "escalated_categories": [],
            "action_taken": "hard_stop",
        }

    # ---------------------------------------------------------
    # 3. Determine previous month
    # ---------------------------------------------------------
    previous_month = get_previous_month(month)

    previous_rows = load_rows(previous_month_csv)

    # ---------------------------------------------------------
    # 4. Select requested months
    # ---------------------------------------------------------
    current_month_rows = get_month_rows(
        current_rows,
        month,
    )

    previous_month_rows = get_month_rows(
        previous_rows,
        previous_month,
    )

    # ---------------------------------------------------------
    # 5. Create category lookup tables
    # ---------------------------------------------------------
    current_by_category = {
        row["category"]: float(row["revenue"])
        for row in current_month_rows
        if row.get("category")
    }

    previous_by_category = {
        row["category"]: float(row["revenue"])
        for row in previous_month_rows
        if row.get("category")
    }

    # ---------------------------------------------------------
    # 6. Calculate MoM and classify every category
    # ---------------------------------------------------------
    flagged = []
    escalated = []

    for category in sorted(current_by_category):

        if category not in previous_by_category:
            continue

        previous_revenue = previous_by_category[category]
        current_revenue = current_by_category[category]

        mom_pct = mom_growth(
            previous_revenue,
            current_revenue,
        )

        status = is_flagged(mom_pct)

        if status == "flagged":
            flagged.append(
                {
                    "category": category,
                    "mom_pct": mom_pct,
                    "previous_revenue": previous_revenue,
                    "current_revenue": current_revenue,
                }
            )

        elif status == "escalate_exact_boundary":
            escalated.append(
                {
                    "category": category,
                    "mom_pct": mom_pct,
                    "previous_revenue": previous_revenue,
                    "current_revenue": current_revenue,
                }
            )

    # ---------------------------------------------------------
    # 7. Rank flagged categories by absolute MoM
    # ---------------------------------------------------------
    flagged.sort(
        key=lambda item: abs(item["mom_pct"]),
        reverse=True,
    )

    # ---------------------------------------------------------
    # 8. Draft only the top 3 flagged categories
    # ---------------------------------------------------------
    top_three = flagged[:3]
    suppressed = flagged[3:]

    drafted_categories = []

    for item in top_three:

        message = fill_prompt(
            category=item["category"],
            previous_revenue=item["previous_revenue"],
            current_revenue=item["current_revenue"],
            mom_pct=item["mom_pct"],
            month=month,
            prev_month=previous_month,
        )

        drafted_categories.append(
            {
                "category": item["category"],
                "mom_pct": item["mom_pct"],
                "previous_revenue": item["previous_revenue"],
                "current_revenue": item["current_revenue"],
                "drafted": True,
                "message": message,
            }
        )

    # Suppressed categories are returned as category-name strings.
    suppressed_categories = [
        item["category"]
        for item in suppressed
    ]

    # Escalated categories are also returned as category-name strings.
    escalated_categories = [
        item["category"]
        for item in escalated
    ]

    # ---------------------------------------------------------
    # 9. Build required structured output
    # ---------------------------------------------------------
    return {
        "run_month": month,
        "validation_status": "valid",
        "validation_errors": [],
        "flagged_categories": drafted_categories,
        "suppressed_categories": suppressed_categories,
        "escalated_categories": escalated_categories,
        "action_taken": "drafted_and_held_for_approval",
    }


def main():
    """Command-line entry point."""

    if len(sys.argv) != 4:
        print(
            "Usage: python part4_agent\\mock_agent_runner.py "
            "<month> <previous_month_csv> <current_month_csv>"
        )

        print("Example:")

        print(
            "python part4_agent\\mock_agent_runner.py "
            "May "
            "part1_sql\\output\\monthly_category_revenue.csv "
            "part1_sql\\output\\monthly_category_revenue.csv"
        )

        sys.exit(1)

    month = sys.argv[1]
    previous_month_csv = sys.argv[2]
    current_month_csv = sys.argv[3]

    result = run(
        month,
        previous_month_csv,
        current_month_csv,
    )

    print(
        json.dumps(
            result,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()