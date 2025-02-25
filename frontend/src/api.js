// api.js

import axios from "axios";

const api = axios.create({
  baseURL: "http://127.0.0.1:5001"
});

export const getPredioByCol7a9f2b3c = async (col_7a9f2b3c) => {
  try {
    const response = await api.get("/search", { params: { col_7a9f2b3c } });
    return response.data;
  } catch (error) {
    console.error("Error fetching predio:", error);
    throw error;
  }
};

export default api;
