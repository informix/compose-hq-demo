import os
os.system('pip install requests')
from datetime import datetime
import json
import requests
import time

if os.environ.get('REST_ENDPOINT'):
   API_ENDPOINT=os.environ['REST_ENDPOINT']
else:
   API_ENDPOINT="http://server1:27018/tsdb/tstab_v"

print ("REST_ENDPOINT: ", API_ENDPOINT)

timelive=60
headers={'Content-type': 'application/json'}
NUMINS=10

def insert_data():
    for i in range(1, NUMINS+1):
       ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-1]
       print("ts: ", ts);
       jdata={
         "x": 5.4,
         "y": 3.2
       }
       data= {
          "id" : 1,
          "tstamp" : ts,
          "json_data" : jdata
       }
       print("data: ", data);
       rs=requests.post(url=API_ENDPOINT, data=json.dumps(data), headers=headers)
       print("Result:", rs)


insert_data()
