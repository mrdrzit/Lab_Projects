import numpy as np
import seaborn as sns
import pandas as pd
import matplotlib.image as mpimg
from matplotlib import pyplot as plt

plt.rcParams["axes.facecolor"] = "black"
plt.rcParams["figure.facecolor"] = "black"

animal = [
    r"D:\Documents\Deeplabcut\Comportamento_social_Leo_Pilocarpina\1.csv",
    r"D:\Documents\Deeplabcut\Comportamento_social_Leo_Pilocarpina\1-2.csv",
    r"D:\Documents\Deeplabcut\Comportamento_social_Leo_Pilocarpina\2.csv",
    r"D:\Documents\Deeplabcut\Comportamento_social_Leo_Pilocarpina\2-1.csv",
    r"D:\Documents\Deeplabcut\Comportamento_social_Leo_Pilocarpina\3.csv",
]
bg = mpimg.imread(r"D:\Documents\Deeplabcut\Comportamento_social_Leo_Pilocarpina\1 - Copia.png")

# animal.interpolate(method="linear", inplace=True, limit_direction="both")
# x = animal.iloc[0:, 0]
# y = animal.iloc[0:, 1]


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


for file in animal:
    animal = pd.read_csv(file, header=None)
    animal.interpolate(method="linear", inplace=True, limit_direction="both")
    x = animal.iloc[0:, 0]
    y = animal.iloc[0:, 1]

    grid = create_heatmap_grid(x, y)
    alpha = np.zeros(grid.shape) + 0.7
    image_height = 450
    image_width = 446
    max_height = 720
    max_width = 1280
    ratio = min(max_height / image_width, max_width / image_height)
    new_resolution_in_inches = (
        int(image_width * ratio / 100),
        int(image_height * ratio / 100),
    )

    fig, ax = plt.subplots()

    fig.set_size_inches(new_resolution_in_inches)
    ax.imshow(grid, cmap="inferno", alpha=alpha, interpolation="bessel")
    ax.axis("tight")
    ax.axis("off")
    ax.set_title("Overall heatmap of the mice's position in the maze", loc="center")
    ax.set_xlabel("X (pixels)")
    ax.set_ylabel("Y (pixels)")
    ax.set_xticks([])
    ax.set_yticks([])

plt.show()
plt.close("all")
