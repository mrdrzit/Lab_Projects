import os
import re
import tkinter as tk
import itertools as it
import matplotlib.image as mpimg
import pandas as pd
import skimage
import matplotlib.pyplot as plt
import shapely
import traceback
import matplotlib
from tqdm import tqdm
from pathlib import Path
from shapely.plotting import plot_polygon
from tkinter import filedialog

matplotlib.use("Agg")

class DataFiles:
    """
    This class organizes the files to be analyzed in separate dictionaries for each type of file
    Each dictionary has the animal name as key and the file path as value for each file

    Attributes:
        pos_file (dict): A dictionary containing the position files for each animal
        skeleton_file (dict): A dictionary containing the skeleton files for each animal
        jpg_file (dict): A dictionary containing the jpg files for each animal

    Methods:
        add_pos_file: Adds a position file to the pos_file dictionary
        add_skeleton_file: Adds a skeleton file to the skeleton_file dictionary
        add_jpg_file: Adds a jpg file to the jpg_file dictionary
    """

    def __init__(self):
        self.position_files = {}
        self.skeleton_files = {}
        self.experiment_images = {}
        self.roi_files = {}

    def add_pos_file(self, key, file):
        self.position_files[key] = file

    def add_skeleton_file(self, key, file):
        self.skeleton_files[key] = file

    def add_image_file(self, key, file):
        self.experiment_images[key] = file

    def add_roi_file(self, key, file):
        self.roi_files[key] = file
