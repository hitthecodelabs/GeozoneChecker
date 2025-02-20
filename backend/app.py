### app.py

from flask import Flask, request, jsonify, send_file
import geopandas as gpd
from shapely.geometry import shape
import os
from werkzeug.utils import secure_filename
import pandas as pd

app = Flask(__name__)

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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)