import paho.mqtt.client as mqtt
import json
import subprocess

with open('/etc/inverter/mqtt.json') as f:
    config = json.load(f)

MQTT_SERVER = config['server']
MQTT_PORT = config['port']
#MQTT_TOPIC = config['topic']
#MQTT_DEVICENAME = config['devicename']
MQTT_USERNAME = config['username']
MQTT_PASSWORD = config['password']
MQTT_CLIENTID = "UPS-SUB"

def on_message(client, userdata, msg):
    rawcmd = msg.payload.decode("utf-8")
    print("Incoming request send: [{}] to inverter.".format(rawcmd))
    subprocess.run(["/opt/inverter-cli/bin/inverter_poller", "-r", rawcmd])

client = mqtt.Client(client_id=MQTT_CLIENTID)
client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
client.on_message = on_message
client.connect(MQTT_SERVER, MQTT_PORT)
client.subscribe("UPS/rwcmd", qos=1)

client.loop_forever()
