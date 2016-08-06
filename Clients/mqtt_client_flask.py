#program to 
from flask import Flask, render_template, request
import paho.mqtt.client as mqtt
from datetime import datetime

app = Flask(__name__)

@app.route('/', methods = ['POST', 'GET'])
def capture():
    timestring=datetime.now().strftime("%Y%m%d-%H%M%S")
    if 'sessionName' in request.form:
        sessionName = request.form['sessionName']
        path = sessionName + "_" + timestring
        client.publish('all/camera/'+path, 'all')
        return render_template ('capture.html', path=path, timestring=timestring, sessionName=sessionName)
       
    else:
        return render_template ('capture.html',timestring=timestring)

# paho callbacks
def on_connect(client, userdata, flags, rc):

    #sub here will re subscribe on reconnection
    client.subscribe("oven/#")
    client.subscribe("refrigrator/#")

# Main Code
if __name__=='__main__':

    client = mqtt.Client()
    client.on_connect = on_connect
    client.connect("127.0.0.1",1883,60)
    client.loop_start()
    client.publish('debug', 'server running')

    app.run(host = '0.0.0.0' , debug = True, port=5000)
