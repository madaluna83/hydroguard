import csv
import random
from datetime import datetime, timedelta

# Funcție pentru generarea unui fișier CSV
def generate_water_quality_csv(file_name, num_entries=10000):
    # Parametrii de configurare
    sensor_ids = [1, 2, 3]  # ID-urile celor trei senzori pentru colectarea datelor 
    start_time = datetime.now() - timedelta(days=1)  

    # Deschidem fișierul CSV pentru scriere
    with open(file_name, mode='w', newline='') as file:
        writer = csv.writer(file)

        # Scrierea antetului
        writer.writerow([
            "entry_id", "sensor_id", "timestamp", "ph", "dissolved_oxygen", 
            "carbon_dioxide_levels", "turbidity"
        ])

        # Generarea datelor simulate
        for entry_id in range(1, num_entries + 1 ): #pt fiecre id de intrare generam datele : 
            
            sensor_id = random.choice(sensor_ids)  # Alegem un senzor aleator
            timestamp = start_time + timedelta(seconds=random.randint(0, 86400))  # Timp aleator în ultimele 24h
            ph = round(random.uniform(6.5, 8.5), 2)  # pH în intervalul 6.5 - 8.5, valori tipice pentru apa 
            dissolved_oxygen = round(random.uniform(5.0, 12.0), 2)  # Oxigen dizolvat (mg/L) intre 5 si 12 mg/L 
            carbon_dioxide = round(random.uniform(0.5, 3.0), 2)  # CO2 (mg/L) intre 0.5 si 3 mg/L
            turbidity = round(random.uniform(0.1, 5.0), 2)  # Turbiditate (NTU) intre 0.1 si 5, indica claritatea apei

            # Scriem rândul în fișier
            writer.writerow([
                entry_id, sensor_id, timestamp.strftime("%Y-%m-%d %H:%M:%S"), 
                ph, dissolved_oxygen, carbon_dioxide, turbidity
            ])

    print(f"CSV file '{file_name}' generated successfully!")

# Apelăm funcția pentru a genera fișierul
generate_water_quality_csv("water_quality_data.csv", num_entries=10000)