class Animal:
    """
    Class to store the data for each animal
    The data is separated in bodyparts, skeleton and experiment_jpg where each one is a dictionary
    containing keys that represent the data scheme from the deeplabcut analysis

    Attributes:
        name (str): The name of the animal
        experiment_jpg (str): The path to the experiment jpg file
        bodyparts (dict): A dictionary containing the bodyparts data for each animal
        skeleton (dict): A dictionary containing the skeleton data for each animal

    Methods:
        exp_dimensions: Returns the dimensions of the arena that the experiment was performed in
        exp_length: Returns the length of the experiment
    """

    def __init__(self):
        # Currently the initialization is hardcoding the bodyparts and skeleton names to mirror
        # the ones used in the test data.
        # See the TODO above to add an option to dinamically add bodypart name
        # TODO: Currently the initialization is hardcoding the bodyparts and skeleton names to mirror and throwing a message to the user:
        """
        "Bone {bone} not found in the skeleton file for the animal {self.name}"
        "Please check the name of the bone in the skeleton file"
        "The following bones are available:"
        "focinho_orelhae": [],
        "focinho_orelhad": [],
        "orelhad_orelhae": [],
        "orelhae_orelhad": [],
        "orelhad_centro": [],
        "orelhae_centro": [],
        "centro_rabo": [],
        """
        # This should automatically select the correct bones and assign them to the skeleton dictionary

        self.name = None
        self.animal_jpg = []
        self.position_file = []
        self.skeleton_file = []
        self.rois = [
            {
                "file": [],
                "x": [],
                "y": [],
                "width": [],
                "height": [],
            },
            {
                "file": [],
                "x": [],
                "y": [],
                "width": [],
                "height": [],
            },
            {
                "file": [],
                "x": [],
                "y": [],
                "width": [],
                "height": [],
            },
            {
                "file": [],
                "x": [],
                "y": [],
                "width": [],
                "height": [],
            },
        ]
        self.bodyparts = {
            "focinho": [],
            "orelhad": [],
            "orelhae": [],
            "centro": [],
            "rabo": [],
        }
        self.skeleton = {
            "focinho_orelhae": [],
            "focinho_orelhad": [],
            "orelhad_orelhae": [],
            "orelhae_orelhad": [],
            "orelhad_centro": [],
            "orelhae_centro": [],
            "centro_rabo": [],
        }

    def exp_dimensions(self):
        """
        __exp_dimensions__ Returns the dimensions of the arena that the experiment was performed in

        Args:
            data (DataFiles): DataFiles object containing the image file
            animal_name (str): The name of the animal that the image belongs to

        Returns:
            tuple: A tuple containing the dimensions of the image
        """
        try:
            image = self.animal_jpg
        except FileNotFoundError:
            print("Image file not found in animal object\nWas it loaded properly?\n")
            return None
        return image.shape

    def exp_length(self):
        """
        __exp_length__ Returns the length of the experiment

        Returns:
            int: An int containing the length of the experiment in frames
        """

        return len(self.bodyparts["focinho"]["x"])

    def add_roi(self, roi_file):
        rois = []
        [rois.append(key) for key in roi_file]
        for i, roi_path in enumerate(rois):
            roi_data = pd.read_csv(
                roi_path,
                sep=",",
            )
            self.rois[i]["file"] = roi_path
            self.rois[i]["x"] = roi_data["X"][0]
            self.rois[i]["y"] = roi_data["Y"][0]
            self.rois[i]["width"] = roi_data["Width"][0]
            self.rois[i]["height"] = roi_data["Height"][0]
        pass

    def add_bodypart(self, bodypart):
        """
        add_bodypart gets the data from the csv file and stores it in the bodyparts dictionary.
        Remember that, to extract the data from this csv file, as it has a header with 3 rows,
        the indexing method should be: dataframe.loc[:, ('bodypart', 'axis/likelihood')]

        Args:
            bodypart (str): A string containing the name of the bodypart to be added
            data (DataFiles): A DataFiles object containing the files to be analyzed
            animal_name (str): A string containing the name of the animal to be analyzed
        """
        extracted_data = pd.read_csv(
            self.position_file,
            sep=",",
            header=[1, 2],
            index_col=0,
            skip_blank_lines=False,
        )

        # The following line is necessary to convert the column names to lowercase
        # The data is stored in a MultiIndex dataframe, so the column names are tuples with the bodypart name and the axis/likelihood
        # The following line converts the tuples to lowercase strings
        extracted_data.columns = pd.MultiIndex.from_frame(extracted_data.columns.to_frame().map(str.lower))
        self.bodyparts[bodypart] = {
            "x": extracted_data[bodypart, "x"],
            "y": extracted_data[bodypart, "y"],
            "likelihood": extracted_data[bodypart, "likelihood"],
        }

    def add_experiment_jpg(self, image_file):
        """
        add_experiment_jpg gets the data from the jpg file and stores it in the experiment_jpg attribute.

        Args:
            data (DataFiles): A DataFiles object containing the files to be analyzed
            animal_name (str): A string containing the name of the animal to be analyzed
        """
        try:
            raw_image = mpimg.imread(image_file)
            self.animal_jpg = raw_image
        except KeyError:
            print(f"\nJPG file for the animal {self.name} not found.\nPlease, check if the name of the file is correct.\n")
        return

    def add_position_file(self, position_file):
        """This function adds a reference to the position file to the animal object

        Args:
            position_file (csv): A csv file containing the position data for each bodypart of the animal
        """

        self.position_file = position_file

    def add_skeleton_file(self, skeleton_file):
        """This function adds a reference to the skeleton file to the animal object

        Args:
            skeleton_file (csv): A csv file containing the skeleton data for each bone created for the animal
        """

        self.skeleton_file = skeleton_file

    def get_jpg_dimensions(self):
        """
        get_jpg_dimensions returns the dimensions of the experiment's recording

        Returns:
            tuple: A tuple containing the dimensions of the jpg file
        """
        return self.animal_jpg.shape

def get_unique_names(file_list, regex):
    """
    get_unique_names generates a list of unique names from a list of files

    Args:
        file_list (list): A list of files containing the duplicated names to be reduced to unique names
        regex (object): A regex object to be used to extract the file names from the file list

    Returns:
        list: A list of unique names
    """
    unique_names = []

    for file in file_list:
        file_name = os.path.basename(file)
        if file_name.endswith(".jpg") or file_name.endswith(".png") or file_name.endswith(".jpeg"):
            try:
                unique_names.append(regex.search(file_name).group(0))
            except AttributeError:
                print(f"'{file_name}' not recognized")
                pass
        elif file_name.endswith(".csv"):
            try:
                unique_names.append(regex.search(file_name).group(0))
            except AttributeError:
                pass

    names = list(dict.fromkeys(unique_names))

    return names

