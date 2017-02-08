# (c) Copyright IBM Corporation 2016
# LICENSE: BSD-3, https://opensource.org/licenses/BSD-3-Clause

# simple script to launch the IPython kernel
# this is equivalent to  "python -m ipykernel", but can be submitted
# via the dashDB Spark REST interface

def _notebook_init():
    from ipykernel import kernelapp

    print("Starting IPython kernel")
    kernelapp.launch_new_instance()

_notebook_init()

