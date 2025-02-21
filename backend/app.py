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

# Load the protected zones from KML files (instead of GeoJSON)
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
            user_gdf["inside_protected_zone"] = user_gdf.intersects(protected_zones.unary_union)
            
            # Save report
            report_path = os.path.join(app.config['UPLOAD_FOLDER'], "report.csv")
            user_gdf[["inside_protected_zone"]].to_csv(report_path, index=False)
            
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
    # Get the 'codigo_cat' parameter from the query string
    codigo_cat = request.args.get('codigo_cat')
    if not codigo_cat:
        return jsonify({"error": "Missing codigo_cat parameter"}), 400

    try:
        conn = get_db_connection()
        # Use DictCursor so that results come back as a dictionary
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        
        # Define the query; ST_AsText converts the geometry to WKT
        query = """
            SELECT fid, codigo_cat, uso_de_edi, lindero_no, lindero_su, 
                   lindero_es, lindero_oe, longitud_n, longitud_s, 
                   longitud_e, longitud_o, area_escri, calle, shape_area, 
                   shape_length, ST_AsText(geom) AS geom, fecha_registro
            FROM predios
            WHERE codigo_cat = %s
            LIMIT 1;
        """
        cursor.execute(query, (codigo_cat,))
        record = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        if record is None:
            return jsonify({"error": "No record found for the given codigo_cat"}), 404

        # Convert record (a DictRow) to a plain dictionary and return as JSON
        return jsonify(dict(record))
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)