def get_files(line_edit, data: DataFiles, animal_list: list, *args):
    """
    get_files organizes que files to be analyzed in separate dictionaries for each type of file
    where each dictionary has the animal name as key and the file path as value for each file

    Args:
        data (DataFiles): A DataFiles object to store the files in an organized way
        animal_list (list): An empty list of animal objects to be filled with the data from the files

    Returns:
        None: The function does not return anything, but it fills the data and animal_list objects
    """
    if args:
        data_files = args[0]
    else:
        file_explorer = tk.Tk()
        file_explorer.withdraw()
        file_explorer.call("wm", "attributes", ".", "-topmost", True)
        data_files = filedialog.askopenfilename(title="Select the files to analyze", multiple=True, filetypes=[("DLC Analysis files", "*.csv *.jpg *.png *.jpeg")])

    ## Uncomment the following lines to test the code without the GUI
    # data_dir = os.path.dirname(__file__)
    # data_files = [os.path.join(data_dir, "bouts_Data", f) for f in os.listdir(os.path.join(data_dir, "bouts_Data")) if f.endswith(".csv") or f.endswith(".jpg") or f.endswith(".png") or f.endswith(".jpeg")]

    get_name = re.compile(r"^.*?(?=DLC)|^.*?(?=(\.jpg|\.png|\.bmp|\.jpeg|\.svg))")
    unique_animals = get_unique_names(data_files, get_name)
    roi_iter_obejct = it.filterfalse(lambda x: not (re.search("roi", x)), data_files)
    rois = []
    [rois.append(roi) for roi in roi_iter_obejct if "border_roi" not in roi]

    for animal in unique_animals:
        for file in data_files:
            if animal in file:
                if "filtered" in file and not data.position_files.get(animal):
                    line_edit.append("Position file found for " + animal)
                    data.add_pos_file(animal, file)
                    continue
                if (file.endswith(".jpg") or file.endswith(".png") or file.endswith(".jpeg")) and not data.experiment_images.get(animal):
                    line_edit.append("Image file found for " + animal)
                    data.add_image_file(animal, file)
                    continue
                if "_roi" in file and not data.roi_files.get(animal) and (not "border_roi" in file):
                    line_edit.append("ROI file found for " + animal)
                    data.add_roi_file(animal, file)
                    continue
    for exp_number, animal in enumerate(unique_animals):
        animal_list.append(Animal())
        animal_list[exp_number].name = animal
        animal_list[exp_number].add_experiment_jpg(data.experiment_images[animal])
        animal_list[exp_number].add_position_file(data.position_files[animal])
        tmp = it.filterfalse(lambda roi: not (re.search(animal, roi)), rois)
        animal_list[exp_number].add_roi(tmp)

        for bodypart in animal_list[exp_number].bodyparts:
            animal_list[exp_number].add_bodypart(bodypart)

    return data_files

def check_roi_files(roi):
    extracted_data = pd.read_csv(roi, sep=",")
    must_have = ["x", "y", "width", "height"]
    header = extracted_data.columns.to_frame().map(str.lower).to_numpy()
    return all(elem in header for elem in must_have)

def get_folder_path_function(self):
    file_explorer = tk.Tk()
    file_explorer.withdraw()
    file_explorer.call("wm", "attributes", ".", "-topmost", True)
    folder = str(Path(filedialog.askdirectory(title="Select the folder", mustexist=True)))
    self.interface.folder_path_lineedit.setText(folder)

