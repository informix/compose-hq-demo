FROM python:3.6-alpine

ADD  datareader.py /home 
ADD  datareader_entry.sh    /home 

WORKDIR /home
RUN pip install paho-mqtt
RUN pip install requests 
RUN chmod 755 /home/*.sh 


RUN apk add curl

ENTRYPOINT ["/home/datareader_entry.sh"]