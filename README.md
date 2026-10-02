# Meesho Reseller Growth & Alert Intelligence Pipeline

An end-to-end offline pipeline for monitoring Meesho reseller category revenue, detecting significant month-on-month movements, validating corrupted feeds, generating deterministic stakeholder narratives, and producing a mock agent decision output.

## Project Goal

The pipeline connects four parts:

1. Part 1 — SQL analytics
2. Part 2 — Growth engine and guardrails
3. Part 3 — Deterministic narrative and masking
4. Part 4 — Agent specification and mock runner

The complete workflow is:

```text
CSV dataset
    ↓
SQLite
    ↓
SQL outputs
    ↓
Python validation
    ↓
MoM growth
    ↓
Threshold classification
    ↓
Narrative drafting
    ↓
Top-3 suppression
    ↓
Structured agent output
    ↓
Human approval
```

The project is completely offline and deterministic. No API keys or external AI services are required.

## Requirements

- Python 3.x
- SQLite
- Git
- VS Code or another code editor
- No API keys are required

## Project Structure

```text
meesho-reseller-growth/
│
├── README.md
│
├── data/
│   ├── generate_dataset.py
│   ├── resellers.csv
│   ├── orders.csv
│   └── meesho_reseller.db
│
├── part1_sql/
│   ├── queries.sql
│   ├── run_query.py
│   └── output/
│       ├── monthly_category_revenue.csv
│       ├── region_revenue.csv
│       ├── top_resellers.csv
│       ├── zero_order_resellers.csv
│       └── june_delivered_aov.csv
│
├── part2_engine/
│   ├── growth_engine.py
│   ├── test_growth_engine.py
│   └── fixtures/
│       ├── monthly_category_revenue.csv
│       └── corrupted_feed.csv
│
├── part3_narrative/
│   ├── prompt_pack.md
│   ├── narrative_report.md
│   └── masking.py
│
└── part4_agent/
    ├── agent_spec.md
    └── mock_agent_runner.py
```

## Dataset

The supplied dataset generator creates:

- 24 resellers
- 900 orders
- 300 orders per month
- April, May and June data
- 5 product categories
- Deterministic data using `random.Random(42)`
- A zero-order reseller: `RS024`

Regenerate the dataset:

```powershell
python data\generate_dataset.py
```

Expected output:

```text
Wrote 24 resellers and 900 orders. Zero-order reseller: RS024
```

## Part 1 — SQL Analytics

Part 1 loads the reseller and order data into SQLite and answers the required business questions using SQL.

### Run Part 1

```powershell
python part1_sql\run_query.py 1
python part1_sql\run_query.py 2
python part1_sql\run_query.py 3
python part1_sql\run_query.py 4
python part1_sql\run_query.py 5
```

Outputs are written to:

```text
part1_sql/output/
```

### Question 1 — Monthly Category Revenue

Output:

```text
part1_sql/output/monthly_category_revenue.csv
```

Contains monthly revenue by category.

Expected output size: 15 rows representing 3 months × 5 categories.

This file becomes the verified numeric input for Part 2.

### Question 2 — Region Revenue

Output:

```text
part1_sql/output/region_revenue.csv
```

Contains revenue and order counts by region.

### Question 3 — Top Resellers

Output:

```text
part1_sql/output/top_resellers.csv
```

Returns the top resellers according to the required SQL logic.

### Question 4 — Zero-Order Resellers

Output:

```text
part1_sql/output/zero_order_resellers.csv
```

Expected zero-order reseller:

```text
RS024
Ahmedabad Reseller 6
West
```

The query demonstrates the difference between:

```sql
COUNT(*)
```

and:

```sql
COUNT(order_id)
```

### Question 5 — June Delivered AOV

Output:

```text
part1_sql/output/june_delivered_aov.csv
```

Expected AOV:

```text
1267.69
```

Expected grand total revenue:

```text
1262066.92
```

## Part 2 — Growth Engine and Guardrails

