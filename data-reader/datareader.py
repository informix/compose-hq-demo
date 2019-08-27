import os 
os.system('pip install paho-mqtt')
os.system('pip install requests')
from datetime import datetime
import paho.mqtt.client as mqtt
import json
import requests
import time

if os.environ.get('BROKER'):
   broker=os.environ['BROKER']
else:
   broker="msgbroker"

if os.environ.get('BROKER_PORT'):
   port=int(os.environ['BROKER_PORT'])
else: 
   port=1883

if os.environ.get('BROKER_TOPIC'):
   topic=os.environ['BROKER_TOPIC']
else: 
   topic='datagen/datagen1'

if os.environ.get('REST_ENDPOINT'):
   API_ENDPOINT=os.environ['REST_ENDPOINT']
else: 
   API_ENDPOINT="http://server1:27018/tsdb/tstab_v"


print ("BROKER: ", broker)
print ("BROKER_PORT: ", port)
print ("BROKER_TOPIC: ", topic)
print ("REST_ENDPOINT: ", API_ENDPOINT)

timelive=60
headers={'Content-type': 'application/json'}


def waitForWL():
    API_URL="http://server1:27018/sysmaster/sysdatabases"
    data= { 'query': '{"name": "tsdb" }' }
    while True:
        try:
         rs=requests.get(url=API_URL, params=data, headers=headers)
         print ("Connection Made")
         break;
        except requests.exceptions.RequestException as e:
            print ("ERROR: ",e)
            print ("Sleeping 1 second")
            time.sleep(1) 


def waitForDatabase():
    API_URL="http://server1:27018/sysmaster/sysdatabases"
    data= { 'query': '{"name": "tsdb" }' }
    while True:
        try:
            rs=requests.get(url=API_URL, params=data, headers=headers)
            if "errmsg" in rs.text:
                print("**** ERROR **** - Retrying")
                continue;
            if len(rs.json()) == 0: 
                print ("Waiting For Database Creation")
                print ("Sleeping 1 second")
            else:                                                          
                print ("Database Found")
                break;
        except requests.exceptions.RequestException as e:
            print ("ERROR: ",e)
            print ("Sleeping 1 second")
        time.sleep(1) 

def waitForDatabaseTable():
    API_URL="http://server1:27018/tsdb/systables"
    data= { 'query': '{"tabname": "tstab_v" }' }
    while True:
        try:
            rs=requests.get(url=API_URL, params=data, headers=headers)
            if "errmsg" in rs.text:
                print("**** ERROR **** - Retrying")
                continue;
            if len(rs.json()) == 0: 
                print ("Waiting For Table Creation")
                print ("Sleeping 1 second")
            else:                                                          
                print ("Table Found")
                break;
        except requests.exceptions.RequestException as e:
            print ("ERROR: ",e)
            print ("Sleeping 1 second")
        time.sleep(1) 



def on_connect(client, userdata, flags, rc):
  print("Connected with result code "+str(rc))
  client.subscribe(topic)

def on_message(client, userdata, msg):
    msgdata=json.loads(msg.payload.decode())
    print(msgdata)
    jdata=msgdata['json_data']
    data= {
       "id" : msgdata['id'],
       "tstamp" : msgdata['tstamp'],
       "json_data" : jdata 
    }
    rs=requests.post(url=API_ENDPOINT, data=json.dumps(data), headers=headers)
    print("Result:", rs)




waitForWL()
waitForDatabase()
waitForDatabaseTable()

client = mqtt.Client()
client.connect(broker,port,timelive)
client.on_connect = on_connect
client.on_message = on_message
client.loop_forever()



