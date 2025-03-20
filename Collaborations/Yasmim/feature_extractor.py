import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import json
import math

def angle_between_points(x1, y1, x2, y2, angle_type='degrees'):
   """
   Calculate the angle between two points (x1, y1) and (x2, y2) in degrees.
   """
   # Calculate the differences
   dx = x2 - x1
   dy = y2 - y1

   # Calculate the angle in radians
   angle_radians = math.atan2(dy, dx)

   # Convert the angle to degrees
   if angle_type == 'degrees':
      angle_degrees = math.degrees(angle_radians) % 360 # Convert to degrees and normalize to [0, 360)
   elif angle_type == 'radians':
      angle_degrees = angle_radians
   else:
      raise ValueError("The angle_type must be 'degrees' or 'radians'.")

   return angle_degrees

## Features to extract and save into SimBA
"""
### Behavioral Features:
1. **Sniffing**  
   - Ângulo da cabeça em relação ao centro
   - Desaparecimento do ponto do nariz
   - Velocidade do ponto do nariz
   - Posição do ponto do nariz

2. **Resting/locomoção**  
   - Movimento dos pontos
   - Velocidade dos pontos
   - Velocidade do centro de massa
   - Movimentação do centro de massa

3. **Grooming**  
   - Ângulo da cabeça-centro/quadril
   - Distância cabeça-centro  
   - Distância cabeça-quadril  
   - Movimento do ponto da cabeça
   - Posição do centro de massa
   - Velocidade do centro de massa

4. **Rearing**  
   - Ângulo cabeça-centro  
   - Distância cabeça-centro
   - Posição do centro de massa
   - Velocidade do centro de massa
   - Posição do ponto do nariz em relação ao centro de massa

"""

# Define the data folders
raw_position_data = os.path.join(os.path.dirname(__file__), 'raw_data')
raw_features_data = os.path.join(os.path.dirname(__file__), 'raw_extracted_features')

# Load DLC tracking data
tracking_data_file = [os.path.join(raw_position_data, file) for file in os.listdir(raw_position_data) if file.endswith('.h5') if "skeleton" not in file]
skeleton_tracking_data_file = [os.path.join(raw_position_data, file) for file in os.listdir(raw_position_data) if file.endswith('.h5') if "skeleton" in file]
example_features_data_file = [os.path.join(raw_features_data, file) for file in os.listdir(raw_features_data) if file.endswith('.csv')]

# Load the tracking data
tracking_data = pd.read_hdf(tracking_data_file[0])
if "scorer" in tracking_data.columns.names:
   tracking_data.columns = tracking_data.columns.droplevel(0)

skeleton_tracking_data = pd.read_hdf(skeleton_tracking_data_file[0])
example_features_data = pd.read_csv(example_features_data_file[0], index_col=0)

## Sniffing features extraction
# Head angle from center ----------------------------------------------------------------------------------------------------------------------
focinho_x_pos = ("Focinho", "x")
focinho_y_pos = ("Focinho", "y")
focinho_p = ("Focinho", "likelihood")
orelha_E_x_pos = ("OrelhaE", "x")
orelha_E_y_pos = ("OrelhaE", "y")
orelha_E_p = ("OrelhaE", "likelihood")
orelha_D_x_pos = ("OrelhaD", "x")
orelha_D_y_pos = ("OrelhaD", "y")
orelha_D_p = ("OrelhaD", "likelihood")
centro_x_pos = ("Centro", "x")
centro_y_pos = ("Centro", "y")
centro_p = ("Centro", "likelihood")
rabo_x_pos = ("Rabo", "x")
rabo_y_pos = ("Rabo", "y")
rabo_p = ("Rabo", "likelihood")

head_angle_from_center = []
for x1, y1, x2, y2 in zip(tracking_data[centro_x_pos], tracking_data[centro_y_pos], tracking_data[focinho_x_pos], tracking_data[focinho_y_pos]):
   head_angle_from_center.append(angle_between_points(x1, y1, x2, y2))
head_angle_from_center = pd.DataFrame(head_angle_from_center, columns=['head_angle_from_center'])

# Nose point disappearance ----------------------------------------------------------------------------------------------------------------------
nose_point_disappearance = (tracking_data[focinho_p] < 0.4).astype(int).rename('nose_point_disappearance')

# Nose point velocity ----------------------------------------------------------------------------------------------------------------------
nose_point_velocity = pd.DataFrame(np.sqrt(np.diff(tracking_data[focinho_x_pos])**2 + np.diff(tracking_data[focinho_y_pos])**2)).rename(columns={0: 'nose_point_velocity'})

# Nose point position ----------------------------------------------------------------------------------------------------------------------
nose_point_position_x = tracking_data[focinho_x_pos].rename('nose_point_position_x')
nose_point_position_y = tracking_data[focinho_y_pos].rename('nose_point_position_y')

