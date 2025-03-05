import json
import websocket

class ThermexAPI:
    def __init__(self, host, code):
        self._host = host
        self._password = code
        ws_url = f'ws://{self._host}:9999/api'
        self.ws = websocket.create_connection(ws_url)
        self.authenticate()

    def __del__(self):
        self.ws.close()

    def authenticate(self):
        return self.transceive({
            "Request": "Authenticate",
            "Data": {"Code": self._password}
        }, allow_codes=(200,))

    def transceive(self, message, allow_codes=(200, 400)):
        self.ws.send(json.dumps(message))

        while response := json.loads(self.ws.recv()) and response.get("Notify"):
            print("Discarding notify:", response)

        if response.get("Status") not in allow_codes:
            raise Exception("Unexpected response from Thermex API", message, response)

        return response

    def fetch_status(self):
        return self.transceive({"Request": "STATUS"})

    def update_fan(self, fanonoff, fanspeed):
        return self.transceive({
            "Request": "Update",
            "Data": {
                "fan": {
                    "fanonoff": fanonoff,
                    "fanspeed": fanspeed
                }
            }
        })

    def update_light(self, lightonoff, brightness):
        return self.transceive({
            "Request": "Update",
            "Data": {
                "light": {
                    "lightonoff": lightonoff,
                    "lightbrightness": brightness
                }
            }
        })
