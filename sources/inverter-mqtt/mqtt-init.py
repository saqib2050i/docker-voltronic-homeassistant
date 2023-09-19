import json
import paho.mqtt.client as mqtt
import time


# Read the MQTT configuration from the JSON file
with open('/etc/inverter/mqtt.json', 'r') as f:
    mqtt_config = json.load(f)
    
MQTT_TOPIC = mqtt_config['topic']
MQTT_DEVICENAME = mqtt_config['devicename']
MQTT_CLIENTID = "ups_init"

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
    lwt_topic = "UPS/AEROX/LWT"

    config_message = {
        "name": name,
        "unit_of_measurement": unit_of_measurement,
        "state_topic": state_topic,
        "icon": "mdi:{}".format(icon),
        "unique_id": name,
        "entity_category": entity_category,
        "device_class": device_class,
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

    register_topic(client,"Inverter_mode", "", "solar-power", "aqi", "", "config")
    register_topic(client,"AC_grid_voltage", "V", "power-plug", "voltage", "", "diagnostic")
    register_topic(client, "AC_grid_frequency", "Hz", "current-ac", "frequency", "", "diagnostic")
    register_topic(client, "AC_out_voltage", "V", "power-plug", "voltage", "", "diagnostic")
    register_topic(client, "AC_out_frequency", "Hz", "current-ac", "frequency", "", "diagnostic")
    register_topic(client, "PV_in_voltage", "V", "solar-panel-large", "voltage", "", "config")
    register_topic(client, "PV_in_current", "A", "solar-panel-large", "current", "", "config")
    register_topic(client, "PV_in_watts", "W", "solar-panel-large", "power", "measurement", "config")
    register_topic(client, "PV_in_watthour", "Wh", "solar-panel-large", "energy", "measurement", "config")
    register_topic(client, "SCC_voltage", "V", "current-dc", "voltage", "", "diagnostic")
    register_topic(client, "Load_pct", "%", "brightness-percent", "power_factor", "", "config")
    register_topic(client, "Load_watt", "W", "chart-bell-curve", "power", "measurement", "config")
    register_topic(client, "Load_watthour", "Wh", "chart-bell-curve", "energy", "measurement", "config")
    register_topic(client, "Load_va", "VA", "chart-bell-curve", "apparent_power", "", "diagnostic")
    register_topic(client, "Bus_voltage", "V", "details", "voltage", "", "diagnostic")
    register_topic(client, "Heatsink_temperature", "C", "thermometer", "temperature", "", "diagnostic")
    register_topic(client, "Battery_capacity", "%", "battery-outline", "battery", "", "config")
    register_topic(client, "Battery_voltage", "V", "battery-outline", "voltage", "", "diagnostic")
    register_topic(client, "Battery_charge_current", "A", "current-dc", "current", "", "diagnostic")
    register_topic(client, "Battery_discharge_current", "A", "current-dc", "current", "", "diagnostic")
    register_topic(client, "Load_status_on", "", "power", "aqi", "", "config")
    register_topic(client, "SCC_charge_on", "", "power", "aqi", "", "config")
    register_topic(client, "AC_charge_on", "", "power", "aqi", "", "config")
    register_topic(client, "Battery_recharge_voltage", "V", "current-dc", "voltage", "", "diagnostic")
    register_topic(client, "Battery_under_voltage", "V", "current-dc", "voltage", "", "diagnostic")
    register_topic(client, "Battery_bulk_voltage", "V", "current-dc", "voltage", "", "diagnostic")
    register_topic(client, "Battery_float_voltage", "V", "current-dc", "voltage", "", "config")
    register_topic(client, "Max_grid_charge_current", "A", "current-ac", "current", "", "diagnostic")
    register_topic(client, "Max_charge_current", "A", "current-ac", "current", "", "diagnostic")
    register_topic(client, "Out_source_priority", "", "grid", "aqi", "", "config")
    register_topic(client, "Charger_source_priority", "", "solar-power", "aqi", "", "config")
    register_topic(client, "Battery_redischarge_voltage", "V", "battery-negative", "voltage", "", "diagnostic")
    register_topic(client, "Warnings", "", "", "aqi", "", "diagnostic")
    time.sleep(300)


#client.loop_forever()

# Disconnect from the MQTT broker
client.disconnect()
