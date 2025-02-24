### app.py

import os
import pandas as pd
import geopandas as gpd
import psycopg2
import psycopg2.extras

from shapely.geometry import shape
from werkzeug.utils import secure_filename
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Folder to store uploaded files
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Load the protected zones from KML files
PROTECTED_ZONES_FOLDER = "protected_zones/kmls"
protected_zones = gpd.GeoDataFrame()

# Read all KML files and combine them into one GeoDataFrame
for file in os.listdir(PROTECTED_ZONES_FOLDER):
    if file.endswith(".kml"):
        kml_path = os.path.join(PROTECTED_ZONES_FOLDER, file)
        try:
            gdf = gpd.read_file(kml_path, driver="KML")
            protected_zones = pd.concat([protected_zones, gdf], ignore_index=True)
        except Exception as e:
            print(f"Error loading {file}: {e}")

# Allowed file extensions
ALLOWED_EXTENSIONS = {"geojson", "kml", "kmz", "shp", "shx", "dbf"}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        try:
            # Read the uploaded file as a GeoDataFrame
            user_gdf = gpd.read_file(filepath, driver="KML" if filename.endswith(".kml") else None)
            
            # Check if any polygon intersects with protected zones
            user_gdf["col_xxx_protected"] = user_gdf.intersects(protected_zones.unary_union)
            
            # Save report
            report_path = os.path.join(app.config['UPLOAD_FOLDER'], "report.csv")
            user_gdf[["col_xxx_protected"]].to_csv(report_path, index=False)
            
            return send_file(report_path, as_attachment=True)
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    return jsonify({"error": "Invalid file type"}), 400

# Function to get a database connection
def get_db_connection():
    return psycopg2.connect(
        host="127.0.0.1",
        database="prediosql",
        user="jpaul",
        password="1 de3fr41."  # Use your plain password here
    )

@app.route("/predio", methods=["GET"])
def get_predio():
    # Get the hashed version of 'codigo_cat' from the query string
    col_7a9f2b3c_value = request.args.get('col_7a9f2b3c')  # Was 'codigo_cat'
    if not col_7a9f2b3c_value:
        return jsonify({"error": "Missing col_7a9f2b3c parameter"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        
        # Query using anonymized column names
        query = """
            SELECT col_d41d8cd9, col_f72e3a4b, col_7a9f2b3c, col_1d3e4a9f, col_a2b3c4d5, col_b4c3d2e1, 
                   col_d5e4c3b2, col_c1d2e3f4, col_8d9e7c6b, col_9c8d7e6f, 
                   col_6e7d8c9b, col_7d6c8e9f, col_f1e2d3c4, col_a4b3c2d1, col_c3d4e5f6, 
                   col_d5e4c3b2, ST_AsText(col_f7e6d5c4) AS col_f7e6d5c4, col_e9f8d7c6
            FROM predios
            WHERE col_7a9f2b3c = %s
            LIMIT 1;
        """
        cursor.execute(query, (col_7a9f2b3c_value,))
        record = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        if record is None:
            return jsonify({"error": "No record found for the given col_7a9f2b3c"}), 404

        return jsonify(dict(record))
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)