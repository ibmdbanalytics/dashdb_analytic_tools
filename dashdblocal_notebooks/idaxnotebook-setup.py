#!/usr/bin/env python3

# Upload Toree kernel to dashDB local via REST API

import sys, os
import shutil, glob
import json, requests
from requests.auth import HTTPBasicAuth

if (len(sys.argv) < 2): sys.exit("Expecting upload file name as first argument")

upload_file = sys.argv[1]

DASHDBHOST = os.environ.get('DASHDBHOST')
DASHDBUSR = os.environ.get('DASHDBUSR')
DASHDBPW = os.environ.get('DASHDBPW')
if(not DASHDBHOST): DASHDBHOST='localhost'; print("Using default localhost for DASHDBHOST")
if (not DASHDBUSR or not DASHDBPW): sys.exit("DASHDBUSR and DASHDBPW variables must be defined")

auth = HTTPBasicAuth(DASHDBUSR, DASHDBPW)

print("Uploading {0} to {1} apps directory on {2}".format(upload_file, DASHDBUSR, DASHDBHOST))

upload = {'file1': ('toree.jar', open(upload_file, 'rb')) }

try:
	resp = requests.post("https://{0}:8443/dashdb-api/home/spark/apps".format(DASHDBHOST),
		files = upload, auth=auth, verify=False)
except requests.exceptions.ConnectionError:
	sys.exit("Could not connect to dashDB server {0}".format(DASHDBHOST))

if (resp.status_code != requests.codes.ok and
		resp.json().get('resultCode') != 'SUCCESS'):
	sys.exit ("Failed to upload toree assembly")

print("Upload complete: " + resp.text)
