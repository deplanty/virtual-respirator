import tkinter as tk
from tkinter import ttk

import src.constants as cst


class ViewModeVSAI:
    def __init__(self, master:tk.Widget):

        # Variables
        self.var_peep = tk.IntVar(master)
        self.var_ai = tk.IntVar(master)
        self.var_ti = tk.DoubleVar(master)
        self.var_trigger = tk.DoubleVar(master)

        # Elements
        self.peep_label = ttk.Label(master, text="PEP", width=cst.W_LABEL)
        self.peep_spin = ttk.Spinbox(master, textvariable=self.var_peep, width=cst.W_SPINBOX)
        self.peep_unit = ttk.Label(master, text="cmH2O", width=cst.W_UNIT)
        self.ai_label = ttk.Label(master, text="AI", width=cst.W_LABEL)
        self.ai_spin = ttk.Spinbox(master, textvariable=self.var_ai, width=cst.W_SPINBOX)
        self.ai_unit = ttk.Label(master, text="cmH2O", width=cst.W_UNIT)
        self.ti_label = ttk.Label(master, text="Temps  inspi", width=cst.W_LABEL)
        self.ti_spin = ttk.Spinbox(master, textvariable=self.var_ti, width=cst.W_SPINBOX)
        self.ti_unit = ttk.Label(master, text="s", width=cst.W_UNIT)
        self.trigger_label = ttk.Label(master, text="Trigger", width=cst.W_LABEL)
        self.trigger_spin = ttk.Spinbox(master, textvariable=self.var_trigger, width=cst.W_SPINBOX)
        self.trigger_unit = ttk.Label(master, text="l/min", width=cst.W_UNIT)

        # Place the elements
        self.peep_label.grid(row=0, column=0)
        self.peep_spin.grid(row=0, column=1)
        self.peep_unit.grid(row=0, column=2, padx=(5, 0))
        self.ai_label.grid(row=1, column=0)
        self.ai_spin.grid(row=1, column=1)
        self.ai_unit.grid(row=1, column=2, padx=(5, 0))
        self.ti_label.grid(row=2, column=0)
        self.ti_spin.grid(row=2, column=1)
        self.ti_unit.grid(row=2, column=2, padx=(5, 0))
        self.trigger_label.grid(row=3, column=0)
        self.trigger_spin.grid(row=3, column=1)
        self.trigger_unit.grid(row=3, column=2, padx=(5, 0))
