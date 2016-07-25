# (c) Copyright IBM Corporation 2016   
# LICENSE: Apache V2, https://opensource.org/licenses/Apache-2.0

from distutils.core import setup

setup(
    name='SparkApp Bundler',
    version='0.1dev',
    packages=['jupyter_cms_sparkapp'],
    package_data = {
        '': ['*.tpl'],
    },
)