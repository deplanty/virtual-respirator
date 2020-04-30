import json
import tkinter as tk
from tkinter import ttk

from src.frames.views.modes import ViewModeCPAP
from src.objects.modes import CPAP

from .mode import FrameMode


class FrameModeCPAP(FrameMode, ttk.Frame):
    def __init__(self, master:tk.Widget):
        super().__init__(master)

        self.ui = ViewModeCPAP(self)
        self.set_default()


    def set_default(self):
        """
        Sets the default values to the variables and sets the spinbox limits.
        """

        with open("resources/modes.json") as fid:
            vsai = json.load(fid)["cpap"]

        start, from_, to, step = vsai["peep"]
        self.ui.var_peep.set(start)
        self.ui.peep_spin.configure(from_=from_, to=to, increment=step)


    def get(self):
        """
        Returns the VSAI parameters.
        """

        return CPAP(
            peep=self.ui.var_peep.get()
        )

    def set(self, **kwargs):
        """
        Sets the CPAP parameters.
        """

        self.ui.var_peep.set(kwargs["peep"])
