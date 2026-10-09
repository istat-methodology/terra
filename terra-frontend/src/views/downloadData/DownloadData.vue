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
                class="card-label form-field form-field--span-2">
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
                class="card-label form-field form-field--span-2">
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

          <div v-if="isComext" class="form-section form-section--measure">
            <div class="form-section__title">
              <span>2</span>
              {{ $t("download-data.form.sections.filters") }}
            </div>
            <div class="form-section__grid">
              <label id="label__comextYearFrom" class="card-label form-field">
                {{ $t("download-data.form.fields.yearFrom") }}
                <v-select
                  v-model="comextYearFrom"
                  label="descr"
                  :options="comextYearOptions"
                  :class="{ 'is-invalid': $v.comextYearFrom.$error }"
                  :clearable="false" />
              </label>
              <label id="label__comextMonthFrom" class="card-label form-field">
                {{ $t("download-data.form.fields.monthFrom") }}
                <v-select
                  v-model="comextMonthFrom"
                  label="descr"
                  :options="comextMonthFromOptions"
                  :class="{ 'is-invalid': $v.comextMonthFrom.$error }"
                  :clearable="false" />
              </label>
              <label id="label__comextYearTo" class="card-label form-field">
                {{ $t("download-data.form.fields.yearTo") }}
                <v-select
                  v-model="comextYearTo"
                  label="descr"
                  :options="comextYearOptions"
                  :class="{ 'is-invalid': $v.comextYearTo.$error }"
                  :clearable="false" />
              </label>
              <label id="label__comextMonthTo" class="card-label form-field">
                {{ $t("download-data.form.fields.monthTo") }}
                <v-select
                  v-model="comextMonthTo"
                  label="descr"
                  :options="comextMonthToOptions"
                  :class="{ 'is-invalid': $v.comextMonthTo.$error }"
                  :clearable="false" />
              </label>
              <label id="label__comextFlow" class="card-label form-field">
                {{ $t("download-data.form.fields.flow") }}
                <v-select
                  v-model="comextFlow"
                  label="descr"
                  :options="flowsTs"
                  :class="{ 'is-invalid': $v.comextFlow.$error }"
                  :clearable="false" />
              </label>
              <label id="label__comextCountry" class="card-label form-field">
                {{ $t("download-data.form.fields.country") }}
                <v-select
                  v-model="comextCountry"
                  label="name"
                  :options="countries"
                  :class="{ 'is-invalid': $v.comextCountry.$error }"
                  :clearable="false" />
              </label>
              <label id="label__comextPartner" class="card-label form-field">
                {{ $t("download-data.form.fields.partner") }}
                <v-select
                  v-model="comextPartner"
                  label="descr"
                  :options="partners"
                  :class="{ 'is-invalid': $v.comextPartner.$error }"
                  :clearable="false" />
              </label>
              <label id="label__comextProduct" class="card-label form-field">
                {{ $t("download-data.form.fields.productsCPA") }}
                <v-select
                  v-model="comextProduct"
                  label="descr"
                  :options="productsCPA"
                  :class="{ 'is-invalid': $v.comextProduct.$error }"
                  :clearable="false" />
              </label>
              <label id="label__comextCriterion" class="card-label form-field">
                {{ $t("download-data.form.fields.criterion") }}
                <input
                  type="text"
                  class="form-control"
                  :value="$t('download-data.form.options.valueEuros')"
                  disabled />
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
            :data="[tsCsvTable, '']"
            :header="timeseriesHeaders"
            :options="['csv']"
            source="table" />
          <exporter
            v-if="isTrade && tradeCsvData.length"
            ref="tradeExporter"
            filename="terra_basket"
            :data="[tradeCsvData, '']"
            :header="tradeHeaders"
            :options="['csv']"
            source="table" />
          <exporter
            v-if="isMap && mapCsvData.length"
            ref="mapExporter"
            filename="terra_mapseries"
            :data="[mapCsvData, '']"
            :header="mapHeaders"
            :options="['csv']"
            source="table" />
          <exporter
            v-if="isComext && comextData.length"
            ref="comextExporter"
            :filename="comextFilename"
            :data="[comextData, '']"
            :header="comextHeaders"
            :options="['csv']"
            source="table" />
        </div>
      </form>
    </div>
  </div>
