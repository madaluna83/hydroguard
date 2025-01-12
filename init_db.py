import psycopg2

def init_db():
    conn = psycopg2.connect(
        dbname = "water_quality", 
        user = "postgres", 
        password = "12341234", 
        host = "localhost",
        port = "5432"
    )
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS water_data (
            id SERIAL PRIMARY KEY,
            entry_id INTEGER NOT NULL,
            sensor_id INTEGER NOT NULL,
            timestamp TIMESTAMP NOT NULL,
            ph REAL NOT NULL,
            dissolved_oxygen REAL NOT NULL,
            carbon_dioxide_levels REAL NOT NULL,
            turbidity REAL NOT NULL
        );
    """)

    conn.commit()
    conn.close()
    print("Database initialized successfully!")

if __name__ == "__main__":
    init_db()