import json
import paho.mqtt.client as mqtt
import time


# Read the MQTT configuration from the JSON file
with open('/etc/inverter/mqtt.json', 'r') as f:
    mqtt_config = json.load(f)
    
MQTT_TOPIC = mqtt_config['topic']
MQTT_DEVICENAME = mqtt_config['devicename']
MQTT_CLIENTID = "ups_init2"

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.publish(UPS/AEROX/LWT, payload="online", qos=0, retain=True)
    client.will_set(UPS/AEROX/LWT, payload="offline", qos=2, retain=True)
#client.subscribe("test/#")

#def on_message(client, userdata, msg):
  #  print(msg.topic+" "+str(msg.payload))

def on_publish(client, userdata, mid):
    print("Message published")
    
    
# Create a MQTT client instance
client = mqtt.Client(MQTT_CLIENTID)

# Connect to the MQTT broker
client.username_pw_set(mqtt_config['username'], mqtt_config['password'])
client.connect(mqtt_config['server'], int(mqtt_config['port']), 300)

client.on_connect = on_connect
#client.on_message = on_message
client.on_publish = on_publish


# Publish a message to a topic
#client.publish('test/paho/mqtt', 'Hello World!')

def register_topic(client, name, unit_of_measurement, icon, device_class, measurement_class, entity_category):
     
 

    config_topic = "{}/sensor/{}/{}/config".format(MQTT_TOPIC, MQTT_DEVICENAME, name)
    state_topic = "UPS/sensor/{}/{}/state".format(MQTT_DEVICENAME, name)
    lwt_topic = "UPS/{}/LWT".format(MQTT_DEVICENAME)

    config_message = {
        "name": name,
        "unit_of_measurement": unit_of_measurement,
        "state_topic": state_topic,
        "icon": "mdi:{}".format(icon),
        "unique_id": name,
        "entity_category": entity_category,
        "device": {
            "name": MQTT_DEVICENAME,
            "manufacturer": "Inverex",
            "model": "AeroxIII",
            "identifiers": [MQTT_CLIENTID],
            "connections": [["ip", "192.168.0.112"]]
        },
        "availabilty_topic": lwt_topic
    }


    client.publish(config_topic, payload=json.dumps(config_message), qos=0, retain=False)
    

while True:
  
    register_topic(client, "Qflag", "", "details", "null", "", "diagnostic")
    register_topic(client, "Model", "", "details", "null", "", "diagnostic")
    time.sleep(300)


#client.loop_forever()

# Disconnect from the MQTT broker
client.disconnect()
