FROM jupyter/base-notebook

USER root

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    unzip zip

USER jovyan

RUN pip install --pre toree

# modify log4.properties in toree so we get Spark INFO output expected by dashDB Spark support
RUN	cp /opt/conda/lib/python3.5/site-packages/toree/lib/toree-assembly-*.jar /opt/conda/share/jupyter/kernels/toree.jar
RUN cd /tmp && \
	unzip /opt/conda/share/jupyter/kernels/toree.jar log4j.properties && \
	echo "log4j.logger.org.apache.spark=INFO" >> log4j.properties && \
	zip -r /opt/conda/share/jupyter/kernels/toree.jar log4j.properties
RUN rm /tmp/log4j.properties

COPY run-toree.py /opt/conda/share/jupyter/kernels/
RUN mkdir /opt/conda/share/jupyter/kernels/idax-scala
COPY kernel-scala.json /opt/conda/share/jupyter/kernels/idax-scala/kernel.json
RUN mkdir /opt/conda/share/jupyter/kernels/idax-python
COPY kernel-python.json /opt/conda/share/jupyter/kernels/idax-python/kernel.json
COPY idaxnotebook-setup.py launch-with-idax.sh /usr/local/bin/

# default host for dashDB connection
ENV BLUHOST 127.0.0.1

# put our setup on top of the base image startup script
CMD ["launch-with-idax.sh"]

