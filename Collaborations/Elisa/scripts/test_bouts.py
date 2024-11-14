import re
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import re
from pathlib import Path
from tkinter import filedialog
from matplotlib import colors as mcolors
from dlc_helper_functions import *

plt.ioff()

INTERACTIVE = True
save_fig = True
if INTERACTIVE:
    file_explorer = tk.Tk()
    file_explorer.withdraw()
    file_explorer.call("wm", "attributes", ".", "-topmost", True)
    figures_folder = str(Path(filedialog.askdirectory(title="Select the folder to save the plots", mustexist=True)))

data = DataFiles()
animals = []
all_results = {}
get_files([], data, animals)


for animal in animals:
    collision_data = []
    dimensions = animal.exp_dimensions()
    focinho_x = animal.bodyparts["focinho"]["x"]
    focinho_y = animal.bodyparts["focinho"]["y"]
    orelha_esq_x = animal.bodyparts["orelhae"]["x"]
    orelha_esq_y = animal.bodyparts["orelhae"]["y"]
    orelha_dir_x = animal.bodyparts["orelhad"]["x"]
    orelha_dir_y = animal.bodyparts["orelhad"]["y"]
    centro_x = animal.bodyparts["centro"]["x"]
    centro_y = animal.bodyparts["centro"]["y"]
    roi_X = []
    roi_Y = []
    roi_D = []
    roi_NAME = []
    roi_regex = re.compile(r"\\([^\\]+)\.")
    number_of_filled_rois = sum(1 for roi in animal.rois if roi["x"])
    for i in range(number_of_filled_rois):
        # Finds the name of the roi in the file name
        roi_name = Path(animal.rois[i]["file"]).stem.split("_")[0]
        roi_NAME.append(roi_name)
        roi_X.append(animal.rois[i]["x"])
        roi_Y.append(animal.rois[i]["y"])
        roi_D.append((animal.rois[i]["width"] + animal.rois[i]["height"]) / 2)
    # ---------------------------------------------------------------

    # General data
    arena_width = 30
    arena_height = 30
    frames_per_second = 30
    max_analysis_time = 300
    threshold = 0.0267
    # Maximum video height set by user
    # (height is stored in the first element of the list and is converted to int beacuse it comes as a string)
    max_video_height = 1920
    max_video_width = 1080
    plot_options = True
    trim_amount = 0
    video_height, video_width, _ = dimensions
    factor_width = arena_width / video_width
    factor_height = arena_height / video_height
    number_of_frames = animal.exp_length()
    bin_size = 10
    # ----------------------------------------------------------------------------------------------------------

    runtime = range(int(max_analysis_time * frames_per_second))

    # Try to clean the animal name from the date and time timestamp
    clean_animal_name = None
    date_time_timestamp_regex = re.compile(r"\d{4}-\d{2}-\d{2} \d{2}-\d{2}-\d{2}")
    try:
        date_time_timestamp = date_time_timestamp_regex.search(animal.name).group(0)
        # Replace the date and time timestamp with the an empty string
        # Replace all remaining underscores, spcaces and dashes with a single underscore
        new_key = re.sub(r"\d{4}-\d{2}-\d{2} \d{2}-\d{2}-\d{2}", "", animal.name)
        new_key = re.sub(r"[_\s-]+", "_", new_key)
        clean_animal_name = new_key
    except:
        print(f"Could not find the date and time timestamp for the animal {animal.name}")
        print("Using the complete animal name instead.")
        clean_animal_name = animal.name

    for i in runtime:
        # Calculate the area of the mice's head
        Side1 = np.sqrt(((orelha_esq_x[i] - focinho_x[i]) ** 2) + ((orelha_esq_y[i] - focinho_y[i]) ** 2))
        Side2 = np.sqrt(((orelha_dir_x[i] - orelha_esq_x[i]) ** 2) + ((orelha_dir_y[i] - orelha_esq_y[i]) ** 2))
        Side3 = np.sqrt(((focinho_x[i] - orelha_dir_x[i]) ** 2) + ((focinho_y[i] - orelha_dir_y[i]) ** 2))
        S = (Side1 + Side2 + Side3) / 2
        mice_head_area = np.sqrt(S * (S - Side1) * (S - Side2) * (S - Side3))
        # ------------------------------------------------------------------------------------------------------

        # Calculate the exploration threshold in front of the mice's nose
        A = np.array([focinho_x[i], focinho_y[i]])
        B = np.array([orelha_esq_x[i], orelha_esq_y[i]])
        C = np.array([orelha_dir_x[i], orelha_dir_y[i]])
        P, Q = line_trough_triangle_vertex(A, B, C)
        # ------------------------------------------------------------------------------------------------------

        # Calculate the collisions between the ROI and the mice's nose
        for ii in range(number_of_filled_rois):
            collision = detect_collision([Q[0], Q[1]], [P[0], P[1]], [roi_X[ii], roi_Y[ii]], roi_D[ii] / 2)
            if collision:
                collision_data.append([1, collision, mice_head_area, roi_NAME[ii]])
            else:
                collision_data.append([0, None, mice_head_area, None])

    # ----------------------------------------------------------------------------------------------------------
    corrected_runtime_last_frame = runtime[-1] + 1
    corrected_first_frame = runtime[1] - 1
    ANALYSIS_RANGE = [corrected_first_frame, corrected_runtime_last_frame]
    # ----------------------------------------------------------------------------------------------------------
    ## TODO: #43 If there is no collision, the collision_data will be empty and the code will break. Throw an error and print a message to the user explaining what is a collision.
    collisions = pd.DataFrame(collision_data)
    xy_data = collisions[1].dropna()

    # Calculate the total exploration time
    exploration_mask = collisions[0] > 0
    exploration_mask = exploration_mask.astype(int)
    exploration_time = np.sum(exploration_mask) * (1 / frames_per_second)

    # get sections
    exploration_bouts = find_sections(collisions, frames_per_second)
    exploration_bouts = exploration_bouts[exploration_bouts["duration"] > (1 / frames_per_second) * 2].reset_index(drop=True)

    # Save excel file with the exploration bouts
    exploration_bouts_sec = exploration_bouts.copy(deep=True)
    exploration_bouts_sec["start"] = exploration_bouts_sec["start"] / frames_per_second
    exploration_bouts_sec["end"] = exploration_bouts_sec["end"] / frames_per_second
    exploration_bouts_sec = exploration_bouts_sec.astype(float).round(2)
    exploration_bouts_sec = exploration_bouts_sec.rename(columns={"start": "start (s)", "end": "end (s)", "duration": "duration (s)"})
    print(f"Saving the exploration bouts data for {clean_animal_name}...")
    exploration_bouts_sec.to_excel(os.path.join(figures_folder, f"{clean_animal_name}_exploration_bouts.xlsx"))
    durations = np.array(exploration_bouts["duration"])

    # Normalize durations and map to colors
    cmap = plt.get_cmap("afmhot")
    half_cmap = mcolors.LinearSegmentedColormap.from_list(f"half_{cmap.name}", cmap(np.linspace(0.1, 0.5, 256)))
    norm = mcolors.Normalize(vmin=durations.min(), vmax=durations.max(), clip=True)
    mapper = cm.ScalarMappable(norm=norm, cmap=half_cmap)
    colors = [mapper.to_rgba(duration) for duration in durations]
    x_positions = np.linspace(0, len(runtime) / frames_per_second, len(runtime))

    # Create the event plot
    # sns.set_style('darkgrid')
    # plt.style.use("dark_background")

    fig, ax = plt.subplots(2, 2, figsize=(15, 7.5), gridspec_kw={"width_ratios": [1, 0.025]})
    [axi[1].set_axis_off() for axi in ax]
    plt.subplots_adjust(wspace=0.1, hspace=1)

    # Calculate the center positions for each line
    mid_points = [(start + end) / 2 for start, end in zip(exploration_bouts["start"], exploration_bouts["end"])]

    # Create horizontal event lines at y positions [0, 1, 2, ..., len(durations)-1]
    y_offset = 0
    positions = np.zeros(len(durations)) + y_offset
    lengths = np.array(durations)[:, np.newaxis]
    transposed_positions = (np.array(positions)[:, np.newaxis]) / frames_per_second
    transposed_mid_points = np.array(mid_points)[:, np.newaxis] / frames_per_second
    x_points_sec = len(x_positions) / frames_per_second

    # with plt.style.use("dark_background"):
    # Plot event lines
    ax[0][0].eventplot(transposed_mid_points, orientation="horizontal", colors="k", lineoffsets=transposed_positions, linelengths=durations)
    ax[0][0].set_xlim(0, x_points_sec)
    ax[0][0].set_ylim(y_offset - max(durations), y_offset + max(durations))
    ax[0][0].set_xlabel("Time (s)")
    ax[0][0].legend(["Exploration bouts"], loc="upper right", prop={"size": 6})
    ax[0][0].set_title(f"Duration mapped by size")

    ax[1][0].eventplot(transposed_mid_points, orientation="horizontal", colors=colors, lineoffsets=transposed_positions, linelengths=max(durations), linewidths=durations)
    ax[1][0].set_xlim(0, x_points_sec)
    ax[1][0].set_ylim(y_offset - max(durations), y_offset + max(durations))
    ax[1][0].set_xlabel("Time (s)")
    ax[1][0].legend(["Exploration bouts"], loc="upper right", prop={"size": 6})
    ax[1][0].set_title(f"Duration mapped by color and linewidth")

    for axi in [ax[1]]:
        cbar = fig.colorbar(mapper, ax=axi[1], location="right", ticks=np.around(np.linspace(0, max(durations), 6), 1))
        cbar.set_label("Duration (s)")
    [ax[0].set_yticks([]) for ax in ax]
    fig.text(0.10, 0.5, f"Exploration bouts for animal {clean_animal_name}", va="center", rotation="vertical", fontsize=14)
    # fig.tight_layout()
    # plt.pause(10)
    if save_fig:
        print(f"Saving the exploration bouts comparison figure for {animal.name}...")
        fig.savefig(os.path.join(figures_folder, f"{clean_animal_name}_exploration_bouts.png"))

    fig, ax = plt.subplots(figsize=(13, 4))
    unique, counts = np.unique(np.round(durations, decimals=1), return_counts=True)
    histogram_values = dict(zip(unique, counts))
    positions = range(len(unique))
    xticklabels = [str(val) for val in unique]
    ax.set_axisbelow(True)
    ax.grid(color="gray", linestyle="dashed", alpha=0.2, zorder=0)
    ax.bar(positions, counts, color="r", alpha=0.5, zorder=3)
    ax.set_title(f"Exploration bout duration histogram for animal {clean_animal_name}")
    ax.set_xlabel("Duration (s)")
    ax.set_ylabel("Frequency")
    ax.set_xticks(positions)
    ax.set_xticklabels(xticklabels, rotation=60)
    fig.tight_layout()
    if save_fig:
        print(f"Saving the exploration bouts histogram for {clean_animal_name}...")
        fig.savefig(os.path.join(figures_folder, f"{clean_animal_name}_exploration_bouts_histogram.png"))

    fig, ax = plt.subplots(figsize=(18, 4))
    ax.plot(x_positions, np.zeros(len(x_positions)), color="k", alpha=0.8, linewidth=10)
    for index, row in exploration_bouts.iterrows():
        ax.plot(
            [row["start"] / 30, row["end"] / 30],
            np.zeros(len([row["start"], row["end"]])),
            color="lightsalmon",
            alpha=0.5,
            linewidth=10,
            label="Exploration bouts" if index == 0 else "",
        )
    ax.set_title(f"Exploration bouts - Time series - Animal {clean_animal_name}")
    ax.set_xlabel("Time (s)")
    ax.set_yticks([0])
    ax.set_yticklabels([animal.name])
    ax.legend()
    fig.tight_layout()
    if save_fig:
        print(f"Saving the exploration bouts time series for {clean_animal_name}...")
        fig.savefig(os.path.join(figures_folder, f"{clean_animal_name}_exploration_bouts_time_series.png"))

    fig, ax = plt.subplots(figsize=(10, 10))
    analysis_runtime = int(max_analysis_time * frames_per_second)
    plt.plot(centro_x.iloc[0:analysis_runtime], centro_y.iloc[0:analysis_runtime], label="x coordinates")
    for _, row in exploration_bouts.iterrows():
        start_idx = row["start"]
        end_idx = row["end"]
        was_inside = False
        for x, y in zip(centro_x[start_idx:end_idx], centro_y[start_idx:end_idx]):
            if is_inside_circle(x, y, roi_X[0], roi_Y[0], roi_D[0]):
                was_inside = True
                break
        if was_inside:
            continue
        plt.plot(centro_x[start_idx:end_idx], centro_y[start_idx:end_idx], color="red", linewidth=2)
    plt.xlabel("X Coordinate")
    plt.ylabel("Y Coordinate")
    plt.title(f"2D Plot of Coordinates with Highlighted Segments for Animal {clean_animal_name}")
    plt.tight_layout()

    if save_fig:
        print(f"Saving the 2D plot of coordinates with highlighted segments for {clean_animal_name}...")
        fig.savefig(os.path.join(figures_folder, f"{clean_animal_name}_2D_plot_of_coordinates_with_highlighted_segments.png"))

    fig, ax = plt.subplots(figsize=(23, 2))
    time_in_seconds = np.arange(0, max_analysis_time, 1 / frames_per_second)
    time_in_seconds = time_in_seconds[: len(centro_x.iloc[0 : max_analysis_time * frames_per_second])]

    plt.plot(time_in_seconds, centro_x.iloc[0 : max_analysis_time * frames_per_second], label="x coordinates", color="b", linewidth=2)
    for _, row in exploration_bouts_sec.iterrows():
        start_time = row["start (s)"]
        end_time = row["end (s)"]
        start_idx = int(start_time * frames_per_second)
        end_idx = int(end_time * frames_per_second)
        plt.plot(time_in_seconds[start_idx:end_idx], centro_x[start_idx:end_idx], color="r", linewidth=2)
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("X Coordinates")
    ax.set_title(f"X Coordinates with Highlighted Segments for Animal {clean_animal_name}")
    fig.tight_layout()

    if save_fig:
        print(f"Saving the X coordinates with highlighted segments for {clean_animal_name}...")
        fig.savefig(os.path.join(figures_folder, f"{clean_animal_name}_X_coordinates_with_highlighted_segments.png"))

    fig, ax = plt.subplots(figsize=(23, 2))
    time_in_seconds = np.arange(0, max_analysis_time, 1 / frames_per_second)
    time_in_seconds = time_in_seconds[: len(centro_y.iloc[0 : max_analysis_time * frames_per_second])]

    plt.plot(time_in_seconds, centro_y.iloc[0 : max_analysis_time * frames_per_second], label="x coordinates", color="b", linewidth=2)
    for _, row in exploration_bouts_sec.iterrows():
        start_time = row["start (s)"]
        end_time = row["end (s)"]
        start_idx = int(start_time * frames_per_second)
        end_idx = int(end_time * frames_per_second)
        plt.plot(time_in_seconds[start_idx:end_idx], centro_y[start_idx:end_idx], color="r", linewidth=2)
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Y Coordinates")
    ax.set_title(f"Y Coordinates with Highlighted Segments for Animal {clean_animal_name}")
    fig.tight_layout()

    if save_fig:
        print(f"Saving the Y coordinates with highlighted segments for {clean_animal_name}...")
        fig.savefig(os.path.join(figures_folder, f"{clean_animal_name}_Y_coordinates_with_highlighted_segments.png"))

    plt.close("all")
    all_results[animal.name] = exploration_bouts_sec

cleaned_results = {}
for key in all_results.keys():
    date_time_timestamp_regex = re.compile(r"\d{4}-\d{2}-\d{2} \d{2}-\d{2}-\d{2}")
    try:
        date_time_timestamp = date_time_timestamp_regex.search(key).group(0)
        # Replace the date and time timestamp with the an empty string
        # Replace all remaining underscores, spcaces and dashes with a single underscore
        new_key = re.sub(r"\d{4}-\d{2}-\d{2} \d{2}-\d{2}-\d{2}", "", key)
        new_key = re.sub(r"[_\s-]+", "_", new_key)
        cleaned_results[new_key] = all_results[key]
    except AttributeError:
        print(f"Could not find the date and time timestamp for the animal {key}")
        print("Using the complete animal name instead.")
        cleaned_results[key] = key

with pd.ExcelWriter(os.path.join(figures_folder, "Combined_results_by_sheet.xlsx"), engine="openpyxl") as writer:
    for animal_name, animal_df in cleaned_results.items():
        animal_df.to_excel(writer, sheet_name=animal_name, index=False)


plt.show()
