import os
import math
import logging
import pandas as pd
import numpy as np
import re
from pathlib import Path

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def angle_between_points(x1, y1, x2, y2, angle_type='degrees'):
   """
   Calculate the angle between two points (x1, y1) and (x2, y2) in degrees.
   """
   # Calculate the differences
   dx = x2 - x1
   dy = y2 - y1

   # Calculate the angle in radians
   angle_radians = math.atan2(dy, dx)
   if angle_type == 'degrees':
      return math.degrees(angle_radians) % 360
   elif angle_type == 'radians':
      return angle_radians

   else:
      raise ValueError("The angle_type must be 'degrees' or 'radians'.")

logging.info("Starting feature extraction script.")

# Define the data folders
script_dir = os.path.abspath(os.path.dirname(__file__))
raw_position_data_sleap = os.path.join(script_dir, 'raw_data_sleap')

# Check if data folders exist
if not os.path.exists(raw_position_data_sleap):
    logging.error(f"Missing data directory: {raw_position_data_sleap}")
    raise FileNotFoundError(f"Missing data directory: {raw_position_data_sleap}")

# Load DLC tracking data
tracking_data_files_sleap = [os.path.join(raw_position_data_sleap, file) for file in os.listdir(raw_position_data_sleap) if file.endswith('.csv')]

logging.info(f"Tracking data file found: {len(tracking_data_files_sleap)}")

