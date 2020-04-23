import tkinter as tk
from tkinter import ttk

import src.constants as cst
from src.objects import Patient


class ViewPatient:
    def __init__(self, master):

        # Variables
        self.var_r = tk.IntVar(master)
        self.var_c = tk.IntVar(master)
        self.var_br = tk.IntVar(master)
        self.var_ti = tk.DoubleVar(master)
        self.var_pmus = tk.IntVar(master)

        # Elements
        self.r_label = ttk.Label(master, text="Résistance", width=cst.W_LABEL)
        self.r_spin = ttk.Spinbox(master, textvariable=self.var_r, width=cst.W_SPINBOX)
        self.r_unit = ttk.Label(master, text="cmH2O/(l/min)", width=cst.W_UNIT)
        self.c_label = ttk.Label(master, text="Compliance", width=cst.W_LABEL)
        self.c_spin = ttk.Spinbox(master, textvariable=self.var_c, width=cst.W_SPINBOX)
        self.c_unit = ttk.Label(master, text="ml/cmH2O", width=cst.W_UNIT)
        self.br_label = ttk.Label(master, text="Fréquence Respi", width=cst.W_LABEL)
        self.br_spin = ttk.Spinbox(master, textvariable=self.var_br, width=cst.W_SPINBOX)
        self.br_unit = ttk.Label(master, text="/min", width=cst.W_UNIT)
        self.ti_label = ttk.Label(master, text="Temps inspiratoire", width=cst.W_LABEL)
        self.ti_spin = ttk.Spinbox(master, textvariable=self.var_ti, width=cst.W_SPINBOX)
        self.ti_unit = ttk.Label(master, text="s", width=cst.W_UNIT)
        self.pmus_label = ttk.Label(master, text="Pmus", width=cst.W_LABEL)
        self.pmus_spin = ttk.Spinbox(master, textvariable=self.var_pmus, width=cst.W_SPINBOX)
        self.pmus_unit = ttk.Label(master, text="cmH2O", width=cst.W_UNIT)

        # Place the elements
        self.r_label.grid(row=0, column=0)
        self.r_spin.grid(row=0, column=1)
        self.r_unit.grid(row=0, column=2, padx=(5, 0))
        self.c_label.grid(row=1, column=0)
        self.c_spin.grid(row=1, column=1)
        self.c_unit.grid(row=1, column=2, padx=(5, 0))
        self.br_label.grid(row=2, column=0)
        self.br_spin.grid(row=2, column=1)
        self.br_unit.grid(row=2, column=2, padx=(5, 0))
        self.ti_label.grid(row=3, column=0)
        self.ti_spin.grid(row=3, column=1)
        self.ti_unit.grid(row=3, column=2, padx=(5, 0))
        self.pmus_label.grid(row=4, column=0)
        self.pmus_spin.grid(row=4, column=1)
        self.pmus_unit.grid(row=4, column=2, padx=(5, 0))
