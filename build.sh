docker compose -f /home/ubuntu/apps/docker/docker-compose.yml down acdc
docker rmi mservatius/acdc:arm
docker build -t acdc:arm .
docker tag acdc:arm mservatius/acdc:arm
docker push mservatius/acdc:arm
docker rmi acdc:arm
docker rmi mservatius/acdc:arm
docker compose -f /home/ubuntu/apps/docker/docker-compose.yml up acdc -d