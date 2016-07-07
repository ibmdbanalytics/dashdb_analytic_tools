FROM jupyter/base-notebook
# tested with jupyter/base-notebook ID 27f6af6e1dcc

USER root

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    unzip zip 

RUN wget https://bintray.com/artifact/download/sbt/debian/sbt-0.13.11.deb && \
    apt-get -y install default-jre-headless && \
    dpkg -i sbt-0.13.11.deb && \
    apt-get -y update && \
    apt-get -y install sbt && \
    sbt about && \
    wget www.scala-lang.org/files/archive/scala-2.11.8.deb && \
    dpkg -i scala-2.11.8.deb && \
    apt-get -y update && \
    apt-get -y install scala && \
    mkdir -p /root/sparkapp/src/main/java /root/sparkapp/src/main/resources /root/sparkapp/src/main/scala/com/ibm/idax/spark/examples

USER jovyan

COPY build.sbt.template build.sbt.template 
COPY build.sh build.sh 

RUN mkdir -p /opt/conda/share/jupyter/kernels/idax-scala /opt/conda/share/jupyter/kernels/idax-python
RUN mkdir -p sparkapp/src/main/java sparkapp/src/main/resources sparkapp/src/main/scala/com/ibm/idax/spark/examples

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

