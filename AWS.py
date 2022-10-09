import paho.mqtt.client as paho
from time import sleep
from random import uniform
import datetime
import json

connflag = False

def datetime_to_int(dt):
    return int(dt.strftime("%Y%m%d%H%M%S"))
    
def on_connect(client, userdata, flags, rc):                #  connection
    global connflag
    print("Connected to AWS")
    connflag = True
    #if connection is successful, rc value will be 0
    print("Connection returned result: " + str(rc) )
    #print(flags)

def on_message(client, userdata, msg):                      # Func for Sending msg
    print(msg.topic+" "+str(msg.payload))

mqttc = paho.Client()
#create an mqtt client object
#attach call back function
mqttc.on_connect = on_connect
#attach on_connect function written in the
#mqtt class, (which will be invoked whenever
#mqtt client gets connected with the broker)
#is attached with the on_connect function
#written by you.

mqttc.on_message = on_message                               # assign on_message func


ValveStatus = 1011 #dummy status data. Please assign the status value here




def on_message(client, userdata, message):
    print("message received " ,str(message.payload.decode("utf-8")))
    print("message topic=",message.topic)
    print("message qos=",message.qos)
    print("message retain flag=",message.retain)


while 1:
    sleep(2) #I have added a delay of 10 second. Please modify accordingly
    if connflag == True:
        timeStamp=datetime_to_int(datetime.datetime.now())
        valId1 = "001"
        valstatus1="1"
        valId2="002"
        valstatus2="0"
        message = {"data": valId1+valstatus1 + "," + valId2+valstatus2  }
        print(json.dumps(message))
        #mqttc.publish(valvestopic, json.dumps(message), 1)        # topic: Valvedata # Publishing Temperature values
        #print("Valvedata:" + "%.2f" % ValveStatus ) # Print sent temperature msg on console
        
        #now public cycle start and end event
        if((counter > 2) or (counter > 6)):
            counter = 0
            print("publishing data")
            if(cyclestate == True):
                #cyclemessage={"cycle":cyclecounter, 02"}
                cyclemessage={"cycle":{"cycle":cyclecounter, "mode":1, "status": 1, "data":"0011,0020,0032,0043,0056"}}
                print(cyclemessage)
                mqttc.publish(cycletopic,json.dumps(cyclemessage), 1)
                cyclestate = False
                cyclecounter = cyclecounter + 1
            else:
#                 mqttc.publish(cycletopic, str(timeStamp) + "," + "0", 1)
                 cyclestate = True
        else:
            counter = counter + 1
        
    else:
        print("waiting for connection...")




