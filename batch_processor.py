#!/usr/bin/env python3
"""
CSV Sales Toolkit - Day 3: Batch CSV Processor
Discovers every CSV in a folder, cleans each one, merges them all into a
single dataset, and produces a consolidated multi-month sales report.
"""

import pandas as pd
from pathlib import Path
from datetime import datetime

# ---------------------------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------------------------
INPUT_FOLDER = "monthly_sales"
COMBINED_OUTPUT = "all_sales_clean.csv"
REPORT_OUTPUT = "consolidated_report.txt"
TEXT_COLUMNS = ["customer_name", "product", "category", "status"]
LINE = "=" * 80
THIN = "-" * 80


# ---------------------------------------------------------------------------
# CLEANING (lifted from Day 1, packaged as a reusable function)
# ---------------------------------------------------------------------------
def clean_dataframe(df):
    """Apply the full Day 1 cleaning pipeline and return the cleaned DataFrame."""
    # Strip whitespace from text columns.
    for col in TEXT_COLUMNS:
        df[col] = df[col].astype(str).str.strip()

    # Standardize capitalization.
    df["category"] = df["category"].str.title()
    df["status"] = df["status"].str.lower()

    # Fix the price column.
    df["unit_price"] = (
        df["unit_price"]
        .astype(str)
        .str.replace("$", "", regex=False)
        .str.replace(",", "", regex=False)
    )
    df["unit_price"] = pd.to_numeric(df["unit_price"], errors="coerce")

    # Fix quantity.
    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
    df["quantity"] = df["quantity"].fillna(1).astype(int)

    # Fill missing prices with the category average.
    category_avg = df.groupby("category")["unit_price"].transform("mean")
    df["unit_price"] = df["unit_price"].fillna(category_avg).round(2)

    # Add the calculated total_price column.
    df["total_price"] = (df["quantity"] * df["unit_price"]).round(2)

    return df


# ---------------------------------------------------------------------------
# BATCH PROCESSING
# ---------------------------------------------------------------------------
def discover_files(folder):
    """Find every CSV in the folder, sorted for predictable ordering."""
    return sorted(Path(folder).glob("*.csv"))


def process_files(csv_files):
    """Clean every file; collect successes, log failures, return both."""
    cleaned_dfs = []
    failures = []

    print("\nProcessing files...")
    for i, path in enumerate(csv_files, 1):
        try:
            df = pd.read_csv(path)
            df = clean_dataframe(df)
            cleaned_dfs.append(df)
            print(f"  [{i}/{len(csv_files)}] {path.name} "
                  f"\u2713 {len(df)} rows cleaned")
        except Exception as e:
            failures.append((path.name, str(e)))
            print(f"  [{i}/{len(csv_files)}] {path.name} \u2717 {e}")

    return cleaned_dfs, failures


# ---------------------------------------------------------------------------
# METRIC CALCULATIONS
# ---------------------------------------------------------------------------
def headline_metrics(df, completed, cancelled):
    """Top-level summary numbers."""
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


def monthly_breakdown(completed):
    """Orders and revenue per month, with month-over-month change."""
    monthly = (
        completed.assign(month=completed["order_date"].dt.to_period("M"))
        .groupby("month")
        .agg(
            orders=("order_id", "count"),
            revenue=("total_price", "sum"),
        )
    )
    monthly["change"] = monthly["revenue"].pct_change() * 100
    return monthly


def revenue_by_category(completed):
    """Total revenue per category across the full period."""
    return (
        completed.groupby("category")["total_price"]
        .sum()
        .sort_values(ascending=False)
    )


def top_products(completed, n=5):
    """Top n products by total revenue across the full period."""
    return (
        completed.groupby("product")["total_price"]
        .sum()
        .sort_values(ascending=False)
        .head(n)
    )


