import pickle
import os
import numpy as np
import matplotlib.pyplot as plt
import math
import seaborn as sns
import scipy.stats as stats
from helper_functions import *

# Set the path to the data folder and the pre-processed data file
data_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
figures_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'figures'))
pre_processed_data = os.path.join(data_folder, 'animals_data_elisa.pkl')


# Load the animals data from the pickle file
with open(pre_processed_data, 'rb') as file:
    animals_data = pickle.load(file)
print("Data loaded successfully!")

# Get the maximum exploration bout duration overall
max_duration = 0
for session in animals_data.keys():
    for animal in animals_data[session].keys():
        max_duration = max(max_duration, max(animals_data[session][animal]) if len(animals_data[session][animal]) > max_duration else max_duration)

# Set the bin size for the histograms
bins = np.arange(0, math.ceil(max_duration), 0.5)

paired_data = []
paired_cdf = []
paired_bins = []

treino, reativacao, teste = list(animals_data.keys())

for animal_tr, animal_re, animal_tt in zip(animals_data[treino], animals_data[reativacao], animals_data[teste]):
    paired_data.append([animals_data[treino][animal_tr], animals_data[reativacao][animal_re], animals_data[teste][animal_tt]])
    paired_cdf.append([cumulative_distribution(animals_data[treino][animal_tr]), cumulative_distribution(animals_data[reativacao][animal_re]), cumulative_distribution(animals_data[teste][animal_tt])])
    paired_bins.append([np.histogram(animals_data[treino][animal_tr], bins=bins)[0], np.histogram(animals_data[reativacao][animal_re], bins=bins)[0], np.histogram(animals_data[teste][animal_tt], bins=bins)[0]])

# Set the colors for each experiment day
TR_color = '#b57ecb'
RE_color = '#5b9999'
TT_color = '#E45C5C'

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

# Plot the cdfs for each session
fig, ax = plt.subplots(figsize=(15, 8))
plt.plot(values_TR, cdf_TR, label="TR", color=TR_color)
plt.plot(values_RE, cdf_RE, label="RE", color=RE_color)
plt.plot(values_TT, cdf_TT, label="TT", color=TT_color)
plt.legend()
plt.xlabel('Duration (s)', fontsize=12)
plt.ylabel('Cumulative Probability', fontsize=12)
plt.grid()
plt.title('Bout Durations for every animal in each session (TR, RE, TT)')
plt.tight_layout()

# Find the maximum length
max_len = max(len(TR_durations), len(RE_durations), len(TT_durations))

# Pad the arrays with zeros
TR_durations_homogenous = np.pad(TR_durations, (0, max_len - len(TR_durations)), 'constant')
RE_durations_homogenous = np.pad(RE_durations, (0, max_len - len(RE_durations)), 'constant')
TT_durations_homogenous = np.pad(TT_durations, (0, max_len - len(TT_durations)), 'constant')

data = np.array((TR_durations_homogenous, RE_durations_homogenous, TT_durations_homogenous))
data_dataframe = pd.DataFrame(data.T, columns=["TR", "RE", "TT"])
data_dataframe["TR"] = data_dataframe["TR"]
data_dataframe["RE"] = data_dataframe["RE"]
data_dataframe["TT"] = data_dataframe["TT"]

kernel_tr = stats.gaussian_kde(data_dataframe["TR"])
kernel_re = stats.gaussian_kde(data_dataframe["RE"])
kernel_tt = stats.gaussian_kde(data_dataframe["TT"])

kt = kernel_tr.pdf(data_dataframe["TR"])

# Plot the kde for each session
fig, ax = plt.subplots(figsize=(15, 8))
ax.plot(kt, range(len(kt)), label="TR", color=TR_color)

fig, ax = plt.subplots(figsize=(15, 8))
sns.kdeplot(
    data=data_dataframe,
    ax=ax,
    palette=[TR_color, RE_color, TT_color],
    fill=True,
    alpha=0.8,
    linewidth=0.5,
    multiple="stack",
    edgecolor="white",
)
ax.set_xlabel("Duration (s)", fontsize=12)
ax.set_ylabel("Density", fontsize=12)
ax.set_title("Normalized KDE for Bout Durations (TR, RE, TT)", fontsize=14)
plt.tight_layout()

# Add legend
ax.legend()

fig, axes = plt.subplots(1, 3, sharex=True, sharey=True, figsize=(15, 8))
axes[0].hist(TR_durations, bins=bins, color=TR_color, alpha=0.7, label='TR')
axes[1].hist(RE_durations, bins=bins, color=RE_color, alpha=0.7, label='RE')
axes[2].hist(TT_durations, bins=bins, color=TT_color, alpha=0.7, label='TT')

axes[0].axvline(np.mean(TR_durations), color='k', linestyle='dashed', linewidth=1, label='TR Mean')
axes[1].axvline(np.mean(RE_durations), color='k', linestyle='dashed', linewidth=1, label='RE Mean')
axes[2].axvline(np.mean(TT_durations), color='k', linestyle='dashed', linewidth=1, label='TT Mean')
for ax in axes:
    ax.legend()
    ax.set_xlabel('Duration (s)')
    ax.set_ylabel('Frequency')
    ax.grid()

plt.title('Bout Durations for every animal in each session (TR, RE, TT)')
plt.tight_layout()

# plt.hist(TR_durations, bins=bins, density=True, color=TR_color, alpha=0.1, label='TR')
# plt.hist(RE_durations, bins=bins, density=True, color=RE_color, alpha=0.1, label='RE')
# plt.hist(TT_durations, bins=bins, density=True, color=TT_color, alpha=0.1, label='TT')
# plt.legend()
# plt.xlabel('Duration (s)')
# plt.ylabel('Frequency')
# plt.title('Bout Durations')

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

# Plot the cdfs for each animal through the experiment days
for animal in range(len(paired_data)):
    fig, ax = plt.subplots(figsize=(15, 8))
    plt.plot(paired_cdf[animal][0][0], paired_cdf[animal][0][1], label="TR", color=TR_color)
    plt.plot(paired_cdf[animal][1][0], paired_cdf[animal][1][1], label="RE", color=RE_color)
    plt.plot(paired_cdf[animal][2][0], paired_cdf[animal][2][1], label="TT", color=TT_color)
    plt.legend()
    plt.xlabel('Duration (s)', fontsize=12)
    plt.ylabel('Cumulative Probability', fontsize=12)
    plt.grid()
    plt.title(f'Cumulative Distribution Function for Animal {list(animals_data["treino"].keys())[animal].replace("TR", "")} in each session')
    plt.tight_layout()
    plt.savefig(os.path.join(figures_folder, f'animal_{list(animals_data["treino"].keys())[animal].replace("TR", "")}_cdfs.png'))