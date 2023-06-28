<template>
  <div class="row">
    <div class="col-sm-6 col-md-9">
      <CCard>
        <CCardHeader>
          <span class="card-title">
            {{ $t("trade.card.title") }} {{ title }}
          </span>

          <span class="btn-group float-right">
            <span>
              <exporter
                v-if="this.charts && this.tradePeriod"
                tabindex="0"
                filename="terra_basket"
                :data="getData(this.charts.data, 'trade')"
                :filter="getSearchFilter()"
                source="matrix"
                :timePeriod="this.tradePeriod">
              </exporter>
            </span>
            <CButton
              color="link"
              size="sm"
              @click="helpOn(true)"
              tabindex="0"
              class="float-right"
              >Info</CButton
            >
          </span>
        </CCardHeader>
        <CCardBody>
          <circle-spin v-if="!this.chartData" class="circle-spin"></circle-spin>
          <line-chart
            :chartData="chartData"
            :options="options"
            :height="600"
            id="trade"
            ref="trade" />
        </CCardBody>
      </CCard>
    </div>
    <div class="col-sm-6 col-md-3">
      <CCard class="card-filter">
        <CCardHeader>
          <span class="card-filter-title">{{ $t("trade.form.title") }} </span>
        </CCardHeader>
        <CCardBody>
          <label aria-labelledby="input__1" class="card-label col-12"
            >{{ $t("trade.form.fields.seriesType") }}
            <v-select
              label="descr"
              :options="seriesTypes"
              :placeholder="$t('trade.form.fields.seriesType_placeholder')"
              v-model="seriesType" />
          </label>
          <label aria-labelledby="input__2" class="card-label mt-3 col-12"
            >{{ $t("trade.form.fields.varType") }}
            <v-select
              label="descr"
              :options="varTypes"
              :placeholder="$t('trade.form.fields.varType_placeholder')"
              v-model="varType" />
          </label>
          <label aria-labelledby="input__3" class="card-label mt-3 col-12"
            >{{ $t("trade.form.fields.flow") }}
            <v-select
              label="descr"
              :options="flows"
              :placeholder="$t('trade.form.fields.flow_placeholder')"
              v-model="flow" />
          </label>
          <label aria-labelledby="input__4" class="card-label mt-3 col-12"
            >{{ $t("trade.form.fields.country") }}
            <v-select
              label="name"
              :options="countries"
              :placeholder="$t('trade.form.fields.country_placeholder')"
              v-model="country" />
          </label>
          <label
            aria-labelledby="input__5"
            v-if="products"
            class="card-label mt-3 col-12"
            >{{ $t("trade.form.fields.products") }}
            <v-select
              v-if="products"
              label="displayName"
              :options="products"
              :placeholder="$t('trade.form.fields.products_placeholder')"
              multiple
              v-model="product"
              ref="prod" />
          </label>
          <CButton
            color="primary"
            shape="square"
            size="sm"
            @click="handleSubmit"
            class="mt-3 ml-3"
            >{{ $t("common.submit") }}
          </CButton>
        </CCardBody>
      </CCard>
    </div>
    <CModal
      :title="$t('trade.modal.main.title')"
      :show.sync="isModalHelp"
      size="lg"
      ><p v-html="$t('trade.modal.main.body')"></p>
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
import { Context, optionsTrade } from "@/common"
import { metadataService } from "@/services"
import paletteMixin from "@/components/mixins/palette.mixin"
import LineChart from "@/components/charts/LineChart"
import spinnerMixin from "@/components/mixins/spinner.mixin"
import exporter from "@/components/Exporter"

