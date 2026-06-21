#!/usr/bin/env python3
"""
CSV Sales Toolkit - Day 1: Visual CSV Cleaner
A Tkinter desktop app to load a messy orders CSV, clean it visually,
and save the tidy result.
"""

import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext
import pandas as pd

TEXT_COLUMNS = ["customer_name", "product", "category", "status"]


class CSVCleanerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Visual CSV Cleaner")
        self.root.geometry("950x600")
        self.df = None
        self.setup_styles()
        self.build_ui()

    # -------------------------------------------------
    # STYLE FIX (Mac compatible)
    # -------------------------------------------------
    def setup_styles(self):
        self.style = ttk.Style()
        # Important for macOS so custom colors work
        self.style.theme_use("clam")
        self.style.configure("Blue.TButton", background="#2196F3", foreground="white")
        self.style.map("Blue.TButton", background=[("active", "#1976D2")])
        self.style.configure("Green.TButton", background="#4CAF50", foreground="white")
        self.style.map("Green.TButton", background=[("active", "#388E3C")])
        self.style.configure("Orange.TButton", background="#FF9800", foreground="white")
        self.style.map("Orange.TButton", background=[("active", "#F57C00")])

    # -------------------------------------------------
    # UI
    # -------------------------------------------------
    def build_ui(self):
        title = tk.Label(
            self.root,
            text="\U0001f9f9 VISUAL CSV CLEANER",
            font=("Arial", 16, "bold"),
        )
        title.pack(pady=10)

        button_bar = tk.Frame(self.root)
        button_bar.pack(fill=tk.X, padx=10)

        ttk.Button(
            button_bar,
            text="\U0001f4c2 Load CSV",
            style="Blue.TButton",
            command=self.load_csv,
        ).pack(side=tk.LEFT, padx=5)

        ttk.Button(
            button_bar,
            text="\u2728 Clean Data",
            style="Green.TButton",
            command=self.clean_data,
        ).pack(side=tk.LEFT, padx=5)

        ttk.Button(
            button_bar,
            text="\U0001f4be Save Clean CSV",
            style="Orange.TButton",
            command=self.save_csv,
        ).pack(side=tk.LEFT, padx=5)

        table_frame = tk.Frame(self.root)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.tree = ttk.Treeview(table_frame, show="headings")
        y_scroll = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        x_scroll = ttk.Scrollbar(table_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=y_scroll.set, xscrollcommand=x_scroll.set)
        y_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        x_scroll.pack(side=tk.BOTTOM, fill=tk.X)
        self.tree.pack(fill=tk.BOTH, expand=True)

        tk.Label(self.root, text="STATUS LOG:", font=("Arial", 10, "bold")).pack(
            anchor=tk.W, padx=10
        )
        self.status_log = scrolledtext.ScrolledText(
            self.root, height=6, font=("Courier", 9)
        )
        self.status_log.pack(fill=tk.X, padx=10, pady=(0, 10))
        self.log("Ready. Click 'Load CSV' to begin.")

    # -------------------------------------------------
    # LOGGING
    # -------------------------------------------------
    def log(self, message):
        self.status_log.insert(tk.END, message + "\n")
        self.status_log.see(tk.END)

    # -------------------------------------------------
    # TABLE
    # -------------------------------------------------
    def show_dataframe(self, df):
        self.tree.delete(*self.tree.get_children())
        self.tree["columns"] = list(df.columns)
        for col in df.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=110, anchor=tk.W)
        for _, row in df.iterrows():
            self.tree.insert("", "end", values=list(row))

    # -------------------------------------------------
    # LOAD
    # -------------------------------------------------
    def load_csv(self):
        path = filedialog.askopenfilename(
            title="Select a CSV file",
            filetypes=[("CSV files", "*.csv")],
        )
        if not path:
            return
        try:
            self.df = pd.read_csv(path)
        except Exception as e:
            self.log(f"\u2717 Could not load file: {e}")
            return
        self.show_dataframe(self.df)
        filename = path.split("/")[-1]
        self.log(f"\u2713 Loaded {filename} \u2014 {len(self.df)} rows")

    # -------------------------------------------------
    # CLEAN
    # -------------------------------------------------
    def clean_data(self):
        if self.df is None:
            self.log("\u2717 Load a CSV first!")
            return
        df = self.df

        for col in TEXT_COLUMNS:
            df[col] = df[col].astype(str).str.strip()

        df["category"] = df["category"].str.title()
        df["status"] = df["status"].str.lower()

        df["unit_price"] = (
            df["unit_price"]
            .astype(str)
            .str.replace("$", "", regex=False)
            .str.replace(",", "", regex=False)
        )
        df["unit_price"] = pd.to_numeric(df["unit_price"], errors="coerce")

        df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
        df["quantity"] = df["quantity"].fillna(1).astype(int)

        category_avg = df.groupby("category")["unit_price"].transform("mean")
        df["unit_price"] = df["unit_price"].fillna(category_avg).round(2)

        df["total_price"] = (df["quantity"] * df["unit_price"]).round(2)

        self.df = df
        self.show_dataframe(self.df)
        self.log("\u2713 Cleaned data successfully")

    # -------------------------------------------------
    # SAVE
    # -------------------------------------------------
    def save_csv(self):
        if self.df is None:
            self.log("\u2717 Nothing to save")
            return
        path = filedialog.asksaveasfilename(
            title="Save cleaned CSV",
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")],
        )
        if not path:
            return
        self.df.to_csv(path, index=False)
        filename = path.split("/")[-1]
        self.log(f"\u2713 Saved {filename}")


def main():
    root = tk.Tk()
    app = CSVCleanerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
