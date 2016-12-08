FROM centos:7
## This handle reaches Torsten
MAINTAINER "Torsten Steinbach" torsten@de.ibm.com

RUN yum install -y \
  java-1.8.0-openjdk-headless \
  curl

WORKDIR /producer

RUN curl -S http://www-eu.apache.org/dist/zookeeper/zookeeper-3.4.8/zookeeper-3.4.8.tar.gz | tar -xz \
  && ln -s zookeeper-* zookeeper

RUN curl -S http://www-eu.apache.org/dist/kafka/0.10.1.0/kafka_2.11-0.10.1.0.tgz | tar -xz \
  && ln -s kafka_* kafka

COPY zoo.cfg zookeeper/conf
COPY start.sh /usr/local/bin

ENV JAVA_HOME=/etc/alternatives/jre
ENV PATH=$PATH:$JAVA_HOME/bin:/producer/kafka/bin

ENTRYPOINT ["start.sh"]
CMD ["1000"]
