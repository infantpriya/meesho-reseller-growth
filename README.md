# Meesho Reseller Growth & Alert Intelligence Pipeline

An end-to-end offline pipeline for monitoring Meesho reseller category revenue, detecting significant month-on-month movements, validating corrupted feeds, generating deterministic stakeholder narratives, and producing a mock agent decision output.

## Project Goal

The pipeline connects four parts:

1. Part 1 — SQL analytics
2. Part 2 — Growth engine and guardrails
3. Part 3 — Deterministic narrative and masking
4. Part 4 — Agent specification and mock runner

The complete workflow is:

CSV dataset → SQLite → SQL outputs → validation → MoM growth → threshold classification → narrative drafting → top-3 suppression → structured agent output

No paid API, network service, or API key is required.

---

## Project Structure

```text
meesho-reseller-growth/
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
│       └── corrupted_feed.csv
│
├── part3_narrative/
│   ├── prompt_pack.md
│   ├── narrative_report.md
│   └── masking.py
│
├── part4_agent/
│   ├── agent_spec.md
│   └── mock_agent_runner.py
│
└── README.md