# Building and deploying an RStudio container for dashDB

## Overview ##

This project generates a Docker image that is based on the [rocker/rstudio](https://github.com/rocker-org/rocker/tree/master/rstudio) image but that includes additional dashDB-specific components, such as IBM Data Server Driver packages and the ibmdbR and ibmdbRXt packages for R. The components provided by the rocker/rstudio image are described in the [documentation](https://github.com/rocker-org/rocker/wiki) for that image.     For more information about RStudio, e.g. resource requirements, please refer to the [RStudio documentation](www.rstudio.com).

## Getting started ##

Follow these steps to get your own Docker container instance:

12. Install a Git client in your path, see [https://git-scm.com/downloads]. You can perfom this and
 the following clone step as either the root user or a normal system user. When working as root user,
 run an `umask 0022` before cloning the repository, to avoid stripping file permissions from the
 local repository files.

2. Issue this command to clone the repository into a new directory:

  `git clone https://github.com/ibmdbanalytics/dashdb_analytic_tools.git`

 This creates a new directory **dashdb_analytic_tools** with subdirectory dashdb_rstudio.
 Change to the dashdb_rstudio subdirectory.

3. Download the dashDB driver package **ibm_data_server_driver_package_linuxx64_v11.1.tar.gz** into the same dashdb_rstudio directory from either of the following sources:
  * From the dashDB web console:
    1. Log in with your dashDB credentials.
    2. Click **Connect > Download Tools**.
  * From the [IBM support web site] (http://www-01.ibm.com/support/docview.wss?uid=swg21385217):
    1. Select the package **IBM Data Server Driver Package (DS Driver)**.
    2. Log in with your IBM ID (sign-up is free).
    3. Select the offering **IBM Data Server Driver Package (Linux AMD64 and Intel EM64T)** for the Linux platform.
  * Make sure the downloaded file is really named **ibm_data_server_driver_package_linuxx64_v11.1.tar.gz**. Rename it if this is not the case before you continue with the build process. Be aware that *.gz files will be automatically extracted on some operation systems (OS X), however it is necessary to use the gzipped compressed package.
  
4. As a user with root authority, build the image:
  * If you want to build the image and run the container in your own Linux environment, issue these commands:
    - `docker build -t <image name> <path to your dashdb_rstudio directory>`
    - `docker run -d -p 8787:8787 <image name>`
  * If you want to use Bluemix to host your RStudio container, issue these commands:
    - `cf ic build -t registry.ng.bluemix.net/<private namespace>/<image name>  <path to your dashdb_rstudio directory>`
    - `cf ic run -p 8787 registry.ng.bluemix.net/<private namespace>/<image name>`
    - `cf ic ip`
  * If you already built the image locally you can push it to Bluemix like this:
    - `cf login`
    - `cf ic login`
    - `docker tag <image name> registry.ng.bluemix.net/<private namespace>/<image name>`
    - `docker push registry.ng.bluemix.net/<private namespace>/<image name>`

    The last of these commands returns the IP address of the RStudio container in Bluemix. Click [here] (https://www.ng.bluemix.net/docs/containers/container_cli_reference_cfic.html) for more information about Bluemix containers.

5. To launch the RStudio web UI:
  * On a Linux system, point your browser to `<ip_addr>:8787`, where `<ip_addr>` represents the IP address of the Linux system that hosts the RStudio container.
  * On a Windows or Mac system, use the [Docker Toolbox] (https://www.docker.com/products/docker-toolbox) to create a Docker environment on you computer in which you can run Docker commands and containers.
6. Log in to RStudio. The default user and password are both **rstudio**. For security, change the password immediately after you log in for the first time.

## Running a sample R script ##

The docker file you build in step #4 creates a "samples" directory in your home directory, with a sample scripts. You can load these samples directly from RStudio by opening the samples directory. To run any example you have to edit the file to contain the right host, user name and password variables according to your dashDB system.

Most samples upload their own data, however some expect the following tables to be present. This should be the case for dashDB aaS, but might not be true on other systems. If the data is not present, you need to upload it before running the samples using the following steps:

1. Download the following three CSV files:
   * [SHOWCASE_SYSTYPES.csv] (./SHOWCASE_SYSTYPES.csv)
   * [SHOWCASE_SYSUSAGE.csv] (./SHOWCASE_SYSUSAGE.csv)
   * [SHOWCASE_SYSTEMS.csv] (./SHOWCASE_SYSTEMS.csv)
2. Load the contents of these CSV files into the following tables in your database:
   * SHOWCASE_SYSTYPES
   * SHOWCASE_SYSUSAGE
   * SHOWCASE_SYSTEMS

If you choose different table names, modify the script to reflect these different names.

## Status ##

This is work in progress. For any request please contact torsten@de.ibm.com.

## License ##

The docker file above and the content of the samples directory are provided under the GPL v2 or later.

## Base Docker containers ##

| Docker Container Source on GitHub             | Docker Hub Build Status and URL
| :---------------------------------------      | :-----------------------------------------
| r-base (base package to build from)           | [good](https://registry.hub.docker.com/u/rocker/r-base/)
| rstudio (base plus RStudio Server)            | [good](https://registry.hub.docker.com/u/rocker/rstudio/)
