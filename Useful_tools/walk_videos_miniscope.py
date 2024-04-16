import os
import itertools
import tkinter as tk
from tkinter import filedialog
from pathlib import Path

def walk_videos_miniscope(root_dir):
    """
    Walks through the root directory and returns a list of all the miniscope videos

    Parameters
    ----------
    root_dir : str
        The root directory to walk through
    
    Returns
    -------
    videos : list
        A list of all the miniscope videos in the root directory

    """
    # Initialize an empty list to store the videos
    videos = []
    
    # Walk through the root directory and all its subdirectories
    for root, dirs, files in os.walk(root_dir):
        # Get all the files that end with .avi
        videos.extend([os.path.join(root, f) for f in files if f.endswith('.mp4')])
    
    # Return the list of videos
    return videos
    

root = tk.Tk()
root.attributes('-topmost', True)
root.withdraw()
current_path = Path(filedialog.askdirectory(title="Choose the folder containing only the video files to be processed."))

videos = walk_videos_miniscope(current_path)
print(videos)