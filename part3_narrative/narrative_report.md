# Reliable Narrative Report

## 1. Worked Narrative — May Ethnic Wear

### Context

This update measures Ethnic Wear revenue growth from April to May 2026. April revenue was INR 104520.77 and May revenue was INR 185107.61.

### Insight

**Fact:** Ethnic Wear revenue increased by **77.1% month-on-month** from April to May 2026. The 77.1% figure is the verified Part 2 MoM result.

### Implication

**Action:** The regional manager should review the May Ethnic Wear result alongside reseller and regional performance, then identify which regions or reseller groups contributed to the change before deciding whether the May pattern should be sustained or investigated further.

**Hypothesis:** The available category-level revenue data alone does not establish why the increase occurred, so any proposed cause should be treated as a hypothesis until reseller- or region-level evidence is checked.

---

## 2. Worked Narrative — June Ethnic Wear

### Context

This update measures Ethnic Wear revenue growth from May to June 2026. May revenue was INR 185107.61 and June revenue was INR 76371.53.

### Insight

**Fact:** Ethnic Wear revenue decreased by **58.74% month-on-month** from May to June 2026. The -58.74% figure is the verified Part 2 MoM result.

### Implication

**Action:** The regional manager should review June Ethnic Wear performance by region and reseller activity, then check whether the decline is concentrated in particular areas before deciding on a corrective action.

**Hypothesis:** The category-level figures alone do not prove the cause of the decline. Possible explanations should therefore be treated as hypotheses until the underlying regional and reseller-level data is reviewed.

---

## 3. Four-Criterion Refinement Self-Score

### Specificity

Pass — Both narratives identify the correct category, comparison months, revenue values, and verified MoM percentages.

### Audience Fit

Pass — The wording is directed to a regional manager and focuses on what should be reviewed or acted upon rather than on implementation details for a data engineer.

### Completeness

Pass — Each narrative contains all three required sections: Context, Insight, and Implication.

### Actionability

Pass — Each narrative gives a concrete next step: review the result by region and reseller activity before deciding on a corrective action.

---

## 4. Chart-Choice Justification

### 4.1 Which month had the highest total revenue?

**Recommended chart: Column chart.**

This is a univariate comparison of total revenue across three months, so a simple column chart makes the month-to-month comparison immediately visible. The y-axis should start at zero so that the differences in revenue are not visually exaggerated. The message should be understandable within about 10 seconds, and no legend is necessary because there is only one series.

The supplied totals are April = INR 419417.43, May = INR 444594.25, and June = INR 398055.24.

### 4.2 What percentage share does Ethnic Wear represent of April's total revenue?

**Recommended chart: Single-series pie chart.**

This question concerns the relationship between one category and the whole April total, so the underlying relationship is a part-to-whole comparison. A simple pie chart can communicate the 24.92% share quickly when only the relevant category share and remainder are being considered. The chart should remain simple and avoid unnecessary 3D effects.

The supplied figures are Ethnic Wear revenue = INR 104520.77, April total revenue = INR 419417.43, and the calculated share = 24.92%.

### 4.3 How do the four regions compare on total revenue?

**Recommended chart: Column chart.**

This is a univariate comparison of total revenue across four categorical regions. A column chart with a zero-based y-axis makes the differences between North, South, East, and West easy to compare within 10 seconds. Because there is only one measure, a legend is unnecessary and 3D should be avoided.

The Part 1 regional totals are North = INR 337125.46, West = INR 333106.33, South = INR 316736.68, and East = INR 275098.45.

---

## 5. Masked Top-Reseller Narrative

For any external-facing narrative, reseller names must not be exposed. The five resellers identified by the Part 1 top-reseller query are therefore referenced only by coded aliases and region.

- ALIAS-19 — Mumbai region
- ALIAS-22 — Mumbai region
- ALIAS-12 — Hyderabad region
- ALIAS-06 — Lucknow region
- ALIAS-05 — Jaipur region

**Action:** A regional manager reviewing an external-facing summary should use these aliases when discussing the top-reseller results and should investigate regional performance using the aliases rather than raw reseller names.

No raw reseller name is included in this narrative.