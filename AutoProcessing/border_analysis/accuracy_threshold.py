import os
import numpy as np
import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from tqdm import tqdm
from dlc_helper_functions import *
import matplotlib;matplotlib.use('Qt5Agg')

data_folder = r"C:\Users\Matheus\Desktop\accuracy_threshold_files"
data = DataFiles()
animals = []
all_results = {}
get_files([], data, animals)
animal_names = [string for string in data.position_files.keys()]
animal_accuracies = {}
accuracy_descriptors = {}
P_THRESOLD = 0.6

with tqdm(total=len(animal_names), leave=False) as pbar:
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
            animal_accuracies[name][bodypart] = (p_values)
            values_below_threshold = p_values[p_values < P_THRESOLD]
            indices_below_threshold = p_values[p_values < P_THRESOLD].index.tolist()
            percent_below_threshold = (len(values_below_threshold) / len(p_values)) * 100
            third_quartile = np.percentile(p_values, 75)
            first_quartile = np.percentile(p_values, 25)

            accuracy_descriptors[name][bodypart] = {
                "mean": p_values.mean(),
                "std_dev": p_values.std(),
                "max": p_values.max(),
                "min": p_values.min(),
                "values_below_threshold": len(values_below_threshold),
                "indices_below_threshold": indices_below_threshold,
                "percent_below_threshold": percent_below_threshold,
                "first_quartile": first_quartile,
                "third_quartile": third_quartile,
            }
        
    original_cmap = plt.get_cmap('afmhot')
    half_cmap = colors.LinearSegmentedColormap.from_list('half_afmhot', original_cmap(np.linspace(0.4, 0.6, 256)))
    parts_dict = {"focinho": "Focinho", "orelhae": "Orelha Esquerda", "orelhad": "Orelha Direita", "centro": "Centro", "rabo": "Cauda"}

    fig, ax = plt.subplots(len(bodyparts), 1, figsize=(18, 9.40))
    fig.suptitle(f'{name} - Accuracy Threshold', fontsize=16)

    for animal in animal_accuracies:
        for bodypart in animal_accuracies[animal]:
            current_bodypart = animal_accuracies[animal][bodypart]
            current_bodypart_descriptors = accuracy_descriptors[name][bodypart]
            
            ax[bodyparts.index(bodypart)].plot(current_bodypart, color='black', alpha=0.7)
            ax[bodyparts.index(bodypart)].set_title(f'{parts_dict[bodypart]}')
            ax[bodyparts.index(bodypart)].axhline(P_THRESOLD, color='red', linestyle='dashed', linewidth=1)
            ax[bodyparts.index(bodypart)].set_xlim(0, len(current_bodypart))
            ax[bodyparts.index(bodypart)].plot(accuracy_descriptors[name][bodypart]['indices_below_threshold'], current_bodypart[accuracy_descriptors[name][bodypart]['indices_below_threshold']], 'ro', markersize=2)
            
            ax[bodyparts.index(bodypart)].annotate(f'Mean: {current_bodypart_descriptors["mean"]:.6f}', xy=(1, 0.8), xytext=(1.005, 0.8), textcoords='axes fraction', fontsize=8, horizontalalignment='left')
            ax[bodyparts.index(bodypart)].annotate(f'Std Dev: {current_bodypart_descriptors["std_dev"]:.6f}', xy=(1, 0.7), xytext=(1.005, 0.7), textcoords='axes fraction', fontsize=8, horizontalalignment='left')
            ax[bodyparts.index(bodypart)].annotate(f'Max: {current_bodypart_descriptors["max"]:.6f}', xy=(1, 0.6), xytext=(1.005, 0.6), textcoords='axes fraction', fontsize=8, horizontalalignment='left')
            ax[bodyparts.index(bodypart)].annotate(f'Min: {current_bodypart_descriptors["min"]:.6f}', xy=(1, 0.5), xytext=(1.005, 0.5), textcoords='axes fraction', fontsize=8, horizontalalignment='left')
            ax[bodyparts.index(bodypart)].annotate(f'Values below threshold: {current_bodypart_descriptors["values_below_threshold"]}', xy=(1, 0.4), xytext=(1.005, 0.4), textcoords='axes fraction', fontsize=8, horizontalalignment='left')
            ax[bodyparts.index(bodypart)].annotate(f'Percent below threshold: {current_bodypart_descriptors["percent_below_threshold"]:.2f}%', xy=(1, 0.3), xytext=(1.005, 0.3), textcoords='axes fraction', fontsize=8, horizontalalignment='left')
            ax[bodyparts.index(bodypart)].annotate(f'First Quartile: {current_bodypart_descriptors["first_quartile"]:.6f}', xy=(1, 0.2), xytext=(1.005, 0.2), textcoords='axes fraction', fontsize=8, horizontalalignment='left')
    fig.set_tight_layout('tight')
    plt.savefig(os.path.join(r"C:\Users\Matheus\Desktop\accuracy_check", f'{name}_accuracy_analysis.png'))
    plt.close()
    pbar.update(1)