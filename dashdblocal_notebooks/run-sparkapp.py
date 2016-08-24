#!/usr/bin/env python3
# (c) Copyright IBM Corporation 2016
# LICENSE: BSD-3, https://opensource.org/licenses/BSD-3-Clause

import warnings
import sys, os, time
import json, requests
from requests.auth import HTTPBasicAuth

def usage():
	sys.exit('''
Usage: {0} <submit-spec>
  Submit a Spark application eith the given specification on dashDB server $DASHDBHOST,
  authenticating with $DASHDBUSER and $DASHDBPASS.
  Application must have been uploaded before.
'''.format(sys.argv[0]))

def submit(submit_spec):
	headers = { "Content-Type": "application/json;charset=UTF-8" }
	resp = session.post("https://{0}:8443/dashdb-api/analytics/public/apps/submit".format(DASHDBHOST),
		data=submit_spec, headers=headers, auth=auth, verify=False)

	if (resp.status_code == requests.codes.unauthorized):
		sys.exit("Could not authenticate to {0} as user {1}. Verify DASHDBUSER and DASDBPW information"
				.format(DASHDBHOST, DASHDBUSER))
	if (resp.status_code != requests.codes.ok):
		sys.exit ("Failed to submit Spark application: " + resp.text)
	resp_data = resp.json()
	if (resp_data.get('status') != 'submitted'):
		sys.exit ("Failed to submit Spark application: " + resp.text)

	jobid = resp_data['jobid']
	return (jobid, resp.text)

def wait_for_app(jobid):
	while (True):
		with warnings.catch_warnings():
			warnings.simplefilter("ignore")
			resp = session.get("https://{0}:8443/dashdb-api/analytics/public/monitoring/app_status".format(DASHDBHOST),
				params={'submissionid': jobid}, auth=auth, verify=False)
		if (resp.status_code != requests.codes.ok):
			sys.exit ("Failed to monitor Spark application: " + str(resp))
		if (resp.json().get('status') != 'running'):
			break
		time.sleep(1)

def print_app_log(jobid, filename):
	url = "https://{0}:8443/dashdb-api/home/spark/log/submit_{1}/{2}".format(DASHDBHOST, jobid, filename)
	print("Retrieving logs from {0}".format(url))
	with warnings.catch_warnings():
		warnings.simplefilter("ignore")
		resp = session.get(url, auth=auth, verify=False)
	if (resp.status_code == 404):
		return False
	if (resp.status_code == 400 and ('path does not exist' in resp.json().get('message'))):
		# dashdb_api reports non-existing files as 'bad request' like all other errors
		return False
	if (resp.status_code != requests.codes.ok):
		sys.exit ("Failed to retrieve Spark logs: " +resp.text)
	for chunk in resp.iter_content(1024):
		sys.stdout.buffer.write(chunk)
	return True



if (len(sys.argv) != 2): usage()

submit_spec = sys.argv[1]

DASHDBHOST = os.environ.get('DASHDBHOST')
DASHDBUSER = os.environ.get('DASHDBUSER')
DASHDBPASS = os.environ.get('DASHDBPASS')
if(not DASHDBHOST): DASHDBHOST='localhost'; print("Using default localhost for DASHDBHOST")
if (not DASHDBUSER or not DASHDBPASS): sys.exit("DASHDBUSER and DASHDBPASS variables must be defined")

session = requests.Session()
auth = HTTPBasicAuth(DASHDBUSER, DASHDBPASS)

try:
	print("Submitting application for user {0} on {1}".format(DASHDBUSER, DASHDBHOST))
	(jobid, resp) = submit(submit_spec)
	print("Submit successful: " + resp)

	print("Waiting for application to execute...")
	wait_for_app(jobid)
	print("Application has finished")

	print("\nOutput of application\n")
	if (not print_app_log(jobid, 'submit.out')):
		print("No output for application")
	print("\nError output of application\n")
	if (not print_app_log(jobid, 'submit.err')):
		print("No error output for application")

except requests.exceptions.ConnectionError:
	sys.exit("Could not connect to dashDB server {0}".format(DASHDBHOST))
