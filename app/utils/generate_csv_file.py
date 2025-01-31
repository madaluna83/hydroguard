import csv
import psycopg2
import random
import time
from datetime import datetime, timedelta

DB_CONFIG = {
    "dbname": "water_quality",
    "user": "postgres",
    "password": "12341234",  
    "host": "localhost",
    "port": "5432"
}

def generate_random_data(num_entries=10000, anomaly_percentage=5):
    """Generates synthetic water quality data with anomalies."""
    data = []
    base_time = datetime.now() - timedelta(days=num_entries // 1440)  # Spread over time
    anomaly_count = int((anomaly_percentage / 100) * num_entries)  # Număr de anomalii de generat

    for _ in range(num_entries):
        sensor_id = random.randint(1, 10)
        timestamp = base_time.strftime('%Y-%m-%d %H:%M:%S')
        
        # Generăm valori normale
        ph = round(random.uniform(6.0, 9.0), 2)
        dissolved_oxygen = round(random.uniform(5.0, 10.0), 2)
        carbon_dioxide_levels = round(random.uniform(0.1, 1.0), 2)
        turbidity = round(random.uniform(0.1, 5.0), 2)

        # Adăugăm anomalii în mod aleatoriu
        if random.random() < (anomaly_percentage / 100):
            anomaly_type = random.choice(["extreme", "null", "future", "duplicate"])

            if anomaly_type == "extreme":
                ph = round(random.choice([random.uniform(2.0, 4.0), random.uniform(10.0, 14.0)]), 2)  # pH foarte acid sau alcalin
                dissolved_oxygen = round(random.choice([random.uniform(0.1, 2.0), random.uniform(15.0, 20.0)]), 2)  # Oxigen anormal
                carbon_dioxide_levels = round(random.uniform(5.0, 10.0), 2)  # CO2 foarte mare
                turbidity = round(random.uniform(10.0, 50.0), 2)  # Turbiditate extremă

            elif anomaly_type == "null":
                if random.random() < 0.5:
                    ph = None  # Valoare lipsă
                if random.random() < 0.5:
                    dissolved_oxygen = None
                if random.random() < 0.5:
                    carbon_dioxide_levels = None
                if random.random() < 0.5:
                    turbidity = None

            elif anomaly_type == "future":
                timestamp = (base_time + timedelta(days=random.randint(1, 365))).strftime('%Y-%m-%d %H:%M:%S')  # Dată în viitor

            elif anomaly_type == "duplicate":
                if data:
                    data.append(random.choice(data))  # Adăugăm un rând duplicat
                
        data.append((sensor_id, timestamp, ph, dissolved_oxygen, carbon_dioxide_levels, turbidity))
        base_time += timedelta(minutes=1)  # Incrementare timp
    
    return data

def export_to_csv(filename="water_quality_data.csv", num_entries=10000, anomaly_percentage=5):
    """Exports synthetic water quality data with anomalies to a CSV file."""
    headers = ["Sensor ID", "Timestamp", "pH", "Dissolved Oxygen", "CO2 Levels", "Turbidity"]
    data = generate_random_data(num_entries, anomaly_percentage)
    
    with open(filename, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(data)
    
    print(f"CSV file '{filename}' generated with {num_entries} entries, including {anomaly_percentage}% anomalies!")

if __name__ == "__main__":
    export_to_csv()