Part 2 receives the verified monthly category revenue feed from Part 1.

The growth engine contains exactly three required functions:

```text
mom_growth()
is_flagged()
validate_feed()
```

### Month-on-Month Growth

The calculation is:

```text
(current - previous) / previous * 100
```

The result is rounded to two decimal places.

Example:

```text
April → May
Ethnic Wear
+77.10%
```

### Threshold Classification

The threshold is based on an absolute MoM change of 8%:

```text
abs(MoM) > 8
    → flagged

abs(MoM) < 8
    → not_flagged

abs(MoM) == 8
    → escalate_exact_boundary
```

### Feed Validation

`validate_feed()` checks for:

- Missing category
- Missing revenue
- Non-numeric revenue
- Negative revenue

Validation errors are reported in row order.

## Part 2 Tests

Run:

```powershell
python part2_engine\test_growth_engine.py
```

The tests cover:

- April → May Ethnic Wear: `77.10%` → `flagged`
- May → June Beauty & Personal Care: `5.67%` → `not_flagged`
- `100000 → 108000`: `8.00%` → `escalate_exact_boundary`

Corrupted feed expected errors:

```text
line 3: negative revenue (-4200.0) for category=Western Wear
line 4: missing category (month=July)
line 6: missing revenue (category=Home & Kitchen)
```

## Part 3 — Deterministic Narrative

Part 3 converts verified numeric results into a deterministic stakeholder-facing narrative.

Files:

```text
part3_narrative/prompt_pack.md
part3_narrative/narrative_report.md
part3_narrative/masking.py
```

The prompt pack contains four required sections:

1. Trigger
2. Input
3. Prompt
4. Checklist

The prompt uses these verified values:

```text
category
previous_revenue
current_revenue
mom_pct
month
prev_month
```

The narrative separates:

```text
FACT
```

from:

```text
HYPOTHESIS
```

The report includes:

- May Ethnic Wear: `+77.10%`
- June Ethnic Wear: `-58.74%`
- Real numeric values
- FACT/HYPOTHESIS labels
- Actionable implications
- A self-check
- Chart-choice guidance

## Part 3 — Masking

The masking requirement prevents reseller IDs from being exposed in stakeholder-facing narratives.

Examples:

```text
RS019 → ALIAS-19
RS006 → ALIAS-06
```

Run:

```powershell
python part3_narrative\masking.py
```

## Part 4 — Agent Specification and Mock Runner

Part 4 demonstrates an agent-style workflow that orchestrates the verified pipeline without external API calls.

Files:

```text
part4_agent/agent_spec.md
part4_agent/mock_agent_runner.py
```

The runner imports the Part 2 guardrail functions:

```text
validate_feed()
mom_growth()
is_flagged()
```

The mock runner produces deterministic structured JSON and holds the result for human approval.

## Part 4 Planner

The required ordered planner is:

```text
1. Load monthly revenue feed
2. Run validate_feed()
3. If INVALID → Hard Stop
4. If VALID → compute mom_growth() for every category versus the previous month
5. Run is_flagged() on every category
6. Sort flagged categories by abs(mom_pct) descending
6b. Draft via the Part 3 template for at most the top 3
7. Log remaining flagged categories as suppressed and review manually
7b. Separately log exact-boundary categories into escalated_categories
8. Emit one structured JSON object
```

No automatic external sending is performed. Human approval remains the final step.

## Part 4 Guardrails

### Input Guardrail

The monthly category revenue feed must pass:

```text
validate_feed()
```

before growth calculations or narrative drafting occur.

### Action Guardrail

If validation fails:

```text
Hard Stop
```

No narrative is drafted, no flagged categories are generated, and no external action is performed.

### Output Guardrail

The runner emits one structured JSON object containing the required fields.

## Part 4 Output Schema

The structured output contains:

```text
run_month
validation_status
validation_errors
flagged_categories
suppressed_categories
escalated_categories
action_taken
```

Each flagged category contains:

