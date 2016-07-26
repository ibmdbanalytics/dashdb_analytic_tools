# (c) Copyright IBM Corporation 2016
# LICENSE: Apache V2, https://opensource.org/licenses/Apache-2.0

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


USER $NB_USER

# first start of sbt downloads maven dependencies -- do that early in the docker buid process
# need to define correct scalaVersion and dependencies for Spark before we start downloading
RUN mkdir tmp
COPY build.sbt.template tmp/build.sbt
USER root
RUN chmod -R a+rx tmp
USER $NB_USER
RUN cd tmp &&  \
	mkdir -p src/main/scala && \
	echo "object Dummy {}" > src/main/scala/Dummy.scala && \
	echo "Note: downloading sbt may seem to be stuck for a few minutes, be patient" && \
	sbt package
RUN rm -rf tmp

# set up jupyter environment
RUN pip install --pre toree
RUN pip install jupyter_cms
RUN jupyter cms quick-setup --sys-prefix


USER root

# modify log4.properties in toree so we get Spark INFO output expected by dashDB Spark support
RUN	cp /opt/conda/lib/python3.5/site-packages/toree/lib/toree-assembly-*.jar /usr/local/lib/toree.jar
RUN cd /tmp && \
	unzip /usr/local/lib/toree.jar log4j.properties && \
	echo "log4j.logger.org.apache.spark=INFO" >> log4j.properties && \
	zip -r /usr/local/lib/toree.jar log4j.properties
RUN rm /tmp/log4j.properties

ENV PROJECTS_DIR /home/$NB_USER/projects

# copy other files late in the build to avoid cache busting
COPY build.sbt.template build.sh $PROJECTS_DIR/
COPY kernel-scala.json /home/$NB_USER/.local/share/jupyter/kernels/idax-scala/kernel.json
COPY kernel-python.json /home/$NB_USER/.local/share/jupyter/kernels/idax-python/kernel.json
COPY upload-sparkapp.py run-sparkapp.py run-toree.py launch-with-idax.sh /usr/local/bin/
COPY Spark_KMeansSample.ipynb ./

# copy template project files
ADD src /src
RUN chmod -R a+rx /src

# don't rely on github to preserve exec permissions, set them explicitly
RUN chmod a+rx /usr/local/bin/*
# fix ownership for all files copied into homedir
RUN chown -R $NB_USER /home/$NB_USER

USER $NB_USER

# set up template project
RUN bash -c "mkdir -p $PROJECTS_DIR/sparkapp/src/main/{java,scala,resources}" && \
	cp /usr/local/bin/*-sparkapp.py $PROJECTS_DIR/sparkapp/ && \
	cp $PROJECTS_DIR/build.sh $PROJECTS_DIR/sparkapp/

RUN pip install /src/sparkapp_bundler

RUN jupyter serverextension enable --py jupyter_cms_sparkapp --sys-prefix
RUN jupyter bundler enable --py jupyter_cms_sparkapp --sys-prefix


# put our setup on top of the base image startup script
CMD ["launch-with-idax.sh"]
