<template>
  <div class="row">
    <h1 class="sr-only">
      {{ $t("landing.timeseries.title") }}
    </h1>

    <div class="col-12 col-xl-9">
      <CCard
        :title="
          country && partner
            ? 'TERRA - ' +
              $t('timeseries.card.title') +
              ': ' +
              country.name +
              ' - ' +
              partner.descr
            : 'TERRA - ' +
              $t('timeseries.card.title') +
              ' - ' +
              $t('timeseries.card.comext')
        ">
        <CCardHeader>
          <span class="card-title" role="heading" aria-level="2">
            <span v-if="country && partner"
              >{{ dataType.descr }}: {{ country.name }} -
              {{ getPartners }}</span
            >
            <span v-else
              >{{ $t("timeseries.card.title") }} -
              {{ $t("timeseries.card.comext") }}</span
            >
          </span>
          <span class="btn-group float-right">
            <exporter
              v-if="getPartners"
              filename="terra_timeseries"
              :data="[csvTable, 'timeseries']"
              :header="timeseriesHeaders"
              :options="['jpeg', 'png', 'pdf', 'csv']"
              source="table">
            </exporter>
          </span>
        </CCardHeader>
        <CCardBody v-if="isMainChart">
          <circle-spin v-if="spinner" class="circle-spin"></circle-spin>
          <line-chart
            aria-hidden="true"
            :chartData="chartDataDiagMain"
            :options="options"
            :key="chartKey"
            id="timeseries" />
          <div v-if="provisionalWarning" class="timeseries-info" role="status">
            {{ provisionalWarning }}
          </div>
        </CCardBody>
      </CCard>
    </div>
    <div class="col-12 col-xl-3">
      <CCard class="card-filter" :title="$t('timeseries.form.title')">
        <CCardHeader>
          <span class="card-filter-title" role="heading" aria-level="2">{{
            $t("timeseries.form.title")
          }}</span>
        </CCardHeader>
        <CCardBody>
          <label
            id="label__1"
            class="card-label col-12"
            :title="$t('timeseries.form.fields.dataType')"
            >{{ $t("timeseries.form.fields.dataType") }}
            <v-select
              label="descr"
              :options="dataTypes"
              :placeholder="$t('timeseries.form.fields.dataType_placeholder')"
              v-model="dataType"
              :class="{
                'is-invalid': $v.dataType.$error
              }"
              :clearable="false" />
          </label>
          <label
            id="label__2"
            class="card-label col-12 mt-2"
            :title="$t('timeseries.form.fields.varType')">
            {{ $t("timeseries.form.fields.varType") }}
            <v-select
              label="descr"
              :options="varTypes"
              :placeholder="$t('timeseries.form.fields.varType_placeholder')"
              v-model="varType"
              :class="{
                'is-invalid': $v.varType.$error
              }"
              :clearable="false" />
          </label>
          <label
            id="label__3"
            class="card-label col-12 mt-2"
            :title="$t('timeseries.form.fields.flow')">
            {{ $t("timeseries.form.fields.flow") }}
            <v-select
              label="descr"
              :options="flowsTs"
              :placeholder="$t('timeseries.form.fields.flow_placeholder')"
              v-model="flow"
              :class="{
                'is-invalid': $v.flow.$error
              }"
              :clearable="false" />
          </label>
          <label
            id="label__4"
            class="card-label col-12 mt-2"
            :title="$t('timeseries.form.fields.country')">
            {{ $t("timeseries.form.fields.country") }}
            <v-select
              label="name"
              :options="countries"
              :placeholder="$t('timeseries.form.fields.country_placeholder')"
              v-model="country"
              :class="{
                'is-invalid': $v.country.$error
              }"
              :clearable="false" />
          </label>
          <label
            id="label__5"
            class="card-label col-12 mt-2"
            :title="$t('timeseries.form.fields.partner')">
            {{ $t("timeseries.form.fields.partner") }}
            <v-select
              id="selectPartner"
              name="selectPartner"
              label="descr"
              multiple
              :options="partners"
              :placeholder="$t('timeseries.form.fields.partner_placeholder')"
              v-model="partner"
              :class="{
                'is-invalid': $v.partner.$error
              }"
              :clearable="false" />
          </label>
          <label
            id="label__6"
            class="card-label col-12 mt-2"
            :title="$t('timeseries.form.fields.productsCPA')">
            {{ $t("timeseries.form.fields.productsCPA") }}
            <v-select
              label="descr"
              :options="productsCPA"
              :placeholder="
                $t('timeseries.form.fields.productsCPA_placeholder')
              "
              v-model="productCPA"
              :class="{
                'is-invalid': $v.productCPA.$error
              }"
              :clearable="false" />
          </label>
          <CButton
            color="primary"
            shape="square"
            size="sm"
            @click="handleSubmit"
            class="mt-2 ml-3"
            :title="$t('common.submit')"
            >{{ $t("common.submit") }}</CButton
          >
        </CCardBody>
      </CCard>
    </div>
    <CModal
      :title="$t('timeseries.modal.main.title')"
      :show.sync="isModalHelp"
      size="lg">
      <p v-html="$t('timeseries.modal.main.body')"></p>
      <template #footer>
        <CButton color="primary" shape="square" size="sm" @click="helpOn(false)"
          >Close</CButton
        >
      </template>
    </CModal>
  </div>
