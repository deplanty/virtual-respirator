import json
import tkinter as tk
from tkinter import ttk

from src.frames.views.modes import ViewModeVAC
from src.objects.modes import VAC

from .mode import FrameMode


class FrameModeVAC(FrameMode, ttk.Frame):
    def __init__(self, master:tk.Widget):
        super().__init__(master)

        self.ui = ViewModeVAC(self)
        self.set_default()


    def set_default(self):
        """
        Sets the default values to the variables and sets the spinbox limits.
        """

        with open("resources/modes.json") as fid:
            vac = json.load(fid)["vac"]

        start, from_, to, step = vac["peep"]
        self.ui.var_peep.set(start)
        self.ui.peep_spin.configure(from_=from_, to=to, increment=step)
        start, from_, to, step = vac["vt"]
        self.ui.var_vt.set(start)
        self.ui.vt_spin.configure(from_=from_, to=to, increment=step)
        start, from_, to, step = vac["flow"]
        self.ui.var_flow.set(start)
        self.ui.flow_spin.configure(from_=from_, to=to, increment=step)
        start, from_, to, step = vac["br"]
        self.ui.var_br.set(start)
        self.ui.br_spin.configure(from_=from_, to=to, increment=step)
        start, from_, to, step = vac["pause inspi"]
        self.ui.var_pause_inspi.set(start)
        self.ui.pause_inspi_spin.configure(from_=from_, to=to, increment=step)
        start, from_, to, step = vac["trigger"]
        self.ui.var_trigger.set(start)
        self.ui.trigger_spin.configure(from_=from_, to=to, increment=step)


    def get(self):
        """
        Returns the VAC parameters.
        """

        return VAC(
            peep=self.ui.var_peep.get(),
            vt=self.ui.var_vt.get(),
            flow=self.ui.var_flow.get(),
            br=self.ui.var_br.get(),
            pause_inspi=self.ui.var_pause_inspi.get(),
            trigger=self.ui.var_trigger.get()
        )


    def set(self, **kwargs):
        """
        Sets the VAC parameters.
        """

        self.ui.var_peep.set(kwargs["peep"])
        self.ui.var_vt.set(kwargs["vt"])
        self.ui.var_flow.set(kwargs["flow"])
        self.ui.var_br.set(kwargs["br"])
        self.ui.var_pause_inspi.set(kwargs["pause_inspi"])
        self.ui.var_trigger.set(kwargs["trigger"])
