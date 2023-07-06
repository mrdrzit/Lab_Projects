import os
import shutil
import re

root_dir = r"D:\Documents\NESTINGFP"
hdd_regex = re.compile(r"^animal\d+cx\d+(L\d+)?F\d+HDD\d+x\d+\.tif$")
hde_regex = re.compile(r"^animal\d+cx\d+(L\d+)?F\d+HDE\d+x\d+\.tif$")
hve_regex = re.compile(r"^animal\d+cx\d+(L\d+)?F\d+HVE\d+x\d+\.tif$")
hvd_regex = re.compile(r"^animal\d+cx\d+(L\d+)?F\d+HVD\d+x\d+\.tif$")

for subdir, dirs, files in os.walk(root_dir):
    for file in files:
        if hdd_regex.match(file):
            # skip the file if it has "10x" in the filename
            if "10x" in file:
                continue
            # create a new directory for the matching files
            new_dir = os.path.join(subdir, "HDD")
            os.makedirs(new_dir, exist_ok=True)
            # move the file to the new directory
            old_path = os.path.join(subdir, file)
            new_path = os.path.join(new_dir, file)
            shutil.copy(old_path, new_path)
        elif hde_regex.match(file):
            # skip the file if it has "10x" in the filename
            if "10x" in file:
                continue
            # create a new directory for the matching files
            new_dir = os.path.join(subdir, "HDE")
            os.makedirs(new_dir, exist_ok=True)
            # move the file to the new directory
            old_path = os.path.join(subdir, file)
            new_path = os.path.join(new_dir, file)
            shutil.copy(old_path, new_path)
        elif hve_regex.match(file):
            # skip the file if it has "10x" in the filename
            if "10x" in file:
                continue
            # create a new directory for the matching files
            new_dir = os.path.join(subdir, "HVE")
            os.makedirs(new_dir, exist_ok=True)
            # move the file to the new directory
            old_path = os.path.join(subdir, file)
            new_path = os.path.join(new_dir, file)
            shutil.copy(old_path, new_path)
        elif hvd_regex.match(file):
            # skip the file if it has "10x" in the filename
            if "10x" in file:
                continue
            # create a new directory for the matching files
            new_dir = os.path.join(subdir, "HVD")
            os.makedirs(new_dir, exist_ok=True)
            # move the file to the new directory
            old_path = os.path.join(subdir, file)
            new_path = os.path.join(new_dir, file)
            shutil.copy(old_path, new_path)
