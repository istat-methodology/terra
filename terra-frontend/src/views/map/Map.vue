<template>
  <div class="row">
    <h1 class="sr-only">
      {{ $t("landing.map.title") }}
    </h1>
    <div class="col-sm-12 col-md-12">
      <div class="card card-map" :title="$t('sidebar.map')">
        <CCardBody tabindex="-1">
          <l-map
            ref="map"
            id="map"
            :zoom="zoom"
            :center="center"
            class
            style="height: 100%; width: 100%"
            @ready="setMapScreenShooter()"
            @click="closeInfo()"
            tabindex="-1">
            <l-tile-layer
              :url="url"
              :attribution="attribution"
              aria-hidden="true" />
            <l-geo-json
              aria-hidden="true"
              v-if="geoJson"
              :visible="!isFeature"
              :geojson="geoJson"
              :options="options"
              :options-style="styleFunction"
              @click="openInfoOnFeature"
              tabindex="0"></l-geo-json>

            <l-circle-marker
              aria-hidden="true"
              v-for="(marker, i) in markerPeriodSeries"
              v-bind:key="i"
              :lat-lng="[
                marker.coordinates.latitude,
                marker.coordinates.longitude
              ]"
              :visible="isMarker"
              :fillOpacity="0.65"
              :radius="getRadius(marker.series)"
              :color="getColor(marker.series, markerMin, markerMax)"
              :fillColor="getColor(marker.series, markerMin, markerMax)"
              @click="openInfo(marker)"
              tabindex="0">
              <l-tooltip
                aria-hidden="true"
                role="tooltip"
                :options="{ interactive: true, permanent: false }"
                tabindex="0">
                <span class="tooltip-span" tabindex="-1"
                  >{{ marker.name }} {{ ie }}
                  {{ marker.series + "%" }}
                </span>
              </l-tooltip>
            </l-circle-marker>

            <l-control position="topright" tabindex="-1" aria-hidden="true">
              <div id="Legend" class="legend"></div>
              <div class="legend-title">
                {{
                  !isImport
                    ? $t("map.legend.title.export")
                    : $t("map.legend.title.import")
                }}
              </div>
            </l-control>
            <l-control position="bottomleft" tabindex="0">
              <div class="info" v-if="isInfo" aria-hidden="true">
                <div class="font-class pl-2 pt-2 pb-2" :title="infoTitle">
                  <strong>{{ infoTitle }}</strong>
                </div>
                <CTabs v-if="infoData" variant="tabs" :active-tab="0">
                  <CTab :title="infoTabMain">
                    <CDataTable :items="micro" :fields="mainFields" hover />
                  </CTab>
                  <CTab :title="infoTabImport">
                    <CDataTable
                      :items="importDataItems"
                      :fields="importFields"
                      hover />
                  </CTab>
                  <CTab :title="infoTabExport">
                    <CDataTable
                      :items="exportDataItems"
                      :fields="exportFields"
                      hover />
                  </CTab>
                </CTabs>
              </div>
            </l-control>
            <l-control position="topleft">
              <div class="leaflet-bar">
                <a
                  class="control-btn"
                  :title="
                    !isMarker
                      ? $t('map.toolbar.feature')
                      : $t('map.toolbar.marker')
                  "
                  role="button"
                  @click="setFeatureMarker()"
                  tabindex="0"
                  >{{ btnFeatureMarker }}</a
                >
                <a
                  class="control-btn"
                  :title="
                    !isImport
                      ? $t('map.toolbar.import')
                      : $t('map.toolbar.export')
                  "
                  role="button"
                  @click="setImportExport()"
                  tabindex="0"
                  >{{ btnImportExport }}</a
                >
                <a
                  :title="$t('map.toolbar.shot')"
                  class="control-btn"
                  role="button"
                  @click="shot(true, $event.code, 'terra_mapseries')"
                  @keydown="shot(false, $event.code, 'terra_mapseries')"
                  tabindex="0"
                  ><camera-icon alt="" class="icon-size"
                /></a>
                <exporter
                  filename="terra_mapseries"
                  iam="map"
                  :data="[seriesData, '']"
                  source="map"
                  tabindex="0">
                </exporter>
              </div>
            </l-control>
          </l-map>
        </CCardBody>
      </div>
      <div class="row">
        <div class="col-sm-12 col-md-12">
          <vue-slider
            v-if="mapPeriod"
            :adsorb="true"
            :tooltip="'none'"
            v-model="seriesPeriod"
            :data="mapPeriod"
            :data-value="'id'"
            :data-label="'selectName'"
            @change="handleCounterChange"
            :dot-attrs="{
              'aria-valuemin': mapPeriod[0].id,
              'aria-valuemax': mapPeriod[mapPeriod.length - 1].id
            }" />
        </div>
      </div>
    </div>
    <!-- Marker modal -->
    <CModal
      :title="$t('map.modal.main.title')"
      :show.sync="isModalHelp"
      size="lg">
      <p v-html="$t('map.modal.main.body')"></p>
      <template #footer>
        <CButton color="outline-primary" square size="sm" @click="helpOn(false)"
          >Close</CButton
        >
      </template>
    </CModal>
  </div>
