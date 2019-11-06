GIT_PROJECT=jmacenka/flask-bee-project
PROJECT_PORT=5000

if [ -e ./.git ]; then
    echo "Now: Repository already cloned local, stopping all containers"
    docker rm -f $(docker ps -aq)
else
    echo "Now: pulling project form github"
    git clone https://github.com/$GIT_PROJECT.git app && cd app
fi
echo "Now: building the docker image and starting a container"
docker rm -f $(docker ps -aq)
docker build -t app:latest .
docker run -p 80:5000 -d --restart always --name app app
echo "All Done, Container is up and running. Visite http://$(hostname -I | cut -d' ' -f1)"