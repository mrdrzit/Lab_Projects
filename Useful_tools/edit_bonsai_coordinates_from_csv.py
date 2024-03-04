import os
import tkinter as tk
import pandas as pd
import math
from tkinter import filedialog
from lxml import etree as ET
from pathlib import Path

DEBUG = False

def process_folder(folder_path):

    if DEBUG:
        bonsai_file = Path(r"C:\Users\Matheus\Desktop\templates\tmp.bonsai")
        layout_file = Path(r"C:\Users\Matheus\Desktop\templates\tmp.bonsai.layout")

    file_list = os.listdir(folder_path)
    
    # remove all files that are not .avi from the list
    file_list = [file for file in file_list if file.endswith(".avi")]
    total_files = len(file_list)

    for i, filename in enumerate(file_list):
        current_bonsai_file = os.path.join(folder_path, filename[:-4] + ".bonsai")
        current_roi_file = os.path.join(folder_path, filename[:-4] + "_coordinates.csv")

        coordinates = get_roi_coordinates(current_roi_file)
        # Parse bonsai XML file
        bonsai_tree = ET.parse(current_bonsai_file)
        bonsai_root = bonsai_tree.getroot()

        # Define the namespace
        ns = {'cv': 'clr-namespace:Bonsai.Vision;assembly=Bonsai.Vision'}

        # Find all <cv:Point> elements
        points = bonsai_root.findall('.//cv:Point', namespaces=ns)

        # Modify each point
        for ii, point in enumerate(points):
            row = ii // 4  # Get the row index
            col = ii % 4  # Get the column index
            x = point.find('cv:X', namespaces=ns)
            y = point.find('cv:Y', namespaces=ns)
            
            # Modify the X and Y values as needed
            if coordinates[row][col][0] < 0:
                x.text = "0"
            else:
                x.text = str(math.ceil(coordinates[row][col][0]))
            if coordinates[row][col][1] < 0:
                y.text = "0"
            else:
                y.text = str(math.ceil(coordinates[row][col][1]))
            print(f"coordinates[{row}][{col}] = {coordinates[row][col]}")

        # Find and update <cv:FileName> tag
        for filename_tag in bonsai_root.findall(".//{clr-namespace:Bonsai.Vision;assembly=Bonsai.Vision}FileName"):
            if filename_tag.text.endswith(".avi"):
                filename_tag.text = filename[:-4] + ".avi"
            else:
                filename_tag.text = filename + ".png"
        for filename_tag in bonsai_root.findall(".//{clr-namespace:Bonsai.IO;assembly=Bonsai.System}FileName"):
            filename_tag.text = filename[:-4] + ".csv"

        # Write changes back to file
        new_bonsai_file = os.path.join(current_path, os.path.splitext(filename)[0] + ".bonsai")
        bonsai_tree.write(new_bonsai_file, pretty_print=True)
        with open(new_bonsai_file, "wb") as f:
            f.write(b'<?xml version="1.0" encoding="UTF-8"?>\n')
            bonsai_tree.write(f, pretty_print=True)
            
        # Progress bar
        progress = (i + 1) / total_files
        bar_length = 20  # Modify this to change the length of the progress bar
        block = int(round(bar_length * progress))
        text = "\rProgress: [{0}] {1:.1f}%".format("#" * block + "-" * (bar_length - block), progress * 100)
        print(text, end='')
    print("\nDone!")

def get_roi_coordinates(roi_file):
    roi_data = pd.read_csv(
        roi_file,
        sep=",",
    )
    # Extract the coordinates from the DataFrame
    up_open_1 = roi_data.loc[0:3, ['X', 'Y']].values
    right_closed_2 = roi_data.loc[3:6, ['X', 'Y']].values
    down_open_3 = roi_data.loc[6:9, ['X', 'Y']].values
    left_closed_4 = pd.concat([roi_data.loc[9:9, ['X', 'Y']], roi_data.loc[10:10, ['X', 'Y']], roi_data.loc[11:11, ['X', 'Y']], roi_data.loc[0:0, ['X', 'Y']]]).values
    center_5 = pd.concat([roi_data.loc[0:0, ['X', 'Y']], roi_data.loc[3:3, ['X', 'Y']], roi_data.loc[6:6, ['X', 'Y']], roi_data.loc[9:9, ['X', 'Y']]]).values
    # print("up_open\n", up_open_1), print("right_closed\n", right_closed_2), print("down_open\n", down_open_3), print("left_closed\n", left_closed_4), print("center\n", center_5)

    return [up_open_1, right_closed_2, down_open_3, left_closed_4, center_5]

if DEBUG:
    current_path = Path(r"F:\Matheus\Bonsai\UFAL\CONVERTED_FROM_DAV\LCE\LCE_FEMEAS_19.06.23\All")
else:
    root = tk.Tk()
    root.withdraw()
    current_path = Path(filedialog.askdirectory(title="Choose the folder containing only the video files to be processed."))

process_folder(current_path)