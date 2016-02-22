# dashdb_analytic_tools

## Overview ##

This project generates a Docker image that is based on the [rocker/rstudio](https://github.com/rocker-org/rocker/tree/master/rstudio) image but that includes additional dashDB-specific components, such as IBM Data Server Driver packages and the ibmdbR and ibmdbRXt packages for R. The components provided by the rocker/rstudio image are described in the [documentation](https://github.com/rocker-org/rocker/wiki) for that image.

## Getting started ##

Follow these steps to get your own Docker container instance:

1. Issue this command to clone the repository into a new directory:
   
  `git clone https://github.com/ibmdbanalytics/dashdb_analytic_tools.git`
2. Download the dashDB driver package **ibm_data_server_driver_package_linuxx64_v10.5.tar.gz** into the same directory from either of the following sources:
  * From the dashDB web console:
    1. Log in with your dashDB credentials.
    2. Click **Connect > Download Tools**.
  * From the [IBM support web site] (http://www-01.ibm.com/support/docview.wss?uid=swg21385217):
    1. Select the package **IBM Data Server Driver Package (DS Driver)**.
    2. Log in with your IBM ID (sign-up is free).
    3. Select the offering **IBM Data Server Driver Package (Linux AMD64 and Intel EM64T)** for the Linux platform.
3. Build the image:
  * If you want to build the image and run the container in your own Linux environment, issue these commands:
    - `docker build -t <image name>`
    - `docker run -d -p 8787:8787 <image name>`
  * If you want to use Bluemix to host your RStudio container, issue these commands:
    - `cf ic build -t registry.ng.bluemix.net/<private namespace>/<image name>`
    - `cf ic run -p 8787 registry.ng.bluemix.net/<private namespace>/<image name>`
    - `cf ic ip`

    The last of these commands returns the IP address of the RStudio container in Bluemix. Click [here] (https://www.ng.bluemix.net/docs/containers/container_cli_reference_cfic.html) for more information about Bluemix containers.
4. To launch the RStudio web UI:
  * On a Linux system, point your browser to `<ip_addr>:8787`, where `<ip_addr>` represents the IP address of the Linux system that hosts the RStudio container.  
  * On a Windows or Mac system, use the [Docker Toolbox] (https://www.docker.com/products/docker-toolbox) to create a Docker environment on you computer in which you can run Docker commands and containers.
5. Log in to RStudio. The default user and password are both **rstudio**. For security, change the password immediately after you log in for the first time.

## Running a sample R script ##

The docker file above creates a directory of sample scripts in the user home directory. To run a sample script in this directory directly, modify the user, password, and host variables in the script as appropriate for the database that you are connecting to. 

If you use IBM dashDB on BlueMix, all the sample data used by these scripts is already preloaded. If you use a different system, you will need to upload the sample data before running the sample scripts. To do this:

1. Download the following three CSV files: 
   * [SHOWCASE_SYSTYPES.csv] (https://github.com/ibmdbanalytics/dashdb_analytic_tools/blob/master/SHOWCASE_SYSTYPES.csv)
   * [SHOWCASE_SYSUSAGE.csv] (https://github.com/ibmdbanalytics/dashdb_analytic_tools/blob/master/SHOWCASE_SYSUSAGE.csv)
   * [SHOWCASE_SYSTEMS.csv] (https://github.com/ibmdbanalytics/dashdb_analytic_tools/blob/master/SHOWCASE_SYSTEMS.csv)
2. Load the contents of these CSV files into the following tables in your database:
   * SAMPLES.SHOWCASE_SYSTYPES 
   * SAMPLES.SHOWCASE_SYSUSAGE 
   * SAMPLES.SHOWCASE_SYSTEMS

If you choose different table names, modify the script to reflect these different names. 

## Status ##

This is work in progress. For any request please contact torsten@de.ibm.com or mwurst@de.ibm.com.

## License ##

The docker file above and the content of the samples directory are provided under the GPL v2 or later. 

## Base Docker containers ##

| Docker Container Source on GitHub             | Docker Hub Build Status and URL
| :---------------------------------------      | :-----------------------------------------
| r-base (base package to build from)           | [good](https://registry.hub.docker.com/u/rocker/r-base/)
| rstudio (base plus RStudio Server)            | [good](https://registry.hub.docker.com/u/rocker/rstudio/)
