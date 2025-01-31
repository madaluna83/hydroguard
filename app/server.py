from flask import Flask, jsonify, request, render_template
from flask_socketio import SocketIO
import psycopg2

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# Database Configuration
DB_CONFIG = {
    "dbname": "water_quality",
    "user": "postgres",
    "password": "12341234",  # 
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

#@app.route("/api/data", methods=["POST"])


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
    # Connect to the database
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()

    # Execute the SQL query to get stats
    cursor.execute("""
        SELECT sensor_id, 
               MIN(ph), MAX(ph), AVG(ph),
               MIN(dissolved_oxygen), MAX(dissolved_oxygen), AVG(dissolved_oxygen),
               MIN(carbon_dioxide_levels), MAX(carbon_dioxide_levels), AVG(carbon_dioxide_levels),
               MIN(turbidity), MAX(turbidity), AVG(turbidity)
        FROM water_data
        GROUP BY sensor_id
    """)
    
    # Fetch all the results
    stats = cursor.fetchall()
    conn.close()

    # Format the data into a list of dictionaries (this is how we'll send it as JSON)
    data = []
    for stat in stats:
        data.append({
            'sensor_id': stat[0],
            'min_ph': stat[1],
            'max_ph': stat[2],
            'avg_ph': stat[3],
            'min_oxygen': stat[4],
            'max_oxygen': stat[5],
            'avg_oxygen': stat[6],
            'min_co2': stat[7],
            'max_co2' : stat[8],
            'avg_co2' : stat[9],
            'min_turbidity': stat[10],
            'max_turbidity': stat[11],
            'avg_turbidity': stat[12]
        })

    # Return the data as JSON
    return jsonify(data)

#trimite datele la cloud pt gateway 
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


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)
