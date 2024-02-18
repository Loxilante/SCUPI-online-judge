#!/bin/bash

# 停止并删除之前可能存在的同名容器
docker stop javasandboxcontainer
docker rm javasandboxcontainer
current_directory=$(pwd)
parent_directory=$(dirname $(dirname "$current_directory"))
# 运行 Docker 容器
docker run -d -p 8002:80 -v "$parent_directory/files:/code/files" --name javasandboxcontainer java_sandbox
