<template>
  <div id="app">
    <h1>GIS Map - Environmental Protection Zones</h1>
    <MapView />
    <UploadFile />
  </div>
</template>

<script>
import MapView from "./components/MapView.vue";
// import UploadFile from "./components/UploadFile.vue";

export default {
  components: {
    MapView,
    // UploadFile
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
