#!/usr/bin/env python3
"""
THE APP:
A visual desktop app for cleaning messy CSV data. Load a raw orders file,
see it in a table, click a button to clean it (fix whitespace, capitalization,
currency symbols, missing values), watch the table update, and save the result.

WHAT TO FIGURE OUT:
- How do you structure a Tkinter app as a class with shared data?
- How do you show a pandas DataFrame in a Treeview table?
- How do you load a file with a file-picker dialog?
- How do you clean data with pandas (whitespace, casing, types, missing values)?
- How do you re-render the table after the data changes?
- How do you save the result with a save dialog?

START HERE:
First, build the class skeleton with self.df = None.
Then build the UI: a button bar, a Treeview table, a status log.
Next, write show_dataframe() - it renders ANY DataFrame into the table.
Then write load_csv(), clean_data(), and save_csv().
The cleaning logic is pure pandas - one step per problem.

KEY CONCEPTS:
- Class-based GUI: self.df holds the data so all methods share it
- ttk.Treeview: the table widget; show="headings" hides the empty first column
- tree.insert("", "end", values=(...)): adds one row
- filedialog.askopenfilename / asksaveasfilename: file picker dialogs
- pd.to_numeric(..., errors="coerce"): text -> numbers, bad values -> NaN
- .str.strip() / .str.title() / .str.lower(): column-wide string ops
- groupby(...).transform("mean"): per-group average, aligned to every row
- to_csv(index=False): save WITHOUT the junk index column
"""

# ---------------------------------------------------------------------------
# THE CODE SKELETON
# Imports: tkinter as tk; ttk, filedialog, scrolledtext from tkinter; pandas as pd
# TEXT_COLUMNS: list of columns that need whitespace stripped
# ---------------------------------------------------------------------------

# THE APP CLASS
# class CSVCleanerApp:
#   __init__(self, root)
#     - store root, set title and geometry
#     - self.df = None (no data loaded yet)
#     - call self.build_ui()
#
#   build_ui(self)
#     - A title label
#     - A button bar (Frame) with 3 buttons:
#         "Load CSV"        -> command=self.load_csv
#         "Clean Data"      -> command=self.clean_data
#         "Save Clean CSV"  -> command=self.save_csv
#     - A ttk.Treeview table (show="headings") inside a frame,
#       ideally with vertical + horizontal scrollbars
#     - A scrolledtext.ScrolledText box for the status log
#
#   log(self, message)
#     - insert message + newline into the status log
#     - .see(tk.END) so it scrolls to the newest line
#
#   show_dataframe(self, df)
#     - Clear the table: self.tree.delete(*self.tree.get_children())
#     - Set self.tree["columns"] to the DataFrame's columns
#     - For each column: set its heading text and width
#     - For each row (df.iterrows()): tree.insert("", "end", values=list(row))
#
#   load_csv(self)
#     - filedialog.askopenfilename(...) -> path
#     - if no path (cancelled): return
#     - self.df = pd.read_csv(path)
#     - call show_dataframe(self.df) and log what loaded
#     - optionally: inspect and log the problems found
#
#   clean_data(self)
#     - if self.df is None: log a warning and return
#     - Strip whitespace: for each col in TEXT_COLUMNS,
#         df[col] = df[col].astype(str).str.strip()
#     - Standardize: df["category"].str.title(), df["status"].str.lower()
#     - Fix prices: remove "$" and ",", then pd.to_numeric(errors="coerce")
#     - Fix quantity: pd.to_numeric(errors="coerce"), fillna(1), astype(int)
#     - Fill missing prices with category average
#         (groupby("category")["unit_price"].transform("mean"))
#     - Add df["total_price"] = quantity * unit_price
#     - Save back to self.df, call show_dataframe, and log each step
#
#   save_csv(self)
#     - if self.df is None: log a warning and return
#     - filedialog.asksaveasfilename(defaultextension=".csv", ...) -> path
#     - if no path: return
#     - self.df.to_csv(path, index=False)
#     - log that the file was saved
# ---------------------------------------------------------------------------

# MAIN
# main()
#   - create the Tk root
#   - create CSVCleanerApp(root)
#   - root.mainloop()
# Run main() if executed directly

# --- YOUR CODE BELOW ---
