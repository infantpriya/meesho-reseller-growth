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
