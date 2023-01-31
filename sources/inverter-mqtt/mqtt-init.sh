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
        -t "$MQTT_TOPIC/sensor/$MQTT_DEVICENAME/$1/config" \
        -m "{
            \"name\": \"$1\",
            \"unit_of_measurement\": \"$2\",
            \"state_topic\": \"UPS/sensor/$MQTT_DEVICENAME/$1/state\",
            \"icon\": \"mdi:$3\",
            \"unique_id\": \"$1\",
            \"entity_category\": \"$6\",
            \"device_class\": \"$4\",
            \"device\": {
                \"name\": \"$MQTT_DEVICENAME\",
                \"manufacturer\": \"Inverex\",
                \"model\": \"AeroxIII\",
                \"identifiers\": [ \"$MQTT_CLIENTID\" ],
                \"connections\": [[\"ip\", \"192.168.0.112\"]]
                },
            \"availabilty_topic\": \"UPS/$MQTT_DEVICENAME/$1/LWT\"
        }"
        
        
        mosquitto_pub \
        -h $MQTT_SERVER \
        -p $MQTT_PORT \
        -u "$MQTT_USERNAME" \
        -P "$MQTT_PASSWORD" \
        -r \
        -i $MQTT_CLIENTID \
        -t "UPS/$MQTT_DEVICENAME/$1/LWT" \
        -m online
}

registerInverterRawCMD () {
    mosquitto_pub \
        -h $MQTT_SERVER \
        -p $MQTT_PORT \
        -u "$MQTT_USERNAME" \
        -P "$MQTT_PASSWORD" \
        -i "$MQTT_CLIENTID" \
        -t "$MQTT_TOPIC/button/$MQTT_DEVICENAME/$2/$1/config" \
        -r \
        -m "{
            \"name\": \""$1"_"$2"\",
            \"command_topic\": \"UPS/$MQTT_DEVICENAME/$1\",
            \"unique_id\": \""$1"_"$2"\",
            \"entity_category\": \"$4\",
            \"payload_press\": \"$3\",
            \"device\": {
                \"name\": \""$MQTT_DEVICENAME"_button\",
                \"manufacturer\": \"Inverex\",
                \"model\": \"AeroxIII\",
                \"identifiers\": [ \""$MQTT_CLIENTID"_button\" ],
                \"connections\": [[\"ip\", \"192.168.0.112\"]]
                },
            \"availabilty_topic\": \"UPS/$MQTT_DEVICENAME/$2/$1/LWT\"
        }"
        
           mosquitto_pub \
        -h $MQTT_SERVER \
        -p $MQTT_PORT \
        -u "$MQTT_USERNAME" \
        -P "$MQTT_PASSWORD" \
        -i $MQTT_CLIENTID \
        -r \
        -t "UPS/$MQTT_DEVICENAME/$2/$1/LWT" \
        -m online

}


registerTopic "Inverter_mode" "" "solar-power" "aqi" "" "config"                                        # 1 = Power_On, 2 = Standby, 3 = Line, 4 = Battery, 5 = Fault, 6 = Power_Saving, 7 = Unknown
registerTopic "AC_grid_voltage" "V" "power-plug" "voltage" "" "diagnostic"
registerTopic "AC_grid_frequency" "Hz" "current-ac" "frequency" "" "diagnostic"
registerTopic "AC_out_voltage" "V" "power-plug" "voltage" "" "diagnostic"
registerTopic "AC_out_frequency" "Hz" "current-ac" "frequency" "" "diagnostic"
registerTopic "PV_in_voltage" "V" "solar-panel-large" "voltage" "" "config"
registerTopic "PV_in_current" "A" "solar-panel-large" "current" "" "config"
registerTopic "PV_in_watts" "W" "solar-panel-large" "power" "measurement" "config"
registerTopic "PV_in_watthour" "Wh" "solar-panel-large" "energy" "measurement" "config"
registerTopic "SCC_voltage" "V" "current-dc" "voltage" "" "diagnostic"
registerTopic "Load_pct" "%" "brightness-percent" "power_factor" "" "config"
registerTopic "Load_watt" "W" "chart-bell-curve" "power" "measurement" "config"
registerTopic "Load_watthour" "Wh" "chart-bell-curve" "energy" "measurement" "config"
registerTopic "Load_va" "VA" "chart-bell-curve" "apparent_power" "" "diagnostic"
registerTopic "Bus_voltage" "V" "details" "voltage" "" "diagnostic"
registerTopic "Heatsink_temperature" "C" "thermometer" "temperature" "" "diagnostic"
registerTopic "Battery_capacity" "%" "battery-outline" "battery" "" "config"
registerTopic "Battery_voltage" "V" "battery-outline" "voltage" "" "diagnostic"
registerTopic "Battery_charge_current" "A" "current-dc" "current" "" "diagnostic"
registerTopic "Battery_discharge_current" "A" "current-dc" "current" "" "diagnostic"
registerTopic "Load_status_on" "" "power" "aqi" "" "config"
registerTopic "SCC_charge_on" "" "power" "aqi" "" "config"
registerTopic "AC_charge_on" "" "power" "aqi" "" "config"
registerTopic "Battery_recharge_voltage" "V" "current-dc" "voltage" "" "diagnostic"
registerTopic "Battery_under_voltage" "V" "current-dc" "voltage" "" "diagnostic"
registerTopic "Battery_bulk_voltage" "V" "current-dc" "voltage" "" "diagnostic"
registerTopic "Battery_float_voltage" "V" "current-dc" "voltage" "" "config"
registerTopic "Max_grid_charge_current" "A" "current-ac" "current" "" "diagnostic"
registerTopic "Max_charge_current" "A" "current-ac" "current" "" "diagnostic"
registerTopic "Out_source_priority" "" "grid" "aqi" "" "config"
registerTopic "Charger_source_priority" "" "solar-power" "aqi" "" "config"
registerTopic "Battery_redischarge_voltage" "V" "battery-negative" "voltage" "" "diagnostic"
registerTopic "Warnings" "" "" "aqi" "" "diagnostic"



# Add in a separate topic so we can send raw commands from assistant back to the inverter via MQTT (such as changing power modes etc)...
registerInverterRawCMD "Solar_first" "Output" "POP01" "config"
registerInverterRawCMD "Utility_first" "Output" "POP00" "config"
registerInverterRawCMD "SBU" "Output" "POP02" "config"
registerInverterRawCMD "Utility_first" "Charge" "PCP00" "config"
registerInverterRawCMD "Solar_&_utility" "Charge" "PCP02" "config"
registerInverterRawCMD "Solar_only" "Charge" "PCP03" "config"
registerInverterRawCMD "Solar_first" "Charge" "PCP01" "config"
