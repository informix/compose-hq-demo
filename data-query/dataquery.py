import os 
os.system('pip install requests')
from datetime import datetime
import json
import requests
import time
import threading
import random
import urllib.parse

sqlStatements2 = [
   "select fname from customer;",
   "select fname from customer where customer_num > 108;"
]

sqlStatements = [
   "select fname from customer;",
   "select fname from customer where customer_num > 108;",
   "select max(ship_charge), min(ship_charge) from orders;",
   "select o.order_num, sum(i.total_price) price, paid_date - order_date span from orders o, items i where o.order_date > '01/01/1989' and o.customer_num > 110 and o.order_num = i.order_num group by 1,3 having count(*) < 5 order by 3;",
   "select order_num, count(*) number, avg(total_price) avg from items group by order_num having count(*) > 2;",
   "select c.customer_num, c.lname, c.company, c.phone, u.call_dtime, u.call_descr from customer c, cust_calls u where c.customer_num =u.customer_num order by 1;",
   "select c.customer_num, c.lname, c.company, c.phone, u.call_dtime, u.call_descr from customer c, outer cust_calls u where c.customer_num=u.customer_num order by 1",
   "select c.customer_num, c.lname, o.order_num, i.stock_num, i.manu_code, i.quantity from customer c, outer (orders o, items i) where c.customer_num=o.customer_num and o.order_num=i.order_num and manu_code IN ('KAR', 'SHM') order by lname;",
   "select * from stock where description like '%bicycle%' and manu_code not like 'PRC' order by description, manu_code",
   "select order_num, total_price from items a where 10 > (select count(*) from items b where b.total_price < a.total_price) order by total_price",
   "select distinct stock_num, manu_code from stock where unit_price < 25.00 union select stock_num, manu_code from items where quantity > 3"
]

if os.environ.get('NUM_THREADS'):
       numThreads=int(os.environ['NUM_THREADS'])
else: 
   numThreads=1

if os.environ.get('REST_ENDPOINT'):
   API_ENDPOINT=os.environ['REST_ENDPOINT']
else: 
   API_ENDPOINT="http://server2:27018/stores_demo"


print ("REST_ENDPOINT: ", API_ENDPOINT)

timelive=60
headers={'Content-type': 'application/json'}


def waitForWL():
    API_URL="http://server2:27018/sysmaster/sysdatabases"
    data= { 'query': '{"name": "sysmaster" }' }
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
    API_URL="http://server2:27018/sysmaster/sysdatabases"
    data= { 'query': '{"name": "stores_demo" }' }
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
    API_URL="http://server2:27018/stores_demo/customer"
    data= { 'query': '{"customer_num": 101}' }
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




def workerThread(tid):
    print ("Thread %d Starting:" % (tid))
    arrSize = len(sqlStatements)
    while True:
        rnd = random.randint(1,arrSize)-1
        sql=sqlStatements[rnd]
        encSQL=urllib.parse.quote('{"$sql": "' + sql + '"}')
        qryURL = API_ENDPOINT + '/system.sql?query=' + encSQL
        rs=requests.get(url=qryURL) 
        #print("Result:", rs, sql)
        #print("Result.content:", rs.content)




waitForWL()
waitForDatabase()
waitForDatabaseTable()

threads = []
for i in range(numThreads):
    t = threading.Thread(target=workerThread, args=[i])
    threads.append(t)
    t.start()





