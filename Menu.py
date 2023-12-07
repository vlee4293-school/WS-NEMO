import customtkinter
import os
from tkinter import filedialog
import yaml
import toplevel


class Menu:
    def __init__(self, master):
        self.frame = customtkinter.CTkFrame(master, corner_radius=0, fg_color=None, bg_color="transparent")
        self.config = customtkinter.CTkFrame(self.frame, corner_radius=0, fg_color=None, bg_color="transparent")
        self.tasks = customtkinter.CTkFrame(self.frame, corner_radius=0, fg_color=None, bg_color="transparent")

        self.filepath = None
        self.text = None
        self.new_config = None
        self.import_config = None
        self.config_values = {}
        self.load_config_buttons(self.config)
        self.config.pack(pady=(0,5))

        self.train = None
        self.test = None
        self.evaluate = None
        self.load_task_buttons(self.tasks)
        self.tasks.pack()

    def browse(self, w):
        self.filepath = filedialog.askopenfilename()
        w.configure(state="normal")
        w.delete(0, 999)
        w.insert(0, os.path.basename(self.filepath))
        w.configure(state="disabled")
        self.load_config()

    def create_new(self, w):
        toplevel.ToplevelWindow(w)

    def load_config_buttons(self, frame):
        self.text = customtkinter.CTkEntry(frame, state="disabled", corner_radius=0)
        self.new_config = customtkinter.CTkButton(frame, text="New Config YAML",
                                               command=lambda: self.create_new(self.text), corner_radius=0)
        self.import_config = customtkinter.CTkButton(frame, text="Import Config YAML", command=lambda: self.browse(self.text),
                                               corner_radius=0)
        self.new_config.pack(side="left", padx=(0, 5))
        self.import_config.pack(side="left", padx=(0, 5))
        self.text.pack(side="left")

    def load_config(self):
        with open(os.path.basename(self.filepath), "r") as f:
            self.config_values = yaml.safe_load(f)

    def pack(self, **kwargs):
        self.frame.pack(**kwargs)

    def load_task_buttons(self, frame):
        self.train = customtkinter.CTkButton(frame, text="Train", corner_radius=0)
        self.test = customtkinter.CTkButton(frame, text="Test", corner_radius=0)
        self.evaluate = customtkinter.CTkButton(frame, text="Evaluate", corner_radius=0)
        self.train.pack(side="left", padx=(0, 5))
        self.test.pack(side="left", padx=(0, 5))
        self.evaluate.pack(side="left")
