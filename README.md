This is a fork of https://github.com/hsk-dk/home-assistant-thermex to add support in Homebridge. Big thanks to the original author!


Quick guide:
A Thermex extractor hood supporting voicelink is needed (https://thermex.eu/advice-and-guidance/all-options/voicelink)

Setup API
1) Check software version, minimum version is 1.30/1.10
![Screenshot_app_0](https://github.com/user-attachments/assets/d5a0f1ad-e006-4d50-9a16-9d79af83f132)
2)Enable API and set password in native phone app from Thermex
![Screenshot_app_1](https://github.com/user-attachments/assets/c80412a1-1f13-4f23-b347-01a2cd9c2202)
![Screenshot_app_2](https://github.com/user-attachments/assets/2bc877bb-490f-4272-afdf-2f059b35dd1c)

Setup Homebridge

0) Setup an MQTT server like [mosquitto](https://hub.docker.com/_/eclipse-mosquitto)
1) Install the plugin `homebridge-mqttthing` in Homebridge
2) Create two devices of any type in mqttthing. We'll change it in a second.
3) Open the JSON config for mqttthing and paste this in the first device:
```json
{
    "type": "fanv2",
    "name": "Thermex Emhætte",
    "url": "mqtt://mosquitto:1883",
    "accessory": "mqttthing",
    "logMqtt": true,
    "topics": {
        "setActive": "thermex/set_active",
        "getActive": "thermex/get_active",
        "setRotationSpeed" : "thermex/set_speed",
        "getRotationSpeed" : "thermex/get_speed"
    }
}
```
4) Paste this in the second device:
```json
{
    "type": "lightbulb-Dimmable",
    "name": "Thermex Lys",
    "url": "mqtt://mosquitto:1883",
    "accessory": "mqttthing",
    "logMqtt": true,
    "topics": {
        "getOn": "thermex/get_on",
        "setOn": "thermex/set_on",
        "getBrightness": "thermex/get_brightness",
        "setBrightness": "thermex/set_brightness"
    }
}
```
5) Replace the IP and code (1234) for the Thermex hood and `mosquitto_hostname` in `main.py` to your setup
6) (Optional) change the `base_topic` in `main.py` and in Homebridge if needed