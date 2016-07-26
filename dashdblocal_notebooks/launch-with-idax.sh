#!/usr/bin/env bash
# (c) Copyright IBM Corporation 2016   
# LICENSE: Apache V2, https://opensource.org/licenses/Apache-2.0

# call upload script. also verifies that required environment variables are defined
# and target host exists
upload-sparkapp.py /usr/local/lib/toree.jar || exit 1

# call base startup script
. /usr/local/bin/start-notebook.sh

