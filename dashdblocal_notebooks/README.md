# Building and deploying a Jupyter notebook container for dashDB local

## Overview

This project generates a Docker image that is based on the
[jupyter/base-notebook](https://github.com/jupyter/docker-stacks/tree/master/base-notebook) image,
providing a [Jupyter notebook](http://jupyter.org/) container for
[dashDB local](http://www.ibm.com/analytics/us/en/technology/cloud-data-services/dashdb-local/).
It supports execution of Spark/Scala and Spark/Python kernels in the Apache Spark environment provided
by dashDB local.

Unlike the Spark notebooks in
[jupyter/docker-stacks](https://github.com/jupyter/docker-stacks), there is no Apache Spark installation
in the notebook container, all Spark driver and executor processes run in the dashDB local
Spark environment. The Spark applications can access dashDB data easily and efficiently
and you do not need to maintain version compatibility between Spark installations in
multiple containers.

Using this container requires a dashDB local installation where the integrated Spark support has been enabled.

### Update: IPython kernel support

While Spark/Scala support uses the [Apache Toree](https://toree.incubator.apache.org/) kernel,
Spark/Python support now attempts to use the more common [IPython](https://ipython.org/) kernel, thus
enabling the use of IPython magics and particularly graphic output from Python notebook cells.

Since IPython is not normally installed in a dashDB local image, the notebook container checks IPython
availablilty on startup and, if needed, tries to install IPython into the python environment of the
configured user via `pip install --user ipykernel`.

## PowerPC

The `base-notebook` image used by the Dockerfile is not pre-built for the
PowerPC architecture. It is therefore necessary to build it manually on machines
using the PowerPC architecture:

1. Log in to a host machine that hosts a dashDB local SMP installation or to the head node of a MPP installation.

2. Install a Git client in your path, see https://git-scm.com/downloads. You can perfom this and
 the following clone step as either the root user or a normal system user. When working as root user,
 run an `umask 0022` before cloning the repository, to avoid stripping file permissions from the
 local repository files.

3. Issue the following command to clone the repository into a new directory:

  `git clone https://github.com/jupyter/docker-stacks.git`

 This creates a new directory **docker-stacks** with subdirectory base-notebook.

4. Switch to the `base-notebook` directory.

  `cd docker-stacks/base-notebook`

4. As root user, build the `base-notebook` image:

  `docker build -t base-notebook -f Dockerfile.ppc64le .`

5. Continue with the steps below.

## Getting started

Follow these steps to get your own Docker container instance:

1. Log in to a host machine that hosts a dashDB local SMP installation or to the head node of a MPP installation.

2. Install a Git client in your path, see https://git-scm.com/downloads. You can perfom this and
 the following clone step as either the root user or a normal system user. When working as root user,
 run an `umask 0022` before cloning the repository, to avoid stripping file permissions from the
 local repository files.

3. Issue the following command to clone the repository into a new directory:

  `git clone https://github.com/ibmdbanalytics/dashdb_analytic_tools.git`

 This creates a new directory **dashdb_analytic_tools** with subdirectory dashdblocal_notebooks.

4. Switch to the `dashdblocal_notebooks` directory.

  `cd dashdb_analytic_tools/dashdblocal_notebooks`

5. As root user, build the image (for non-PowerPC architectures):

  `docker build -t dashdblocal_notebook .`

  For PowerPC-based systems, use:

  `docker build -t dashdblocal_notebook -f Dockerfile.ppc64le .`

6. As root user, start a notebook container, specifying the user name and the password of a user that you have created
 inside the dashDB installation (e.g. bluadmin). The provided user credentials are used to submit Spark applications
 to dashDB, so your notebooks will execute with the credentials of this user.

  `docker run -it --rm --net=host -e DASHDBUSER=<user> -e DASHDBPASS=<password> dashdblocal_notebook`

 It is recommended to start the container as a foreground process for the first time. If you have verified that the
 container works and want to run it as a background service, replace the `-it --rm`  arguments with `-d` and give it
 a name for easier referencing:

  `docker run -d --net=host -e DASHDBUSER=<user> -e DASHDBPASS=<password> --name <user>_notebook dashdblocal_notebook`


 Note that the dashDB local container as well as the notebook container use `--net=host` so they share
 the same network devices (fortunately, there are no port conflicts). In particular, the Jupyter server "sees" the
 kernel's communication ports on localhost

7. Open the Jupyter start page `http://<hostname>:8888` in a browser, where <hostname> is the external hostname or IP of
 the docker host and the dashDB system running on it. This can be done as any user from any system.

 If the message from `docker run` above indicates that the Jupyter server is started and listening on
 port 8888, but you cannot connect, then this may be caused by a firewall setup on your docker host. Since
 we're running with --net=host, docker will not create iptables rules automatically to ACCEPT connections
 on that port and you may need to configure that manually according to your docker host OS, e.g. with

  `iptables -A INPUT -p tcp --dport 8888 -j ACCEPT`

 When you see the Jupyter start page, log in using the password for the dashDB user (the one you specified
 as DASHDBPASS) and open the Spark_KMeansSample.ipynb notebook.
 Watch the output of the notebook container while the notebook kernel launches a kernel application inside dashDB
 and the browser title for the notebook still displays "(Starting) <notebook name>".
 Note that it can take more than a minute before the kernel is fully started and responsive.

8. Run the sample notebook to verify that you can access the dashDB database and perform Spark
analytics modeling.

## Shutting down

To shut down the notebook server and the container, press Ctrl-C from the console and confirm with 'y'
when running the container as a foreground process.
For containers running as a daemon process, use `docker stop <container-name>`.
Stopped containers can be re-started; use the `docker rm` command to dispose them.
Use `docker ps -a` to find the names of all containers, including stopped ones.
See the [https://docs.docker.com](docker documentation) for more information on managing containers.

Note: Running `docker kill` or `docker rm -f` while notebooks are still open
will terminate the container without giving it a chance to stop the associated Spark kernels running in dashDB.
This will lead to stale spark applications that consume resources in dashDB. Use the monitoring facilities of
dashDB (see below) to locate and kill stale "IBM Spark Kernel" applications.


## Monitoring

Use `docker logs <container-name>` to see the Jupyter log output for a background container.

In the dashDB local web console you can find a tab for Spark under Monitor->Workloads. From there, you can launch
the Apache Spark monitoring web UI. The Toree Spark kernel used by the Notebook can be monitored
with the application name "IBM Spark Kernel" (for Toree) or "IPython Notebook" (for IPython).

To see the output of the Spark kernel, first note its submission ID from the docker logs:
  `docker logs <notebook-container-name> | grep "Started Spark kernel"`
Then download the logs using the dashDB REST API with
  `curl -k -v -u <user>:<password> https://<host>:8443/dashdb-api/home/spark/log/submission_<ID>/submission.out`


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

The second option will download a complete SBT project generated from your application to your local system.
You can use this as a starting
point to extend the Spark application in a local Scala/SBT development environment. The project is pre-compiled and
includes two additional command line scripts:

* upload_<appname>.sh  uploads the packaged application to dashDB local
* submit_<appname>.sh  launches the application in the dashDB local Spark environment

Before you run the scripts, edit the settings.sh script that provides the environment variables to
connect to dashDB local from your local system

In order to flag certain cells to NOT be exported because they contain e.g. visualization or interaction elements or because they have some Jupyter magics that won't work in a standalone Spark application you can add the comment
  `//NOT-FOR-APP`
in these cells.

# Additional configuration options

## Running multiple containers

Jupyter notebook server is a single-user application, but you can run multiple notebook containers for
different users. The default notebook port is 8888, Jupyter notebook will retry with incrementing port
numbers if you start more than one notebook container on the same server, so the next notebook container
will connect at 8889 etc.

If you want to explicitly set the notebook port when running multiple containers with `--net=host`,
append the the container launch script `launch-with-idax.sh`
and the `--port` argument and. Launch script arguments are passed through to the
Jupyter notebook command, see https://jupyter-notebook.readthedocs.io/en/latest/config.html for possible options.

  `docker run -it --rm --net=host -e DASHDBUSER=<user> -e DASHDBPASS=<password> dashdblocal_notebook launch-with-idax.sh --port=9999`

## Storing notebooks outside the container

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

  `docker run -v /mnt/clusterfs/home/bluuser1/work:/home/jovyan/work -e NB_UID=5003 --user=root -e DASHDBUSER=bluuser1 -e DASHDBPASS=blupass1 -it --rm --net=host dashdblocal_notebook`

  Notebooks are now stored in /mnt/clusterfs/home/bluuser1/work, which is inside the home folder
  of user bluuser1 in the dasdDB container. The directory is created if it does not exist.

## HTTPS support and other options from jupyter/base-notebook

Most of the configuration options supported by the base image
[jupyter/base-notebook](https://github.com/jupyter/docker-stacks/tree/master/base-notebook#docker-options)
also apply to this notebook container. You can specify `-e USE_HTTPS=yes` to switch
the notebook server to HTTPS with a self-signed certificate and you can use the process
described there for installing your own certificate.

## Remote kernel

The notebook container also includes basic support for remote kernels by forwarding the Jupyter notebook
communication ports. So instead of running it on the same docker host that hosts the dashDB container,
you can run it on any machine.

  `docker run -it --rm -p 8888:8888 -e DASHDBHOST=<dashDB-hostname> -e DASHDBUSER=<user> -e DASHDBPASS=<password> dashdblocal_notebook`

Note the missing --net=host and and the DASHDBHOST env variable.

The port forwarding mechanism is quite basic and has shown to be unstable under some conditions.
Running the notebook container on the same docker host with `--net=host` is currently the preferred approach.


# Limitations

## Limited number of parallel Spark applications

The number of Spark applications that can execute in parallel on a Spark cluster is limited by the available memory.
This limit also applies to Spark notebook kernels. On dashDB local, the maximum number of all parallel Spark applications
(including notebooks) for _all users_ is usually 3 to 5, depending on the system configuration.

When that number has been reached, starting additional Spark kernels will fail and you see a message in your notebook
that the "Kernel has failed and could not be restarted". Unfortunately, Jupyter does not currently allow kernels to report
error information when they fail to start, so you can only diagnose the problem by looking at the notebook server log with
`docker log <container-name>`. If the maximum number of parallel Spark applications has been exceeded, you should see
a message like the following:

  `Failed to submit Spark kernel job: {"statusDesc":"Attempt to submit the application failed because the maximum number of running applications has already been reached.` ...

Note: be sure to shut down Spark kernels when you are finished with a notebook, either by selecting
"File -> Close and Halt" in the Notebook window or by marking the notebook and selecting "Shutdown"
from the main notebook server view.
You can also kill "orphaned" Spark kernel applications from the Spark monitoring page; see the information above under
[Monitoring](#monitoring)


## Kernel interrupt

Currently, we have no way to forward an interrupt signal to the notebook kernel which runs in a different container
without a terminal. Therefore kernel interrupting is not supported and has no effect.
