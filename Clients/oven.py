import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import paho.mqtt.subscribe as subscribe
import RPi.GPIO as GPIO

#pin_definitions
door_stat     = 21
cur_temp  = 23
cur_state = 29
temp_set      = 31
door_set      = 33
preheat_set   = 8

GPIO.setup(door_stat, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(cur_temp, GPIO.IN)
GPIO.setup(cur_state, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(temp_set, GPIO.OUT)
GPIO.setup(door_set, GPIO.OUT)
GPIO.setup(preheat_set,  GPIO.OUT)
GPIO.setmode(GPIO.BCM)

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

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, rc):
    print("Connected with result code "+str(rc))
	# Subscribing in on_connect() means that if we lose the connection and
	# reconnect then subscriptions will be renewed.
	client.subscribe("$SYS/#")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
	print(msg.topic+" "+str(msg.payload))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("iot.eclipse.org", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()

