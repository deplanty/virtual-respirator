import tkinter as tk
from tkinter import ttk

import src.constants as cst


class ViewModeCPAP:
    def __init__(self, master:tk.Widget):

        # Variables
        self.var_peep = tk.IntVar(master)

        # Elements
        self.peep_label = ttk.Label(master, text="PEP", width=cst.W_LABEL)
        self.peep_spin = ttk.Spinbox(master, textvariable=self.var_peep, width=cst.W_SPINBOX)
        self.peep_unit = ttk.Label(master, text="cmH2O", width=cst.W_UNIT)

        # Place the elements
        self.peep_label.grid(row=0, column=0)
        self.peep_spin.grid(row=0, column=1)
        self.peep_unit.grid(row=0, column=2, padx=(5, 0))
