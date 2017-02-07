#!/bin/sh
# (c) Copyright IBM Corporation 2016
# LICENSE: BSD-3, https://opensource.org/licenses/BSD-3-Clause

set -e

NBCONVERT_OPTIONS="--to=markdown --ExecutePreprocessor.enabled=True --Application.log_level=DEBUG"
WORKDIR=/test/output/notebooks

# nvbconvert always writes to the same directory where the notebooks are located
# so copy them to the test directory
mkdir -p $WORKDIR
cp *.ipynb $WORKDIR

# run nbconvert to execute the notebooks with the Spark kernel in headless mode
for notebook in $WORKDIR/*.ipynb; do
    cmd="jupyter nbconvert $NBCONVERT_OPTIONS $notebook"
    echo "Processing test notebook $notebook: $cmd"
    $($cmd)
    # When nbconvert kills the kernel wrapper, the actual Spark app keeps running.
    # As a hack to avoid filling our cluster and running out of free apps, we shut down the entire
    # Spark cluster after each converted notebook
    curl -k -u $DASHDBUSER:$DASHDBPASS -XPOST https://$DASHDBHOST:8443/dashdb-api/analytics/public/cluster/deallocate
done


