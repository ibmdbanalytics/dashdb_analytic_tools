#!/usr/bin/env python3
# (c) Copyright IBM Corporation 2016
# LICENSE: BSD-3, https://opensource.org/licenses/BSD-3-Clause

# Startup file for Spark IPython kernels
# This file is executed after launching an IPython kernel

from pyspark.sql import SparkSession
spark = SparkSession.builder.getOrCreate()
sc = spark.sparkContext

