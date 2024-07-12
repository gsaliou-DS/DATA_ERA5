import os
import re
import sys
import numpy as np
from netCDF4 import Dataset

class NetCDFProcessor:
    def __init__(self, year, data_dir):
        self.year = year
        self.data_dir = data_dir
        self.nc_files = [os.path.join(data_dir, f'{year}_surface.nc'), 
                         os.path.join(data_dir, f'{year}_atmos.nc'), 
                         os.path.join(data_dir, f'{year}_tisr.nc')]
        self.data = {
            'time': [],
            'tcwv': [],
            'msl': [],
            'sp': [],
            't2m': [],
            'skt': [],
            'z': [],
            't': [],
            'q': [],
            'u': [],
            'v': [],
            'tisr': []
        }

    def load_data(self):
        """
        Load data from the provided NetCDF files.
        """
        for nc_file in self.nc_files:
            try:
                if not os.path.exists(nc_file):
                    raise FileNotFoundError(f"File not found: {nc_file}")

                with Dataset(nc_file, 'r') as dataset:
                    if 'surface' in nc_file:
                        self.data['time'].append(dataset.variables['time'][:])
                        self.data['tcwv'].append(dataset.variables['tcwv'][:, :, :])
                        self.data['msl'].append(dataset.variables['msl'][:, :, :])
                        self.data['sp'].append(dataset.variables['sp'][:, :, :])
                        self.data['t2m'].append(dataset.variables['t2m'][:, :, :])
                        self.data['skt'].append(dataset.variables['skt'][:, :, :])
                    elif 'atmos' in nc_file:
                        self.data['z'].append(dataset.variables['z'][:, :, :, :])
                        self.data['t'].append(dataset.variables['t'][:, :, :, :])
                        self.data['q'].append(dataset.variables['q'][:, :, :, :])
                        self.data['u'].append(dataset.variables['u'][:, :, :, :])
                        self.data['v'].append(dataset.variables['v'][:, :, :, :])
                    else:
                        self.data['tisr'].append(dataset.variables['tisr'][:, :, :])
            except FileNotFoundError as e:
                print(e)
            except OSError as e:
                print(f"OS error: {e}")
            except Exception as e:
                print(f"Unexpected error: {e}")

        # Concatenate the lists into numpy arrays
        for key in self.data.keys():
            self.data[key] = np.concatenate(self.data[key]) if self.data[key] else None

    def split_pressure_levels(self):
        """
        Split the variables with pressure levels into separate variables for each level.
        """
        split_data = {}
        for var in ['z', 't', 'q', 'u', 'v']:
            if self.data[var] is not None:
                for level in range(12):
                    split_data[f'{var}{level+1}'] = self.data[var][:, level]
            else:
                for level in range(12):
                    split_data[f'{var}{level+1}'] = None
        self.data.update(split_data)

    def save_to_netcdf(self, output_file):
        """
        Save the processed data to a new NetCDF file.
        """
        with Dataset(output_file, 'w', format='NETCDF4') as dataset:
            # Define dimensions
            dataset.createDimension('time', len(self.data['time']))
            dataset.createDimension('level', 12)
            dataset.createDimension('lat', 81)
            dataset.createDimension('lon', 121)

            # Define variables
            times = dataset.createVariable('time', 'f4', ('time',))
            tcwv = dataset.createVariable('tcwv', 'f4', ('time', 'lat', 'lon'))
            msl = dataset.createVariable('msl', 'f4', ('time', 'lat', 'lon'))
            sp = dataset.createVariable('sp', 'f4', ('time', 'lat', 'lon'))
            t2m = dataset.createVariable('t2m', 'f4', ('time', 'lat', 'lon'))
            skt = dataset.createVariable('skt', 'f4', ('time', 'lat', 'lon'))
            tisr = dataset.createVariable('tisr', 'f4', ('time', 'lat', 'lon'))

            # Define variables with pressure levels
            for var in ['z', 't', 'q', 'u', 'v']:
                for level in range(12):
                    dataset.createVariable(f'{var}{level+1}', 'f4', ('time', 'lat', 'lon'))

            # Assign data to variables
            times[:] = self.data['time']
            tcwv[:, :, :] = self.data['tcwv']
            msl[:, :, :] = self.data['msl']
            sp[:, :, :] = self.data['sp']
            t2m[:, :, :] = self.data['t2m']
            skt[:, :, :] = self.data['skt']
            tisr[:, :, :] = self.data['tisr']

            for var in ['z', 't', 'q', 'u', 'v']:
                for level in range(12):
                    dataset.variables[f'{var}{level+1}'][:, :, :] = self.data[f'{var}{level+1}']

    def process(self, output_file):
        """
        Perform the entire data processing workflow and save the result.
        """
        self.load_data()
        self.split_pressure_levels()
        self.save_to_netcdf(output_file)

def find_years(data_dir):
    """
    Find unique years in the given directory by examining file names.
    """
    files = os.listdir(data_dir)
    years = set()
    pattern = re.compile(r'(\d{4})_(surface|atmos|tisr)\.nc')
    for file in files:
        match = pattern.match(file)
        if match:
            years.add(match.group(1))
    return sorted(years)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python script.py <data_directory> <output_directory>")
        sys.exit(1)

    data_dir = sys.argv[1]
    output_dir = sys.argv[2]

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    years = find_years(data_dir)

    for year in years:
        output_file = os.path.join(output_dir, f'{year}_local.nc')
        processor = NetCDFProcessor(year, data_dir)
        processor.process(output_file)
        print(f"Processed data for {year} and saved to {output_file}")
