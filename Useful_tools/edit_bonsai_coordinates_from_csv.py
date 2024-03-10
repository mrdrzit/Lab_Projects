import os
import tkinter as tk
import pandas as pd
import math
from collections import Counter
from tkinter import filedialog
from lxml import etree as ET
from pathlib import Path

DEBUG = False

def process_folder(folder_path):

    if DEBUG:
        bonsai_file = Path(r"C:\Users\Matheus\Desktop\templates\tmp.bonsai")
        layout_file = Path(r"C:\Users\Matheus\Desktop\templates\tmp.bonsai.layout")

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
        current_bonsai_file = os.path.join(folder_path, filename[:-4] + ".bonsai")
        current_roi_file = os.path.join(folder_path, filename[:-4] + "_coordinates.csv")

        coordinates, experiment_type = get_roi_coordinates(current_roi_file)
        if coordinates is None or experiment_type is None:
            print(f"Could not determine the layout of the coordinates for {filename}. Please make sure the .csv file has the correct number of coordinates and try again for this file.\nSkipping to the next file...")
            continue
        # Parse bonsai XML file
        bonsai_tree = ET.parse(current_bonsai_file)
        bonsai_root = bonsai_tree.getroot()

        # Define the namespace
        ns = {'cv': 'clr-namespace:Bonsai.Vision;assembly=Bonsai.Vision'}

        # Find all <cv:Point> elements
        points = bonsai_root.findall('.//cv:Point', namespaces=ns)
        
        if experiment_type == "plus_maze":
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
        elif experiment_type == "open_field":
            # Modify each point
            for ii, point in enumerate(points):
                x = point.find('cv:X', namespaces=ns)
                y = point.find('cv:Y', namespaces=ns)
                
                # Modify the X and Y values as needed
                if coordinates[ii][0][0] < 0:
                    x.text = "0"
                else:
                    x.text = str(math.ceil(coordinates[ii][0][0]))
                if coordinates[ii][0][1] < 0:
                    y.text = "0"
                else:
                    y.text = str(math.ceil(coordinates[ii][0][1]))
                print(f"coordinates[{ii}][{0}] = {coordinates[ii][0]}")

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

    if len(roi_data["X"]) == len(roi_data["Y"]) and len(roi_data["X"]) == 12:
        # Extract the coordinates from the DataFrame
        print("\nFound 12 coordinates, treating as an Elevated Plus Maze layout. Where, in order, the coordinates are: up_open_1, right_closed_2, down_open_3, left_closed_4, center_5.")
        up_open_1 = roi_data.loc[0:3, ['X', 'Y']].values
        right_closed_2 = roi_data.loc[3:6, ['X', 'Y']].values
        down_open_3 = roi_data.loc[6:9, ['X', 'Y']].values
        left_closed_4 = pd.concat([roi_data.loc[9:9, ['X', 'Y']], roi_data.loc[10:10, ['X', 'Y']], roi_data.loc[11:11, ['X', 'Y']], roi_data.loc[0:0, ['X', 'Y']]]).values
        center_5 = pd.concat([roi_data.loc[0:0, ['X', 'Y']], roi_data.loc[3:3, ['X', 'Y']], roi_data.loc[6:6, ['X', 'Y']], roi_data.loc[9:9, ['X', 'Y']]]).values
        return [up_open_1, right_closed_2, down_open_3, left_closed_4, center_5], "plus_maze"
    
    elif len(roi_data["X"]) == len(roi_data["Y"]) and len(roi_data["X"]) == 4:
        print("\nFound 4 coordinates, treating as an Open Field. Where, in order, the coordinates are: top_left, top_right, bottom_right, bottom_left.")
        top_left = roi_data.loc[0:0, ['X', 'Y']].values
        top_right = roi_data.loc[1:1, ['X', 'Y']].values
        bottom_right = roi_data.loc[2:2, ['X', 'Y']].values
        bottom_left = roi_data.loc[3:3, ['X', 'Y']].values
        return [top_left, top_right, bottom_right, bottom_left], "open_field"
    else:
        return None, None

if DEBUG:
    current_path = Path(r"F:\Matheus\Bonsai\UFAL\CONVERTED_FROM_DAV\LCE\LCE_FEMEAS_19.06.23\All")
else:
    root = tk.Tk()
    root.attributes('-topmost', True)
    root.withdraw()
    current_path = Path(filedialog.askdirectory(title="Choose the folder containing only the video files to be processed."))

process_folder(current_path)