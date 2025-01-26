import paho.mqtt.client as mqtt
import time
import random
import json  # Importăm json pentru serializare

MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "sensors/water_quality"

def publish_sensor_data():
    client = mqtt.Client()
    client.connect(MQTT_BROKER, MQTT_PORT)

    while True:
        # Generăm date simulate
        sensor_data = {
            "sensor_id": random.randint(1, 5),
            "timestamp": time.time(),
            "ph": round(random.uniform(6.5, 8.5), 2),
            "dissolved_oxygen": round(random.uniform(5.0, 10.0), 2),
            "carbon_dioxide_levels": round(random.uniform(0.1, 1.0), 2),
            "turbidity": round(random.uniform(0.1, 5.0), 2)
        }

        # Serializăm datele în JSON
        sensor_data_json = json.dumps(sensor_data)

        # Publicăm mesajul pe topicul MQTT
        client.publish(MQTT_TOPIC, sensor_data_json)
        print(f"Trimis: {sensor_data_json}")

        time.sleep(5)

if __name__ == "__main__":
    publish_sensor_data()
