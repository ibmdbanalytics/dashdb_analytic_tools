# (c) Copyright IBM Corporation 2016   
# LICENSE: Apache V2, https://opensource.org/licenses/Apache-2.0

def _jupyter_bundler_paths():
    '''API for notebook bundler installation on notebook 4.2'''
    return [{
            'name': 'sparkapp_bundler',
            'label': 'export as Spark SBT project (.zip)',
            'module_name': 'jupyter_cms_sparkapp.sparkapp_bundler',
            'group': 'download'
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
