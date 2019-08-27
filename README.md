# compose-hq-demo

## Default compose file:
    docker-compose.yml

## Steps

### Start docker compose:
    1.  In dir where compose file exists
    2.  docker-compose up 

### Stop and remove Containers & volume
    1.  docker-compose down -v

### Scaling 
    1. docker-compose -f dokcer-compose.scale.yml up --scale informix-server=2

 * Scaling doesn't allow variable replacement of ```hostname```


### Build compose (Not used in this demo):
    1.  In dir where docker-compose.yml exists
    2.  docker-compose build 
 
 * Used if you need to build a custom image 
