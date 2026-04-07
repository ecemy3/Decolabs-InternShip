from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.ticker import FuncFormatter

PROJECT_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_DIR / "data" / "cleaned" / "cleanedEDA.csv"
CHART_DIR = PROJECT_DIR / "reports" / "figures"
REPORT_PATH = PROJECT_DIR / "reports" / "project4_story_report.txt"


def currency_axis_formatter(value, _):
    return f"${value:,.0f}"


def money(value):
    return f"${value:,.0f}"


def setup_style():
    sns.set_theme(style="whitegrid")
    plt.rcParams.update(
        {
            "figure.dpi": 130,
            "axes.titlesize": 14,
            "axes.labelsize": 11,
            "xtick.labelsize": 10,
            "ytick.labelsize": 10,
        }
    )


def load_data(path):
    df = pd.read_csv(path)
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df["TotalPrice"] = pd.to_numeric(df["TotalPrice"], errors="coerce")
    df = df.dropna(subset=["Date", "TotalPrice", "Product", "OrderStatus", "PaymentMethod"])
    return df


def plot_product_revenue(df):
    revenue = (
        df.groupby("Product", as_index=False)["TotalPrice"]
        .sum()
        .sort_values("TotalPrice", ascending=False)
        .reset_index(drop=True)
    )

    top_product = revenue.loc[0, "Product"]
    top_value = revenue.loc[0, "TotalPrice"]
    low_product = revenue.loc[len(revenue) - 1, "Product"]
    low_value = revenue.loc[len(revenue) - 1, "TotalPrice"]

    colors = []
    for product in revenue["Product"]:
        if product == top_product:
            colors.append("#1f8a70")
        elif product == low_product:
            colors.append("#d64550")
        else:
            colors.append("#7aa6c2")

    fig, ax = plt.subplots(figsize=(11, 6))
    bars = ax.bar(revenue["Product"], revenue["TotalPrice"], color=colors)

    ax.set_title(
        "Chairs and Printers lead revenue while Phones lag, signaling product mix pressure",
        loc="left",
        fontweight="bold",
    )
    ax.set_xlabel("Product")
    ax.set_ylabel("Revenue")
    ax.yaxis.set_major_formatter(FuncFormatter(currency_axis_formatter))

    for bar in bars:
        ax.annotate(
            money(bar.get_height()),
            xy=(bar.get_x() + bar.get_width() / 2, bar.get_height()),
            xytext=(0, 4),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=9,
        )

    ax.annotate(
        f"Top: {top_product} ({money(top_value)})",
        xy=(0.01, 0.96),
        xycoords="axes fraction",
        ha="left",
        va="top",
        fontsize=10,
        fontweight="bold",
        color="#1f8a70",
    )
    ax.annotate(
        f"Lowest: {low_product} ({money(low_value)})",
        xy=(0.01, 0.90),
        xycoords="axes fraction",
        ha="left",
        va="top",
        fontsize=10,
        fontweight="bold",
        color="#d64550",
    )

    fig.tight_layout()
    fig.savefig(CHART_DIR / "product_revenue.png", bbox_inches="tight")
    plt.close(fig)

    return revenue


def plot_sales_trend(df):
    monthly = (
        df.set_index("Date")
        .resample("ME")["TotalPrice"]
        .sum()
        .reset_index()
        .rename(columns={"TotalPrice": "Revenue"})
    )

    x = np.arange(len(monthly))
    trend_coef = np.polyfit(x, monthly["Revenue"], 1)
    trend = np.poly1d(trend_coef)(x)

    start_revenue = monthly.iloc[0]["Revenue"]
    end_revenue = monthly.iloc[-1]["Revenue"]
    pct_change = ((end_revenue - start_revenue) / start_revenue) * 100 if start_revenue else 0

    peak_idx = monthly["Revenue"].idxmax()
    low_idx = monthly["Revenue"].idxmin()

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(monthly["Date"], monthly["Revenue"], marker="o", linewidth=2.2, color="#2b6cb0", label="Monthly revenue")
    ax.plot(monthly["Date"], trend, linestyle="--", linewidth=2, color="#d64550", label="Trend line")

    ax.scatter(monthly.loc[peak_idx, "Date"], monthly.loc[peak_idx, "Revenue"], color="#1f8a70", s=90, zorder=5)
    ax.scatter(monthly.loc[low_idx, "Date"], monthly.loc[low_idx, "Revenue"], color="#d64550", s=90, zorder=5)

    ax.set_title(
        "Monthly sales are softening over time, indicating weaker demand",
        loc="left",
        fontweight="bold",
    )
    ax.set_xlabel("Month")
    ax.set_ylabel("Revenue")
    ax.yaxis.set_major_formatter(FuncFormatter(currency_axis_formatter))
    ax.legend(loc="upper right")

    ax.annotate(
        f"Start: {money(start_revenue)} | End: {money(end_revenue)} ({pct_change:+.1f}%)",
        xy=(0.01, 0.96),
        xycoords="axes fraction",
        ha="left",
        va="top",
        fontsize=10,
        fontweight="bold",
    )

    for label in ax.get_xticklabels():
        label.set_rotation(45)
        label.set_horizontalalignment("right")

    fig.tight_layout()
    fig.savefig(CHART_DIR / "sales_trend.png", bbox_inches="tight")
    plt.close(fig)

    return monthly, pct_change


