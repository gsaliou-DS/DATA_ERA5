import os
import numpy as np
from netCDF4 import Dataset
import matplotlib.pyplot as plt

# Spécifiez le répertoire des fichiers de données et le répertoire de sortie
data_dir = '/data_aip05/gsaliou/era5/local/DATA_ERA5/new/'
output_dir = '/data_aip05/gsaliou/era5/local/DATA_ERA5/new/'

# Années à traiter
start_year = 1980
end_year = 2022
years = list(range(start_year, end_year + 1))

# Initialisation des tableaux pour les moyennes et écarts-types globaux
variables = ['tcwv', 'msl', 'sp', 't2m', 'skt', 'z', 't', 'q', 'u', 'v', 'tisr']
global_means = {var: np.zeros((1, 1, 1)) for var in variables}
global_stds = {var: np.zeros((1, 1, 1)) for var in variables}
time_means = {var: np.zeros((1, 721, 1440)) for var in variables}

# Fonction pour charger les données d'un fichier NetCDF
def load_data(file_path, var):
    with Dataset(file_path, 'r') as dataset:
        return dataset.variables[var][:]

# Traitement des fichiers année par année
for year in years:
    file_path = os.path.join(data_dir, f'{year}_local.nc')
    
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        continue

    for var in variables:
        data = load_data(file_path, var)
        
        # Vérifiez que data a suffisamment d'éléments sur l'axe temporel pour éviter l'indexation hors limites
        if data.shape[0] < 500:
            print(f"Not enough data in {file_path} for variable {var}")
            continue

        rnd_idx = np.random.randint(0, data.shape[0] - 500)  # Sélectionne un indice aléatoire
        data_subset = data[rnd_idx:rnd_idx+500]  # Sous-ensemble de 500 éléments

        global_means[var] += np.mean(data_subset, keepdims=True, axis=(0, 2, 3))
        global_stds[var] += np.var(data_subset, keepdims=True, axis=(0, 2, 3))
        time_means[var] += np.mean(data_subset, axis=0, keepdims=True)  # Ajout pour les moyennes temporelles

# Calcul des moyennes et écarts-types globaux
for var in variables:
    global_means[var] /= len(years)
    global_stds[var] = np.sqrt(global_stds[var] / len(years))
    time_means[var] /= len(years)

# Sauvegarde des résultats
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Sauvegarde des moyennes globales, des écarts-types globaux et des moyennes temporelles dans des fichiers uniques
np.save(os.path.join(output_dir, 'global_means.npy'), global_means)
np.save(os.path.join(output_dir, 'global_stds.npy'), global_stds)
np.save(os.path.join(output_dir, 'time_means.npy'), time_means)

# Affichage des moyennes globales
for var in variables:
    plt.figure(figsize=(10, 4))
    plt.imshow(global_means[var].reshape(1, -1), aspect='auto', cmap='viridis')
    plt.colorbar(label=f'{var} mean')
    plt.title(f'Global Mean of {var}')
    plt.xlabel('Variable Index')
    plt.ylabel('Mean Value')
    plt.show()

print("Global means: ", global_means)
print("Global stds: ", global_stds)
