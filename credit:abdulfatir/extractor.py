import zipfile
import os
import shutil

def extract_all_recursive(base_dir):
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
                            print(f"Extracted {zip_path} to {target_dir}")
                        os.remove(zip_path)
                        found = True
                    except Exception as e:
                        print(f"Failed to extract {zip_path}: {e}")
        if not found:
            break
        round += 1
        print(f"Extraction round {round} complete.")

if __name__ == "__main__":
    os.makedirs("bomb_detonated", exist_ok=True)
    shutil.copy("bomb.zip", "bomb_detonated/bomb.zip")
    extract_all_recursive("bomb_detonated")
