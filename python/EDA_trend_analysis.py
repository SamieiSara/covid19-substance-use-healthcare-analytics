# ============================================================
# EXPLORATORY DATA ANALYSIS (EDA) & TREND EXPLORATION
# COVID-19 Substance Use & Healthcare Harm Analytics Project
#
# Description:
# This script performs exploratory analysis on CIHI's public
# healthcare reporting data related to substance-related harms
# during the COVID-19 pandemic.
#
# The goal is to explore trends in emergency department (ED)
# visits, hospitalizations, opioid poisonings, and healthcare
# burden before building the final interactive dashboard in
# Power BI.
#
# Python is used for data exploration, validation, trend analysis,
# and preparing analysis-ready tables. Final interactive KPIs and
# dashboard measures are developed in Power BI using DAX.
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


# ================================
# SECTION 2: LOAD AND REVIEW DATA
# ================================

# File path for the CIHI Excel data table
file_path = "../data/raw/unintended-consequences-covid-19-substance-use-data-table-en.xlsx"

# Open the Excel workbook
excel_file = pd.ExcelFile(file_path)

# Review all available sheets in the workbook
print("Available Sheets:")
for sheet in excel_file.sheet_names:
    print(sheet)


# Load the main tables needed for analysis
# The CIHI workbook contains notes and titles above the actual tables,
# so header rows are adjusted based on where each table begins.

ed_substances = pd.read_excel(
    file_path,
    sheet_name="1 ED type substances",
    header=4
)

ed_monthly = pd.read_excel(
    file_path,
    sheet_name="2 ED volume by month ",
    header=4
)

ed_opioids = pd.read_excel(
    file_path,
    sheet_name="5 ED opioids",
    header=4
)

hosp_substances = pd.read_excel(
    file_path,
    sheet_name="8 Hosp type substances",
    header=4
)

hosp_monthly = pd.read_excel(
    file_path,
    sheet_name="9 Hosp volume by month",
    header=4
)

hosp_opioids = pd.read_excel(
    file_path,
    sheet_name="12 Hosp opioids",
    header=4
)


# Preview the loaded tables
print("\nED Substance Table:")
print(ed_substances.head())

print("\nED Monthly Trend Table:")
print(ed_monthly.head())

print("\nED Opioid Table:")
print(ed_opioids.head())

print("\nHospitalization Substance Table:")
print(hosp_substances.head())

print("\nHospitalization Monthly Trend Table:")
print(hosp_monthly.head())

print("\nHospitalization Opioid Table:")
print(hosp_opioids.head())


# Review table dimensions
print("\nTable Shapes:")
print("ED Substances:", ed_substances.shape)
print("ED Monthly:", ed_monthly.shape)
print("ED Opioids:", ed_opioids.shape)
print("Hospitalization Substances:", hosp_substances.shape)
print("Hospitalization Monthly:", hosp_monthly.shape)
print("Hospitalization Opioids:", hosp_opioids.shape)


# ================================
# SECTION 3: BASIC DATA PREPARATION
# ================================

# Remove fully empty rows and columns
ed_substances = ed_substances.dropna(how="all").dropna(axis=1, how="all")
hosp_substances = hosp_substances.dropna(how="all").dropna(axis=1, how="all")
ed_opioids = ed_opioids.dropna(how="all").dropna(axis=1, how="all")
hosp_opioids = hosp_opioids.dropna(how="all").dropna(axis=1, how="all")

# Rename substance summary columns for easier analysis
ed_substances.columns = [
    "Substance",
    "ED_2019",
    "ED_2020",
    "ED_Percentage_Change"
]

hosp_substances.columns = [
    "Substance",
    "Hosp_2019",
    "Hosp_2020",
    "Hosp_Percentage_Change"
]

# Remove rows where the main category is missing
ed_substances = ed_substances.dropna(subset=["Substance"])
hosp_substances = hosp_substances.dropna(subset=["Substance"])


# ================================
# SECTION 4: SUBSTANCE-LEVEL ANALYSIS
# ================================

# Merge ED and hospitalization tables by substance type
substance_summary = ed_substances.merge(
    hosp_substances,
    on="Substance",
    how="inner"
)

print("\nSubstance Summary:")
print(substance_summary.head())


# Rank substances by ED visit percentage change
ed_growth_rank = substance_summary.sort_values(
    by="ED_Percentage_Change",
    ascending=False
)

print("\nSubstances Ranked by ED Visit Growth:")
print(
    ed_growth_rank[
        ["Substance", "ED_2019", "ED_2020", "ED_Percentage_Change"]
    ]
)


# Rank substances by hospitalization percentage change
hosp_growth_rank = substance_summary.sort_values(
    by="Hosp_Percentage_Change",
    ascending=False
)

print("\nSubstances Ranked by Hospitalization Growth:")
print(
    hosp_growth_rank[
        ["Substance", "Hosp_2019", "Hosp_2020", "Hosp_Percentage_Change"]
    ]
)


# ================================
# SECTION 5: ED VISITS VS HOSPITALIZATIONS
# ================================

# Compare ED visit percentage change by substance
plt.figure(figsize=(10, 6))
plt.bar(
    substance_summary["Substance"],
    substance_summary["ED_Percentage_Change"]
)
plt.title("Percentage Change in ED Visits by Substance")
plt.xlabel("Substance")
plt.ylabel("Percentage Change")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.show()


# Compare hospitalization percentage change by substance
plt.figure(figsize=(10, 6))
plt.bar(
    substance_summary["Substance"],
    substance_summary["Hosp_Percentage_Change"]
)
plt.title("Percentage Change in Hospitalizations by Substance")
plt.xlabel("Substance")
plt.ylabel("Percentage Change")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.show()


