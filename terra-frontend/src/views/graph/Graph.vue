<template>
  <div class="row">
    <div class="col-sm-6 col-md-9">
      <CTabs class="ctablist" variant="tabs" :active-tab="0">
        <CTab :title="$t('graph.card.title')">
          <h1 class="sr-only">{{ $t("graph.card.title") }}</h1>
          <cosmo-graph
            :title="$t('graph.card.title')"
            ref="cosmograph"
            :nodes="nodes"
            :edges="edges"
            :metrics="metrics"
            :spinner="spinner"
            :isIntra="isIntra"
            :displayTransport="!isIntra"
            :transports="transport"
            @applyConstraints="handleApplyConstraints"
            @showinfo="showMainModal">
            <cosmo-slider
              :interval="timeRange"
              :currentTime="currentTime"
              @change="handleTimeChange" />
          </cosmo-graph>
        </CTab>
        <CTab :title="$t('graph.table.title')">
          <h1 class="sr-only">{{ $t("graph.table.title") }}</h1>
          <CCard :title="$t('graph.table.title')">
            <CCardHeader>
              <span class="card-title">{{ title }}</span>
              <span class="btn-group float-right">
                <exporter
                  filename="terra_metrics"
                  :data="getData(csvFields, 'table')"
                  :options="['csv']"
                  :filter="getSearchFilter()"
                  source="table"
                  :header="csvHeader">
                </exporter>
                <!--CButton
                    color="link"
                    @click="showMainModal"
                    class="float-right"
                    title="Info"
                    tabindex="0"
                    >Info</CButton
                  -->
              </span>
            </CCardHeader>
            <CCardBody class="pb-1">
              <cosmo-table
                :data="metricsTable"
                :fields="metricsFields"
                :sorterValue="sorterValue" />
            </CCardBody>
          </CCard>
        </CTab>
      </CTabs>
    </div>
    <div class="col-sm-6 col-md-3 padding-tab">
      <CCard class="card-filter" :title="$t('graph.form.title')">
        <CCardHeader>
          <span class="card-title">{{ $t("graph.form.title") }}</span>
          <!--span class="btn-help">
              <CButton
                color="link"
                @click="showInfoModal"
                title="Info"
                tabindex="0"
                >Info</CButton
              >
            </span-->
        </CCardHeader>
        <CCardBody>
          <label
            for="montly"
            class="card-label mt-3 col-12"
            :title="$t('graph.form.fields.monthly_trimester')"
            >{{ $t("graph.form.fields.monthly_trimester") }}
            <div class="border rounded pl-2 pt-2">
              <label class="radio" :title="$t('graph.form.fields.monthly')">
                <input
                  id="montly"
                  type="radio"
                  name="radioPeriod"
                  value="Monthly"
                  v-model="frequency" />
                <span for="timerange">{{
                  $t("graph.form.fields.monthly")
                }}</span>
              </label>
              <label class="radio" :title="$t('graph.form.fields.trimester')">
                <input
                  id="trimester"
                  type="radio"
                  name="radioPeriod"
                  value="Trimester"
                  v-model="frequency" />
                <span>{{ $t("graph.form.fields.trimester") }}</span>
              </label>
            </div>
          </label>

          <label
            class="card-label mt-3 col-12"
            for="input__1"
            :title="$t('graph.form.fields.period')">
            {{ $t("graph.form.fields.period") }}
            <v-select
              v-if="timeRange"
              label="selectName"
              :options="timeRange"
              :placeholder="$t('graph.form.fields.period_placeholder')"
              v-model="currentTime"
              :class="{
                'is-invalid': $v.currentTime.$error
              }"
              :clearable="false" />
          </label>
          <label
            class="card-label mt-3 col-12"
            for="input__2"
            :title="$t('graph.form.fields.flow')"
            >{{ $t("graph.form.fields.flow") }}
            <v-select
              label="descr"
              :options="flows"
              :placeholder="$t('graph.form.fields.flow_placeholder')"
              v-model="flow"
              :class="{
                'is-invalid': $v.flow.$error
              }"
              :clearable="false" />
          </label>
          <label
            class="card-label mt-3 col-12"
            :title="$t('graph.form.fields.percentage')"
            >{{ $t("graph.form.fields.percentage") }}
            <CInput
              :placeholder="$t('graph.form.fields.percentage_placeholder')"
              v-model="percentage"
              :class="{
                'is-invalid': $v.percentage.$error
              }" />
          </label>
          <label
            class="card-label mt-3 col-12"
            for="input__3"
            :title="
              displayTransport
                ? $t('graph.form.fields.product_nstr')
                : $t('graph.form.fields.product_cpa3')
            "
            ><span v-if="displayTransport">{{
              $t("graph.form.fields.product_nstr")
            }}</span>
            <span v-else>{{ $t("graph.form.fields.product_cpa3") }}</span>
            <v-select
              label="descr"
              :options="products"
              :placeholder="$t('graph.form.fields.product_placeholder')"
              v-model="product"
              :class="{
                'is-invalid': $v.product.$error
              }"
              :clearable="false" />
          </label>
          <label
            class="card-label mt-3 col-12"
            for="input__4"
            :title="$t('graph.form.fields.transport')"
            v-if="displayTransport"
            >{{ $t("graph.form.fields.transport") }}
            <v-select
              class="style-chooser"
              v-if="displayTransport"
              label="descr"
              multiple
              :options="transports"
              :placeholder="$t('graph.form.fields.transport_placeholder')"
              v-model="transport"
              :class="{
                'is-invalid': $v.transport.$error
              }"
              :clearable="false" />
          </label>

          <div class="col-12">
            <CButton
              color="primary"
              shape="square"
              size="sm"
              @click="handleSubmit"
              class="mt-3"
              >{{ $t("common.submit") }}</CButton
            >
          </div>
        </CCardBody>
      </CCard>
    </div>
  </div>
