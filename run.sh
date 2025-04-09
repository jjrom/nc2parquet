#!/bin/bash

ROOT_DIR=/Users/jrom/Downloads/ \
LONGITUDE_DIMENSION=lon \
LATITUDE_DIMENSION=lat \
TIME_DIMENSION=time \
VARIABLE_NAME=__xarray_dataarray_variable__ \
python3 nc2parquet.py march_2022_pred.nc