## Resting and locomotion features extraction
# Movement of points ----------------------------------------------------------------------------------------------------------------------
focinho_x_movement = pd.DataFrame(np.diff(tracking_data[focinho_x_pos])).rename(columns={0: 'focinho_x_movement'})
focinho_y_movement = pd.DataFrame(np.diff(tracking_data[focinho_y_pos])).rename(columns={0: 'focinho_y_movement'})
orelha_E_x_movement = pd.DataFrame(np.diff(tracking_data[orelha_E_x_pos])).rename(columns={0: 'orelha_E_x_movement'})
orelha_E_y_movement = pd.DataFrame(np.diff(tracking_data[orelha_E_y_pos])).rename(columns={0: 'orelha_E_y_movement'})
orelha_D_x_movement = pd.DataFrame(np.diff(tracking_data[orelha_D_x_pos])).rename(columns={0: 'orelha_D_x_movement'})
orelha_D_y_movement = pd.DataFrame(np.diff(tracking_data[orelha_D_y_pos])).rename(columns={0: 'orelha_D_y_movement'})
centro_x_movement = pd.DataFrame(np.diff(tracking_data[centro_x_pos])).rename(columns={0: 'centro_x_movement'})
centro_y_movement = pd.DataFrame(np.diff(tracking_data[centro_y_pos])).rename(columns={0: 'centro_y_movement'})
rabo_x_movement = pd.DataFrame(np.diff(tracking_data[rabo_x_pos])).rename(columns={0: 'rabo_x_movement'})
rabo_y_movement = pd.DataFrame(np.diff(tracking_data[rabo_y_pos])).rename(columns={0: 'rabo_y_movement'})

# Velocity of points ----------------------------------------------------------------------------------------------------------------------
focinho_velocity = pd.DataFrame(np.sqrt(np.diff(tracking_data[focinho_x_pos])**2 + np.diff(tracking_data[focinho_y_pos])**2)).rename(columns={0: 'focinho_velocity'})
orelha_E_velocity = pd.DataFrame(np.sqrt(np.diff(tracking_data[orelha_E_x_pos])**2 + np.diff(tracking_data[orelha_E_y_pos])**2)).rename(columns={0: 'orelha_E_velocity'})
orelha_D_velocity = pd.DataFrame(np.sqrt(np.diff(tracking_data[orelha_D_x_pos])**2 + np.diff(tracking_data[orelha_D_y_pos])**2)).rename(columns={0: 'orelha_D_velocity'})
centro_velocity = pd.DataFrame(np.sqrt(np.diff(tracking_data[centro_x_pos])**2 + np.diff(tracking_data[centro_y_pos])**2)).rename(columns={0: 'centro_velocity'})
rabo_velocity = pd.DataFrame(np.sqrt(np.diff(tracking_data[rabo_x_pos])**2 + np.diff(tracking_data[rabo_y_pos])**2)).rename(columns={0: 'rabo_velocity'})

# Velocity of center of mass ----------------------------------------------------------------------------------------------------------------------
focinho_position_x = tracking_data[focinho_x_pos].rename('focinho_position_x')
focinho_position_y = tracking_data[focinho_y_pos].rename('focinho_position_y')
orelha_E_position_x = tracking_data[orelha_E_x_pos].rename('orelha_E_position_x')
orelha_E_position_y = tracking_data[orelha_E_y_pos].rename('orelha_E_position_y')
orelha_D_position_x = tracking_data[orelha_D_x_pos].rename('orelha_D_position_x')
orelha_D_position_y = tracking_data[orelha_D_y_pos].rename('orelha_D_position_y')
centro_position_x = tracking_data[centro_x_pos].rename('centro_position_x')
centro_position_y = tracking_data[centro_y_pos].rename('centro_position_y')
rabo_position_x = tracking_data[rabo_x_pos].rename('rabo_position_x')
rabo_position_y = tracking_data[rabo_y_pos].rename('rabo_position_y')

try:
   assert len(focinho_position_x) == len(focinho_position_y) == len(orelha_E_position_x) == len(orelha_E_position_y) == len(orelha_D_position_x) == len(orelha_D_position_y) == len(centro_position_x) == len(centro_position_y) == len(rabo_position_x) == len(rabo_position_y)
except AssertionError:
   raise ValueError("The position data must have the same length.")

center_of_mass_position_x = (focinho_position_x + orelha_E_position_x + orelha_D_position_x + centro_position_x + rabo_position_x) / 5
center_of_mass_position_y = (focinho_position_y + orelha_E_position_y + orelha_D_position_y + centro_position_y + rabo_position_y) / 5

center_of_mass_velocity = pd.DataFrame(np.sqrt(np.diff(center_of_mass_position_x)**2 + np.diff(center_of_mass_position_y)**2)).rename(columns={0: 'center_of_mass_velocity'})

# Movement of center of mass ----------------------------------------------------------------------------------------------------------------------
center_of_mass_movement_x = pd.DataFrame(np.diff(center_of_mass_position_x)).rename(columns={0: 'center_of_mass_movement_x'})
center_of_mass_movement_y = pd.DataFrame(np.diff(center_of_mass_position_y)).rename(columns={0: 'center_of_mass_movement_y'})

## Grooming features extraction
# Head angle from center/quadril ----------------------------------------------------------------------------------------------------------------------
head_angle_from_center_quadril = []







temporary_dataframe = pd.DataFrame([head_angle_from_center, nose_point_disappearance, nose_point_velocity, nose_point_position], columns=['head_angle_from_center', 'nose_point_disappearance', 'nose_point_velocity', 'nose_point_position'])

