import os
from pydoc import plain
import re
import shutil
import tkinter as tk
from tkinter import filedialog

def group_files(files_list, new_folder, folder):
  print(f"\nGrouping files in the folder '{folder}'... please wait")
  for i, file in enumerate(files_list):
    position = (re.search(r"(20x).{2}", file, re.IGNORECASE)).group(0)
    if position[-2:] == "01" and i > 0:
      last_file_index = (re.search(r"(20x).{2}", files_list[i-1], re.IGNORECASE)).group(0)[-2:]
      oncoto = i - int(last_file_index)
      oncovo = i
      for pic_index in range(oncoto, oncovo):
        new_folder.append(files_list[pic_index])
      
      newfolder = folder + '\\' + files_list[oncoto][0:-4]
      
      if not os.path.exists(newfolder):
        os.makedirs(newfolder)
      else:
        print(f"Folder {path} already exists")

      jk=oncoto+1
      for pic in new_folder:
        oldpath = folder + '\\' + pic
        newpath = newfolder + "\\" + pic
        print("Working on " + pic + ", which is " + str(jk) + " of " + str(len(files_list)))
        jk+=1
        shutil.copy(oldpath, newpath)
      
      new_folder = []
    elif i == len(files_list)-1:
      last_file_index = (re.search(r"(20x).{2}", files_list[i], re.IGNORECASE)).group(0)[-2:]
      oncoto = i - int(last_file_index) + 1
      oncovo = i + 1
      for pic_index in range(oncoto, oncovo):
        new_folder.append(files_list[pic_index])
      
      newfolder = folder + '\\' + files_list[oncoto][0:-4]
      

      if not os.path.exists(newfolder):
        os.makedirs(newfolder)
      else:
        print(f"Folder {path} already exists")

      jk=oncoto+1
      for pic in new_folder:
        oldpath = folder + '\\' + pic
        newpath = newfolder + "\\" + pic
        print("Working on " + pic + ", which is " + str(jk) + " of " + str(len(files_list)))
        jk+=1
        shutil.copy(oldpath, newpath)
      
      new_folder = []
  pass

def get_unique_names(file_list):
  unique_names = []
  for file in file_list:
    unique_names.append(name.search(file).group(0))
  return list(dict.fromkeys(unique_names))

def copy_to_folder(grouped_files, dest_folder):
  if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)
  for file in grouped_files:
    shutil.copy(file, dest_folder)
  pass





# find all files missing the token _20x  = "[^20]{2}(?=x)"
# find all number following the token _20x  = "(?<=_20).{3}"
# regex to get the name of the slice without the numbering = "^[0-9_]{3,4}\D{5}\d{1,2}[DEde]\d{0,2}"

file_explorer = tk.Tk()
file_explorer.withdraw()
file_explorer.call('wm', 'attributes', '.', '-topmost', True)
path = filedialog.askdirectory(title = "Select the folder", mustexist = True).replace("/", "\\") + '\\'
dirs = next(os.walk(path))[1]

folder_with_slides = path
folders_with_pics = dirs

current_folder = path 
to_folder = []

name = re.compile("^[0-9_]{3,4}\D{5}\d{1,2}[DEde]\d{0,2}")


for folder in folders_with_pics:
  files = os.listdir(current_folder + folder)
  unique_file_names = get_unique_names(files)
  grouped_files = []
  for name in unique_file_names:
    for i, file in enumerate(files):
      file = '10_2fatia1D42_20x01.tif'
      if name in file and name in files[i+1]:
        grouped_files.append(file)
      else:
        grouped_files.append(file)
        # copy_to_folder()
        grouped_files = []
        break







to_folder = []

if len(dirs) > 1:
  print("\nThere are multiple folders in this folder.\nChecking them one by one...")
  for folder in dirs:
    files = os.listdir(path + '\\' + folder)
    current_folder = path + '\\' + folder
    group_files(files, to_folder, current_folder)
    to_folder = []
else:
  print("\nThere are only images in this folder.\nWorking with all of them...")
  files = os.listdir(path)
  current_folder = path
  group_files(files, to_folder, current_folder)
  to_folder = []

print("\nDone!\n:]")

# Listening to: Eyes Without a Face by Billy Idol