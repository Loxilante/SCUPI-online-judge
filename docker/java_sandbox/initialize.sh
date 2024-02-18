#!/bin/bash
docker build -t java_sandbox .
current_directory=$(pwd)
parent_directory=$(dirname $(dirname "$current_directory"))
# 运行 Docker 容器
docker run -d -p 8002:80 -v "$parent_directory/files:/code/files" --name javasandboxcontainer java_sandbox
#遇到^M问题请运行 sed -i 's/\r$//' initialize.sh