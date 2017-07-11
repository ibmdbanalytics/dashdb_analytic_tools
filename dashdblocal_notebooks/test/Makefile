# (c) Copyright IBM Corporation 2016
# LICENSE: BSD-3, https://opensource.org/licenses/BSD-3-Clause

ifndef DASHDBHOST
$(error DASHDBHOST is not set)
endif
ifndef DASHDBUSER
$(error DASHDBUSER is not set)
endif
ifndef DASHDBPASS
$(error DASHDBPASS is not set)
endif

CONTAINER_NAME = test_dashdblocal_notebook
IMAGE_NAME = dashdblocal_notebook:dev

# need bash for the recipes
SHELL = /bin/bash
SUBMIT_SCRIPT = output/spark-submit.sh

ARCH := $(shell uname -m)

CONTAINER_CFG := -e DASHDBHOST=$(DASHDBHOST) -e DASHDBUSER=$(DASHDBUSER) -e DASHDBPASS=$(DASHDBPASS)
ifeq ($(DASHDBHOST), localhost)
	CONTAINER_CFG += --net=host
else
	CONTAINER_CFG += -p 8888:8888
endif

run-test: image
	# run test in a sub-make because we want to clean up after a test failure
	$(MAKE) start test; rc=$$?; $(MAKE) stop; exit $$rc

image: Dockerfile.$(ARCH)
	@echo -e '\n\n### Building docker image for $ARCH###'
	docker build --no-cache -t $(IMAGE_NAME) -f Dockerfile.$(ARCH) ..


# Default Dockerfile is for Intel, just copy
Dockerfile.x86_64: ../Dockerfile
	cp $< $@

# Patch Dockerfile for Power
# - patch FROM line Assuming that a local base-notebook image exists
# - comment "RUN echo ... /etc/apt/sources.list" command
Dockerfile.ppc64le: ../Dockerfile
	sed 's/FROM/FROM base-notebook\n#FROM/; s!\(RUN echo .* /etc/apt/sources.list\)!#\1!' < $< > $@

# start the test container
start:
	@echo -e '\n\n### Starting test container ###'
	# cleanup old stuff
	-docker rm -f $(CONTAINER_NAME)
	# fix permissions if we are root
	rm -rf output && mkdir -p output
	chmod -R a+rX .
	# launch docker container
	docker run -d -v `pwd`:/test --name=$(CONTAINER_NAME) $(CONTAINER_CFG) $(IMAGE_NAME)
	# wait for the container to start, write container output to stderr so we can see it
	@grep -m1 'The Jupyter Notebook is running' <(timeout 1m docker logs -f $(CONTAINER_NAME) 2>&1 | tee /dev/stderr)
	@echo "Started notebook container $(CONTAINER_NAME)"
	
# start the test container using bundler sources from the current directory,
# overriding the bundler code that was deployed at image build time
# useful when you are working on the bundler code; start the test container this way
# and run testcases directly from the command line while making code changes
start_dev:
	@echo '\n\n### Starting test container for development environment ###'
	# cleanup old stuff
	-docker rm -f $(CONTAINER_NAME)
	# launch docker container
	docker run -d -v `pwd`:/test -v `pwd`/../src:/src --name=$(CONTAINER_NAME) $(CONTAINER_CFG) $(IMAGE_NAME)
	# wait for the container to start, write container output to stderr so we can see it
	@grep -m1 'The Jupyter Notebook is running' <(timeout 1m docker logs -f $(CONTAINER_NAME) 2>&1 | tee /dev/stderr)
	@echo "Started notebook container $(CONTAINER_NAME)"
	docker exec $(CONTAINER_NAME) pip install -e /src/sparkapp_bundler
	
start_interactive:
	@echo '\n\n### Starting interactive container for development environment ###'
	# cleanup old stuff
	-docker rm -f $(CONTAINER_NAME)
	# launch docker container
	docker run -it --rm --entrypoint=bash -v `pwd`:/test -v `pwd`/../src:/src --name=$(CONTAINER_NAME) $(CONTAINER_CFG) $(IMAGE_NAME)
	
# stop and remove the test container
# Note: simply killing the container with rm -f will not shut down running kernels in Spark
# also shut down the Spark cluster to make sure we have no orphaned kernels left over
stop:
	@echo -e '\n\n### Cleaning up test container ###'
	-docker stop $(CONTAINER_NAME)
	-docker rm $(CONTAINER_NAME)
	@echo -e '\n\n### Stopping Spark cluster for $(DASHDBUSER) ###'
	curl -k -u $(DASHDBUSER):$(DASHDBPASS) -XPOST https://$(DASHDBHOST):8443/dashdb-api/analytics/public/cluster/deallocate

test: test_container_logs test_notebook_ui test_notebooks get_launcher test_bundlers


# check container logs for some output that we expect
test_container_logs:
	@echo -e '\n\n### Checking test container logs ###'
	docker logs test_dashdblocal_notebook 2>&1 | grep 'Loaded jupyter_cms_sparkapp' >/dev/null
	docker logs test_dashdblocal_notebook 2>&1 | grep 'Upload complete: {"result":{"filesUploaded"' >/dev/null

# a few simple checks that the notebook UI is up and running
test_notebook_ui:
	@echo -e '\n\n### Checking notebook UI in test container ###'
	DASHDBHOST=$(DASHDBHOST) DASHDBUSER=$(DASHDBUSER) DASHDBPASS=$(DASHDBPASS) python2 test_notebook_ui.py
	
# run the sample notebooks, test the kernel
test_notebooks:
	@echo -e '\n\n### Checking kernel and sample notebook ###'
	rm -rf output/notebooks && mkdir -p output/notebooks && chmod a+rwx output/notebooks
	docker exec $(CONTAINER_NAME) /test/test_notebooks.sh
	
# get spark-submit script from the dashDB server
get_launcher:
	curl -k -v -o $(SUBMIT_SCRIPT) -u $(DASHDBUSER):$(DASHDBPASS) https://$(DASHDBHOST):8443/blushiftservices/userfiledownload.do?path=spark-submit.sh
	chmod a+rx $(SUBMIT_SCRIPT)
	
# test the bundlers. need the downloaded spark-submit script in the PATH
test_bundlers:
	@echo -e '\n\n### Checking notebook bundlers ###'
	# add -ti here to see output more interactively and avoid buffering -- fails if started from Jenkins (no tty)
	docker exec $(CONTAINER_NAME) /bin/sh -c 'cd /test && export PATH=/test/output:$$PATH && python3 test_bundlers.py'