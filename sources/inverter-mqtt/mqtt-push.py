import json
import paho.mqtt.client as mqtt
import subprocess
import time


with open('/etc/inverter/mqtt.json') as f:
    config = json.load(f)

MQTT_SERVER = config['server']
#MQTT_PORT = int(MQTT_PORTX)

#MQTT_PORTX = config['port']
MQTT_TOPIC = "test"
MQTT_DEVICENAME = config['devicename']
MQTT_USERNAME = config['username']
MQTT_PASSWORD = config['password']
MQTT_CLIENTID = "testingpaho"



def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    
    
client = mqtt.Client(MQTT_CLIENTID)
client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
client.on_connect = on_connect
client.connect(MQTT_SERVER, 1883, 60)
client.loop_start()

def pushMQTTData(client, name, payload):
    
    state_topic = "UPS/sensor/{}/{}/state".format(MQTT_DEVICENAME, name)

    
    client.publish(state_topic, payload)


result = subprocess.run(["/opt/inverter-cli/bin/inverter_poller", "-1"], capture_output=True, text=True)
inverter_data = json.loads(result.stdout)

inverter_mode = inverter_data.get('Inverter_mode')
if inverter_mode is not None:
       pushMQTTData(client, "Inverter_mode", str(inverter_mode))

ac_grid_voltage = inverter_data.get('AC_grid_voltage')
if ac_grid_voltage is not None:
        pushMQTTData(client, "Ac_grid_voltage", str(ac_grid_voltage))

ac_grid_frequency = inverter_data.get('AC_grid_frequency')
if ac_grid_frequency is not None:
        pushMQTTData(client, "Ac_grid_frequency", str(ac_grid_frequency))


client.loop_stop()

