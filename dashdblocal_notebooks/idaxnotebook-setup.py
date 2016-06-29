#!/usr/bin/env python3

# Upload Toree kernel to dashDB local via REST API

import sys, os
import shutil, glob
import json, requests
from requests.auth import HTTPBasicAuth

if (len(sys.argv) < 2): sys.exit("Expecting upload file name as first argument")

upload_file = sys.argv[1]

bluhost = os.environ['BLUHOST']
bluuser = os.environ['BLUUSER']
blupw = os.environ['BLUPW']
if (not bluuser or not blupw or not bluhost): sys.exit("BLUHOST, BLUUSER and BLUPW variables must be defined")

auth = HTTPBasicAuth(bluuser, blupw)

print("Uploading {0} to {1} apps directory on {2}".format(upload_file, bluuser, bluhost))

upload = {'file1': ('toree.jar', open(upload_file, 'rb')) }

try:
	resp = requests.post("https://{0}:8443/dashdb-api/home/spark/apps".format(bluhost),
		files = upload, auth=auth, verify=False)
except requests.exceptions.ConnectionError:
	sys.exit("Could not connect to dashDB server {0}".format(bluhost))

if (resp.status_code != requests.codes.ok and
		resp.json()['resultCode'] != 'SUCCESS'):
	sys.exit ("Failed to upload toree assembly")

print("Upload complete: " + resp.text)
