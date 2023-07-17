import numpy as np
import seaborn as sns
import pandas as pd
import matplotlib.image as mpimg
from matplotlib import pyplot as plt

animal_bonsai = pd.read_csv(r"D:\Documents\Deeplabcut\validacao_flavio\2023-05-30_14-57-53.csv")
# animal_bonsai = pd.read_csv(r"D:\Documents\Deeplabcut\validacao_flavio\2023-05-30_14-57-53_2_bonsai.csv")
animal_dlc = pd.read_csv(r"D:\Documents\Deeplabcut\validacao_flavio\2023-05-30_14-57-53_DLC.csv")
bg = mpimg.imread(r"D:\Documents\Deeplabcut\validacao_flavio\m1.jpeg")

x_bonsai = animal_bonsai["y"]
y_bonsai = animal_bonsai["x"]

x_dlc = animal_dlc["x"]
y_dlc = animal_dlc["y"]

dist_x = np.diff(x_dlc)
dist_y = np.diff(y_dlc)
dist_x_dlc = np.diff(x_bonsai)
dist_y_dlc = np.diff(y_bonsai)

raw_ecld_bonsai = []
raw_ecld_dlc = []

# raw euclidean distance between the two datasets
for i in range(len(x_bonsai)):
    raw_ecld_bonsai.append(np.sqrt((dist_x[i - 1] ** 2) + (dist_y[i - 1] ** 2)))
    raw_ecld_dlc.append(np.sqrt((dist_x_dlc[i - 1] ** 2) + (dist_y_dlc[i - 1] ** 2)))

corr = pd.DataFrame(list(zip(raw_ecld_bonsai, raw_ecld_dlc)), columns=["bonsai", "dlc"])
corr_coefs = corr.corr(method="pearson")

# fig, ax = plt.subplots()
# ax.plot(raw_ecld_dlc, ".", color="black", alpha=0.2, label="dlc")
# ax.plot(raw_ecld_bonsai, ".", color="orange", alpha=0.2, label="bonsai")
# ax.set_title("Euclidean distance between consecutive points")
# ax.legend()

pass


def create_heatmap_grid(x_values, y_values):
    xy_values = np.array(list(zip(x_values, y_values)))

    # Find the minimum and maximum values of x and y
    min_x = min(x_values)
    max_x = max(x_values)
    min_y = min(y_values)
    max_y = max(y_values)

    bin_size = 10

    # Calculate the number of bins in each dimension
    num_bins_x = int((max_x - min_x) / bin_size) + 1
    num_bins_y = int((max_y - min_y) / bin_size) + 1

    # Create a grid to store the frequencies
    grid = np.zeros((num_bins_y, num_bins_x), dtype=int)

    # Assign the values to their corresponding bins in the grid
    for xy in xy_values:
        xi, yi = xy
        bin_x = (xi - min_x) // bin_size
        bin_y = (yi - min_y) // bin_size
        grid[int(bin_y), int(bin_x)] += 1  # Increment the frequency of the corresponding bin

    return grid


def plot_analysis_social_behavior():
    grid_bonsai = create_heatmap_grid(x_bonsai, y_bonsai)
    grid_dlc = create_heatmap_grid(x_dlc, y_dlc)
    image_height = 450
    image_width = 446
    max_height = 720
    max_width = 1280
    ratio = min(max_height / image_width, max_width / image_height)
    new_resolution_in_inches = (
        int(image_width * ratio / 100),
        int(image_height * ratio / 100),
    )

    fig, ax = plt.subplot_mosaic(
        [["bonsai", "dlc"]],
        layout="constrained",
        sharex=True,
        sharey=True,
    )
    fig.set_size_inches(new_resolution_in_inches)
    ax["dlc"].imshow(grid_dlc, cmap="inferno", interpolation="bessel")
    ax["dlc"].axis("tight")
    ax["dlc"].axis("off")
    ax["dlc"].set_title("Overall heatmap of the mice's nose position from Diliça", loc="center")
    ax["dlc"].set_xlabel("X (pixels)")
    ax["dlc"].set_ylabel("Y (pixels)")
    ax["dlc"].set_xticks([])
    ax["dlc"].set_yticks([])
    ax["bonsai"].imshow(grid_bonsai, cmap="inferno", interpolation="bessel")
    ax["bonsai"].axis("tight")
    ax["bonsai"].axis("off")
    ax["bonsai"].set_title("Overall heatmap of the mice's nose position from Bonsai", loc="center")
    ax["bonsai"].set_xlabel("X (pixels)")
    ax["bonsai"].set_ylabel("Y (pixels)")
    ax["bonsai"].set_xticks([])
    ax["bonsai"].set_yticks([])

    plt.show()
    plt.close("all")
    pass


plot_analysis_social_behavior()
