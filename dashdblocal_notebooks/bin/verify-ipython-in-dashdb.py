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

def run_installer():
    auth = HTTPBasicAuth(DASHDBUSER, DASHDBPASS)
    request_data = { 'appResource' : 'ipython-installer.py' }
    resp = session.post("https://{0}:8443/dashdb-api/analytics/public/apps/submit".format(DASHDBHOST),
        json=request_data, auth=auth, verify=False)

    if (resp.status_code == requests.codes.unauthorized):
        sys.exit("Could not authenticate to {0} as user {1}. Verify DASHDBUSER and DASHDBPASS information"
                .format(DASHDBHOST, DASHDBUSER))
    # we're exepcting an error statuscode here, because we use this to return information
    # so there is no success statuscode check
    try:
        resp_data = resp.json()
        message = resp_data['exitInfo']['message']
        if (not message.startswith("Success:")):
            sys.exit("IPython install failed: {0}".format(message))
        print(message)
        return message
    except:
        # json decoding error or unexpected json
        sys.exit("Failed to submit IPython install job with status {0}: {1}"
                .format(resp.status_code, resp.text))

if __name__ == "__main__":
    DASHDBHOST = os.environ.get('DASHDBHOST')
    DASHDBUSER = os.environ.get('DASHDBUSER')
    DASHDBPASS = os.environ.get('DASHDBPASS')
    if(not DASHDBHOST): DASHDBHOST='localhost'; print("Using default localhost for DASHDBHOST")
    if (not DASHDBUSER or not DASHDBPASS): sys.exit("DASHDBUSER and DASHDBPASS variables must be defined")
    
    warnings.filterwarnings('ignore', category=InsecureRequestWarning)
    
    try:
        print("Verifying IPython installation on {0}.".format(DASHDBHOST))
        session = requests.Session()
        message = run_installer();
        if ("IPython installed" in message):
            # had to be installed first; try again if it is available now
            message = run_installer();
            if (not "IPython available" in message):
                sys.exit("IPython was installed but could not be used")
        elif (not "IPython available" in message):
            sys.exit("Error checking for IPython kernel")
        
        print("Can use IPython kernel.")
    except requests.exceptions.ConnectionError:
        sys.exit("Could not connect to dashDB server {0}".format(DASHDBHOST))
