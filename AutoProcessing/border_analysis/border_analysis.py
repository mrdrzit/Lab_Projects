import pandas as pd
import skimage
import shapely
from dlc_helper_functions import *


analysis_dir = str(Path(filedialog.askdirectory(title="Select the analysis folder", mustexist=True)))
folders_to_process = []
print(f"Looking through the folders in {analysis_dir}")
for root, dirs, files in os.walk(analysis_dir):
    if not files:
        continue
    elif "data" in dirs:
        if os.listdir(os.path.join(root, "data")) != []:
            file_list_in_data = [file for file in os.listdir(os.path.join(root, "data")) if not file.endswith(".xlsx")]
            image_list_in_parent = [file for file in os.listdir(root) if file.endswith(".jpg")]
            if len(file_list_in_data) == len(image_list_in_parent):
                print(f"[WARNING]: The folder {root} has already been processed.")
                continue
            else:
                folders_to_process.append(root)
        else:
            folders_to_process.append(root)
    elif "data" in root:
        continue
    else:
        folders_to_process.append(root)

print(f"Found {len(folders_to_process)} folders with data to analyze")
for i, folder in enumerate(folders_to_process):
    files_to_analyze = [os.path.join(folder, file) for file in os.listdir(folder) if "data" not in file]
    save_dir = os.path.join(folder, "data")
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)


data = DataFiles()
animals = []
all_results = {}
print(f"Organizing files to analyze. This takes a second...")
get_files([], data, animals, files_to_analyze)
print(f"Files organized. Starting analysis...")
mouse_width_px = 27
runtime = 300
framerate = 30
images = [os.path.join(folder, file) for file in data.experiment_images.values()]
roi_files = [os.path.join(folder, file) for file in os.listdir(folder) if "border_roi" in file]

for image, roi_file, animal in zip(images, roi_files, animals):
    no_points_in_border = False
    no_points_in_center = False
    border_roi = pd.read_csv(roi_file, sep=",")
    last_frame = skimage.color.rgb2gray(skimage.io.imread(image))
    image_height, image_width = last_frame.shape
    width = border_roi['Width'][0]
    height = border_roi['Height'][0]
    top_left = (border_roi['BX'][0], border_roi['BY'][0])
    top_right = (top_left[0] + width, top_left[1])
    bottom_left = (top_left[0], top_left[1] + height)
    bottom_right = (top_right[0], bottom_left[1])
    mouse_center_x = animal.bodyparts['centro']['x'][0:runtime * framerate]
    mouse_center_y = animal.bodyparts['centro']['y'][0:runtime * framerate]
    mouse_center_pos_shapely = []

    for point in zip(mouse_center_x, mouse_center_y):
        pnt = shapely.geometry.Point(point)
        mouse_center_pos_shapely.append(pnt)

    internal_top_left = (border_roi['BX'][0] + mouse_width_px, border_roi['BY'][0] + mouse_width_px)
    internal_top_right = ((internal_top_left[0] + width) - (2 * mouse_width_px), internal_top_left[1])
    internal_bottom_left = (internal_top_left[0], (internal_top_left[1] + height) - (2 * mouse_width_px))
    internal_bottom_right = (internal_top_right[0], internal_bottom_left[1])

    bouding_box_exterior = [top_left, top_right, bottom_right, bottom_left]
    bouding_box_interior = [internal_top_left, internal_top_right, internal_bottom_right, internal_bottom_left]

    ROI = shapely.geometry.Polygon(bouding_box_exterior, [bouding_box_interior])
    full_arena_ROI = shapely.geometry.Polygon(bouding_box_exterior)