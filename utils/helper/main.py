import shutil
import os
from pathlib import Path


# Define source and destination paths
source_folder = Path(os.path.abspath("utils/helper"))
destination_folder = Path(os.path.abspath("docker"))


# Check if the source folder exists
if not source_folder.exists():
    print(f"Error: Source folder '{source_folder}' does not exist.")
else:
    # Remove the destination folder if it already exists
    if destination_folder.exists():
        shutil.rmtree(destination_folder)

    # Create the destination folder and copy the contents
    try:
        shutil.copytree(source_folder, destination_folder)
        print(f"Folder copied from {source_folder} to {destination_folder}")
    except Exception as e:
        print(f"Error: {e}")