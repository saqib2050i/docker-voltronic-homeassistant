#!/bin/bash
#
# Simple script to register the MQTT topics when the container starts for the first time...

MQTT_SERVER=`cat /etc/inverter/mqtt.json | jq '.server' -r`
MQTT_PORT=`cat /etc/inverter/mqtt.json | jq '.port' -r`
MQTT_TOPIC=`cat /etc/inverter/mqtt.json | jq '.topic' -r`
MQTT_DEVICENAME=`cat /etc/inverter/mqtt.json | jq '.devicename' -r`
MQTT_USERNAME=`cat /etc/inverter/mqtt.json | jq '.username' -r`
MQTT_PASSWORD=`cat /etc/inverter/mqtt.json | jq '.password' -r`
MQTT_CLIENTID=`cat /etc/inverter/mqtt.json | jq '.clientid' -r`

registerTopic () {
    mosquitto_pub \
        -h $MQTT_SERVER \
        -p $MQTT_PORT \
        -u "$MQTT_USERNAME" \
        -P "$MQTT_PASSWORD" \
        -i $MQTT_CLIENTID \
        -r \
        -t "$MQTT_TOPIC/sensor/"$MQTT_DEVICENAME/$1/config" \
        -m "{
            \"name\": \"$1\",
            \"unit_of_measurement\": \"$2\",
            \"device\": { 
                \"Name\":\"$MQTT_DEVICENAME\",
                \"manufacturer\":\"Inverex\",
                \"model\":\"AeroxIII\",
                \"identifiers\": [
                    \"$MQTT_CLIENTID\"
                    ],
                \"conections\": [[\"ip\", \"192.168.0.113\"]]    
                },
            \"unique_id\": \""$MQTT_CLIENTID"_$1\",
            \"device_class\": \"$4\",
            \"entity_category\": \"$6\",
            \"state_class\": \"$5\",  
            \"state_topic\": \"$MQTT_TOPIC/sensor/$MQTT_DEVICENAME/$1\",
            \"icon\": \"mdi:$3\"
        }"
}

registerInverterRawCMD () {
    mosquitto_pub \
        -h $MQTT_SERVER \
        -p $MQTT_PORT \
        -u "$MQTT_USERNAME" \
        -P "$MQTT_PASSWORD" \
        -i $MQTT_CLIENTID \
        -t "$MQTT_TOPIC/sensor/$MQTT_DEVICENAME/config" \
        -m "{
            \"name\": \""$MQTT_DEVICENAME"\",
            \"state_topic\": \"$MQTT_TOPIC/sensor/"$MQTT_DEVICENAME\"
        }"
}

registerTopic "Inverter_mode" "" "solar-power" "None" "" "sensor"                                        # 1 = Power_On, 2 = Standby, 3 = Line, 4 = Battery, 5 = Fault, 6 = Power_Saving, 7 = Unknown
registerTopic "AC_grid_voltage" "V" "power-plug" "voltage" "" "diagnostic"
registerTopic "AC_grid_frequency" "Hz" "current-ac" "frequency" "" "diagnostic"
registerTopic "AC_out_voltage" "V" "power-plug" "voltage" "" "diagnostic"
registerTopic "AC_out_frequency" "Hz" "current-ac" "frequency" "" "diagnostic"
registerTopic "PV_in_voltage" "V" "solar-panel-large" "voltage" "" "sensor"
registerTopic "PV_in_current" "A" "solar-panel-large" "current" "" "sensor"
registerTopic "PV_in_watts" "W" "solar-panel-large" "power" "measurement" "sensor"
registerTopic "PV_in_watthour" "Wh" "solar-panel-large" "energy" "measurement" "sensor"
registerTopic "SCC_voltage" "V" "current-dc" "voltage" "" "diagnostic"
registerTopic "Load_pct" "%" "brightness-percent" "power_factor" "" "sensor"
registerTopic "Load_watt" "W" "chart-bell-curve" "power" "measurement" "sensor"
registerTopic "Load_watthour" "Wh" "chart-bell-curve" "energy" "measurement" "sensor"
registerTopic "Load_va" "VA" "chart-bell-curve" "apparent_power" "" "diagnostic"
registerTopic "Bus_voltage" "V" "details" "voltage" "" "diagnostic"
registerTopic "Heatsink_temperature" "C" "thermometer" "temperature" "" "diagnostic"
registerTopic "Battery_capacity" "%" "battery-outline" "battery" "" "sensor"
registerTopic "Battery_voltage" "V" "battery-outline" "voltage" "" "diagnostic"
registerTopic "Battery_charge_current" "A" "current-dc" "current" "" "diagnostic"
registerTopic "Battery_discharge_current" "A" "current-dc" "current" "" "diagnostic"
registerTopic "Load_status_on" "" "power" "None" "" "sensor"
registerTopic "SCC_charge_on" "" "power" "None" "" "sensor"
registerTopic "AC_charge_on" "" "power" "None" "" "sensor"
registerTopic "Battery_recharge_voltage" "V" "current-dc" "voltage" "" "diagnostic"
registerTopic "Battery_under_voltage" "V" "current-dc" "voltage" "" "diagnostic"
registerTopic "Battery_bulk_voltage" "V" "current-dc" "voltage" "" "diagnostic"
registerTopic "Battery_float_voltage" "V" "current-dc" "voltage" "" "sensor"
registerTopic "Max_grid_charge_current" "A" "current-ac" "current" "" "diagnostic"
registerTopic "Max_charge_current" "A" "current-ac" "current" "" "diagnostic"
registerTopic "Out_source_priority" "" "grid" "None" "" "sensor"
registerTopic "Charger_source_priority" "" "solar-power" "None" "" "sensor"
registerTopic "Battery_redischarge_voltage" "V" "battery-negative" "voltage" "" "diagnostic"
registerTopic "warnings" "" "" "None" "" ""

# Add in a separate topic so we can send raw commands from assistant back to the inverter via MQTT (such as changing power modes etc)...

registerInverterRawCMD
