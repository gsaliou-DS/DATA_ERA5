import cdsapi

c = cdsapi.Client()

c.retrieve(
    'reanalysis-era5-single-levels',
    {
        'product_type': 'reanalysis',
        'variable': 'geopotential',
        'year': '2023',
        'month': '01',
        'day': '01',
        'time': '00:00',
        'format': 'netcdf',
        'grid': [2.5, 2.5]
    },
    'geopotential_2.5_global.nc')