# ================================
# SECTION 6: HEALTHCARE BURDEN ANALYSIS
# ================================

# Calculate hospitalization-to-ED ratio for each substance
# This helps identify whether substance-related cases became
# more hospital-intensive during the pandemic.

substance_summary["Hosp_to_ED_Ratio_2019"] = (
    substance_summary["Hosp_2019"] / substance_summary["ED_2019"]
)

substance_summary["Hosp_to_ED_Ratio_2020"] = (
    substance_summary["Hosp_2020"] / substance_summary["ED_2020"]
)

substance_summary["Ratio_Change"] = (
    substance_summary["Hosp_to_ED_Ratio_2020"]
    - substance_summary["Hosp_to_ED_Ratio_2019"]
)

print("\nHospitalization-to-ED Ratio by Substance:")
print(
    substance_summary[
        [
            "Substance",
            "Hosp_to_ED_Ratio_2019",
            "Hosp_to_ED_Ratio_2020",
            "Ratio_Change"
        ]
    ]
)


# Visualize change in hospitalization-to-ED ratio
plt.figure(figsize=(10, 6))
plt.bar(
    substance_summary["Substance"],
    substance_summary["Ratio_Change"]
)
plt.title("Change in Hospitalization-to-ED Ratio by Substance")
plt.xlabel("Substance")
plt.ylabel("Ratio Change")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.show()


# ================================
# SECTION 7: OPIOID TREND ANALYSIS
# ================================

# Rename opioid tables for readability
ed_opioids.columns = [
    "Month",
    "ED_Opioid_Poisoning_2019",
    "ED_Opioid_Poisoning_2020",
    "ED_Opioid_Poisoning_Percentage_Change",
    "ED_Opioid_Use_Disorder_2019",
    "ED_Opioid_Use_Disorder_2020",
    "ED_Opioid_Use_Disorder_Percentage_Change"
]

hosp_opioids.columns = [
    "Month",
    "Hosp_Opioid_Poisoning_2019",
    "Hosp_Opioid_Poisoning_2020",
    "Hosp_Opioid_Poisoning_Percentage_Change",
    "Hosp_Opioid_Use_Disorder_2019",
    "Hosp_Opioid_Use_Disorder_2020",
    "Hosp_Opioid_Use_Disorder_Percentage_Change"
]

# Remove rows without month values
ed_opioids = ed_opioids.dropna(subset=["Month"])
hosp_opioids = hosp_opioids.dropna(subset=["Month"])


# Plot ED opioid poisoning percentage change
plt.figure(figsize=(10, 6))
plt.plot(
    ed_opioids["Month"],
    ed_opioids["ED_Opioid_Poisoning_Percentage_Change"],
    marker="o"
)
plt.title("Monthly Percentage Change in ED Visits for Opioid Poisoning")
plt.xlabel("Month")
plt.ylabel("Percentage Change")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# Plot hospitalization opioid poisoning percentage change
plt.figure(figsize=(10, 6))
plt.plot(
    hosp_opioids["Month"],
    hosp_opioids["Hosp_Opioid_Poisoning_Percentage_Change"],
    marker="o"
)
plt.title("Monthly Percentage Change in Hospitalizations for Opioid Poisoning")
plt.xlabel("Month")
plt.ylabel("Percentage Change")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# ================================
# SECTION 8: SPIKE DETECTION
# ================================

# Identify months with the highest opioid poisoning growth
highest_ed_opioid_spike = ed_opioids.loc[
    ed_opioids["ED_Opioid_Poisoning_Percentage_Change"].idxmax()
]

highest_hosp_opioid_spike = hosp_opioids.loc[
    hosp_opioids["Hosp_Opioid_Poisoning_Percentage_Change"].idxmax()
]

print("\nHighest ED Opioid Poisoning Spike:")
print(highest_ed_opioid_spike)

print("\nHighest Hospitalization Opioid Poisoning Spike:")
print(highest_hosp_opioid_spike)


# ================================
# SECTION 9: ANALYTICAL SUMMARY FOR DASHBOARD DESIGN
# ================================

# This summary supports dashboard planning and validation.
# Final interactive KPI cards and measures should be created in
# Power BI using DAX.

dashboard_summary = pd.DataFrame({
    "Metric": [
        "Highest ED Growth Substance",
        "Highest Hospitalization Growth Substance",
        "Highest ED Opioid Poisoning Spike Month",
        "Highest Hospitalization Opioid Poisoning Spike Month"
    ],
    "Value": [
        ed_growth_rank.iloc[0]["Substance"],
        hosp_growth_rank.iloc[0]["Substance"],
        highest_ed_opioid_spike["Month"],
        highest_hosp_opioid_spike["Month"]
    ]
})

print("\nAnalytical Summary for Dashboard Design:")
print(dashboard_summary)


# ================================
# SECTION 10: EXPORT OUTPUTS
# ================================

# Export analysis-ready files for Power BI if needed.
# These files support dashboard development but do not replace
# DAX measures in Power BI.

substance_summary.to_csv(
    "../data/processed/substance_summary.csv",
    index=False
)

ed_opioids.to_csv(
    "../data/processed/ed_opioid_trends.csv",
    index=False
)

hosp_opioids.to_csv(
    "../data/processed/hospitalization_opioid_trends.csv",
    index=False
)

dashboard_summary.to_csv(
    "../data/processed/dashboard_summary.csv",
    index=False
)

print("\nExport completed successfully.")
