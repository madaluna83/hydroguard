from flask import Flask, request, jsonify, render_template
import psycopg2

app = Flask(__name__)

def get_db_connection():
    return psycopg2.connect(
        dbname = "water_quality",
        user = "postgres", 
        password = "12341234", 
        host = "localhost",
        port = "5432"
    )

@app.route("/")
def home():
    return render_template("index.html")

@app.route('/data', methods=['GET'])
def get_all_data():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM water_data")
    rows = cursor.fetchall()
    conn.close()
    data = [
        {
            "id": row[0],
            "entry_id": row[1],
            "sensor_id": row[2],
            "timestamp": row[3],
            "ph": row[4],
            "dissolved_oxygen": row[5],
            "carbon_dioxide_levels": row[6],
            "turbidity": row[7]
        }
        for row in rows 
    ]
    return jsonify(data)

@app.route('/data/<int:sensor_id>', methods=['GET'])
def get_data_by_sensor(sensor_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM water_data WHERE sensor_id = %s", (sensor_id))
    rows = cursor.fetchall()
    conn.close()

    data = [
        {
            "id": row[0],
            "entry_id": row[1],
            "sensor_id": row[2],
            "timestamp": row[3],
            "ph": row[4],
            "dissolved_oxygen": row[5],
            "carbon_dioxide_levels": row[6],
            "turbidity": row[7]
        }
        for row in rows
    ]

    return jsonify(data)

@app.route('/data', methods=['POST'])
def add_data():
    new_data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
                    INSERT INTO water_data (entry_id, sensor_id, timestamp, ph, dissloved_oxygen, carbon_dioxide_levels, turbidity)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                   """, (
                       new_data["entry_id"],
                       new_data["sensor_id"],
                       new_data["timestamp"],
                       new_data["ph"],
                       new_data["dissolved_oxygen"],
                       new_data["carbon_dioxide_levels"],
                       new_data["turbidity"]
                   )
                   )
    conn.commit()
    conn.close()
    return jsonify({"message": "Data added successfully"}), 201

@app.route('/data/stats', methods = ['GET'])
def get_statistics():
    sensor_id = request.args.get('sensor_id', None)
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if sensor_id:
        cursor.execute("""
                SELECT
                       AVG(ph), MIN(ph), MAX(ph),
                       AVG(dissolved_oxygen), MIN(dissolved_oxygen), MAX(dissolved_oxygen),
                       AVG(carbon_dioxide_levels), MIN(carbon_dioxide_levels), MAX(carbon_dioxide_levels),
                       AVG(turbidity), MIN(turbidity), MAX(turbidity)
                       from water_data
                       WHERE sensor_id = %s
                       """, (sensor_id))
        
    else: 
        cursor.execute("""
                SELECT
                       AVG(ph), MIN(ph), MAX(ph),
                       AVG(dissolved_oxygen), MIN(dissolved_oxygen), MAX(dissolved_oxygen),
                       AVG(carbon_dioxide_levels), MIN(carbon_dioxide_levels), MAX(carbon_dioxide_levels),
                       AVG(turbidity), MIN(turbidity), MAX(turbidity)
                       from water_data
            """
        )

    stats = cursor.fetchone()
    conn.close()

    return jsonify({
        "ph" : {"avg": stats[0], "min": stats[1], "max": stats[2]},
        "dissolved_oxygen" : {"avg": stats[3], "min": stats[4], "max": stats[5]}, 
        "carbon_dioxide_levels" : {"avg": stats[6], "min": stats[7], "max": stats[8]}, 
        "turbidity" : {"avg": stats[9], "min": stats[10], "max": stats[11]}
    })

@app.route('/data/alerts', methods=['GET'])
def get_alerts():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
            SELECT entry_id, sensor_id, timestamp, ph, dissolved_oxygen, carbon_dioxide_levels, turbidity
            FROM water_data
            WHERE ph < 6.5 OR ph > 8.5 
            OR dissolved_oxygen < 4.0
            OR turbidity > 5.0 
        """
    )

    alerts = cursor.fetchall()
    conn.close()

    data = [
        {
            "entry_id": row[0], 
            "sensor_id": row[1],
            "timestamp": row[2], 
            "ph": row[3],
            "dissolved_oxygen": row[4], 
            "carbon_dioxide_levels": row[5], 
            "turbidity": row[6]
        }
        for row in alerts
    ]

    return jsonify(data)



if __name__ == "__main__":
    app.run(debug=True)