#!/bin/bash
echo "Building docker image"
sudo docker build -t scriptfile -f ./Dockerfile-script ./
echo "Image built, Check with docker image command"