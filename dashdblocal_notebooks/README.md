# Building and deploying a Jupyter notebook container for dashDB local

## Overview ##

This project generates a Docker image that is based on the
[jupyter/base-notebook](https://github.com/jupyter/docker-stacks/tree/master/base-notebook) image,
providing a [Jupyter notebook](http://jupyter.org/) container for
[dashDB local](http://www.ibm.com/analytics/us/en/technology/cloud-data-services/dashdb-local/).
It supports execution of Spark/Scala and Spark/Python kernels in the Apache Spark environment provided
by dashDB local, using the [Apache Toree](https://toree.incubator.apache.org/) kernel.

Unlike the Spark notebooks in
[jupyter/docker-stacks](https://github.com/jupyter/docker-stacks), there is no Apache Spark installation
in the notebook container, Spark driver and executor processes run in the dashDB local
Spark environment. The Spark applications can access dashDB data easily and efficiently
and there are no versioning issues between Spark components running in different containers.

Using this container requires a dashDB local installation where the integrated Spark support has been enabled.

## Getting started ##

Follow these steps to get your own Docker container instance:

1. Log in to a host machine that hosts a dashDB local SMP installation or to the head node of a MPP installation.

1. Install a Git client in your path.

2. Issue this command to clone the repository into a new directory:

  `git clone https://github.com/ibmdbanalytics/dashdb_analytic_tools.git`

 This creates a new directory **dashdb_analytic_tools** with subdirectory dashdblocal_notebooks.
 Change to the dashdblocal_notebooks subdirectory.

3. As a user with root authority, build the image:

  `docker build -t <image name> <path to your dashdblocal_notebooks directory>`

4. Start a notebook container, specifying the user name and the password of a user that you have created
 inside the dashDB installation (e.g. bluadmin)

  `docker run -it --rm --net=host -e DASHDBUSR=<user> -e DASHDBPW=<password> <image name>`

 Note that the dashDB local container as well as the notebook container use `--net=host` so they share
 the same network devices (fortunately, there are no port conflicts). In particular, the Jupyter server "sees" the
 kernel's communication ports on localhost

6. Open the Jupyter start page http://<hostname>:8888 in your browser. In the upper right of the start page,
 click "New" -> "IDAX - Scala" to open a new notebook. Watch the output of the notebook container while the
 notebook kernel launches a toree server inside dashDB. Note that it can take more than a minute before the
 kernel is fully started and responsive.

7. You can now enter `println(sc.getConf.toDebugString)` in a notebook cell to verify your settings (e.g. the
 active class path) and `java.sql.DriverManager.getConnection("jdbc:db2:BLUDB")` to check that you can connect
 to the dashDB database.

To shut down the notebook server and the container, press Ctrl-C from the console
or use `docker stop <container>` from a different terminal
If you have verified that the container works and want to run it as a background service, replace the `-i --rm`
arguments with `-d`

## Monitoring

In the dashDB local web console you can find under Monitor->Workloads a tab for Spark. From there you can launch
the Apache Spark monitoring web UI. The Toree Spark kernel used by the Notebook can be accessed there to be monitored
with the application name "IBM Spark Kernel".

# Using Spark in notebooks

## Sample notebook

The container provides a sample notebook for Spark/Scala, which shows how to run Spark analytics algorithms on dashDB
data stored in dashDB local

## Exporting a Spark/Scala application

The notebook menu has two options for exporting notebooks as packaged Spark/Scala applications:

1. File -> Deploy as -> Deploy to dashDB Spark
2. File -> Download as -> Spark SBT project

The first option will compile your notebook into a stand-alone Spark application and upload the resulting .jar file
to the spark/apps directory of the dashDB local user. You can then use the dashDB local REST API to launch the
application.

The second option will download a complete SBT project generated from your application. You can use this as a starting
point to extend the Spark application in a local Scala/SBT development environment. The project is pre-compiled and
includes two additional command line scripts:

* upload-<appname>.sh  uploads the packaged application to dashDB local
* run-<appname>.sh  launches the applcation in the dashDB local Spark environment

Both scripts require that you have the `DASHDBUSR` and `DASHDBPW` environment variables set and specify the target
dashDB installation with the `DASHDBHOST` environment variable


# Additional configuration options

## Running multiple containers ##

Jupyter notebook server is a single-user application, but you can run multiple notebook containers for
different users. The default notebook port is 8888, Jupyter notebook will retry with incrementing port
numbers if you start more than one notebook container on the same server, so the next notebook container
will connect at 8889 etc.

If you want to explicitly set the notebook port when running multiple containers with `--net=host`, append the
`--port` argument and the container launch script. Launch script arguments are passed through to the
Jupyter notebook command, see https://jupyter-notebook.readthedocs.io/en/latest/config.html for possible options.

  `docker run -it --rm --net=host -e DASHDBUSR=<user> -e DASHDBPW=<password> <image name> launch-with-idax.sh --port=9999`

## Storing notebooks outside the container ##

The default configuration of the notebook container will store notebook files within the container.
This means that the files are removed along with your container. You can keep the files on a mounted volume
to preserve them across containers. As you are running on the same docker host as the dashDB local image,
the recommended place for keeping the files is the user's home directory:

1. Find the source volume where the use home is mounted in the dashDB container:

  `docker inspect <dashDB-container> | grep -B 1 'Destination.*/blumeta0`

  `"Source": "/mnt/clusterfs",<br>"Destination": "/mnt/blumeta0",`

  shows that home directory is mounted from /mnt/clusterfs.

2. Find the userid of the notebook target user (e.g. bluuser1) in the dashDB container:

  `> docker exec -t <dashDB-container> /usr/bin/id -u bluuser1`

  `5003`

3. Now add the following arguments when running the notebook container

  `docker run -v /mnt/clusterfs/home/bluuser1/notebooks:/home/jovyan/work -e NB_UID=5003 --user=root -e DASHDBUSR=bluuser1 -e DASHDBPW=blupass1 -it --rm --net=host <image name>`

  Notebooks are now stored in /mnt/clusterfs/home/bluuser1/notebooks, which corresponds to the home folder
  of user bluuser1 in the dasdDB container. The directory is created if it does not exist.

## Remote kernel ##

The notebook container also includes basic support for remote kernels by forwarding the Jupyter notebook
communication ports. So instead of running it on the same docker host that hosts the dashDB container,
you can run it on any machine.

  `docker run -it --rm -p 8888:8888 -e DASHDBHOST=<dashDB-hostname> -e DASHDBUSR=<user> -e DASHDBPW=<password> <image name>`

Note the missing --net=host and and the DASHDBHOST env variable.

The port forwarding mechanism is quite basic and has shown to be unstable under some conditions.
Running the notebook container on the same docker host with `--net=host` is currently the preferred approach.


## Limitations ##

Currently, we have no way to forward an interrupt signal to the Toree kernel which runs in a different container
without a terminal. Therefore Kernel interrupting is not supported and has no effect.
