# Reusable Prompt Pack

## Trigger

Run this prompt when a category's `is_flagged` result is `"flagged"`.

## Input list

The prompt requires these verified values:

- `{category}` — the category name
- `{previous_revenue}` — revenue for the previous month
- `{current_revenue}` — revenue for the current month
- `{mom_pct}` — verified month-on-month growth percentage
- `{month}` — current month
- `{prev_month}` — previous month

## Prompt

Using only the supplied verified inputs, write a stakeholder update for a regional manager about `{category}` for `{month}` versus `{prev_month}`.

Structure the update as:

**Context:** State what is being measured and explicitly name the comparison period `{month}` versus `{prev_month}`.

**Insight:** State the verified month-on-month change as `{mom_pct}%` and identify the category as `{category}`. Use only the supplied values `{previous_revenue}`, `{current_revenue}`, and `{mom_pct}` when stating numbers.

**Implication:** Give one specific, actionable next step for the regional manager. If a possible cause is suggested, clearly label it as a hypothesis because the supplied data does not by itself prove causation.

Never invent, estimate, or calculate any number that is not one of the supplied placeholders. Do not introduce additional numerical facts. Keep the narrative concise and suitable for a regional manager.

## Checklist

Before using the drafted update, verify:

1. Every number in the draft matches a supplied placeholder value exactly.
2. The category name and both months are stated correctly.
3. The month-on-month percentage matches `{mom_pct}` exactly.
4. Facts are clearly distinguished from hypotheses about possible causes.
5. The implication contains a specific and actionable next step rather than a vague suggestion.
6. No reseller's raw name is included; any reseller reference must use its coded alias.