# (c) Copyright IBM Corporation 2016
# LICENSE: BSD-3, https://opensource.org/licenses/BSD-3-Clause

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
    (scalacode, resources) = export_to_scala(absolute_notebook_path)

    handler.set_header('Content-Type', 'text/plain; charset=us-ascii ')
    for dep in resources['mvn_deps'] or []:
        handler.write("// requires {0}\n".format(dep))
    handler.write(scalacode)
    handler.finish()