def plot_order_status(df):
    status = (
        df["OrderStatus"]
        .value_counts()
        .rename_axis("OrderStatus")
        .reset_index(name="Count")
        .sort_values("Count", ascending=False)
        .reset_index(drop=True)
    )
    status["Pct"] = (status["Count"] / len(df)) * 100

    risk_statuses = {"Cancelled", "Returned"}
    colors = ["#d64550" if row in risk_statuses else "#7aa6c2" for row in status["OrderStatus"]]

    risk_pct = status.loc[status["OrderStatus"].isin(risk_statuses), "Pct"].sum()
    delivered_pct = status.loc[status["OrderStatus"] == "Delivered", "Pct"].sum()

    fig, ax = plt.subplots(figsize=(11, 6))
    bars = ax.bar(status["OrderStatus"], status["Count"], color=colors)

    ax.set_title(
        "Cancelled and Returned orders exceed 40%, exposing a severe execution risk",
        loc="left",
        fontweight="bold",
    )
    ax.set_xlabel("Order status")
    ax.set_ylabel("Order count")

    for bar, pct in zip(bars, status["Pct"]):
        ax.annotate(
            f"{int(bar.get_height())} ({pct:.1f}%)",
            xy=(bar.get_x() + bar.get_width() / 2, bar.get_height()),
            xytext=(0, 4),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=9,
        )

    ax.annotate(
        f"Risk statuses (Cancelled + Returned): {risk_pct:.1f}% | Delivered: {delivered_pct:.1f}%",
        xy=(0.01, 0.96),
        xycoords="axes fraction",
        ha="left",
        va="top",
        fontsize=10,
        fontweight="bold",
    )

    fig.tight_layout()
    fig.savefig(CHART_DIR / "order_status.png", bbox_inches="tight")
    plt.close(fig)

    return status


def plot_payment_analysis(df):
    payment = (
        df.groupby("PaymentMethod", as_index=False)
        .agg(Revenue=("TotalPrice", "sum"), Transactions=("OrderID", "count"))
        .sort_values("Revenue", ascending=False)
        .reset_index(drop=True)
    )

    top_revenue_method = payment.loc[payment["Revenue"].idxmax(), "PaymentMethod"]
    top_revenue_value = payment.loc[payment["Revenue"].idxmax(), "Revenue"]
    top_usage_method = payment.loc[payment["Transactions"].idxmax(), "PaymentMethod"]
    top_usage_count = payment.loc[payment["Transactions"].idxmax(), "Transactions"]

    fig, axes = plt.subplots(1, 2, figsize=(15, 6))

    revenue_colors = ["#1f8a70" if m == top_revenue_method else "#7aa6c2" for m in payment["PaymentMethod"]]
    trans_colors = ["#2b6cb0" if m == top_usage_method else "#b7c7d6" for m in payment["PaymentMethod"]]

    bars1 = axes[0].bar(payment["PaymentMethod"], payment["Revenue"], color=revenue_colors)
    axes[0].set_title("Revenue by payment method", fontweight="bold")
    axes[0].set_ylabel("Revenue")
    axes[0].yaxis.set_major_formatter(FuncFormatter(currency_axis_formatter))
    axes[0].tick_params(axis="x", rotation=30)

    for bar in bars1:
        axes[0].annotate(
            money(bar.get_height()),
            xy=(bar.get_x() + bar.get_width() / 2, bar.get_height()),
            xytext=(0, 4),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=8,
        )

    bars2 = axes[1].bar(payment["PaymentMethod"], payment["Transactions"], color=trans_colors)
    axes[1].set_title("Transactions by payment method", fontweight="bold")
    axes[1].set_ylabel("Transaction count")
    axes[1].tick_params(axis="x", rotation=30)

    for bar in bars2:
        axes[1].annotate(
            f"{int(bar.get_height())}",
            xy=(bar.get_x() + bar.get_width() / 2, bar.get_height()),
            xytext=(0, 4),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=8,
        )

    fig.suptitle(
        "Credit Card drives the highest revenue while Online is the most used method",
        x=0.05,
        y=1.03,
        ha="left",
        fontsize=14,
        fontweight="bold",
    )

    fig.tight_layout()
    fig.savefig(CHART_DIR / "payment.png", bbox_inches="tight")
    plt.close(fig)

    return payment


