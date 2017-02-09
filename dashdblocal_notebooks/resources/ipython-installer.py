# (c) Copyright IBM Corporation 2016
# LICENSE: BSD-3, https://opensource.org/licenses/BSD-3-Clause

# script to check availablilty of IPython
# tries a "pip --user" install if IPython is not found

import sys

# Currently, throwing an exception is the only way to return info
# directly to the caller of the dashDB Spark REST API
# So we're disguising our success messages as exceptions...
class Success(Exception):
    def __init__(self, msg):
        self.msg = msg
    def __str__(self):
        return self.msg

try:
    import ipykernel
    raise Success("IPython available at {0}\n".format(ipykernel.__file__))
except ImportError:
    print("IPython not found, trying to install...\n")
    import pip, os
    pip.main(['install', "--user", "ipykernel"])
    print("...successfully installed\n")
    raise Success("IPython installed as {0}".format(os.environ.get("USER")))
