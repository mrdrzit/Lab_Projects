import os
import re
import shutil
import tkinter as tk
from tkinter import filedialog

# find all files missing the token _20x  = "[^20]{2}(?=x)"
# find all number following the token _20x  = "(?<=_20).{3}"

file_explorer = tk.Tk()
file_explorer.withdraw()
file_explorer.call('wm', 'attributes', '.', '-topmost', True)
path = filedialog.askdirectory(title = "Select the folder", mustexist = True).replace("/", "\\")
dirs = next(os.walk(path))[1]

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