#!/usr/bin/env python3
# (c) Copyright IBM Corporation 2016
# LICENSE: BSD-3, https://opensource.org/licenses/BSD-3-Clause

# Use the dashDB analytics REST API to check that the dashDB Spark support
# is configured and accessible

import warnings
import sys, os
import json, requests
from requests.auth import HTTPBasicAuth
from requests.packages.urllib3.exceptions import InsecureRequestWarning

MINUMUM_BUILD_NUMBER = '140'
MINUMUM_DASHDB_LEVEL = '1.4.0'

def verify_sparkenv():
    auth = HTTPBasicAuth(DASHDBUSER, DASHDBPASS)
    resp = requests.get("https://{0}:8443/dashdb-api/analytics/public/configuration/version".format(DASHDBHOST),
        auth=auth, verify=False)
    if (resp.status_code == requests.codes.unauthorized):
        sys.exit("Could not authenticate to {0} as user {1}. Verify DASHDBUSER and DASHDBPASS information"
                .format(DASHDBHOST, DASHDBUSER))
    if (resp.status_code == requests.codes.not_found):
        # try accessing the old API endpoint
        resp2 = requests.get("https://{0}:8443/clues/public/configuration/version".format(DASHDBHOST),
                        auth=auth, verify=False)
        if (resp2.status_code == requests.codes.ok):
            newer_dashdb_required()
    if (resp.status_code != requests.codes.ok):
        sys.exit("Error accessing dashDB analytics REST API on {0}: {1}".format(DASHDBHOST, resp))

    spark_build = next ((x.get('spark_build_number') for x in resp.json().get('IDAX') if x.get('spark_build_number')), 
                        "000_unknown")
    print("Detected build {0}".format(spark_build))
    if (spark_build < MINUMUM_BUILD_NUMBER):
        newer_dashdb_required()

def newer_dashdb_required():
    sys.exit("The dashDB version running on {0} is not compatible with this notebook; "
             "the version must be at least {1}.\n"
             "Check your dashDB version with 'docker exec <container_name> version'.\n"
             "Upgrade your dashDB local docker images in order to use this notebook."
             .format(DASHDBHOST, MINUMUM_DASHDB_LEVEL))


if __name__ == "__main__":
    DASHDBHOST = os.environ.get('DASHDBHOST')
    DASHDBUSER = os.environ.get('DASHDBUSER')
    DASHDBPASS = os.environ.get('DASHDBPASS')
    if(not DASHDBHOST): DASHDBHOST='localhost'; print("Using default localhost for DASHDBHOST")
    if (not DASHDBUSER or not DASHDBPASS): sys.exit("DASHDBUSER and DASHDBPASS variables must be defined")
    
    warnings.filterwarnings('ignore', category=InsecureRequestWarning)
    
    try:
        print("Verifying Spark environment on {0}".format(DASHDBHOST))
        verify_sparkenv();
        print("Success.")
    except requests.exceptions.ConnectionError:
        sys.exit("Could not connect to dashDB server {0}".format(DASHDBHOST))
