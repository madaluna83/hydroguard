import psycopg2
import csv

def import_csvfile(csv_file):
    conn = psycopg2.connect(
        dbname = "water_quality", 
        user = "postgres", 
        password = "12341234", 
        host = "localhost",
        port = "5432"
    )
    cursor = conn.cursor()

    with open(csv_file, mode = 'r') as file: 
        reader = csv.DictReader(file)
        for row in reader: 
            cursor.execute(
                """
                INSERT INTO water_data (entry_id, sensor_id, timestamp, ph, dissolved_oxygen, carbon_dioxide_levels, turbidity)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                int(row["entry_id"]),
                int(row["sensor_id"]),
                row["timestamp"],
                float(row["ph"]),
                float(row["dissolved_oxygen"]),
                float(row["carbon_dioxide_levels"]),
                float(row["turbidity"])
            ))

    conn.commit()
    conn.close()
    print("Data has successfully imported from the file")

if __name__ == "__main__":
    import_csvfile("water_quality_data.csv")