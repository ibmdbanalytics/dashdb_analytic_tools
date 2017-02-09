#!/usr/bin/env python3
# (c) Copyright IBM Corporation 2016
# LICENSE: BSD-3, https://opensource.org/licenses/BSD-3-Clause

import warnings
import _thread, sys, os, socket, time
import signal, atexit
import json, requests
from requests.auth import HTTPBasicAuth
from requests.packages.urllib3.exceptions import InsecureRequestWarning


# upload connection JSON file to dashDB local
def upload_conn_info(conn_file_name, conn_file_content):
    conn_upload = conn_file_content
    if (IS_REMOTE_KERNEL):
        # reconfigure remote kernel to listen on all interfaces
        conn_upload['ip'] = '0.0.0.0'
    upload = { conn_file_name: json.dumps(conn_file_content) }
    resp = session.post("https://{0}:8443/dashdb-api/home/tmp".format(DASHDBHOST),
                    files = upload, auth=auth, verify=False)
    if (resp.status_code != requests.codes.ok or
            resp.json().get('resultCode') != 'SUCCESS'):
        sys.exit ("Failed to upload communication file " + conn_file_in)
    print("Upload complete: " + resp.text)


# start kernel app on dashDB local
def start_kernel(request_data):
    global submissionid
    resp = session.post("https://{0}:8443/dashdb-api/analytics/public/apps/submit".format(DASHDBHOST),
        json=request_data, auth=auth, verify=False)

    if (resp.status_code != requests.codes.ok):
        sys.exit ("Failed to submit Spark kernel job: code {0}, {1}".format(resp.status_code, resp.text))
    resp_data = resp.json()
    if (resp_data.get('status') != 'submitted'):
        sys.exit ("Failed to submit Spark kernel job: {0}".format(resp.text))

    submissionid = resp_data['submissionId']
    print("Started Spark kernel with submission id " + submissionid)
    print(resp.text)


# poll kernel app status and wait for termination
def monitor_kernel():
    global submissionid
    i = 0
    while (True):
        resp = session.get("https://{0}:8443/dashdb-api/analytics/public/monitoring/app_status".format(DASHDBHOST),
            params={'submissionid': submissionid}, auth=auth, verify=False)
        if (resp.json().get('status') != 'running'):
            print(resp.text)
            break
#        if (i == 0):
#            print(resp.text)  #  print message every minute that we're still alive
#            i = 60
#        i -= 1
        time.sleep(1) # sleep a second
    submissionid = None


# explicitly request to shut down the kernel app
def stop_kernel():
    global submissionid
    print("Shutting down")
    if (submissionid):
        print("Trying to stop kernel")
        resp = session.post("https://{0}:8443/dashdb-api/analytics/public/apps/cancel".format(DASHDBHOST),
            params={'submissionid': submissionid}, auth=auth, verify=False)
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
        _thread.start_new_thread(forward_socket, (port, DASHDBHOST))

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


if __name__ == "__main__":
    if(len(sys.argv) < 3): 
        sys.exit("Syntax: run-kernel-in-dashdb.py <kernel_type> <connection_file> <extra_kernel_args...>")

    # kernel type is first argument
    kernel_type = sys.argv[1]
    # comm file is second argument
    conn_file_in = sys.argv[2]
    # extra arguments are passed on to the kernel
    extra_kernel_args = sys.argv[3:]
    
    DASHDBHOST = os.environ.get('DASHDBHOST') or 'localhost'
    DASHDBUSER = os.environ.get('DASHDBUSER')
    DASHDBPASS = os.environ.get('DASHDBPASS')
    if (not DASHDBUSER or not DASHDBPASS): sys.exit("DASHDBUSER and DASHDBPASS variables must be defined")
    IS_REMOTE_KERNEL = (DASHDBHOST != "localhost" and DASHDBHOST != "127.0.0.1")
    
    submissionid = None
    
    conn_file_name = os.path.basename(conn_file_in)
    conn_file_out = "/mnt/blumeta0/home/{0}/tmp/{1}".format(DASHDBUSER, conn_file_name)
    
    session = requests.Session()
    auth = HTTPBasicAuth(DASHDBUSER, DASHDBPASS)
    
    # handle kernel interrupting explicitly
    signal.signal(signal.SIGINT, interrupted)
    # if the wrapper script is terminated externally, then we want to shut down the toree kernel as well
    atexit.register(stop_kernel)
    
    warnings.filterwarnings('ignore', category=InsecureRequestWarning)
    
    print("Uploading {0} to {1} on {2}".format(conn_file_in, conn_file_out, DASHDBHOST))
    with open(conn_file_in, 'r') as f:
        conn_file_content = json.loads(f.read())
    upload_conn_info(conn_file_name, conn_file_content)

    if (kernel_type == 'toree'):
        request_data = {
            'appArgs' : [ '--profile', conn_file_out ] + extra_kernel_args,
            'appResource' : 'toree.jar',
            'mainClass' : 'org.apache.toree.Main'
            # Providing an app name here is no use, because Toree will override the app name at execution
        }
    elif (kernel_type == 'ipython'):
        request_data = {
            'appArgs' : [ '-f', conn_file_out ] + extra_kernel_args,
            'appResource' : 'ipython-launcher.py',
            'sparkProperties' : { 'sparkAppName' : 'IPython Notebook' }
        }
    else:
        sys.exit("Invalid kernel type" + kernel_type)

    print("Starting Spark kernel with " + str(request_data))
    start_kernel(request_data)
    
    if (IS_REMOTE_KERNEL):
        forward_ports(conn_file_content)
    
    # monitor job
    monitor_kernel()
    print("Spark kernel has terminated")

