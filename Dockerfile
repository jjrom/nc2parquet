#
# nc2parquet
#
# Build
#
#   docker build --pull -t jjrom/nc2parquet -f ./Dockerfile .
#
# Usage
#
#   docker run -t --rm -v `pwd`:/output jjrom/nc2parquet NETCDF_FILE_NAME
#
FROM python:3.9.21-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    # Prevents Python from buffering stdout and stder
    # Fixes emtpy logs issue `docker logs -f ID` or `kubectl -n processing logs -f ID`
    PYTHONUNBUFFERED=1

RUN mkdir /app
RUN mkdir /output
WORKDIR /app

RUN apt-get update && apt-get install -y python3-pip

COPY ./requirements.txt /app

RUN pip3 install -r /app/requirements.txt

COPY ./nc2parquet.py /app

ENTRYPOINT [ "python", "/app/nc2parquet.py" ]