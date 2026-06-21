# CSV Sales Toolkit — Days 1, 2 & 3

A 3-day Python project series for building a complete CSV sales data pipeline: clean, analyze, and batch-process sales CSVs using Python, Tkinter, and pandas.

Part of the **CSV Sales Toolkit** series from [Daily Python Projects](https://dailypythonprojects.substack.com/).

---

## Repository Structure

```
csv-sales-toolkit-day1/
├── data/
│   ├── orders_raw.csv          # Messy sample data (Day 1 input)
│   └── orders_clean.csv        # Cleaned sample data (Day 2 & 3 input)
├── csv_cleaner.py              # Day 1 — Visual CSV Cleaner (solution)
├── csv_cleaner_skeleton.py     # Day 1 — Practice skeleton with guided TODOs
├── analyze_sales.py            # Day 2 — Sales Analyzer & Report
├── batch_processor.py          # Day 3 — Batch CSV Processor
├── requirements.txt            # Python dependencies
└── README.md
```

---

## Day 1 — Visual CSV Cleaner

A desktop GUI app that loads a messy sales CSV, cleans it with a button click, and saves the result.

**File:** `csv_cleaner.py`

**What it does:**
- Loads a raw orders CSV and displays it in a scrollable table
- Cleans data on a button click:
  - Strips whitespace from text columns
  - Standardizes category names to Title Case
  - Standardizes order status to lowercase
  - Removes `$` signs and converts prices to floats
  - Converts quantity to whole numbers
  - Fills missing values (quantity → 1, price → category average)
  - Adds a calculated `total_price` column
- Shows a status log of what was cleaned
- Saves the cleaned data to a new CSV

**Run:**
```bash
python csv_cleaner.py
```

**Practice version:** `csv_cleaner_skeleton.py` — guided skeleton with TODO comments for self-study.

---

## Day 2 — Sales Analyzer & Report

A console script that reads the cleaned CSV and generates a full sales performance report.

**File:** `analyze_sales.py`

**What it does:**
- Reads `data/orders_clean.csv`
- Calculates total revenue, order count, and average order value
- Breaks down revenue and quantity by product category
- Identifies top 5 products by revenue
- Flags cancelled orders and calculates cancellation rate
- Prints a formatted summary report to the terminal

**Run:**
```bash
python analyze_sales.py
```

---

## Day 3 — Batch CSV Processor

A batch processing script that automatically cleans and analyzes multiple CSV files in a folder.

**File:** `batch_processor.py`

**What it does:**
- Scans a folder for all `.csv` files
- Applies the same cleaning logic from Day 1 to each file
- Generates a per-file summary report
- Saves each cleaned file with a `_clean` suffix
- Produces a combined summary across all processed files

**Run:**
```bash
python batch_processor.py
```

> By default it processes all CSVs in the `data/` folder. Edit the `INPUT_FOLDER` variable at the top of the file to point to a different directory.

---

## Setup

### 1. Clone the repo
```bash
git clone https://github.com/eboekenh/csv-sales-toolkit-day1.git
cd csv-sales-toolkit-day1
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run any day
```bash
python csv_cleaner.py       # Day 1
python analyze_sales.py     # Day 2
python batch_processor.py   # Day 3
```

---

## Requirements

- Python 3.8+
- pandas
- tkinter (included with standard Python)

See `requirements.txt` for full dependency list.

---

## Series Articles

| Day | Topic | Link |
|-----|-------|------|
| 1 | Visual CSV Cleaner | [Read on Substack](https://dailypythonprojects.substack.com/) |
| 2 | Sales Analyzer & Report | [Read on Substack](https://dailypythonprojects.substack.com/) |
| 3 | Batch CSV Processor | [Read on Substack](https://dailypythonprojects.substack.com/) |

---

## License

MIT — free to use and modify for learning purposes.
