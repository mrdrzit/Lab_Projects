# Import necessary libraries
import os
import re
import shutil
import tkinter as tk
from tkinter import filedialog
from natsort import os_sorted 

# Define a regular expression for extracting unique names from file names
def get_unique_names(file_list, regex):
  '''
  Returns a list of unique names from a list of files

  Input = list of files, regex
  '''
  unique_names = []
  for file in file_list:
    unique_names.append(regex.search(file).group(0))
  return list(dict.fromkeys(unique_names))

# Copy a list of files to a destination folder
def copy_to_folder(grouped_files, dest_folder):
  '''
  Copies a list of files to a destination folder

  Input = list of files, destination folder
  '''
  if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)
  for file in grouped_files:
    shutil.copy(file, dest_folder)

# Group files based on a specific naming pattern and copy them to corresponding folders
def group_files(folder_with_pics, pics, *args):
  # Define the regular expression for extracting unique names
  name = re.compile(r"^[0-9]{1,2}_[0-9]{1,2}fatia[0-9]{1,2}(\D{1,2}\d{1,2}|[HhVvDdEe]{1,4})_\d{1,2}")

  # Get unique names from the list of file names and sort them
  unique_file_names = os_sorted(get_unique_names(pics, name))
  grouped_files = []
  is_last_group = False

  # Iterate through the list of files
  for i, pic in enumerate(pics):
    try:
      unique_file_names[0] in pic and unique_file_names[0] in pics[i+1]
    except IndexError:
      is_last_group = True
    
    # Check if the current group is the last one
    if not is_last_group:
      # Check if the current file and the next file have the same unique name
      if unique_file_names[0] in pic and unique_file_names[0] in pics[i+1]:
        grouped_files.append(folder_with_pics + pic)
      else:
        grouped_files.append(folder_with_pics + pic)
        dest_folder = folder_with_pics + unique_file_names[0]
        print("Grouping files with the name " + unique_file_names[0])
        copy_to_folder(grouped_files, dest_folder)
        grouped_files = []
        unique_file_names.pop(0)
    else:
      # Check if the unique name is in the current file
      if unique_file_names[0] in pic:
        dest_folder = folder_with_pics + unique_file_names[0]
        grouped_files.append(folder_with_pics + pic)
        print("Grouping files with the name " + unique_file_names[0])
        copy_to_folder(grouped_files, dest_folder)
        grouped_files = []
        unique_file_names.pop(0)

# Set up a Tkinter file explorer
file_explorer = tk.Tk()
file_explorer.withdraw()
file_explorer.call('wm', 'attributes', '.', '-topmost', True)

# Ask user to select a folder using the file explorer
path = filedialog.askdirectory(title="Select the folder", mustexist=True).replace("/", "\\") + '\\'

# List directories in the selected folder
dirs = os_sorted(os.listdir(path))

# Check if there are subdirectories in the selected folder
there_is_folder = False
for dir in dirs:
  if os.path.isdir(path + dir):
    there_is_folder = True
    break

# Extract file names if there are subdirectories, else use the file names directly
if there_is_folder:
  folders = [[0] for _ in range(len(dirs))]
  for i, dir in enumerate(dirs):
    pics = [file for file in os_sorted(os.listdir(path + dir)) if file.endswith(".zvi") or file.endswith(".tif")]
    folders[i] = pics
else:
  pics = [file for file in dirs if file.endswith(".zvi") or file.endswith(".tif")]

# Group files based on naming patterns for each folder or for the main folder
if there_is_folder:
  for i, folder in enumerate(folders):
    print("\nGrouping files in folder: " + dirs[i])
    print("\n")
    group_files(path + dirs[i] + '\\', folder)
else:
  print("\nGrouping files in folder: " + path)
  print("\n")
  group_files(path, pics)

# Display completion message
print("\nDone!\n:]\n")

# Prompt user to press Enter to exit
a = input("Press enter to exit")
if a:
  exit()
 
# Regular expressions for getting the name of the slice without numbering
# regex to get the name of the slice without the numbering = "^[0-9_]{3,4}\D{5}\d{1,2}[DEde]\d{0,2}"
# regex to get the name of the slice without the numbering = "^[0-9]_[0-9]fatia[0-9]{1,2}[HhVvDdEe]{3,4}_\d{0,2}"
# regex to get the name of the slice without the numbering = "^[0-9]_[0-9][a-zA-Z]{0,5}[0-9]{1,2}[HhVvDdEe]{3,4}_\d{0,2}"
# regex to get the name of the slice without the numbering = "^[0-9]{1,2}_[0-9]{1,2}fatia[0-9]{1,2}(\D{1,2}\d{1,2}|[HhVvDdEe]{1,4})_\d{1,2}"

# Listening to: Eyes Without a Face by Billy Idol
