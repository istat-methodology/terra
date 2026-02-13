<template>
  <div class="row">
    <h1 class="sr-only">{{ $t("common.acronym") }}</h1>
    <div class="col-sm-12 col-md-10">
      <h3>{{ $t("landing.download.title") }}</h3>
    </div>
    <div class="col-sm-12 col-md-10">
      <div class="card" :title="$t('landing.download.body')">
        <header class="card-header" role="heading" aria-level="2">
          <CIcon
            name="cilCloudDownload"
            :title="$t('landing.download.body')"
            alt="Download" />{{ $t("landing.download.body") }}
        </header>
        <div class="card-body col-sm-12 col-md-12 mt-1">
          <form class="form" @submit.prevent="onSubmit">
            <div class="row">
              <label
                id="label__seriesData"
                class="card-label col-8 mt-1"
                :title="$t('landing.download.form.fields.seriesData')"
                >{{ $t("landing.download.form.fields.seriesData") }}
                <v-select
                  label="descr"
                  :options="getSeriesData"
                  :placeholder="
                    $t('landing.download.form.fields.seriesData_placeholder')
                  "
                  v-model="seriesData"
                  :class="{
                    'is-invalid': $v.seriesData.$error
                  }"
                  :clearable="false" />
              </label>
              <label
                id="label__period"
                class="card-label col-2 mt-1 pl-0"
                :title="$t('landing.download.form.fields.period')">
                {{ $t("landing.download.form.fields.period") }}
                <input
                  type="month"
                  v-model="period"
                  class="p-1"
                  :class="{ 'is-invalid': $v.period.$error }" />
              </label>
            </div>
            <div class="row">
              <label
                id="label__flow"
                class="card-label col-2 mt-1"
                :title="$t('landing.download.form.fields.flow')">
                {{ $t("landing.download.form.fields.flow") }}
                <v-select
                  label="descr"
                  :options="flows"
                  :placeholder="
                    $t('landing.download.form.fields.flow_placeholder')
                  "
                  v-model="flow"
                  :class="{
                    'is-invalid': $v.flow.$error
                  }"
                  :clearable="false" />
              </label>
              <label
                id="label__criterion"
                class="card-label col-3 mt-1 pl-0"
                :title="$t('landing.download.form.fields.criterion')">
                {{ $t("landing.download.form.fields.criterion") }}
                <v-select
                  v-model="criterion"
                  label="label"
                  :options="getCriterion"
                  :reduce="(opt) => opt.value"
                  :clearable="false" />
              </label>
              <label
                id="label__productClass"
                class="card-label col-3 mt-1 pl-0"
                :title="$t('landing.download.form.fields.productsClass')">
                {{ $t("landing.download.form.fields.productsClass") }}
                <v-select
                  name="selectProductClass"
                  v-model="productClass"
                  label="descr"
                  :options="getProductsClass"
                  :reduce="(opt) => opt.value"
                  :class="{
                    'is-invalid': $v.productClass.$error
                  }"
                  :clearable="false" />
              </label>
              <!-- Transport (solo NSTR) -->
              <label
                v-if="productClass === 'nstr'"
                id="label__transport"
                class="card-label col-4 mt-1 pl-0"
                :title="$t('landing.download.form.fields.transports')">
                {{ $t("landing.download.form.fields.transports") }}
                <v-select
                  v-model="transport"
                  multiple
                  label="descr"
                  :options="transports"
                  :clearable="false" />
              </label>
            </div>
            <div class="row">
              <label
                id="label__productCPA"
                class="card-label col-12 mt-1"
                :title="$t('landing.download.form.fields.productsCPA')">
                {{ $t("landing.download.form.fields.productsCPA") }}
                <v-select
                  label="descr"
                  :options="productsCPA"
                  :placeholder="
                    $t('landing.download.form.fields.productsCPA_placeholder')
                  "
                  v-model="productCPA"
                  :class="{
                    'is-invalid': $v.productCPA.$error
                  }"
                  :clearable="false" />
              </label>
            </div>
            <div class="row">
              <label
                id="label__country"
                class="card-label col-6 mt-1"
                :title="$t('landing.download.form.fields.country')">
                {{ $t("landing.download.form.fields.country") }}
                <v-select
                  label="name"
                  :options="countries"
                  :placeholder="
                    $t('landing.download.form.fields.country_placeholder')
                  "
                  v-model="country"
                  :class="{
                    'is-invalid': $v.country.$error
                  }"
                  :clearable="false" />
              </label>
              <label
                id="label__partner"
                class="card-label col-6 mt-1 pl-0"
                :title="$t('landing.download.form.fields.partner')">
                {{ $t("landing.download.form.fields.partner") }}
                <v-select
                  id="selectPartner"
                  name="selectPartner"
                  label="descr"
                  multiple
                  :options="partners"
                  :placeholder="
                    $t('landing.download.form.fields.partner_placeholder')
                  "
                  v-model="partner"
                  :class="{
                    'is-invalid': $v.partner.$error
                  }"
                  :clearable="false" />
              </label>
            </div>
            <div class="actions">
              <button type="button" class="btn secondary" @click="resetFilters">
                Reset filtri
              </button>
              <button
                type="button"
                class="btn primary"
                :disabled="isDownloading"
                @click="submitDataDownload">
                <span v-if="!isDownloading">Scarica dati</span>
                <span v-else>Preparazione download...</span>
              </button>
            </div>
          </form>
          <!--p>Result: {{ getPeriod }}</p>
          <p v-if="result">{{ result }}</p-->
        </div>
      </div>
    </div>
    <div class="col-sm-12 col-md-10">
      <h3>Analisi dati COMEXT</h3>
    </div>
    <div class="col-sm-12 col-md-10">
      <div class="card" :title="$t('landing.map.title')">
        <header class="card-header" role="heading" aria-level="2">
          <CIcon
            name="cil-location-pin"
            :title="$t('landing.map.title')"
            alt="" />{{ $t("landing.map.title") }}
        </header>
        <div class="card-body">
          <p v-html="$t('landing.map.body')"></p>
          <p class="section-link">
            <a
              @click="handleMap"
              @keypress="handleMap"
              tabindex="0"
              :title="$t('landing.map.link')">
              {{ $t("landing.map.link") }}
            </a>
          </p>
        </div>
      </div>
    </div>
    <div class="col-sm-12 col-md-10">
      <div class="card" :title="$t('landing.graph.extra-ue.title')">
        <header class="card-header" role="heading" aria-level="2">
          <CIcon
            name="cil-graph"
            :title="$t('landing.graph.extra-ue.title')"
            alt="" />
          {{ $t("landing.graph.extra-ue.title") }}
        </header>
        <div class="card-body">
          <p v-html="$t('landing.graph.extra-ue.body')"></p>
          <p class="section-link">
            <a
              @click="handleGraphExtraUe()"
              @keypress="handleGraphExtraUe()"
              tabindex="0"
              :title="$t('landing.graph.extra-ue.link')"
              >{{ $t("landing.graph.extra-ue.link") }}
            </a>
          </p>
        </div>
      </div>
    </div>
    <div class="col-sm-12 col-md-10">
      <div class="card" :title="$t('landing.graph.intra-ue.title')">
        <header class="card-header" role="heading" aria-level="2">
          <CIcon
            name="cil-graph"
            :title="$t('landing.graph.intra-ue.title')"
            alt="" />
          {{ $t("landing.graph.intra-ue.title") }}
        </header>
        <div class="card-body">
          <p v-html="$t('landing.graph.intra-ue.body')"></p>
          <p class="section-link">
            <a
              @click="handleGraphIntraUe()"
              @keypress="handleGraphIntraUe()"
              tabindex="0"
              :title="$t('landing.graph.intra-ue.link')">
              {{ $t("landing.graph.intra-ue.link") }}
            </a>
          </p>
        </div>
      </div>
    </div>
    <div class="col-sm-12 col-md-10">
      <div class="card" :title="$t('landing.timeseries.title')">
        <header class="card-header" role="heading" aria-level="2">
          <CIcon
            name="cil-chart-line"
            :title="$t('landing.timeseries.title')"
            alt="" />
          {{ $t("landing.timeseries.title") }}
        </header>
        <div class="card-body">
          <p v-html="$t('landing.timeseries.body')"></p>
          <p class="section-link">
            <a
              @click="handleTimeSeries()"
              @keypress="handleTimeSeries()"
              tabindex="0"
              :title="$t('landing.timeseries.link')">
              {{ $t("landing.timeseries.link") }}
            </a>
          </p>
        </div>
      </div>
    </div>
    <div class="col-sm-12 col-md-10">
      <div class="card" :title="$t('landing.trade.title')">
        <header class="card-header" role="heading" aria-level="2">
          <CIcon name="cil-layers" :title="$t('landing.trade.title')" alt="" />
          {{ $t("landing.trade.title") }}
        </header>
        <div class="card-body">
          <p v-html="$t('landing.trade.body')"></p>
          <p class="section-link">
            <a
              @click="handleTrade()"
              @keypress="handleTrade()"
              tabindex="0"
              :title="$t('landing.trade.link')">
              {{ $t("landing.trade.link") }}
            </a>
          </p>
        </div>
      </div>
    </div>
    <div class="col-sm-12 col-md-10">
      <h3>News</h3>
    </div>
    <div class="col-sm-12 col-md-10">
      <div class="card" :title="$t('landing.news.title')">
        <header class="card-header" role="heading" aria-level="2">
          <CIcon
            name="cil-newspaper"
            :title="$t('landing.news.title')"
            alt="" />
          {{ $t("landing.news.title") }}
        </header>
        <div class="card-body">
          <p v-html="$t('landing.news.body')"></p>
          <p class="section-link">
            <a
              @click="handleNews()"
              @keypress="handleNews()"
              tabindex="0"
              :title="$t('landing.news.link')">
              {{ $t("landing.news.link") }}
            </a>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import { mapGetters } from "vuex"
