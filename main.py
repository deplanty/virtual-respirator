import csv
import glob
import json
import os
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

        self.title_pattern = "Simulateur - {filename}"
        self.var_theme = tk.StringVar(self, self.ui_config["theme"])
        self.var_filename = tk.StringVar(self, "Nouveau")

        self.withdraw()
        self.cmd_set_title()
        self.iconbitmap(default="resources/images/icon.ico")
        self.configure(theme=self.ui_config["theme"])
        self.setup_style()
        self.setup_ui()
        self.event_ui()
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
        self.menu_file.add_command(label="Nouveau", command=self.menu_file_new, accelerator="Ctrl+N")
        self.menu_file.add_command(label="Ouvrir ...", command=self.menu_file_open, accelerator="Ctrl+O")
        self.menu_file.add_command(label="Enregistrer", command=self.menu_file_save, accelerator="Ctrl+S")
        self.menu_file.add_command(label="Enregistrer sous ...", command=self.menu_file_saveas, accelerator="Ctrl+Shift+S")
        self.menu_file.add_separator()
        self.menu_file.add_command(label="Exporter ...", command=self.menu_file_export)
        self.menu_file.add_separator()
        self.menu_file.add_command(label="Quitter", command=self.quit)
        self.menu_edit = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Edition", menu=self.menu_edit)
        self.menu_edit_theme = tk.Menu(self.menu_edit, tearoff=0)
        self.menu_edit.add_cascade(label="Theme", menu=self.menu_edit_theme)
        self.menu_edit_theme.add_radiobutton(label="Arc", value="arc", variable=self.var_theme, command=set_theme)
        self.menu_edit_theme.add_radiobutton(label="Breeze", value="breeze", variable=self.var_theme, command=set_theme)
        self.menu_edit_theme.add_radiobutton(label="Equilux", value="equilux", variable=self.var_theme, command=set_theme)
        self.menu_edit_theme.add_radiobutton(label="Radiance", value="radiance", variable=self.var_theme, command=set_theme)
        self.menu_presets = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Préselection", menu=self.menu_presets)
        self.config(menu=self.menubar)

        self.set_presets()

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


    def event_ui(self):
        """
        Sets the events in the UI.
        """

        self.bind("<Control-n>", self.menu_file_new)
        self.bind("<Control-o>", self.menu_file_open)
        self.bind("<Control-s>", self.menu_file_save)
        self.bind("<Control-S>", self.menu_file_saveas)
        self.var_filename.trace("w", self.cmd_set_title)


    def set_presets(self):
        """
        Sets presets in the menu bar.
        """

        with open("resources/presets/patients.json", encoding="utf-8") as fid:
            patients = json.load(fid)

        for status in patients:
            menu = tk.Menu(self.menubar, tearoff=0)
            for name, params in patients[status].items():
                menu.add_command(label=name, command=lambda params=params, *args: self.f_patient.set(**params))
            self.menu_presets.add_cascade(label=status, menu=menu)

        list_vrs = glob.glob("resources/presets/*.vrs")
        for filename in list_vrs:
            name, _ = os.path.splitext(os.path.basename(filename))
            self.menu_presets.add_command(label=name, command=lambda filename=filename: self.load(filename))


    def cmd_set_title(self, *args):
        """
        Sets title from filename.
        """

        filename = os.path.basename(self.var_filename.get())
        self.title(self.title_pattern.format(filename=filename))


    def save(self, filename):
        """
        Saves the current parameters in a file.

        Args:
            filename (str): path to file
        """

        # Prepare data
        data = {
            "patient": self.f_patient.get_dict(),
            "respirator": {
                "mode": self.f_respi.ui.var_mode.get(),
                "modes": {name: mode.get_dict() for name, mode in self.f_respi.mode_frames.items()}
            },
            "simulation": self.f_simu.get_dict()
        }

        # Save in file
        with open(filename, "w") as fid:
            json.dump(data, fid, indent=4)
        self.var_filename.set(filename)

        tk.messagebox.showinfo(
            title="Sauvegarde",
            message="Fichier enregistré avec succès."
        )


    def load(self, filename):
        """
        Loads the parameters from a file.

        Args:
            filename (str): path to file
        """

        # Get data
        with open(filename) as fid:
            data = json.load(fid)

        # Set data
        self.f_patient.set(**data["patient"])
        self.f_respi.ui.var_mode.set(data["respirator"]["mode"])
        for name, parameters in data["respirator"]["modes"].items():
            self.f_respi.mode_frames[name].set(**parameters)
        self.f_simu.set(**data["simulation"])

        self.var_filename.set(filename)
        self.f_graph.set_default()


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
        simulation = self.f_simu.get()

        # Process simulation
        respi = Respirator(patient, mode)
        self.f_graph.init(respi.get_array())
        for values in respi.loop(simulation.t_max, simulation.t_step):
            self.f_graph.add(values)
        self.f_graph.show()

        # Change cursor back to normal
        self.configure(cursor="arrow")


    def menu_file_new(self, *args):
        """
        Resets all the values.
        """

        self.var_filename.set("Nouveau")
        self.f_patient.set_default()
        self.f_respi.set_default()
        self.f_simu.set_default()
        self.f_graph.set_default()


    def menu_file_open(self, *args):
        """
        Opens a virtual respirator simulation file.
        """

        # Asks which file to open
        filename = tk.filedialog.askopenfilename(
            filetypes=[("Virtual respirator simulation", "*.vrs"), ("All files", "*.*")]
        )
        if not filename:
            return

        self.load(filename)


    def menu_file_save(self, *args):
        """
        Saves the current simulation file file.
        """

        if self.var_filename.get() != "Nouveau":
            self.save(self.var_filename.get())
        else:
            self.menu_file_saveas()


    def menu_file_saveas(self, *args):
        """
        Saves the simulation parameters in a new file.
        """

        # Asks where to save the file
        filename = tk.filedialog.asksaveasfilename(
            filetypes=[("Virtual respirator simulation", "*.vrs"), ("All files", "*.*")],
            defaultextension=".vrs"
        )
        if not filename:
            return

        self.save(filename)


    def menu_file_export(self, *args):
        """
        Exports the curves of the simulation.
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

        # Process simulation and write file
        respi = Respirator(patient, mode)
        with open(filename, "w", newline="") as fid:
            # Init CSV Faile and graph
            writer = csv.writer(fid, delimiter=";")
            writer.writerow(respi.get_header())
            writer.writerow(respi.get_array())
            self.f_graph.init(respi.get_array())
            for values in respi.loop(duration):
                # Add current value
                writer.writerow(values)
                self.f_graph.add(values)
            # Show graph
            self.f_graph.show()

        # Change cursor back to normal
        self.configure(cursor="arrow")


if __name__ == '__main__':
    app = Application()
    app.mainloop()
