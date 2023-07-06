import os
import shutil
import re

root_dir = r"D:\Documents\NESTINGFP"
new_root_dir = r"D:\Documents\NESTINGFP\to_stitch"
for subdir, dirs, files in os.walk(root_dir):
    for dir in dirs:
        if "HDD" in dir or "HDE" in dir or "HVE" in dir or "HVD" in dir:
            print("Copying {}...".format(dir))
            src_dir = os.path.join(subdir, dir)
            dst_dir = os.path.join(new_root_dir, os.path.relpath(src_dir, root_dir))
            shutil.copytree(src_dir, dst_dir)
