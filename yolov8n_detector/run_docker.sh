#!/bin/bash
sudo docker run -it --rm --ipc=host --runtime=nvidia -v $(pwd)/py_script:/usr/src/ultralytics/py_scripts ultralytics/ultralytics:latest-jetson-jetpack4
