# nc2parquet
Convert netcdf to GeoParquet

## Build

    docker build --pull -t jjrom/nc2parquet -f ./Dockerfile .

## Usage
Convert a NetCDF file (march_2022_pred.nc) with three dimensions "lon,lat,time" and one variable "__xarray_dataarray_variable__"

    docker run -t --rm -v `pwd`:/output \
        -e ROOT_DIR=/Users/jrom/Downloads/ \
        -e LONGITUDE_DIMENSION=lon \
        -e LATITUDE_DIMENSION=lat \
        -e TIME_DIMENSION=time \
        -e VARIABLE_NAME=__xarray_dataarray_variable__ \
        -e NAN_THRESHOLD=0 \
        jjrom/nc2parquet march_2022_pred.nc


    docker run -t --rm -v /Users/jrom/Downloads:/output \
        -e LONGITUDE_DIMENSION=lon \
        -e LATITUDE_DIMENSION=lat \
        -e TIME_DIMENSION=time \
        -e VARIABLE_NAME=__xarray_dataarray_variable__ \
        -e NAN_THRESHOLD=0 \
        jjrom/nc2parquet march_2022_pred.nc

To create a Polygon parquet instead of point, set the GRID_SIZE:

    docker run -t --rm -v `pwd`:/output \
        -e ROOT_DIR=/Users/jrom/Downloads/ \
        -e LONGITUDE_DIMENSION=lon \
        -e LATITUDE_DIMENSION=lat \
        -e TIME_DIMENSION=time \
        -e VARIABLE_NAME=__xarray_dataarray_variable__ \
        -e NAN_THRESHOLD=0 \
        -e GRID_SIZE=0.25 \
        jjrom/nc2parquet march_2022_pred.nc