FROM python:3.6-alpine

ADD  datagen.py /home 
ADD  datagen_entry.sh    /home 


WORKDIR /home
RUN pip install paho-mqtt
RUN chmod 755 /home/*.sh 


ENTRYPOINT ["/home/datagen_entry.sh"]