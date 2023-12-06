# Import necessary libraries
import os
import shutil
import re

# Define the root directory containing the files to be organized
root_dir = r"D:\Documents\NESTINGFP"

# Define regular expressions for matching specific file patterns
hdd_regex = re.compile(r"^animal\d+cx\d+(L\d+)?F\d+HDD\d+x\d+\.tif$")
hde_regex = re.compile(r"^animal\d+cx\d+(L\d+)?F\d+HDE\d+x\d+\.tif$")
hve_regex = re.compile(r"^animal\d+cx\d+(L\d+)?F\d+HVE\d+x\d+\.tif$")
hvd_regex = re.compile(r"^animal\d+cx\d+(L\d+)?F\d+HVD\d+x\d+\.tif$")

# Walk through the root directory, including all subdirectories and files
for subdir, dirs, files in os.walk(root_dir):
    for file in files:
        # Check if the file matches the HDD pattern
        if hdd_regex.match(file):
            # Skip the file if it has "10x" in the filename
            if "10x" in file:
                continue
            # Create a new directory for the matching files (HDD)
            new_dir = os.path.join(subdir, "HDD")
            os.makedirs(new_dir, exist_ok=True)
            # Move the file to the new directory
            old_path = os.path.join(subdir, file)
            new_path = os.path.join(new_dir, file)
            shutil.copy(old_path, new_path)
        # Check if the file matches the HDE pattern
        elif hde_regex.match(file):
            # Skip the file if it has "10x" in the filename
            if "10x" in file:
                continue
            # Create a new directory for the matching files (HDE)
            new_dir = os.path.join(subdir, "HDE")
            os.makedirs(new_dir, exist_ok=True)
            # Move the file to the new directory
            old_path = os.path.join(subdir, file)
            new_path = os.path.join(new_dir, file)
            shutil.copy(old_path, new_path)
        # Check if the file matches the HVE pattern
        elif hve_regex.match(file):
            # Skip the file if it has "10x" in the filename
            if "10x" in file:
                continue
            # Create a new directory for the matching files (HVE)
            new_dir = os.path.join(subdir, "HVE")
            os.makedirs(new_dir, exist_ok=True)
            # Move the file to the new directory
            old_path = os.path.join(subdir, file)
            new_path = os.path.join(new_dir, file)
            shutil.copy(old_path, new_path)
        # Check if the file matches the HVD pattern
        elif hvd_regex.match(file):
            # Skip the file if it has "10x" in the filename
            if "10x" in file:
                continue
            # Create a new directory for the matching files (HVD)
            new_dir = os.path.join(subdir, "HVD")
            os.makedirs(new_dir, exist_ok=True)
            # Move the file to the new directory
            old_path = os.path.join(subdir, file)
            new_path = os.path.join(new_dir, file)
            shutil.copy(old_path, new_path)
