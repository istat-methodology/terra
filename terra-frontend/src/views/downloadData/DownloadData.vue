<template>
  <div class="download-page">
    <h1 class="sr-only">{{ $t("common.acronym") }}</h1>
    <div class="download-heading">
      <div>
        <h2>{{ $t("download-data.title") }}</h2>
        <p>{{ $t("download-data.body") }}</p>
      </div>
    </div>
    <div class="download-card">
      <form class="download-form" @submit.prevent="submitDataDownload">
        <div class="download-form__grid">
          <div class="form-section form-section--source">
            <div class="form-section__title">
              <span>1</span>
              {{ $t("download-data.form.sections.source") }}
            </div>
            <div class="form-section__grid form-section__grid--source">
              <label
                id="label__seriesData"
                class="card-label form-field form-field--wide"
                :title="$t('download-data.form.fields.seriesData')"
                >{{ $t("download-data.form.fields.seriesData") }}
                <v-select
                  label="descr"
                  :options="getSeriesData"
                  :placeholder="
                    $t('download-data.form.fields.seriesData_placeholder')
                  "
                  v-model="seriesData"
                  :class="{
                    'is-invalid': $v.seriesData.$error
                  }"
                  :clearable="false" />
              </label>
            </div>
          </div>

          <div v-if="isTimeSeries" class="form-section form-section--measure">
            <div class="form-section__title">
              <span>2</span>
              {{ $t("download-data.form.sections.filters") }}
            </div>
            <div class="form-section__grid">
              <label id="label__tsDataType" class="card-label form-field">
                {{ $t("timeseries.form.fields.dataType") }}
                <v-select
                  v-model="tsDataType"
                  label="descr"
                  :options="dataTypes"
                  :class="{ 'is-invalid': $v.tsDataType.$error }"
                  :clearable="false" />
              </label>
              <label id="label__tsVarType" class="card-label form-field">
                {{ $t("timeseries.form.fields.varType") }}
                <v-select
                  v-model="tsVarType"
                  label="descr"
                  :options="varTypes"
                  :class="{ 'is-invalid': $v.tsVarType.$error }"
                  :clearable="false" />
              </label>
              <label id="label__tsFlow" class="card-label form-field">
                {{ $t("timeseries.form.fields.flow") }}
                <v-select
                  v-model="tsFlow"
                  label="descr"
                  :options="flowsTs"
                  :class="{ 'is-invalid': $v.tsFlow.$error }"
                  :clearable="false" />
              </label>
              <label id="label__tsCountry" class="card-label form-field">
                {{ $t("timeseries.form.fields.country") }}
                <v-select
                  v-model="tsCountry"
                  label="name"
                  :options="countries"
                  :class="{ 'is-invalid': $v.tsCountry.$error }"
                  :clearable="false" />
              </label>
              <label id="label__tsPartner" class="card-label form-field">
                {{ $t("timeseries.form.fields.partner") }}
                <v-select
                  v-model="tsPartner"
                  label="descr"
                  multiple
                  :options="partners"
                  :class="{ 'is-invalid': $v.tsPartner.$error }"
                  :clearable="false" />
              </label>
              <label id="label__tsProduct" class="card-label form-field">
                {{ $t("timeseries.form.fields.productsCPA") }}
                <v-select
                  v-model="tsProduct"
                  label="descr"
                  :options="productsCPA"
                  :class="{ 'is-invalid': $v.tsProduct.$error }"
                  :clearable="false" />
              </label>
            </div>
          </div>

          <div v-if="isTrade" class="form-section form-section--measure">
            <div class="form-section__title">
              <span>2</span>
              {{ $t("download-data.form.sections.filters") }}
            </div>
            <div class="form-section__grid">
              <label id="label__tradeSeriesType" class="card-label form-field">
                {{ $t("trade.form.fields.seriesType") }}
                <v-select
                  v-model="tradeSeriesType"
                  label="descr"
                  :options="seriesTypes"
                  :class="{ 'is-invalid': $v.tradeSeriesType.$error }"
                  :clearable="false" />
              </label>
              <label id="label__tradeVarType" class="card-label form-field">
                {{ $t("trade.form.fields.varType") }}
                <v-select
                  v-model="tradeVarType"
                  label="descr"
                  :options="varTypes"
                  :class="{ 'is-invalid': $v.tradeVarType.$error }"
                  :clearable="false" />
              </label>
              <label id="label__tradeFlow" class="card-label form-field">
                {{ $t("trade.form.fields.flow") }}
                <v-select
                  v-model="tradeFlow"
                  label="descr"
                  :options="flows"
                  :class="{ 'is-invalid': $v.tradeFlow.$error }"
                  :clearable="false" />
              </label>
              <label id="label__tradeCountry" class="card-label form-field">
                {{ $t("trade.form.fields.country") }}
                <v-select
                  v-model="tradeCountry"
                  label="name"
                  :options="countries"
                  :class="{ 'is-invalid': $v.tradeCountry.$error }"
                  :clearable="false" />
              </label>
              <label
                id="label__tradeProduct"
                class="card-label form-field form-field--full">
                {{ $t("trade.form.fields.products") }}
                <v-select
                  v-model="tradeProduct"
                  label="displayName"
                  multiple
                  :options="tradeProducts"
                  :class="{ 'is-invalid': $v.tradeProduct.$error }"
                  :clearable="false" />
              </label>
            </div>
          </div>

          <div v-if="isMap" class="form-section form-section--measure">
            <div class="form-section__title">
              <span>2</span>
              {{ $t("download-data.form.sections.filters") }}
            </div>
            <div class="form-section__grid">
              <label
                id="label__mapSeries"
                class="card-label form-field form-field--full">
                {{ $t("download-data.form.fields.mapSeries") }}
                <v-select
                  v-model="mapSeries"
                  label="descr"
                  :options="mapSeriesOptions"
                  :class="{ 'is-invalid': $v.mapSeries.$error }"
                  :clearable="false" />
              </label>
            </div>
          </div>
        </div>

        <div class="download-actions">
          <p
            v-if="downloadStatus.message"
            class="download-status"
            :class="`download-status--${downloadStatus.type}`"
            role="status"
            aria-live="polite">
            {{ downloadStatus.message }}
          </p>
          <button
            type="button"
            class="btn btn-light btn-sm"
            @click="resetFilters">
            {{ $t("common.reset_filters") }}
          </button>
          <button
            type="button"
            class="btn btn-primary btn-sm"
            :disabled="isLoading || !canDownload"
            @click="submitDataDownload">
            <span v-if="!isLoading">{{
              $t("download-data.form.download")
            }}</span>
            <span v-else>{{ $t("common.preparing_download") }}</span>
          </button>
        </div>
        <div class="exporters" aria-hidden="true">
          <exporter
            v-if="isTimeSeries && tsCsvTable.length"
            ref="timeSeriesExporter"
            filename="terra_timeseries"
            :data="[tsCsvTable, 'timeseries']"
            :filter="timeSeriesSearchFilter"
            :options="['csv']"
            source="table2" />
          <exporter
            v-if="isTrade && tradeCsvData.length"
            ref="tradeExporter"
            filename="terra_basket"
            :data="[tradeCsvData, 'trade']"
            :filter="tradeSearchFilter"
            :timePeriod="tradeTimePeriod"
            :options="['csv']"
            source="matrix" />
          <exporter
            v-if="isMap && mapCsvData.length"
            ref="mapExporter"
            filename="terra_mapseries"
            :data="[mapCsvData, '']"
            :options="['csv']"
            source="map" />
        </div>
      </form>
    </div>
  </div>
