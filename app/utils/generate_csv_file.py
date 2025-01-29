import csv
import psycopg2
import random
import time
from datetime import datetime, timedelta

DB_CONFIG = {
    "dbname": "water_quality",
    "user": "postgres",
    "password": "diana",  
    "host": "localhost",
    "port": "5432"
}

def generate_random_data(num_entries=10000):
    """Generates synthetic water quality data for export."""
    data = []
    base_time = datetime.now() - timedelta(days=num_entries // 1440)  # Spread over time
    
    for _ in range(num_entries):
        sensor_id = random.randint(1, 10)
        timestamp = base_time.strftime('%Y-%m-%d %H:%M:%S')
        ph = round(random.uniform(6.0, 9.0), 2)
        dissolved_oxygen = round(random.uniform(5.0, 10.0), 2)
        carbon_dioxide_levels = round(random.uniform(0.1, 1.0), 2)
        turbidity = round(random.uniform(0.1, 5.0), 2)
        
        data.append((sensor_id, timestamp, ph, dissolved_oxygen, carbon_dioxide_levels, turbidity))
        base_time += timedelta(minutes=1)  # Increment time
    
    return data

def export_to_csv(filename="water_quality_data.csv", num_entries=10000):
    """Exports synthetic water quality data to a CSV file."""
    headers = ["Sensor ID", "Timestamp", "pH", "Dissolved Oxygen", "CO2 Levels", "Turbidity"]
    data = generate_random_data(num_entries)
    
    with open(filename, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(data)
    
    print(f"CSV file '{filename}' generated with {num_entries} entries!")

if __name__ == "__main__":
    export_to_csv()
