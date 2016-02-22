# dashdb_analytic_tools

## Overview ##

This project generates a Docker image that is based on the [rocker/rstudio](https://github.com/rocker-org/rocker/tree/master/rstudio) image but that includes additional dashDB-specific components, such as IBM Data Server Driver packages and the ibmdbR and ibmdbRXt packages for R. The components provided by the rocker/rstudio image are described in the [documentation](https://github.com/rocker-org/rocker/wiki) for that image.

## Getting Started ##

Follow these steps to get your own Docker container instance:

git clone https://github.com/ibmdbanalytics/dashdb_analytic_tools.git

Download the dashDB driver package ibm_data_server_driver_package_linuxx64_v10.5.tar.gz. You can download it either from the dashDB web console (Log in with your dashDB credentials and then: Connect > Download Tools) or from the IBM support web site: http://www-01.ibm.com/support/docview.wss?uid=swg21385217 (Select package "IBM Data Server Driver Package (DS Driver)", log in with your IBM ID - sign-up is free - and select offering "IBM Data Server Driver Package (Linux AMD64 and Intel EM64T)" with Platform "Linux").

Put the downloaded ibm_data_server_driver_package_linuxx64_v10.5.tar.gz into the same directory as the Dockerfile.

Now you can build the image:

docker build -t &#60;image name&#62; .

docker run -d -p 8787:8787 &#60;image name&#62;

Then point your browser to &#60;IP address&#62;:8787 in order to launch the RStudio web UI. The default user and pw is rstudio/rstudio.

###Bluemix
In case you want to use Bluemix to host your RStudio container for analtics of data in dashDB services use the below Bluemix cf commands instead of the plain docker commands after you have cloned the git repository to a local directory and downloaded the driver package as described above:

cf ic build -t registry.ng.bluemix.net/&#60;private namespace&#62;/&#60;image name&#62; .

cf ic run -p 8787 registry.ng.bluemix.net/&#60;private namespace&#62;/&#60;image name&#62;


You can figure out the IP address of the Bluemix container in Bluemix with cf ic ip <container id>


For more information on Bluemix containers refer to this [documentation](https://www.ng.bluemix.net/docs/containers/container_cli_reference_cfic.html)

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
