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

# verifies that IPython can be used in the dashDB spark environment
verify-ipython-in-dashdb.py 

# patch Jupyter UI to display dashDB user
patch-ui.py

# call base startup script
. /usr/local/bin/start.sh jupyter notebook $*

