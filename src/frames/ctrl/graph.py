import tkinter as tk
from tkinter import ttk

from src.frames.views import ViewGraph


class FrameGraph(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.ui = ViewGraph(self)

        self.setup_graph()


    def setup_graph(self):

        self.axes = self.ui.fig.subplots(4, 1, sharex=True)
        self.ui.fig.tight_layout()

        self.axes[0].set_title("Courbes théoriques")
        self.axes[0].set_ylabel("Paw (cmH2O)")
        self.axes[1].set_ylabel("Débit (l/min)")
        self.axes[2].set_ylabel("Volume (ml)")
        self.axes[3].set_ylabel("Pmus (cmH2O)")
        self.axes[3].set_xlabel("Time (s)")

        for ax in self.axes:
            ax.grid(True, linestyle="dashed")

    def draw_one_time(self, values):
        """
        Draws an element in the graphs

        Args:
            list: time, paw, flow, volume, pmus
        """

        time = values.pop(0)
        # for ax, val in zip(self.axes, values):
        #     ax.add_line([time, val])

    def draw_from_file(self, file):
        """
        Draws a graph from a text file

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
