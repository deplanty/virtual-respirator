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

        self.axes = self.ui.fig.subplots(4, 1, sharex=True)
        self.ui.fig.tight_layout()

        self.line_paw, *_ = self.axes[0].plot([], [])

        self.axes[0].set_title("Courbes théoriques")
        self.axes[0].set_ylabel("Paw (cmH2O)")
        self.axes[1].set_ylabel("Débit (l/min)")
        self.axes[2].set_ylabel("Volume (ml)")
        self.axes[3].set_ylabel("Pmus (cmH2O)")
        self.axes[3].set_xlabel("Time (s)")

        for ax in self.axes:
            ax.grid(True, linestyle="dashed")


    def init(self, values=None):
        """
        Initializes the graph to get values from the simulation.

        Args:
            values (list): initalization values
        """

        for curve in self.array:
            curve.clear()

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
            ax.grid(True, linestyle="dashed")

        for ax in self.axes:
            ax.relim()
            ax.autoscale_view()

        self.ui.canvas.draw()


    def draw_one_time(self, values:list):
        """
        Draws an element in the graphs.

        Args:
            values (list): time, paw, flow, volume and pmus
        """

        time = values.pop(0)
        # for ax, val in zip(self.axes, values):
        #     ax.add_line([time, val])

        self.line_paw.set_xdata(np.append(self.line_paw.get_xdata(), time))
        self.line_paw.set_ydata(np.append(self.line_paw.get_ydata(), values[0]))

        # self.ui.canvas.draw()
        self.axes[0].relim()
        self.axes[0].autoscale_view()
        print(time)


    def draw_from_file(self, file:str):
        """
        Draws a graph from a text file.

        Args:
            file (str): text file with data
        """

        with open(file) as fid:
            header = fid.readline().rstrip().split("\t")
            array = [list() for _ in header]
            for line in fid:
                line = line.rstrip().split("\t")
                for i, element in enumerate(line):
                    array[i].append(float(element))

        time = array.pop(0)
        time_label = header.pop(0)

        # Clear curves
        for ax in self.axes:
            for line in ax.lines:
                line.remove()

        colors = ["magenta", "blue", "gray", "orange"]
        for ax, curve, label, color in zip(self.axes, array, header, colors):
            ax.plot(time, curve, color)
            ax.grid(True, linestyle="dashed")

        for ax in self.axes:
            ax.relim()
            ax.autoscale_view()

        self.ui.canvas.draw()
