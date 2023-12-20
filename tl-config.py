import customtkinter as ctk
from tkinter import filedialog
import yaml
import os

config_labels = {
    'Training images directory.': '',
    'Training labels formatted as COCO json.': '',
    'Validation images directory.': '',
    'Validation labels formatted as COCO json.': '',
    'Testing images directory.': '',
    'Testing labels formatted as COCO json.': '',
    'Images directory for performing inference.': '',
    'Directory to save images and checkpoints.': '',
    'Mode to run the model in.': '',
    'Number of images per batch.': '',
    'Filepath of class-agnostic model weights.': '',
    'Number of classes in the dataset.': '',
    'Dropout probability in the Transformer.': '',
    'Whether to use our joint probability technique instead of learning the detection branch in the MIL classifier.': '',
    'Confidence threshold to display images during inference.': '',
    'IoU threshold for non-maximum suppression (0 for no NMS).': '',
    'Offset of image label indices.': '',
    'Batch interval for updating training progress bar.': '',
    'Whether to resume training using the PL Trainer.': '',
    'Whether to load all possible model weights from checkpoint.': '',
    'Whether to use a balanced random sampler in DataLoader.': '',
    'Whether to use sparsemax instead of softmax in the MIL head across the detections dimension.': '',
    'Whether a fully-supervised model is being used for testing or inference (e.g., when visualizing class-agnostic boxes).': '',
    'How many batches to visualize with prediction and ground-truth boxes during validation and test steps.': '',
    'Filepath of model weights.': '',
    'Number of workers in DataLoader.': '',
    'Learning rate for backbone and input projection.': '',
    'Learning rate for DETR modules.': '',
    'Factor by which to drop the learning rate every lr_patience epochs with no loss improvement.': '',
    'Learning rate for MIL head.': '',
    'How many epochs with no loss improvement after which the learning rate will drop': '',
    'How many epochs to run before dropping the learning rate.': '',
    'Scaling term for objectness regularization.': '',
    'Weight decay factor.': '',
    'Which activation to use in the transformer.': '',
    'How many layers to use in the decoder.': '',
    'How many reference points to use in the decoder.': '',
    'Whether to replace stride with dilation in the last conv block.': '',
    'How many layers to use in the encoder.': '',
    'How many reference points to use in the encoder.': '',
    'How many feature levels to use in the Transformer.': '',
    'Intermediate size of the feedforward layers in the Transformer.': '',
    'How many attention heads to use in the Transformer.': '',
    'Transformer embedding dimensionality.': '',
    'Type of positional embedding to use on the image features.': '',
    'Scale of the transformer position embedding.': '',
    'How many object queries to use in the transformer.': '',
    'Accumulated Gradient Batches': '',
    'Determinism': '',
    'Number of GPUs': '',
    'Max Epochs': ''
}

config_values = {
    'train_imgs_dir': '',
    'train_anns': '',
    'val_imgs_dir': '',
    'val_anns': '',
    'test_imgs_dir': '',
    'test_anns': '',
    'infer_imgs_dir': '',
    'save_dir': '',
    'task': '',
    'batch_size': '',
    'class_agnostic_weights': '',
    'classes': '',
    'dropout': '',
    'joint_probability': '',
    'infer_display_thresh': '',
    'nms_thresh': '',
    'offset': '',
    'refresh_rate': '',
    'resume_training': '',
    'resume_weights': '',
    'sampler': '',
    'sparse': '',
    'supervised': '',
    'viz_test_batches': '',
    'weights': '',
    'workers': '',
    'lr_backbone': '',
    'lr_detr': '',
    'lr_drop': '',
    'lr_mil': '',
    'lr_patience': '',
    'lr_step_size': '',
    'objectness_scale': '',
    'weight_decay': '',
    'activation': '',
    'dec_layers': '',
    'dec_points': '',
    'dilation': '',
    'enc_layers': '',
    'enc_points': '',
    'feature_levels': '',
    'feedforward_dim': '',
    'hidden_dim': '',
    'heads': '',
    'position_embedding': '',
    'position_embedding_scale': '',
    'queries': '',
    'accumulate_grad_batches': '',
    'deterministic': '',
    'gpus': '',
    'max_epochs': ''
}

