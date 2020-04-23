import tkinter as tk
from tkinter import ttk

import src.constants as cst


class ViewModeVAC:
    def __init__(self, master:tk.Widget):

        # Variables
        self.var_peep = tk.IntVar(master)
        self.var_vt = tk.IntVar(master)
        self.var_flow = tk.IntVar(master)
        self.var_br = tk.IntVar(master)
        self.var_pause_inspi = tk.DoubleVar(master)
        self.var_trigger = tk.DoubleVar(master)

        # Elements
        self.peep_label = ttk.Label(master, text="PEP", width=cst.W_LABEL)
        self.peep_spin = ttk.Spinbox(master, textvariable=self.var_peep, width=cst.W_SPINBOX)
        self.peep_unit = ttk.Label(master, text="cmH2O", width=cst.W_UNIT)
        self.vt_label = ttk.Label(master, text="Vt", width=cst.W_LABEL)
        self.vt_spin = ttk.Spinbox(master, textvariable=self.var_vt, width=cst.W_SPINBOX)
        self.vt_unit = ttk.Label(master, text="ml", width=cst.W_UNIT)
        self.flow_label = ttk.Label(master, text="Débit", width=cst.W_LABEL)
        self.flow_spin = ttk.Spinbox(master, textvariable=self.var_flow, width=cst.W_SPINBOX)
        self.flow_unit = ttk.Label(master, text="l/min", width=cst.W_UNIT)
        self.br_label = ttk.Label(master, text="Fréquence respi", width=cst.W_LABEL)
        self.br_spin = ttk.Spinbox(master, textvariable=self.var_br, width=cst.W_SPINBOX)
        self.br_unit = ttk.Label(master, text="/min", width=cst.W_UNIT)
        self.pause_inspi_label = ttk.Label(master, text="Pause inspi", width=cst.W_LABEL)
        self.pause_inspi_spin = ttk.Spinbox(master, textvariable=self.var_pause_inspi, width=cst.W_SPINBOX)
        self.pause_inspi_unit = ttk.Label(master, text="s", width=cst.W_UNIT)
        self.trigger_label = ttk.Label(master, text="Trigger", width=cst.W_LABEL)
        self.trigger_spin = ttk.Spinbox(master, textvariable=self.var_trigger, width=cst.W_SPINBOX)
        self.trigger_unit = ttk.Label(master, text="l/min", width=cst.W_UNIT)

        # Place the elements
        self.peep_label.grid(row=0, column=0)
        self.peep_spin.grid(row=0, column=1)
        self.peep_unit.grid(row=0, column=2, padx=(5, 0))
        self.vt_label.grid(row=1, column=0)
        self.vt_spin.grid(row=1, column=1)
        self.vt_unit.grid(row=1, column=2, padx=(5, 0))
        self.flow_label.grid(row=2, column=0)
        self.flow_spin.grid(row=2, column=1)
        self.flow_unit.grid(row=2, column=2, padx=(5, 0))
        self.br_label.grid(row=3, column=0)
        self.br_spin.grid(row=3, column=1)
        self.br_unit.grid(row=3, column=2, padx=(5, 0))
        self.pause_inspi_label.grid(row=4, column=0)
        self.pause_inspi_spin.grid(row=4, column=1)
        self.pause_inspi_unit.grid(row=4, column=2, padx=(5, 0))
        self.trigger_label.grid(row=5, column=0)
        self.trigger_spin.grid(row=5, column=1)
        self.trigger_unit.grid(row=5, column=2, padx=(5, 0))
