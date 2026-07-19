# Healthcare Substance Use & Opioid Harm Analytics During COVID-19

## Overview
This project analyzes the impact of COVID-19 on substance-related harms across Canada, using public healthcare data from the Canadian Institute for Health Information (CIHI). It compares emergency department (ED) visits and hospitalizations for substance-related harm between March–September 2020 and the same period in 2019.

The project combines Python (data cleaning and exploratory analysis) with Power BI (interactive dashboard) to turn a static CIHI report into an explorable analytics tool.

**Source data:** [CIHI data table](data/cihi-substance-use-data-restructured.xlsx) — from CIHI's *Unintended Consequences of COVID-19: Impact on Harms Caused by Substance Use* (2021)

**Note:** 
CIHI's original file was a single print-ready report layout. I restructured it into separate sheets by table for easier programmatic access. No data values were changed.

---

## Business Problem
During COVID-19, healthcare access patterns shifted dramatically — but substance-related harm did not decline at the same rate as overall ED visits, and in some categories increased sharply. Public health agencies need to identify:
- Which substances drove the largest increases in ED visits and hospitalizations
- Which months saw the sharpest spikes (to understand pandemic-phase effects)
- Which populations (by age, sex, income, province) were most affected

This dashboard turns CIHI's static report tables into an interactive tool for exploring those questions by substance, time period, and demographic group.

---

## Key Findings
- **Overall ED visits for substance-related harm fell 5%** (186,529 → 176,902), while **hospitalizations rose 5%** (76,948 → 80,954). This is the opposite of trends for "any reason" visits, which dropped much more sharply.
- **Opioid-related ED visits rose 8% overall** but spiked to **+55% in September 2020** vs. September 2019. Opioid poisonings alone rose 16%, peaking at +88% in September.
- **Alcohol ED visits fell 11%**, but **alcohol-related hospitalizations rose 5%**, suggesting patients presented later and with more severe conditions.
- **Stimulant-related ED visits peaked early** (+29% in May 2020) while opioid visits surged later in the year, a possible substitution effect as drug supply was disrupted.
- **Lowest-income neighbourhoods saw the steepest increases** in alcohol (+14%) and opioid (+11%) hospitalizations, while the highest-income group saw almost no change.
- **Men accounted for 64% of substance-related hospitalizations** and saw an 8% increase overall, vs. 1% for women. Opioid hospitalizations rose 17% for men and fell 5% for women.
- **Substance-related deaths rose in both care settings**: 12% in EDs and 13% in inpatient care. Opioid deaths alone rose 23% in EDs and 18% in inpatient settings, and over two-thirds of these opioid deaths were attributed to poisoning.

 **What this means:** 
Opioid harm-reduction resources should scale seasonally rather than stay static, with capacity peaking around September to match the observed surge. Outreach and hospitalization support should also be prioritized in lower-income neighbourhoods, where increases in alcohol and opioid harm consistently outpaced the national average.

---

## Dashboard

The dashboard is organized around three questions:
1. **What changed overall?** ED visits vs. hospitalizations, all substances, monthly trend
   
   <img width="855" height="513" alt="Screenshot 2026-06-29 at 3 08 35 PM" src="https://github.com/user-attachments/assets/232ddb75-223e-4a25-b082-2e15a813c45f" />

2. **Which substances drove the change?**  opioids, alcohol, cannabis, stimulants
   
<img width="866" height="545" alt="Screenshot 2026-06-29 at 3 08 45 PM" src="https://github.com/user-attachments/assets/6ff1ab8e-d817-4587-a7a9-014c5a3d1c78" />

3. **Who was most affected?**  age group, sex, income quintile, province

<img width="775" height="541" alt="Screenshot 2026-06-29 at 3 08 54 PM" src="https://github.com/user-attachments/assets/8e6e03e9-6568-4b96-8d6d-185944f26d88" />

---

## Tools & Methods
- **Python (pandas, matplotlib):** used for exploratory analysis on the CIHI data, data quality checks (missing values, duplicates, invalid negatives) and exploratory charts to understand trends before dashboard design
- **Power BI / DAX:** primary analysis tool — imports the edited CIHI Excel workbook directly, builds KPI cards, trend visuals, and demographic drill-throughs
  
---

## Sample EDA Output

Python was used to validate the data and explore trends before the dashboard was built. A few highlights:

**Monthly % change in ED visits by substance** — opioid-related visits spiked sharply in September 2020, while other substances stayed closer to baseline.
<img width="1500" height="900" alt="monthly_ed_trends" src="https://github.com/user-attachments/assets/01d6d347-7aa9-485e-912f-9da3d39eac81" />

**% change in ED visits by age group** — decreases were most pronounced among younger age groups, likely reflecting reduced social activity during pandemic closures.
[drag ed_visits_by_age.png here]

Full data quality checks (missing values, duplicate rows) are included in `EDA_trend_analysis.py` and confirmed no data quality issues across the analyzed tables.

---

## How to Run
Dashboard screenshots are shown above — no software needed to view the results.

To explore the project yourself:
1. `EDA_trend_analysis.py` — exploratory analysis script (data quality checks + charts) run against the CIHI data table
2. `Substance_Use_Dashboard.pbix` — open in Power BI Desktop (free download) to explore the interactive dashboard

---

## Data Limitations
- Data is **provisional** (CIHI estimates ~90% complete) and may change in future updates
- **Quebec is excluded from hospitalization data**; ED data covers ~80% of the Canadian population
- ED visit counts likely underestimate true substance-related harm — many cases (especially fatal ones) never reach a hospital
- 
