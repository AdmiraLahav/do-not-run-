import os

def create_terabyte_filler(filename="filler.txt"):
    """Creates a 1TB file filled with compressible data, showing progress in MB."""
    chunk_size = 1024 * 1024  # 1MB
    total_chunks = 1024 * 1024  # 1,048,576 MB = 1TB

    with open(filename, "wb") as f:
        for i in range(total_chunks):
            f.write(b"Nice" * chunk_size)
            print(f"Wrote {i + 1} MB...")

    print("Done: 1TB written to", filename)

create_terabyte_filler()
