#!/usr/bin/env bash
# (c) Copyright IBM Corporation 2016
# LICENSE: BSD-3, https://opensource.org/licenses/BSD-3-Clause

# verifies that required environment variables are defined and we can connect
# to dashDB analytics REST API on target host
verify-sparkenv.py || exit 1

# upload toree server to dashDB spark environment
upload-sparkapp.py /usr/local/lib/toree.jar || exit 1

# call base startup script
. /usr/local/bin/start-notebook.sh

