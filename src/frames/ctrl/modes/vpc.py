import json
import tkinter as tk
from tkinter import ttk

from src.frames.views.modes import ViewModeVPC
from src.objects.modes import VPC


class FrameModeVPC(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.ui = ViewModeVPC(self)
        self.set_default()

    def set_default(self):
        """
        Sets the default values to the variables and sets the spinbox limits.
        """

        with open("resources/modes.json") as fid:
            vpc = json.load(fid)["vpc"]

        start, from_, to, step = vpc["peep"]
        self.ui.var_peep.set(start)
        self.ui.peep_spin.configure(from_=from_, to=to, increment=step)
        start, from_, to, step = vpc["p support"]
        self.ui.var_p_support.set(start)
        self.ui.p_support_spin.configure(from_=from_, to=to, increment=step)
        start, from_, to, step = vpc["ti"]
        self.ui.var_ti.set(start)
        self.ui.ti_spin.configure(from_=from_, to=to, increment=step)
        start, from_, to, step = vpc["br"]
        self.ui.var_br.set(start)
        self.ui.br_spin.configure(from_=from_, to=to, increment=step)
        start, from_, to, step = vpc["trigger"]
        self.ui.var_trigger.set(start)
        self.ui.trigger_spin.configure(from_=from_, to=to, increment=step)


    def get(self):
        """
        Returns the VAC parameters.
        """

        return VPC(
            peep=self.ui.var_peep.get(),
            p_support=self.ui.var_p_support.get(),
            ti=self.ui.var_ti.get(),
            br=self.ui.var_br.get(),
            trigger=self.ui.var_trigger.get()
        )
