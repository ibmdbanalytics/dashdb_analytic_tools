# (c) Copyright IBM Corporation 2016   
# LICENSE: Apache V2, https://opensource.org/licenses/Apache-2.0

import os, subprocess
from shutil import make_archive
from tornado import gen
from .sparkapp_bundler import *
from subprocess import STDOUT

HOME = os.getenv('HOME')
APPDIR = HOME + '/work/sparkapp'
SOURCEFILE = APPDIR + '/src/main/scala/notebook.scala'


@gen.coroutine
def bundle(handler, absolute_notebook_path):
    '''
    Transforms, converts, bundles, etc. the notebook. Then issues a Tornado web 
    response using the handler to redirect the browser, download a file, show
    an HTML page, etc. This function must finish the handler response before
    returning either explicitly or by raising an exception.
    
    :param handler: The tornado.web.RequestHandler that serviced the request
    :param absolute_notebook_path: The path of the notebook on disk
    '''

    #TEMPORARY hardcode path for development
    absolute_notebook_path = '/home/jovyan/work/notebooks/Spark_KMeansSample.ipynb'
    notebook_filename = os.path.splitext(os.path.basename(absolute_notebook_path))[0]
    
    export_to_scalafile(absolute_notebook_path, SOURCEFILE)
    print("noteboook exported to {0}".format(SOURCEFILE))

    print("building scala application in {0}...".format(APPDIR))
    jarfile = build_scala_project(APPDIR, notebook_filename)
    print("created jar file {0}".format(jarfile))
    
    upload = subprocess.run(["upload-sparkapp.py", jarfile], 
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    handler.set_header('Content-Type', 'text/plain; charset=us-ascii ')
    if (upload.returncode == 0):
        handler.write("Success!\n\n")
        handler.write(upload.stdout)
    else:
        handler.write("Failed!\n\n")
        handler.write(upload.stdout)

    handler.finish()
