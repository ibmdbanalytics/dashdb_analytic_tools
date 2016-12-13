FROM centos:7
## This handle reaches Torsten
MAINTAINER "Torsten Steinbach" torsten@de.ibm.com

RUN yum install -y \
  java-1.8.0-openjdk-headless \
  curl

WORKDIR /producer

ENV ZOOKEEPER_VERSION 3.4.8
ENV KAFKA_VERSION 0.10.1.0

# get zookeeper and unpack
RUN curl -S http://www-eu.apache.org/dist/zookeeper/zookeeper-${ZOOKEEPER_VERSION}/zookeeper-${ZOOKEEPER_VERSION}.tar.gz | tar -xz \
  && ln -s zookeeper-* zookeeper

# get kafka and unpack
RUN curl -S http://www-eu.apache.org/dist/kafka/${KAFKA_VERSION}/kafka_2.11-${KAFKA_VERSION}.tgz | tar -xz \
  && ln -s kafka_* kafka

COPY zoo.cfg zookeeper/conf
COPY start.sh /usr/local/bin

ENV JAVA_HOME=/etc/alternatives/jre
ENV PATH=$PATH:$JAVA_HOME/bin:/producer/kafka/bin

RUN chmod a+rx /usr/local/bin/start.sh

ENTRYPOINT ["start.sh"]
CMD ["1000"]
