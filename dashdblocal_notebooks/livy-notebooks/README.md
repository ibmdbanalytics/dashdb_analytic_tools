# Configure Livy 

Here we explain how to configure a livy connection so you are able to :
* work on a Jupyter notebook which you open locally 
* let it run on a Spark cluster with IBM Db2 Warehouse.

Livy is an open-source REST service for Apache Spark. You can use it with sparkmagic in a Jupyter notebook to execute Spark jobs easily. Read more on the official Apache Livy page : https://livy.apache.org/.

Sparkmagic (https://github.com/jupyter-incubator/sparkmagic) enables to work with remote Spark clusters through Livy in Jupyter notebooks. It will run a Spark job through Livy when you write Spark code on your local Jupyter client. This means you can run a Spark job from your own Jupyter notebook, which is running on your local host.

Let's open a terminal window and execute the following commands:
> pip install sparkmagic

> jupyter nbextension enable --py --sys-prefix widgetsnbextension

Then retrieve installation directory of sparkmagic with
> pip show sparkmagic

Move to this directory to install the notebook kernels for Scala, R and Python with:
> cd your_install_dir

> jupyter-kernelspec install sparkmagic/kernels/sparkkernel

> jupyter-kernelspec install sparkmagic/kernels/sparkrkernel

> jupyter-kernelspec install sparkmagic/kernels/pysparkkernel

Create the config.json file for the sparkmagic configuration file in your home directory with
> cd 

> mkdir .sparkmagic

> cd .sparkmagic

> wget https://raw.githubusercontent.com/jupyter-incubator/sparkmagic/master/sparkmagic/example_config.json

Create the config.json file as a copy of example_config.json
> cp example_config.json config.json

Edit the config.json file and specify username, password and url of the Db2 Warehouse system in the „credentials”-sections of the 3 kernels. "8998" is the default Livy server port. As value for the “auth” attribute enter “Basic_Access”
Example: 
```
{
 "kernel_python_credentials" : {
    "username": "your_name",
    "password": "your_password",
    "url": "http://yoururl:8998",
    "auth": "Basic_Access"
 },
 ...
```
Also remove the following section (lines 52 to 55), because the configuraion of Spark is adapted automatically to the available resources in the Db2 Warehouse container:
```
"session_configs": {
    "driverMemory": "1000M",
    "executorCores": 2
  },
```
In case you want to change these defaults you can use the "%%configuration" magic.
```
%%configure -f 
{"executorCores": 16}
```

You can now start the Jupyter notebook with
> jupyter notebook

In the notebook you can start one of the following kernels: PySpark, Spark or R. 
You're ready!

Please note that paths used in the present notebooks assume that the notebook is run by the **bluadmin** user inside of the Db2 Warehouse container. Please make sure you adapt the user name if you are not using bluadmin.