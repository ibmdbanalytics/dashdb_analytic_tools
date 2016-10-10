# (c) Copyright IBM Corporation 2015
# LICENSE: GPL-2.0, https://opensource.org/licenses/GPL-2.0

## Start with the official rocker image providing 'base R'
FROM rocker/rstudio:latest
## This handle reaches Torsten
MAINTAINER "Torsten Steinbach" torsten@de.ibm.com

COPY supervisor.conf /supervisor.conf
COPY install.R /install.R
COPY ibm_data_server_driver_package_linuxx64_v11.1.tar.gz /

## Install some system commands
## Install ibmdbR and RODBC from CRAN
## Install IBM data server package, install it and set up odbc.ini
RUN rm -rf /var/lib/apt/lists/ \
  && apt-get update \
  && apt-get -y install procps \
  && apt-get -y install unixodbc-dev \
  && (apt-get -y install ksh; true) \
  && apt-get -y install ssh \
  && apt-get -y install libxml2 \
  && R -f /install.R \
  && tar -xvzf ibm_data_server_driver_package_linuxx64_v11.1.tar.gz \
  && /bin/ksh dsdriver/installDSDriver \
  && printf "[DASHDB]\nDriver = /dsdriver/lib/libdb2o.so\n" >> /etc/odbc.ini \
  && adduser rstudio sudo \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/

ADD samples /home/rstudio/samples

## Copy and call startup script
COPY startup.sh /tmp/startup.sh
CMD ["/bin/bash", "/tmp/startup.sh"]

## Add ssh deamon to startup sequence
##RUN cat /supervisor.conf >> /etc/supervisor/conf.d/supervisord.conf