</template>
<script>
import { mapGetters } from "vuex"
import {
  buildMapCsvRows,
  buildTradeCsvRows,
  buildTimeseriesCsvRows,
  Context,
  getMapHeaders,
  getTradeHeaders,
  getTimeseriesHeaders
} from "@/common"
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
    comextYearFrom: null,
    comextMonthFrom: null,
    comextYearTo: null,
    comextMonthTo: null,
    comextFlow: null,
    comextCountry: null,
    comextPartner: null,
    comextProduct: null,
    comextData: [],
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
    },
    comextYearFrom() {
      if (
        this.comextMonthFrom &&
        !this.comextMonthFromOptions.some(
          (month) => month.id === this.comextMonthFrom.id
        )
      ) {
        this.comextMonthFrom = null
      }
    },
    comextYearTo() {
      if (
        this.comextMonthTo &&
        !this.comextMonthToOptions.some(
          (month) => month.id === this.comextMonthTo.id
        )
      ) {
        this.comextMonthTo = null
      }
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
    isComext() {
      return this.seriesData?.value === "06"
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
      if (this.isComext) {
        return Boolean(
          this.comextPeriodFrom &&
            this.comextPeriodTo &&
            this.isComextPeriodRangeValid &&
            this.comextFlow &&
            this.comextCountry &&
            this.comextPartner &&
            this.comextProduct
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
        },
        {
          value: "06",
          descr: this.$t("download-data.form.options.comext")
        }
      ]
    },
    comextHeaders() {
      return [
        "DECLARANT_ISO",
        "DECLARANT_NAME",
        "PARTNER_ISO",
        "PARTNER_NAME",
        "FLOW_CODE",
        "FLOW_LABEL",
        "PRODUCT_CODE",
        "PRODUCT_DESCRIPTION",
        "PRODUCT_LEVEL",
        "PERIOD",
        "YEAR",
        "MONTH",
        "VALUE_IN_EUROS"
      ]
    },
    timeseriesHeaders() {
      return getTimeseriesHeaders(this.tsVarType)
    },
    mapHeaders() {
      return getMapHeaders()
    },
    mapFlow() {
      const flowId = this.mapSeries?.value === "importseries" ? 1 : 2
      return this.flowsTs.find((flow) => flow.id === flowId)
    },
    comextAvailablePeriods() {
      return Array.isArray(this.tradePeriod) ? this.tradePeriod : []
    },
    comextYearOptions() {
      const years = [
        ...new Set(
          this.comextAvailablePeriods.map((period) => period.id.slice(0, 4))
        )
      ]
      return years.reverse().map((year) => ({ id: year, descr: year }))
    },
    comextMonthFromOptions() {
      return this.getComextMonthOptions(this.comextYearFrom)
    },
    comextMonthToOptions() {
      return this.getComextMonthOptions(this.comextYearTo)
    },
    comextPeriodFrom() {
      return this.comextYearFrom && this.comextMonthFrom
        ? `${this.comextYearFrom.id}${this.comextMonthFrom.id}`
        : ""
    },
    comextPeriodTo() {
      return this.comextYearTo && this.comextMonthTo
        ? `${this.comextYearTo.id}${this.comextMonthTo.id}`
        : ""
    },
    isComextPeriodRangeValid() {
      return (
        Boolean(this.comextPeriodFrom && this.comextPeriodTo) &&
        this.comextPeriodFrom <= this.comextPeriodTo
      )
    },
    comextFilename() {
      const flow = this.comextFlow?.id === 1 ? "import" : "export"
      const period =
        this.comextPeriodFrom === this.comextPeriodTo
          ? this.comextPeriodFrom
          : `${this.comextPeriodFrom}_${this.comextPeriodTo}`
      return `terra_comext_${flow}_${period}`
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
      return buildTradeCsvRows({
        country: this.tradeCountry,
        partnerName: this.$t("download-data.form.options.allPartners"),
        flow: this.tradeFlow,
        selectedProducts: this.tradeProduct,
        products: this.tradeCharts?.data,
        seriesType: this.tradeSeriesType,
        varType: this.tradeVarType,
        periods: this.tradeTimePeriod
      })
    },
    tradeHeaders() {
      return getTradeHeaders(this.tradeSeriesType, this.tradeVarType)
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
    },
    comextYearFrom: {
      required: requiredIf(function () {
        return this.isComext
      })
    },
    comextMonthFrom: {
      required: requiredIf(function () {
        return this.isComext
      })
    },
    comextYearTo: {
      required: requiredIf(function () {
        return this.isComext
      })
    },
    comextMonthTo: {
      required: requiredIf(function () {
        return this.isComext
      })
    },
    comextFlow: {
      required: requiredIf(function () {
        return this.isComext
      })
    },
    comextCountry: {
      required: requiredIf(function () {
        return this.isComext
      })
    },
    comextPartner: {
      required: requiredIf(function () {
        return this.isComext
      })
    },
    comextProduct: {
      required: requiredIf(function () {
        return this.isComext
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
        if (this.isComext) await this.downloadComext()
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
      this.tsCsvTable = buildTimeseriesCsvRows({
        country: this.tsCountry,
        partners,
        flow: this.tsFlow,
        product: this.tsProduct,
        dataType: this.tsDataType,
        varType: this.tsVarType,
        dates: date,
        byPartner
      })
      if (!this.tsCsvTable.length) return this.showEmptyResult()
      await this.exportCsv("timeSeriesExporter", this.tsCsvTable.length)
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
      await this.$store.dispatch("geomap/getSeries", this.mapSeries.value)
      const { rows, removedPeriod } = buildMapCsvRows({
        series: this.$store.getters["geomap/seriesData"],
        flow: this.mapFlow,
        getCountryName: this.$store.getters["classification/getCountryName"]
      })
      this.mapCsvData = rows
      if (!this.mapCsvData.length) return this.showEmptyResult()
      await this.exportCsv("mapExporter", this.mapCsvData.length)
      if (removedPeriod) {
        this.downloadStatus.message += ` ${this.$t(
          "download-data.form.feedback.provisionalExcluded",
          { period: removedPeriod }
        )}`
      }
    },
    async downloadComext() {
      const response = await this.$store.dispatch("download/fetchData", {
        product_class: "cpa",
        period_from: this.comextPeriodFrom,
        period_to: this.comextPeriodTo,
        country: this.comextCountry.country,
        partner: this.comextPartner.id,
        product: this.comextProduct.id,
        flow: this.comextFlow.id,
        criterion: 1
      })
      this.comextData = Array.isArray(response)
        ? response.map((row) => this.enrichComextRow(row))
        : []
      if (!this.comextData.length) return this.showEmptyResult()
      await this.exportCsv("comextExporter", this.comextData.length)
    },
    enrichComextRow(row) {
      const productCode = String(row.PRODUCT ?? "")
      const product = this.productsCPA.find((item) => item.id === productCode)
      const period = String(row.PERIOD ?? "").padStart(6, "0")

      return {
        DECLARANT_ISO: row.DECLARANT_ISO,
        DECLARANT_NAME: this.getComextCountryName(row.DECLARANT_ISO),
        PARTNER_ISO: row.PARTNER_ISO,
        PARTNER_NAME: this.getComextCountryName(row.PARTNER_ISO),
        FLOW_CODE: row.FLOW,
        FLOW_LABEL: this.comextFlow?.descr || "",
        PRODUCT_CODE: productCode,
        PRODUCT_DESCRIPTION:
          product?.descr?.replace(`${productCode} - `, "") || "",
        PRODUCT_LEVEL: productCode === "00" ? 0 : productCode.length,
        PERIOD: row.PERIOD,
        YEAR: period.slice(0, 4),
        MONTH: period.slice(4, 6),
        VALUE_IN_EUROS: row.VALUE_IN_EUROS
      }
    },
    getComextCountryName(code) {
      if (!code) return this.$t("download-data.comext.partnerCodes.na")

      const country = this.countries.find((item) => item.country === code)
      if (country?.name) return country.name.trim()

      const partner = this.partners.find((item) => item.id === code)
      if (partner?.descr) return partner.descr.trim()

      return this.$t("download-data.comext.partnerCodes.na")
    },
    getComextMonthOptions(year) {
      if (!year) return []

      return this.comextAvailablePeriods
        .filter((period) => period.id.startsWith(year.id))
        .map((period) => {
          const month = period.id.slice(4, 6)
          const description = new Intl.DateTimeFormat(this.$i18n.locale, {
            month: "long"
          }).format(new Date(2000, Number(month) - 1, 1))
          return {
            id: month,
            descr: description.charAt(0).toUpperCase() + description.slice(1)
          }
        })
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
      this.comextData = []
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
      this.comextFlow = timeSeries.flow
      this.comextCountry = timeSeries.country
      this.comextPartner = Array.isArray(timeSeries.partner)
        ? timeSeries.partner[0]
        : timeSeries.partner
      this.comextProduct = timeSeries.productCPA
      const latestComextPeriod =
        this.comextAvailablePeriods[this.comextAvailablePeriods.length - 1]
      if (latestComextPeriod && !this.comextYearFrom) {
        const year = latestComextPeriod.id.slice(0, 4)
        const month = latestComextPeriod.id.slice(4, 6)
        this.comextYearFrom = { id: year, descr: year }
        this.comextYearTo = { id: year, descr: year }
        this.comextMonthFrom = this.comextMonthFromOptions.find(
          (option) => option.id === month
        )
        this.comextMonthTo = this.comextMonthToOptions.find(
          (option) => option.id === month
        )
      }
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
  overflow: visible;
  border: 1px solid #d8dbe0;
  border-radius: 0.25rem;
  background: #fff;
  box-shadow: 0 1px 1px 0 rgba(60, 75, 100, 0.14);
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

.download-actions {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 0.75rem;
  padding: 1.25rem 1.75rem;
  border-radius: 0 0 0.25rem 0.25rem;
  background: #fff;
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

  .form-field--span-2 {
    grid-column: span 2;
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