</template>
<script>
import { mapGetters } from "vuex"
import {
  buildTimeseriesCsvRows,
  Context,
  filterAnomalousLastPeriod,
  getTimeseriesHeaders,
  PROVISIONAL_LAST_VALUE_THRESHOLD,
  Status
} from "@/common"
import { metadataService } from "@/services"
import paletteMixin from "@/components/mixins/palette.mixin"
import timeseriesDiagMixin from "@/components/mixins/timeseriesDiag.mixin"
import timeseriesMixin from "@/components/mixins/timeseries.mixin"
import LineChart from "@/components/charts/LineChart"
import { required } from "vuelidate/lib/validators"
import spinnerMixin from "@/components/mixins/spinner.mixin"
import exporter from "@/components/Exporter"

export default {
  name: "TimeSeries",
  components: {
    //ScatterChart,
    LineChart,
    exporter
  },
  mixins: [paletteMixin, timeseriesDiagMixin, timeseriesMixin, spinnerMixin],
  data: () => ({
    chartKey: 0,
    //Spinner
    spinner: false,

    //Form fields
    dataType: null,
    varType: null,
    flow: null,
    country: null,
    partner: null,
    productCPA: null,

    partnersArr: [],
    chartData: [],
    csvTable: [],

    //Charts
    chartDataDiagMain: null,
    labelPeriod: [],
    isMainChart: true,
    isModalHelp: false,
    provisionalWarning: ""
  }),
  watch: {
    language() {
      this.$store.dispatch("message/success", this.$t("common.update_cls"))
      this.$store.dispatch("classification/getClassifications").then(() => {
        this.loadData()
        this.fixLanguageAccessibility()
        this.fixMetaTitle()
      })
    }
  },
  computed: {
    ...mapGetters("coreui", ["language"]),
    ...mapGetters("classification", [
      "loaded",
      "countries",
      "partners",
      "flowsTs",
      "dataTypes",
      "varTypes",
      "productsCPA"
    ]),
    ...mapGetters("timeseries", [
      "timeseriesCharts",
      "statusMain",
      "statusACF",
      "statusNorm"
    ]),
    options() {
      return this.getOptions(
        this.statusMain != "00" ? true : false,
        this.$i18n.locale
      )
    },
    getPartners() {
      if (Array.isArray(this.chartData)) {
        return this.chartData.map((p) => p.descr).join(", ")
      }
      return ""
    },
    timeseriesHeaders() {
      return getTimeseriesHeaders(this.varType)
    }
  },
  validations: {
    dataType: {
      required
    },
    varType: {
      required
    },
    flow: {
      required
    },
    country: {
      required
    },
    partner: {
      required
    },
    productCPA: {
      required
    }
  },
  methods: {
    helpOn(showModal) {
      this.isModalHelp = showModal
    },
    handleMainChart() {
      this.isMainChart = !this.isMainChart
    },
    handleDiagNorm() {
      this.isDiagNorm = !this.isDiagNorm
    },
    handleDiagACF() {
      this.isDiagACF = !this.isDiagACF
    },
    setPartners() {
      this.partnersArr = Array.isArray(this.partner)
        ? this.partner
        : [this.partner]
    },
    handleSubmit() {
      this.$v.$touch()

      if (
        !this.$v.dataType.$invalid &&
        !this.$v.varType.$invalid &&
        !this.$v.flow.$invalid &&
        !this.$v.productCPA.$invalid &&
        !this.$v.country.$invalid &&
        !this.$v.partner.$invalid
      ) {
        this.spinnerStart(true)
        this.provisionalWarning = ""
        this.setPartners() // fills this.partnersArr
        this.chartData = []

        const form = {
          flow: this.flow.id,
          var: this.productCPA.id,
          country: this.country.country,
          partner: this.partnersArr.map((p) => p.id), // send array of partner ids
          dataType: this.dataType.id,
          varType: this.varType.id
        }

        this.$store
          .dispatch("timeseries/findByFiltersMultiPartners", form)
          .then((response) => {
            if (
              response.statusMain === Status.success &&
              response.diagMain?.byPartner
            ) {
              const filteredResult = filterAnomalousLastPeriod({
                dates: response.diagMain.date,
                byPartner: response.diagMain.byPartner,
                partnerIds: this.partnersArr.map((partner) => partner.id)
              })
              const byPartner = filteredResult.byPartner
              const date = filteredResult.dates
              if (filteredResult.removed) {
                this.provisionalWarning = this.$t(
                  "timeseries.message.provisionalExcluded",
                  {
                    period: this.getDate([filteredResult.removedDate])[0],
                    threshold: PROVISIONAL_LAST_VALUE_THRESHOLD * 100
                  }
                )
              }
              this.labelPeriod = date

              this.chartDataDiagMain = {
                labels: this.getDate(date),
                datasets: []
              }

              this.partnersArr.forEach((p) => {
                const partnerData = byPartner[p.id]
                if (partnerData && partnerData.series) {
                  this.buildChartObject(p.descr, partnerData.series)
                  this.chartData.push({
                    id: p.id,
                    descr: p.descr,
                    series: partnerData.series,
                    date: date
                  })
                }
              })

              if (filteredResult.removed && this.partnersArr.length === 1) {
                this.addAverageReferenceLine(
                  filteredResult.referenceAverage,
                  date.length
                )
              }

              if (this.chartDataDiagMain.datasets.length > 0) {
                this.csvTable = buildTimeseriesCsvRows({
                  country: this.country,
                  partners: this.partnersArr,
                  flow: this.flow,
                  product: this.productCPA,
                  dataType: this.dataType,
                  varType: this.varType,
                  dates: date,
                  byPartner
                })
              } else {
                this.chartDataDiagMain = this.emptyChart()
                this.$store.dispatch(
                  "message/warning",
                  this.$t("timeseries.message.empty")
                )
              }

              this.chartKey += 1 // force re-render
            } else {
              this.chartDataDiagMain = this.emptyChart()
              this.$store.dispatch(
                "message/warning",
                this.$t("timeseries.message.empty")
              )
              this.chartKey += 1
            }
          })
          .finally(() => {
            this.spinnerStart(false)
          })
      }
    },
    buildChartObject(description, value) {
      if (!Array.isArray(value) || value.length === 0) {
        console.warn("Skipped dataset due to empty series:", description)
        return
      }
      const color = this.getColor()
      this.chartDataDiagMain.datasets.push({
        label: description,
        fill: false,
        backgroundColor: color.background,
        borderColor: color.border,
        borderWidth: 2,
        data: value,
        showLine: true,
        lineTension: 0,
        pointRadius: 3,
        pointBackgroundColor: color.border,
        pointBorderColor: color.border,
        pointBorderWidth: 0,
        pointHoverRadius: 5,
        borderDash: [0, 0]
      })
    },
    addAverageReferenceLine(value, length) {
      if (!Number.isFinite(value)) return

      this.chartDataDiagMain.datasets.push({
        label: this.$t("timeseries.plot.previousAverage"),
        data: Array(length).fill(value),
        fill: false,
        borderColor: "#4f5d73",
        backgroundColor: "#4f5d73",
        borderWidth: 1.5,
        borderDash: [6, 4],
        pointRadius: 0,
        pointHoverRadius: 0,
        lineTension: 0
      })
    },
    loadData() {
      this.$store.dispatch("coreui/setContext", Context.Policy)
      //Set form default values
      metadataService
        .getTimeSeriesDefault()
        .then(({ dataType, varType, flow, country, partner, productCPA }) => {
          this.dataType = dataType
          this.varType = varType
          this.flow = flow
          this.country = country
          this.partner = partner
          this.productCPA = productCPA
          //Submit form
          this.handleSubmit()
        })
    },
    removeData(chart) {
      chart.data.labels.pop()
      chart.data.datasets.forEach((dataset) => {
        dataset.data.pop()
      })
      chart.update()
    },
    getData(data, id) {
      if (data != null) {
        return [data, id]
      }
      return null
    },
    getSearchFilter() {
      let data = []
      data.push({
        field: this.$t("timeseries.download.title"),
        value: ""
      })
      data.push({
        field: this.$t("timeseries.form.fields.dataType"),
        value: this.dataType ? this.dataType.descr : ""
      })
      data.push({
        field: this.$t("timeseries.form.fields.varType"),
        value: this.varType ? this.varType.descr : ""
      })
      data.push({
        field: this.$t("timeseries.form.fields.flow"),
        value: this.flow ? this.flow.descr : ""
      })
      data.push({
        field: this.$t("timeseries.form.fields.country"),
        value: this.country ? this.country.name : ""
      })
      data.push({
        field: this.$t("timeseries.form.fields.partner"),
        value: this.getPartners
      })
      data.push({
        field: this.$t("timeseries.form.fields.productsCPA"),
        value: this.productCPA ? this.productCPA.descr : ""
      })

      data.push({
        field: this.$t("common.start_date"),
        //value: this.timeseriesCharts
        //  ? this.timeseriesCharts.diagMain.date[0]
        //  : ""
        value: this.timeseriesCharts?.diagMain?.date?.[0] ?? ""
      })
      data.push({
        field: this.$t("common.end_date"),
        //value: this.timeseriesCharts
        //  ? this.timeseriesCharts.diagMain.date[
        //     this.timeseriesCharts.diagMain.date.length - 1
        //    ]
        //  : ""
        value:
          this.timeseriesCharts?.diagMain?.date?.[
            this.timeseriesCharts?.diagMain?.date?.length - 1
          ] ?? ""
      })

      return data
    },
    formatNumber(num) {
      return num ? num.toLocaleString(this.$i18n.locale) : "-"
    },
    fixLabelAccessibility() {
      setTimeout(() => {
        document.querySelectorAll("label > *").forEach((element, index) => {
          const i = index + 1
          element
            .getElementsByClassName("vs__search")[0]
            .setAttribute("aria-labelledby", "label__" + i)
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
    spinnerStart(bool) {
      this.spinner = bool
    },
    clearChart() {
      document.getElementById("timeseries").removeChild("canvas")
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
  created() {
    this.loadData()
    this.fixMetaTitle()
    this.fixLabelAccessibility()
    this.fixLanguageAccessibility()
    this.fixSelectAccessibility()
    this.fixASidebarMenu()
  }
}
</script>
<style scoped>
.timeseries-info {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  margin: 0.75rem 0 0 2.5em;
  color: #4f5d73;
  font-size: 0.875rem;
}

.card-filter .card-body {
  padding-left: 0.5rem;
}

@media (min-width: 768px) and (max-width: 1199.98px) {
  .card-filter .card-body {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 1rem;
    padding: 1rem;
  }

  .card-filter .card-label {
    margin-top: 0 !important;
    padding: 0;
  }

  .card-filter .btn {
    align-self: end;
    justify-self: start;
    margin: 0 !important;
  }
}
</style>
