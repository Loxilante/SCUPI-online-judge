#!/bin/bash
docker build -t cpp_sandbox .
current_directory=$(pwd)
parent_directory=$(dirname $(dirname "$current_directory"))
# 运行 Docker 容器
docker run -d -p 8001:80 -v "$parent_directory/files:/code/cpp_files" --name cppsandboxcontainer cpp_sandbox