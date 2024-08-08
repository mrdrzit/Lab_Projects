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
for roi, image in zip(roi_borders, images):
    image = skimage.io.imread(image)
    coordinates = pd.read_csv(roi, header=None, delimiter = "\t").values
    roi_polygon = shapely.geometry.Polygon(coordinates)

    roi_border = roi_polygon.buffer(-27)
    
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.imshow(image, cmap='gray')
    plt.show()
    plot_polygon(roi_polygon, ax=ax, color='blue', alpha=0.7, fill=False, linewidth=2) 
    plot_polygon(roi_border, ax=ax, color='red', alpha=0.7, fill=False, linewidth=2)
    fig.set_tight_layout()   
    print(coordinates)

