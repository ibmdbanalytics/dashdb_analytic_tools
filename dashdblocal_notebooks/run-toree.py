#!/usr/bin/env python3

import warnings
import _thread, sys, os, socket,time
import signal, atexit
import json, requests
from requests.auth import HTTPBasicAuth


if (len(sys.argv) < 2): sys.exit("Expecting connection file name as first argument")

# comm file is first argument
conn_file_in = sys.argv[1]
# extra arguments are passed on to toree kernel
extra_args = sys.argv[2:]

BLUHOST = os.environ['BLUHOST']
BLUUSER = os.environ['BLUUSER']
BLUPW = os.environ['BLUPW']
if (not BLUUSER or not BLUPW): sys.exit("BLUHOST, BLUUSER and BLUPW variables must be defined")
IS_REMOTE_KERNEL = (BLUHOST != "localhost" and BLUHOST != "127.0.0.1")

jobid = None


# upload connection JSON file to dashDB local
def upload_conn_info(conn_file_name, conn_file_content):
	conn_upload = conn_file_content
	if (IS_REMOTE_KERNEL):
		# reconfigure remote kernel to listen on all interfaces
		conn_upload['ip'] = '0.0.0.0'
	upload = { conn_file_name: json.dumps(conn_file_content) }
	resp = session.post("https://{0}:8443/dashdb-api/home/tmp".format(BLUHOST),
					files = upload, auth=auth, verify=False)
	if (resp.status_code != requests.codes.ok and
			resp.json()['resultCode'] != 'SUCCESS'): 
		sys.exit ("Failed to upload communication file " + conn_file_in)
	print("Upload complete: " + resp.text)


# start toree server on dashDB local
def start_kernel(toree_args):
	global jobid
	req_data = {
		'appArgs' : toree_args,
		'appResource' : 'toree.jar',
		'mainClass' : 'org.apache.toree.Main'
	}
	resp = session.post("https://{0}:8443/clues/public/jobs/submit".format(BLUHOST),
		json=req_data, auth=auth, verify=False)

	if (resp.status_code != requests.codes.ok): 
		sys.exit ("Failed to submit Spark kernel job: " + resp.text)
	resp_data = resp.json()
	if (resp_data['status'] != 'submitted'):
		sys.exit ("Failed to submit Spark kernel job: " + resp.text)

	jobid = resp_data['jobid']
	print("Started Spark kernel job with id" + jobid)
	print(resp.text)


# poll toree server status and wait for termination
def monitor_kernel():
	global jobid
	i = 0
	while (True):
		with warnings.catch_warnings():
			warnings.simplefilter("ignore")
			resp = session.get("https://{0}:8443/clues/public/monitoring/job_status".format(BLUHOST),
				params={'jobid': jobid}, auth=auth, verify=False)
		if (resp.json()['status'] != 'running'):
			print(resp.text)
			break
		if (i == 0):
			print(resp.text)  #  print message every 10 seconds that we're still alive
			i = 10
		i -= 1
		time.sleep(1) # sleep a second
	jobid = None


# explicitly request to shut down the toree server
def stop_kernel():
	global jobid
	print("Shutting down")
	if (jobid):
		print("Trying to stop kernel")
		resp = session.post("https://{0}:8443/clues/public/jobs/cancel".format(BLUHOST),
			params={'jobid': jobid}, auth=auth, verify=False)
		print(resp.text)
		
		
# interrupt handler for SIGINT
# currently, there is no mechanism to forward the interruption to the remote
# toree kernel
def interrupted(signum, frame):
	print("Kernel interrupting not yet supported")


# Is possible to connect to a remote kernel with the Jupyter console, but the
# Jupyter notebook application fails when you specify a remote kernel IP.
# So we need to simulate a local kernel by forwarding the ZeroMQ ports for
# kernel communication
def forward_ports(connection_info):
	ports = [ connection_info['iopub_port'], connection_info['shell_port'],
			connection_info['control_port'], connection_info['stdin_port'],
			connection_info['hb_port'] ]
	print("Forwarding ports " + str(ports))
	for port in ports:
		_thread.start_new_thread(forward_socket, (port, BLUHOST))
		
def forward_socket(port, target):
	try:
		print("waiting for local connections on {0}".format(port))
		dock_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		# avoid "Address already in use" errors when the kernel is interrupted and restarted
		dock_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		dock_socket.bind(('127.0.0.1', port))
		dock_socket.listen(5)
		while True:
			client_socket = dock_socket.accept()[0]
			print("connecting to {1} on {0}".format(port, target))
			server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			server_socket.connect((target, port))
			print("forwarding {0}".format(port))
			_thread.start_new_thread(forward_connection, (client_socket, server_socket, 
				"outgoing forward for {0}".format(port)))
			_thread.start_new_thread(forward_connection, (server_socket, client_socket,
				"incoming forward for {0}".format(port)))
	finally:
		print("forwarding for {0} ended".format(port))
 
def forward_connection(source, destination, id):
	try:
		while (True):
			data = source.recv(1024)
			if (not data): break
			destination.sendall(data)
	finally:
		print("finished {0}".format(id))
		source.close()
		destination.close()


conn_file_name = os.path.basename(conn_file_in)
conn_file_out = "/mnt/blumeta0/home/{0}/tmp/{1}".format(BLUUSER, conn_file_name)

session = requests.Session()
auth = HTTPBasicAuth(BLUUSER, BLUPW)

# handle kernel interrupting explicitly
signal.signal(signal.SIGINT, interrupted)
# if the wrapper script is terminated externally, then we want to shut down the toree kernel as well
atexit.register(stop_kernel)


print("Uploading {0} to {1} on {2}".format(conn_file_in, conn_file_out, BLUHOST))
with open(conn_file_in, 'r') as f:
	conn_file_content = json.loads(f.read())
upload_conn_info(conn_file_name, conn_file_content)

toree_args = [ '--profile', conn_file_out ] + extra_args
print("Starting Spark kernel with arguments " + str(toree_args))
start_kernel(toree_args)

if (IS_REMOTE_KERNEL):
	forward_ports(conn_file_content)

# monitor job
monitor_kernel()
print("Spark kernel has terminated")

