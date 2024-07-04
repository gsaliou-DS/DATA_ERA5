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
    pressure_level_params = {
        "class": "ea",
        "date": f"{start_date}/to/{end_date}",
        "expver": "1",
        "levelist": "50/100/200/300/400/500/600/700/800/850/925/1000",
        "levtype": "pl",
        "param": "129.128/130.128/131/132/133.128",
        "stream": "oper",
        "time": "00:00:00/01:00:00/02:00:00/03:00:00/04:00:00/05:00:00/06:00:00/07:00:00/08:00:00/09:00:00/10:00:00/11:00:00/12:00:00/13:00:00/14:00:00/15:00:00/16:00:00/17:00:00/18:00:00/19:00:00/20:00:00/21:00:00/22:00:00/23:00:00",
        "type": "an",
        "area": [50, 125, 30, 155],
        'grid': '0.25/0.25',
        'format': 'netcdf',
    }
    filename = f"{year}_atmos.nc"
    return pressure_level_params, filename

if __name__ == "__main__":
    start_year = 2016
    end_year = 2022  
    years = range(start_year, end_year + 1)


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
