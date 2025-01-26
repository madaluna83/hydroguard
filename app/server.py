from flask import Flask, request, jsonify, render_template

import psycopg2

app = Flask(__name__)

# Configurare conexiune la baza de date
DB_CONFIG = {
    "dbname": "water_quality",
    "user": "postgres",
    "password": "diana",
    "host": "localhost",
    "port": "5432"
}

def save_to_db(data):
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO water_data (entry_id, sensor_id, timestamp, ph, dissolved_oxygen, carbon_dioxide_levels, turbidity)
        VALUES (DEFAULT, %s, TO_TIMESTAMP(%s), %s, %s, %s, %s)
    """, (
        data["sensor_id"],
        data["timestamp"],
        data["ph"],
        data["dissolved_oxygen"],
        data["carbon_dioxide_levels"],
        data["turbidity"]
    ))
    conn.commit()
    conn.close()

@app.route("/api/data", methods=["POST"])
def receive_data():
    sensor_data = request.json
    print(f"Date primite de la gateway: {sensor_data}")
    save_to_db(sensor_data)
    return jsonify({"message": "Date salvate cu succes"}), 200

@app.route("/")
def index():
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()

    # Calculăm statistici
    cursor.execute("""
        SELECT sensor_id, AVG(ph) AS avg_ph, AVG(dissolved_oxygen) AS avg_oxygen, AVG(turbidity) AS avg_turbidity
        FROM water_data
        GROUP BY sensor_id
    """)
    stats = cursor.fetchall()
    conn.close()

    # Generăm conținut HTML
    html_content = "<h1>Statistici Calitatea Apei</h1>"
    for stat in stats:
        html_content += f"""
            <p>
                Senzor {stat[0]}:<br>
                - pH mediu: {stat[1]:.2f}<br>
                - Oxigen dizolvat mediu: {stat[2]:.2f}<br>
                - Turbiditate medie: {stat[3]:.2f}<br>
            </p>
        """

    return html_content

@app.route("/stats", methods=["GET"])
def stats():
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()

    # Obține statistici pe fiecare senzor
    cursor.execute("""
        SELECT sensor_id, 
               MIN(ph) AS min_ph, MAX(ph) AS max_ph, AVG(ph) AS avg_ph,
               MIN(dissolved_oxygen) AS min_oxygen, MAX(dissolved_oxygen) AS max_oxygen, AVG(dissolved_oxygen) AS avg_oxygen,
               MIN(turbidity) AS min_turbidity, MAX(turbidity) AS max_turbidity, AVG(turbidity) AS avg_turbidity
        FROM water_data
        GROUP BY sensor_id
    """)
    stats = cursor.fetchall()
    conn.close()

    html_content = "<h1>Statistici Calitatea Apei</h1>"
    for stat in stats:
        html_content += f"""
            <h2>Senzor {stat[0]}</h2>
            <p>pH: Min={stat[1]:.2f}, Max={stat[2]:.2f}, Medie={stat[3]:.2f}</p>
            <p>Oxigen Dizolvat: Min={stat[4]:.2f}, Max={stat[5]:.2f}, Medie={stat[6]:.2f}</p>
            <p>Turbiditate: Min={stat[7]:.2f}, Max={stat[8]:.2f}, Medie={stat[9]:.2f}</p>
        """

    return html_content


@app.route("/stats/chart", methods=["GET"])
def stats_chart():
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()

    # Obține datele pentru grafic
    cursor.execute("SELECT timestamp, ph FROM water_data ORDER BY timestamp")
    data = cursor.fetchall()
    conn.close()

    # Extrage timestamp-urile și valorile pH-ului
    timestamps = [row[0].strftime('%Y-%m-%d %H:%M:%S') for row in data]
    ph_values = [row[1] for row in data]

    # Trimite datele către template
    return render_template("stats.html", timestamps=timestamps, ph_values=ph_values)



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