def plot_outlier_boxplot(df):
    high_value_count = int((df["TotalPrice"] > 3000).sum())
    high_value_ratio = (high_value_count / len(df)) * 100 if len(df) else 0

    fig, ax = plt.subplots(figsize=(12, 6))
    sns.boxplot(data=df, x="Product", y="TotalPrice", color="#9bb9cf", ax=ax)
    ax.axhline(3000, color="#d64550", linestyle="--", linewidth=2, label="Outlier threshold ($3,000)")

    ax.set_title(
        "A small set of high-value outliers can materially swing reported performance",
        loc="left",
        fontweight="bold",
    )
    ax.set_xlabel("Product")
    ax.set_ylabel("Order value")
    ax.yaxis.set_major_formatter(FuncFormatter(currency_axis_formatter))
    ax.legend(loc="upper right")

    ax.annotate(
        f"Orders above $3,000: {high_value_count} ({high_value_ratio:.1f}%)",
        xy=(0.01, 0.96),
        xycoords="axes fraction",
        ha="left",
        va="top",
        fontsize=10,
        fontweight="bold",
    )

    fig.tight_layout()
    fig.savefig(CHART_DIR / "outlier_orders.png", bbox_inches="tight")
    plt.close(fig)

    return high_value_count, high_value_ratio


def write_story_report(df, revenue, monthly, trend_pct, status, payment, outlier_count, outlier_ratio):
    top_product = revenue.iloc[0]
    low_product = revenue.iloc[-1]

    risk_pct = status.loc[status["OrderStatus"].isin(["Cancelled", "Returned"]), "Pct"].sum()
    delivered_pct = status.loc[status["OrderStatus"] == "Delivered", "Pct"].sum()

    top_revenue_payment = payment.loc[payment["Revenue"].idxmax()]
    top_usage_payment = payment.loc[payment["Transactions"].idxmax()]

    start_month = monthly.iloc[0]["Date"].strftime("%b %Y")
    end_month = monthly.iloc[-1]["Date"].strftime("%b %Y")

    report = f"""PROJECT 4 - VISUAL STORYTELLING REPORT

Situation:
Sales operations are active across products, channels, and payment methods. The business generated {money(df['TotalPrice'].sum())} from {len(df):,} orders, showing strong transaction volume.

Complication:
1) Product mix pressure: {top_product['Product']} leads with {money(top_product['TotalPrice'])}, while {low_product['Product']} trails at {money(low_product['TotalPrice'])}.
2) Demand softening: Monthly revenue from {start_month} to {end_month} changed by {trend_pct:+.1f}%, signaling weaker momentum.
3) Fulfillment risk: Cancelled + Returned orders account for {risk_pct:.1f}% of all orders, while Delivered is only {delivered_pct:.1f}%.
4) Payment imbalance: {top_revenue_payment['PaymentMethod']} has the highest revenue ({money(top_revenue_payment['Revenue'])}), but {top_usage_payment['PaymentMethod']} is used most ({int(top_usage_payment['Transactions'])} transactions), indicating usage and value are not aligned.

Resolution (So What / What should we do next?):
1) Protect revenue quality: Reduce cancellations and returns with stricter order verification, faster support response, and root-cause analysis by product and referral source.
2) Recover demand: Launch targeted campaigns in low months and test product bundles around high performers (Chair/Printer/Laptop).
3) Improve conversion to delivered orders: Track cancellation and return KPIs weekly and assign ownership to operations.
4) Optimize payment strategy: Incentivize higher-value payment behaviors while keeping Online friction low.
5) Monitor outliers separately: {outlier_count} orders ({outlier_ratio:.1f}%) exceed $3,000; track them as a special segment because they can distort monthly performance.

Action Titles Used In Charts:
1) Chairs and Printers lead revenue while Phones lag, signaling product mix pressure.
2) Monthly sales are softening over time, indicating weaker demand.
3) Cancelled and Returned orders exceed 40%, exposing a severe execution risk.
4) Credit Card drives the highest revenue while Online is the most used method.
5) A small set of high-value outliers can materially swing reported performance.
"""

    REPORT_PATH.write_text(report, encoding="utf-8")


def main():
    CHART_DIR.mkdir(parents=True, exist_ok=True)
    setup_style()
    df = load_data(DATA_PATH)

    revenue = plot_product_revenue(df)
    monthly, trend_pct = plot_sales_trend(df)
    status = plot_order_status(df)
    payment = plot_payment_analysis(df)
    outlier_count, outlier_ratio = plot_outlier_boxplot(df)

    write_story_report(df, revenue, monthly, trend_pct, status, payment, outlier_count, outlier_ratio)

    print("Project 4 outputs created:")
    print(f"- {CHART_DIR / 'product_revenue.png'}")
    print(f"- {CHART_DIR / 'sales_trend.png'}")
    print(f"- {CHART_DIR / 'order_status.png'}")
    print(f"- {CHART_DIR / 'payment.png'}")
    print(f"- {CHART_DIR / 'outlier_orders.png'}")
    print(f"- {REPORT_PATH}")


if __name__ == "__main__":
    main()