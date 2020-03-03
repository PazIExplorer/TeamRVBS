#!/bin/bash
app=""
docker build -t ${app} .
docker run -d -p :80 \
 --name=${app} \
 -v $PWD:/app ${app}
