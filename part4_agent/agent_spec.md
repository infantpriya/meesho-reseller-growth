# Meesho Reseller Growth Monitoring Agent Specification

## 1. Goal

Keep Meesho category managers informed of category month-on-month revenue movements beyond the 8% threshold, while requiring human approval before any drafted message is considered sent.

## 2. Tools

The agent uses the following project functions:

- `validate_feed()` from `part2_engine/growth_engine.py`
- `mom_growth()` from `part2_engine/growth_engine.py`
- `is_flagged()` from `part2_engine/growth_engine.py`
- The reusable narrative template defined in `part3_narrative/prompt_pack.md`

The agent does not re-implement the Part 2 growth functions.

## 3. Memory / State

Between runs, the agent must retain or receive the previous month's verified revenue per category.

The previous month's category revenue is required to calculate the next month's month-on-month growth:

`mom_growth(previous_revenue, current_revenue)`

The current run's validation result, calculated MoM values, flagged categories, suppressed categories, and escalated categories form the state of that run.

## 4. Planner

The agent executes these subtasks in the following exact order:

1. Load the monthly revenue feed.
2. Run `validate_feed()`.
3. If INVALID → Hard Stop.
4. If VALID → compute `mom_growth()` for every category versus the previous month.
5. Run `is_flagged()` on every category.
6. Sort flagged categories by `abs(mom_pct)` descending.
6b. Draft via the Part 3 template for at most the top 3.
7. Log remaining flagged categories as suppressed and review manually.
7b. Separately log exact-boundary categories into `escalated_categories`.
9. Emit one structured JSON object.

## 5. Feedback Loop

Every drafted message is held for human approval.

The mock runner does not send email, call an external service, or automatically publish a message. Its output records:

`action_taken = "drafted_and_held_for_approval"`

Human approval is therefore the checkpoint between drafting and any hypothetical future sending step.

---

# Guardrails

## Input Guardrail

`validate_feed()` must pass before any MoM calculation, flagging, suppression, escalation, or drafting occurs.

If validation returns `False`, the agent performs a Hard Stop.

## Action Guardrail

No message is ever automatically sent.

The runner only creates drafts and holds them for human approval.

## Output Guardrail

Every number in a drafted message must trace back to a verified Part 1 or Part 2 value.

The agent must not invent figures, estimates, or unsupported numerical claims.

---

# Success and Error Stopping Conditions

## Success

A successful run produces drafts for the permitted flagged categories, or correctly produces zero drafts when no category crosses the threshold.

Every number in every drafted message must be traceable to a verified Part 1 or Part 2 value.

Flagged categories beyond the top-3 drafting cap are recorded as suppressed for manual review.

Exact-boundary categories are recorded separately in `escalated_categories`.

## Error

If `validate_feed()` returns `False`, the run is a Hard Stop.

The validation errors must be surfaced in the structured output.

No MoM computation or message drafting is attempted after an input validation failure.

---

# Agent-Level Given–When–Then Specifications

## Specification 1 — April to May Ethnic Wear

**Given:** April → May Ethnic Wear revenue moves from `104520.77` to `185107.61`.

**When:** The agent runs `mom_growth` and then `is_flagged`.

**Then:** `mom_growth` returns `77.1` and `is_flagged` returns `"flagged"`.

## Specification 2 — May to June Beauty & Personal Care

**Given:** May → June Beauty & Personal Care revenue moves from `35542.11` to `37559.07`.

**When:** The agent evaluates the category.

**Then:** `mom_growth` returns `5.67` and `is_flagged` returns `"not_flagged"`.

## Specification 3 — Exact 8% Boundary

**Given:** Previous revenue is `100000` and current revenue is `108000`.

**When:** The agent evaluates the change.

**Then:** `mom_growth` returns exactly `8.0` and `is_flagged` returns `"escalate_exact_boundary"`.

## Specification 4 — Corrupted Feed

**Given:** The corrupted feed fixture contains the negative-revenue, missing-category, and missing-revenue errors defined in Part 2.

**When:** The agent validates the feed.

**Then:** validation fails with exactly the three required errors, and the agent performs a Hard Stop without attempting MoM computation or drafting.

---

# Structured Run Output

Every run must emit one JSON object containing exactly these top-level keys:

- `run_month`
- `validation_status`
- `validation_errors`
- `flagged_categories`
- `suppressed_categories`
- `escalated_categories`
- `action_taken`

Each object in `flagged_categories` contains:

- `category`
- `mom_pct`
- `previous_revenue`
- `current_revenue`
- `drafted`
- `message` when drafted

`validation_status` is either:

- `"valid"`
- `"invalid"`

`action_taken` is either:

- `"drafted_and_held_for_approval"`
- `"hard_stop"`
