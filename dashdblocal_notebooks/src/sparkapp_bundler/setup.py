# (c) Copyright IBM Corporation 2016
# LICENSE: BSD-3, https://opensource.org/licenses/BSD-3-Clause

from distutils.core import setup

setup(
    name='SparkApp Bundler',
    version='0.1dev',
    packages=['jupyter_cms_sparkapp'],
    package_data = {
        '': ['*.tpl'],
    },
)