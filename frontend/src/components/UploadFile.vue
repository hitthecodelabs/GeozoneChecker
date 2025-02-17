//UploadFile.vue
// Code to upload a file to the server

<template>
    <div>
      <h2>Upload a File</h2>
      <input type="file" @change="handleFileUpload" />
      <button @click="submitFile">Upload</button>
      <p v-if="message">{{ message }}</p>
    </div>
  </template>
  
  <script>
  import api from '../api';
  
  export default {
    data() {
      return {
        file: null,
        message: ""
      };
    },
    methods: {
      handleFileUpload(event) {
        this.file = event.target.files[0];
      },
      async submitFile() {
        if (!this.file) {
          this.message = "Please select a file first.";
          return;
        }
  
        let formData = new FormData();
        formData.append("file", this.file);
  
        try {
          await api.post("/upload", formData, {
            headers: { "Content-Type": "multipart/form-data" }
          });
          this.message = "Upload successful! Report is being generated.";
        } catch (error) {
          this.message = "Upload failed: " + (error.response?.data?.error || error.message);
        }
      }
    }
  };
  </script>
  
  <style scoped>
  h2 {
    color: #333;
  }
  button {
    margin-top: 10px;
    padding: 10px;
    background-color: #007bff;
    color: white;
    border: none;
    cursor: pointer;
  }
  </style>
  