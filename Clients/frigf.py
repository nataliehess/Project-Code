#This Code represents Oven which connects to an MQTT Broker which gets and sets device attributes 
#Vamshi Teja

#edit this file to refrigrator functionalities

import paho.mqtt.client as paho
import RPi.GPIO as GPIO
import json, time

# device credentials
device_id        = '<DEVICE_ID>'      #  set your device id (will be the MQTT client username)
device_secret    = '<DEVICE_SECRET>'  #  set your device secret (will be the MQTT client password)
random_client_id = '<CLIENT_ID>'      #  set a random client_id (max 23 char)


# Board settings 

buttonPin    = 7
ledPin       = 12
door_stat    = 21
cur_temp     = 23
cur_state    = 29
temp_set     = 31
door_set     = 33
preheat_set  = 8

GPIO.setmode(GPIO.BOARD)          # use P1 header pin numbering convention
GPIO.cleanup()                    # clean up resources
GPIO.setup(door_stat, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(cur_temp, GPIO.IN)
GPIO.setup(cur_state, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(temp_set, GPIO.OUT)
GPIO.setup(door_set, GPIO.OUT)
GPIO.setup(preheat_set,  GPIO.OUT)

#to read analog values
def RC_Analog (Pin):  
  counter = 0  
  # Discharge capacitor  
  GPIO.setup(Pin, GPIO.OUT)  
  GPIO.output(Pin, GPIO.LOW)  
  time.sleep(0.1)  
  GPIO.setup(Pin, GPIO.IN)  
  # Count loops until voltage across capacitor reads high on GPIO  
  while(GPIO.input(Pin)==GPIO.LOW):  
        counter =counter+1  
  return counter


# Callback events #

# connection event
def on_connect(client, data, flags, rc):
    print('Connected, rc: ' + str(rc))

# subscription event
def on_subscribe(client, userdata, mid, gqos):
    print('Subscribed: ' + str(mid))

# received message event
def on_message(client, obj, msg):
    # get the JSON message
    json_data = msg.payload
    # check the status property value
    print(json_data)
    door_set = json.loads(json_data)['oven'][0]['door_set']
    temp_set = json.loads(json_data)['oven'][1]['temp_set']
    preheat_set = json.loads(json_data)['oven'][0]['preheat_set']
    if door_set == 'on':
        door_set = GPIO.HIGH
        GPIO.output(door_set, GPIO.HIGH)
    elif door_set == 'off':
        led_status = GPIO.LOW
        GPIO.output(ledPin, GPIO.LOW)
    if preheat_set == 'on':
        door_set = GPIO.HIGH
        GPIO.output(door_set, GPIO.HIGH)
    elif(door_set == 'off'):
        led_status = GPIO.LOW
        GPIO.output(ledPin, GPIO.LOW)
    print(temp_set)

    # confirm changes to 
    client.publish(out_topic, json_data)



# MQTT settings #


# create the MQTT client
client = paho.Client(client_id=random_client_id, protocol=paho.MQTTv31)  # * set a random string (max 23 chars)

# assign event callbacks
client.on_message = on_message
client.on_connect = on_connect
client.on_subscribe = on_subscribe


# device topics
in_oven_preheat_set  = 'oven/preheat_set' + device_id + '/get'   # receiving messages
in_oven_temp_set     = 'oven/temp_set' + device_id + '/get'      # receiving messages
in_oven_door_set     = 'oven/door_set' + device_id + '/get'      # receiving messages
out_oven_door_stat   = 'oven/door_stat' + device_id + '/set'     # publishing messages
out_oven_cur_stat    = 'oven/cur_stat' + device_id + '/set'      # publishing messages
out_oven_cur_temp    = 'oven/cur_temp' + device_id + '/set'      # publishing messages


# client connection
client.username_pw_set(device_id, device_secret)      # MQTT server credentials
client.connect("127.0.0.1",1883,60)                   # MQTT server address
client.subscribe('oven/#/get', 1)                     # MQTT subscribtion (with QoS level 0)


# Button logic 
prev_door_stat        = GPIO.LOW
led_status_door_stat  = GPIO.LOW
prev_cur_stat         = GPIO.LOW
led_status_cur_stat   = GPIO.LOW
updated_at  = 0  # the last time the output pin was toggled
debounce    = 0.5  # the debounce time, increase if the output flickers

# Continue the network loop, exit when an error occurs
rc = 0
while rc == 0:
    rc = client.loop()
    door_status = GPIO.input(door_stat)
    cur_status  = GPIO.input(cur_stat)
    cur_temp    = RC_Analog(cur_temp)
    if door_status != prev_door_stat and time.time() - updated_at > debounce:
        prev_door_stat = door_status
        updated_at  = time.time()

        if door_status:
            door_status = not led_status_door_stat
            door_stat_payload = 'off'
            if led_status_door_stat == GPIO.HIGH:
                door_stat_payload = 'on'
            # effectively update the light status
            GPIO.output(door_stat, door_status)
            payload_door = { 'oven': [{ 'id': '518be5a700045e1521000001', 'door_status': payload_door }] }
    if cur_status != prev_cur_stat and time.time() - updated_at > debounce:
        prev_cur_stat = cur_status
        updated_at  = time.time()

        if cur_status:
            cur_status = not led_status_door_stat
            cur_stat_payload = 'off'
            if led_status_cur_stat == GPIO.HIGH:
                cur_stat_payload = 'on'
            # effectively update the light status
            GPIO.output(door_stat, door_status)
            payload_cur = { 'oven': [{ 'id': '', 'cur_status': payload_cur }] }
            payload_temp = { 'oven': [{ 'id': '', 'cur_temp': cur_temp }] }
client.publish(out_oven_door_stat, json.dumps(payload_door))
client.publish(out_oven_cur_stat, json.dumps(payload_cur))
client.publish(out_oven_cur_temp, json.dumps(payload_temp))

print('rc: ' + str(rc)) 
