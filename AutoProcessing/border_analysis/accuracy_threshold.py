import os
import numpy as np
import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from tqdm import tqdm
from dlc_helper_functions import *
import matplotlib;matplotlib.use('Qt5Agg')

def find_max_and_min(arrays):
    max_value = max([max(array) for array in arrays])
    min_value = min([min(array) for array in arrays])
    return max_value, min_value

print("Loading data files")
data_folder = r"C:\Users\Matheus\Desktop\accuracy_threshold_files"
data = DataFiles()
animals = []
all_results = {}
get_files([], data, animals)
animal_names = [string for string in data.position_files.keys()]
animal_accuracies = {}
accuracy_descriptors = {}
P_THRESOLD = 0.6


for name in animal_names:
    animal_accuracies[name] = {}
    accuracy_descriptors[name] = {}
    position_file = pd.read_csv(
        data.position_files[name],
        sep=",",
        header=[1, 2],
        index_col=0,
        skip_blank_lines=False,
    )
    position_file.columns = pd.MultiIndex.from_frame(position_file.columns.to_frame().map(str.lower))
    bodyparts = position_file.columns.get_level_values(0).unique().tolist()

    for bodypart in bodyparts:
        animal_accuracies[name][bodypart] = {}
        p_values = position_file[bodypart]["likelihood"]
        animal_accuracies[name][bodypart] = p_values
        values_below_threshold = p_values[p_values < P_THRESOLD]
        indices_below_threshold = p_values[p_values < P_THRESOLD].index.tolist()
        percent_below_threshold = (len(values_below_threshold) / len(p_values)) * 100

        accuracy_descriptors[name][bodypart] = {
            "mean": p_values.mean(),
            "std_dev": p_values.std(),
            "max": p_values.max(),
            "min": p_values.min(),
            "values_below_threshold": len(values_below_threshold),
            "indices_below_threshold": indices_below_threshold,
            "percent_below_threshold": percent_below_threshold,
        }

original_cmap = plt.get_cmap('afmhot')
half_cmap = colors.LinearSegmentedColormap.from_list('half_afmhot', original_cmap(np.linspace(0.4, 0.6, 256)))
parts_dict = {"focinho": "Focinho", "orelhae": "Orelha Esquerda", "orelhad": "Orelha Direita", "centro": "Centro", "rabo": "Cauda"}

print("Generating mean and threshold plots")
with tqdm(total=len(animal_names), leave=False) as pbar:
    for animal in animal_accuracies:
        plt.close("all")
        fig, ax = plt.subplots(2, 1, figsize=(6.7, 8.5), sharex=True)
        fig.suptitle(f'Distribution of mean accuracy and percentage below 60% of the confidence', fontsize=12)
        for bodypart in animal_accuracies[animal]:
            percent_below_threshold = [accuracy_descriptors[animal][bodypart]['percent_below_threshold'] for animal in animal_accuracies for bodypart in animal_accuracies[animal]]
            means = [accuracy_descriptors[animal][bodypart]['mean'] for bodypart in animal_accuracies[animal]]
            max_y_accuracy, min_y_accuracy = find_max_and_min([means])
            max_y_percent_below_threshold, min_y_percent_below_threshold = find_max_and_min([percent_below_threshold])

            animal_parts_mean_accuracy = [accuracy_descriptors[animal][bodypart]['mean'] for bodypart in animal_accuracies[animal]]
            animal_parts_percent_below_threshold = [accuracy_descriptors[animal][bodypart]['percent_below_threshold'] for bodypart in animal_accuracies[animal]]

        ax[0].boxplot(np.multiply(animal_parts_mean_accuracy, 100), showfliers=False)
        ax[0].set_title('Mean Accuracy')
        ax[0].set_ylim(min_y_accuracy * 100 - 0.05, max_y_accuracy * 100 + 0.05)
        ax[0].set_ylabel('Accuracy (%)')

        ax[1].boxplot(animal_parts_percent_below_threshold, showfliers=False)
        ax[1].set_title('Percent Below Threshold')
        ax[1].set_ylim(min_y_percent_below_threshold - 0.1, max_y_percent_below_threshold + 0.1)
        ax[1].set_ylabel('Percentage (%)')
        ax[1].set_xlabel(animal)
        ax[1].set_xticklabels([])
        
        fig.set_tight_layout('tight')
        plt.savefig(os.path.join(r"C:\Users\Matheus\Desktop\accuracy_check", f'{animal}_boxplot.png'))
        pbar.update(1)

print("Generating time series plots")
with tqdm(total=len(animal_names), leave=False) as pbar:
    for animal in animal_accuracies:
        fig, ax = plt.subplots(len(bodyparts), 1, figsize=(18, 9.40))
        fig.suptitle(f'{animal} - Accuracy Threshold', fontsize=16)
        for bodypart in animal_accuracies[animal]:
            current_bodypart = animal_accuracies[animal][bodypart]
            current_bodypart_descriptors = accuracy_descriptors[animal][bodypart]
            
            ax[bodyparts.index(bodypart)].plot(current_bodypart, color='black', alpha=0.7)
            ax[bodyparts.index(bodypart)].set_title(f'{parts_dict[bodypart]}')
            ax[bodyparts.index(bodypart)].axhline(P_THRESOLD, color='red', linestyle='dashed', linewidth=1)
            ax[bodyparts.index(bodypart)].set_ylim(0, 1)
            ax[bodyparts.index(bodypart)].plot(current_bodypart_descriptors['indices_below_threshold'], current_bodypart[current_bodypart_descriptors['indices_below_threshold']], 'ro', markersize=2)
            
            ax[bodyparts.index(bodypart)].annotate(f'Mean: {current_bodypart_descriptors["mean"]:.6f}', xy=(1, 0.8), xytext=(1.005, 0.8), textcoords='axes fraction', fontsize=8, horizontalalignment='left')
            ax[bodyparts.index(bodypart)].annotate(f'Std Dev: {current_bodypart_descriptors["std_dev"]:.6f}', xy=(1, 0.7), xytext=(1.005, 0.7), textcoords='axes fraction', fontsize=8, horizontalalignment='left')
            ax[bodyparts.index(bodypart)].annotate(f'Max: {current_bodypart_descriptors["max"]:.6f}', xy=(1, 0.6), xytext=(1.005, 0.6), textcoords='axes fraction', fontsize=8, horizontalalignment='left')
            ax[bodyparts.index(bodypart)].annotate(f'Min: {current_bodypart_descriptors["min"]:.6f}', xy=(1, 0.5), xytext=(1.005, 0.5), textcoords='axes fraction', fontsize=8, horizontalalignment='left')
            ax[bodyparts.index(bodypart)].annotate(f'Values below threshold: {current_bodypart_descriptors["values_below_threshold"]}', xy=(1, 0.4), xytext=(1.005, 0.4), textcoords='axes fraction', fontsize=8, horizontalalignment='left')
            ax[bodyparts.index(bodypart)].annotate(f'Percent below threshold: {current_bodypart_descriptors["percent_below_threshold"]:.2f}%', xy=(1, 0.3), xytext=(1.005, 0.3), textcoords='axes fraction', fontsize=8, horizontalalignment='left')

        fig.set_tight_layout('tight')
        plt.savefig(os.path.join(r"C:\Users\Matheus\Desktop\accuracy_check", f'{animal}_accuracy_analysis.png'))
        plt.close("all")
        pbar.update(1)

