var path = require("path")

module.exports = {
  devServer: {
    host: "0.0.0.0",
    port: 8070,
    compress: true
  },

  productionSourceMap: true,

  configureWebpack: (config) => {
    // source map più leggibili in sviluppo
    if (process.env.NODE_ENV === "development") {
      config.devtool = "source-map" // oppure "eval-source-map"
    }

    config.resolve = config.resolve || {}
    config.resolve.alias = {
      ...(config.resolve.alias || {}),
      icons: path.resolve(__dirname, "node_modules/vue-material-design-icons")
    }
    config.resolve.extensions = [".vue", ...(config.resolve.extensions || [])]
  }
}
