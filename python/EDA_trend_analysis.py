# ============================================================
# EXPLORATORY DATA ANALYSIS (EDA) & TREND EXPLORATION
# COVID-19 Substance Use & Healthcare Harm Analytics Project
#
# Description:
# This script explores CIHI's public healthcare reporting data
# related to substance-related harms during the COVID-19 pandemic.
#
# The goal is to analyze ED visits, hospitalizations, monthly
# trends, opioid harms, patient characteristics, and regional
# patterns before building the final interactive Power BI dashboard.
#
# Python is used for data exploration, validation, and charting.
# The Power BI dashboard imports directly from the CIHI Excel
# workbook and is built independently using Power Query and DAX.
#
# Dataset Source:
# Canadian Institute for Health Information (CIHI)
# Report: Unintended Consequences of COVID-19:
# Impact on Harms Caused by Substance Use
# ============================================================


# ================================
# SECTION 1: IMPORT LIBRARIES
# ================================

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def clean_percentage_column(df, col_index):
    # grab column by position (CIHI sheets have no clean headers)
    raw_column = df.iloc[:, col_index]

    # convert to numbers, turn junk/blank rows into NaN instead of crashing
    numeric_column = pd.to_numeric(raw_column, errors="coerce")

    # CIHI stores % as decimal (0.08) → convert to whole percent (8)
    return numeric_column * 100


# ================================
# SECTION 2: LOAD AND REVIEW DATA
# ================================

# File path for the CIHI Excel data table
file_path = "edited-unintended-consequences-covid-19-substance-use-data-table-en.xlsx"

# Open the Excel workbook
excel_file = pd.ExcelFile(file_path)

# Review all available sheets in the workbook
print("Available Sheets:")
for sheet in excel_file.sheet_names:
    print(sheet)

# ================================
# SECTION 3: DATA QUALITY REVIEW
# ================================

# Load Table 1
ed_substances = pd.read_excel(
    file_path,
    sheet_name="1 ED type substances",
    header=None,
    skiprows=4,
    names=[
        "Substance",
        "ED_2019",
        "ED_2020",
        "Percentage_Change"
    ]
)

# Keep only actual substance rows
ed_substances = ed_substances.iloc[:8]


# Review data structure
print("\nDataset Information:")
print(ed_substances.info())


# Summary statistics for numeric columns
print("\nSummary Statistics:")
print(
    ed_substances[
        ["ED_2019", "ED_2020", "Percentage_Change"]
    ].describe()
)


# Check for missing values
print("\nMissing Values:")
print(ed_substances.isnull().sum())
print("-> No missing values found; table is complete as extracted.")


# Check for duplicate rows
print("\nDuplicate Rows:")
print(ed_substances.duplicated().sum())
print("-> 0 duplicates, as expected for 8 distinct substance categories.")


# Check for negative ED visit values
negative_values = (
    (ed_substances["ED_2019"] < 0)
    | (ed_substances["ED_2020"] < 0)
)

print("\nRows with Invalid Negative Values:")
print(ed_substances[negative_values])


# ================================
# SECTION 4: ED VISITS BY SUBSTANCE
# ================================

# Sort by percentage change
change_rank = ed_substances.sort_values(
    by="Percentage_Change",
    ascending=False
)

plt.figure(figsize=(10,6))

plt.bar(
    change_rank["Substance"],
    change_rank["Percentage_Change"]
)

plt.title("Percentage Change in ED Visits by Substance")
plt.xlabel("Type of Substance")
plt.ylabel("Percentage Change (%)")

plt.xticks(rotation=45, ha="right")

# Add zero reference line
plt.axhline(0, linestyle="--")

plt.tight_layout()
plt.show()

# ================================
# SECTION 5: MONTHLY ED TRENDS
# ================================

# load the data first
monthly_ed = pd.read_excel(
    file_path,
    sheet_name="2 ED volume by month ",
    header=None,
    skiprows=5
)

monthly_ed = monthly_ed.iloc[:7]

# column positions verified against raw sheet: 0=Month, 3=All, 6=Alcohol, 9=Opioids, 12=Cannabis
monthly_trends = pd.DataFrame({
    "Month": monthly_ed.iloc[:, 0].astype(str),
    "All_Substances_Change": clean_percentage_column(monthly_ed, 3),
    "Alcohol_Change": clean_percentage_column(monthly_ed, 6),
    "Opioids_Change": clean_percentage_column(monthly_ed, 9),
    "Cannabis_Change": clean_percentage_column(monthly_ed, 12)
})

monthly_trends = monthly_trends.dropna()

plt.figure(figsize=(10, 6))

