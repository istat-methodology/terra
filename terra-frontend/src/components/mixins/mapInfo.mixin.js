export default {
  data: () => ({
    isInfo: false,
    infoTitle: "",
    mainFields: [
      {
        key: "Year",
        label: ""
      },
      {
        key: "2020",
        label: "2020"
      },
      {
        key: "2021",
        label: "2021"
      }
    ],
    importFields_it: [
      {
        key: "Main partner 2020",
        label: "Partner principale 2020"
      },
      {
        key: "Total import 2020",
        label: "Importazione totale 2020"
      },
      {
        key: "Main partner 2021",
        label: "Partner principale 2021"
      },
      {
        key: "Total import 2021",
        label: "Importazione totale 2020"
      }
    ],
    importFields_en: [
      {
        key: "Main partner 2020",
        label: "Main partner 2020"
      },
      {
        key: "Total import 2020",
        label: "Total import 2020"
      },
      {
        key: "Main partner 2021",
        label: "Main partner 2021"
      },
      {
        key: "Total import 2021",
        label: "Total import 2021"
      }
    ],
    exportFields_it: [
      {
        key: "Main partner 2020",
        label: "Partner principale 2020"
      },
      {
        key: "Total export 2020",
        label: "Esportazione totale 2020"
      },
      {
        key: "Main partner 2021",
        label: "Partner principale 2021"
      },
      {
        key: "Total export 2021",
        label: "Esportazione totale 2020"
      }
    ],
    exportFields_en: [
      {
        key: "Main partner 2020",
        label: "Main partner 2020"
      },
      {
        key: "Total export 2020",
        label: "Total export 2020"
      },
      {
        key: "Main partner 2021",
        label: "Main partner 2021"
      },
      {
        key: "Total export 2021",
        label: "Total export 2021"
      }
    ]
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
      let mainInfoItalian = []
      for (var info of mainInfo) {
        switch (info["Year"]) {
          case "Population.":
            info["Year"] = isItalian ? "Popolazione" : "Population"
            break
          case "Industrial Production.":
            info["Year"] = isItalian
              ? "Produzione industriale"
              : "Industrial production"
            break
          case "Unemployment.":
            info["Year"] = isItalian ? "Disoccupazione" : "Unemployment"
            break
          case "Import.":
            info["Year"] = isItalian ? "Importazioni (euro)" : "Import (eur)"
            break
          case "Export.":
            info["Year"] = isItalian ? "Esportazioni (euro)" : "Export (eur)"
            break
        }
        mainInfoItalian.push(info)
      }
      return isItalian ? mainInfoItalian : mainInfo
    }
  }
}