import { Context } from "@/common"
import { metadataService } from "@/services"
import { required } from "vuelidate/lib/validators"
import spinnerMixin from "@/components/mixins/spinner.mixin"

export default {
  name: "Home",

  mixins: [spinnerMixin],
  data: () => ({
    spinner: false,
    /* Form fields */
    seriesData: null,
    period: null,
    minPeriod: "2010-01",
    maxPeriod: "2035-12",
    flow: null,
    criterion: null,
    productClass: null,
    transport: null,
    productCPA: null,
    country: null,
    partner: null,

    /* Form fields */
    partnersArr: [],
    labelPeriod: [],
    isDownloading: false,
    result: null,
    //Dati NSTR per specifico declarant-partner per tutti i trasporti
    CASE_1: {
      product_class: "nstr",
      period: "202505",
      country: "IT",
      partner: "AL",
      product: "011",
      flow: 2,
      criterion: 1,
      transport: []
    },
    //Dati NSTR per specifico declarant-partner per specifici tipi di trasporto
    CASE_2: {
      product_class: "nstr",
      period: "202505",
      country: "IT",
      partner: "AL",
      product: "011",
      flow: 1,
      criterion: 2,
      transport: [1]
    },
    //Come CASO 1 ma invece che lista vuota viene passato null
    CASE_3: {
      product_class: "nstr",
      period: "202505",
      country: "IT",
      partner: "AL",
      product: "011",
      flow: 1,
      criterion: 2,
      transport: null
    },
    //Come CASO 1 ma invece che lista vuota non viene passato il parametro
    CASE_4: {
      product_class: "nstr",
      period: "202505",
      country: "IT",
      partner: "AL",
      product: "011",
      flow: 1,
      criterion: 2
    },
    //prodotti CPA di uno specifico caso
    CASE_5: {
      product_class: "cpa",
      period: "202505",
      country: "IT",
      partner: "ES",
      product: "00",
      flow: 1,
      criterion: 2
    },

    //prodotti CPA prendendo tutti i prodotti
    CASE_6: {
      product_class: "cpa",
      period: "202505",
      country: "IT",
      partner: "ES",
      product: null,
      flow: 1,
      criterion: 2
    },
    //come CASO 6 ma invece di null non viene passato il parametro
    CASE_7: {
      product_class: "cpa",
      period: "202505",
      country: "IT",
      partner: "ES",
      flow: 1,
      criterion: 2
    },
    //prodotti CPA specifico prodotto con tutti i partner
    CASE_8: {
      product_class: "cpa",
      period: "202505",
      country: "IT",
      partner: null,
      product: "00",
      flow: 1,
      criterion: 2
    },
    //come CASO 8 ma invece di null non viene passato il parametro
    CASE_9: {
      product_class: "cpa",
      period: "202505",
      country: "IT",
      product: "00",
      flow: 1,
      criterion: 2
    }
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
      //"dataTypes",
      //"varTypes",
      "productsCPA",
      "transports",
      "productsIntra",
      "productsExtra"
    ]),
    ...mapGetters("timeseries", ["timeseriesCharts"]),
    getCriterion() {
      return [
        { value: 1, label: "Value" },
        { value: 2, label: "Quantity" }
      ]
    },
    getSeriesData() {
      return [
        { value: "01", descr: "dati Extra UE" },
        { value: "02", descr: "dati Mondo" },
        { value: "03", descr: "dati serie storiche" },
        { value: "04", descr: "dati paniere dei prodotti" }
      ]
    },
    getProductsClass() {
      return [
        { value: "nstr", descr: "NSTR" },
        { value: "cpa", descr: "CPA" }
      ]
    },
    options() {
      return this.getOptions(this.$i18n.locale)
    },
    getPartners() {
      if (Array.isArray(this.chartData)) {
        return this.chartData.map((p) => p.descr).join(", ")
      }
      return ""
    }
  },

  // Parametri obbligatori :
  // seriesData,
  // period,
  // flow,
  // criterion,
  // product_class,
  // product,
  // country,
  // partner

  validations: {
    seriesData: {
      required
    },
    period: {
      required
    },
    criterion: {
      required
    },
    flow: {
      required
    },
    productClass: {
      required
    },
    productCPA: {
      required
    },
    country: {
      required
    },
    partner: {
      required
    }
  },
  methods: {
    getPeriod() {
      return (this.period || "").replace("-", "") // "202501"
    },
    buildDownloadPayload() {
      const partner = Array.isArray(this.partner)
        ? this.partner.map((p) => p.id)
        : this.partner?.id ?? null
      const transport = Array.isArray(this.transport)
        ? this.transport.map((t) => t.id)
        : this.transport?.id ?? null
      return {
        seriesData: this.seriesData?.value ?? null,
        period: this.getPeriod(this.period),
        flow: this.flow?.id ?? null,
        criterion: this.criterion,
        productClass: this.productClass,
        transport: transport,
        product: this.productCPA?.id ?? null,
        country: this.country?.country ?? null,
        partner: partner
      }
    },

    async download() {
      this.isDownloading = true
      try {
        const payload_build = this.buildDownloadPayload()
        console.log("Download payload:", payload_build)
        const payload = this.CASE_1
        console.log("Using test payload:", payload)
        this.result = await this.$store.dispatch("download/fetchData", payload)
      } finally {
        this.isDownloading = false
      }
    },
    submitDataDownload() {
      return this.download()
    },

    resetFilters() {
      this.seriesData = null
      this.period = null
      this.flow = null
      this.criterion = null
      this.productClass = null
      this.transport = []
      this.productCPA = null
      this.country = null
      this.partner = null
      this.partnersArr = []
      this.labelPeriod = []
      this.result = null
      this.$v.$reset()
    },
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
        !this.$v.seriesData.$invalid &&
        !this.$v.period.$invalid &&
        !this.$v.flow.$invalid &&
        !this.$v.criterion.$invalid &&
        !this.$v.productClass.$invalid &&
        !this.$v.country.$invalid &&
        !this.$v.partner.$invalid
      ) {
        this.spinnerStart(true)
        this.setPartners() // fills this.partnersArr

        const form = {
          seriesData: this.seriesData.value,
          period: this.period.replace("-", ""),
          flow: this.flow.id,
          criterion: this.criterion.value,
          productClass: this.productClass,
          transport: this.product_class === "nstr" ? this.transport : null,
          product: this.productCPA.id,
          country: this.country.country,
          partner: this.partnersArr.map((p) => p.id) // send array of partner ids
        }
        this.$store
          .dispatch("timeseries/fetchData", form)
          .then(() => {
            this.spinnerStart(false)
          })
          .catch(() => {
            this.spinnerStart(false)
          })
      }
    },

    loadData() {
      this.$store.dispatch("coreui/setContext", Context.Policy)
      //Set form default values
      metadataService
        .getTimeSeriesDefault()
        .then(({ flow, country, partner, productCPA }) => {
          this.flow = flow
          this.country = country
          this.partner = partner
          this.productCPA = productCPA
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
        field: this.$t("landing.download.form.fields.seriesData"),
        value: this.seriesData ? this.eriesData.descr : ""
      })
      data.push({
        field: this.$t("landing.download.form.fields.period"),
        value: this.period ? this.period.descr : ""
      })
      data.push({
        field: this.$t("landing.download.form.fields.flow"),
        value: this.flow ? this.flow.descr : ""
      })
      data.push({
        field: this.$t("landing.download.form.fields.criterion"),
        value: this.criterion ? this.criterion.descr : ""
      })
      data.push({
        field: this.$t("landing.download.form.fields.productClass"),
        value: this.productClass ?? ""
      })
      if (this.product_class === "nstr") {
        data.push({
          field: this.$t("landing.download.form.fields.transports"),
          value: this.transport ? this.transport.descr : ""
        })
      }
      data.push({
        field: this.$t("landing.download.form.fields.productsCPA"),
        value: this.productCPA ? this.productCPA.descr : ""
      })
      data.push({
        field: this.$t("landing.download.form.fields.country"),
        value: this.country ? this.country.name : ""
      })
      data.push({
        field: this.$t("landing.download.form.fields.partner"),
        value: this.getPartners
      })
      return data
    },
    getTabularData(data, partner, date) {
      if (!Array.isArray(data)) {
        console.warn("getTabularData: 'data' is not an array", data)
        return null
      }

      if (!Array.isArray(date)) {
        console.warn("getTabularData: 'date' is not an array", date)
        return null
      }
      console.log(partner)

      const table = []

      date.forEach((tp, index) => {
        const dt = new Date(tp)
        const year = dt.getFullYear()
        const month = String(dt.getMonth() + 1).padStart(2, "0")
        table.push({
          field: `${year}-${month}`,
          value: this.formatNumber(data[index])
        })
      })

      return [
        {
          partner: partner,
          data: table
        }
      ]
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
    },

    onSubmit() {
      this.handleSubmit()
    },
    handleHome() {
      this.$router.push({ name: "Home" })
    },
    handleMap() {
      this.$router.push({ name: "Map" })
    },
    handleGraphExtraUe() {
      this.$router.push({ name: "GraphExtraUe" })
    },
    handleGraphIntraUe() {
      this.$router.push({ name: "GraphIntraUe" })
    },
    handleTimeSeries() {
      this.$router.push({ name: "TimeSeries" })
    },
    handleTrade() {
      this.$router.push({ name: "Trade" })
    },
    handleNews() {
      this.$router.push({ name: "News" })
    }
    /*
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
    */
    /*  
    fixMetaTitle() {
      setTimeout(() => {
        document.querySelectorAll("title").forEach((element) => {
          element.textContent = "Terra - Home"
        })
      }, 300)
    }
   */
  },

  created() {
    this.$store.dispatch("coreui/setContext", Context.Home)
    this.fixMetaTitle()
    this.fixASidebarMenu()
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
.card-filter .card-body {
  padding-left: 0.5rem;
}

.material-design-icon > .material-design-icon__svg {
  bottom: -0.17rem;
}

.card-body {
  padding-bottom: 0.5rem;
}

a {
  text-decoration: underline;
}

a:not([href]) {
  background-color: transparent;
  color: #321fdb;
}

a:not([href]):hover {
  text-decoration: underline;
  cursor: pointer;
}

.filters-form {
  max-width: 500px;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.field {
  display: flex;
  flex-direction: column;
}

label {
  font-weight: 600;
  margin-bottom: 0.25rem;
}

select,
button {
  padding: 0.4rem;
}
</style>
