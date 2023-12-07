import os
import time

import customtkinter
from PIL import Image, ImageOps
import Menu


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # Windows
        self.title("WS-NEMO Demo")
        self.geometry(f"{600}x{400}")
        self.resizable(False,False)
        self.iconbitmap("favicon.ico")

        # Main Frame
        self.main_frame = customtkinter.CTkFrame(self, corner_radius=0, height=400)
        self.main_frame.pack_propagate(False)
        self.main_frame.pack(fill="both")

        self.header = None
        self.menu = None
        self.slideshow = customtkinter.CTkFrame(self.main_frame, corner_radius=0, height=250, width=400)
        self.slideshow.pack_propagate(False)
        self.load_home(self.main_frame)
        self.slideshow.pack(pady=25, fill="x")
        self.enable_eval_button()
        self.current_image = 0
        self.enable_train_button()
        self.enable_test_button()


    def load_home(self, m):
        self.header = customtkinter.CTkLabel(m, text="WS-Nemo", font=("Inter", 24, "bold"), corner_radius=0)
        self.header.pack(fill="x", pady=(0, 5))
        self.menu = Menu.Menu(m)
        self.menu.pack()

    def next_image(self):
        self.slideshow.winfo_children()[self.current_image].pack_forget()
        self.current_image = (self.current_image + 1) % len(self.slideshow.winfo_children())
        self.slideshow.winfo_children()[self.current_image].pack()

    def back_image(self):
        self.slideshow.winfo_children()[self.current_image].pack_forget()
        self.current_image = (self.current_image - 1) % len(self.slideshow.winfo_children())
        self.slideshow.winfo_children()[self.current_image].pack()



    def load_evaluate_images(self):
        for i in self.slideshow.winfo_children():
            i.destroy()
        for i in os.listdir(os.getcwd()+"\images"):
            image = Image.open(os.getcwd()+"\images\\"+i)
            image = ImageOps.contain(image, size=(400, 250))
            width, height = image.size
            ar = height / width
            image = customtkinter.CTkImage(image, size=(width, int(width * ar)))

            label = customtkinter.CTkLabel(self.slideshow, image=image, text="")
        self.slideshow.winfo_children()[0].pack()
        next_button = customtkinter.CTkButton(self.main_frame, text="Next", command=self.next_image, corner_radius=0)
        back_button = customtkinter.CTkButton(self.main_frame, text="Previous", command=self.back_image, corner_radius=0)
        next_button.pack(side="bottom", anchor="se", pady=5)
        back_button.pack(side="bottom", anchor="se")
        self.geometry(f"{600}x{475}")
        self.main_frame.configure(height=475)

    def display_progress(self):
        self.geometry(f"{600}x{400}")
        for i in self.slideshow.winfo_children():
            i.destroy()
        bar = customtkinter.CTkProgressBar(self.slideshow, mode="indeterminate")
        bar.set(0)
        bar.pack(pady=10, fill="x", padx=20)
        bar.start()


    def enable_eval_button(self):
        self.menu.evaluate.configure(command=self.load_evaluate_images)

    def enable_train_button(self):
        self.menu.train.configure(command=self.display_progress)

    def enable_test_button(self):
        self.menu.test.configure(command=self.display_progress)









if __name__ == "__main__":
    app = App()
    app.mainloop()