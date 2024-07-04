import cdsapi
import logging
import sys
import time 
import concurrent.futures
from requests.exceptions import ConnectionError

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def retrieve_data_wrapper(params_filename):
    c = cdsapi.Client()
    params, filename = params_filename
    try:
        logging.info(f"Starting data retrieval for {filename}")
        c.retrieve("reanalysis-era5-complete", params, filename)
        logging.info(f"Data successfully retrieved and saved to {filename}")
    except (ConnectionError, OSError) as e:
        logging.warning(f"Connection error: {e}")
    except Exception as e:
        logging.error(f"Failed to retrieve data: {e}")

def retrieve_yearly_data(start_date, end_date, year):
    surface_level_params = {
        "class": "ea",
        "date": f"{start_date}/to/{end_date}",
        "expver": "1",
        "levtype": "sfc",
        "param": "134.128/137.128/151.128/167.128/235.128",
        "stream": "oper",
        "time": "00:00:00/01:00:00/02:00:00/03:00:00/04:00:00/05:00:00/06:00:00/07:00:00/08:00:00/09:00:00/10:00:00/11:00:00/12:00:00/13:00:00/14:00:00/15:00:00/16:00:00/17:00:00/18:00:00/19:00:00/20:00:00/21:00:00/22:00:00/23:00:00",
        "type": "an",
        "area": [50, 125, 30, 155],
        'grid': '0.25/0.25',
        'format': 'netcdf',
    }
    filename = f"{year}_surface.nc"
    return surface_level_params, filename

if __name__ == "__main__":
    start_year = 1979
    end_year = 2005  # Adjust this to the range of years you want to retrieve
    years = range(start_year, end_year + 1)
    #years = (2009,2012,2018)

    try:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []
            for year in years:
                params, filename = retrieve_yearly_data(f"{year}-01-01", f"{year}-12-31", str(year))
                futures.append(executor.submit(retrieve_data_wrapper, (params, filename)))
            
            # Wait for all futures (threads) to complete
            for future in concurrent.futures.as_completed(futures):
                pass  # Optionally, you can handle results or errors here

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        sys.exit(1)
