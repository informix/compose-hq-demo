#!/bin/bash


function setup_system()
{ 

echo "N" | dbaccessdemo7

}


function wait_for_sysadmin() {
while true 
do
   cnt=`echo "select count(*) from sysdatabases where name='sysadmin' "| dbaccess sysmaster - |grep -v count|tr -d ' \n'`
   if [[ $cnt == "1" ]]
   then
      break
   else
      sleep 1
   fi

done
}


wait_for_sysadmin
setup_system

curl -X PUT -basic -u admin:Passw0rd -H 'Content-Type: application/json' -H 'Accept: application/json' http://hqserver:8080/api/informix/3/monitoring --data-binary "{sensors: [ {'type': 'diskio', 'runInterval': 15, 'dataRetention': 30, 'disabled': false}, {'type': 'seqscans', 'runInterval': 15, 'dataRetention': 30, 'disabled': false}, {'type': 'vps', 'runInterval': 60, 'dataRetention': 30, 'disabled': false} ] } "