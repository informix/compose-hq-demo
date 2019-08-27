#!/bin/bash


function setup_system()
{ 

dbaccess - $INFORMIX_CONFIG_DIR/timeseries_generic.sql

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