for tracking_data_file in tracking_data_files_sleap:
   split_sleap_prefix_re = re.compile(r"^[A-Za-z]{6}.v[0-9]{0,6}.[0-9]{0,6}_((?:.*?))\.analysis")
   current_animal_name = split_sleap_prefix_re.match(Path(tracking_data_file).stem).groups()[0]
   
   if not current_animal_name:
      logging.error(f"Error extracting animal name from file: {tracking_data_file}")
      logging.error(f"Perhaps the file name format is incorrect.")
      logging.error(f"Regex used was {split_sleap_prefix_re}")
      exit()
   
   logging.info(f"======================================== Starting feature extraction for {current_animal_name} ========================================")

   # Load the tracking data
   try:
      tracking_data = pd.read_csv(tracking_data_file)
      logging.info(f"Successfully loaded tracking data ")
   except Exception as e:
      logging.error(f"Error loading tracking data: {e}")
      exit()

   logging.info("Starting Sniffing feature extraction.")
   ## Sniffing features extraction
   # Head angle from center ----------------------------------------------------------------------------------------------------------------------
   focinho_x_pos = ("snout.x")
   focinho_y_pos = ("snout.y")
   focinho_p = ("snout.score")

   orelha_E_x_pos = ("left_ear.x")
   orelha_E_y_pos = ("left_ear.y")
   orelha_E_p = ("left_ear.score")

   orelha_D_x_pos = ("right_ear.x")
   orelha_D_y_pos = ("right_ear.y")
   orelha_D_p = ("right_ear.score")

   cintura_direita_x_pos = ("right_hip.x")
   cintura_direita_y_pos = ("right_hip.y")
   cintura_direita_p = ("right_hip.score")

   cintura_esquerda_x_pos = ("left_hip.x")
   cintura_esquerda_y_pos = ("left_hip.y")
   cintura_esquerda_p = ("left_hip.score")

   centro_x_pos = ("center.x")
   centro_y_pos = ("center.y")
   centro_p = ("center.score")

   rabo_x_pos = ("tail_base.x")
   rabo_y_pos = ("tail_base.y")
   rabo_p = ("tail_base.score")

   head_angle_from_center = []
   for x1, y1, x2, y2 in zip(tracking_data[centro_x_pos], tracking_data[centro_y_pos], tracking_data[focinho_x_pos], tracking_data[focinho_y_pos]):
      head_angle_from_center.append(angle_between_points(x1, y1, x2, y2))
   head_angle_from_center = pd.DataFrame(head_angle_from_center, columns=['head_angle_from_center']).fillna(0)
   logging.info("Head angle from center calculated.")

   # Nose point disappearance --------------------------------------------------------------------------------------------------------------------
   nose_point_disappearance = (tracking_data[focinho_p] < 0.4).astype(int).rename('nose_point_disappearance').fillna(0)
   logging.info("Nose point disappearance feature extracted.")

   # Nose point velocity -------------------------------------------------------------------------------------------------------------------------
   nose_point_velocity = pd.DataFrame(np.sqrt(tracking_data[focinho_x_pos].diff().fillna(0)**2 + tracking_data[focinho_y_pos].diff().fillna(0)**2)).rename(columns={0: 'nose_point_velocity'})
   logging.info("Nose point velocity feature extracted.")

   # Nose point position -------------------------------------------------------------------------------------------------------------------------
   nose_point_position_x = tracking_data[focinho_x_pos].rename('nose_point_position_x').fillna(0)
   nose_point_position_y = tracking_data[focinho_y_pos].rename('nose_point_position_y').fillna(0)
   logging.info("Nose point position feature extracted.")

   logging.info("Starting Resting and Locomotion feature extraction.")
   ## Resting and locomotion features extraction
   # Movement of points --------------------------------------------------------------------------------------------------------------------------
   focinho_x_movement = tracking_data[focinho_x_pos].diff().fillna(0).rename('focinho_x_movement')
   focinho_y_movement = tracking_data[focinho_y_pos].diff().fillna(0).rename('focinho_y_movement')
   orelha_E_x_movement = tracking_data[orelha_E_x_pos].diff().fillna(0).rename('orelha_E_x_movement')
   orelha_E_y_movement = tracking_data[orelha_E_y_pos].diff().fillna(0).rename('orelha_E_y_movement')
   orelha_D_x_movement = tracking_data[orelha_D_x_pos].diff().fillna(0).rename('orelha_D_x_movement')
   orelha_D_y_movement = tracking_data[orelha_D_y_pos].diff().fillna(0).rename('orelha_D_y_movement')
   centro_x_movement = tracking_data[centro_x_pos].diff().fillna(0).rename('centro_x_movement')
   centro_y_movement = tracking_data[centro_y_pos].diff().fillna(0).rename('centro_y_movement')
   rabo_x_movement = tracking_data[rabo_x_pos].diff().fillna(0).rename('rabo_x_movement')
   rabo_y_movement = tracking_data[rabo_y_pos].diff().fillna(0).rename('rabo_y_movement')
   logging.info("Movement of points features extracted.")

   # Velocity of points --------------------------------------------------------------------------------------------------------------------------
   focinho_velocity = pd.DataFrame(np.sqrt(tracking_data[focinho_x_pos].diff().fillna(0)**2 + tracking_data[focinho_y_pos].diff().fillna(0)**2)).rename(columns={0: 'focinho_velocity'})
   orelha_E_velocity = pd.DataFrame(np.sqrt(tracking_data[orelha_E_x_pos].diff().fillna(0)**2 + tracking_data[orelha_E_y_pos].diff().fillna(0)**2)).rename(columns={0: 'orelha_E_velocity'})
   orelha_D_velocity = pd.DataFrame(np.sqrt(tracking_data[orelha_D_x_pos].diff().fillna(0)**2 + tracking_data[orelha_D_y_pos].diff().fillna(0)**2)).rename(columns={0: 'orelha_D_velocity'})
   centro_velocity = pd.DataFrame(np.sqrt(tracking_data[centro_x_pos].diff().fillna(0)**2 + tracking_data[centro_y_pos].diff().fillna(0)**2)).rename(columns={0: 'centro_velocity'})
   rabo_velocity = pd.DataFrame(np.sqrt(tracking_data[rabo_x_pos].diff().fillna(0)**2 + tracking_data[rabo_y_pos].diff().fillna(0)**2)).rename(columns={0: 'rabo_velocity'})
   logging.info("Velocity of points features extracted.")

   # Center of mass velocity ------------------------------------------------------------------------------------------------------------------
   focinho_position_x = tracking_data[focinho_x_pos].rename('focinho_position_x').fillna(0)
   focinho_position_y = tracking_data[focinho_y_pos].rename('focinho_position_y').fillna(0)
   orelha_E_position_x = tracking_data[orelha_E_x_pos].rename('orelha_E_position_x').fillna(0)
   orelha_E_position_y = tracking_data[orelha_E_y_pos].rename('orelha_E_position_y').fillna(0)
   orelha_D_position_x = tracking_data[orelha_D_x_pos].rename('orelha_D_position_x').fillna(0)
   orelha_D_position_y = tracking_data[orelha_D_y_pos].rename('orelha_D_position_y').fillna(0)
   centro_position_x = tracking_data[centro_x_pos].rename('centro_position_x').fillna(0)
   centro_position_y = tracking_data[centro_y_pos].rename('centro_position_y').fillna(0)
   rabo_position_x = tracking_data[rabo_x_pos].rename('rabo_position_x').fillna(0)
   rabo_position_y = tracking_data[rabo_y_pos].rename('rabo_position_y').fillna(0)

   try:
      assert len(focinho_position_x) == len(focinho_position_y) == len(orelha_E_position_x) == len(orelha_E_position_y) == len(orelha_D_position_x) == len(orelha_D_position_y) == len(centro_position_x) == len(centro_position_y) == len(rabo_position_x) == len(rabo_position_y)
   except AssertionError:
      raise ValueError("The position data must have the same length.")

   center_of_mass_position_x = pd.DataFrame((focinho_position_x + orelha_E_position_x + orelha_D_position_x + centro_position_x + rabo_position_x) / 5).rename(columns={0: 'center_of_mass_position_x'})
   center_of_mass_position_y = pd.DataFrame((focinho_position_y + orelha_E_position_y + orelha_D_position_y + centro_position_y + rabo_position_y) / 5).rename(columns={0: 'center_of_mass_position_y'})
   center_of_mass_velocity = pd.DataFrame(np.sqrt(center_of_mass_position_x.diff().fillna(0).values.flatten()**2 + center_of_mass_position_y.diff().fillna(0).values.flatten()**2)).rename(columns={0: 'center_of_mass_velocity'}).fillna(0)
   logging.info("Center of mass velocity features extracted.")

   # Movement of center of mass ------------------------------------------------------------------------------------------------------------------
   center_of_mass_movement_x = pd.DataFrame(center_of_mass_position_x.diff().fillna(0).values.flatten()).rename(columns={0: 'center_of_mass_movement_x'})
   center_of_mass_movement_y = pd.DataFrame(center_of_mass_position_y.diff().fillna(0).values.flatten()).rename(columns={0: 'center_of_mass_movement_y'})
   logging.info("Movement of center of mass features extracted.")

   ## Grooming features extraction
   # Head angle from center/quadril --------------------------------------------------------------------------------------------------------------
   head_angle_from_center_quadril = head_angle_from_center # This feature is already calculated
   logging.info("Head angle from center/quadril feature extracted.")

   # Center-head distance ------------------------------------------------------------------------------------------------------------------------
   cat1 = (tracking_data[focinho_x_pos] - tracking_data[centro_x_pos])**2
   cat2 = (tracking_data[focinho_y_pos] - tracking_data[centro_y_pos])**2
   center_head_distance = pd.DataFrame(np.sqrt(cat1 + cat2)).rename(columns={0: 'center_head_distance'}).fillna(0)
   logging.info("Center-head distance feature extracted.")

   # Center-left hip distance ---------------------------------------------------------------------------------------------------------------------
   cat_1_focinho_cintura_esquerda = (tracking_data[focinho_x_pos] - tracking_data[cintura_esquerda_x_pos])**2
   cat_2_focinho_cintura_esquerda = (tracking_data[focinho_y_pos] - tracking_data[cintura_esquerda_y_pos])**2
   center_left_hip_distance = pd.DataFrame(np.sqrt(cat_1_focinho_cintura_esquerda + cat_2_focinho_cintura_esquerda)).rename(columns={0: 'center_left_hip_distance'}).fillna(0)
   logging.info("Center-left hip distance feature extracted.")

   # Center-right hip distance --------------------------------------------------------------------------------------------------------------------
   cat_1_focinho_cintura_direita = (tracking_data[focinho_x_pos] - tracking_data[cintura_direita_x_pos])**2
   cat_2_focinho_cintura_direita = (tracking_data[focinho_y_pos] - tracking_data[cintura_direita_y_pos])**2
   center_right_hip_distance = pd.DataFrame(np.sqrt(cat_1_focinho_cintura_direita + cat_2_focinho_cintura_direita)).rename(columns={0: 'center_right_hip_distance'}).fillna(0)
   logging.info("Center-right hip distance feature extracted.")

   # Center of mass position ---------------------------------------------------------------------------------------------------------------------
   # This feature is already calculated

   # Center of mass velocity ---------------------------------------------------------------------------------------------------------------------
   # This feature is already calculated

   ## Rearing features extraction
   # Head angle from center ----------------------------------------------------------------------------------------------------------------------
   # This feature is already calculated

   # Center-head distance ------------------------------------------------------------------------------------------------------------------------
   # This feature is already calculated

   # Center of mass position ---------------------------------------------------------------------------------------------------------------------
   # This feature is already calculated

   # Center of mass velocity ---------------------------------------------------------------------------------------------------------------------
   # This feature is already calculated
   logging.info("Skipping already extracted features: head angle from center, center-head distance, center of mass position, and center of mass velocity.")

   # Nose point position in relation to the center of mass ---------------------------------------------------------------------------------------
   center_of_mass_to_nose_point_x = tracking_data[focinho_x_pos] - center_of_mass_position_x.values.flatten()
   center_of_mass_to_nose_point_y = tracking_data[focinho_y_pos] - center_of_mass_position_y.values.flatten()
   center_of_mass_to_nose_distance = pd.DataFrame(np.sqrt(center_of_mass_to_nose_point_x**2 + center_of_mass_to_nose_point_y**2)).rename(columns={0: 'center_of_mass_to_nose_distance'}).fillna(0)
   logging.info("Center of mass to nose distance feature extracted.")
   logging.info("Feature extraction complete.")

   logging.info("Saving features into separate folders and csv files for each feature set.")
   ## Save the features into separate folders and csv files for each feature set
   # Create the folders
   logging.info("Creating folders for each feature set.")
   features_folders = ['sniffing_features_from_sleap', 'resting_locomotion_features_from_sleap', 'grooming_features_from_sleap', 'rearing_features_from_sleap']
   for folder in features_folders:
      if not os.path.exists(os.path.abspath(os.path.join(os.path.dirname(__file__), folder))):
         logging.info(f"Creating folder: {folder}")
         os.makedirs(os.path.abspath(os.path.join(os.path.dirname(__file__), folder)))
      else:
         logging.info(f"Folder already exists: {folder}")

   logging.info("Generating DataFrames for each feature set.")
   # Create a dataframe for each feature set
   sniffing_features = pd.concat([pd.DataFrame([f'"{num}"' for num in range(len(head_angle_from_center))]), head_angle_from_center, nose_point_disappearance, nose_point_velocity, nose_point_position_x, nose_point_position_y], axis=1).fillna(0)
   resting_features = pd.concat([pd.DataFrame([f'"{num}"' for num in range(len(head_angle_from_center))]), focinho_x_movement, focinho_y_movement, orelha_E_x_movement, orelha_E_y_movement, orelha_D_x_movement, orelha_D_y_movement, centro_x_movement, centro_y_movement, rabo_x_movement, rabo_y_movement, focinho_velocity, orelha_E_velocity, orelha_D_velocity, centro_velocity, rabo_velocity, center_of_mass_velocity, center_of_mass_movement_x, center_of_mass_movement_y], axis=1).fillna(0)
   locomotion_features = resting_features
   grooming_features = pd.concat([pd.DataFrame([f'"{num}"' for num in range(len(head_angle_from_center))]), head_angle_from_center_quadril, center_head_distance, center_of_mass_position_x, center_of_mass_position_y, center_of_mass_velocity], axis=1).fillna(0)
   rearing_features = pd.concat([pd.DataFrame([f'"{num}"' for num in range(len(head_angle_from_center))]), head_angle_from_center, center_head_distance, center_of_mass_position_x, center_of_mass_position_y, center_of_mass_velocity, center_of_mass_to_nose_distance], axis=1).fillna(0)

   # Add quotes to match the features file template
   sniffing_features.columns = ['""'if col == 0 else f'"{col}"' for col in sniffing_features.columns]
   resting_features.columns = ['""' if col == 0 else f'"{col}"' for col in resting_features.columns]
   grooming_features.columns = ['""' if col == 0 else f'"{col}"' for col in grooming_features.columns]
   rearing_features.columns = ['""' if col == 0 else f'"{col}"' for col in rearing_features.columns]

   error = {
   "Sniffing": True,
   "Resting": True,
   "Locomotion": True,
   "Grooming": True,
   "Rearing": True
   }

   try:
      # Save the features into CSV files
      sniffing_file_path = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), 'sniffing_features_from_sleap')), f'{current_animal_name}.csv')
      resting_file_path = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), 'resting_locomotion_features_from_sleap')), f'{current_animal_name}.csv')
      locomotion_file_path = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), 'resting_locomotion_features_from_sleap')), f'{current_animal_name}.csv')
      grooming_file_path = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), 'grooming_features_from_sleap')), f'{current_animal_name}.csv')
      rearing_file_path = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), 'rearing_features_from_sleap')), f'{current_animal_name}.csv')

      sniffing_features.to_csv(sniffing_file_path, index=False, quoting=3)
      error["Sniffing"] = False
      logging.info(f"Sniffing features saved")

      resting_features.to_csv(resting_file_path, index=False, quoting=3)
      error["Resting"] = False
      logging.info(f"Resting features saved")

      locomotion_features.to_csv(locomotion_file_path, index=False, quoting=3)
      error["Locomotion"] = False
      logging.info(f"Locomotion features saved")

      grooming_features.to_csv(grooming_file_path, index=False, quoting=3)
      error["Grooming"] = False
      logging.info(f"Grooming features saved")

      rearing_features.to_csv(rearing_file_path, index=False, quoting=3)
      error["Rearing"] = False
      logging.info(f"Rearing features saved")
   except Exception as e:
      # Identify which file failed to save
      for feature, status in error.items():
         if status == True:
               logging.error(f"Error saving {feature} features to CSV")
               exit()

   # Dictionary of all DataFrames with their names
   dataframes = {
      "head_angle_from_center": head_angle_from_center,
      "nose_point_disappearance": nose_point_disappearance,
      "nose_point_velocity": nose_point_velocity,
      "nose_point_position_x": nose_point_position_x,
      "nose_point_position_y": nose_point_position_y,
      "focinho_x_movement": focinho_x_movement,
      "focinho_y_movement": focinho_y_movement,
      "orelha_E_x_movement": orelha_E_x_movement,
      "orelha_E_y_movement": orelha_E_y_movement,
      "orelha_D_x_movement": orelha_D_x_movement,
      "orelha_D_y_movement": orelha_D_y_movement,
      "centro_x_movement": centro_x_movement,
      "centro_y_movement": centro_y_movement,
      "rabo_x_movement": rabo_x_movement,
      "rabo_y_movement": rabo_y_movement,
      "focinho_velocity": focinho_velocity,
      "orelha_E_velocity": orelha_E_velocity,
      "orelha_D_velocity": orelha_D_velocity,
      "centro_velocity": centro_velocity,
      "rabo_velocity": rabo_velocity,
      "center_of_mass_position_x": center_of_mass_position_x,
      "center_of_mass_position_y": center_of_mass_position_y,
      "center_of_mass_velocity": center_of_mass_velocity,
      "center_of_mass_movement_x": center_of_mass_movement_x,
      "center_of_mass_movement_y": center_of_mass_movement_y,
      "center_head_distance": center_head_distance,
      "center_of_mass_to_nose_distance": center_of_mass_to_nose_distance,
      "center_left_hip_distance": center_left_hip_distance,
      "center_right_hip_distance": center_right_hip_distance,
   }

   logging.info("Checking for inconsistencies in the DataFrames.")
   # Get row counts
   row_counts = {name: df.shape[0] for name, df in dataframes.items()}

   # Check for inconsistencies
   unique_counts = set(row_counts.values())

   if len(unique_counts) == 1:
      logging.info(f"All DataFrames have the same number of rows: {list(unique_counts)[0]}")
   else:
      logging.error("DataFrames have different row counts!")
      for name, count in row_counts.items():
         logging.error(f"{name}: {count} rows")