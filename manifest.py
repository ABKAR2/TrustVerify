import os
import json
from hashing import generate_file_hash


def generate_manifest(directory, output_file="output/metadata.json"):
    manifest = {}

    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)

        if os.path.isfile(file_path):
            file_hash = generate_file_hash(file_path)
            manifest[filename] = file_hash

    os.makedirs("output", exist_ok=True)

    with open(output_file, "w") as f:
        json.dump(manifest, f, indent=4)

    print("Metadata file generated successfully.")


def check_integrity(directory, metadata_file="output/metadata.json"):
    if not os.path.exists(metadata_file):
        print("Metadata file not found.")
        return

    with open(metadata_file, "r") as f:
        old_manifest = json.load(f)

    for filename, old_hash in old_manifest.items():
        file_path = os.path.join(directory, filename)

        if not os.path.exists(file_path):
            print(f"{filename} was deleted!")
            continue

        new_hash = generate_file_hash(file_path)

        if new_hash != old_hash:
            print(f"{filename} has been modified!")
        else:
            print(f"{filename} is OK.")