import os
import tkinter as tk
import pandas as pd
from tkinter import filedialog
from lxml import etree as ET
from pathlib import Path

DEBUG = True

def process_folder(folder_path, coordinates):

    if DEBUG:
        bonsai_file = Path(r"C:\Users\Matheus\Desktop\templates\tmp.bonsai")
        layout_file = Path(r"C:\Users\Matheus\Desktop\templates\tmp.bonsai.layout")
    else:
        root = tk.Tk()
        root.wm_attributes('-topmost', 1)
        root.withdraw()

        # Get the bonsai file
        bonsai_file = Path(filedialog.askopenfilename(title="Choose the .bonsai file to be used as template.", ))
        # Get the layout file
        layout_file = Path(filedialog.askopenfilename(title="Choose the .layout file to be used as template."))

    file_list = os.listdir(folder_path)
    
    # remove all files that are not .avi from the list
    file_list = [file for file in file_list if file.endswith(".avi")]

    for i, filename in enumerate(file_list):
        # Parse bonsai XML file
        bonsai_tree = ET.parse(bonsai_file)
        bonsai_root = bonsai_tree.getroot()
        layout_tree = ET.parse(layout_file)

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
            x.text = str(coordinates[row][col][0])
            y.text = str(coordinates[row][col][1])

        # Find and update <cv:FileName> tag
        for filename_tag in bonsai_root.findall(".//{clr-namespace:Bonsai.Vision;assembly=Bonsai.Vision}FileName"):
            if filename_tag.text.endswith(".avi"):
                filename_tag.text = filename[:-4] + ".avi"
            else:
                filename_tag.text = filename + ".png"
        for filename_tag in bonsai_root.findall(".//{clr-namespace:Bonsai.IO;assembly=Bonsai.System}FileName"):
            filename_tag.text = filename[:-4] + ".csv"

        # Write changes back to file

        new_bonsai_file = os.path.join(current_path, os.path.splitext(filename)[0] + "_EPM.bonsai")
        bonsai_tree.write(new_bonsai_file, pretty_print=True)
        with open(new_bonsai_file, "wb") as f:
            f.write(b'<?xml version="1.0" encoding="UTF-8"?>\n')
            bonsai_tree.write(f, pretty_print=True)

        new_layout_file = os.path.join(current_path, os.path.splitext(filename)[0] + "_EPM.bonsai.layout")
        layout_tree.write(new_layout_file, pretty_print=True)
        with open(new_layout_file, "wb") as f:
            f.write(b'<?xml version="1.0" encoding="UTF-8"?>\n')
            layout_tree.write(f, pretty_print=True)

def get_roi_coordinates(roi_file):
    roi_data = pd.read_csv(
        roi_file,
        sep=",",
    )
    # Extract the coordinates from the DataFrame
    up_open_1 = roi_data.loc[0:3, ['BX', 'BY']].values
    right_closed_2 = roi_data.loc[3:6, ['BX', 'BY']].values
    down_open_3 = roi_data.loc[6:9, ['BX', 'BY']].values
    left_closed_4 = pd.concat([roi_data.loc[9:9, ['BX', 'BY']], roi_data.loc[10:10, ['BX', 'BY']], roi_data.loc[11:11, ['BX', 'BY']], roi_data.loc[0:0, ['BX', 'BY']]]).values
    center_5 = pd.concat([roi_data.loc[0:0, ['BX', 'BY']], roi_data.loc[3:3, ['BX', 'BY']], roi_data.loc[6:6, ['BX', 'BY']], roi_data.loc[9:9, ['BX', 'BY']]]).values
    print("up_open\n", up_open_1), print("right_closed\n", right_closed_2), print("down_open\n", down_open_3), print("left_closed\n", left_closed_4), print("center\n", center_5)

    return [up_open_1, right_closed_2, down_open_3, left_closed_4, center_5]

# Replace 'folder_path' with the path to your folder containing video files, .bonsai, and .layout files
# Make the user choose the path to the folder

if DEBUG:
    current_path = Path(r"F:\Matheus\Bonsai\UFAL\CONVERTED_FROM_DAV\LCE\LCE_FEMEAS_19.06.23\All")
else:
    root = tk.Tk()
    root.withdraw()
    current_path = Path(filedialog.askdirectory(title="Choose the folder containing only the video files to be processed."))

roi_path = r"C:\Users\Matheus\Desktop\coordinates.csv"
coordinates = get_roi_coordinates(roi_path)

process_folder(current_path, coordinates)