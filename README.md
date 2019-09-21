# compose-hq-demo

## Default compose file:
    docker-compose.yml

## Steps

### Start docker compose:
    1.  cd to project directory 
    2.  Run __chmod 777 -R *__
    2.  Run __docker-compose up__ 

### Up & Running:
    1.  After a few minutes 2 informix containers will be  start.  With a load placed on both servers.
    2.  An HQ server will be started 
    3.  Go to http://<ip address> (user: admin Password: Passw0rd) 

### Stop and remove Containers & volume
    1.  docker-compose down -v


