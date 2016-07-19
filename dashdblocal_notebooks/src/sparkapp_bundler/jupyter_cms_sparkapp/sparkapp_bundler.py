import os, io, glob, json, zipfile
from subprocess import call
from shutil import make_archive
from nbconvert import TemplateExporter
from jinja2 import FileSystemLoader
from tornado import gen


HOME = os.getenv('HOME')
INSTALLDIR = os.path.dirname(os.path.realpath(__file__))
    
APPDIR = HOME + '/work/sparkapp'
SOURCEFILE = APPDIR + '/src/main/scala/notebook.scala'


def export_to_scalafile(absolute_notebook_path, scala_source):
    '''convert the notebook source to scala and save it into the given filename'''
    
    exporter = TemplateExporter(extra_loaders=[FileSystemLoader(INSTALLDIR)])
    exporter.template_file = 'scala_sparkapp'
    (body, resources) = exporter.from_file(absolute_notebook_path)
    with open(scala_source, 'wt') as sourcefile:
        sourcefile.write(body)

        
def build_scala_project(project_dir, appname):
    '''build the given scala project, replacing the <appname> tag in build.sbt.template
    with the given application name.
    Return the name of the generated JAR'''
            
    with open(project_dir+"/../build.sbt.template", "rt") as buildfile_in:
        with open(project_dir+"/build.sbt", "wt") as buildfile_out:
            for line in buildfile_in:
                buildfile_out.write(line.replace('<appname>', appname))
    call(["./build.sh"], cwd=APPDIR)
    
    jars = glob.glob(project_dir + "/target/**/*.jar")
    assert len(jars) == 1, "Expected exactly one output JAR bout found {0}".format(','.join(jars))
    return jars[0]


def add_launcher_scripts(project_dir, jarfile, appname):
    scriptfile = "{0}/upload_{1}.sh".format(project_dir, appname)
    with open(scriptfile, "wt") as script:
        script.write("#!/bin/sh\n")
        script.write("./upload-sparkapp.py {0}\n".format(jarfile))
    os.chmod(scriptfile, 0o755)

    resource = os.path.basename(jarfile)
    scriptfile = "{0}/run_{1}.sh".format(project_dir, appname)
    submit_spec = { "appResource" : resource, "mainClass" : "SampleApp" }
    with open(scriptfile, "wt") as script:
        script.write("#!/bin/sh\n")
        script.write("./run-sparkapp.py '{0}'\n".format(json.dumps(submit_spec)))
    os.chmod(scriptfile, 0o755)
    

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
    #absolute_notebook_path = '/home/jovyan/work/notebooks/Spark_KMeansSample.ipynb'
    notebook_filename = os.path.splitext(os.path.basename(absolute_notebook_path))[0]
    
    export_to_scalafile(absolute_notebook_path, SOURCEFILE)
    print("noteboook exported to {0}".format(SOURCEFILE))

    print("building scala application in {0}...".format(APPDIR))
    jarfile = build_scala_project(APPDIR, notebook_filename)
    print("created jar file {0}".format(jarfile))
    
    relpath = os.path.relpath(jarfile, APPDIR)
    add_launcher_scripts(APPDIR, relpath, notebook_filename)
    print("created launcher scripts")

    print("zipping project")
    archive_path = make_archive("/tmp/"+notebook_filename, 'zip', APPDIR)
    archive_base = os.path.basename(archive_path)
    
    handler.set_header('Content-Disposition', 'attachment; filename="{0}"'.format(archive_base))
    handler.set_header('Content-Type', 'application/zip')
    
    with open(archive_path, "rb") as data:
        handler.write(data.read())
    print("export complete")
    handler.finish()
