import json
import paho.mqtt.client as mqtt
import time

MQTT_TOPIC = "test"
MQTT_DEVICENAME = "inverter"
MQTT_CLIENTID = "testingpaho"



# Read the MQTT configuration from the JSON file
with open('/etc/inverter/mqtt.json', 'r') as f:
    mqtt_config = json.load(f)


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
 #   client.subscribe("test/#")

#def on_message(client, userdata, msg):
  #  print(msg.topic+" "+str(msg.payload))

def on_publish(client, userdata, mid):
    print("Message published")
    
    
# Create a MQTT client instance
client = mqtt.Client(client_id="testingpaho")

# Connect to the MQTT broker
client.username_pw_set(mqtt_config['username'], mqtt_config['password'])
client.connect(mqtt_config['server'], int(mqtt_config['port']), 60)

client.on_connect = on_connect
#client.on_message = on_message
client.on_publish = on_publish


# Publish a message to a topic
#client.publish('test/paho/mqtt', 'Hello World!')

def register_topic(client, name, unit_of_measurement, icon, device_class, entity_category):
  #while True:     

    config_topic = "{}/sensor/{}/{}/config".format(MQTT_TOPIC, MQTT_DEVICENAME, name)
    state_topic = "{}/sensor/{}/{}/state".format(MQTT_TOPIC, MQTT_DEVICENAME, name)
    lwt_topic = "{}/{}/{}/LWT".format(MQTT_TOPIC, MQTT_DEVICENAME, name)

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

    client.publish(config_topic, payload=json.dumps(config_message), qos=0, retain=True)
    client.publish(lwt_topic, payload="online", qos=0, retain=True)
   #time.sleep(1) 

registerTopic("Inverter_mode", "", "solar-power", "aqi", "", "config")                                        
registerTopic("AC_grid_voltage", "V", "power-plug", "voltage", "", "diagnostic")
registerTopic("AC_grid_frequency", "Hz", "current-ac", "frequency", "", "diagnostic")
registerTopic("AC_out_voltage", "V", "power-plug", "voltage", "", "diagnostic")
registerTopic("AC_out_frequency", "Hz", "current-ac", "frequency", "", "diagnostic")
registerTopic("PV_in_voltage", "V", "solar-panel-large", "voltage", "", "config")
registerTopic("PV_in_current", "A", "solar-panel-large", "current", "", "config")
registerTopic("PV_in_watts", "W", "solar-panel-large", "power", "measurement", "config")
registerTopic("PV_in_watthour", "Wh", "solar-panel-large", "energy", "measurement", "config")
registerTopic("SCC_voltage", "V", "current-dc", "voltage", "", "diagnostic")
registerTopic("Load_pct", "%", "brightness-percent", "power_factor", "", "config")
registerTopic("Load_watt", "W", "chart-bell-curve", "power", "measurement", "config")
registerTopic("Load_watthour", "Wh", "chart-bell-curve", "energy", "measurement", "config")
registerTopic("Load_va", "VA", "chart-bell-curve", "apparent_power", "", "diagnostic")
registerTopic("Bus_voltage", "V", "details", "voltage", "", "diagnostic")
registerTopic("Heatsink_temperature", "C", "thermometer", "temperature", "", "diagnostic")
registerTopic("Battery_capacity", "%", "battery-outline", "battery", "", "config")
registerTopic("Battery_voltage", "V", "battery-outline", "voltage", "", "diagnostic")
registerTopic("Battery_charge_current", "A", "current-dc", "current", "", "diagnostic")
registerTopic("Battery_discharge_current", "A", "current-dc", "current", "", "diagnostic")
registerTopic("Load_status_on", "", "power", "aqi", "", "config")
registerTopic("SCC_charge_on", "", "power", "aqi", "", "config")
registerTopic("AC_charge_on", "", "power", "aqi", "", "config")
registerTopic("Battery_recharge_voltage", "V", "current-dc", "voltage", "", "diagnostic")
registerTopic("Battery_under_voltage", "V", "current-dc", "voltage", "", "diagnostic")
registerTopic("Battery_bulk_voltage", "V", "current-dc", "voltage", "", "diagnostic")
registerTopic("Battery_float_voltage", "V", "current-dc", "voltage", "", "config")
registerTopic("Max_grid_charge_current", "A", "current-ac", "current", "", "diagnostic")
registerTopic("Max_charge_current", "A", "current-ac", "current", "", "diagnostic")
registerTopic("Out_source_priority", "", "grid", "aqi", "", "config")
registerTopic("Charger_source_priority", "", "solar-power", "aqi", "", "config")
registerTopic("Battery_redischarge_voltage", "V", "battery-negative", "voltage", "", "diagnostic")
registerTopic("Warnings", "", "", "aqi", "", "diagnostic")

#client.loop_forever()

# Disconnect from the MQTT broker
#client.disconnect()
