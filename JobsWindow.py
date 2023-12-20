import customtkinter as ctk
import multiprocessing as mp
from job import my_job
import datetime
from evaluate_top_level import EvaluateTop
from tl_config import ConfigTL
import os
from PIL import Image, ImageOps






class Jobs(ctk.CTk):


    def open_eval(self):
        EvaluateTop(self)
    # Reload the Job Lists
    def reload_job_list(self):
        try:
            # Check for jobs in the list
            for key in self.job_to_processes.keys():
                process = self.job_to_processes[key]

                # If any job processes are done, transfer to completed tab
                if process is not None and not process.is_alive():
                    print(self.job_to_processes[key])
                    cfg = [key.winfo_children()[i].cget('text') for i in range(4)]
                    job = ctk.CTkFrame(self.job_list[1], height=50, corner_radius=0)
                    job.grid_propagate(False)
                    job.columnconfigure((0, 1, 2, 3, 4), weight=2)
                    job.columnconfigure((5, 6), weight=1)
                    job.rowconfigure(0, weight=1)
                    job_id = ctk.CTkLabel(job, text=cfg[0])
                    job_task = ctk.CTkLabel(job, text=cfg[1])
                    job_cfg = ctk.CTkLabel(job, text=cfg[2])
                    job_date = ctk.CTkLabel(job, text=cfg[3])
                    progress = ctk.CTkLabel(job, text='Done')
                    start_button = ctk.CTkButton(job, text='Evaluate', width=75, command=self.open_eval)
                    remove_button = ctk.CTkButton(job, text='Remove', width=75, command=lambda: self.remove_completed_job(job))
                    job.pack(fill='x', expand=True, pady=3)
                    job_id.grid(row=0, column=0)
                    job_task.grid(row=0, column=1)
                    job_cfg.grid(row=0, column=2)
                    job_date.grid(row=0, column=3)
                    progress.grid(row=0, column=4)
                    start_button.grid(row=0, column=5)
                    remove_button.grid(row=0, column=6)

                    # Remove instance from processing tab
                    self.completed_frames.append(job)
                    self.remove_job(key)

            print("Reloaded")

        # If the dictionary size changes during iteration, reload again
        except RuntimeError:
            self.reload_job_list()

    # Switch frames between each other
    def switch(self, target):
        if target == self.current:
            pass
        else:
            if target == 'processing':
                self.buttons[0].pack_forget()
                self.job_list[1].pack_forget()
                self.job_list[0].pack(fill='both', expand=True)
                self.buttons[1].pack(side='right', padx=5)
                self.buttons[0].pack(side='left', padx=5)
            else:
                self.buttons[0].pack_forget()
                self.job_list[0].pack_forget()
                self.job_list[1].pack(fill='both', expand=True)
                self.buttons[1].pack_forget()
                self.buttons[0].pack(side='left', padx=5)
            self.current = target

    # Remove a job from the list
    def remove_job(self, job):

        # If there is a running job, terminate to remove
        if self.job_to_processes[job] is not None and self.job_to_processes[job].is_alive():
            self.job_to_processes[job].terminate()
            print("Canceled")

        # Get rid of the job in the dictionary and GUI
        del self.job_to_processes[job]
        job.destroy()

    def remove_completed_job(self, job):
        self.completed_frames.remove(job)
        job.destroy()


    # Start multiprocessing for jobs and update frames.
    def start_job(self, job):
        job_process = mp.Process(target=my_job)
        job_process.start()
        job.winfo_children()[4].configure(text='Started')
        job.winfo_children()[5].configure(state='disabled')
        self.job_to_processes.update({job: job_process})


    # Add a frame for job details based on input.
    def add_job(self):
        # Display Job
        job = ctk.CTkFrame(self.job_list[0], height=50, corner_radius=0)
        job.grid_propagate(False)
        job.columnconfigure((0,1,2,3,4), weight=2)
        job.columnconfigure((5,6), weight=1)
        job.rowconfigure(0, weight=1)
        job_id = ctk.CTkLabel(job, text=str(self.counter))
        job_task = ctk.CTkLabel(job, text="Training")
        job_cfg = ctk.CTkLabel(job, text=self.config)
        job_date = ctk.CTkLabel(job, text=datetime.datetime.now().strftime('%y-%m-%d %H:%M:%S'))
        progress = ctk.CTkLabel(job, text="Not Started")
        start_button = ctk.CTkButton(job, command=lambda: self.start_job(job), text='Start', width=75)
        remove_button = ctk.CTkButton(job, command=lambda: self.remove_job(job), text='Remove', width=75)
        job.pack(fill='x', expand=True, pady=3)
        job_id.grid(row=0, column=0)
        job_task.grid(row=0, column=1)
        job_cfg.grid(row=0, column=2)
        job_date.grid(row=0, column=3)
        progress.grid(row=0, column=4)
        start_button.grid(row=0, column=5)
        remove_button.grid(row=0, column=6)
        self.job_to_processes.update({job: None})
        self.counter += 1

        self.reload_job_list()


    def open_config(self):
        ConfigTL(self)

    def get_config(self, config):
        self.config = config
        self.add_job()

    # The App
    def __init__(self):
        super().__init__()

        self.counter = 0
        self.geometry(f'{700}x{500}')
        self.resizable(False, False)
        self.current = None
        self.config = None
        self.iconbitmap("favicon.ico")
        self.title("WS-NEMO Demo")

        self.center_frame = ctk.CTkFrame(self)
        self.tab_bar = ctk.CTkFrame(self, height=35)
        self.tab_bar.propagate(False)
        self.tab_bar.pack(fill='x')
        self.center_frame.pack(fill='both', expand=True)

        self.tabs = [ctk.CTkButton(self.tab_bar) for _ in range(3)]
        self.tabs[0].configure(text='Processing', command=lambda: self.switch('processing'))
        self.tabs[1].configure(text='Complete', command=lambda: self.switch('completed'))
        self.tabs[0].pack(side='left', padx=5)
        self.tabs[1].pack(side='left', padx=5)

        self.job_list = []
        self.job_list.append(ctk.CTkScrollableFrame(self.center_frame, label_text='Processing Jobs'))
        self.job_list.append(ctk.CTkScrollableFrame(self.center_frame, label_text='Completed Jobs'))
        self.job_frames = []
        self.completed_frames = []
        self.job_processes = []
        self.job_to_processes = {}

        self.button_bar = ctk.CTkFrame(self, height=35)
        self.button_bar.propagate(False)
        self.button_bar.pack(fill='x')

        self.buttons = [ctk.CTkButton(self.button_bar) for _ in range(2)]
        self.buttons[0].configure(text='Refresh', command=self.reload_job_list)
        self.buttons[1].configure(text='New', command=self.open_config)










if __name__ == '__main__':
    app = Jobs()
    app.mainloop()