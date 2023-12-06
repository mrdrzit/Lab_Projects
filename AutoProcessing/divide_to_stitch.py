# Import necessary libraries
import os
import shutil
import re

# Define the root directory and the new root directory for copying
root_dir = r"D:\Documents\NESTINGFP"
new_root_dir = r"D:\Documents\NESTINGFP\to_stitch"

# Iterate through all subdirectories, directories, and files in the root directory
for subdir, dirs, files in os.walk(root_dir):
    # Iterate through the directories in the current subdirectory
    for dir in dirs:
        # Check if the directory name contains specific substrings
        if "HDD" in dir or "HDE" in dir or "HVE" in dir or "HVD" in dir:
            # Print a message indicating the start of the copying process
            print("Copying {}...".format(dir))
            
            # Define source and destination directories for copying
            src_dir = os.path.join(subdir, dir)
            dst_dir = os.path.join(new_root_dir, os.path.relpath(src_dir, root_dir))
            
            # Copy the entire directory tree from source to destination
            shutil.copytree(src_dir, dst_dir)
