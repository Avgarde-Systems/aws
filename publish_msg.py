import paho.mqtt.client as paho
import ssl
from time import sleep
from random import uniform
import datetime

connflag = False


def on_connect(client, userdata, flags, rc):  # connection
    global connflag
    print("Connected to AWS")
    connflag = True
    # if connection is successful, rc value will be 0
    print("Connection returned result: " + str(rc))
    # print(flags)


def on_message(client, userdata, msg):  # Func for Sending msg
    print(msg.topic + " " + str(msg.payload))


mqttc = paho.Client()
# create an mqtt client object
# attach call back function
mqttc.on_connect = on_connect
# attach on_connect function written in the
# mqtt class, (which will be invoked whenever
# mqtt client gets connected with the broker)
# is attached with the on_connect function
# written by you.


mqttc.on_message = on_message  # assign on_message func
# attach on_message function written inside
# mqtt class (which will be invoked whenever
# mqtt client gets a message) with the on_message
# function written by you

#### Change following parameters ####
#ahgvl0vt66ic3-ats.iot.ap-south-1.amazonaws.com
awshost = "ahgvl0vt66ic3-ats.iot.ap-south-1.amazonaws.com"  # Broker
awsport = 8883  # The secure Port no.
clientId = "iitSensorData"  # Thing_Name
thingName = "iitSensorData"
caPath = "certificates/AmazonRootCA1.crt"  # Amazon's certificate from Third party                                     # Root_CA_Certificate_Name
certPath = "certificates/fd1f1448997f7a4a001341074b1e817c6be9c8baee305f8b8363dbb3fcb4bfd0_certificate.pem"  # <Thing_Name>.cert.pem.crt. Thing's certificate from Amazon
keyPath = "certificates/fd1f1448997f7a4a001341074b1e817c6be9c8baee305f8b8363dbb3fcb4bfd0_private.pem"  # <Thing_Name>.private.key Thing's private key from Amazon

mqttc.tls_set(caPath, certfile=certPath, keyfile=keyPath, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2,
              ciphers=None)  # pass parameters
mqttc.connect(awshost, awsport, keepalive=60)  # connect to aws server
mqttc.loop_start()  # Start the loop

# Add the water parameters
temperatureData = 98  # dummy temperature data. Please assign the temperature value here
phData = 2  # dummy ph data. Please assign the PH value here
doData = 6.6  # dummy dissolved oxygen data. Please assign the dissolved oxygen value here

# Publish the data to the aws
while 1:
    sleep(10)  # I have added a delay of 10 second. Please modify accordingly
    if connflag == True:
        timeStamp = datetime.datetime.now()
        # Generating Temperature Readings
        message = '{"timeStamp":' + '"' + str(timeStamp) + '",' + '"temperature":' + str(
            temperatureData) + ',' + '"PH":' + str(phData) + ',' + '"DO":' + str(doData) + '}'
        mqttc.publish("sensorData789", message, 1)  # topic: temperature # Publishing Temperature values
        print("Temperature:" + "%.2f" % temperatureData)  # Print sent temperature msg on console
        print("PH:" + "%.2f" % phData)  # Print sent ph msg on console
        print("DO:" + "%.2f" % doData)  # Print sent DO msg on console


    else:
        print("waiting for connection...")
