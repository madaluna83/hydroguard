import csv
import psycopg2

DB_CONFIG = {
    "dbname": "water_quality",
    "user": "postgres",
    "password": "12341234",
    "host": "localhost",
    "port": "5432"
}

def import_from_csv(filename="water_quality_data.csv"):
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()

    with open(filename, mode="r") as file:
        reader = csv.reader(file)
        next(reader)  # Skip header row

        for row in reader:
            cursor.execute("""
                INSERT INTO water_data (sensor_id, timestamp, ph, dissolved_oxygen, carbon_dioxide_levels, turbidity)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, row)  # Ensure the order matches the updated DB schema

    conn.commit()
    conn.close()
    print(f"CSV file '{filename}' imported successfully!")

if __name__ == "__main__":
    import_from_csv()
