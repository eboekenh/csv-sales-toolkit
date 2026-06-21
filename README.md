# CSV Sales Toolkit — Day 1: Visual CSV Cleaner

A visual desktop app for cleaning messy CSV sales data, built with Python, Tkinter, and pandas.

Part of the **CSV Sales Toolkit** series (Days 1–3) from [Daily Python Projects](https://dailypythonprojects.substack.com/).

---

## What It Does

- Loads a raw orders CSV and displays it in a scrollable table
- Cleans data on a button click:
  - Strips whitespace from text columns
  - Standardizes category names to Title Case
  - Standardizes order status to lowercase
  - Removes `$` signs and converts prices to numbers
  - Converts quantity to whole numbers
  - Fills missing values sensibly (quantity → 1, price → category average)
  - Adds a calculated `total_price` column
- Shows a status log of what was cleaned
- Saves the cleaned data to a new CSV

---

## Project Structure

```
csv-sales-toolkit-day1/
├── csv_cleaner.py          # Full solution
├── csv_cleaner_skeleton.py # Skeleton with comment guides for practice
├── orders_raw.csv          # Sample messy data (download separately)
├── README.md
└── .gitignore
```

---

## Setup

### Requirements

- Python 3.x (Tkinter ships with Python)
- pandas

```bash
pip install pandas
```

### Run

```bash
python csv_cleaner.py
```

Then click **Load CSV**, select `orders_raw.csv`, click **Clean Data**, and finally **Save Clean CSV**.

> Download the sample `orders_raw.csv` file [here](https://drive.google.com/file/d/1REpTTz5lzXhXh5fW6vtT3yms3X9jBKRp/view?usp=sharing).

---

## Key Concepts Covered

| Concept | Detail |
|---|---|
| Class-based Tkinter app | `self.df` shared across all methods |
| `ttk.Treeview` | Table widget for displaying DataFrames |
| `filedialog` | Open/save file picker dialogs |
| `.str.strip()` / `.str.title()` / `.str.lower()` | Column-wide string operations |
| `pd.to_numeric(..., errors='coerce')` | Text to numbers, bad values → NaN |
| `groupby().transform('mean')` | Fill missing prices with category average |
| `to_csv(index=False)` | Save without junk index column |

---

## Data Problems Solved

| Problem | Example | Fix |
|---|---|---|
| Whitespace | `" Alice Johnson"` | `.str.strip()` |
| Inconsistent categories | `electronics`, `ELECTRONICS` | `.str.title()` |
| Inconsistent status | `COMPLETED`, `Completed` | `.str.lower()` |
| Currency symbols | `$12.99` | `.str.replace('$', '')` |
| Missing quantity | empty cell | fill with `1` |
| Missing price | empty cell | fill with category average |

---

## Series

- **Day 1:** Visual CSV Cleaner ← you are here
- **Day 2:** Sales Analyzer & Report
- **Day 3:** Batch CSV Processor

---

*Source: [Daily Python Projects — Build a CSV Sales Toolkit](https://dailypythonprojects.substack.com/p/build-a-csv-sales-toolkit-day-1-csv)*
