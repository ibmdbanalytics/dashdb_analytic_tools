# (c) Copyright IBM Corporation 2015
# LICENSE: GPL-2.0, https://opensource.org/licenses/GPL-2.0

## Start with the official rocker image providing 'base R'
FROM rocker/rstudio:latest
## This handle reaches Torsten
MAINTAINER "Torsten Steinbach" torsten@de.ibm.com

COPY supervisor.conf /supervisor.conf
COPY install.R /install.R
COPY ibm_data_server_driver_package_linuxx64_v10.5.tar.gz /

## Install some system commands
## Install ibmdbR and RODBC from CRAN
## Install IBM data server package, install it and set up odbc.ini
RUN rm -rf /var/lib/apt/lists/ \
  && apt-get update \
  && apt-get -y install procps \
  && apt-get -y install unixodbc-dev \
  && apt-get -y install ksh \
  && apt-get -y install ssh \
  && apt-get -y install libxml2 \
  && R -f /install.R \
##  && wget https://delivery04.dhe.ibm.com/sdfdl/v2/sar/CM/IM/05ug4/2/Xa.2/Xb.jusyLTSp44S0BvkRF-6duDE3qesroroRBMJdiMD4DvzE79MnOVFibW_Co8s/Xc.CM/IM/05ug4/2/v10.5fp7_linuxx64_dsdriver.tar.gz/Xd./Xf.LPR.D1vk/Xg.8476663/Xi.habanero/XY.habanero/XZ.WqDh2N0pS7knJ72Xe6qnGtcdc1o/v10.5fp7_linuxx64_dsdriver.tar.gz \
  && tar -xvzf ibm_data_server_driver_package_linuxx64_v10.5.tar.gz \
  && dsdriver/installDSDriver \
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
