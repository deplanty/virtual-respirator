import tkinter as tk
from tkinter import ttk

import src.constants as cst


class ViewSimulation:
    def __init__(self, master):

        # Variables
        self.var_time = tk.DoubleVar(master)

        # Elements
        self.time_label = ttk.Label(master, text="Durée", width=cst.W_LABEL)
        self.time_spin = ttk.Spinbox(master, textvariable=self.var_time, width=cst.W_SPINBOX)
        self.time_unit = ttk.Label(master, text="s", width=cst.W_UNIT)

        # Place the elements
        self.time_label.grid(row=0, column=0)
        self.time_spin.grid(row=0, column=1)
        self.time_unit.grid(row=0, column=2)
