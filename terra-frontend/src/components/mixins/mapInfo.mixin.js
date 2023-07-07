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
        key: "2021",
        label: "2021"
      },
      {
        key: "2022",
        label: "2022"
      }
    ],
    importFields_it: [
      {
        key: "Main partner 2021",
        label: "Partner principale 2021"
      },
      {
        key: "Total import 2021",
        label: "Importazione totale 2021"
      },
      {
        key: "Main partner 2022",
        label: "Partner principale 2022"
      },
      {
        key: "Total import 2022",
        label: "Importazione totale 2021"
      }
    ],
    importFields_en: [
      {
        key: "Main partner 2021",
        label: "Main partner 2021"
      },
      {
        key: "Total import 2021",
        label: "Total import 2021"
      },
      {
        key: "Main partner 2022",
        label: "Main partner 2022"
      },
      {
        key: "Total import 2022",
        label: "Total import 2022"
      }
    ],
    exportFields_it: [
      {
        key: "Main partner 2021",
        label: "Partner principale 2021"
      },
      {
        key: "Total export 2021",
        label: "Esportazione totale 2021"
      },
      {
        key: "Main partner 2022",
        label: "Partner principale 2022"
      },
      {
        key: "Total export 2022",
        label: "Esportazione totale 2021"
      }
    ],
    exportFields_en: [
      {
        key: "Main partner 2021",
        label: "Main partner 2021"
      },
      {
        key: "Total export 2021",
        label: "Total export 2021"
      },
      {
        key: "Main partner 2022",
        label: "Main partner 2022"
      },
      {
        key: "Total export 2022",
        label: "Total export 2022"
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
              ? "Produzione industriale (%)"
              : "Industrial production (%)"
            break
          case "Unemployment.":
            info["Year"] = isItalian ? "Disoccupazione (%)" : "Unemployment (%)"
            break
          case "Import.":
            info["Year"] = isItalian ? "Importazioni (euro)" : "Import (euro)"
            break
          case "Export.":
            info["Year"] = isItalian ? "Esportazioni (euro)" : "Export (euro)"
            break
        }
        mainInfoItalian.push(info)
      }
      return isItalian ? mainInfoItalian : mainInfo
    }
  }
}