</template>

<script>
import { mapGetters } from "vuex"
import { required, numeric } from "vuelidate/lib/validators"
import { metadataService } from "@/services"
import {
  Context,
  Status,
  getScenarioNodes,
  metricsFieldsIt,
  metricsFieldsEn,
  monthDefault,
  trimesterDefault,
  getCleanTransports,
  getTransportIds,
  restoreAllProdId
} from "@/common"
import Slider from "@/components/Slider"
import GraphVis from "@/views/graph/GraphVis"
import GraphTable from "@/views/graph/GraphTable"
//import GraphInfoModal from "@/views/graph/GraphInfoModal"
import exporter from "@/components/Exporter"

export default {
  name: "Graph",
  components: {
    "cosmo-slider": Slider,
    "cosmo-graph": GraphVis,
    "cosmo-table": GraphTable,
    //"cosmo-info-modal": GraphInfoModal,
    exporter
  },
  props: {
    isIntra: {
      type: Boolean,
      default: false
    }
  },
  data: () => ({
    //State
    displayTransport: true,
    currentTime: null,
    frequency: "",

    //Form fields
    percentage: 0,
    transport: null,
    product: null,
    flow: null,

    //Graph
    graphForm: null,

    //Metrics table
    metricsFieldsIt: [...metricsFieldsIt],
    metricsFieldsEn: [...metricsFieldsEn],
    sorterValue: { column: "vulnerability", asc: false },

    //Spinner
    spinner: false,

    //Modal
    isHelpModal: false,
    isMainModal: false
  }),
  watch: {
    language() {
      this.$store.dispatch("message/success", this.$t("common.update_cls"))
      this.$store.dispatch("classification/getClassifications").then(() => {
        this.loadData()
      })
    },
    frequency() {
      this.currentTime = this.isTrimester
        ? { id: trimesterDefault.id, selectName: trimesterDefault.descr }
        : { id: monthDefault.id, selectName: monthDefault.descr_it }
    }
  },
  computed: {
    ...mapGetters("metadata", ["graphPeriod", "graphTrimesterPeriod"]),
    ...mapGetters("coreui", ["isItalian", "language"]),
    ...mapGetters("graph", ["nodes", "edges", "metrics", "metricsTable"]),
    ...mapGetters("classification", [
      "transports",
      "productsIntra",
      "productsExtra",
      "flows"
    ]),
    isTrimester() {
      return this.frequency == "Monthly" ? false : true
    },
    timeRange() {
      return this.isTrimester ? this.graphTrimesterPeriod : this.graphPeriod
    },
    title() {
      return this.isIntra
        ? this.$t("graph.metricIntra")
        : this.$t("graph.metricExtra")
    },
    products() {
      return this.isIntra ? this.productsIntra : this.productsExtra
    },
    metricsFields() {
      return this.isItalian ? this.metricsFieldsIt : this.metricsFieldsEn
    },
    csvFields() {
      return this.metricsTable.map((field) => {
        return {
          label: field.label,
          name: field.name,
          vulnerability: field.vulnerability,
          hubness: field.hubness,
          exportStrenght: field.exportStrenght
        }
      })
    },
    csvHeader() {
      return this.metricsFields.map((field) => field.label)
    }
  },
  validations: {
    currentTime: {
      required
    },
    percentage: {
      required,
      numeric
    },
    transport: {
      validationRule(tr) {
        return this.displayTransport ? tr !== null : true
      }
    },
    product: {
      required
    },
    flow: {
      required
    }
  },
  methods: {
    handleTimeChange(time) {
      this.currentTime = time
      if (this.graphForm) {
        this.graphForm.tg_period = this.currentTime.id
        this.graphForm.pos = { nodes: this.nodes }
        this.requestToServer()
      }
    },
    handleApplyConstraints(constraints) {
      //console.log(constraints);
      this.$store.dispatch("message/info", this.$t("graph.message.scenario"))
      if (this.graphForm) {
        this.graphForm.pos = { nodes: getScenarioNodes(this.nodes) }
        this.graphForm.selezioneMezziEdges = constraints
        this.requestToServer()
      }
    },
    handleSubmit() {
      //Save selected transports for scenario analysis
      //this.transport = form.transports

      this.$v.$touch() //validate form data
      if (
        !this.$v.currentTime.$invalid &&
        !this.$v.percentage.$invalid &&
        !this.$v.transport.$invalid &&
        !this.$v.product.$invalid &&
        !this.$v.flow.$invalid
      ) {
        //Manage "all" transports in the select (if select is displayed)
        var cleanTransports = []
        var cleanTransportIds = []
        if (this.displayTransport) {
          cleanTransports = getCleanTransports(this.transport, this.transports)
          cleanTransportIds = getTransportIds(cleanTransports)
        }
        this.graphForm = {
          tg_period: this.currentTime.id,
          tg_perc: this.percentage,
          listaMezzi: cleanTransportIds,
          product: restoreAllProdId(this.product),
          flow: this.flow.id,
          weight_flag: true,
          pos: "None",
          selezioneMezziEdges: "None"
        }
        this.requestToServer()
      }
    },
    requestToServer() {
      this.spinnerStart(true)

      this.$store
        .dispatch(
          this.isIntra ? "graph/postGraphIntra" : "graph/postGraphExtra",
          {
            form: this.graphForm,
            trimester: this.isTrimester
          }
        )
        .then((status) => {
          if (status == Status.wide) {
            this.$store.dispatch(
              "message/error",
              this.$t("graph.message.graph_wide")
            )
          } else if (status == Status.empty) {
            this.$store.dispatch(
              "message/error",
              this.$t("graph.message.graph_empty")
            )
          } else {
            this.$store.dispatch(
              "message/success",
              this.$t("common.data_updated")
            )
            this.$refs.cosmograph.handleGraphFit()
          }
          this.spinnerStart(false)
        })
    },
    loadData() {
      this.$store.dispatch(
        "coreui/setContext",
        this.isIntra ? Context.GraphIntra : Context.Graph
      )
      this.$store.dispatch("graph/clear")

      this.displayTransport = !this.isIntra

      // Set form default values
      metadataService
        .getGraphDefault(this.isIntra)
        .then(({ time, frequency, percentage, transport, product, flow }) => {
          // Default state
          this.currentTime = time
          this.frequency = frequency
          this.percentage = percentage
          this.transport = this.isIntra ? null : transport
          this.product = product
          this.flow = flow
          //Sumit form
          this.handleSubmit()
        })
    },
    getSearchFilter() {
      let data = []
      data.push({
        field: this.$t("graph.form.fields.period"),
        value: this.currentTime ? this.currentTime.selectName : ""
      })
      data.push({
        field: this.$t("graph.form.fields.percentage"),
        value: this.percentage ? this.percentage : ""
      })
      if (this.displayTransport) {
        data.push({
          field: this.$t("graph.form.fields.transport"),
          value: this.transport
            ? this.transport
                .map((transp) => {
                  return transp.descr
                })
                .join("#")
            : ""
        })
        data.push({
          field: this.$t("graph.form.fields.product_nstr"),
          value: this.product ? this.product.descr : ""
        })
      } else {
        data.push({
          field: this.$t("graph.form.fields.product_cpa3"),
          value: this.product ? this.product.descr : ""
        })
      }
      data.push({
        field: this.$t("graph.form.fields.flow"),
        value: this.flow ? this.flow.descr : ""
      })
      return data
    },
    showMainModal() {
      this.isMainModal = true
      this.isHelpModal = true
    },
    showInfoModal() {
      this.isMainModal = false
      this.isHelpModal = true
    },
    closeModal() {
      this.isMainModal = false
      this.isHelpModal = false
    },
    spinnerStart(bool) {
      this.spinner = bool
    },
    getData(data, id) {
      if (data != null) {
        return [data, id]
      }
      return null
    },
    fixSliderAccessibility() {
      setTimeout(() => {
        document.querySelectorAll(".vue-slider-dot").forEach((element) => {
          element.setAttribute("aria-label", "slider-graph")
        })
      }, 300)
    },
    fixTabsAccessibility() {
      setTimeout(() => {
        document.querySelectorAll(".nav-tabs").forEach((element) => {
          element.setAttribute("aria-busy", "true")
        })
      }, 300)
    },
    fixTabListAccessibility() {
      setTimeout(() => {
        document.querySelectorAll(".ctablist").forEach((element) => {
          element.setAttribute("aria-busy", "true")
        })
      }, 300)
    },
    fixLabelForSelectAccessibility() {
      setTimeout(() => {
        document.querySelectorAll(".vs__search").forEach((element, index) => {
          const i = index + 1
          element.setAttribute("id", "input__" + i)
        })
      }, 300)
    },
    fixHeaderTableForAccessibility() {
      setTimeout(() => {
        document.querySelectorAll("th").forEach((element) => {
          element.setAttribute("title", element.innerText)
          element.setAttribute("aria-label", element.innerText)
        })
      }, 300)
    },

    setFocusOn() {
      document.getElementById("vs1__combobox").focus()
    }
  },
  created() {
    this.loadData()
    this.fixSliderAccessibility()
    this.fixTabsAccessibility()
    this.fixTabListAccessibility()
    this.fixLabelForSelectAccessibility()
    this.fixHeaderTableForAccessibility()
  }
}
</script>

<style scoped>
.padding-tab {
  padding-top: 45px;
}

label.radio {
  margin-right: 20px;
  margin-bottom: 10px;
}
label {
  margin-bottom: 0px;
}
span {
  padding-left: 5px;
}
</style>