def run_analysis(self, text_signal=None, progress=None):
    analysis_dir = self.interface.folder_path_lineedit.text()
    folders_to_process = []
    text_signal.emit((f"Looking through the folders in {analysis_dir}"))
    print(f"Looking through the folders in {analysis_dir}")
    for root, dirs, files in os.walk(analysis_dir):
        if not files:
            continue
        elif "data" in dirs:
            if os.listdir(os.path.join(root, "data")) != []:
                file_list_in_data = [file for file in os.listdir(os.path.join(root, "data")) if not file.endswith(".xlsx")]
                image_list_in_parent = [file for file in os.listdir(root) if file.endswith(".jpg")]
                if len(file_list_in_data) == len(image_list_in_parent):
                    text_signal.emit((f"[WARNING]: The folder {root} has already been processed."))
                    continue
                else:
                    folders_to_process.append(root)
            else:
                folders_to_process.append(root)
        elif "data" in root:
            continue
        else:
            folders_to_process.append(root)

    text_signal.emit((f"Found {len(folders_to_process)} folders to process."))
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
        mouse_width_px = int(self.interface.mouse_width_lineedit.text())
        runtime = int(self.interface.task_duration_lineedit.text())
        framerate = 30
        images = [os.path.join(folder, file) for file in data.experiment_images.values()]
        roi_files = [os.path.join(folder, file) for file in os.listdir(folder) if "border_roi" in file]
        
        with tqdm(total=len(animals), desc="Analyzing animals", leave=False) as pbar:
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

                in_border = 0
                nothing_at_all = 0
                outliers = 0
                points_in_border = []
                points_in_center = []
                outlier_points = []
            
                for _, coords in enumerate(zip(mouse_center_x, mouse_center_y, mouse_center_pos_shapely)):
                    x, y, shapely_point = coords
                    if not full_arena_ROI.contains(shapely_point):
                        outliers += 1
                        outlier_points.append((x, y))
                        continue
                    if ROI.contains(shapely_point):
                        in_border += 1
                        points_in_border.append((x, y))
                    else:
                        points_in_center.append((x, y))
                        nothing_at_all += 1

                if points_in_border == []:
                    text_signal.emit((f"[WARNING]: No points in the border for {animal.name}"))
                    print()
                    print(f"No points in border for {animal.name}")
                    no_points_in_border = True
                elif points_in_center == []:
                    text_signal.emit((f"[WARNING]: No points in the center for {animal.name}"))
                    print()
                    print(f"No points in center for {animal.name}")
                    print(f"This is probably a problem in the DLC analysis, please check the integrity of the data.")
                    no_points_in_center = True
                    
                moments_in_border_sec = in_border/framerate
                moments_outside_border_sec = nothing_at_all/framerate
                percent_in_border = (moments_in_border_sec / (moments_in_border_sec + moments_outside_border_sec)) * 100
                percent_outliers = (outliers / len(mouse_center_x)) * 100

                plt.close("all")
                fig, ax = plt.subplots(figsize=((image_width * 2) / 100, (image_height * 2) / 100))
                plot_polygon(ROI, ax=ax, color='blue', alpha=0.7, fill=False, linewidth=2)
                ax.imshow(last_frame, interpolation="bessel", alpha=0.9, cmap="gray")
                if no_points_in_center:
                    x_center = []
                    y_center = []
                else:
                    x_center, y_center = zip(*points_in_center)
                if no_points_in_border:
                    x_border = []
                    y_border = []
                else:
                    x_border, y_border = zip(*points_in_border)
                ax.scatter(x_center, y_center, color="red", s=4)
                ax.scatter(x_border, y_border, color="blue", s=4)
                ax.set_xticks([])
                ax.set_yticks([])
                ax.set_title(f"{animal.name} - Movement in arena (Blue: Border, Red: Center)")
                fig.tight_layout()
                fig.savefig(os.path.join(save_dir, f"{animal.name}_movement_in_arena.png"))

                all_results[animal.name] = {
                    "Moments in border (s)": f"{moments_in_border_sec:.2f}",
                    "Moments in the center (s)": f"{moments_outside_border_sec:.2f}",
                    "Percentage of the time in the border (%)": f"{percent_in_border:.2f}",
                    "Outliers": f"{outliers}",
                    "Percentage of outliers (%": f"{percent_outliers:.2f}"
                }

                pd.DataFrame(all_results).T.to_excel(os.path.join(save_dir, "border_analysis.xlsx"))
                pbar.update(1)
            progress.emit(round(((i + 1) / len(folders_to_process)) * 100))
    text_signal.emit((f"All folders have been processed."))
    print("All folders have been processed.")

def warning_message_function(title, text):
    warning = QMessageBox()  # Create the message box
    warning.setWindowTitle(title)  # Message box title
    warning.setText(text)  # Message box text
    warning.setIcon(QMessageBox.Icon.Warning)  # Message box icon
    warning.setStyleSheet(
        "QMessageBox{background:#353535;}QLabel{font:10pt/DejaVu Sans/;"
        + "font-weight:bold;color:#FFFFFF;}QPushButton{width:52px; border:2px solid #A21F27;border-radius:8px;"
        + "background-color:#2C53A1;color:#FFFFFF;font:10pt/DejaVu Sans/;"
        + "font-weight:bold;}QPushButton:pressed{border:2px solid #A21F27;"
        + "border-radius:8px;background-color:#A21F27;color:#FFFFFF;}"
    )
    warning.setStandardButtons(QMessageBox.StandardButton.Ok)  # Message box buttons
    warning.exec()

def on_worker_finished():
    text = "Analysis completed successfully."
    title = "Analysis completed"
    warning_message_function(title, text)