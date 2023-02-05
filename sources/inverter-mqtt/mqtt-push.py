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
MQTT_CLIENTID = "UPS_PUB"



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

while True:
    
    result = subprocess.run(["/opt/inverter-cli/bin/inverter_poller", "-1"], capture_output=True, text=True)
    inverter_data = json.loads(result.stdout)

    Inverter_mode = inverter_data.get('Inverter_mode')
    if Inverter_mode is not None:
        pushMQTTData(client,"Inverter_mode", str(Inverter_mode))

    AC_grid_voltage = inverter_data.get('AC_grid_voltage')
    if AC_grid_voltage is not None:
        pushMQTTData(client,"AC_grid_voltage", str(AC_grid_voltage))
    
    AC_out_voltage = inverter_data.get('AC_out_voltage')
    if AC_out_voltage is not None:
        pushMQTTData(client, "AC_out_voltage",  str(AC_out_voltage))

    AC_out_frequency = inverter_data.get('AC_out_frequency')
    if AC_out_frequency is not None:
        pushMQTTData(client, "AC_out_frequency", str(AC_out_frequency))

    PV_in_voltage = inverter_data.get('PV_in_voltage')
    if PV_in_voltage is not None:
        pushMQTTData(client, "PV_in_voltage", str(PV_in_voltage))

    PV_in_current = inverter_data.get('PV_in_current')
    if PV_in_current is not None:
        pushMQTTData(client, "PV_in_current", str(PV_in_current))

    PV_in_watts = inverter_data.get('PV_in_watts')
    if PV_in_watts is not None:
        pushMQTTData(client, "PV_in_watts", str(PV_in_watts))

    PV_in_watthour = inverter_data.get('PV_in_watthour')
    if PV_in_watthour is not None:
        pushMQTTData(client, "PV_in_watthour", str(PV_in_watthour))

    Load_pct = inverter_data.get('Load_pct')
    if Load_pct is not None:
        pushMQTTData(client, "Load_pct", str(Load_pct))

    Load_watt = inverter_data.get('Load_watt')
    if Load_watt is not None:
        pushMQTTData(client, "Load_watt", str(Load_watt))

    Load_watthour = inverter_data.get('Load_watthour')
    if Load_watthour is not None:
        pushMQTTData(client, "Load_watthour", str(Load_watthour))

    Load_va = inverter_data.get('Load_va')
    if Load_va is not None:
        pushMQTTData(client, "Load_va", str(Load_va))

    Battery_capacity = inverter_data.get('Battery_capacity')
    if Battery_capacity is not None:
        pushMQTTData(client, "Battery_capacity", str(Battery_capacity))

    Battery_voltage = inverter_data.get('Battery_voltage')
    if Battery_voltage is not None:
        pushMQTTData(client, "Battery_voltage", str(Battery_voltage))

    Battery_charge_current = inverter_data.get('Battery_charge_current')
    if Battery_charge_current is not None:
        pushMQTTData(client, "Battery_charge_current", str(Battery_charge_current))

    Battery_discharge_current = inverter_data.get('Battery_discharge_current')
    if Battery_discharge_current is not None:
        pushMQTTData(client, "Battery_discharge_current", str(Battery_discharge_current))

    Load_status_on = inverter_data.get('Load_status_on')
    if Load_status_on is not None:
        pushMQTTData(client, "Load_status_on",str(Load_status_on))

    Out_source_priority = inverter_data.get('Out_source_priority')
    if Out_source_priority is not None:
        pushMQTTData(client, "Out_source_priority", str(Out_source_priority))

    Charger_source_priority = inverter_data.get('Charger_source_priority')
    if Charger_source_priority is not None:
        pushMQTTData(client, "Charger_source_priority", str(Charger_source_priority))

    Battery_redischarge_voltage = inverter_data.get('Battery_redischarge_voltage')
    if Battery_redischarge_voltage is not None:
        pushMQTTData(client, "Battery_redischarge_voltage", str(Battery_redischarge_voltage))
    
    
    AC_grid_frequency = inverter_data.get('AC_grid_frequency')
    if AC_grid_frequency is not None:
        pushMQTTData(client, "AC_grid_frequency", str(AC_grid_frequency))

    SCC_voltage = inverter_data.get('SCC_voltage')
    if SCC_voltage is not None:
        pushMQTTData(client, "SCC_voltage", str(SCC_voltage))


    Bus_voltage = inverter_data.get('Bus_voltage')
    if Bus_voltage is not None:
        pushMQTTData(client, "Bus_voltage", str(Bus_voltage))

    Heatsink_temperature = inverter_data.get('Heatsink_temperature')
    if Heatsink_temperature is not None:
        pushMQTTData(client, "Heatsink_temperature", str(Heatsink_temperature))


    SCC_charge_on = inverter_data.get('SCC_charge_on')
    if SCC_charge_on is not None:
        pushMQTTData(client, "SCC_charge_on",str(SCC_charge_on))

    AC_charge_on = inverter_data.get('AC_charge_on')
    if AC_charge_on is not None:
        pushMQTTData(client, "AC_charge_on", str(AC_charge_on))

    Battery_recharge_voltage = inverter_data.get('Battery_recharge_voltage')
    if Battery_recharge_voltage is not None:
        pushMQTTData(client, "Battery_recharge_voltage", str(Battery_recharge_voltage))

    Battery_under_voltage = inverter_data.get('Battery_under_voltage')
    if Battery_under_voltage is not None:
        pushMQTTData(client, "Battery_under_voltage", str(Battery_under_voltage))

    Battery_bulk_voltage = inverter_data.get('Battery_bulk_voltage')
    if Battery_bulk_voltage is not None:
        pushMQTTData(client, "Battery_bulk_voltage", str(Battery_bulk_voltage))

    Battery_float_voltage = inverter_data.get('Battery_float_voltage')
    if Battery_float_voltage is not None:
        pushMQTTData(client, "Battery_float_voltage", str(Battery_float_voltage))

    Max_grid_charge_current = inverter_data.get('Max_grid_charge_current')
    if Max_grid_charge_current is not None:
        pushMQTTData(client, "Max_grid_charge_current", str(Max_grid_charge_current))

    Max_charge_current = inverter_data.get('Max_charge_current')
    if Max_charge_current is not None:
        pushMQTTData(client, "Max_charge_current", str(Max_charge_current))


    Warnings = inverter_data.get('Warnings')
    if Warnings is not None:
        pushMQTTData(client, "Warnings", str(Warnings))


client.loop_stop()

