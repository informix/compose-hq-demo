import os
os.system('pip install paho-mqtt')
from datetime import datetime
import paho.mqtt.client as mqtt
import json
from time import sleep
import random
from random import randrange


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

print ("BROKER: ", broker)
print ("BROKER_PORT: ", port)
print ("BROKER_TOPIC: ", topic)

scale=0.5;
POKE_SKIP_RANGE=20
POKE_SKIP=randrange(POKE_SKIP_RANGE)



def generateValue(scale):
       return random.random() * scale * 2 -scale;

def on_publish(client, userdata, mid):
    #print("MID Published: ", mid)
    if mid == NUMINS:
        client.disconnect()


client = mqtt.Client(protocol=mqtt.MQTTv31)
client.on_publish = on_publish
client.connect(broker, port)
client.loop_start()

while True:
    # Generate data
    ct = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-1]
    x=abs(generateValue(scale));               
    y=abs(generateValue(scale));               
    z=abs(generateValue(scale));  



    # Publish Data
    msgstr = '{  "id":"1", "tstamp" : "%s",  "json_data" : { "x": %f, "y": %f, "z" : %f }  }'  % (ct,x,y,z) 
    (result, mid) = client.publish(topic, msgstr, qos=1)
    if result != mqtt.MQTT_ERR_SUCCESS:
        print("Error Publish: ", )


    # Randomize Data
    if (scale > 0.5) :                         
      drop = min(0.1, scale/5.0);             
      scale = max(0.5, scale-drop);           
      #print ("drop = %f" % (drop));           
    else:                                      
      if POKE_SKIP < 1:                       
         poke = randrange(5)             
         #print ("poke= %d" % (poke));    
         scale += poke;                  
         POKE_SKIP=randrange(POKE_SKIP_RANGE)
      else:                                  
         POKE_SKIP -=1;                      
                                             
    #print ("POKE_SKIP = %d" % (POKE_SKIP));   
    #print ("Scale = %f" % (scale));        

    sleep (0.5)
                                    
client.loop_forever()     