- category
- mom_pct
- previous_revenue
- current_revenue
- drafted
- message

`suppressed_categories` contains category names.

`escalated_categories` contains category names for exact-boundary cases.

## Part 4 — Running the Mock Agent

The current `mock_agent_runner.py` expects three positional arguments:

```text
<month> <previous_month_csv> <current_month_csv>
```

### May

```powershell
python part4_agent\mock_agent_runner.py May part1_sql\output\monthly_category_revenue.csv part1_sql\output\monthly_category_revenue.csv
```

Expected drafted categories:

```text
Ethnic Wear    +77.10%
Western Wear   -23.60%
Kids Wear      -23.48%
```

Suppressed:

```text
Beauty & Personal Care
Home & Kitchen
```

### June

```powershell
python part4_agent\mock_agent_runner.py June part1_sql\output\monthly_category_revenue.csv part1_sql\output\monthly_category_revenue.csv
```

Expected drafted categories:

```text
Ethnic Wear     -58.74%
Home & Kitchen  +42.59%
Kids Wear       +23.90%
```

Suppressed:

```text
Western Wear
```

Beauty & Personal Care is `+5.67%` and is not flagged.

### Corrupted Feed

```powershell
python part4_agent\mock_agent_runner.py July part1_sql\output\monthly_category_revenue.csv part2_engine\fixtures\corrupted_feed.csv
```

Expected:

```text
validation_status = invalid
action_taken = hard_stop
```

Expected validation errors:

```text
line 3: negative revenue (-4200.0) for category=Western Wear
line 4: missing category (month=July)
line 6: missing revenue (category=Home & Kitchen)
```

Expected lists on hard stop:

```text
flagged_categories = []
suppressed_categories = []
escalated_categories = []
```

## How the Parts Connect

The pipeline is intentionally integrated rather than being four independent scripts.

### Part 1 → Part 2

Part 1 calculates verified monthly category revenue.

```text
part1_sql/output/monthly_category_revenue.csv
        ↓
Part 2 validate_feed()
        ↓
Part 2 growth calculations
```

### Part 2 → Part 3

Part 2 validates and classifies the numeric data before Part 3 converts verified values into a stakeholder-facing narrative.

```text
Validated numbers
        ↓
MoM classification
        ↓
Narrative template
```

### Part 3 → Part 4

Part 4 uses the deterministic narrative approach when drafting the top three flagged categories.

```text
Part 2 verified movement
        ↓
Part 3 deterministic template
        ↓
Part 4 structured agent output
```

### Complete Integration

```text
Dataset
   ↓
SQLite
   ↓
Part 1 SQL
   ↓
monthly_category_revenue.csv
   ↓
Part 2 validate_feed()
   ↓
Part 2 mom_growth()
   ↓
Part 2 is_flagged()
   ↓
Part 3 deterministic narrative
   ↓
Part 4 top-3 drafting
   ↓
Suppression / escalation
   ↓
Structured JSON
   ↓
Human approval
```

## Workflow Pattern Mapping

### Part 1 → Part 2

**Compute-real-numbers-then-hand-off**

Part 1 computes verified SQL metrics and hands the monthly category revenue feed to the Python growth engine.

### Part 2 → Part 3

**Verified-numbers-to-stakeholder-draft**

Part 2 validates and classifies numeric data before Part 3 converts verified values into a stakeholder-facing narrative.

### Part 4

**Intake → Summary → Report Draft → Validate**

Part 4 receives the monthly feed, summarizes category movements, drafts only the top flagged items using the deterministic template, validates the input, and applies the required guardrails before producing structured output.

## Suppression and Escalation Logic

Only the top three flagged categories are drafted.

Remaining flagged categories are placed into:

```text
suppressed_categories
```

for manual review.

Exact-boundary cases where:

```text
abs(MoM) == 8.00%
```

are handled separately and placed into:

```text
escalated_categories
```

## Human Approval

The pipeline does not automatically send alerts, emails, or reports.

The final output is intended for human review and approval.

