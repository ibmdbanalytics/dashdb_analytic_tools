# (c) Copyright IBM Corporation 2016   
# LICENSE: Apache V2, https://opensource.org/licenses/Apache-2.0

import os
from shutil import make_archive
from tornado import gen
from .sparkapp_bundler import *

def bundle(handler, absolute_notebook_path):
    '''
    Converts the notebook into a Spark-Scala app and returns the source code
    
    :param handler: The tornado.web.RequestHandler that serviced the request
    :param absolute_notebook_path: The path of the notebook on disk
    '''

    notebook_filename = os.path.splitext(os.path.basename(absolute_notebook_path))[0]
    scalacode = export_to_scala(absolute_notebook_path)

    handler.set_header('Content-Type', 'text/plain; charset=us-ascii ')
    handler.write(scalacode)
    handler.finish()
