import pickle
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from pathlib import Path
from tkinter import filedialog
from matplotlib import colors as mcolors
from dlc_helper_functions import *


data_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
pre_processed_data = os.path.join(data_folder, 'animals_data_elisa.pkl')

# Load the animals data from the pickle file
with open(pre_processed_data, 'rb') as file:
    animals_data = pickle.load(file)

print("Data loaded successfully!")