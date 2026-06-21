# Healthcare Substance Use & Opioid Harm Analytics During COVID-19

## Overview
This project analyzes the impact of COVID-19 on substance-related harms across Canada, using public healthcare data from the Canadian Institute for Health Information (CIHI). It compares emergency department (ED) visits and hospitalizations for substance-related harm between March–September 2020 and the same period in 2019.

The project combines Python (data cleaning and exploratory analysis) with Power BI (interactive dashboard) to turn a static CIHI report into an explorable analytics tool.

**Source report:** [Unintended Consequences of COVID-19: Impact on Harms Caused by Substance Use (CIHI, 2021)](https://www.cihi.ca/)

---

## Business Problem
During COVID-19, healthcare access patterns shifted dramatically — but substance-related harm did not decline at the same rate as overall ED visits, and in some categories increased sharply. Public health agencies need to identify:
- Which substances drove the largest increases in ED visits and hospitalizations
- Which months saw the sharpest spikes (to understand pandemic-phase effects)
- Which populations (by age, sex, income, province) were most affected

This dashboard turns CIHI's static report tables into an interactive tool for exploring those questions by substance, time period, and demographic group.

---

## Key Findings
- **Overall ED visits for substance-related harm fell 5%** (186,529 → 176,902), while **hospitalizations rose 5%** (76,948 → 80,954) — the opposite of trends for "any reason" visits, which dropped much more sharply.
- **Opioid-related ED visits rose 8% overall**, but spiked to **+55% in September 2020** vs. September 2019 — opioid poisonings alone rose 16%, peaking at +88% in September.
- **Alcohol ED visits fell 11%**, but **alcohol-related hospitalizations rose 5%**, suggesting patients presented later and with more severe conditions.
- **Stimulant-related ED visits peaked early** (+29% in May 2020) while opioid visits surged later in the year — a possible substitution effect as drug supply was disrupted.
- **Lowest-income neighbourhoods saw the steepest increases** in alcohol (+14%) and opioid (+11%) hospitalizations, while the highest-income group saw almost no change.
- **Men accounted for 64% of substance-related hospitalizations** and saw an 8% increase overall, vs. 1% for women — opioid hospitalizations rose 17% for men and fell 5% for women.
- **Substance-related deaths rose in both care settings** — 12% in EDs and 13% in inpatient care — with opioid poisoning responsible for over two-thirds of these deaths.

 **What this means:** 
****opioid harm-reduction resources should scale seasonally rather than stay static, with capacity peaking around September to match the observed surge. Outreach and hospitalization support should also be prioritized in lower-income neighbourhoods, where increases in alcohol and opioid harm consistently outpaced the national average.
****
---

## Dashboard

The dashboard is organized around three questions:
1. **What changed overall?** — ED visits vs. hospitalizations, all substances, monthly trend
2. **Which substances drove the change?** — opioids, alcohol, cannabis, stimulants
3. **Who was most affected?** — age group, sex, income quintile, province

---

## Tools & Methods
- **Python (pandas, matplotlib):** loading CIHI's Excel tables, data quality checks (missing values, duplicates, invalid negatives), reshaping wide tables into analysis-ready long format
- **Power BI / DAX:** interactive KPI cards, filters by substance/year/province, drill-through by demographic

---

## How to Run
1. Download the CIHI data table: `unintended-consequences-covid-19-substance-use-data-table-en.xlsx`
2. Run `eda_review.py` to generate cleaned tables and exploratory charts
3. Open `dashboard.pbix` in Power BI Desktop to explore the interactive report

---

## Data Limitations
- Data is **provisional** (CIHI estimates ~90% complete) and may change in future updates
- **Quebec is excluded from hospitalization data**; ED data covers ~80% of the Canadian population
- ED visit counts likely underestimate true substance-related harm — many cases (especially fatal ones) never reach a hospital

---

## Key Business Questions Answered
- Which substance-related harms increased most during COVID-19?
- How did ED visits and hospitalizations diverge during the pandemic?
- Which demographic groups bore the greatest increase in harm?
