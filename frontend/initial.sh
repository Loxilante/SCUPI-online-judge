
docker stop frontendcontainer
docker rm frontendcontainer

docker build -t vuefrontend . --progress=plain --no-cache 
docker run -d -p 3000:80 --name frontendcontainer vuefrontend