```text
Structured output
        ↓
Human approval
        ↓
Any external action
```

This is a mock/offline agent workflow rather than an autonomous sending system.

## API Keys and External Services

No API keys are required.

The project is designed to run offline.

There are:

- No OpenAI API calls
- No external LLM calls
- No external email sending
- No automatic notifications
- No external production integrations

The narrative and agent behavior are deterministic.

## Complete Run Order

### 1. Generate the dataset

```powershell
python data\generate_dataset.py
```

### 2. Run Part 1

```powershell
python part1_sql\run_query.py 1
python part1_sql\run_query.py 2
python part1_sql\run_query.py 3
python part1_sql\run_query.py 4
python part1_sql\run_query.py 5
```

### 3. Run Part 2 tests

```powershell
python part2_engine\test_growth_engine.py
```

### 4. Run Part 3 masking tests

```powershell
python part3_narrative\masking.py
```

### 5. Run Part 4 — May

```powershell
python part4_agent\mock_agent_runner.py May part1_sql\output\monthly_category_revenue.csv part1_sql\output\monthly_category_revenue.csv
```

### 6. Run Part 4 — June

```powershell
python part4_agent\mock_agent_runner.py June part1_sql\output\monthly_category_revenue.csv part1_sql\output\monthly_category_revenue.csv
```

### 7. Run Part 4 — Corrupted Feed

```powershell
python part4_agent\mock_agent_runner.py July part1_sql\output\monthly_category_revenue.csv part2_engine\fixtures\corrupted_feed.csv
```

## Reproducibility

The project is deterministic.

The dataset generator uses:

```text
random.Random(42)
```

Regenerating the dataset produces the same deterministic dataset and expected project outputs.

The generated dataset contains:

```text
24 resellers
900 orders
```

## Expected Part 1 Acceptance Values

```text
Monthly category revenue:
15 rows

Zero-order reseller:
RS024
Ahmedabad Reseller 6
West

June delivered AOV:
1267.69

Grand total revenue:
1262066.92
```

## Expected Part 2 Acceptance Values

```text
April → May Ethnic Wear:
77.10%
flagged

May → June Beauty & Personal Care:
5.67%
not_flagged

100000 → 108000:
8.00%
escalate_exact_boundary
```

Corrupted feed:

```text
3 validation errors
```

## Expected Part 4 Acceptance Values

### May

```text
Ethnic Wear:
+77.10%

Western Wear:
-23.60%

Kids Wear:
-23.48%
```

Suppressed:

```text
Beauty & Personal Care
Home & Kitchen
```

### June

```text
Ethnic Wear:
-58.74%

Home & Kitchen:
+42.59%

Kids Wear:
+23.90%
```

Suppressed:

```text
Western Wear
```

Beauty & Personal Care:

```text
+5.67%
not flagged
```

### Corrupted Feed

```text
validation_status:
invalid

action_taken:
hard_stop
```

## Final Acceptance Checklist

- [x] 24 resellers
- [x] 900 orders
- [x] Deterministic dataset generation
- [x] 15 monthly category revenue rows
- [x] Required Part 1 SQL outputs
- [x] Zero-order reseller detection
- [x] June delivered AOV
- [x] Three Part 2 growth-engine functions
- [x] Growth-engine tests
- [x] Exact 8% boundary handling
- [x] Three corrupted-feed validation errors in order
- [x] Four-section Part 3 prompt pack
- [x] May and June narrative examples
- [x] FACT/HYPOTHESIS distinction
- [x] Reseller ID masking
- [x] Part 4 ordered planner
- [x] Input/action/output guardrails
- [x] Top-3 drafting
- [x] Suppression
- [x] Exact-boundary escalation
- [x] Structured JSON output
- [x] Hard stop on invalid input
- [x] Zero API keys
- [x] Human approval
- [x] One public GitHub repository

## Repository

Public GitHub repository:

`https://github.com/infantpriya/meesho-reseller-growth`

This repository contains the offline capstone implementation.