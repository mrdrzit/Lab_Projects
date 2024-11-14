import os
import pandas as pd
import pickle

# Define data folder and file paths
data_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
file_list = [os.path.join(data_folder, file) for file in os.listdir(data_folder)]

# Load Excel files
treino = pd.read_excel(file_list[0], header=None)
reativacao = pd.read_excel(file_list[1], header=None)
teste = pd.read_excel(file_list[2], header=None)

# Function to parse data and organize it by animal ID
def organize_data_by_animal(df):
    animal_data = {}
    current_animal = None
    values = []
    
    for _, row in df.iterrows():
        cell_value = row[0]
        
        # Check if the cell value matches the animal ID pattern
        if isinstance(cell_value, str):
            # If there is an active animal ID, store its data before moving to the next
            if current_animal:
                # Apply name corrections based on specified conditions
                if current_animal.endswith("_L1") or current_animal.endswith("_L2"):
                    current_animal = current_animal[:-3]
                elif current_animal.endswith("_"):
                    current_animal = current_animal[:-1]
                elif current_animal.endswith("_animal"):
                    current_animal = current_animal[:-7]
                
                animal_data[current_animal] = values
            
            # Set the new current animal ID and reset values
            current_animal = cell_value
            values = []
        else:
            # Collect numerical values for the current animal ID
            values.append(cell_value)
    
    # Apply the correction for the last animal ID outside the loop
    if current_animal:
        if current_animal.endswith("_L1") or current_animal.endswith("_L2"):
            current_animal = current_animal[:-3]
        elif current_animal.endswith("_"):
            current_animal = current_animal[:-1]
        elif current_animal.endswith("_animal"):
            current_animal = current_animal[:-7]
        
        animal_data[current_animal] = values
    
    return animal_data

# Organize data for each file type and store in the dictionary
animals_dictionary = {
    'treino': organize_data_by_animal(treino),
    'reativacao': organize_data_by_animal(reativacao),
    'teste': organize_data_by_animal(teste)
}


# Save the dictionary to a pickle file
print("Saving the organized data to a pickle file...")
with open(os.path.join(data_folder, 'animals_data_elisa.pkl'), 'wb') as file:
    pickle.dump(animals_dictionary, file)

