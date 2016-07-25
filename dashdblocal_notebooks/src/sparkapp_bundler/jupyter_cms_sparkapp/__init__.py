# (c) Copyright IBM Corporation 2016   
# LICENSE: Apache V2, https://opensource.org/licenses/Apache-2.0

def _jupyter_bundler_paths():
    '''API for notebook bundler installation on notebook 4.2'''
    return [{
            'name': 'spark_project_download',
            'label': 'Spark SBT project (.zip)',
            'module_name': 'jupyter_cms_sparkapp.sbt_project_download',
            'group': 'download'
    },
    {
            'name': 'sparkapp_dashdb_upload',
            'label': 'Deploy to dashDB Spark',
            'module_name': 'jupyter_cms_sparkapp.sparkapp_upload',
            'group': 'deploy'
    }]
        
def _jupyter_server_extension_paths():
    '''API for server extension installation on notebook 4.2'''
    return [{
        "module": "jupyter_cms_sparkapp"
    }]

def load_jupyter_server_extension(nb_app):
    '''
    Loads all extensions within this package.
    '''
    nb_app.log.info('Loaded jupyter_cms_sparkapp')
