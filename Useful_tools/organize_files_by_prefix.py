import os
import shutil

def organize_files(source_dir):
    # Change to the source directory
    os.chdir(source_dir)

    # List all files in the directory
    files = os.listdir()

    for filename in files:
        # Extract the part of the filename to create a folder
        folder_name = filename.split('.')[0]

        # Create the folder if it doesn't exist
        folder_path = os.path.join(source_dir, folder_name)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        # Move the file to the corresponding folder
        source_file = os.path.join(source_dir, filename)
        destination_file = os.path.join(folder_path, filename)
        shutil.move(source_file, destination_file)

if __name__ == "__main__":
    source_directory = r'F:\Matheus\Bonsai\UFAL\CONVERTED_FROM_DAV\LCE\LCE_MACHOS_21.06.23'  # Change this to your source directory
    organize_files(source_directory)
