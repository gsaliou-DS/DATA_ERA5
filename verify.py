import os 

# Répertoire contenant les fichiers .nc
directory = '/Volumes/IMT-SC-015/DATA_ERA5'

# Liste des années attendues
expected_years = list(range(1980, 2022 + 1))

# Préparer les fichiers attendus pour chaque année
expected_files = {
    f"{year}_atmos.nc": False for year in expected_years
}
expected_files.update({
    f"{year}_surface.nc": False for year in expected_years
})
expected_files.update({
    f"{year}_tisr.nc": False for year in expected_years
})

# Parcourir les fichiers dans le répertoire et marquer ceux qui existent
for filename in os.listdir(directory):
    if filename in expected_files:
        expected_files[filename] = True

# Afficher les fichiers manquants
missing_files = [file for file, exists in expected_files.items() if not exists]

if missing_files:
    print("Fichiers manquants :")
    for file in missing_files:
        print(file)
else:
    print("Tous les fichiers sont présents.")
