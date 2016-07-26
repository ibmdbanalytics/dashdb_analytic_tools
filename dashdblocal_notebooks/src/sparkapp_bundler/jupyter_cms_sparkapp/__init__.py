# (c) Copyright IBM Corporation 2016
# LICENSE: Apache V2, https://opensource.org/licenses/Apache-2.0

import logging

# logger for bundle
SPARKAPP_LOG = logging.getLogger(__package__)

def _jupyter_bundler_paths():
    '''API for notebook bundler installation on notebook 4.2'''
    return [{
            'name': 'scalafile_download',
            'label': 'Scala class (in browser)',
            'module_name': 'jupyter_cms_sparkapp.scalafile_download',
            'group': 'download'
    },
    {
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
    global SPARKAPP_LOG
    SPARKAPP_LOG = nb_app.log
    SPARKAPP_LOG.info('Loaded jupyter_cms_sparkapp')
