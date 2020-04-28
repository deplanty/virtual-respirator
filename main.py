import json
import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk

from src.frames.ctrl import FrameGraph, FramePatient, FrameRespirator, FrameSimuation
from src.objects import Respirator


with open(".mpp_config") as fid:
    __version__ = json.load(fid)["version"]


class Application(ThemedTk):
    def __init__(self):
        # Themes : arc, breeze, equilux, radiance
        super().__init__()
        self.configure(theme="arc")

        self.var_theme = tk.StringVar(self, "arc")

        self.withdraw()
        self.title("Simulateur")
        self.iconbitmap(default="resources/images/icon.ico")
        self.setup_style()
        self.setup_ui()
        self.state("zoomed")
        self.deiconify()


    def setup_style(self):
        """
        Sets-up own style in the window.
        """

        with open("resources/config/style.json") as fid:
            style = json.load(fid)

        self.style = ttk.Style(self)
        for name, params in style.items():
            self.style.configure(name, **params)


    def setup_ui(self):
        """
        Sets-up frames in the mainwindow.
        """

        def set_theme(*args):
            self.configure(theme=self.var_theme.get())

        self.menubar = tk.Menu(self)
        self.menu_edit = tk.Menu(self.menubar, tearoff=0)
        self.menu_edit_theme = tk.Menu(self.menu_edit, tearoff=0)
        self.menu_edit_theme.add_radiobutton(label="Arc", value="arc", variable=self.var_theme, command=set_theme)
        self.menu_edit_theme.add_radiobutton(label="Breeze", value="breeze", variable=self.var_theme, command=set_theme)
        self.menu_edit_theme.add_radiobutton(label="Equilux", value="equilux", variable=self.var_theme, command=set_theme)
        self.menu_edit_theme.add_radiobutton(label="Radiance", value="radiance", variable=self.var_theme, command=set_theme)

        self.menubar.add_cascade(label="Edition", menu=self.menu_edit)
        self.menu_edit.add_cascade(label="Theme", menu=self.menu_edit_theme)
        self.config(menu=self.menubar)

        f_params = ttk.Frame(self)
        f_params.pack(side="left", fill="y")
        self.f_patient = FramePatient(f_params)
        self.f_patient.pack(fill="x", padx=5, pady=(5, 0))
        self.f_respi = FrameRespirator(f_params)
        self.f_respi.pack(fill="x", padx=5, pady=(5, 0))
        self.f_simu = FrameSimuation(f_params)
        self.f_simu.pack(fill="x", padx=5, pady=(5, 0))
        b = ttk.Button(f_params, text="Lancer la simulation", command=self.simulate)
        b.pack(fill="x", padx=5, pady=5)

        self.separator = ttk.Separator(self, orient="vertical")
        self.separator.pack(side="left", fill="y")

        self.f_graph = FrameGraph(self)
        self.f_graph.pack(side="left", fill="both", expand=True)


    def simulate(self):
        """
        Runs the simulation with all the parameters.
        """

        # Change cursor
        self.configure(cursor="wait")
        self.update()

        # Get simulation parameters
        patient = self.f_patient.get()
        mode = self.f_respi.get()
        duration = self.f_simu.get()

        # Process simulation
        respi = Respirator(patient, mode)
        self.f_graph.init(respi.as_array())
        for values in respi.loop(duration):
            self.f_graph.add(values)
        self.f_graph.show()

        # Change cursor back to normal
        self.configure(cursor="arrow")


if __name__ == '__main__':
    app = Application()
    app.mainloop()
