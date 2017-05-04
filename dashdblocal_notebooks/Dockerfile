# (c) Copyright IBM Corporation 2016
# LICENSE: BSD-3, https://opensource.org/licenses/BSD-3-Clause

# Jupyter notebook server for connecting to dashDB local Spark

# To build on Power instead of x86
# - manually build the base image from https://github.com/jupyter/docker-stacks/tree/master/base-notebook
#   using Dockerfile.ppc64
# - change the FROM clause below to specify your base image
# - remove the first RUN statement updating sources.list

FROM jupyter/base-notebook@sha256:5d2090dfb04036ec32c8c4632bb0368ffcb9a304f98e811a6386ef1c9ad010bf
USER root

# Following line is needed to install OpenJDK with the debian base of jupyter/base-notebook
# remove for Power builds (ubuntu-based)
RUN echo "deb http://cdn-fastly.deb.debian.org/debian jessie-proposed-updates main" >> /etc/apt/sources.list

# sort packages alphabetically following docker convention
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       curl \
       default-jre-headless \
       unzip \
       zip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# sbt is not in apt repo
RUN cd /tmp && \
	wget -nv https://bintray.com/artifact/download/sbt/debian/sbt-0.13.11.deb && \
	dpkg -i sbt-0.13.11.deb && \
	rm *.deb

# don't need to download a debian packaged scala interpreter; sbt will get all we need
# wget -nv www.scala-lang.org/files/archive/scala-2.11.8.deb

# first start of sbt downloads maven dependencies -- do that early in the docker buid process
# need to define correct scalaVersion and dependencies for Spark before we start downloading
COPY build.sbt.template tmp/build.sbt
COPY plugins.sbt tmp/project/
RUN chown -R $NB_USER tmp
USER $NB_USER
RUN cd tmp &&  \
	mkdir -p src/main/scala && \
	echo "object Dummy {}" > src/main/scala/Dummy.scala && \
	echo "Note: downloading sbt may seem to be stuck for a few minutes, be patient" && \
	sbt assembly && \
	cd .. && rm -rf tmp

# set up jupyter environment
# widgetsnbextension needed to avoid warning during notebook start
RUN pip install 'jupyter_cms<0.7.0' widgetsnbextension && \
	jupyter cms quick-setup --sys-prefix


USER root

ENV PROJECTS_DIR /home/$NB_USER/projects

# copy other files late in the build to avoid cache busting
COPY bin/* /usr/local/bin/
COPY resources/* /home/$NB_USER/resources/
COPY jupyter /home/$NB_USER/.local/share/jupyter/
COPY *.ipynb ./
COPY build.sbt.template build.sh $PROJECTS_DIR/
COPY plugins.sbt $PROJECTS_DIR/sparkapp/project/

# copy jupyter CMS extensions
COPY src /src

# fix permissions if git repo was checked out as root
# fix ownership for all files copied into homedir
RUN chmod -R a+rX /src && \
	chmod a+rx /usr/local/bin/* && \
	chown -R $NB_USER /home/$NB_USER

USER $NB_USER

# set up template project
RUN bash -c "mkdir -p $PROJECTS_DIR/sparkapp/src/main/{java,scala,resources}" && \
	cp $PROJECTS_DIR/build.sh $PROJECTS_DIR/sparkapp/

# install and enable spark app bundler
RUN pip install /src/sparkapp_bundler && \
	jupyter serverextension enable --py jupyter_cms_sparkapp --sys-prefix && \
	jupyter bundler enable --py jupyter_cms_sparkapp --sys-prefix

# set DASHDBPASS as notebook login password
RUN echo "from IPython.lib import passwd\nc.NotebookApp.password = passwd(os.environ['DASHDBPASS'])" >> ~/.jupyter/jupyter_notebook_config.py


# put our setup on top of the base image startup script
CMD ["launch-with-idax.sh"]
