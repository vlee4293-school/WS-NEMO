import customtkinter
import yaml
from tkinter import filedialog
import os


config_labels = {}


with open("quickstart.yaml", "r") as f:
    try:
        config_labels = dict(yaml.safe_load(f))
    except yaml.YAMLError as exc:
        print(exc)


class ToplevelWindow(customtkinter.CTkToplevel):

    def __init__(self, w=None):
        super().__init__()

        # Windows
        self.title("WS-NEMO Demo")
        self.geometry(f"{800}x{400}")
        self.resizable(False,False)

        self.entries = {}
        self.load_config_frame(self, w)



    def clear_config(self, frame):
        for entry in frame.winfo_children()[1::2]:
            entry.delete(0, 1000)

    def read_entries(self, w):
        for i in self.entries.keys():
            self.entries[i] = self.entries[i].get()
        filename = filedialog.asksaveasfilename(initialdir=os.getcwd())
        with open(filename, "w") as f:
            try:
                yaml.dump(self.entries, f, default_flow_style=False, sort_keys=False)
            except yaml.YAMLError as exc:
                print(exc)
        w.configure(state="normal")
        w.delete(0, 999)
        w.insert(0, os.path.basename(os.path.basename(filename)))
        w.configure(state="disabled")
        self.destroy()

    def load_config_frame(self, m, w):
        config = customtkinter.CTkFrame(self, bg_color="white", width=800, height=400, corner_radius=0)
        config.pack_propagate(False)
        config.pack(side="left", fill="both")

        config_topbar = customtkinter.CTkFrame(config, bg_color="white", height=40,
                                                    corner_radius=0)
        config_topbar.pack_propagate(False)
        config_topbar.pack(side="top", padx=5, pady=5, fill="x")

        config_midbar = customtkinter.CTkFrame(config, bg_color="white", height=290,
                                                    corner_radius=0)
        config_midbar.pack_propagate(False)
        config_midbar.pack(side="top", padx=5, pady=5, fill="x")

        config_botbar = customtkinter.CTkFrame(config, bg_color="white", height=40,
                                                    corner_radius=0)
        config_botbar.pack_propagate(False)
        config_botbar.pack(side="top", padx=5, pady=5, fill="x")

        # Top Buttons
        clear_button = customtkinter.CTkButton(config_topbar, text="Clear", command=lambda: self.clear_config(scrollable_frame))
        clear_button.pack(side="left", anchor="nw", padx=5, pady=5)

        # Scrollable Frame
        scrollable_frame = customtkinter.CTkScrollableFrame(config_midbar, label_text="Configuration",
                                                                 height=290, corner_radius=0)
        scrollable_frame.pack(side="top", fill="x")
        for i in range(0, len(config_labels) * 2, 2):
            lbl = customtkinter.CTkLabel(scrollable_frame, text=tuple(config_labels.keys())[int(i / 2)],
                                         anchor="w")
            entry = customtkinter.CTkEntry(scrollable_frame)
            lbl.pack(fill="x", padx=5)
            entry.pack(fill="x", padx=5, pady=(0, 5))
            self.entries.update({lbl.cget("text"): entry})

        # Bottom Buttons
        apply_button = customtkinter.CTkButton(config_botbar, text="Save", command=lambda: self.read_entries(w))
        apply_button.pack(side="right", anchor="se", padx=5, pady=5)



