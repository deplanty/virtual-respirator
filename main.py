import json
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
        respi = Respirator(patient, mode, duration)
        self.f_graph.init(respi.as_array())
        for values in respi.loop():
            self.f_graph.add(values)
        self.f_graph.show()

        # Change cursor back to normal
        self.configure(cursor="arrow")


if __name__ == '__main__':
    app = Application()
    app.mainloop()
