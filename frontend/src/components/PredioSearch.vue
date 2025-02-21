<!-- PredioDetail.vue -->

<template>
  <div class="predio-search">
    <h2>Search Predio by Catastral Code</h2>
    <div class="search-form">
      <input
        v-model="codigoCat"
        placeholder="Enter catastral code"
        @keyup.enter="searchPredio"
      />
      <button @click="searchPredio">Search</button>
    </div>

    <div v-if="loading" class="loading">Loading...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else-if="predio">
      <h3>Predio Details:</h3>
      <table>
        <thead>
          <tr>
            <th>Field</th>
            <th>Value</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(value, key) in predio" :key="key">
            <td>{{ key }}</td>
            <td>{{ value }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import { getPredioByCodigoCat } from "@/api";
import wkt from "wellknown"; // This converts WKT to GeoJSON

export default {
  name: "PredioSearch",
  data() {
    return {
      codigoCat: "",
      predio: null,
      loading: false,
      error: null
    };
  },
  methods: {
    async searchPredio() {
      if (!this.codigoCat) {
        this.error = "Please enter a catastral code";
        return;
      }
      this.loading = true;
      this.error = null;
      this.predio = null;
      try {
        const data = await getPredioByCodigoCat(this.codigoCat);
        this.predio = data;
        // Convert the WKT geometry to GeoJSON
        if (data.geom) {
          const geojson = wkt(data.geom);
          // Emit an event so the parent (App.vue) can update the map
          this.$emit("update-polygon", geojson);
        }
      } catch (err) {
        console.error("Error fetching predio:", err);
        this.error = "Error fetching predio data.";
      } finally {
        this.loading = false;
      }
    }
  }
};
</script>

<style scoped>
.predio-search {
  padding: 20px;
  max-width: 800px;
  margin: 0 auto;
}

.search-form {
  display: flex;
  justify-content: center;
  gap: 10px;
  margin-bottom: 20px;
}

input {
  padding: 8px;
  font-size: 16px;
  width: 250px;
}

button {
  padding: 8px 12px;
  font-size: 16px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:hover {
  background-color: #0056b3;
}

.loading {
  font-size: 18px;
  text-align: center;
  margin-top: 20px;
}

.error {
  color: red;
  font-size: 16px;
  text-align: center;
  margin-top: 20px;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}

th,
td {
  border: 1px solid #ddd;
  padding: 8px;
}

th {
  background-color: #f2f2f2;
  text-align: left;
}
</style>
