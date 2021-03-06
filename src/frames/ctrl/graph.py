import tkinter as tk
from tkinter import ttk

import numpy as np

from src.frames.views import ViewGraph


class FrameGraph(ttk.Frame):
    def __init__(self, master:tk.Widget):
        super().__init__(master)

        self.ui = ViewGraph(self)
        self.array = [list() for _ in range(5)]

        self.setup_graph()


    def setup_graph(self):
        """
        Initializes the graph in the window.
        """

        def math(label):
            label = label.replace(" ", "\\;")
            return "$\\mathrm{%s}$" % label

        self.axes = self.ui.fig.subplots(4, 1, sharex=True)
        self.ui.fig.tight_layout()
        self.ui.fig.subplots_adjust(hspace=0.15)

        self.axes[0].set_ylabel(math("P_{aw} (cm H_{2}O)"))
        self.axes[1].set_ylabel(math("Débit (l/min)"))
        self.axes[2].set_ylabel(math("Volume (ml)"))
        self.axes[3].set_ylabel(math("P_{mus} (cm H_{2}O)"))
        self.axes[3].set_xlabel(math("Temps (s)"))

        for ax in self.axes:
            ax.grid(True, linestyle="dashed")
            ax.relim()
            ax.autoscale_view()


    def set_default(self):
        """
        Resets the graphs to their default states.
        """

        # Remove stored data
        self.init()

        # Clear curves
        for ax in self.axes:
            for line in ax.lines:
                line.remove()
            ax.relim()
            ax.autoscale_view()
        self.ui.canvas.draw()


    def init(self, values=None):
        """
        Initializes the graph to get values from the simulation.

        Args:
            values (list): initalization values
        """

        for curve in self.array:
            curve.clear()

        if values:
            self.add(values)


    def add(self, values:list):
        """
        Add values a the current time.

        Args:
            values (list): time, paw, flow, volume and pmus
        """

        for i, v in enumerate(values):
            self.array[i].append(v)


    def show(self):
        """
        Draws the curves from all added values.
        """

        time = self.array[0]

        # Clear curves
        for ax in self.axes:
            for line in ax.lines:
                line.remove()

        colors = ["magenta", "blue", "gray", "orange"]
        for ax, curve, color in zip(self.axes, self.array[1:], colors):
            ax.plot(time, curve, color)

        for ax in self.axes:
            ax.relim()
            ax.autoscale_view()
        self.ui.fig.align_ylabels(self.axes)

        self.ui.canvas.draw()
