#!/bin/bash
export TERM=xterm

# stty -F /dev/ttyUSB0 2400 raw

# Init the mqtt server for the first time, then every 5 minutes
# This will re-create the auto-created topics in the MQTT server if HA is restarted...

nohup python3 /opt/inverter-mqtt/mqtt-init.py &
nohup python3 /opt/inverter-mqtt/mqtt-init2.py &
nohup python3 /opt/inverter-mqtt/pub.py &
nohup python3 /opt/inverter-mqtt/sub.py 
# Run the MQTT Subscriber process in the background (so that way we can change the configuration on the inverter from home assistant)
#/opt/inverter-mqtt/mqtt-subscriber.sh &

# execute exactly every 30 seconds...
#watch -n 5 /opt/inverter-mqtt/mqtt-push.sh > /dev/null 2>&1
