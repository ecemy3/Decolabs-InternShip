from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.backends.backend_pdf import PdfPages


def trend_label(monthly_sales: pd.Series) -> str:
    """Return a simple trend label by comparing first and last month totals."""
    if monthly_sales.empty or len(monthly_sales) == 1:
        return "stable"

    first_value = float(monthly_sales.iloc[0])
    last_value = float(monthly_sales.iloc[-1])

    if last_value > first_value:
        return "increase"
    if last_value < first_value:
        return "decrease"
    return "stable"


def save_simple_bar_plot(series: pd.Series, title: str, y_label: str, output_path: Path) -> None:
    """Save a horizontal bar chart for a Series."""
    fig, ax = plt.subplots(figsize=(10, 6))
    series.sort_values(ascending=True).plot(kind="barh", ax=ax, color="#2c7fb8")
    ax.set_title(title)
    ax.set_xlabel(y_label)
    ax.set_ylabel("")
    ax.grid(axis="x", alpha=0.25)
    fig.tight_layout()
    fig.savefig(output_path, dpi=160)
    plt.close(fig)


def build_pdf_report(
    pdf_path: Path,
    summary_lines: list[str],
    product_revenue: pd.Series,
    order_status_counts: pd.Series,
    payment_revenue: pd.Series,
    month_sales: pd.Series,
    outliers: pd.DataFrame,
    customer_revenue: pd.Series,
) -> None:
    """Create a multi-page PDF report with summary and key plots."""
    with PdfPages(pdf_path) as pdf:
        fig, ax = plt.subplots(figsize=(8.27, 11.69))
        ax.axis("off")
        ax.text(
            0.03,
            0.97,
            "EDA REPORT SUMMARY",
            fontsize=18,
            fontweight="bold",
            va="top",
        )
        ax.text(0.03, 0.90, "\n".join(summary_lines), fontsize=11, va="top")
        pdf.savefig(fig)
        plt.close(fig)

        fig, ax = plt.subplots(figsize=(11, 6))
        product_revenue.sort_values(ascending=True).plot(kind="barh", ax=ax, color="#41ab5d")
        ax.set_title("Product Revenue")
        ax.set_xlabel("Total Revenue")
        ax.grid(axis="x", alpha=0.25)
        fig.tight_layout()
        pdf.savefig(fig)
        plt.close(fig)

        fig, ax = plt.subplots(figsize=(9, 6))
        order_status_counts.plot(kind="bar", ax=ax, color="#fe9929")
        ax.set_title("Order Status Distribution")
        ax.set_xlabel("Order Status")
        ax.set_ylabel("Count")
        ax.grid(axis="y", alpha=0.25)
        fig.tight_layout()
        pdf.savefig(fig)
        plt.close(fig)

        fig, ax = plt.subplots(figsize=(9, 6))
        payment_revenue.sort_values(ascending=False).plot(kind="bar", ax=ax, color="#9ecae1")
        ax.set_title("Revenue by Payment Method")
        ax.set_xlabel("Payment Method")
        ax.set_ylabel("Total Revenue")
        ax.grid(axis="y", alpha=0.25)
        fig.tight_layout()
        pdf.savefig(fig)
        plt.close(fig)

        fig, ax = plt.subplots(figsize=(11, 6))
        month_labels = month_sales.index.astype(str)
        ax.plot(month_labels, month_sales.values, marker="o", linewidth=1.8, color="#253494")
        ax.set_title("Monthly Sales Trend")
        ax.set_xlabel("Month")
        ax.set_ylabel("Total Revenue")
        ax.tick_params(axis="x", rotation=45)
        ax.grid(alpha=0.25)
        fig.tight_layout()
        pdf.savefig(fig)
        plt.close(fig)

        fig, ax = plt.subplots(figsize=(9, 6))
        ax.boxplot(outliers["TotalPrice"] if not outliers.empty else [0], vert=True)
        ax.set_title("Outlier Snapshot (TotalPrice)")
        ax.set_ylabel("TotalPrice")
        ax.grid(axis="y", alpha=0.25)
        fig.tight_layout()
        pdf.savefig(fig)
        plt.close(fig)

        fig, ax = plt.subplots(figsize=(11, 6))
        customer_revenue.head(10).sort_values(ascending=True).plot(kind="barh", ax=ax, color="#fdd49e")
        ax.set_title("Top 10 Customers by Revenue")
        ax.set_xlabel("Total Revenue")
        ax.grid(axis="x", alpha=0.25)
        fig.tight_layout()
        pdf.savefig(fig)
        plt.close(fig)


