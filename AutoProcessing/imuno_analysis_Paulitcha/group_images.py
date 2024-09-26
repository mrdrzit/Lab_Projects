# Import necessary libraries
import os
import shutil
import tkinter as tk
from tkinter import filedialog
from natsort import os_sorted

def organize_zvi_files():
    def check_if_folder_exists(folder, file_list):
        """
        Checks if a folder exists and creates it if it doesn't

        Input = folder
        """

        if os.path.exists(folder):
            for file in file_list:
                if file in folder:
                    return False
        else:
            return True


    # Define a regular expression for extracting unique names from file names
    def get_unique_names(file_list):
        """
        Returns a list of unique names from a list of files

        Input = list of files, regex
        """
        file_list = list(dict.fromkeys(file_list))
        unique_names = {"right_hemisphere": [], "left_hemisphere": []}
        for file in file_list:
            if " " in file:
                exit("[ERROR] There are files with spaces in the folder, please rename them and try again or sort them manually")
            hemisphere = file[-9:]
            if not file.endswith(".zvi"):
                exit("There are files that are not .zvi files in the folder")
            if "D" in hemisphere:
                unique_names["right_hemisphere"].append(file)
            elif "E" in hemisphere:
                unique_names["left_hemisphere"].append(file)

        unique_names["right_hemisphere"] = os_sorted(unique_names["right_hemisphere"])
        unique_names["left_hemisphere"] = os_sorted(unique_names["left_hemisphere"])
        return unique_names


    # Copy a list of files to a destination folder
    def copy_to_folder(grouped_files, dest_folder):
        """
        Copies a list of files to a destination folder

        Input = list of files, destination folder
        """
        for file in grouped_files:
            shutil.copy(file, dest_folder)


    # Group files based on a specific naming pattern and copy them to corresponding folders
    def group_files(folder_with_pics, pics):

        # Get unique names from the list of file names and sort them
        unique_file_names = get_unique_names(pics)

        for key in unique_file_names.keys():
            print("Grouping files for " + key)
            print("Putting files in " + folder_with_pics + key)

            folder_to_save_to = os.path.join(folder_with_pics, key)

            # Check if the folder exists and create it if it doesn't
            if not check_if_folder_exists(folder_to_save_to, pics):
                exit("[ERROR] The folder " + folder + " already exists, and contains files that are to be copied\nPlease move and try again")
            else:
                # Make directory and copy the files to the corresponding folder
                os.makedirs(folder_to_save_to)
                file_list_to_copy = [os.path.join(folder_with_pics, file) for file in unique_file_names[key]]
                copy_to_folder(file_list_to_copy, folder_to_save_to)

    # Set up a Tkinter file explorer
    file_explorer = tk.Tk()
    file_explorer.withdraw()
    file_explorer.call("wm", "attributes", ".", "-topmost", True)

    # Ask user to select a folder using the file explorer
    path = filedialog.askdirectory(title="Select the folder", mustexist=True).replace("/", "\\") + "\\"

    # List directories in the selected folder
    dirs = os_sorted([file for file in os.listdir(path) if os.path.isfile(os.path.join(path, file))])


    # Check if there are subdirectories in the selected folder
    there_is_folder = False
    for dir in dirs:
        if os.path.isdir(os.path.join(path, dir)):
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
            group_files(os.path.join(path, dirs[i], folder))
    else:
        group_files(path, pics)

    # Display completion message
    print("\nDone!\n:]\n")

    # Prompt user to press Enter to exit
    enter = input("Press enter to exit")
    if enter or enter == "":
        exit()

    # Listening to: Eyes Without a Face by Billy Idol
