<!-- babel-disable-file -->
<template>
  <div class="row">
    <h1 class="sr-only">{{ $t("landing.trade.title") }}</h1>
    <div class="col-12 col-xl-9">
      <CCard :title="'TERRA - ' + $t('trade.card.title') + title">
        <CCardHeader>
          <span class="card-title" role="heading" aria-level="2">
            {{ $t("trade.card.title") }} {{ title }}
          </span>
          <span class="btn-group float-right">
            <exporter
              v-if="
                this.charts && this.tradePeriod && this.tradeVariationPeriod
              "
              filename="terra_basket"
              :data="[tradeCsvData, 'trade']"
              :header="tradeHeaders"
              source="table"
              :options="['jpeg', 'png', 'pdf', 'csv']"
              :icon-trigger="true">
            </exporter>
            <!--CButton
              color="link"
              @click="helpOn(true)"
              tabindex="0"
              class="float-right"
              title="Info"
              >Info</CButton
            -->
          </span>
        </CCardHeader>
        <CCardBody>
          <circle-spin v-if="!this.chartData" class="circle-spin"></circle-spin>
          <line-chart
            aria-hidden="true"
            :chartData="chartData"
            :options="options"
            :height="720"
            id="trade"
            ref="trade" />
        </CCardBody>
      </CCard>
    </div>
    <div class="col-12 col-xl-3">
      <CCard class="card-filter" :title="$t('trade.form.title')">
        <CCardHeader>
          <span class="card-filter-title" role="heading" aria-level="2"
            >{{ $t("trade.form.title") }}
          </span>
        </CCardHeader>
        <CCardBody>
          <label
            id="label__1"
            class="card-label col-12"
            :title="$t('trade.form.fields.seriesType')"
            >{{ $t("trade.form.fields.seriesType") }}
            <v-select
              label="descr"
              :options="seriesTypes"
              :placeholder="$t('trade.form.fields.seriesType_placeholder')"
              v-model="seriesType"
              :clearable="false"
              :class="{
                'is-invalid': $v.seriesType.$error
              }" />
          </label>
          <label
            id="label__2"
            class="card-label mt-2 col-12"
            :title="$t('trade.form.fields.varType')"
            >{{ $t("trade.form.fields.varType") }}
            <v-select
              label="descr"
              :options="varTypes"
              :placeholder="$t('trade.form.fields.varType_placeholder')"
              v-model="varType"
              :clearable="false"
              :class="{
                'is-invalid': $v.varType.$error
              }" />
          </label>
          <label
            id="label__3"
            class="card-label mt-2 col-12"
            :title="$t('trade.form.fields.flow')"
            >{{ $t("trade.form.fields.flow") }}
            <v-select
              label="descr"
              :options="flows"
              :placeholder="$t('trade.form.fields.flow_placeholder')"
              v-model="flow"
              :clearable="false"
              :class="{
                'is-invalid': $v.flow.$error
              }" />
          </label>
          <label
            id="label__4"
            class="card-label mt-2 col-12"
            :title="$t('trade.form.fields.country')"
            >{{ $t("trade.form.fields.country") }}
            <v-select
              label="name"
              :options="countries"
              :placeholder="$t('trade.form.fields.country_placeholder')"
              v-model="country"
              :clearable="false"
              :class="{
                'is-invalid': $v.country.$error
              }" />
          </label>
          <label
            id="label__5"
            v-if="products"
            class="card-label mt-2 col-12"
            :title="$t('trade.form.fields.products')"
            >{{ $t("trade.form.fields.products") }}
            <v-select
              class="style-chooser"
              label="displayName"
              :options="products"
              :placeholder="$t('trade.form.fields.products_placeholder')"
              multiple
              required
              v-model="product"
              ref="prod"
              :class="{
                'is-invalid': $v.product.$error
              }"
              :aria-invalid="$v.product.$error ? 'true' : 'false'"
              :aria-describedby="
                $v.product.$error ? 'error-message-product' : null
              "
              :clearable="false" />
            <span
              v-if="$v.product.$error"
              id="error-message-product"
              class="error d-block"
              role="alert">
              {{ $t("trade.form.errors.product_required") }}
            </span>
          </label>
          <CButton
            color="primary"
            shape="square"
            size="sm"
            @click="handleSubmit"
            class="mt-2 ml-3"
            :title="$t('common.submit')"
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
//import { Context, optionsTrade } from "@/common"
import { buildTradeCsvRows, Context, getTradeHeaders } from "@/common"
import { metadataService } from "@/services"
import { required } from "vuelidate/lib/validators"
import paletteMixin from "@/components/mixins/palette.mixin"
import tradeDiagMixin from "@/components/mixins/tradeDiag.mixin"
import LineChart from "@/components/charts/LineChart"
import spinnerMixin from "@/components/mixins/spinner.mixin"
import exporter from "@/components/Exporter"
export default {
  name: "Trade",
  components: { LineChart, exporter },
  mixins: [paletteMixin, spinnerMixin, tradeDiagMixin],
  data: () => ({
    //Form (default values)

    idAllProducts: "",
    product: null,
    seriesType: null,
    varType: null,
    country: null,
    flow: null,
    submitStatus: "OK",
    //Chart
    chartData: null,
    labelPeriod: [],
    //options: { ...optionsTrade },

    //Spinner
    spinner: false,
    isModalHelp: false
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
    ...mapGetters("metadata", ["tradePeriod", "tradeVariationPeriod"]),
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
    },
    options() {
      return this.getOptions(true, this.$i18n.locale)
    },
    tradeTimePeriod() {
      return this.seriesType?.id == 1
        ? this.tradePeriod
        : this.tradeVariationPeriod
    },
    tradeCsvData() {
      return buildTradeCsvRows({
        country: this.country,
        partnerName: this.$t("download-data.form.options.allPartners"),
        flow: this.flow,
        selectedProducts: this.product,
        products: this.charts?.data,
        seriesType: this.seriesType,
        varType: this.varType,
        periods: this.tradeTimePeriod
      })
    },
    tradeHeaders() {
      return getTradeHeaders(this.seriesType, this.varType)
    }
  },
  validations: {
    flow: { required },
    product: { required },
    seriesType: { required },
    varType: { required },
    country: { required }
  },
  methods: {
    helpOn(showModal) {
      this.isModalHelp = showModal
    },
    handleSubmit() {
      this.$v.$touch() //validate form data
      if (
        !this.$v.seriesType.$invalid &&
        !this.$v.varType.$invalid &&
        !this.$v.country.$invalid &&
        !this.$v.product.$invalid &&
        !this.$v.flow.$invalid
      ) {
        this.submitStatus = "OK"
        this.spinnerStart(true)
        this.$store
          .dispatch("trade/findByName", {
            type: this.varType.id,
            seriesType: this.seriesType.id,
            country: this.country.country,
            flow: this.flow.id
          })
          .then(() => {
            // Build x axis
            if (
              this.tradePeriod !== null &&
              this.tradeVariationPeriod !== null
            ) {
              this.labelPeriod = []

              console.log("Series type: " + this.seriesType.id)

              const tradePer =
                this.seriesType.id == 1
                  ? this.tradePeriod
                  : this.tradeVariationPeriod
              for (const period of tradePer) {
                this.labelPeriod.push(period.name)
              }
            }

            this.chartData = {}
            this.chartData.datasets = []
            this.chartData.labels = this.labelPeriod
            this.product.forEach((product) => {
              if (product.id === "00") {
                this.charts.data.forEach((element, index) => {
                  this.buildChartObject(element.dataname, element.value, index)
                })
              } else {
                this.buildChartObject(
                  this.charts.data[product.id].dataname,
                  this.charts.data[product.id].value,
                  Number(product.id)
                )
              }
            })
          })
        this.spinnerStart(true)
      } else {
        this.submitStatus = "PENDING"
      }
    },
    buildChartObject(description, value, productIndex) {
      const color = this.getTradeColor(productIndex)
      //reset options to default (to force update)
      //this.options = { ...optionsTrade }

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
        let datacsv = []
        data.forEach((products) => {
          datacsv.push({
            dataname: products.dataname,
            productID: products.productID,
            value: this.setValue(products.value)
          })
        })
        let selectedAll = false
        const selectedProds = this.product.map((prod) => {
          if (prod.id == "00") selectedAll = true
          return prod.dataname
        })
        //filter on selected products
        //console.log(datacsv)
        if (selectedAll) return [datacsv, id]
        else {
          const selectedData = datacsv.filter((series) => {
            if (selectedProds.includes(series.dataname)) return series
          })
          return [selectedData, id]
        }
      }
      return null
    },
    setValue(values) {
      let productValues = []
      values.forEach((value) => {
        productValues.push(this.formatNumber(value))
      })
      return productValues
    },
    formatNumber(num) {
      return num ? num.toLocaleString(this.$i18n.locale) : "-"
    },
    loadData() {
      this.spinnerStart(true)
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
                // Build x axis
                if (
                  this.tradePeriod !== null &&
                  this.tradeVariationPeriod !== null
                ) {
                  this.labelPeriod = []

                  console.log("Series type: " + this.seriesType.id)

                  const tradePer =
                    this.seriesType.id == 1
                      ? this.tradePeriod
                      : this.tradeVariationPeriod
                  for (const period of tradePer) {
                    this.labelPeriod.push(period.name)
                  }
                }
                this.chartData = {}
                this.chartData.datasets = []
                this.chartData.labels = this.labelPeriod
                this.charts.data.forEach((element, index) => {
                  this.buildChartObject(element.dataname, element.value, index)
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
    fixLanguageAccessibility() {
      setTimeout(() => {
        document.querySelectorAll(".vs__clear ").forEach((element) => {
          element.setAttribute("title", this.$t("common.clear_selected"))
          element.setAttribute("aria-label", this.$t("common.clear_selected"))
        })
        document.querySelectorAll(".vs__deselect").forEach((element) => {
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
          element.textContent = "Terra - " + this.$t("landing.trade.title")
        })
      }, 300)
    },
    fixLabelSelectAccessibility() {
      setTimeout(() => {
        document.querySelectorAll(".vs__search").forEach((element, index) => {
          const i = index + 1
          element.setAttribute("aria-labelledby", "label__" + i)
        })
      }, 300)
    },
    fixLabelForSelectAccessibility() {
      setTimeout(() => {
        document.querySelectorAll(".vs__search").forEach((element, index) => {
          const i = index + 1
          if (i === 5) {
            element.setAttribute("id", "vs__input__" + i)
          }
        })
      }, 300)
    }
  },
  created() {
    this.loadData()
    this.fixLabelSelectAccessibility()
    this.fixLabelForSelectAccessibility()
    this.fixLanguageAccessibility()
    this.fixSelectAccessibility()
    this.fixASidebarMenu()
    this.fixMetaTitle()
    this.$v.$touch()
  }
}
</script>
<style scoped>
.card-title {
  font-size: 0.9375rem;
  font-weight: 600;
  line-height: 1.5;
}

.align-right {
  text-align: right;
}
.card-filter .card-body {
  padding-left: 0.5rem;
}
.error {
  margin-top: 0.25rem;
  color: #b00020;
  font-size: 0.8rem;
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
