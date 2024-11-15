import pickle
import os
import numpy as np
import matplotlib.pyplot as plt
from helper_functions import *

# Set the path to the data folder and the pre-processed data file
data_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
pre_processed_data = os.path.join(data_folder, 'animals_data_elisa.pkl')

# Load the animals data from the pickle file
with open(pre_processed_data, 'rb') as file:
    animals_data = pickle.load(file)
print("Data loaded successfully!")

# Set the bin size for the histograms
bins = np.arange(0, 5, 0.5)

# Set the colors for each experiment day
TR_color = '#f50707'
RE_color = '#ed5c5c'
TT_color = '#1809eb'

TR_durations = []
RE_durations = []
TT_durations = []

for array in animals_data["treino"].values():
    TR_durations.extend(array)

for array in animals_data["reativacao"].values():
    RE_durations.extend(array)

for array in animals_data["teste"].values():
    TT_durations.extend(array)

# Create histograms for each session
TR_binned = np.histogram(TR_durations, bins=bins)[0]
RE_binned = np.histogram(RE_durations, bins=bins)[0]
TT_binned = np.histogram(TT_durations, bins=bins)[0]

# Calculate the cumulative distribution function for each session
values_TR, cdf_TR = cumulative_distribution(TR_durations)
values_RE, cdf_RE = cumulative_distribution(RE_durations)
values_TT, cdf_TT = cumulative_distribution(TT_durations)

# Plot the cdfs
fig, ax = plt.subplots()
plt.plot(values_TR, cdf_TR, label="TR", color=TR_color)
plt.plot(values_RE, cdf_RE, label="RE", color=RE_color)
plt.plot(values_TT, cdf_TT, label="TT", color=TT_color)
plt.legend()
plt.xlabel('Duration (s)')
plt.ylabel('Cumulative Probability')
plt.title('Bout Durations')
plt.tight_layout()
plt.show()

# Plot the histograms for each session
fig, ax = plt.subplots()
plt.hist(TR_durations, bins=bins, color=TR_color, alpha=0.1, label='TR')
plt.hist(RE_durations, bins=bins, color=RE_color, alpha=0.1, label='RE')
plt.hist(TT_durations, bins=bins, color=TT_color, alpha=0.1, label='TT')
plt.legend()
plt.xlabel('Duration (s)')
plt.ylabel('Frequency')
plt.title('Bout Durations')
plt.show()

# Find bin centers
# This is used to set where the plot bars will be placed. 
# That is, for them to be evenly spaced between the bin edges
bin_centers = (bins[:-1] + bins[1:]) / 2

# Plot the maximum values as a line
fig, ax = plt.subplots()
plt.plot(bin_centers, TR_binned, "--", linewidth=1, label="TR", color=TR_color, alpha=0.9)
plt.plot(bin_centers, RE_binned, "--", linewidth=1, label="RE", color=RE_color, alpha=0.9)
plt.plot(bin_centers, TT_binned, "--", linewidth=1, label="TT", color=TT_color, alpha=0.9)
plt.legend()
plt.xlabel('Duration (s)')
plt.ylabel('Frequency')
plt.title('Bout Durations')
plt.tight_layout()
plt.show()