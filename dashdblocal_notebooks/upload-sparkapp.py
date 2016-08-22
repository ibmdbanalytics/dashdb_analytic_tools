#!/usr/bin/env python3
# (c) Copyright IBM Corporation 2016
# LICENSE: BSD-3, https://opensource.org/licenses/BSD-3-Clause

# Upload Toree kernel to dashDB local via REST API

import sys, os
import json, requests
from requests.auth import HTTPBasicAuth

def usage():
	sys.exit('''
Usage: {0} <filename>
  Upload given Spark application file to dashDB server $DASHDBHOST,
  authenticating with $DASHDBUSR and $DASHDBPW.
'''.format(sys.argv[0]))

def upload(upload_file):
	auth = HTTPBasicAuth(DASHDBUSR, DASHDBPW)
	upload = {'file1': open(upload_file, 'rb') }
	resp = requests.post("https://{0}:8443/dashdb-api/home/spark/apps".format(DASHDBHOST),
		files = upload, auth=auth, verify=False)
	if (resp.status_code == requests.codes.unauthorized):
		sys.exit("Could not authenticate to {0} as user {1}. Verify DASHDBUSR and DASDBPW information"
				.format(DASHDBHOST, DASHDBUSR))
	if (resp.status_code != requests.codes.ok):
		sys.exit("Failed to upload {0}: {1}".format(upload_file, resp))
	if (resp.json().get('resultCode') != 'SUCCESS'):
		sys.exit("Failed to upload {0}: {1}".format(upload_file, resp.txt))
	return resp.text



if (len(sys.argv) != 2): usage()

upload_file = sys.argv[1]

DASHDBHOST = os.environ.get('DASHDBHOST')
DASHDBUSR = os.environ.get('DASHDBUSR')
DASHDBPW = os.environ.get('DASHDBPW')
if(not DASHDBHOST): DASHDBHOST='localhost'; print("Using default localhost for DASHDBHOST")
if (not DASHDBUSR or not DASHDBPW): sys.exit("DASHDBUSR and DASHDBPW variables must be defined")

try:
	print("Uploading {0} to {1} apps directory on {2}".format(upload_file, DASHDBUSR, DASHDBHOST))
	resp = upload(upload_file)
	print("Upload complete: " + resp)
except requests.exceptions.ConnectionError:
	sys.exit("Could not connect to dashDB server {0}".format(DASHDBHOST))
