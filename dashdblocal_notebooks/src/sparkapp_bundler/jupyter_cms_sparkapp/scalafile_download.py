# (c) Copyright IBM Corporation 2016   
# LICENSE: Apache V2, https://opensource.org/licenses/Apache-2.0

import os
from shutil import make_archive
from tornado import gen
from .sparkapp_bundler import *

def bundle(handler, absolute_notebook_path):
    '''
    Transforms, converts, bundles, etc. the notebook. Then issues a Tornado web 
    response using the handler to redirect the browser, download a file, show
    an HTML page, etc. This function must finish the handler response before
    returning either explicitly or by raising an exception.
    
    :param handler: The tornado.web.RequestHandler that serviced the request
    :param absolute_notebook_path: The path of the notebook on disk
    '''

    notebook_filename = os.path.splitext(os.path.basename(absolute_notebook_path))[0]
    scalacode = export_to_scala(absolute_notebook_path)

    handler.set_header('Content-Type', 'text/plain; charset=us-ascii ')
    for (n, line) in enumerate(scalacode.splitlines(), 1):
        handler.write("{0:>5}:  {1}\n".format(n, line))
    handler.finish()
