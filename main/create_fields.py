import tkinter as tk


def add_field(parent, label_text, row, column, width=20):
    label = tk.Label(parent, text=label_text)
    label.grid(row=row, column=column, sticky="w", padx=8, pady=4)

    entry = tk.Entry(parent, width=width, border=3)
    entry.grid(row=row, column=column + 1, sticky="w")
    return label, entry
