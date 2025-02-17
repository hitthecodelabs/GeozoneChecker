// api.js

import axios from 'axios';

const api = axios.create({
  baseURL: "http://127.0.0.1:5001",  // Update from 5000 to 5001
});

export default api;
