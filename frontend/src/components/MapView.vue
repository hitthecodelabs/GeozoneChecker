// MapView.vue

<template>
    <div id="map-container">
      <div id="map"></div>
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
  
  export default {
    data() {
      return {
        map: null,
        tileLayer: null,
        selectedTile: "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", // Default OSM
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
        this.map = L.map("map").setView([0, -78.5], 6);
  
        // Add default tile layer
        this.tileLayer = L.tileLayer(this.selectedTile, {
          attribution: "&copy; OpenStreetMap contributors"
        }).addTo(this.map);
      },
      updateTileLayer() {
        // Remove the existing tile layer
        this.map.removeLayer(this.tileLayer);
  
        // Add the new selected tile layer
        this.tileLayer = L.tileLayer(this.selectedTile, {
          attribution: "&copy; OpenStreetMap contributors"
        }).addTo(this.map);
      }
    }
  };
  </script>
  
  <style scoped>
  #map {
    height: 500px;
    width: 100%;
  }
  select {
    position: absolute;
    top: 10px;
    left: 10px;
    z-index: 1000;
    padding: 5px;
  }
  </style>
  