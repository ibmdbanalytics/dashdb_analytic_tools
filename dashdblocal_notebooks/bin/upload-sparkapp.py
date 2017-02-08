#!/usr/bin/env python3
# (c) Copyright IBM Corporation 2016
# LICENSE: BSD-3, https://opensource.org/licenses/BSD-3-Clause

# Upload Toree kernel to dashDB local via REST API

import warnings
import sys, os
import json, requests
from requests.auth import HTTPBasicAuth
from requests.packages.urllib3.exceptions import InsecureRequestWarning

def usage():
    sys.exit('''
Usage: {0} <filename>
  Upload given Spark application file to dashDB server $DASHDBHOST,
  authenticating with $DASHDBUSER and $DASHDBPASS.
'''.format(sys.argv[0]))

def upload(upload_file):
    auth = HTTPBasicAuth(DASHDBUSER, DASHDBPASS)
    upload = {'file1': open(upload_file, 'rb') }
    resp = requests.post("https://{0}:8443/dashdb-api/home/spark/apps".format(DASHDBHOST),
        files = upload, auth=auth, verify=False)
    if (resp.status_code == requests.codes.unauthorized):
        sys.exit("Could not authenticate to {0} as user {1}. Verify DASHDBUSER and DASHDBPASS information"
                .format(DASHDBHOST, DASHDBUSER))
    if (resp.status_code != requests.codes.ok):
        sys.exit("Failed to upload {0}: {1}".format(upload_file, resp))
    if (resp.json().get('resultCode') != 'SUCCESS'):
        sys.exit("Failed to upload {0}: {1}".format(upload_file, resp.txt))
    return resp.text


if __name__ == "__main__":
    if (len(sys.argv) != 2): usage()
    
    upload_file = sys.argv[1]
    
    DASHDBHOST = os.environ.get('DASHDBHOST') or 'localhost'
    DASHDBUSER = os.environ.get('DASHDBUSER')
    DASHDBPASS = os.environ.get('DASHDBPASS')
    if (not DASHDBUSER or not DASHDBPASS): sys.exit("DASHDBUSER and DASHDBPASS variables must be defined")
    
    warnings.filterwarnings('ignore', category=InsecureRequestWarning)
    
    try:
        print("Uploading {0} to {1} apps directory on {2}".format(upload_file, DASHDBUSER, DASHDBHOST))
        resp = upload(upload_file)
        print("Upload complete: " + resp)
    except requests.exceptions.ConnectionError:
        sys.exit("Could not connect to dashDB server {0}".format(DASHDBHOST))
