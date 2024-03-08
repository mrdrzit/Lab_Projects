import os
import tkinter as tk
import glob
from tkinter import filedialog
from lxml import etree as ET
from pathlib import Path

DEBUG = False
def process_folder(folder_path):

    bonsai_files = glob.glob(os.path.join(folder_path, "*.bonsai"))
    # remove all files that are not .avi from the list

    for i, file in enumerate(bonsai_files):

        # Parse bonsai XML file
        bonsai_tree = ET.parse(file)
        bonsai_root = bonsai_tree.getroot()

        # Define the namespace
        ns = {'cv': 'clr-namespace:Bonsai.Vision;assembly=Bonsai.Vision'}

        # Find elements
        file_name = bonsai_root.findall('.//cv:FileName', namespaces=ns)  
        playback_rate = bonsai_root.findall('.//cv:PlaybackRate', namespaces=ns)
        start_position = bonsai_root.findall('.//cv:StartPosition', namespaces=ns)
        position_units = bonsai_root.findall('.//cv:PositionUnits', namespaces=ns)
        loop = bonsai_root.findall('.//cv:Loop', namespaces=ns)
        playing = bonsai_root.findall('.//cv:Playing', namespaces=ns)

        # Modify elements
        start_position[0].text = "160"

        # Write changes back to file
        new_bonsai_file = os.path.join(current_path, os.path.splitext(file)[0] + ".bonsai")
        bonsai_tree.write(new_bonsai_file, pretty_print=True)
        with open(new_bonsai_file, "wb") as f:
            f.write(b'<?xml version="1.0" encoding="UTF-8"?>\n')
            bonsai_tree.write(f, pretty_print=True)
            
        # Progress bar
        progress = (i + 1) / len(bonsai_files)
        bar_length = 20  # Modify this to change the length of the progress bar
        block = int(round(bar_length * progress))
        text = "\rProgress: [{0}] {1:.1f}%".format("#" * block + "-" * (bar_length - block), progress * 100)
        print(text, end='')
    print("\nDone!")

root = tk.Tk()
root.attributes('-topmost', True)
root.withdraw()
current_path = Path(filedialog.askdirectory(title="Choose the folder containing only the video files to be processed."))

process_folder(current_path)