import math
import os
import re
import tkinter as tk
import itertools as it
import matplotlib
import matplotlib.image as mpimg
import pandas as pd
import subprocess
import numpy as np
import json
from pathlib import Path
from tkinter import filedialog

matplotlib.use("qtagg")

def check_roi_files(roi):
    extracted_data = pd.read_csv(roi, sep=",")
    must_have = ["x", "y", "width", "height"]
    header = extracted_data.columns.to_frame().map(str.lower).to_numpy()
    return all(elem in header for elem in must_have)


def create_frequency_grid(x_values, y_values, bin_size, analysis_range, *extra_data):
    """
    Creates a frequency grid based on the given x and y values.

    Args:
        x_values (list): List of x-coordinate values.
        y_values (list): List of y-coordinate values.
        bin_size (float): Size of each bin in the grid.
        analysis_range (tuple): Range of indices to consider for analysis.
        *extra_data: Additional data (e.g., speed, mean_speed).

    Returns:
        numpy.ndarray: The frequency grid.

    """
    if extra_data:
        speed = extra_data[0]
        mean_speed = extra_data[1]

    # Calculate a gridmap with an exploration heatmap
    xy_values = [(int(x_values[i]), int(y_values[i])) for i in range(analysis_range[0], analysis_range[1])]

    # Find the minimum and maximum values of x and y
    min_x = int(min(x_values))
    max_x = int(max(x_values))
    min_y = int(min(y_values))
    max_y = int(max(y_values))

    # Calculate the number of bins in each dimension
    num_bins_x = int((max_x - min_x) / bin_size) + 1
    num_bins_y = int((max_y - min_y) / bin_size) + 1

    # Create a grid to store the frequencies
    grid = np.zeros((num_bins_y, num_bins_x), dtype=int)
    if extra_data:
        # Assign the values to their corresponding bins in the grid
        for ii, xy in enumerate(xy_values):
            xi, yi = xy
            bin_x = (xi - min_x) // bin_size
            bin_y = (yi - min_y) // bin_size
            if speed[ii] > mean_speed:
                grid[bin_y, bin_x] += 1
    else:
        # Assign the values to their corresponding bins in the grid
        for xy in xy_values:
            xi, yi = xy
            bin_x = (xi - min_x) // bin_size
            bin_y = (yi - min_y) // bin_size
            grid[bin_y, bin_x] += 1  # Increment the frequency of the corresponding bin

    return grid

def find_sections(dataframe, framerate):
    in_interval = False
    start_idx = None
    intervals = pd.DataFrame(columns=["start", "end", "duration"])
    for idx, row in dataframe.iterrows():
        value = row[0]
        if value == 1 and not in_interval:
            start_idx = idx
            in_interval = True
        elif value == 0 and in_interval:
            duration = (idx - (start_idx - 1)) * (1 / framerate)
            new_dataframe = pd.DataFrame(data=[[start_idx, idx, duration]], columns=["start", "end", "duration"])
            intervals = pd.concat([intervals, new_dataframe])
            in_interval = False

    if in_interval:
        duration = (idx - (start_idx - 1)) * (1 / framerate)
        intervals = pd.concat([intervals, pd.DataFrame({"start": [start_idx], "end": [idx], "duration": [duration]})], ignore_index=True)
    return intervals


def is_inside_circle(x, y, roi_X, roi_Y, roi_D):
    # Calculate the radius
    radius = roi_D / 2.0

    # Calculate the distance between the point and the circle center
    distance = math.sqrt((x - roi_X) ** 2 + (y - roi_Y) ** 2)

    # Check if the distance is less than or equal to the radius
    return distance <= radius
