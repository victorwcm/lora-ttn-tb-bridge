# -*- coding: utf-8 -*-
import paho.mqtt.client as mqtt
import json
import base64
import struct

# load configurations from YAML config file
# with open("config.yaml", 'r') as yamlfile:
#    cfg_params = yaml.load(yamlfile)


# FIRST - subscribe to the ttn mqtt broker for getting data
# the callback for when the client receives a CONNACK response from the broker.
def on_connect(client, userdata, rc):
	print("Connected with result code "+str(rc))
	# Subscribing in on_connect() means that if we lose the connection and
	# reconnect then subscriptions will be renewed.
	mqtt_ttn.subscribe("+/devices/+/up")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
	print "Topic: ", msg.topic+"\nMessage: "+str(msg.payload)
	ttn_msg = json.loads(str(msg.payload))
	datab64 = ttn_msg['payload_raw']
	received_bytes = bytearray(base64.b64decode(datab64))
	lat, long = struct.unpack('2f', received_bytes[1:10])
	cur_data = '{"latitude":' + str(lat) + ',"longitude":' + str(long) + '}'
	print(cur_data)
	# SECOND - connect to TB
	mqtt_tb.publish("v1/devices/me/telemetry", cur_data)

mqtt_tb = mqtt.Client("")
mqtt_tb.username_pw_set("tuO7zcFdeDLRs1trFbPq", "")
mqtt_tb.connect("demo.thingsboard.io", 1883)
mqtt_ttn = mqtt.Client()
mqtt_ttn.on_connect = on_connect
mqtt_ttn.on_message = on_message
mqtt_ttn.username_pw_set("jualabs-first-app", "ttn-account-v2.vx435Pm0OOkxCnstrrKqbJO1PdrLTmKkYL2EQTUPRxU")
mqtt_ttn.connect("thethings.meshed.com.au", 1883, 60)
# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
mqtt_ttn.loop_forever()

