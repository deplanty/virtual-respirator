import json
import tkinter as tk
from tkinter import ttk

from src.frames.views.modes import ViewModeVSAI
from src.objects.modes import VSAI

from .mode import FrameMode


class FrameModeVSAI(FrameMode, ttk.Frame):
    def __init__(self, master:tk.Widget):
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
        start, from_, to, step = vsai["trigger inspi"]
        self.ui.var_trigger_inspi.set(start)
        self.ui.trigger_inspi_spin.configure(from_=from_, to=to, increment=step)
        start, from_, to, step = vsai["trigger expi"]
        self.ui.var_trigger_expi.set(start)
        self.ui.trigger_expi_spin.configure(from_=from_, to=to, increment=step)
        start, from_, to, step = vsai["ti max"]
        self.ui.var_ti_max.set(start)
        self.ui.ti_max_spin.configure(from_=from_, to=to, increment=step)


    def get(self):
        """
        Returns the VSAI parameters.
        """

        return VSAI(
            peep=self.ui.var_peep.get(),
            ai=self.ui.var_ai.get(),
            trigger_inspi=self.ui.var_trigger_inspi.get(),
            trigger_expi=self.ui.var_trigger_expi.get(),
            ti_max=self.ui.var_ti_max.get(),
        )


    def get_dict(self):
        """
        Returns the mode parameters as a dict.

        Returns:
            dict: VAC parameters
        """

        return {
            "peep": self.ui.var_peep.get(),
            "ai": self.ui.var_ai.get(),
            "trigger_inspi": self.ui.var_trigger_inspi.get(),
            "trigger_expi": self.ui.var_trigger_expi.get(),
            "ti_max": self.ui.var_ti_max.get()
        }


    def set(self, **kwargs):
        """
        Sets the VPC parameters.
        """

        self.ui.var_peep.set(kwargs["peep"])
        self.ui.var_ai.set(kwargs["ai"])
        self.ui.var_trigger_inspi.set(kwargs["trigger_inspi"])
        self.ui.var_trigger_expi.set(kwargs["trigger_expi"])
        self.ui.var_ti_max.set(kwargs["ti_max"])
