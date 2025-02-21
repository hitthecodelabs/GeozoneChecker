<!-- App.vue -->

<template>
  <div id="app">
    <h1>GIS Map - Environmental Protection Zones</h1>
    <MapView :predioPolygon="predioPolygon" />
    <!-- Pass the event from PredioSearch to update the polygon -->
    <PredioSearch @update-polygon="handleUpdatePolygon" />
  </div>
</template>

<script>
import MapView from "./components/MapView.vue";
import PredioSearch from "./components/PredioSearch.vue";

export default {
  name: "App",
  components: {
    MapView,
    PredioSearch
  },
  data() {
    return {
      predioPolygon: null
    };
  },
  methods: {
    handleUpdatePolygon(geojson) {
      this.predioPolygon = geojson;
    }
  }
};
</script>

<style>
#app {
  text-align: center;
  font-family: Arial, sans-serif;
  padding: 20px;
}
</style>
