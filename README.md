# dashdb_analytic_tools

## Overview ##

This project generates a Docker image that is based on the [rocker/rstudio](https://github.com/rocker-org/rocker/tree/master/rstudio) image but that includes additional dashDB-specific components, such as IBM Data Server Driver packages and the ibmdbR and ibmdbRXt packages for R. The components provided by the rocker/rstudio image are described in the [documentation](https://github.com/rocker-org/rocker/wiki) for that image.

## Getting Started ##

Follow these steps to get your own Docker container instance:

1. Issue this command to clone the repository into a new directory:
  - git clone https://github.com/ibmdbanalytics/dashdb_analytic_tools.git
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
  - The last of these commands returns the IP address of the RStudio container in Bluemix. For more information about Bluemix containers, refer to this [documentation](https://www.ng.bluemix.net/docs/containers/container_cli_reference_cfic.html).
4. To launch the RStudio web UI:
  * On a Linux system, point your browser to `<ip_addr>:8787`, where `<ip_addr>` represents the IP address of the Linux system that hosts the RStudio container.  
  * On a Windows or Mac system, use the [Docker Toolbox] (https://www.docker.com/products/docker-toolbox) to create a Docker environment on you computer in which you can run Docker commands and containers.
5. Log in to RStudio. The default user and password are both **rstudio**. For security, change the password immediately after you log in for the first time.

## Running a sample R script ##

The docker file above creates a directory samples in the user home directory. You can run the samples in this directory directly, just modify the user, password and host variables in the upper part of script to the ones that reflect the database you are connecting to. If you use IBM dashDB on BlueMix, then all sample data is already preloaded. If you run against a different system, you might need to upload some sample data before running the samples. To do so, upload the three CSV files above to tables in your database, using the table names SAMPLES.SHOWCASE_SYSTYPES, SAMPLES.SHOWCASE_SYSUSAGE and SAMPLES.SHOWCASE_SYSTEMS. If you choose different table names, you have to modify the script where indicated.

## Status ##

This is work in progress. For any request please contact torsten@de.ibm.com or MWURST@de.ibm.com.

## License ##

The docker file above and the content of the samples directory are provided under the GPL v2 or later. 

## Base Docker Containers ##

| Docker Container Source on GitHub             | Docker Hub Build Status and URL
| :---------------------------------------      | :-----------------------------------------
| r-base (base package to build from)           | [good](https://registry.hub.docker.com/u/rocker/r-base/)
| rstudio (base plus RStudio Server)            | [good](https://registry.hub.docker.com/u/rocker/rstudio/)
