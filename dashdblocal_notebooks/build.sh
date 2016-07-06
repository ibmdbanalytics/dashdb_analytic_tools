#!/bin/bash

sbt -mem 256 update
sbt -mem 256 compile
sbt -mem 256 package

