<template>
  <div class="row">
    <h1 class="sr-only">
      {{ $t("landing.timeseries.title") }}
    </h1>

    <div class="col-sm-6 col-md-9">
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
              >{{ $t("timeseries.card.title") }}: {{ country.name }} -
              {{ partner.descr }}</span
            >
            <span v-else
              >{{ $t("timeseries.card.title") }} -
              {{ $t("timeseries.card.comext") }}</span
            >
          </span>
          <span class="btn-group float-right">
            <exporter
              v-if="timeseriesCharts"
              filename="terra_timeseries"
              :data="getTabularData(timeseriesCharts.diagMain, 'timeseries')"
              :filter="getSearchFilter()"
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
            id="timeseries" />
          <div class="timeseries-info">
            <span>
              <span class="text-primary" v-if="mean">
                {{ $t("common.mean") }}: </span
              >{{ mean }}
              <span class="text-primary" v-if="std"
                >{{ $t("common.std") }}: </span
              >{{ std }}
            </span>
          </div>
        </CCardBody>
      </CCard>
      <!--CCard v-if="chartDataDiagNorm">
        <CCardHeader>
          <span class="card-title">
            {{ this.diagNormTitle }}
          </span>
          <span class="btn-help">
            <CButton color="link" size="sm" @click="helpOn(true)">Info</CButton>
          </span>
          <span class="float-right">
            <exporter
              filename="Terra_diagnorm"
              :data="getData(chartDataDiagNorm, 'diagnorm')">
            </exporter>
          </span>
        </CCardHeader>
        <CCardBody v-if="isDiagNorm">
          <scatter-chart
            :chartData="chartDataDiagNorm"
            :options="optionsNorm"
            id="diagnorm" />
        </CCardBody>
      </CCard-->
      <!--CCard v-if="chartDataDiagACF">
        <CCardHeader>
          <span class="card-title">
            {{ this.diagACFTitle }}
          </span>
          <span class="btn-help">
            <CButton color="link" size="sm" @click="helpOn(true)">Info</CButton>
          </span>
          <span class="float-right">
            <exporter
              filename="Terra_diagacf"
              :data="getData(chartDataDiagACF, 'diagacf')">
            </exporter>
          </span>
        </CCardHeader>
        <CCardBody v-if="isDiagACF">
          <line-chart
            :chartData="chartDataDiagACF"
            :options="optionsACF"
            id="diagacf" />
        </CCardBody>
      </CCard-->
    </div>
    <div class="col-sm-6 col-md-3">
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
              :options="flows"
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
import { Context, Status } from "@/common"
import { metadataService } from "@/services"
import paletteMixin from "@/components/mixins/palette.mixin"
import timeseriesDiagMixin from "@/components/mixins/timeseriesDiag.mixin"
import timeseriesMixin from "@/components/mixins/timeseries.mixin"
//import ScatterChart from "@/components/charts/ScatterChart"
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
    //Spinner
    spinner: false,

    //Form fields
    dataType: null,
    varType: null,
    flow: null,
    country: null,
    partner: null,
    productCPA: null,

    //Charts
    chartDataDiagMain: null,
    chartDataDiagNorm: null,
    chartDataDiagACF: null,

    isMainChart: true,
    isDiagNorm: true,
    isDiagACF: true,
    isModalHelp: false,
    mean: null,
    std: null
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
      "flows",
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
        const form = {
          flow: this.flow.id,
          var: this.productCPA.id,
          country: this.country.country,
          partner: this.partner.id,
          dataType: this.dataType.id,
          varType: this.varType.id
        }
        this.spinnerStart(true)
        this.$store.dispatch("timeseries/findByFilters", form).then(() => {
          if (this.statusMain == Status.success) {
            this.buildTimeseriesCharts(
              this.timeseriesCharts,
              this.dataType.descr,
              this.statusMain,
              this.$i18n.locale
            )
            this.optionsNorm.scales.yAxes[0].scaleLabel.labelString = this.$t(
              "timeseries.plot.qqnormy"
            )
            this.optionsNorm.scales.xAxes[0].scaleLabel.labelString = this.$t(
              "timeseries.plot.qqnormx"
            )
          } else {
            this.chartDataDiagMain = this.emptyChart()
            this.mean = null
            this.std = null
            this.chartDataDiagNorm = null
            this.chartDataDiagACF = null
            this.$store.dispatch(
              "message/warning",
              this.$t("timeseries.message.empty")
            )
          }
          this.spinnerStart(false)
        })
      }
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
          //Sumit form
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
        value: this.partner ? this.partner.descr : ""
      })
      data.push({
        field: this.$t("timeseries.form.fields.productsCPA"),
        value: this.productCPA ? this.productCPA.descr : ""
      })
      data.push({
        field: this.$t("common.start_date"),
        value: this.timeseriesCharts
          ? this.timeseriesCharts.diagMain.date[0]
          : ""
      })
      data.push({
        field: this.$t("common.end_date"),
        value: this.timeseriesCharts
          ? this.timeseriesCharts.diagMain.date[
              this.timeseriesCharts.diagMain.date.length - 1
            ]
          : ""
      })
      return data
    },
    getTabularData(data, id) {
      if (data != null) {
        const table = []
        const timePoints = data.date
        const values = data.series
        if (timePoints)
          timePoints.forEach((tp, index) => {
            const dt = new Date(tp)
            const year = dt.getFullYear()
            const month = dt.getMonth() + 1
            table.push({
              field: year + "-" + month,
              value: this.formatNumber(values[index])
            })
          })
        return [table, id]
      }
      return null
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
  margin-left: 2.5em;
  margin-top: 0.4em;
  font-size: small;
}

.card-filter .card-body {
  padding-left: 0.5rem;
}
</style>
