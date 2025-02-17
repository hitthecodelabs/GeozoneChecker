# 🌍 Geozone Checker

**Geozone Checker** is a web-based tool that allows users to upload GIS files (**KML, GeoJSON, Shapefiles**) and analyze whether they intersect with **protected environmental zones**. The project is built using **Flask** (backend) and **Vue.js** (frontend) with **Leaflet.js** for interactive mapping.

## 🚀 Features

- 📍 **Interactive GIS Map** with multiple tile layers (OpenStreetMap, Google Satellite, Esri, etc.).
- 🔄 **Upload GIS files** (KML, GeoJSON, Shapefile) for analysis.
- 🛡️ **Protected Environmental Zones** are stored securely on the backend.
- 📊 **Generates Reports** to inform users about intersections with protected areas.
- ⚡ **Fast & Efficient** using `geopandas` and `shapely` for spatial analysis.

---

## 🛠️ Tech Stack

### **Backend (Flask)**
- Flask (`app.py`)
- `geopandas`, `shapely` → Spatial analysis
- `flask-cors` → CORS handling
- `fiona` → GIS file processing

### **Frontend (Vue.js)**
- `Vue 3`
- `Leaflet.js` → GIS visualization
- `axios` → API communication

---

## 📂 Project Structure

```
/GeozoneChecker
├── backend              # Flask API
│   ├── app.py           # Main Flask app
│   ├── uploads/         # Stores user-uploaded GIS files
│   ├── protected_zones/ # Private KML/GeoJSON files
│   ├── requirements.txt # Dependencies
│   ├── scripts/         # Utility scripts
│   └── notebooks/       # Jupyter Notebooks (if used)
├── frontend             # Vue.js UI
│   ├── src/
│   │   ├── components/
│   │   ├── App.vue
│   │   ├── main.js
│   ├── public/
│   ├── package.json
│   ├── vue.config.js
│   └── .gitignore
├── README.md
└── .gitignore
```

---

## 🔧 Setup & Installation

### **1️⃣ Clone the Repository**
```bash
git clone https://github.com/hitthecodelabs/GeozoneChecker.git
cd GeozoneChecker
```

### **2️⃣ Backend Setup (Flask)**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # (On Windows, use `venv\Scripts\activate`)
pip install -r requirements.txt
python app.py
```
Flask will run at `http://127.0.0.1:5000`.

### **3️⃣ Frontend Setup (Vue.js)**
```bash
cd frontend
npm install
npm run serve
```
Vue will run at `http://localhost:8080`.

---

## 📊 How It Works
1. **Select a tile layer** (e.g., OpenStreetMap, Google Satellite).
2. **Upload a GIS file** (`.kml`, `.geojson`, `.shp`).
3. **Flask backend analyzes intersections** with protected areas.
4. **A report is generated**, informing users about overlaps.

---

## 📌 TODO & Future Improvements
- [ ] ✅ Overlay protected zones on the interactive map.
- [ ] 📜 Generate PDF reports instead of CSV.
- [ ] 🔒 User authentication for secure access.
- [ ] 📊 Dashboard for visual analytics.

---

## 🤝 Contributing
Contributions are welcome! Feel free to submit issues or pull requests.

1. Fork the project.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -m "Added new feature"`).
4. Push to your fork (`git push origin feature-branch`).
5. Open a pull request.

---

## 📄 License
This project is licensed under the **MIT License**.

---

## 📩 Contact
For any inquiries or support, reach out at:  
📧 hitthecodelabs@gmail.com  
🌍 [GitHub](https://github.com/hitthecodelabs/GeozoneChecker)
