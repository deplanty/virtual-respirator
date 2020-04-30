import tkinter as tk
from tkinter import ttk

from src.frames.views import ViewSimulation
from src.objects import Simulation


class FrameSimuation(ttk.LabelFrame):
    def __init__(self, master:tk.Widget):
        super().__init__(master)
        self.configure(text="Simulation")

        self.ui = ViewSimulation(self)

        self.set_default()


    def set_default(self):
        """
        Sets the default values and limits for the variables.
        """

        self.ui.var_time.set(10)
        self.ui.time_spin.configure(from_=1, to=120, increment=1)
        self.ui.var_step.set(0.02)
        self.ui.step_spin.configure(from_=0.01, to=1, increment=0.01)


    def get(self):
        """
        Returns the duration of the simulation.
        """

        return Simulation(
            t_max=self.ui.var_time.get(),
            t_step=self.ui.var_step.get()
        )
