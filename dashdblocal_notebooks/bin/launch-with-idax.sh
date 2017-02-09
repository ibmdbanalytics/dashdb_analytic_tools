#!/bin/bash
# (c) Copyright IBM Corporation 2016
# LICENSE: BSD-3, https://opensource.org/licenses/BSD-3-Clause

set -e

# verifies that required environment variables are defined and we can connect
# to dashDB analytics REST API on target host
verify-sparkenv.py

# upload toree server and ipython scripts to dashDB spark environment
upload-sparkapp.py $HOME/resources/toree.jar
upload-sparkapp.py $HOME/resources/ipython-launcher.py
upload-sparkapp.py $HOME/resources/ipython-installer.py
upload-sparkapp.py $HOME/resources/startup-ipython-notebook.py

# select appropriate python kernel, default to IPython
PYTHON_KERNEL=kernel-ipython
if [ -n "$PYSPARK_OVER_TOREE" ]; then
    echo "Toree selected for Python notebooks; some Python notebook functions are limited"
    PYTHON_KERNEL=kernel-toree
else
    echo "Checking IPython availablility. This may take some time on the first attempt..."
    if ! verify-ipython-in-dashdb.py; then
        echo "Warning: No IPython available in dashDB; some Python notebook functions are limited"
        PYTHON_KERNEL=kernel-toree
    fi
fi
# overwrite kernel.json to use toree instead of ipython
cp $HOME/.local/share/jupyter/kernels/idax-python/$PYTHON_KERNEL.json $HOME/.local/share/jupyter/kernels/idax-python/kernel.json



# patch Jupyter UI to display dashDB user
patch-ui.py

# call base startup script
. /usr/local/bin/start.sh jupyter notebook $*

