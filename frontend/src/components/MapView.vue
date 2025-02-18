<!-- MapView.vue -->
<template>
    <div id="map-container">
      
      <!-- Coordinate Display -->
      <div id="coordinate-display">
        Lat: {{ cursorLat.toFixed(6) }} | Lon: {{ cursorLng.toFixed(6) }}
      </div>
      
      <!-- File Upload Input with ref -->
      <input type="file" @change="onFileChange" ref="fileInput" accept=".geojson,.kml" />
      
      <!-- Loading Indicator (spinner only) -->
      <div v-if="loading" class="loading-indicator">
        <div class="spinner"></div>
      </div>
      
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
  import * as toGeoJSON from "togeojson";
  
  export default {
    data() {
      return {
        map: null,
        tileLayer: null,
        uploadedLayer: null,
        isHidden: false,
        loading: false,
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
    
        // Update cursor position on mouse move
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
    
        // Show loading spinner
        this.loading = true;
    
        // Give the DOM time to render the spinner before heavy parsing
        this.$nextTick(() => {
          setTimeout(() => {
            const reader = new FileReader();
            reader.onload = (e) => {
              const data = e.target.result;
              let geojsonData;
    
              if (file.name.endsWith(".geojson")) {
                try {
                  geojsonData = JSON.parse(data);
                } catch (err) {
                  console.error("Error parsing GeoJSON:", err);
                  this.loading = false;
                  return;
                }
              } else if (file.name.endsWith(".kml")) {
                // Remove "kml:" prefixes
                const kmlString = data.replace(/(<\/?)kml:/g, '$1');
                const parser = new DOMParser();
                const kml = parser.parseFromString(kmlString, "text/xml");
                geojsonData = toGeoJSON.kml(kml);
              } else {
                console.error("Unsupported file type.");
                this.loading = false;
                return;
              }
    
              // Remove previous layer if it exists
              if (this.uploadedLayer) {
                this.map.removeLayer(this.uploadedLayer);
              }
    
              // Add new layer with blue color instead of red
              this.uploadedLayer = L.geoJSON(geojsonData, {
                style: { color: "blue" }
              }).addTo(this.map);
    
              // Show polygons
              this.isHidden = false;
    
              // Fit map to layer bounds
              const bounds = this.uploadedLayer.getBounds();
              if (bounds.isValid()) {
                const center = bounds.getCenter();
                const ne = bounds.getNorthEast();
                const sw = bounds.getSouthWest();
                const latDiff = Math.abs(ne.lat - sw.lat);
                const lngDiff = Math.abs(ne.lng - sw.lng);
    
                // Adjust zoom based on bounds size
                if (latDiff < 0.0001 && lngDiff < 0.0001) {
                  this.map.setView(center, 18);
                } else if (latDiff < 0.001 || lngDiff < 0.001) {
                  const newBounds = L.latLngBounds(
                    [center.lat - 0.005, center.lng - 0.005],
                    [center.lat + 0.005, center.lng + 0.005]
                  );
                  this.map.fitBounds(newBounds, { padding: [20, 20], maxZoom: 18 });
                } else {
                  this.map.fitBounds(bounds, { padding: [20, 20], maxZoom: 18 });
                }
              }
    
              // Hide loading spinner
              this.loading = false;
            };
    
            reader.onerror = () => {
              console.error("Error reading file");
              this.loading = false;
            };
    
            reader.readAsText(file);
          }, 50);
        });
      },
      toggleVisibility() {
        if (this.uploadedLayer) {
          if (!this.isHidden) {
            this.map.removeLayer(this.uploadedLayer);
            this.isHidden = true;
          } else {
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
          // Reset file input
          this.$refs.fileInput.value = "";
        }
      }
    }
  };
  </script>
  
  <style>
  /* No 'scoped' so keyframes and global classes work */
  
  /* Map */
  #map {
    height: 500px;
    width: 100%;
    border-radius: 8px;
    box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2);
    margin-top: 10px;
  }
  
  /* Dropdown for tiles */
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
  
  /* Coordinate display */
  #coordinate-display {
    background: rgba(0, 0, 0, 0.7);
    color: white;
    padding: 8px 12px;
    font-size: 14px;
    border-radius: 5px;
    font-family: monospace;
    margin-bottom: 10px;
  }
  
  /* File input */
  input[type="file"] {
    display: block;
    margin-bottom: 10px;
  }
  
  /* Loading indicator (spinner only) */
  .loading-indicator {
    margin-bottom: 10px;
    display: flex;
    align-items: center;
  }
  
  .spinner {
    width: 30px;
    height: 30px;
    border: 5px solid #ccc;
    border-top-color: #007bff;
    border-radius: 50%;
    animation: spin 1s linear infinite;
  }
  
  @keyframes spin {
    to {
      transform: rotate(360deg);
    }
  }
  
  /* Buttons container */
  .button-container {
    margin-bottom: 10px;
  }
  
  /* Shared button styling */
  button {
    margin-right: 10px;
    padding: 8px 12px;
    border: none;
    color: white;
    border-radius: 5px;
    cursor: pointer;
  }
  </style>
  