import pandas as pd
import skimage
import shapely
import os
import matplotlib
import matplotlib.pyplot as plt
from shapely.plotting import plot_polygon
from dlc_helper_functions import *

matplotlib.use('TkAgg')

data_folder = "C:\\Users\\Matheus\\Desktop\\border_test"
roi_borders = [os.path.join(data_folder, file) for file in os.listdir(data_folder) if file.endswith(".txt") and ("_border_roi" in file)]
images = [os.path.join(data_folder, file) for file in os.listdir(data_folder) if file.endswith(".jpg")]
mouse_width_px = 27

for roi, image in zip(roi_borders, images):
    image = skimage.io.imread(image)
    # Read the coordinates from the ROI file
    arbitrary_coordinates = pd.read_csv(roi, header=None, delimiter="\t").values

    # Convert the coordinates to a list of tuples
    coordinates = list(zip(arbitrary_coordinates[:, 0], arbitrary_coordinates[:, 1]))

    # Create the arbitrary polygon
    arbitrary_polygon = shapely.geometry.Polygon(coordinates)

    # Create the buffered (inside border) polygon
    buffered_polygon = arbitrary_polygon.buffer(-mouse_width_px)
    buffered_coordinates = list(buffered_polygon.exterior.coords)

    # Create the ARBITRARY_ROI and FULL_ARBITRARY_ROI polygons
    ARBITRARY_ROI = shapely.geometry.Polygon(coordinates, [buffered_coordinates])
    FULL_ARBITRARY_ROI = arbitrary_polygon
    
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.imshow(image, cmap='gray')
    plot_polygon(ARBITRARY_ROI, ax=ax, color='blue', alpha=0.7, fill=False, linewidth=2) 
    plt.show()

