#!/bin/bash
sbt -mem 256 -Dsbt.log.noformat=true clean assembly

