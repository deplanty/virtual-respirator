import tkinter as tk
from tkinter import ttk

from src.frames.views import ViewSimulation


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


    def get(self):
        """
        Returns the duration of the simulation.
        """

        return self.ui.var_time.get()
