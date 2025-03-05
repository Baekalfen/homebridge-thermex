import paho.mqtt.client as mqtt
from api import ThermexAPI
import asyncio

mosquitto_hostname = "mosquitto"
API = ThermexAPI('192.168.5.4', '1234')
base_topic = "thermex"

last_speed = 2
last_brightness = 100

def on_message(client, userdata, msg):
    global last_brightness, last_speed
    _base_topic, topic = msg.topic.split("/")
    if base_topic != _base_topic:
        print("Unknown base topic:", _base_topic)
        return

    if topic == "set_active":
        state = msg.payload.decode()
        new_state = state == "true"
        # We are guessing a speed here, as the API is designed differently
        asyncio.run(API.update_fan(new_state, last_speed))
        client.publish(base_topic + "/get_active", new_state)
    elif topic == "set_speed":
        value = msg.payload.decode()
        if not value.isnumeric():
            print("Speed value is not numeric", value)
            return
        speed = max(min(int(value)//25, 4), 0)
        last_speed = speed
        asyncio.run(API.update_fan(speed>0, speed))
        client.publish(base_topic + "/get_speed", speed*25)
    elif topic == "set_on":
        state = msg.payload.decode()
        new_state = state == "true"
        # We are guessing a brightness here, as the API is designed differently
        asyncio.run(API.update_light(new_state, last_brightness))
        client.publish(base_topic + "/get_on", new_state)
    elif topic == "set_brightness":
        value = msg.payload.decode()
        if not value.isnumeric():
            print("Brightness value is not numeric", value)
            return
        brightness = max(min(int(value), 100), 0)
        last_brightness = brightness
        asyncio.run(API.update_light(brightness>0, brightness))
        client.publish(base_topic + "/get_brightness", new_state)
    else:
        print("Unknown topic:", topic, msg)


client = mqtt.Client()
client.on_message = on_message
client.connect(mosquitto_hostname, 1883, 60)

client.subscribe(base_topic+"/#")
client.loop_forever()



