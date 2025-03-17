import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import json

## Features to extract and save into SimBA
"""
Here is a structured list based on the image:

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
skeleton_tracking_data = pd.read_hdf(skeleton_tracking_data_file[0])
example_features_data = pd.read_csv(example_features_data_file[0], index_col=0)

print(tracking_data.head())
print(skeleton_tracking_data.head())
print(example_features_data.head())