# (c) Copyright IBM Corporation 2015
# LICENSE: GPL-2.0, https://opensource.org/licenses/GPL-2.0

## Start with the official rocker image providing 'base R'
FROM rocker/rstudio:latest
## This handle reaches Torsten
MAINTAINER "Torsten Steinbach" torsten@de.ibm.com

## Install some system commands
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    openjdk-8-jre-headless \
    libxml2 \
    mksh \
    procps \
    ssh \
    unixodbc-dev \
    && apt-get clean

## Install ibmdbR and RODBC from CRAN
COPY install.R /install.R
RUN R -f /install.R

## Install IBM data server package, install it and set up odbc.ini
COPY ibm_data_server_driver_package_linuxx64_v11.1.tar.gz /
RUN tar -xvzf ibm_data_server_driver_package_linuxx64_v11.1.tar.gz \
    && dsdriver/installDSDriver \
    && printf "[DASHDB]\nDriver = /dsdriver/lib/libdb2o.so\n" >> /etc/odbc.ini \
    && adduser rstudio sudo

ENV APACHE_SPARK_VERSION 2.0.0
ENV SPARK_HOME /usr/local/spark
RUN cd /tmp && \
        wget -q http://d3kbcqa49mib13.cloudfront.net/spark-${APACHE_SPARK_VERSION}-bin-hadoop2.7.tgz && \
        tar xzf spark-${APACHE_SPARK_VERSION}-bin-hadoop2.7.tgz -C /usr/local && \
        rm spark-${APACHE_SPARK_VERSION}-bin-hadoop2.7.tgz
RUN cd /usr/local && ln -s spark-${APACHE_SPARK_VERSION}-bin-hadoop2.7 spark

ADD samples /home/rstudio/samples

## Copy and call startup script
COPY startup.sh /tmp/startup.sh
CMD ["/bin/bash", "/tmp/startup.sh"]

## Add ssh deamon to startup sequence
##COPY supervisor.conf /supervisor.conf
##RUN cat /supervisor.conf >> /etc/supervisor/conf.d/supervisord.conf