</template>
<script>
import { mapGetters } from "vuex"
import { Context } from "@/common"
import { metadataService } from "@/services"
import { required, requiredIf } from "vuelidate/lib/validators"
import exporter from "@/components/Exporter"

export default {
  name: "download-data",

  components: { exporter },
  data: () => ({
    spinner: false,
    /* Form fields */
    seriesData: null,
    tsDataType: null,
    tsVarType: null,
    tsFlow: null,
    tsCountry: null,
    tsPartner: null,
    tsProduct: null,
    tsCsvTable: [],
    tsDates: [],
    tradeSeriesType: null,
    tradeVarType: null,
    tradeFlow: null,
    tradeCountry: null,
    tradeProduct: null,
    mapSeries: null,
    mapCsvData: [],
    isLoading: false,
    downloadStatus: {
      type: "",
      message: ""
    }
  }),
  watch: {
    language() {
      this.$store.dispatch("message/success", this.$t("common.update_cls"))
      this.$store.dispatch("classification/getClassifications").then(() => {
        this.applyDefaults()
        this.fixLanguageAccessibility()
        this.fixMetaTitle()
      })
    },
    seriesData() {
      this.downloadStatus = { type: "", message: "" }
      this.$v.$reset()
    }
  },
  computed: {
    ...mapGetters("coreui", ["language"]),
    ...mapGetters("classification", [
      "loaded",
      "countries",
      "partners",
      "flows",
      "flowsTs",
      "dataTypes",
      "varTypes",
      "seriesTypes",
      "productsCPA"
    ]),
    ...mapGetters("trade", {
      tradeCharts: "charts",
      tradeProducts: "products"
    }),
    ...mapGetters("metadata", ["tradePeriod", "tradeVariationPeriod"]),
    isTimeSeries() {
      return this.seriesData?.value === "03"
    },
    isTrade() {
      return this.seriesData?.value === "04"
    },
    isMap() {
      return this.seriesData?.value === "05"
    },
    canDownload() {
      if (this.isTimeSeries) {
        return Boolean(
          this.tsDataType &&
            this.tsVarType &&
            this.tsFlow &&
            this.tsCountry &&
            this.tsProduct &&
            Array.isArray(this.tsPartner) &&
            this.tsPartner.length
        )
      }
      if (this.isTrade) {
        return Boolean(
          this.tradeSeriesType &&
            this.tradeVarType &&
            this.tradeFlow &&
            this.tradeCountry &&
            Array.isArray(this.tradeProduct) &&
            this.tradeProduct.length
        )
      }
      return this.isMap && Boolean(this.mapSeries)
    },
    getSeriesData() {
      return [
        {
          value: "03",
          descr: this.$t("download-data.form.options.timeSeries")
        },
        {
          value: "04",
          descr: this.$t("download-data.form.options.productBasket")
        },
        {
          value: "05",
          descr: this.$t("download-data.form.options.interactiveMap")
        }
      ]
    },
    mapSeriesOptions() {
      return [
        {
          value: "exportseries",
          descr: this.$t("download-data.form.options.exports")
        },
        {
          value: "importseries",
          descr: this.$t("download-data.form.options.imports")
        }
      ]
    },
    tradeTimePeriod() {
      return this.tradeSeriesType?.id == 1
        ? this.tradePeriod
        : this.tradeVariationPeriod
    },
    tradeCsvData() {
      if (!this.tradeCharts?.data || !this.tradeProduct) return []
      const selectedAll = this.tradeProduct.some(
        (product) => product.id === "00"
      )
      const selectedNames = this.tradeProduct.map((product) => product.dataname)
      return this.tradeCharts.data
        .filter(
          (product) => selectedAll || selectedNames.includes(product.dataname)
        )
        .map((product) => ({
          dataname: product.dataname,
          productID: product.productID,
          value: product.value.map((value) => this.formatNumber(value))
        }))
    },
    timeSeriesSearchFilter() {
      return [
        { field: this.$t("timeseries.download.title"), value: "" },
        {
          field: this.$t("timeseries.form.fields.dataType"),
          value: this.tsDataType?.descr || ""
        },
        {
          field: this.$t("timeseries.form.fields.varType"),
          value: this.tsVarType?.descr || ""
        },
        {
          field: this.$t("timeseries.form.fields.flow"),
          value: this.tsFlow?.descr || ""
        },
        {
          field: this.$t("timeseries.form.fields.country"),
          value: this.tsCountry?.name || ""
        },
        {
          field: this.$t("timeseries.form.fields.partner"),
          value: (this.tsPartner || []).map((p) => p.descr).join(", ")
        },
        {
          field: this.$t("timeseries.form.fields.productsCPA"),
          value: this.tsProduct?.descr || ""
        },
        {
          field: this.$t("common.start_date"),
          value: this.tsDates[0] || ""
        },
        {
          field: this.$t("common.end_date"),
          value: this.tsDates[this.tsDates.length - 1] || ""
        }
      ]
    },
    tradeSearchFilter() {
      return [
        { field: this.$t("trade.download.title"), value: "" },
        {
          field: this.$t("trade.form.fields.varType"),
          value: this.tradeVarType?.descr || ""
        },
        {
          field: this.$t("trade.form.fields.country"),
          value: this.tradeCountry?.name || ""
        },
        {
          field: this.$t("trade.form.fields.flow"),
          value: this.tradeFlow?.descr || ""
        },
        {
          field: this.$t("trade.form.fields.products"),
          value: (this.tradeProduct || []).map((p) => p.dataname).join("#")
        },
        {
          field: this.$t("common.start_date"),
          value: this.tradePeriod?.[0]?.isoDate || ""
        },
        {
          field: this.$t("common.end_date"),
          value: this.tradePeriod?.[this.tradePeriod.length - 1]?.isoDate || ""
        }
      ]
    }
  },

  validations: {
    seriesData: {
      required
    },
    tsDataType: {
      required: requiredIf(function () {
        return this.isTimeSeries
      })
    },
    tsVarType: {
      required: requiredIf(function () {
        return this.isTimeSeries
      })
    },
    tsFlow: {
      required: requiredIf(function () {
        return this.isTimeSeries
      })
    },
    tsCountry: {
      required: requiredIf(function () {
        return this.isTimeSeries
      })
    },
    tsPartner: {
      required: requiredIf(function () {
        return this.isTimeSeries
      })
    },
    tsProduct: {
      required: requiredIf(function () {
        return this.isTimeSeries
      })
    },
    tradeSeriesType: {
      required: requiredIf(function () {
        return this.isTrade
      })
    },
    tradeVarType: {
      required: requiredIf(function () {
        return this.isTrade
      })
    },
    tradeFlow: {
      required: requiredIf(function () {
        return this.isTrade
      })
    },
    tradeCountry: {
      required: requiredIf(function () {
        return this.isTrade
      })
    },
    tradeProduct: {
      required: requiredIf(function () {
        return this.isTrade
      })
    },
    mapSeries: {
      required: requiredIf(function () {
        return this.isMap
      })
    }
  },
  methods: {
    async submitDataDownload() {
      this.$v.$touch()
      if (this.$v.$invalid) return

      this.isLoading = true
      this.downloadStatus = { type: "", message: "" }
      try {
        if (this.isTimeSeries) await this.downloadTimeSeries()
        if (this.isTrade) await this.downloadTrade()
        if (this.isMap) await this.downloadMap()
      } catch (error) {
        this.downloadStatus = {
          type: "error",
          message: this.$t("download-data.form.feedback.error")
        }
      } finally {
        this.isLoading = false
      }
    },
    async downloadTimeSeries() {
      const partners = Array.isArray(this.tsPartner)
        ? this.tsPartner
        : [this.tsPartner]
      const response = await this.$store.dispatch(
        "timeseries/findByFiltersMultiPartners",
        {
          flow: this.tsFlow.id,
          var: this.tsProduct.id,
          country: this.tsCountry.country,
          partner: partners.map((partner) => partner.id),
          dataType: this.tsDataType.id,
          varType: this.tsVarType.id
        }
      )
      const date = response?.diagMain?.date || []
      this.tsDates = date
      const byPartner = response?.diagMain?.byPartner || {}
      this.tsCsvTable = [
        partners
          .filter((partner) => Array.isArray(byPartner[partner.id]?.series))
          .map((partner) => ({
            partner: partner.descr,
            data: date.map((period, index) => ({
              field: this.formatPeriod(period),
              value: this.formatNumber(byPartner[partner.id].series[index])
            }))
          }))
      ]
      if (!this.tsCsvTable[0].length) return this.showEmptyResult()
      await this.exportCsv("timeSeriesExporter", this.tsCsvTable[0].length)
    },
    async downloadTrade() {
      await this.$store.dispatch("trade/findByName", {
        type: this.tradeVarType.id,
        seriesType: this.tradeSeriesType.id,
        country: this.tradeCountry.country,
        flow: this.tradeFlow.id
      })
      await this.$nextTick()
      if (!this.tradeCsvData.length) return this.showEmptyResult()
      await this.exportCsv("tradeExporter", this.tradeCsvData.length)
    },
    async downloadMap() {
      await this.$store.dispatch("geomap/findAll")
      await this.$store.dispatch("geomap/getSeries", this.mapSeries.value)
      this.mapCsvData = this.$store.getters["geomap/seriesData"] || []
      if (!this.mapCsvData.length) return this.showEmptyResult()
      await this.exportCsv("mapExporter", this.mapCsvData.length)
    },
    async exportCsv(refName, count) {
      await this.$nextTick()
      this.$refs[refName].download("csv")
      this.downloadStatus = {
        type: "success",
        message: this.$t("download-data.form.feedback.success", { count })
      }
    },
    showEmptyResult() {
      this.downloadStatus = {
        type: "warning",
        message: this.$t("download-data.form.feedback.empty")
      }
    },
    resetFilters() {
      this.seriesData = null
      this.applyDefaults()
      this.tsCsvTable = []
      this.tsDates = []
      this.mapCsvData = []
      this.downloadStatus = { type: "", message: "" }
      this.$v.$reset()
    },
    async applyDefaults() {
      const timeSeries = await metadataService.getTimeSeriesDefault()
      this.tsDataType = timeSeries.dataType
      this.tsVarType = timeSeries.varType
      this.tsFlow = timeSeries.flow
      this.tsCountry = timeSeries.country
      this.tsPartner = Array.isArray(timeSeries.partner)
        ? timeSeries.partner
        : [timeSeries.partner]
      this.tsProduct = timeSeries.productCPA

      const trade = await metadataService.getTradeDefault()
      this.tradeSeriesType = trade.seriesType
      this.tradeVarType = trade.varType
      this.tradeFlow = trade.flow
      this.tradeCountry = trade.country
      this.mapSeries = this.mapSeriesOptions[0]
      await this.$store.dispatch("trade/findByName", {
        type: trade.varType.id,
        seriesType: trade.seriesType.id,
        country: trade.country.country,
        flow: trade.flow.id
      })
      this.tradeProduct = trade.product
      this.$v.$reset()
    },
    formatPeriod(period) {
      const date = new Date(period)
      return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(
        2,
        "0"
      )}`
    },
    formatNumber(num) {
      return num ? num.toLocaleString(this.$i18n.locale) : "-"
    },
    fixLabelAccessibility() {
      setTimeout(() => {
        document.querySelectorAll("label").forEach((label) => {
          const search = label.querySelector(".vs__search")
          if (!search || !label.id) {
            return
          }
          search.setAttribute("aria-labelledby", label.id)
        })
      }, 300)
    },
    fixLanguageAccessibility() {
      setTimeout(() => {
        document.querySelectorAll(".vs__clear ").forEach((element) => {
          element.setAttribute("title", this.$t("common.clear_selected"))
          element.setAttribute("aria-label", this.$t("common.clear_selected"))
        })
      }, 300)
    },
    fixSelectAccessibility() {
      setTimeout(() => {
        document.querySelectorAll(".vs__dropdown-toggle").forEach((element) => {
          element.setAttribute("aria-label", this.$t("common.select_filter"))
        })
      }, 300)
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
    },
    fixMetaTitle() {
      setTimeout(() => {
        document.querySelectorAll("title").forEach((element) => {
          element.textContent = "Terra - " + this.$t("landing.timeseries.title")
        })
      }, 300)
    }
  },
  async created() {
    this.fixMetaTitle()
    this.fixASidebarMenu()
    await this.applyDefaults()
    this.fixLabelAccessibility()
    this.fixLanguageAccessibility()
    this.fixSelectAccessibility()
    this.$store.dispatch("coreui/setContext", Context.DownloadData)
  },
  mounted() {
    this.$store.dispatch("coreui/setContext", Context.DownloadData)
  }
}
</script>

<style scoped>
.download-page {
  width: min(100%, 1080px);
  padding: 0 0 2rem;
}

.download-heading {
  margin-bottom: 1rem;
}

.download-heading h2 {
  margin: 0 0 0.15rem;
  color: #25233a;
  font-size: clamp(1.25rem, 2.4vw, 1.55rem);
  font-weight: 700;
}

.download-heading p {
  margin: 0;
  color: #6b6a7b;
  font-size: 0.9rem;
}

.download-card {
  overflow: hidden;
  border: 1px solid #e5e4ee;
  border-radius: 1rem;
  background: #fff;
  box-shadow: 0 0.75rem 2.5rem rgba(35, 31, 65, 0.08);
}

.exporters {
  display: none;
}

.download-form__grid {
  display: grid;
}

.form-section {
  padding: 1.5rem 1.75rem;
  border-bottom: 1px solid #eeedf4;
}

.form-section:last-child {
  border-bottom: 0;
}

.form-section__title {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  margin-bottom: 1.15rem;
  color: #343247;
  font-size: 0.82rem;
  font-weight: 700;
  letter-spacing: 0.04em;
  text-transform: uppercase;
}

.form-section__title span {
  display: inline-grid;
  width: 1.65rem;
  height: 1.65rem;
  place-items: center;
  border-radius: 50%;
  background: #eeebff;
  color: #321fdb;
  font-size: 0.75rem;
}

.form-section__grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 1rem 1.25rem;
}

.form-section__grid--source {
  grid-template-columns: minmax(0, 2fr) minmax(12rem, 1fr);
}

.form-field {
  min-width: 0;
  margin: 0;
}

.form-field--full {
  grid-column: 1 / -1;
}

.month-input {
  width: 100%;
  height: 2.65rem;
  margin-top: 0.45rem;
  padding: 0 0.75rem;
  border: 1px solid #d8d6e3;
  border-radius: 0.55rem;
  background: #fff;
  color: #302e3d;
  font: inherit;
  font-weight: 500;
  transition: border-color 0.15s ease, box-shadow 0.15s ease;
}

.month-input:focus {
  border-color: #6554e8;
  box-shadow: 0 0 0 0.2rem rgba(50, 31, 219, 0.12);
  outline: 0;
}

.download-actions {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 0.75rem;
  padding: 1.25rem 1.75rem;
  background: #f8f8fb;
}

.download-status {
  flex: 1;
  margin: 0 auto 0 0;
  font-size: 0.88rem;
  font-weight: 600;
}

.download-status--success {
  color: #1d6f42;
}

.download-status--warning {
  color: #8a5b00;
}

.download-status--error {
  color: #b02a37;
}

.download-actions .btn:disabled {
  cursor: not-allowed;
}

.form-field :deep(.v-select) {
  margin-top: 0.45rem;
}

@media (min-width: 900px) {
  .form-section--measure .form-section__grid {
    grid-template-columns: repeat(3, minmax(0, 1fr));
  }
}

@media (max-width: 767px) {
  .download-page {
    padding-top: 0;
  }

  .form-section {
    padding: 1.25rem;
  }

  .form-section__grid,
  .form-section__grid--source {
    grid-template-columns: 1fr;
  }

  .download-actions {
    padding: 1rem 1.25rem;
  }
}

@media (max-width: 480px) {
  .download-actions {
    align-items: stretch;
    flex-direction: column-reverse;
  }

  .download-status {
    margin: 0.25rem 0;
    text-align: center;
  }

  .download-actions .btn {
    width: 100%;
  }
}
</style>
