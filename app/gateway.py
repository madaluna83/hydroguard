import paho.mqtt.client as mqtt
import requests
import json

# Configurare MQTT
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "sensors/water_quality"

# URL-ul serverului web
CLOUD_SERVER_URL = "http://localhost:5000/api/data"

def on_message(client, userdata, message):
    
    sensor_data = json.loads(message.payload.decode())
    print(f"Primit de la senzor: {sensor_data}")

    # Trimitem datele la serverul web
    response = requests.post(CLOUD_SERVER_URL, json=sensor_data)
    if response.status_code == 200:
        print("Date trimise cu succes la serverul web.")
    else:
        print(f"Eroare la trimiterea datelor: {response.status_code}")

def main():
    client = mqtt.Client()
    client.connect(MQTT_BROKER, MQTT_PORT)
    client.subscribe(MQTT_TOPIC)
    client.on_message = on_message

    print("Gateway-ul este activ...")
    client.loop_forever()

if __name__ == "__main__":
    main()
