from os import replace
import tkinter as tk
import tkinter.filedialog
from config import *


class ReplayWindow(tk.Toplevel):
	def __init__(self, master, controller):
		super().__init__(master)
		self.replay_file = ""
		self.var_replay_file = tk.StringVar()
		self.replaylabel = tk.Label(self, text="Choose the replay file: ")
		self.replaylabel.grid(row=0, column=0, sticky="w",pady=2,padx=2)
		self.replayentry = tk.Entry(self, textvariable=self.var_replay_file, width=30)
		self.replayentry.grid(row=1, column=0, sticky="w",pady=2,padx=2)
		self.button_browse = tk.Button(self, text="...", command=lambda: self.browse_files())
		self.button_browse.grid(row=1, column=1, sticky="w")
		self.button_replay = tk.Button(self, text="Play", command=lambda: self.start_new_replay())
		self.button_replay.grid(row=3, column=0, sticky="w",pady=2,padx=2)
		self.label_info_replay_file_loaded=tk.Label(self, text="",foreground="red")
		self.label_info_replay_file_loaded.grid(row=4, column=0, sticky="w",columnspan=2,padx=2)
		self.controller = controller
		
	def browse_files(self):
		self.replay_file = tk.filedialog.askopenfilename(filetypes=[("Json File", "*.json")],initialdir=config['Folders']['replay_folder'])
		self.var_replay_file.set(self.replay_file)

	def start_new_replay(self):
		self.controller.initialize_replay(self.replay_file)
