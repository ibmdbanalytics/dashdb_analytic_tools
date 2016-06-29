#!/usr/bin/env bash

# call upload script. also verifies that required environment variables are defined
# and target host exists
idaxnotebook-setup.py /opt/conda/share/jupyter/kernels/toree.jar || exit 1

# call base startup script
. /usr/local/bin/start-notebook.sh