def main() -> None:
    project_root = Path(__file__).resolve().parents[1]
    preferred = project_root / "data" / "cleaned" / "cleanedEDA.csv"
    fallback_cleaned = project_root / "data" / "cleaned" / "cleaned_data.csv"
    fallback_raw = project_root / "data" / "raw" / "cleaned_data.csv"

    if preferred.exists():
        data_path = preferred
    elif fallback_cleaned.exists():
        data_path = fallback_cleaned
    elif fallback_raw.exists():
        data_path = fallback_raw
    else:
        raise FileNotFoundError(
            "Dataset not found. Expected one of: data/cleaned/cleanedEDA.csv, "
            "data/cleaned/cleaned_data.csv, data/raw/cleaned_data.csv"
        )

    df = pd.read_csv(data_path)

    print("=" * 70)
    print("1) DATASET LOADED")
    print(data_path)

    print("\n" + "=" * 70)
    print("2) DATA OVERVIEW")
    print("Shape:", df.shape)
    print("Columns:", list(df.columns))
    print("\nInfo:")
    print(df.info())
    print("\nDescribe (all numeric):")
    print(df.describe())

    print("\n" + "=" * 70)
    print("3) BASIC STATISTICS (TotalPrice)")
    totalprice_mean = df["TotalPrice"].mean()
    totalprice_median = df["TotalPrice"].median()
    totalprice_count = df["TotalPrice"].count()

    print("Mean:", totalprice_mean)
    print("Median:", totalprice_median)
    print("Count:", totalprice_count)

    print("\nExtra describe (Quantity, UnitPrice, TotalPrice):")
    print(df[["Quantity", "UnitPrice", "TotalPrice"]].describe())

    print("\n" + "=" * 70)
    print("4) PRODUCT ANALYSIS")
    product_revenue = df.groupby("Product")["TotalPrice"].sum().sort_values(ascending=False)
    print(product_revenue)
    top_product = str(product_revenue.index[0])
    low_product = str(product_revenue.index[-1])

    print("\n" + "=" * 70)
    print("5) ORDER STATUS ANALYSIS")
    order_status_counts = df["OrderStatus"].value_counts()
    print(order_status_counts)
    most_common_status = str(order_status_counts.index[0])

    print("\n" + "=" * 70)
    print("6) PAYMENT METHOD ANALYSIS")
    payment_revenue = df.groupby("PaymentMethod")["TotalPrice"].sum().sort_values(ascending=False)
    payment_counts = df["PaymentMethod"].value_counts()
    print("Revenue by payment method:")
    print(payment_revenue)
    print("\nUsage count by payment method:")
    print(payment_counts)
    top_payment_revenue = str(payment_revenue.index[0])
    most_used_payment = str(payment_counts.index[0])

    print("\n" + "=" * 70)
    print("7) TIME TREND ANALYSIS")
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    month_sales = (
        df.assign(Month=df["Date"].dt.to_period("M"))
        .groupby("Month")["TotalPrice"]
        .sum()
        .sort_index()
    )
    print(month_sales)
    sales_trend = trend_label(month_sales)

    print("\n" + "=" * 70)
    print("8) OUTLIER DETECTION (IQR on TotalPrice)")
    q1 = df["TotalPrice"].quantile(0.25)
    q3 = df["TotalPrice"].quantile(0.75)
    iqr = q3 - q1

    outliers = df[
        (df["TotalPrice"] < q1 - 1.5 * iqr)
        | (df["TotalPrice"] > q3 + 1.5 * iqr)
    ]
    print(outliers)
    outlier_count = len(outliers)

    print("\n" + "=" * 70)
    print("9) CUSTOMER ANALYSIS")
    customer_revenue = (
        df.groupby("CustomerID")["TotalPrice"].sum().sort_values(ascending=False)
    )
    print(customer_revenue.head(20))
    top_customer = str(customer_revenue.index[0])

    print("\n" + "=" * 70)
    print("10) FINAL INSIGHTS")

    reports_dir = project_root / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)
    figures_dir = reports_dir / "figures"
    figures_dir.mkdir(parents=True, exist_ok=True)

    summary_path = reports_dir / "eda_summary.txt"
    summary_lines = [
        f"1. The highest revenue comes from {top_product}",
        f"2. Most orders are in status: {most_common_status}",
        f"3. The most used payment method is {most_used_payment} (top revenue method: {top_payment_revenue})",
        f"4. Sales trend shows {sales_trend}",
        f"5. Outliers detected in high-value orders: {outlier_count}",
        f"6. Top customer by total revenue: {top_customer}",
        f"7. Lowest-revenue product: {low_product}",
    ]

    cancellation_count = int(order_status_counts.get("Cancelled", 0))
    cancellation_rate = cancellation_count / len(df) if len(df) else 0.0
    if cancellation_rate >= 0.20:
        cancellation_interpretation = (
            f"- High cancellation rate ({cancellation_rate:.1%}) may indicate operational issues."
        )
    else:
        cancellation_interpretation = (
            f"- Cancellation rate is moderate ({cancellation_rate:.1%}), but should still be monitored."
        )

    avg_order_by_payment = (
        df.groupby("PaymentMethod")["TotalPrice"].mean().sort_values(ascending=False)
    )
    payment_interpretation = (
        f"- {top_payment_revenue} generates the highest revenue; this likely reflects higher-value purchases."
    )
    if not avg_order_by_payment.empty:
        top_avg_payment = str(avg_order_by_payment.index[0])
        payment_interpretation += (
            f" Highest average order value is also in {top_avg_payment}."
        )

    if sales_trend == "decrease":
        trend_interpretation = (
            "- Sales decline over time may be linked to seasonality or demand softening."
        )
    elif sales_trend == "increase":
        trend_interpretation = (
            "- Sales growth indicates improving demand and/or stronger commercial performance."
        )
    else:
        trend_interpretation = (
            "- Sales are relatively stable; growth may require targeted campaigns."
        )

    interpretation_lines = [
        "BUSINESS INTERPRETATION",
        cancellation_interpretation,
        payment_interpretation,
        trend_interpretation,
    ]

    summary = "\n".join(["EDA SUMMARY", "", *summary_lines, "", *interpretation_lines, ""])
    summary_path.write_text(summary, encoding="utf-8")

    save_simple_bar_plot(
        product_revenue,
        "Product Revenue",
        "Total Revenue",
        figures_dir / "product_revenue.png",
    )
    save_simple_bar_plot(
        payment_revenue,
        "Revenue by Payment Method",
        "Total Revenue",
        figures_dir / "payment_revenue.png",
    )
    save_simple_bar_plot(
        order_status_counts,
        "Order Status Count",
        "Count",
        figures_dir / "order_status_counts.png",
    )

    trend_fig, trend_ax = plt.subplots(figsize=(10, 6))
    trend_ax.plot(month_sales.index.astype(str), month_sales.values, marker="o", color="#253494")
    trend_ax.set_title("Monthly Sales Trend")
    trend_ax.set_xlabel("Month")
    trend_ax.set_ylabel("Total Revenue")
    trend_ax.tick_params(axis="x", rotation=45)
    trend_ax.grid(alpha=0.25)
    trend_fig.tight_layout()
    trend_fig.savefig(figures_dir / "monthly_sales_trend.png", dpi=160)
    plt.close(trend_fig)

    box_fig, box_ax = plt.subplots(figsize=(8, 6))
    box_ax.boxplot(df["TotalPrice"], vert=True)
    box_ax.set_title("TotalPrice Distribution with Outlier Visibility")
    box_ax.set_ylabel("TotalPrice")
    box_ax.grid(axis="y", alpha=0.25)
    box_fig.tight_layout()
    box_fig.savefig(figures_dir / "totalprice_boxplot.png", dpi=160)
    plt.close(box_fig)

    pdf_path = reports_dir / "eda_report.pdf"
    build_pdf_report(
        pdf_path=pdf_path,
        summary_lines=[*summary_lines, "", *interpretation_lines],
        product_revenue=product_revenue,
        order_status_counts=order_status_counts,
        payment_revenue=payment_revenue,
        month_sales=month_sales,
        outliers=outliers,
        customer_revenue=customer_revenue,
    )

    print(summary)
    print(f"Summary written to: {summary_path}")
    print(f"Figures written to: {figures_dir}")
    print(f"PDF report written to: {pdf_path}")


if __name__ == "__main__":
    main()