export default {
  name: "Trade",
  components: { LineChart, exporter },
  mixins: [paletteMixin, spinnerMixin],
  data: () => ({
    //Form (default values)
    idAllProducts: "",
    product: null,
    seriesType: null,
    varType: null,
    country: null,
    flow: null,

    //Chart
    chartData: null,
    labelPeriod: [],
    options: { ...optionsTrade },

    //Spinner
    spinner: false,
    isModalHelp: false
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
    ...mapGetters("metadata", ["tradePeriod"]),
    ...mapGetters("coreui", ["language"]),
    ...mapGetters("classification", [
      "seriesTypes",
      "varTypes",
      "countries",
      "flows"
    ]),
    ...mapGetters("trade", ["charts", "products"]),
    title() {
      return this.flow && this.country
        ? this.flow.descr + " - " + this.country.name
        : ""
    }
  },
  methods: {
    helpOn(showModal) {
      this.isModalHelp = showModal
    },
    handleSubmit() {
      if (this.varType && this.country && this.flow) {
        this.spinnerStart(true)
        this.$store
          .dispatch("trade/findByName", {
            type: this.varType.id,
            seriesType: this.seriesType.id,
            country: this.country.country,
            flow: this.flow.id
          })
          .then(() => {
            this.chartData = {}
            this.chartData.datasets = []
            this.chartData.labels = this.labelPeriod
            this.product.forEach((product) => {
              if (product.id === "00") {
                this.charts.data.forEach((element) => {
                  this.buildChartObject(element.dataname, element.value)
                })
              } else {
                this.buildChartObject(
                  this.charts.data[product.id].dataname,
                  this.charts.data[product.id].value
                )
              }
            })
          })
        this.clearColor()
        this.spinnerStart(true)
      }
    },
    buildChartObject(description, value) {
      const color = this.getColor()
      //reset options to default (to force update)
      this.options = { ...optionsTrade }

      this.options.scales.yAxes[0].scaleLabel.labelString =
        this.seriesType.id == 1
          ? this.$t("trade.plot.share")
          : this.$t("trade.plot.label")
      this.chartData.datasets.push({
        label: description,
        fill: false,
        backgroundColor: color.background,
        borderColor: color.border,
        data: value,
        showLine: true,
        pointRadius: 2
      })
    },
    getData(data, id) {
      if (data != null && this.product != null) {
        let selectedAll = false
        const selectedProds = this.product.map((prod) => {
          if (prod.id == "00") selectedAll = true
          return prod.dataname
        })
        //filter on selected products
        if (selectedAll) return [data, id]
        else {
          const selectedData = data.filter((series) => {
            if (selectedProds.includes(series.dataname)) return series
          })
          return [selectedData, id]
        }
      }
      return null
    },
    loadData() {
      this.spinnerStart(true)
      if (this.tradePeriod !== null) {
        this.labelPeriod = []
        for (const period of this.tradePeriod) {
          this.labelPeriod.push(period.name)
        }
      }
      this.$store.dispatch("coreui/setContext", Context.Trade)

      //Set form default values
      metadataService
        .getTradeDefault()
        .then(
          ({ idAllProducts, seriesType, varType, flow, country, product }) => {
            this.idAllProducts = idAllProducts
            this.seriesType = seriesType
            this.varType = varType
            this.flow = flow
            this.country = country
            this.product = product

            this.$store
              .dispatch("trade/findByName", {
                type: this.varType.id,
                seriesType: this.seriesType.id,
                country: this.country.country,
                flow: this.flow.id
              })
              .then(() => {
                this.chartData = {}
                this.chartData.datasets = []
                this.chartData.labels = this.labelPeriod
                this.charts.data.forEach((element) => {
                  this.buildChartObject(element.dataname, element.value)
                })
              })

            this.spinnerStart(false)
          }
        )
    },
    getSearchFilter() {
      let data = []
      data.push({
        field: this.$t("trade.download.title"),
        value: ""
      })
      data.push({
        field: this.$t("trade.form.fields.varType"),
        value: this.varType ? this.varType.descr : ""
      })
      data.push({
        field: this.$t("trade.form.fields.country"),
        value: this.country ? this.country.name : ""
      })
      data.push({
        field: this.$t("trade.form.fields.flow"),
        value: this.flow ? this.flow.descr : ""
      })
      data.push({
        field: this.$t("timeseries.form.fields.productsCPA"),
        value: this.product
          ? this.product
              .map((prod) => {
                return prod.dataname
              })
              .join("#")
          : ""
      })
      data.push({
        field: this.$t("common.start_date"),
        value: this.tradePeriod ? this.tradePeriod[0].isoDate : ""
      })
      data.push({
        field: this.$t("common.end_date"),
        value: this.tradePeriod
          ? this.tradePeriod[this.tradePeriod.length - 1].isoDate
          : ""
      })
      return data
    },
    spinnerStart(bool) {
      this.spinner = bool
    },
    fixLabelAccessibility() {
      setTimeout(() => {
        document.querySelectorAll("label > *").forEach((element, index) => {
          const i = index + 1
          element
            .getElementsByClassName("vs__search")[0]
            .setAttribute("id", "input__" + i)
        })
      }, 300)
    }
  },
  created() {
    this.loadData()
    this.fixLabelAccessibility()
  }
}
</script>
<style scoped>
.align-right {
  text-align: right;
}
</style>
