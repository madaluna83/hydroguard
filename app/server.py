from flask import Flask, jsonify, request, render_template
from flask_socketio import SocketIO
import psycopg2

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# Database Configuration
DB_CONFIG = {
    "dbname": "water_quality",
    "user": "postgres",
    "password": "diana",  # 
    "host": "localhost",
    "port": "5432"
}

def save_to_db(data):
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO water_data (sensor_id, timestamp, ph, dissolved_oxygen, carbon_dioxide_levels, turbidity)
        VALUES (%s, TO_TIMESTAMP(%s), %s, %s, %s, %s)
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

@app.route("/")
def index():
    return render_template("dashboard.html")


def check_water_quality(data):
    """Checks if water quality parameters are within safe limits."""
    warnings = []

    if data["ph"] < 6.5 or data["ph"] > 8.5:
        warnings.append("pH level out of range!")
    if data["dissolved_oxygen"] < 5.0 or data["dissolved_oxygen"] > 10.0:
        warnings.append("Dissolved Oxygen level out of range!")
    if data["carbon_dioxide_levels"] > 1.0:
        warnings.append("CO₂ levels too high!")
    if data["turbidity"] > 3.0:
        warnings.append("Turbidity too high!")

    return warnings

@app.route("/api/data", methods=["POST"])
def receive_data():
    sensor_data = request.json
    print(f"Received Data: {sensor_data}")

    # Save to Database
    save_to_db(sensor_data)

    # Check for unsafe values
    warnings = check_water_quality(sensor_data)
    if warnings:
        alert_message = {
            "sensor_id": sensor_data["sensor_id"],
            "timestamp": sensor_data["timestamp"],
            "warnings": warnings
        }
        socketio.emit("alert", alert_message)
        print("Alert Sent:", alert_message)

    # Emit new data event
    socketio.emit("new_data", sensor_data)

    return jsonify({"message": "Data saved"}), 200



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

@app.route("/api/stats", methods=["GET"])
def stats():
    """Fetches data for graph visualization"""
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()

    # Fetch time series data for each attribute
    cursor.execute("""
        SELECT timestamp, ph, dissolved_oxygen, carbon_dioxide_levels, turbidity
        FROM water_data ORDER BY timestamp
    """)
    data = cursor.fetchall()
    conn.close()

    # Convert to JSON
    timestamps = [row[0].strftime('%Y-%m-%d %H:%M:%S') for row in data]
    ph_values = [row[1] for row in data]
    oxygen_values = [row[2] for row in data]
    co2_values = [row[3] for row in data]
    turbidity_values = [row[4] for row in data]

    return jsonify({
        "timestamps": timestamps,
        "ph_values": ph_values,
        "oxygen_values": oxygen_values,
        "co2_values": co2_values,
        "turbidity_values": turbidity_values
    })



if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)
