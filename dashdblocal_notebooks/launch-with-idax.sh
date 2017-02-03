#!/usr/bin/env bash
# (c) Copyright IBM Corporation 2016
# LICENSE: BSD-3, https://opensource.org/licenses/BSD-3-Clause

# verifies that required environment variables are defined and we can connect
# to dashDB analytics REST API on target host
verify-sparkenv.py || exit 1

# upload toree server and ipython scripts to dashDB spark environment
upload-sparkapp.py /usr/local/lib/toree.jar || exit 1
upload-sparkapp.py /usr/local/bin/ipython-launcher.py || exit 1
upload-sparkapp.py /usr/local/bin/startup-ipython-notebook.py || exit 1

# patch Jupyter UI to display dashDB user
patch-ui.py

# call base startup script
. /usr/local/bin/start.sh jupyter notebook $*

