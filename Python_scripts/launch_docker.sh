docker build -t docker_api_chirpstack .
docker run -p 8080:5000 -d docker_api_chirpstack
