import numpy as np
import seaborn as sns
import pandas as pd
import matplotlib.image as mpimg
from matplotlib import pyplot as plt

animal_bonsai = pd.read_csv(r"D:\Documents\Deeplabcut\validacao_flavio\m1_1.csv")
animal_dlc = pd.read_csv(r"D:\Documents\Deeplabcut\validacao_flavio\2023-05-30_14-57-53_DLC.csv")
bg = mpimg.imread(r"C:\Users\uzuna\Documents\GITHUB\Collabs\behavython\m1.jpeg")

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

fig, ax = plt.subplots()

ax.plot(raw_ecld_dlc, ".", color="black", alpha=0.2, label="dlc")
ax.plot(raw_ecld_bonsai, ".", color="orange", alpha=0.2, label="bonsai")
ax.set_title("Euclidean distance between consecutive points")
ax.legend()
# sns.regplot(x="bonsai", y="dlc", data=corr_coefs, ax=ax)
plt.show()
pass


xy_values = np.array(list(zip(x_bonsai, y_bonsai)))

# Find the minimum and maximum values of x and y
min_x = min(x_bonsai)
max_x = max(x_bonsai)
min_y = min(y_bonsai)
max_y = max(y_bonsai)

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

pass


def plot_analysis_social_behavior():
    plot_option = True
    image_height = 450
    image_width = 446
    max_height = 720
    max_width = 1280
    # x_collisions = self.analysis_results["x_data"]
    # y_collisions = self.analysis_results["y_data"]
    # grid = self.analysis_results["grid"]

    fig_1, axe_1 = plt.subplots()
    axe_1.set_title("Overall heatmap of the mice's nose position", loc="center")
    axe_1.set_xlabel("X (pixels)")
    axe_1.set_ylabel("Y (pixels)")
    axe_1.set_xticks([])
    axe_1.set_yticks([])
    ratio = min(max_height / image_width, max_width / image_height)
    # Calculate the new resolution in inches based on the dpi set

    new_resolution_in_inches = (
        int(image_width * ratio / 100),
        int(image_height * ratio / 100),
    )
    # temp = np.multiply(np.sort(sum(self.analysis_results["grid"])), 1 / 30)
    # range_time_each_bin = np.sort(temp).round(decimals=1)
    # ----------------------------------------------------------------------------------------------------------

    if plot_option == 0:
        pass
    else:
        fig_3, axe_3 = plt.subplots()

        # Do i really need to plot this twice?
        sns.kdeplot(
            x=x_bonsai,
            y=y_bonsai,
            fill=True,
            ax=axe_3,
            cbar=False,
            cmap="inferno",
            cbar_kws={
                "label": "Permanence time (s)",
                "location": "right",
                "cbar": True,
            },
            alpha=0.5,
        )
        # Calculate the ratio to be used for image resizing without losing the aspect ratio
        ratio = min(max_height / image_width, max_width / image_height)
        # Calculate the new resolution in inches based on the dpi set
        axe_3.set_title(
            "Exploration map by ROI",
            loc="center",
            fontdict={"fontsize": "large", "fontweight": "normal"},
        )
        fig_3.set_size_inches(new_resolution_in_inches)
        axe_3.axis("off")
        axe_3.axis("tight")
        fig_3.show()

        fig_4, axe_4 = plt.subplots()
        fig_4.show()
        axe_4.imshow(grid, cmap="inferno", interpolation="bessel")
        fig_4.set_size_inches(new_resolution_in_inches)
        axe_4.axis("tight")
        axe_4.axis("off")
        axe_4.set_title("Overall heatmap of the mice's nose position", loc="center")
        axe_4.set_xlabel("X (pixels)")
        axe_4.set_ylabel("Y (pixels)")
        axe_4.set_xticks([])
        axe_4.set_yticks([])

    plt.show()
    pass


plot_analysis_social_behavior()
