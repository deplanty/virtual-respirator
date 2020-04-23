import json
import tkinter as tk
from tkinter import ttk

from src.frames.views.modes import ViewModeVSAI
from src.objects.modes import VSAI


class FrameModeVSAI(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.ui = ViewModeVSAI(self)
        self.set_default()


    def set_default(self):
        """
        Sets the default values to the variables and sets the spinbox limits.
        """

        with open("resources/modes.json") as fid:
            vsai = json.load(fid)["vsai"]

        start, from_, to, step = vsai["peep"]
        self.ui.var_peep.set(start)
        self.ui.peep_spin.configure(from_=from_, to=to, increment=step)
        start, from_, to, step = vsai["ai"]
        self.ui.var_ai.set(start)
        self.ui.ai_spin.configure(from_=from_, to=to, increment=step)
        start, from_, to, step = vsai["ti"]
        self.ui.var_ti.set(start)
        self.ui.ti_spin.configure(from_=from_, to=to, increment=step)
        start, from_, to, step = vsai["trigger"]
        self.ui.var_trigger.set(start)
        self.ui.trigger_spin.configure(from_=from_, to=to, increment=step)


    def get(self):
        """
        Returns the VAC parameters.
        """

        return VSAI(
            peep=self.ui.var_peep.get(),
            ai=self.ui.var_ai.get(),
            ti=self.ui.var_ti.get(),
            trigger=self.ui.var_trigger.get()
        )
