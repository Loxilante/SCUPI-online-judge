
docker stop aisandboxcontainer >nul 2>&1
docker rm aisandboxcontainer >nul 2>&1

docker run -d -p 8302:80 --name aisandboxcontainer -v "%cd%:/code" ai_sandbox python manage.py runserver 0.0.0.0:80

pause