plt.plot(monthly_trends["Month"], monthly_trends["All_Substances_Change"], marker="o", label="All Substances")
plt.plot(monthly_trends["Month"], monthly_trends["Alcohol_Change"], marker="o", label="Alcohol")
plt.plot(monthly_trends["Month"], monthly_trends["Opioids_Change"], marker="o", label="Opioids")
plt.plot(monthly_trends["Month"], monthly_trends["Cannabis_Change"], marker="o", label="Cannabis")

plt.title("Monthly Percentage Change in ED Visits During COVID-19")
plt.xlabel("Month")
plt.ylabel("Percentage Change (%)")
plt.axhline(0, linestyle="--")
plt.legend()
plt.tight_layout()
plt.show()

# ================================
# SECTION 6: PROVINCIAL ED VISIT ANALYSIS
# ================================

# Load Table 3
ed_province = pd.read_excel(
    file_path,
    sheet_name="3 ED volume by province",
    header=None,
    skiprows=5
)

# Keep province rows only
ed_province = ed_province.iloc[:8]

# column positions: 0=Province, 3=% change
province_trends = pd.DataFrame({
    "Province": ed_province.iloc[:,0].astype(str),
    "Percentage_Change": clean_percentage_column(ed_province, 3)
})

# Remove invalid rows
province_trends = province_trends.dropna()

# Sort provinces by percentage change
province_trends = province_trends.sort_values(
    by="Percentage_Change",
    ascending=True
)

# Plot provincial comparison
plt.figure(figsize=(10,6))

plt.barh(
    province_trends["Province"],
    province_trends["Percentage_Change"]
)

plt.title("Percentage Change in Substance-Related ED Visits by Province")
plt.xlabel("Percentage Change (%)")
plt.ylabel("Province")

# Add reference line
plt.axvline(0, linestyle="--")

plt.tight_layout()
plt.show()

# ================================
# SECTION 7: PATIENT AGE ANALYSIS
# ================================

# Load Table 4
ed_characteristics = pd.read_excel(
    file_path,
    sheet_name="4 ED characteristics",
    header=None,
    skiprows=7
)

# Keep age-group rows only
age_analysis = ed_characteristics.iloc[:8]

# column positions: 0=Age Group, 3=% change
age_trends = pd.DataFrame({
    "Age_Group": age_analysis.iloc[:,0].astype(str),
    "Percentage_Change": clean_percentage_column(age_analysis, 3)
})

# Remove invalid rows
age_trends = age_trends.dropna()

# sort chronologically by age (not by value) — fixes age-axis ordering
age_order = ["10–19", "20–29", "30–39", "40–49", "50–59", "60–69", "70–79", "80+"]
age_trends["Age_Group"] = pd.Categorical(age_trends["Age_Group"], categories=age_order, ordered=True)
age_trends = age_trends.sort_values(by="Age_Group")

# Create conditional colors
colors = [
    "red" if x < 0 else "green"
    for x in age_trends["Percentage_Change"]
]

# Plot age-group comparison
plt.figure(figsize=(10,6))

plt.barh(
    age_trends["Age_Group"],
    age_trends["Percentage_Change"],
    color=colors
)

plt.title("Percentage Change in Substance-Related ED Visits by Age Group")
plt.xlabel("Percentage Change (%)")
plt.ylabel("Age Group")

plt.axvline(0, linestyle="--")

plt.tight_layout()
plt.show()

# ================================
# SECTION 8: HOSPITALIZATION ANALYSIS
# ================================

# Load Table 8
hosp_substances = pd.read_excel(
    file_path,
    sheet_name="8 Hosp type substances",
    header=None,
    skiprows=4,
    names=[
        "Substance",
        "Hosp_2019",
        "Hosp_2020",
        "Percentage_Change"
    ]
)

# Keep actual substance rows only
hosp_substances = hosp_substances.iloc[:8]

# this sheet already has named columns, so we clean Percentage_Change directly
hosp_substances["Percentage_Change"] = pd.to_numeric(
    hosp_substances["Percentage_Change"],
    errors="coerce"
) * 100

# Remove invalid rows
hosp_substances = hosp_substances.dropna()

# Sort substances by percentage change
hosp_rank = hosp_substances.sort_values(
    by="Percentage_Change",
    ascending=True
)

# Plot hospitalization percentage changes
plt.figure(figsize=(10,6))

plt.barh(
    hosp_rank["Substance"],
    hosp_rank["Percentage_Change"]
)

plt.title("Percentage Change in Substance-Related Hospitalizations")
plt.xlabel("Percentage Change (%)")
plt.ylabel("Substance")

# Add reference line
plt.axvline(0, linestyle="--")

plt.tight_layout()
plt.show()
