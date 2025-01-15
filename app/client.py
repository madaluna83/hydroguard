import requests

BASE_URL = "http://127.0.0.1:5000"

response = requests.get(f"{BASE_URL}/data")
if response.status_code == 200:
    print("All data: ", response.json())


sensor_id = 1
response = requests.get(f"{BASE_URL}/data/{sensor_id}")
if response.status_code == 200:
    print(f"Data for sensor {sensor_id}:", response.json())

response = requests.get(f"{BASE_URL}/data/stats", params = {"sensor_id": sensor_id})
if response.status_code == 200:
    stats = response.json()
    print(f"Statistics for Sensor {sensor_id}:")
    print("pH:", stats["ph"])
    print("Dissolved Oxygen:", stats["dissolved_oxygen"])
    print("Carbon Dioxide Levels:", stats["carbon_dioxide_levels"])
    print("Turbidity:", stats["turbidity"])

response = requests.get(f"{BASE_URL}/data/alerts")
if response.status_code == 200:
    alerts = response.json()
    if alerts:
        print("Alerts:")
        for alert in alerts:
            print(alert)
    else:
        print("No alerts found!")


new_entry = {
    "entry_id": 101,
    "sensor_id": 1,
    "timestamp": "2025-01-11 10:00:00",
    "ph": 7.2,
    "dissolved_oxygen": 8.1,
    "carbon_dioxide_levels": 3.5,
    "turbidity": 1.0
}

response = requests.post(f"{BASE_URL}/data", json=new_entry)
if response.status_code == 201:
    print("New entry added successfully!")

