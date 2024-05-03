export default {
  data: () => ({
    isInfo: false,
    infoTitle: ""
  }),
  methods: {
    openInfo(marker) {
      var name = this.getCountryName(marker.country)
      this.$store.dispatch("geomap/getInfo", marker.country).then(() => {
        this.isInfo = true
        this.infoTitle = name
      })
    },
    openInfoOnFeature(e) {
      var name = this.getCountryName(e.layer.feature.properties.iso_a2)
      var code = e.layer.feature.properties.iso_a2
      this.$store.dispatch("geomap/getInfo", code).then(() => {
        this.isInfo = true
        this.infoTitle = name
      })
    },
    openInfoStart(code) {
      var name = this.getCountryName(name)
      this.$store.dispatch("geomap/getInfo", code).then(() => {
        this.isInfo = true
        this.infoTitle = name
      })
    },
    closeInfo() {
      this.isInfo = false
    },
    localizeMain(mainInfo, isItalian) {
      console.log(isItalian)
      for (var info of mainInfo) {
        switch (info["Year"]) {
          case "Population.":
            info["Year"] = this.$t("map.info.table.information.population")
            break
          case "Industrial Production.":
            info["Year"] = this.$t(
              "map.info.table.information.industrial_production"
            )
            break
          case "Unemployment.":
            info["Year"] = this.$t("map.info.table.information.unemployment")
            break
          case "Import.":
            info["Year"] = this.$t("map.info.table.information.import")
            break
          case "Export.":
            info["Year"] = this.$t("map.info.information.export")
            break
        }
      }
      return mainInfo
    }
  }
}
