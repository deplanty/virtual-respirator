import csv
import json
import tkinter as tk
import tkinter.filedialog
from tkinter import ttk
from ttkthemes import ThemedTk

from src.frames.ctrl import FrameGraph, FramePatient, FrameRespirator, FrameSimuation
from src.objects import Respirator


with open(".mpp_config") as fid:
    __version__ = json.load(fid)["version"]


class Application(ThemedTk):
    def __init__(self):
        super().__init__()

        with open("resources/config/ui.json") as fid:
            self.ui_config = json.load(fid)

        self.var_theme = tk.StringVar(self, self.ui_config["theme"])

        self.withdraw()
        self.title("Simulateur")
        self.iconbitmap(default="resources/images/icon.ico")
        self.configure(theme=self.ui_config["theme"])
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
            theme = self.var_theme.get()

            self.ui_config["theme"] = theme
            with open("resources/config/ui.json", "w") as fid:
                json.dump(self.ui_config, fid, indent=4)

            self.configure(theme=theme)
            self.setup_style()

        # Menu bar
        self.menubar = tk.Menu(self)
        self.menu_file = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Fichier", menu=self.menu_file)
        self.menu_file.add_command(label="Nouveau")
        self.menu_file.add_command(label="Ouvrir ...")
        self.menu_file.add_command(label="Enregistrer")
        self.menu_file.add_command(label="Enregistrer sous ...")
        self.menu_file.add_separator()
        self.menu_file.add_command(label="Exporter ...", command=self.menu_file_export)
        self.menu_file.add_separator()
        self.menu_file.add_command(label="Quitter")
        self.menu_edit = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Edition", menu=self.menu_edit)
        self.menu_edit_theme = tk.Menu(self.menu_edit, tearoff=0)
        self.menu_edit.add_cascade(label="Theme", menu=self.menu_edit_theme)
        self.menu_edit_theme.add_radiobutton(label="Arc", value="arc", variable=self.var_theme, command=set_theme)
        self.menu_edit_theme.add_radiobutton(label="Breeze", value="breeze", variable=self.var_theme, command=set_theme)
        self.menu_edit_theme.add_radiobutton(label="Equilux", value="equilux", variable=self.var_theme, command=set_theme)
        self.menu_edit_theme.add_radiobutton(label="Radiance", value="radiance", variable=self.var_theme, command=set_theme)
        self.config(menu=self.menubar)

        # Elements
        f_params = ttk.Frame(self)
        f_params.pack(side="left", fill="y")
        self.f_patient = FramePatient(f_params)
        self.f_patient.pack(fill="x", padx=5, pady=(5, 0))
        self.f_respi = FrameRespirator(f_params)
        self.f_respi.pack(fill="x", padx=5, pady=(5, 0))
        self.f_simu = FrameSimuation(f_params)
        self.f_simu.pack(fill="x", padx=5, pady=(5, 0))
        b = ttk.Button(f_params, text="Lancer la simulation", command=self.btn_simulate)
        b.pack(fill="x", padx=5, pady=5)

        self.separator = ttk.Separator(self, orient="vertical")
        self.separator.pack(side="left", fill="y")
        self.f_graph = FrameGraph(self)
        self.f_graph.pack(side="left", fill="both", expand=True)


    def btn_simulate(self):
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
        self.f_graph.init(respi.get_array())
        for values in respi.loop(duration):
            self.f_graph.add(values)
        self.f_graph.show()

        # Change cursor back to normal
        self.configure(cursor="arrow")


    def menu_file_export(self):
        """
        Exports the values of the simulation.
        """

        # Asks where to save the file
        filename = tk.filedialog.asksaveasfilename(
            filetypes=[("CSV separateur point-virgule", "*.csv"), ("All files", "*.*")],
            defaultextension=".csv"
        )
        if not filename:
            return

        # Change cursor
        self.configure(cursor="wait")
        self.update()

        # Get simulation parameters
        patient = self.f_patient.get()
        mode = self.f_respi.get()
        duration = self.f_simu.get()

        # Process simulation
        respi = Respirator(patient, mode)
        with open(filename, "w", newline="") as fid:
            writer = csv.writer(fid, delimiter=";")
            writer.writerow(respi.get_header())
            writer.writerow(respi.get_array())
            for values in respi.loop(duration):
                writer.writerow(values)

        # Change cursor back to normal
        self.configure(cursor="arrow")


if __name__ == '__main__':
    app = Application()
    app.mainloop()
