# Project 1 - Data Cleaning

This project is designed to make raw data reliable and analysis-ready.

## Project Goal
- Prevent analysis errors caused by missing, duplicated, or type-inconsistent data
- Produce a clean and consistent dataset to strengthen downstream analysis

## Folder Structure
- `data/raw/data.csv`: Raw dataset
- `src/cleaning.py`: Script that runs the cleaning pipeline
- `data/cleaned/cleaned_data.csv`: Cleaned output dataset
- `reports/summary.txt`: Summary of the performed operations

## Steps Performed and Why
1. Load the dataset
	- Why: To run all cleaning steps on a single dataframe.

2. Fill missing values in `CouponCode` with `NoCoupon`
	- Why: Missing values can lead to loss and inconsistency in analysis.
	- This approach preserves records while semantically completing missing coupon information.

3. Remove duplicate rows based on `OrderID`
	- Why: Counting the same order multiple times distorts revenue/sales metrics.
	- Goal: Ensure each order is represented once.

4. Convert `Date` to datetime type
	- Why: Required for accurate date-based analysis (daily/monthly trends, etc.).
	- With `errors="coerce"`, invalid dates become `NaT`, making them detectable.

5. Convert `Quantity`, `UnitPrice`, and `TotalPrice` to numeric types
	- Why: To ensure reliable numeric calculations.
	- Invalid values are marked as `NaN` and included in quality checks.

6. Recalculate `TotalPrice` as `Quantity * UnitPrice`
	- Why: To prevent inconsistencies and enforce business-rule correctness.

7. Final validation
	- Why: To verify that cleaning goals are achieved.
	- Checks: `Duplicate OrderID` and `Invalid Dates`.

8. Export the cleaned data
	- Why: To create a reusable output for analysis and reporting.

## Run
```bash
python src/cleaning.py
```

## Output
- `data/cleaned/cleaned_data.csv`

## Data Source
https://docs.google.com/spreadsheets/d/1G3ftbt4O2H6d_wZVmWtCqDNaBB89BCav/edit?usp=sharing&ouid=113342137189694556957&rtpof=true&sd=true
