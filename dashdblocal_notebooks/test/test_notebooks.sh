#!/bin/sh

NBCONVERT_OPTIONS="--to=markdown --ExecutePreprocessor.enabled=True"
#NBCONVERT_OPTIONS="--to=markdown --ExecutePreprocessor.enabled=True --Application.log_level=DEBUG"
WORKDIR=/test/output/notebooks

# nvbconvert always writes to the same directory where the notebooks are located
# so copy them to the test directory
cp *.ipynb $WORKDIR
cd $WORKDIR

# run nbconvert to execute the notebooks with the Spark kernel in headless mode
# NOTE the kernel will stay running after nbconvert has completed, need to shut down explicitly
jupyter nbconvert $NBCONVERT_OPTIONS Spark_KMeansSample.ipynb || exit 1

