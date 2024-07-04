import cdsapi
import logging
import sys 
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
        logging.warning(f"Connection or OS error: {e}")
    except Exception as e:
        logging.error(f"Failed to retrieve data: {e}")

def retrieve_yearly_data(start_date, end_date, year):
    # TOA incident solar radiation data
    toa_incident_solar_params = {
        "class": "ea",
        "date": f"{start_date}/to/{end_date}",
        "expver": "1",
        "levtype": "sfc",
        "param": "212",
        "step": "0/1/2/3/4/5/6/7/8/9/10/11",
        "stream": "oper",
        "time": "06:00:00/18:00:00",
        "type": "fc",
        "area": [50, 125, 30, 155],
        'grid': '0.25/0.25', 
        'format': 'netcdf',
    }
    filename = f"{year}_tisr.nc"
    return toa_incident_solar_params, filename

if __name__ == "__main__":
    start_year = 2016
    end_year = 2022  
    years = range(start_year, end_year + 1)
    
    try:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []
            for year in years:
                params, filename = retrieve_yearly_data(f"{year-1}-12-31", f"{year}-12-31", str(year))
                futures.append(executor.submit(retrieve_data_wrapper, (params, filename)))
            
            # Wait for all futures (threads) to complete and handle potential results or exceptions
            for future in concurrent.futures.as_completed(futures):
                try:
                    future.result()  # Raises any exception caught during the execution
                except Exception as e:
                    logging.error(f"Error during data retrieval: {e}")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        sys.exit(1)
