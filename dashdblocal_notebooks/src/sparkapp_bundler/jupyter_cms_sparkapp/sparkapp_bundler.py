import os    
from nbconvert import TemplateExporter
from jinja2 import FileSystemLoader

HOME = os.getenv('HOME')
INSTALLDIR = os.path.dirname(os.path.realpath(__file__))
    
APPDIR = HOME + '/work/sparkapp'
SOURCEFILE = APPDIR + '/src/main/scala/notebook.scala'

def bundle(handler, absolute_notebook_path):
    '''
    Transforms, converts, bundles, etc. the notebook. Then issues a Tornado web 
    response using the handler to redirect the browser, download a file, show
    an HTML page, etc. This function must finish the handler response before
    returning either explicitly or by raising an exception.
    
    :param handler: The tornado.web.RequestHandler that serviced the request
    :param absolute_notebook_path: The path of the notebook on disk
    '''

    #TEMPORARY for development
    absolute_notebook_path = '/home/jovyan/work/notebooks/Spark_KMeansSample.ipynb'
    
    notebook_filename = os.path.basename(absolute_notebook_path)
    
    exporter = TemplateExporter(extra_loaders=[FileSystemLoader(INSTALLDIR)])
    exporter.template_file = 'scala_sparkapp'
    
    (body, resources) = exporter.from_file(absolute_notebook_path)

    with open(SOURCEFILE, 'w') as sourcefile:
        sourcefile.write(body)

    print("noteboook exported to {0}".format(SOURCEFILE))
        
    handler.finish("exported!")