</template>
<script>
import { mapGetters } from "vuex"
import { Context, sliderDefault } from "@/common"
import {
  LMap,
  LGeoJson,
  LTileLayer,
  LControl,
  LTooltip,
  LCircleMarker
} from "vue2-leaflet"
import mapMixin from "@/components/mixins/map.mixin"
import mapInfoMixin from "@/components/mixins/mapInfo.mixin"
import sliderMixin from "@/components/mixins/slider.mixin"
import SimpleMapScreenshoter from "leaflet-simple-map-screenshoter"
import VueSlider from "vue-slider-component"
import exporter from "@/components/Exporter"
import { saveAs } from "file-saver"

export default {
  name: "Map",
  components: {
    LMap,
    LTileLayer,
    "l-geo-json": LGeoJson,
    LControl,
    LCircleMarker,
    LTooltip,
    VueSlider,
    exporter
  },
  mixins: [mapMixin, mapInfoMixin, sliderMixin],
  data: () => ({
    attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a>',
    url: "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
    center: [51.16423, 1.45412],
    zoom: 4,
    seriesPeriod: "",
    markerPeriodSeries: [],
    markerMax: 60,
    markerMin: -60,
    enableTooltip: true,
    layer: {
      style: {
        default: {
          weight: 1,
          opacity: 1,
          color: "gray",
          dashArray: "",
          fillOpacity: 0.7
        },
        over: {
          weight: 1,
          opacity: 1,
          color: "black",
          dashArray: "",
          fillOpacity: 0.7
        }
      }
    },
    btnFeatureMarker: "M",

    isMarker: false,
    isFeature: false,
    seriesName: "exportseries",
    btnImportExport: "IMP",

    isImport: false,
    isExport: false,

    ie: "Export",

    isModalHelp: false,
    simpleMapScreenshoter: {}
  }),
  watch: {
    language() {
      this.$store.dispatch("message/success", this.$t("common.update_cls"))
      this.$store.dispatch("classification/getClassifications").then(() => {
        this.loadData()
      })
    }
  },
  computed: {
    ...mapGetters("metadata", ["mapPeriod", "mapSeries"]),
    ...mapGetters("coreui", ["isItalian", "language"]),
    ...mapGetters("classification", ["getCountryName"]),
    ...mapGetters("geomap", {
      markers: "geomap",
      infoData: "infoData",
      seriesData: "seriesData"
    }),
    ...mapGetters("countries", {
      geoJson: "countriesBorders",
      jsonData: "jsonData"
    }),
    micro() {
      return this.infoData
        ? this.localizeMain(
            this.infoData[0]["Main information"],
            this.isItalian
          )
        : []
    },
    infoTabMain() {
      return this.isItalian ? "Dati macro" : "Main"
    },
    infoTabImport() {
      return this.isItalian ? "Partner di importazione" : "Import partners"
    },
    infoTabExport() {
      return this.isItalian ? "Partner di esportazione" : "Export partners"
    },
    importFields() {
      return this.isItalian ? this.importFields_it : this.importFields_en
    },
    exportFields() {
      return this.isItalian ? this.exportFields_it : this.exportFields_en
    },
    importDataItems() {
      return this.infoData ? this.infoData[0]["Main Import Partners"] : []
    },
    exportDataItems() {
      return this.infoData ? this.infoData[0]["Main Export Partners"] : []
    },
    importGoods() {
      return this.infoData ? this.infoData[0]["Main Import Goods"] : []
    },
    exportGoods() {
      return this.infoData ? this.infoData[0]["Main Export Goods"] : []
    },
    options() {
      return {
        onEachFeature: this.onEachFeatureFunction
      }
    },
    styleFunction() {
      return () => {
        return {
          weight: this.layer.style.default.weight,
          opacity: this.layer.style.defaultopacity,
          color: this.layer.style.default.color,
          dashArray: this.layer.style.default.dashArray,
          fillOpacity: this.layer.style.default.fillOpacity
        }
      }
    },
    onEachFeatureFunction() {
      return (feature, layer) => {
        var value = this.jsonData[feature.properties.iso_a2]
        this.selectedCountry.code = feature.properties.iso_a2
        this.selectedCountry.name = this.getCountryName(
          feature.properties.iso_a2
        )
        layer.options.fillColor = "#00000000"
        if (value != undefined) {
          layer.options.fillColor = this.getColor(
            value,
            this.markerMin,
            this.markerMax
          )
          layer.options.color = "gray"
          layer.bindTooltip(
            "<div>" +
              this.selectedCountry.name +
              "<span> " +
              this.ie +
              "</span> " +
              value +
              "%" +
              "</span>" +
              " </div>",
            { permanent: false, sticky: false }
          )
          layer.on({
            mouseover: this.mouseover,
            mouseout: this.mouseout
          })
        }
      }
    }
  },
  methods: {
    helpOn(showModal) {
      this.isModalHelp = showModal
      this.modalHelpTitle = "About map"
    },
    handleCounterChange(val) {
      this.seriesPeriod = val
      this.buildPeriodSeries()
      this.buildFeatures()
    },
    getPeriodSeries(marker, seriesData, seriesPeriod) {
      const localSeries = seriesData.find((serie) => {
        return serie.country == marker.country
      })
      return localSeries ? localSeries[seriesPeriod] : 0
    },
    buildPeriodSeries() {
      this.markerPeriodSeries = this.markers.map((marker) => {
        return {
          ...marker,
          series: this.getPeriodSeries(
            marker,
            this.seriesData,
            this.seriesPeriod
          )
        }
      })

      this.dataLegend = this.getDataLegend(this.seriesData, this.seriesPeriod)
      this.markerMax = this.getMax()
      this.markerMin = this.getMin()
      this.setLegend(this.markerMin, this.markerMax, this.dataLegend, this.ie)
    },

    buildFeatures() {
      this.$store
        .dispatch("countries/getDataSeries", this.seriesName)
        .then((seriesData) => {
          this.$store.dispatch("countries/getCountriesBorders", {
            seriesData: seriesData,
            seriesPeriod: this.seriesPeriod
          })
        })
    },
    getDataLegend(seriesData, seriesPeriod) {
      var data = []
      seriesData.forEach((obj) => {
        for (const key in obj) {
          if (key == seriesPeriod) {
            data.push(obj[key])
          }
        }
      })
      return data
    },
    loadData() {
      this.$store.dispatch("coreui/setContext", Context.Map)
      this.seriesPeriod = sliderDefault
      this.getDataSeries("exportseries")
    },
    getMax() {
      return 60
    },
    getMin() {
      return -60
    },
    setFeatureMarker() {
      this.btnFeatureMarker = this.btnFeatureMarker == "M" ? "F" : "M"
      this.isFeature = !this.isFeature
      this.isMarker = !this.isMarker
    },
    setImportExport() {
      this.btnImportExport = this.btnImportExport == "IMP" ? "EXP" : "IMP"
      this.seriesName =
        this.btnImportExport != "IMP" ? "importseries" : "exportseries"
      this.ie = this.btnImportExport != "IMP" ? "Import" : "Export"
      this.getDataSeries(this.seriesName)
      this.isImport = !this.isImport
      this.isExport = !this.isExport
    },
    mouseover(e) {
      var layer = e.target
      layer.setStyle({
        color: this.layer.style.over.color,
        dashArray: this.layer.style.over.dashArray
      })
    },
    mouseout(e) {
      var layer = e.target
      layer.setStyle({
        color: this.layer.style.default.color,
        dashArray: this.layer.style.default.dashArray
      })
    },
    getDataSeries() {
      this.$store.dispatch("geomap/findAll").then(() => {
        this.$store.dispatch("geomap/getSeries", this.seriesName).then(() => {
          this.buildPeriodSeries()
          this.buildFeatures()
        })
      })
    },
    fixSliderAccessibility() {
      setTimeout(() => {
        document.querySelectorAll(".vue-slider-dot").forEach((element) => {
          element.setAttribute("aria-label", "slider-map")
        })
      }, 300)
    },
    fixMapAccessibility() {
      setTimeout(() => {
        document
          .querySelectorAll(".leaflet-pane.leaflet-map-pane")
          .forEach((element) => {
            element.setAttribute("aria-hidden", "true")
          })
      }, 300)
    },
    fixHeaderTableForAccessibility() {
      setTimeout(() => {
        document.querySelectorAll("li.a.nav-link").forEach((element) => {
          element.setAttribute("title", element.innerText)
          element.setAttribute("aria-label", element.innerText)
        })
      }, 300)
    },
    setMapScreenShooter() {
      this.simpleMapScreenshoter = new SimpleMapScreenshoter({
        hideElementsWithSelectors: [],
        hidden: true // hide screen btn on map
      }).addTo(this.$refs.map.mapObject)
    },
    shot(mouse, e, filename) {
      if (mouse == true || e == "Enter") {
        this.simpleMapScreenshoter
          .takeScreen("blob")
          .then((blob) => {
            saveAs(blob, filename + ".png")
          })
          .catch((e) => {
            console.log(e.toString())
          })
      }
    },
    fixASidebarMenu() {
      setTimeout(() => {
        document.querySelectorAll(".c-sidebar-nav-link").forEach((element) => {
          element.setAttribute("aria-current", "false")
        })
      }, 300)
      setTimeout(() => {
        document
          .querySelectorAll(".c-sidebar-nav-link.c-active")
          .forEach((element) => {
            element.setAttribute("aria-current", "page")
          })
      }, 300)
    }
  },
  created() {
    this.loadData()
    this.fixSliderAccessibility()
    this.fixMapAccessibility()
    this.fixASidebarMenu()
  }
}
</script>
<style scoped>
@import "~leaflet/dist/leaflet.css";
.card {
  margin-bottom: 0px;
}
.card-body {
  padding: 0;
}
.card-footer {
  background-color: #ebedef;
}
/* Modal */
@media (min-width: 576px) {
  .modal-dialog {
    margin: 5rem auto;
  }
}
.modal-footer {
  padding: 0.4rem 0.75rem;
}
.modal-header {
  padding: 0.75rem 1rem;
}
.btn-primary.disabled,
.btn-primary:disabled {
  color: #fff;
  background-color: #8f85ed;
  border-color: #321fdb;
}
.legend {
  background-color: transparent;
  width: 360px;
  height: 40px;
  margin-left: 10px;
  padding: 1px !important;
}
.legend-title {
  margin-top: 0px;
  margin-left: 0px;
  font-size: 1.2em;
  font-weight: 600;
  fill: rgb(102, 102, 102);
  text-align: center;
}

#Legend .colorlegend-labels {
  font-size: 1em;
  fill: black;
}
.control-btn {
  font-weight: bold;
  text-indent: 1px;
}
.font-class {
  font-size: 1.4rem;
}
.icon-size {
  font-size: 1.5em;
}
.vue-slider-mark-label .vue-slider-mark-label-active {
  color: #000 !important;
}
</style>
