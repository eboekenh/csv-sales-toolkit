#!/usr/bin/env python3
"""
CSV Sales Toolkit - Day 2: Sales Analyzer & Report
Loads the cleaned orders CSV from Day 1, computes business metrics,
and produces a formatted text report.
"""

import pandas as pd
from datetime import datetime

# ---------------------------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------------------------
INPUT_FILE = "orders_clean.csv"
OUTPUT_FILE = "sales_report.txt"
LINE = "=" * 80
THIN = "-" * 80


# ---------------------------------------------------------------------------
# LOADING
# ---------------------------------------------------------------------------
def load_data(path):
    """Load the cleaned CSV; return the DataFrame or None on failure."""
    try:
        return pd.read_csv(path)
    except FileNotFoundError:
        print(f"\u2717 File not found: {path}")
        print(" Run the Day 1 cleaner first to produce orders_clean.csv")
        return None


# ---------------------------------------------------------------------------
# METRIC CALCULATIONS
# Each function takes data and returns numbers - no printing here.
# ---------------------------------------------------------------------------
def headline_metrics(df, completed, cancelled):
    """Calculate the top-level summary numbers."""
    total_revenue = completed["total_price"].sum()
    order_count = len(completed)
    items_sold = int(completed["quantity"].sum())
    average_order = total_revenue / order_count if order_count else 0
    cancellation_rate = len(cancelled) / len(df) * 100 if len(df) else 0
    return {
        "total_orders": len(df),
        "completed_orders": order_count,
        "cancelled_orders": len(cancelled),
        "cancellation_rate": cancellation_rate,
        "total_revenue": total_revenue,
        "average_order": average_order,
        "items_sold": items_sold,
    }


def revenue_by_category(completed):
    """Total revenue per category, biggest first."""
    return (
        completed.groupby("category")["total_price"]
        .sum()
        .sort_values(ascending=False)
    )


def top_products_by_revenue(completed, n=5):
    """The top n products by total revenue."""
    return (
        completed.groupby("product")["total_price"]
        .sum()
        .sort_values(ascending=False)
        .head(n)
    )


def top_products_by_quantity(completed, n=5):
    """The top n products by units sold."""
    return (
        completed.groupby("product")["quantity"]
        .sum()
        .sort_values(ascending=False)
        .head(n)
    )


def daily_sales(completed):
    """Total revenue per day, in date order."""
    completed = completed.copy()
    completed["order_date"] = pd.to_datetime(completed["order_date"])
    return (
        completed.groupby("order_date")["total_price"]
        .sum()
        .sort_index()
    )


# ---------------------------------------------------------------------------
# REPORT BUILDING
# Build the whole report as a list of lines, then join once.
# ---------------------------------------------------------------------------
def build_report(df):
    """Build the full formatted report and return it as a string."""
    completed = df[df["status"] == "completed"]
    cancelled = df[df["status"] == "cancelled"]
    lines = []

    # --- Header ---
    lines.append(LINE)
    lines.append("SALES ANALYSIS REPORT")
    lines.append(LINE)
    lines.append("")
    lines.append(f"Source: {INPUT_FILE}")
    lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d')}")
    lines.append("")

    # --- Headline metrics ---
    m = headline_metrics(df, completed, cancelled)
    lines.append(THIN)
    lines.append("HEADLINE METRICS")
    lines.append(THIN)
    lines.append("")
    lines.append(f"  Total orders:          {m['total_orders']}")
    lines.append(f"  Completed orders:      {m['completed_orders']}")
    lines.append(f"  Cancelled orders:      {m['cancelled_orders']}")
    lines.append(f"  Cancellation rate:     {m['cancellation_rate']:.1f}%")
    lines.append("")
    lines.append(f"  Total revenue:         ${m['total_revenue']:,.2f}")
    lines.append(f"  Average order value:   ${m['average_order']:,.2f}")
    lines.append(f"  Items sold:            {m['items_sold']}")
    lines.append("")

    # --- Revenue by category ---
    cat_revenue = revenue_by_category(completed)
    total = cat_revenue.sum()
    lines.append(THIN)
    lines.append("REVENUE BY CATEGORY")
    lines.append(THIN)
    lines.append("")
    for category, revenue in cat_revenue.items():
        share = revenue / total * 100 if total else 0
        lines.append(f"  {category:<20} ${revenue:>9,.2f}  ({share:.1f}%)")
    lines.append("")

    # --- Top products by revenue ---
    lines.append(THIN)
    lines.append("TOP PRODUCTS BY REVENUE")
    lines.append(THIN)
    lines.append("")
    for i, (product, revenue) in enumerate(top_products_by_revenue(completed).items(), 1):
        lines.append(f"  {i}. {product:<20} ${revenue:>9,.2f}")
    lines.append("")

    # --- Top products by quantity ---
    lines.append(THIN)
    lines.append("TOP PRODUCTS BY QUANTITY SOLD")
    lines.append(THIN)
    lines.append("")
    for i, (product, qty) in enumerate(top_products_by_quantity(completed).items(), 1):
        lines.append(f"  {i}. {product:<20}   {qty:>3} units")
    lines.append("")

    # --- Daily trend ---
    daily = daily_sales(completed)
    lines.append(THIN)
    lines.append("DAILY SALES TREND")
    lines.append(THIN)
    lines.append("")
    for date, revenue in daily.items():
        lines.append(f"  {date.strftime('%Y-%m-%d')}   ${revenue:>8,.2f}")
    lines.append("")
    best_day = daily.idxmax()
    best_amount = daily.max()
    lines.append(f"  Best day: {best_day.strftime('%Y-%m-%d')} (${best_amount:,.2f})")
    lines.append("")
    lines.append(LINE)

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# SAVING
# ---------------------------------------------------------------------------
def save_report(text, path):
    """Write the report text to a file."""
    with open(path, "w") as f:
        f.write(text)


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------
def main():
    df = load_data(INPUT_FILE)
    if df is None:
        return
    report = build_report(df)
    # Show it on screen.
    print(report)
    # And save it to a file.
    save_report(report, OUTPUT_FILE)
    print(f"\u2713 Report saved: {OUTPUT_FILE}")
    print(LINE)


if __name__ == "__main__":
    main()
