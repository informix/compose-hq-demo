## compose-hq-demo

### Default compose file:
    docker-compose.yml

## Steps

Default compose file:
    docker-compose.yml

Build compose:
    1.  In dir where docker-compose.yml exists
    2.  docker-compose build 

Start docker compose:
    1.  In dir where compose file exists
    2.  docker-compose up -d

Stop and remove volume
    1.  docker-compose down -v

docker-compose up --scale informix-server1=2



docker-compose up -e NAME=server --scale informix-server=2