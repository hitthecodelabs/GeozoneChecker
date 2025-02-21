// api.js

import axios from 'axios';

const api = axios.create({
  baseURL: "http://127.0.0.1:5001"
});

export const getPredioByCodigoCat = async (codigo_cat) => {
  try {
    const response = await api.get("/predio", { params: { codigo_cat } });
    return response.data;
  } catch (error) {
    console.error("Error fetching predio:", error);
    throw error;
  }
};

export default api;
