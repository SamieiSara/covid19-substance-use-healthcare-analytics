# DAX Notes

Technical notes on a measure built for the Power BI dashboard, included here for anyone who wants to see the reasoning behind it. The main [README](README.md) covers the project overview and findings — this file is a deeper look at one specific fix.

## Filter Context Bug in Hospitalization KPI Card

**Problem:** The hospitalization percentage-change KPI card was returning incorrect totals. The table (`Hosp-Total`) is in wide format, with rows split by year, but the visual's filter context — coming from slicers and other visuals on the same page — was silently narrowing the data before the year filter could even be applied. This meant the card wasn't summing the totals it appeared to be summing.

**Fix:** Added `ALL('Hosp-Total')` inside `CALCULATE()` to clear any conflicting filters from the table first, so that the explicit year filter is the only thing controlling the result.

```dax
Hosp Arrow + Pct = 
VAR Hosp2019 =
    CALCULATE(
        SUM('Hosp-Total'[Hospitalization]),
        ALL('Hosp-Total'),
        'Hosp-Total'[Year] = 2019
    )
VAR Hosp2020 =
    CALCULATE(
        SUM('Hosp-Total'[Hospitalization]),
        ALL('Hosp-Total'),
        'Hosp-Total'[Year] = 2020
    )
VAR PctChange = DIVIDE(Hosp2020 - Hosp2019, Hosp2019)
VAR Arrow = IF(PctChange > 0, "▲ ", "▼ ")
RETURN Arrow & FORMAT(ABS(PctChange), "0%")
```

**Why this matters:** `CALCULATE()` doesn't automatically ignore filters from the rest of the report — it layers new filters on top of whatever is already active. For a KPI card that always needs to compare two fixed years regardless of what else is selected on the page, `ALL()` is what guarantees that behaviour rather than relying on the report happening to have no conflicting filters at the time.
