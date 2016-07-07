FROM jupyter/base-notebook
# tested with jupyter/base-notebook ID 27f6af6e1dcc

USER root

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    unzip zip default-jre-headless 

# sbt is not in repo for Trusty 
RUN cd /tmp && \
	wget -nv https://bintray.com/artifact/download/sbt/debian/sbt-0.13.11.deb && \
	dpkg -i sbt-0.13.11.deb && \
	rm *.deb

# don't need to download a debian packaged scala interpreter; sbt will get all we need
# wget -nv www.scala-lang.org/files/archive/scala-2.11.8.deb


USER jovyan

COPY build.sh build.sh 

# need to define correct scalaVersion and dependencies for Spark before we start downloading 
COPY build.sbt.template build.sbt 
# first start of sbt downloads mvn dependencies
RUN sbt about


RUN mkdir -p /opt/conda/share/jupyter/kernels/idax-scala /opt/conda/share/jupyter/kernels/idax-python
RUN mkdir -p sparkapp/src/main/java sparkapp/src/main/resources sparkapp/src/main/scala

RUN pip install --pre toree

# modify log4.properties in toree so we get Spark INFO output expected by dashDB Spark support
RUN	cp /opt/conda/lib/python3.5/site-packages/toree/lib/toree-assembly-*.jar /opt/conda/share/jupyter/kernels/toree.jar
RUN cd /tmp && \
	unzip /opt/conda/share/jupyter/kernels/toree.jar log4j.properties && \
	echo "log4j.logger.org.apache.spark=INFO" >> log4j.properties && \
	zip -r /opt/conda/share/jupyter/kernels/toree.jar log4j.properties
RUN rm /tmp/log4j.properties

COPY run-toree.py /opt/conda/share/jupyter/kernels/
COPY kernel-scala.json /opt/conda/share/jupyter/kernels/idax-scala/kernel.json
COPY kernel-python.json /opt/conda/share/jupyter/kernels/idax-python/kernel.json
COPY idaxnotebook-setup.py launch-with-idax.sh /usr/local/bin/

# put our setup on top of the base image startup script
CMD ["launch-with-idax.sh"]

