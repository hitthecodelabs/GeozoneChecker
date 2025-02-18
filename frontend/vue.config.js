const { defineConfig } = require('@vue/cli-service');

module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
    hot: true, // Ensures HMR is enabled
    liveReload: true, // Ensures live reload
    watchFiles: ["src/**/*"], // Watches all Vue files
    port: 8080, // Default Vue port
  }
});
