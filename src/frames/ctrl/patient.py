import json
import tkinter as tk
from tkinter import ttk

from src.frames.views import ViewPatient
from src.objects import Patient


class FramePatient(ttk.LabelFrame):
    def __init__(self, master:tk.Widget):
        super().__init__(master)
        self.configure(text="Patient")

        self.ui = ViewPatient(self)
        self.set_default()


    def set_default(self):
        """
        Sets the default values and limits for the variables.
        """

        with open("resources/patient.json") as fid:
            patient = json.load(fid)

        start, from_, to, step = patient["r"]
        self.ui.var_r.set(start)
        self.ui.r_spin.configure(from_=from_, to=to, increment=step)
        start, from_, to, step = patient["c"]
        self.ui.var_c.set(start)
        self.ui.c_spin.configure(from_=from_, to=to, increment=step)
        start, from_, to, step = patient["br"]
        self.ui.var_br.set(start)
        self.ui.br_spin.configure(from_=from_, to=to, increment=step)
        start, from_, to, step = patient["ti"]
        self.ui.var_ti.set(start)
        self.ui.ti_spin.configure(from_=from_, to=to, increment=step)
        start, from_, to, step = patient["pmus"]
        self.ui.var_pmus.set(start)
        self.ui.pmus_spin.configure(from_=from_, to=to, increment=step)


    def get(self):
        """
        Returns a patient object with the parameters.
        """

        return Patient(
            r=self.ui.var_r.get(),
            c=self.ui.var_c.get(),
            br=self.ui.var_br.get(),
            ti=self.ui.var_ti.get(),
            pmus=self.ui.var_pmus.get()
        )
