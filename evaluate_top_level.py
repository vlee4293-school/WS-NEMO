from PIL import Image, ImageOps
import os
import customtkinter as ctk



class EvaluateTop(ctk.CTkToplevel):
    def next_image(self):
        self.slideshow.winfo_children()[self.current_image].pack_forget()
        self.current_image = (self.current_image + 1) % len(self.slideshow.winfo_children())
        self.slideshow.winfo_children()[self.current_image].pack()

    def back_image(self):
        self.slideshow.winfo_children()[self.current_image].pack_forget()
        self.current_image = (self.current_image - 1) % len(self.slideshow.winfo_children())
        self.slideshow.winfo_children()[self.current_image].pack()

    def load_evaluate_images(self):
        for i in os.listdir(os.getcwd() + "\images"):
            image = Image.open(os.getcwd() + "\images\\" + i)
            image = ImageOps.contain(image, size=(400, 250))
            width, height = image.size
            ar = height / width
            image = ctk.CTkImage(image, size=(width, int(width * ar)))

            label = ctk.CTkLabel(self.slideshow, image=image, text="")
        self.slideshow.winfo_children()[0].pack()
        next_button = ctk.CTkButton(self, text="Next", command=self.next_image, corner_radius=0)
        back_button = ctk.CTkButton(self, text="Previous", command=self.back_image,
                                              corner_radius=0)
        next_button.pack(side="bottom", anchor="se", pady=5)
        back_button.pack(side="bottom", anchor="se")


    def __init__(self, root):
        super().__init__()

        self.slideshow = ctk.CTkFrame(self, corner_radius=0, height=250, width=400)
        self.slideshow.pack_propagate(False)
        self.slideshow.pack(pady=25, fill="x")
        self.current_image = 0
        self.load_evaluate_images()

