import os
import tkinter as tk
from collections import Counter
from tkinter import filedialog
from lxml import etree as ET
from pathlib import Path


def process_folder(folder_path):
    root = tk.Tk()
    root.withdraw()
    # Get the bonsai file
    bonsai_file = Path(filedialog.askopenfilename(title="Choose the .bonsai file to be used as template."))
    # Get the layout file
    layout_file = Path(filedialog.askopenfilename(title="Choose the .layout file to be used as template."))

    file_list = os.listdir(folder_path)
    video_extensions = [os.path.splitext(file)[1] for file in file_list if os.path.splitext(file)[1] in [".avi", ".mp4", ".mov", ".mkv", ".dav", ".flv", ".webm", ".mpeg", ".m4v"]]
    image_extensions = [os.path.splitext(file)[1] for file in file_list if os.path.splitext(file)[1] in [".png", ".jpg", ".jpeg", ".bmp", ".tiff", ".gif"]]
    video_extension_counts = Counter(video_extensions) 
    image_extension_counts = Counter(image_extensions)
    most_common_video_extension, _ = video_extension_counts.most_common(1)[0]
    most_common_image_extension, _ = image_extension_counts.most_common(1)[0]

    # remove all files that are not .avi from the list
    file_list = [file for file in file_list if file.endswith(most_common_video_extension)]
    
    total_files = len(file_list)
    for i, filename in enumerate(file_list):
        # Parse bonsai XML file
        bonsai_tree = ET.parse(bonsai_file)
        bonsai_root = bonsai_tree.getroot()
        layout_tree = ET.parse(layout_file)

        # Find and update <cv:FileName> tag
        for filename_tag in bonsai_root.findall(".//{clr-namespace:Bonsai.Vision;assembly=Bonsai.Vision}FileName"):
            if filename_tag.text.endswith(most_common_video_extension):
                filename_tag.text = filename[:-4] + most_common_video_extension
            else:
                filename_tag.text = filename + most_common_image_extension
        for filename_tag in bonsai_root.findall(".//{clr-namespace:Bonsai.IO;assembly=Bonsai.System}FileName"):
            filename_tag.text = filename[:-4] + ".csv"

        # Write changes back to file

        new_bonsai_file = os.path.join(current_path, os.path.splitext(filename)[0] + ".bonsai")
        bonsai_tree.write(new_bonsai_file, pretty_print=True)
        with open(new_bonsai_file, "wb") as f:
            f.write(b'<?xml version="1.0" encoding="UTF-8"?>\n')
            bonsai_tree.write(f, pretty_print=True)

        new_layout_file = os.path.join(current_path, os.path.splitext(filename)[0] + ".bonsai.layout")
        layout_tree.write(new_layout_file, pretty_print=True)
        with open(new_layout_file, "wb") as f:
            f.write(b'<?xml version="1.0" encoding="UTF-8"?>\n')
            layout_tree.write(f, pretty_print=True)
        # Progress bar
        progress = (i + 1) / total_files
        bar_length = 20  # Modify this to change the length of the progress bar
        block = int(round(bar_length * progress))
        text = "\rProgress: [{0}] {1:.1f}%".format("#" * block + "-" * (bar_length - block), progress * 100)
        print(text, end='')
    print("\nDone!")

# Replace 'folder_path' with the path to your folder containing video files, .bonsai, and .layout files
# Make the user choose the path to the folder
root = tk.Tk()
root.withdraw()
current_path = Path(filedialog.askdirectory(title="Choose the folder containing only the video files to be processed."))
process_folder(current_path)
