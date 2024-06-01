import paho.mqtt.client as mqtt
import json
import subprocess

# Load configuration
with open('/etc/inverter/mqtt.json') as f:
    config = json.load(f)

MQTT_SERVER = config['server']
MQTT_PORT = config['port']
# MQTT_TOPIC = config['topic']
# MQTT_DEVICENAME = config['devicename']
MQTT_USERNAME = config['username']
MQTT_PASSWORD = config['password']
MQTT_CLIENTID = "UPS-SUB"
MQTT_RESPONSE_TOPIC = "UPS/response"

def on_message(client, userdata, msg):
    rawcmd = msg.payload.decode("utf-8")
    print(f"Incoming request: [{rawcmd}]")
    
    try:
        # Run the command and capture the output
        result = subprocess.run(
            ["/opt/inverter-cli/bin/inverter_poller", "-r", rawcmd],
            capture_output=True,
            text=True,
            check=True
        )
        response = result.stdout.strip()
        print(f"Command output: {response}")
        
        # Publish the response to the MQTT topic
        client.publish(MQTT_RESPONSE_TOPIC, response, qos=1)
    except subprocess.CalledProcessError as e:
        error_msg = f"Command failed with error: {e.stderr.strip()}"
        print(error_msg)
        client.publish(MQTT_RESPONSE_TOPIC, error_msg, qos=1)

client = mqtt.Client(MQTT_CLIENTID)
client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
client.on_message = on_message
client.connect(MQTT_SERVER, int(MQTT_PORT), 600)
client.subscribe("UPS/rwcmd", qos=1)

client.loop_forever()
