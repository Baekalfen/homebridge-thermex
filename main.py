import time
import paho.mqtt.client as mqtt
from api import ThermexAPI

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
        print(API.update_fan(new_state, last_speed))
        client.publish(base_topic + "/get_active", new_state)
    elif topic == "set_speed":
        value = msg.payload.decode()
        if not value.isnumeric():
            print("Speed value is not numeric", value)
            return
        speed = max(min(int(value)//25, 4), 0)
        last_speed = speed
        print("Speed", speed)
        print(API.update_fan(speed>0, speed))
        client.publish(base_topic + "/get_speed", speed*25)
    elif topic == "set_on":
        state = msg.payload.decode()
        new_state = state == "true"
        # We are guessing a brightness here, as the API is designed differently
        print(API.update_light(new_state, last_brightness))
        client.publish(base_topic + "/get_on", new_state)
    elif topic == "set_brightness":
        value = msg.payload.decode()
        if not value.isnumeric():
            print("Brightness value is not numeric", value)
            return
        brightness = max(min(int(value), 100), 0)
        last_brightness = brightness
        print(API.update_light(brightness>0, brightness))
        client.publish(base_topic + "/get_brightness", brightness)
    elif topic in ["get_active", "get_speed", "get_on", "get_brightness"]:
        pass
    else:
        print("Unknown topic:", topic, msg.payload)


client = mqtt.Client()
client.on_message = on_message
client.connect(mosquitto_hostname, 1883, 60)

client.subscribe(base_topic+"/#")
# client.loop_forever()

last_update = 0
delay = 60 * 5
if __name__ == "__main__":
    client.loop_start()
    while True:
        if last_update + delay < time.time():
            API.reconnect() # Try to avoid broken connections
            data = API.fetch_status()
            if data.get('Status') == 200:
                light = data.get('Data',{}).get("Light")
                fan = data.get('Data',{}).get("Fan")
                print("Update:", light, fan)
                client.publish(base_topic + "/get_active", fan.get("fanonoff", 0))
                client.publish(base_topic + "/get_speed", fan.get("fanspeed", 0)*25)
                client.publish(base_topic + "/get_on", light.get("lightonoff", 0))
                client.publish(base_topic + "/get_brightness", light.get("lightbrightness", 0))
                last_update = time.time()
            else:
                time.sleep(30)

        time.sleep(0.25)
    client.loop_stop(force=False)

