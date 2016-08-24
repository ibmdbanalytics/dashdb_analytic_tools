# (c) Copyright IBM Corporation 2016
# LICENSE: BSD-3, https://opensource.org/licenses/BSD-3-Clause

import os, subprocess
from shutil import make_archive
from tornado import gen
from .sparkapp_bundler import *
from . import SPARKAPP_LOG


HOME = os.getenv('HOME')
APPDIR = HOME + '/projects/sparkapp'
SOURCEFILE = APPDIR + '/src/main/scala/notebook.scala'

DASHDBHOST = os.environ.get('DASHDBHOST')
DASHDBUSER = os.environ.get('DASHDBUSER')


@gen.coroutine
def bundle(handler, absolute_notebook_path):
    '''
    Converts the notebook into a Spark-Scala app, compiles it and uploads the
    application JAR file to the dashDB target server

    :param handler: The tornado.web.RequestHandler that serviced the request
    :param absolute_notebook_path: The path of the notebook on disk
    '''

    #TEMPORARY hardcode path for development
    #absolute_notebook_path = '/home/jovyan/work/Spark_KMeansSample.ipynb'
    notebook_filename = os.path.splitext(os.path.basename(absolute_notebook_path))[0]

    handler.set_header('Content-Type', 'text/plain; charset=us-ascii ')
    handler.write("Building scala application...\n")
    handler.flush()
    export_to_scalafile(absolute_notebook_path, SOURCEFILE)
    jarfile = build_scala_project(handler, APPDIR, SOURCEFILE, notebook_filename)
    if not jarfile: return

    upload = subprocess.run(["upload-sparkapp.py", jarfile],
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if (upload.returncode != 0):
        handler.write("Failed!\n\n")
        handler.write(upload.stdout)
        handler.finish()
        return

    resource = os.path.basename(jarfile)
    handler.write("Successfully uploaded {0} to {1}!\n\n".format(resource, DASHDBHOST))
    SPARKAPP_LOG.info("Upload output: %s", upload.stdout)
    handler.write("\n\nTo start your spark application, you can set DASHDBPASS and use the following command:\n\n"
                  "curl -k -v -u {0}:$DASHDBPASS -XPOST https://{1}:8443/dashdb-api/analytics/public/apps/submit \\\n"
                  "--header 'Content-Type:application/json;charset=UTF-8'  \\\n"
                  "--data '{{ \"appResource\" : \"{2}\", \"mainClass\" : \"SampleApp\" }}'\n"
                  .format(DASHDBUSER, DASHDBHOST, resource))
    handler.finish()

