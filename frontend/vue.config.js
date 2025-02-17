const { defineConfig } = require('@vue/cli-service');

module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
    watchFiles: ['src/**/*'], // Ensures changes in 'src/' trigger a reload
    port: 8080, // Default port, change if needed
  }
});