# ---------------------------------------------------------------------------
# REPORT BUILDING
# ---------------------------------------------------------------------------
def build_report(combined, file_count):
    """Build the consolidated report and return it as a string."""
    # Parse dates once, up front.
    combined = combined.copy()
    combined["order_date"] = pd.to_datetime(combined["order_date"])
    completed = combined[combined["status"] == "completed"]
    cancelled = combined[combined["status"] == "cancelled"]
    start_date = combined["order_date"].min().strftime("%Y-%m-%d")
    end_date = combined["order_date"].max().strftime("%Y-%m-%d")
    lines = []

    # --- Header ---
    lines.append(LINE)
    lines.append("CONSOLIDATED SALES REPORT")
    lines.append(LINE)
    lines.append("")
    lines.append(f"Period: {start_date} to {end_date} ({file_count} months)")
    lines.append(f"Files processed: {file_count}")
    lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d')}")
    lines.append("")

    # --- Headline metrics ---
    m = headline_metrics(combined, completed, cancelled)
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

    # --- Monthly breakdown ---
    monthly = monthly_breakdown(completed)
    lines.append(THIN)
    lines.append("REVENUE BY MONTH")
    lines.append(THIN)
    lines.append("")
    lines.append("  Month      Orders   Revenue    Change")
    lines.append("  " + "-" * 48)
    for month, row in monthly.iterrows():
        change = row["change"]
        if pd.isna(change):
            change_str = "  \u2014"  # em-dash for the first month
        else:
            sign = "+" if change >= 0 else ""
            change_str = f"  {sign}{change:.1f}%"
        lines.append(
            f"  {str(month):<10} "
            f"  {int(row['orders']):>4} "
            f" ${row['revenue']:>8,.2f} "
            f" {change_str:>6} "
        )
    best_month = monthly["revenue"].idxmax()
    best_revenue = monthly["revenue"].max()
    lines.append("")
    lines.append(f"  Best month: {best_month} (${best_revenue:,.2f})")
    lines.append("")

    # --- Top products ---
    lines.append(THIN)
    lines.append("TOP PRODUCTS \u2014 FULL PERIOD")
    lines.append(THIN)
    lines.append("")
    for i, (product, revenue) in enumerate(top_products(completed).items(), 1):
        lines.append(f"  {i}. {product:<20} ${revenue:>9,.2f}")
    lines.append("")

    # --- Revenue by category ---
    cat_revenue = revenue_by_category(completed)
    total = cat_revenue.sum()
    lines.append(THIN)
    lines.append("REVENUE BY CATEGORY \u2014 FULL PERIOD")
    lines.append(THIN)
    lines.append("")
    for category, revenue in cat_revenue.items():
        share = revenue / total * 100 if total else 0
        lines.append(f"  {category:<20} ${revenue:>9,.2f}  ({share:.1f}%)")
    lines.append("")
    lines.append(LINE)

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------
def main():
    print(LINE)
    print("BATCH SALES PROCESSOR")
    print(LINE)
    print()

    # 1. Discover files.
    print(f"Scanning folder: {INPUT_FOLDER}/")
    csv_files = discover_files(INPUT_FOLDER)
    if not csv_files:
        print(f"  \u2717 No CSV files found in '{INPUT_FOLDER}/'")
        return
    print(f"  Found {len(csv_files)} CSV files")

    # 2. Clean each file.
    cleaned_dfs, failures = process_files(csv_files)
    if not cleaned_dfs:
        print("\n\u2717 No files were processed successfully.")
        return

    # 3. Merge all cleaned data.
    combined = pd.concat(cleaned_dfs, ignore_index=True)
    combined.to_csv(COMBINED_OUTPUT, index=False)
    print(f"\n\u2713 Merged {len(combined)} rows from "
          f"{len(cleaned_dfs)} files")
    print(f"\u2713 Saved combined data: {COMBINED_OUTPUT}")

    # 4. Build the consolidated report.
    print()
    report = build_report(combined, len(cleaned_dfs))
    print(report)

    # 5. Save the report.
    with open(REPORT_OUTPUT, "w") as f:
        f.write(report)
    print(f"\u2713 Combined data: {COMBINED_OUTPUT}")
    print(f"\u2713 Full report: {REPORT_OUTPUT}")
    print(LINE)

    # 6. Note any failures.
    if failures:
        print(f"\n\u26A0 {len(failures)} file(s) failed:")
        for name, error in failures:
            print(f"  - {name}: {error}")


if __name__ == "__main__":
    main()
