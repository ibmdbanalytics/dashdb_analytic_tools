from distutils.core import setup

setup(
    name='SparkApp Bundler',
    version='0.1dev',
    packages=['jupyter_cms_sparkapp'],
    package_data = {
        '': ['*.tpl'],
    },
)