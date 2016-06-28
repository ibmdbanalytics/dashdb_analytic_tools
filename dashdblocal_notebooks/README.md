# Building and deploying a Jupyter noebook container for [dashDB local](http://www.ibm.com/analytics/us/en/technology/cloud-data-services/dashdb-local/) 

## Overview ##

This project generates a Docker image that is based on the [jupyter/base-notebook](https://github.com/jupyter/docker-stacks/tree/master/base-notebook) image. 
It supports execution of Spark/Scala and Spark/Python kernels in the Spark environment provided by dashDB local, using the . Unlike the Spark notebooks in 
(https://github.com/jupyter/docker-stacks), there is no Spark installation in the notebook container, Spark driver and executor processes run in the dashDB local
Spark environment. The Spark applications can access dashDB data easily and efficiently and there are no versioning issues between Spark components running in
different containers.

Using this container requires a dashDB local installation where the integrated Spark support has been enabled.

## Getting started ##

Follow these steps to get your own Docker container instance:

1. Install a Git client in your path.

2. Issue this command to clone the repository into a new directory:
   
  `git clone https://github.com/ibmdbanalytics/dashdb_analytic_tools.git`
 
 This creates a new directory **dashdb_analytic_tools** with subdirectory dashdblocal_notebooks. Change to the dashdblocal_notebooks subdirectory.
3. As a user with root authority, build the image:
    - `docker build -t <image name> <path to your dashdblocal_notebooks directory>`

    ...