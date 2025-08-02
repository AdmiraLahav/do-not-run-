import os

def create_terabyte_filler(filename="filler.txt"):
    """Creates a 1TB file filled with compressible data (repeated 'A')."""
    chunk_size = 1024 * 1024  # 1MB
    total_chunks = 1024 * 1024  # 1MB * 1,048,576 = 1TB

    with open(filename, "wb") as f:
        for i in range(total_chunks):
            f.write(b"A" * chunk_size)
            if i % 1024 == 0:  # Every GB, show progress
                print(f"Wrote {i // 1024} GB...")

    print("Done: 1TB written to", filename)

create_terabyte_filler()
