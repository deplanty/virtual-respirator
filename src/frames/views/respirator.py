import tkinter as tk
from tkinter import ttk

import src.constants as cst


class ViewRespirator:
    def __init__(self, master):

        # Variable
        self.var_mode = tk.StringVar(master)

        # Elements
        self.mode_label = ttk.Label(master, text="Mode Ventilatoire")
        self.mode_combo = ttk.Combobox(master, textvariable=self.var_mode, width=cst.W_COMBOBOX)
        self.mode_f_params = ttk.Frame(master)

        # Place the elements
        self.mode_label.pack()
        self.mode_combo.pack(pady=(2, 6))
        self.mode_f_params.pack(fill="x")
