// MapView.vue

<template>
    <div id="map-container">
      <!-- Title -->
      <h1>Map Title</h1>
      
      <!-- Coordinate Display -->
      <div id="coordinate-display">
        Lat: {{ cursorLat.toFixed(6) }} | Lon: {{ cursorLng.toFixed(6) }}
      </div>
      
      <!-- File Upload Input with ref -->
      <input type="file" @change="onFileChange" ref="fileInput" accept=".geojson,.kml" />
      
      <!-- Toggle and Delete Buttons (shown only if a file has been loaded) -->
      <div v-if="uploadedLayer" class="button-container">
        <button 
          @click="toggleVisibility" 
          :style="{ backgroundColor: isHidden ? '#28a745' : '#dc3545' }">
          {{ isHidden ? 'Show' : 'Hide' }} Polygon(s)
        </button>
        <button @click="deleteUploadedLayer">
          Delete Polygon(s)
        </button>
      </div>
      
      <!-- Map Container -->
      <div id="map"></div>
      
      <!-- Dropdown for Tile Selection -->
      <select v-model="selectedTile" @change="updateTileLayer">
        <option v-for="(url, name) in tileLayers" :key="name" :value="url">
          {{ name }}
        </option>
      </select>
    </div>
  </template>
  
  <script>
  import L from "leaflet";
  import "leaflet/dist/leaflet.css";
  // Use a namespace import for toGeoJSON
  import * as toGeoJSON from "togeojson";
  
  export default {
    data() {
      return {
        map: null,
        tileLayer: null,
        uploadedLayer: null,
        // Flag to track polygon visibility
        isHidden: false,
        cursorLat: 0,
        cursorLng: 0,
        selectedTile: "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
        tileLayers: {
          "OpenStreetMap": "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
          "Google Satellite": "https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}",
          "Esri Satellite": "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
          "CartoDB Dark Matter": "http://basemaps.cartocdn.com/dark_all/{z}/{x}/{y}.png",
          "OpenTopoMap": "https://tile.opentopomap.org/{z}/{x}/{y}.png"
        }
      };
    },
    mounted() {
      this.initMap();
    },
    methods: {
      initMap() {
        this.map = L.map("map").setView([-2, -78.5], 6);
        this.tileLayer = L.tileLayer(this.selectedTile, {
          attribution: "&copy; OpenStreetMap contributors"
        }).addTo(this.map);
        this.map.on("mousemove", this.updateCursorPosition);
      },
      updateTileLayer() {
        this.map.removeLayer(this.tileLayer);
        this.tileLayer = L.tileLayer(this.selectedTile, {
          attribution: "&copy; OpenStreetMap contributors"
        }).addTo(this.map);
      },
      updateCursorPosition(event) {
        this.cursorLat = event.latlng.lat;
        this.cursorLng = event.latlng.lng;
      },
      onFileChange(event) {
        const file = event.target.files[0];
        if (!file) return;
    
        const reader = new FileReader();
        reader.onload = (e) => {
          const data = e.target.result;
          let geojsonData;
    
          if (file.name.endsWith(".geojson")) {
            try {
              geojsonData = JSON.parse(data);
            } catch (err) {
              console.error("Error parsing GeoJSON:", err);
              return;
            }
          } else if (file.name.endsWith(".kml")) {
            // Convert KML to GeoJSON using toGeoJSON
            const parser = new DOMParser();
            const kml = parser.parseFromString(data, "text/xml");
            geojsonData = toGeoJSON.kml(kml);
          } else {
            console.error("Unsupported file type.");
            return;
          }
    
          // Remove previous uploaded layer if it exists
          if (this.uploadedLayer) {
            this.map.removeLayer(this.uploadedLayer);
          }
    
          // Add the new GeoJSON layer and ensure it's visible
          this.uploadedLayer = L.geoJSON(geojsonData, {
            style: {
              color: "red"
            }
          }).addTo(this.map);
    
          // Reset visibility flag
          this.isHidden = false;
    
          // Zoom to the bounds of the uploaded layer (if valid)
          const bounds = this.uploadedLayer.getBounds();
          if (bounds.isValid()) {
            this.map.fitBounds(bounds);
          }
        };
    
        reader.readAsText(file);
      },
      toggleVisibility() {
        if (this.uploadedLayer) {
          if (!this.isHidden) {
            // Hide the polygon by removing it from the map
            this.map.removeLayer(this.uploadedLayer);
            this.isHidden = true;
          } else {
            // Show the polygon by adding it back to the map
            this.uploadedLayer.addTo(this.map);
            this.isHidden = false;
          }
        }
      },
      deleteUploadedLayer() {
        if (this.uploadedLayer) {
          this.map.removeLayer(this.uploadedLayer);
          this.uploadedLayer = null;
          this.isHidden = false;
          // Clear file input value so a new file with the same name can be loaded.
          this.$refs.fileInput.value = "";
        }
      }
    }
  };
  </script>
  
  <style scoped>
  #map {
    height: 500px;
    width: 100%;
    border-radius: 8px;
    box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2);
    margin-top: 10px;
  }
  
  select {
    position: absolute;
    top: 10px;
    left: 10px;
    z-index: 1000;
    padding: 5px;
    border: none;
    background: rgba(255, 255, 255, 0.8);
    font-size: 14px;
    border-radius: 5px;
    cursor: pointer;
  }
  
  #coordinate-display {
    background: rgba(0, 0, 0, 0.7);
    color: white;
    padding: 8px 12px;
    font-size: 14px;
    border-radius: 5px;
    font-family: monospace;
    margin-bottom: 10px;
  }
  
  input[type="file"] {
    display: block;
    margin-bottom: 10px;
  }
  
  .button-container {
    margin-bottom: 10px;
  }
  
  button {
    margin-right: 10px;
    padding: 8px 12px;
    border: none;
    color: white;
    border-radius: 5px;
    cursor: pointer;
  }
  </style>
  
