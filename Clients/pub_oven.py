#oven_appliance mqtt client publish  code
#vamshi Teja

import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO

door_status      = 21
cur_temp         = 23
pre_heat_status  = 29


GPIO.setmode(GPIO.BOARD)

GPIO.setup(door_status, GPIO.IN) 
GPIO.setup(cur_temp, GPIO.IN) 
GPIO.setup(pre_heat_status, GPIO.IN)

door_stat       = GPIO.input(door_status) 
cur_temp        = GPIO.input(cur_temp) 
pre_heat_status = GPIO.input(pre_heat_status)

client_id = "oven"
mqttc = mqtt.Client()
mqttc.connect(“localhost”, 1883,60)
msgs = [("oven/door_status",door_status,1,True), ("oven/cur_temp", cur_temp, 1, True),("oven/pre_heat_status",pre_heat_status,1,True)]
mqttc.publish(msgs,hostname = "127.0.0.1" )
mqttc.loop(2)                         //timeout = 2s 
