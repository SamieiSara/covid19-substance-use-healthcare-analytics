# ============================================================
# EXPLORATORY DATA ANALYSIS (EDA) & TREND EXPLORATION
# COVID-19 Substance Use & Healthcare Harm Analytics Project
#
# This script explores CIHI's healthcare data on substance-related
# harm during the COVID-19 pandemic: ED visits, hospitalizations,
# monthly trends, provincial patterns, and age-group patterns.
#
# Python is used for data exploration, validation, and charting.
# The Power BI dashboard reads the same Excel workbook directly
# and is built independently using Power Query and DAX.
#
# Dataset Source:
# Canadian Institute for Health Information (CIHI)
# Impact on Harms Caused by Substance Use
# ============================================================

import pandas as pd
import matplotlib.pyplot as plt

FILE_PATH = "cihi-substance-use-data-restructured.xlsx"
CHART_DIR = "charts"


# ================================
# HELPER FUNCTIONS
# ================================

def check_data_quality(df, sheet_name):
    """
    Print a quick data quality summary for a loaded sheet:
    missing values per column and number of duplicate rows.
    Run automatically every time a sheet is loaded.
    """
    print(f"\n--- Data quality check: {sheet_name} ---")

    missing = df.isnull().sum()
    missing = missing[missing > 0]
    if missing.empty:
        print("No missing values.")
    else:
        print("Missing values found:")
        print(missing)

    duplicate_count = df.duplicated().sum()
    print(f"Duplicate rows: {duplicate_count}")


def load_cihi_sheet(file_path, sheet_name):
    """
    Load a CIHI sheet, automatically skipping the leftover
    'Screen reader users...' description row if one is present,
    dropping any fully blank trailing rows, trimming stray
    line breaks/extra spaces from the header row, and running
    a data quality check before returning the data.
    """
    preview = pd.read_excel(file_path, sheet_name=sheet_name, header=None, nrows=1)
    first_cell = preview.iloc[0, 0]
    skip = 1 if isinstance(first_cell, str) and first_cell.startswith("Screen reader") else 0

    df = pd.read_excel(file_path, sheet_name=sheet_name, header=skip)
    df = df.dropna(how="all")
    df.columns = [" ".join(str(col).replace("\n", " ").split()) for col in df.columns]

    check_data_quality(df, sheet_name)

    return df


def save_chart(filename):
    """Save the current chart to the charts folder instead of popping up a window."""
    plt.tight_layout()
    plt.savefig(f"{CHART_DIR}/{filename}", dpi=150)
    plt.close()
    print(f"Saved: {CHART_DIR}/{filename}")


# ================================
# SECTION 1: ED VISITS BY SUBSTANCE
# ================================

def chart_ed_by_substance():
    df = load_cihi_sheet(FILE_PATH, "1 ED type substances")
    df["Percentage change"] = df["Percentage change"] * 100

    ranked = df.sort_values("Percentage change", ascending=False)

    plt.figure(figsize=(10, 6))
    plt.bar(ranked["Type of substance"], ranked["Percentage change"])
    plt.title("Percentage Change in ED Visits by Substance")
    plt.xlabel("Type of Substance")
    plt.ylabel("Percentage Change (%)")
    plt.xticks(rotation=45, ha="right")
    plt.axhline(0, linestyle="--")
    save_chart("ed_visits_by_substance.png")


# ================================
# SECTION 2: MONTHLY ED TRENDS
# ================================

def chart_monthly_trends():
    df = load_cihi_sheet(FILE_PATH, "2 ED volume by month ")
    df = df[df["Month"] != "Total"]  # exclude the period-total row, not a real month

    monthly_trends = pd.DataFrame({
        "Month": df["Month"],
        "All Substances": df["All -% change"] * 100,
        "Alcohol": df["Alcohol - % Change"] * 100,
        "Opioids": df["Opioids - % change"] * 100,
        "Cannabis": df["Cannabis - % change"] * 100,
    })

    plt.figure(figsize=(10, 6))
    for col in ["All Substances", "Alcohol", "Opioids", "Cannabis"]:
        plt.plot(monthly_trends["Month"], monthly_trends[col], marker="o", label=col)

    plt.title("Monthly Percentage Change in ED Visits During COVID-19")
    plt.xlabel("Month")
    plt.ylabel("Percentage Change (%)")
    plt.axhline(0, linestyle="--")
    plt.legend()
    save_chart("monthly_ed_trends.png")


# ================================
# SECTION 3: PROVINCIAL ED VISIT ANALYSIS
# ================================

def chart_province_trends():
    df = load_cihi_sheet(FILE_PATH, "3 ED volume by province")
    df = df[df["Province/territory"] != "Canada"]  # national total, not a province

    province_trends = pd.DataFrame({
        "Province": df["Province/territory"],
        "Percentage Change": df["All -% change"] * 100,
    }).sort_values("Percentage Change")

    plt.figure(figsize=(10, 6))
    plt.barh(province_trends["Province"], province_trends["Percentage Change"])
    plt.title("Percentage Change in Substance-Related ED Visits by Province")
    plt.xlabel("Percentage Change (%)")
    plt.ylabel("Province")
    plt.axvline(0, linestyle="--")
    save_chart("ed_visits_by_province.png")


# ================================
# SECTION 4: PATIENT AGE ANALYSIS
# ================================

def chart_age_trends():
    df = load_cihi_sheet(FILE_PATH, "ED-Age")

    age_trends = pd.DataFrame({
        "Age Group": df["Patient age"],
        "Percentage Change": df["All -% change"] * 100,
    })

    age_order = ["10–19", "20–29", "30–39", "40–49", "50–59", "60–69", "70–79", "80+"]
    age_trends["Age Group"] = pd.Categorical(age_trends["Age Group"], categories=age_order, ordered=True)
    age_trends = age_trends.sort_values("Age Group")

    colors = ["red" if x < 0 else "green" for x in age_trends["Percentage Change"]]

    plt.figure(figsize=(10, 6))
    plt.barh(age_trends["Age Group"], age_trends["Percentage Change"], color=colors)
    plt.title("Percentage Change in Substance-Related ED Visits by Age Group")
    plt.xlabel("Percentage Change (%)")
    plt.ylabel("Age Group")
    plt.axvline(0, linestyle="--")
    save_chart("ed_visits_by_age.png")


# ================================
# SECTION 5: HOSPITALIZATION ANALYSIS
# ================================

def chart_hospitalizations_by_substance():
    df = load_cihi_sheet(FILE_PATH, "8 Hosp type substances")
    df["Percentage change"] = df["Percentage change"] * 100

    ranked = df.sort_values("Percentage change")

    plt.figure(figsize=(10, 6))
    plt.barh(ranked["Type of substance"], ranked["Percentage change"])
    plt.title("Percentage Change in Substance-Related Hospitalizations")
    plt.xlabel("Percentage Change (%)")
    plt.ylabel("Substance")
    plt.axvline(0, linestyle="--")
    save_chart("hospitalizations_by_substance.png")


# ================================
# MAIN
# ================================

def main():
    import os
    os.makedirs(CHART_DIR, exist_ok=True)

    chart_ed_by_substance()
    chart_monthly_trends()
    chart_province_trends()
    chart_age_trends()
    chart_hospitalizations_by_substance()


if __name__ == "__main__":
    main()
