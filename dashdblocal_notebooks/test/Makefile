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

CONTAINER_CFG := -e DASHDBHOST=$(DASHDBHOST) -e DASHDBUSER=$(DASHDBUSER) -e DASHDBPASS=$(DASHDBPASS)

all: image start test stop

# build the docker image
image:
	@echo -e '\n\n### Building docker image ###'
	docker build -t $(IMAGE_NAME) ..
	
# start the test container
start:
	@echo -e '\n\n### Starting test container ###'
	# cleanup old stuff
	-docker rm -f $(CONTAINER_NAME)
	# launch docker container
	docker run -d -p 8888:8888 -v `pwd`:/test --name=$(CONTAINER_NAME) $(CONTAINER_CFG) $(IMAGE_NAME)
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
	docker run -d -p 8888:8888 -v `pwd`:/test -v `pwd`/../src:/src --name=$(CONTAINER_NAME) $(CONTAINER_CFG) $(IMAGE_NAME)
	# wait for the container to start, write container output to stderr so we can see it
	@grep -m1 'The Jupyter Notebook is running' <(timeout 1m docker logs -f $(CONTAINER_NAME) 2>&1 | tee /dev/stderr)
	@echo "Started notebook container $(CONTAINER_NAME)"
	#
	docker exec $(CONTAINER_NAME) pip install -e /src/sparkapp_bundler
	
	
# stop and remove the test container
# Note: simply killing the container with rm -f will not shut down running kernels in Spark
stop:
	@echo -e '\n\n### Cleaning up test container ###'
	docker stop $(CONTAINER_NAME)
	docker rm $(CONTAINER_NAME)


test: test_container_logs test_notebook_ui test_notebooks get_launcher test_bundlers


# check container logs for some output that we expect
test_container_logs:
	@echo -e '\n\n### Checking test container logs ###'
	docker logs test_dashdblocal_notebook 2>&1 | grep 'Loaded jupyter_cms_sparkapp' >/dev/null
	docker logs test_dashdblocal_notebook 2>&1 | grep 'Upload complete: {"result":{"filesUploaded"' >/dev/null

# a few simple checks that the notebook UI is up and running
test_notebook_ui:
	@echo -e '\n\n### Checking notebook UI in test container ###'
	DASHDBHOST=$(DASHDBHOST) DASHDBUSER=$(DASHDBUSER) DASHDBPASS=$(DASHDBPASS) python3 test_notebook_ui.py
	
# run the sample notebooks, test the kernel
test_notebooks:
	@echo -e '\n\n### Checking kernel and sample notebook ###'
	rm -rf output/notebooks && mkdir -p output/notebooks && chmod a+w output/notebooks
	docker exec -ti $(CONTAINER_NAME) /test/test_notebooks.sh
	
# get spark-submit script from the dashDB server
get_launcher:
	ssh root@$(DASHDBHOST) docker cp idaxDashDB:/opt/ibm/dashdb_spark/bin/spark-submit.sh /tmp/
	scp root@$(DASHDBHOST):/tmp/spark-submit.sh output/
	
# test the bundlers. need the downloaded spark-submit script in the PATH
test_bundlers:
	@echo -e '\n\n### Checking notebook bundlers ###'
	docker exec -ti $(CONTAINER_NAME) /bin/sh -c 'cd /test && export PATH=/test/output:$$PATH && python3 test_bundlers.py'