class ConfigTL(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.load_main()


    def load_main(self):
        self.config_values = config_values
        self.title = 'Config'
        self.geometry(f'{800}x{600}')
        self.resizable(False, False)
        self.propagate(False)
        self.load_topbar()
        self.load_config()
        self.load_bottombar()

    def load_topbar(self):
        topbar = ctk.CTkFrame(self, height=35, corner_radius=0)
        topbar.propagate(False)
        import_button = ctk.CTkButton(topbar, text='Import', corner_radius=0, command=self.import_config)
        clear_button = ctk.CTkButton(topbar, text='Clear', corner_radius=0, command=self.clear)
        topbar.pack(fill='x')
        clear_button.pack(side='right', padx=3)
        import_button.pack(side='right')

    def load_config(self):
        config = ctk.CTkFrame(self, corner_radius=0)
        config.pack(fill='both', expand=True)
        self.load_entry(config)


    def load_entry(self, frame):
        entry_window = ctk.CTkScrollableFrame(frame, label_text='Model Configurations', corner_radius=0)
        entry_window.pack(side='left', fill='both', expand=True)
        for i in config_labels:
            entry = ctk.CTkFrame(entry_window, corner_radius=0)
            entry.pack(fill='x', padx=10)
            label = ctk.CTkLabel(entry, text=i, anchor='w', corner_radius=0)
            field = ctk.CTkEntry(entry, corner_radius=0)
            label.pack(fill='x', padx=5)
            field.pack(side='left', fill='x', padx=5, expand=True)
        for i in (0, 2, 4, 6, 7):
            dir_button = ctk.CTkButton(entry_window.winfo_children()[i], text='Select Directory', corner_radius=0)
            dir_button.configure(command=lambda i=i: self.button_fill_dir(entry_window.winfo_children()[i].winfo_children()[1]))
            dir_button.pack(side='left', fill='x', padx=5)
        for i in (1, 3, 5, 10, 24):
            file_button = ctk.CTkButton(entry_window.winfo_children()[i], text='Select File', corner_radius=0)
            file_button.configure(command=lambda i=i: self.button_fill_file(entry_window.winfo_children()[i].winfo_children()[1]))
            file_button.pack(side='left', fill='x', padx=5)


    def button_fill_file(self, frame):
        filepath = filedialog.askopenfilename()
        frame.delete(0,ctk.END)
        frame.insert(0, filepath)

    def button_fill_dir(self, frame):
        filepath = filedialog.askdirectory()
        frame.delete(0,ctk.END)
        frame.insert(0, filepath)

    def clear(self):
        for i in self.winfo_children()[1].winfo_children()[0].winfo_children()[0].winfo_children()[0].winfo_children():
            i.winfo_children()[1].delete(0, ctk.END)

    def import_config(self):
        filepath = filedialog.askopenfilename()
        with open(filepath, 'r') as f:
            temp = dict(yaml.safe_load(f))
        for j, i in enumerate(self.winfo_children()[1].winfo_children()[0].winfo_children()[0].winfo_children()[0].winfo_children()):
            i.winfo_children()[1].insert(0, tuple(temp.values())[j])


    def load_bottombar(self):
        bottombar = ctk.CTkFrame(self, height=35, corner_radius=0)
        bottombar.propagate(False)
        save_button = ctk.CTkButton(bottombar, text='Save', corner_radius=0, command=self.save_config)
        bottombar.pack(side='bottom', fill='x')
        save_button.pack(side='right', padx=3)

    def save_config(self):
        for j, i in enumerate(self.winfo_children()[1].winfo_children()[0].winfo_children()[0].winfo_children()[0].winfo_children()):
            entry = i.winfo_children()[1].get()
            self.config_values.update({tuple(config_values.keys())[j]: entry})
        filepath = filedialog.asksaveasfilename(initialdir=os.getcwd())
        with open(filepath, 'w') as f:
            yaml.dump(self.config_values, f, default_flow_style=False, sort_keys=False)
        self.destroy()


if __name__ == '__main__':
    window = ConfigTL()
    window.mainloop()