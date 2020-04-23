import json
import tkinter as tk
from tkinter import ttk

from src.frames.views import ViewRespirator
from src.frames.ctrl.modes import FrameModeVAC, FrameModeVPC, FrameModeVSAI


class FrameRespirator(ttk.LabelFrame):
    def __init__(self, master):
        super().__init__(master)
        self.configure(text="Respirateur")

        self.ui = ViewRespirator(self)
        self.frame = None

        self.mode_frames = {
            "VAC": FrameModeVAC(self.ui.mode_f_params),
            "VPC": FrameModeVPC(self.ui.mode_f_params),
            "VSAI": FrameModeVSAI(self.ui.mode_f_params)
        }

        self.set_default()
        self.load_mode()

        self.ui.mode_combo.bind("<<ComboboxSelected>>", self.load_mode)


    def set_default(self):
        """
        Sets the default values in the window
        """

        with open("resources/modes.json") as fid:
            modes = json.load(fid)

        modes = [name.upper() for name in modes]
        self.ui.mode_combo.configure(values=modes)
        self.ui.mode_combo.current(0)


    def load_mode(self, *args):
        """
        Loads the current selected mode in the window.
        And removes the previous one
        """

        # Get selected frame
        selected = self.ui.var_mode.get()
        selected = self.mode_frames[selected]

        # Do nothing if its the same
        if self.frame == selected:
            return

        # If a first frame has been packed
        if self.frame is not None:
            self.frame.pack_forget()
        # Use selected frame
        self.frame = selected
        self.frame.pack(fill="x")


    def get(self):
        """
        Returns a mode object with the parameters
        """

        return self.frame.get()

