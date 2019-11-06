docker rm -f $(docker ps -aq)
docker build -t app:latest .
docker run -p 80:5000 -d --restart always --name app app
echo "All Done, Container is up and running. Visite http://$(hostname -I | cut -d' ' -f1)"