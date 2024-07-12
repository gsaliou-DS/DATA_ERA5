import os
import sys
from netCDF4 import Dataset

def verify_output(output_file):
    """
    Verify the contents of the output of reshape_data.py NetCDF file.
    """
    if not os.path.exists(output_file):
        print(f"Output file not found: {output_file}")
        return

    with Dataset(output_file, 'r') as dataset:
        # Print dimensions
        print("Dimensions:")
        for dim in dataset.dimensions.values():
            print(f"  {dim.name}: {len(dim)}")

        # Print variables and some of their attributes
        print("\nVariables:")
        for var in dataset.variables.values():
            print(f"  {var.name} ({var.dimensions}): {var.shape}")
            for attr in var.ncattrs():
                print(f"    {attr} = {var.getncattr(attr)}")
            
        # Optionally, print some data from variables
        print("\nData samples:")
        try:
            print(f"time: {dataset.variables['time'][:5]}")
            print(f"tcwv: {dataset.variables['tcwv'][:5, 0, 0]}")
            print(f"msl: {dataset.variables['msl'][:5, 0, 0]}")
            print(f"sp: {dataset.variables['sp'][:5, 0, 0]}")
            print(f"t2m: {dataset.variables['t2m'][:5, 0, 0]}")
            print(f"skt: {dataset.variables['skt'][:5, 0, 0]}")
            print(f"tisr: {dataset.variables['tisr'][:5, 0, 0]}")
            for var in ['z', 't', 'q', 'u', 'v']:
                for level in range(12):
                    var_name = f'{var}{level+1}'
                    print(f"{var_name}: {dataset.variables[var_name][:5, 0, 0]}")
        except KeyError as e:
            print(f"Variable not found: {e}")
        except IndexError as e:
            print(f"Index error: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python verify_output.py <output_file>")
        sys.exit(1)

    output_file = sys.argv[1]
    verify_output(output_file)
