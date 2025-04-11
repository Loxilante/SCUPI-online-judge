
docker build -t ai_sandbox .

docker run -d -p 8302:80 --name aisandboxcontainer ai_sandbox

pause