# dashdb_analytic_tools

## Overview ##

This project generates a Docker image that extends the [rocker/rstudio](https://github.com/rocker-org/rocker/tree/master/rstudio) image by dashDB specific components, such as IBM Data Server Driver packagesd and ibmdbR and ibmdbRXt packages for R. For basic image usage the same [documentation](https://github.com/rocker-org/rocker/wiki) like to the base image applies.

The intention is to extend the image further with other analytical tools suited for dashDB.

## Getting Started ##

Follow these steps to get your own Docker container instance:

git clone https://github.com/ibmdbanalytics/dashdb_analytic_tools.git

docker build -t &#60;image name&#60; .

docker run -d -p 8787:8787 &#60;image name&#60;

###Bluemix
In case you want to use Bluemix to host your container for RStudio and dashDB use the below after your have clones the git repository to a local directory:

cf ic build -t registry.ng.bluemix.net/&#60;private namespace&#60;/&#60;image name&#60; .

cf ic run -p 8787 registry.ng.bluemix.net/&#60;private namespace&#60;/&#60;image name&#60;


You can figure out the IP address of the Bluemix container in Bluemix with cf ic ip <container id>


For more information on Bluemix containers refer to this [documentation](https://www.ng.bluemix.net/docs/containers/container_cli_reference_cfic.html)

## Status ##

This is work in progress. For any request please contact torsten@de.ibm.com or MWURST@de.ibm.com.

## Base Docker Containers ##

| Docker Container Source on GitHub             | Docker Hub Build Status and URL
| :---------------------------------------      | :-----------------------------------------
| r-base (base package to build from)           | [good](https://registry.hub.docker.com/u/rocker/r-base/)
| rstudio (base plus RStudio Server)            | [good](https://registry.hub.docker.com/u/rocker/rstudio/)
