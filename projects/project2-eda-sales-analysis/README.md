# Project 2: EDA Sales Analysis

This project analyzes transaction-level sales data and turns raw records into business-facing insights and reporting artifacts.

## Project Structure

- `data/cleaned/cleanedEDA.csv` -> main cleaned dataset used by the analysis
- `data/raw/cleaned_data.csv` -> original uploaded file stored for traceability
- `data/raw/cleaned_data_from_cleaned_folder.csv` -> backup copy from previous cleaned location
- `src/eda_analysis.py` -> end-to-end EDA pipeline
- `reports/eda_results.txt` -> full terminal output from the pipeline
- `reports/eda_summary.txt` -> concise key findings + business interpretation
- `reports/eda_report.pdf` -> visual, submission-ready report
- `reports/figures/` -> generated PNG charts
- `requirements.txt` -> Python dependencies

## Run

```bash
d:/Decolabs/Project2/.venv/Scripts/python.exe src/eda_analysis.py
```

## Step-by-Step: What Was Done and Why

1. Dataset loading (`cleanedEDA.csv`)
Reason: Use a stable, cleaned source to avoid schema or formatting issues during analysis.

2. Data overview (`shape`, `columns`, `info`, `describe`)
Reason: Validate data quality, data types, and general distribution before drawing conclusions.

3. Basic statistics for `TotalPrice` (mean, median, count)
Reason: Establish central tendency and record volume for baseline business context.

4. Product revenue analysis (`groupby Product`)
Reason: Identify which products drive revenue and which underperform.

5. Order status analysis (`value_counts`)
Reason: Quantify fulfillment health and detect possible operational risk (for example, high cancellations).

6. Payment method analysis (usage + revenue)
Reason: Understand both customer preference and revenue concentration by payment type.

7. Time trend analysis (`Month` aggregation)
Reason: Observe whether sales are growing, stable, or declining over time.

8. Outlier detection (IQR on `TotalPrice`)
Reason: Flag unusually large or small orders that may represent anomalies or high-value opportunities.

9. Customer value analysis (`groupby CustomerID`)
Reason: Identify top-value customers for retention and targeted strategy.

10. Final summary report generation (`reports/eda_summary.txt`)
Reason: Provide a compact decision-oriented narrative for non-technical stakeholders.

11. Business interpretation block
Reason: Translate statistical findings into operational and commercial implications.

12. Figure export (`reports/figures/*.png`)
Reason: Produce reusable visuals for presentations and documentation.

13. PDF report generation (`reports/eda_report.pdf`)
Reason: Deliver a single, shareable artifact that combines insights and visuals.
