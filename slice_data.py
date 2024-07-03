import xarray as xr
import warnings
import os
from glob import glob
import netCDF4
from datetime import datetime

# Suppress specific numpy warning
warnings.filterwarnings("ignore", message="Signature .* for <class 'numpy.longdouble'> does not match any known type")

def process_files(year=None, data_type=None):
    input_folder = 'DATA_ERA5/'
    output_folder = 'DATA_ERA5/TISR_Corrige/'

    # Generate file pattern based on year and data type
    if year and data_type:
        file_pattern = f"{input_folder}{year}_{data_type}.nc"
    elif year:
        file_pattern = f"{input_folder}{year}_*.nc"
    elif data_type:
        file_pattern = f"{input_folder}*_{data_type}.nc"
    else:
        file_pattern = f"{input_folder}*.nc"
    
    # Get list of files matching the pattern
    files = glob(file_pattern)

    for file in files:
        try:
            nc_fichier = netCDF4.Dataset(file, 'r')
            nom_fichier = os.path.basename(file)
            file_year = nom_fichier.split('_')[0].split('/')[-1]

            for nom_var, var in nc_fichier.variables.items():
                    if nom_var == 'time':
                        time_units = var.units
                        dates = netCDF4.num2date(var[:], time_units)
                        premiere_date = dates[0]
                        derniere_date = dates[-1]

                        # Vérification de la première date
                        date_debut_attendue = datetime(year, 1, 1, 0, 0)
                        debut_correct = premiere_date == date_debut_attendue
                        
                        # Vérification de la dernière date
                        date_fin_attendue = datetime(year, 12, 31, 23, 0)
                        fin_correcte = derniere_date == date_fin_attendue
            # Verify the original file date range
            if not (debut_correct and fin_correcte): 
                print(file)
                with xr.open_dataset(file) as data:

                    output_file = f"{output_folder}{file_year}_{data_type}" 
                    
                    # Create a new file without the first 24 hours
                    data_cut = data.sel(time=slice(f'{file_year}-01-01T00:00:00.000000000', f'{file_year}-12-31T23:00:00.000000000'))
                    
                    # Save the sliced data
                    data_cut.to_netcdf(output_file+'.nc')

                    # Verify the new file date range
                    with xr.open_dataset(output_file) as data_cut:
                        print(f"Processed {file}: New file date range: {data_cut['time'].min().values} to {data_cut['time'].max().values}")

        except Exception as e:
            print(f"An error occurred processing {file}: {e}")


process_files(data_type='tisr') 
# process_files(year='2021')  # Specify only the year
# process_files(data_type='atmos')  # Specify only the type
# process_files()  # Process all files
