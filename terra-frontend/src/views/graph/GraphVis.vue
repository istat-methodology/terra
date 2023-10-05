<template>
  <div>
    <CCard class="card-graph" :title="'TERRA - ' + title">
      <CCardHeader>
        <span class="card-title" role="heading" aria-level="2">{{
          title
        }}</span>
        <span class="btn-group float-right">
          <exporter
            filename="terra_graph_analysis"
            :data="getData('graph', this.$refs.graph)"
            :nodes="nodes"
            :edges="edges"
            source="graph">
          </exporter>
          <!--CButton color="link" @click="showInfo" title="Info" tabindex="0"
            >Info</CButton
          -->
        </span>
        <div class="graph-info">
          <span v-if="graphDensity > 0">
            <span
              class="text-primary"
              :title="$t('graph.stats.density') + ' ' + graphDensity">
              {{ $t("graph.stats.density") }} </span
            >{{ graphDensity }}</span
          >
          <span class="pl-2" v-if="nodeMetric">
            <span
              class="text-primary"
              :title="$t('graph.stats.country') + ' ' + nodeMetric.country"
              >{{ $t("graph.stats.country") }} </span
            >{{ nodeMetric.country }}
            <span
              class="text-primary"
              :title="
                $t('graph.stats.exportationstrength') +
                ' ' +
                nodeMetric.exportationstrength
              "
              >, {{ $t("graph.stats.exportationstrength") }} </span
            >{{ nodeMetric.exportationstrength }}
            <span
              class="text-primary"
              :title="
                $t('graph.stats.vulnerability') + '' + nodeMetric.vulnerability
              "
              >, {{ $t("graph.stats.vulnerability") }}
            </span>
            {{ nodeMetric.vulnerability }}
            <span
              class="text-primary"
              :title="$t('graph.stats.hubness') + ' ' + nodeMetric.hubness"
              >, {{ $t("graph.stats.hubness") }} </span
            >{{ nodeMetric.hubness }}</span
          >
        </div>
      </CCardHeader>
      <CCardBody class="card-no-border"
        ><circle-spin v-if="this.spinner" class="circle-spin"></circle-spin>
        <network
          aria-hidden="true"
          id="graph"
          class="network"
          ref="graph"
          keyboard="true"
          :nodes="nodes"
          :edges="edges"
          :options="options"
          @select-edge="handleGraphSelect"
          @hover-node="handleOverNode" />
      </CCardBody>
      <slot>
        <!-- Slider -->
      </slot>
    </CCard>
    <cosmo-scenario
      :showModal="scenarioModal"
      :selectedNodesTable="selectedNodesTable"
      :fields="scenarioFields"
      :displayTransport="displayTransport"
      :selectedNode="selectedNode"
      :selectedTransports="localTransports"
      :selectedScenarioTransports="scenarioTransports"
      @closeModal="closeModal"
      @updateNodesTable="handleNodesTable"
      @updateTransports="handleUpdateTransports"
      @updateScenarioTransports="handleScenarioTransports"
      @applyConstraints="applyConstraints" />
  </div>
</template>
<script>
import { mapGetters } from "vuex"
import { Network } from "vue-visjs"
import {
  options,
  getNode,
  getEdge,
  getCentrality,
  getTransportDifference,
  containsAllTransports,
  containsEdge,
  scenarioFieldsIt,
  scenarioFieldsEn
} from "@/common"
import spinnerMixin from "@/components/mixins/spinner.mixin"
import exporter from "@/components/Exporter"
import GraphScenario from "@/views/graph/GraphScenario"

export default {
  name: "GraphVis",
  components: { Network, exporter, "cosmo-scenario": GraphScenario },
  mixins: [spinnerMixin],
  data: () => ({
    options: { ...options },
    nodeMetric: null,
    selectedNode: {},
    selectedEdges: [],
    selectedNodesTable: [],
    nodeSelected: false,
    //Make a local copy of transports for cosmo-scenario
    localTransports: [],
    scenarioTransports: [],
    //Scenario modal
    scenarioFieldsIt: [...scenarioFieldsIt],
    scenarioFieldsEn: [...scenarioFieldsEn],
    scenarioModal: false,
    //Metrics table
    sorterValue: { column: "percentage", asc: false }
  }),
  computed: {
    ...mapGetters("coreui", ["isItalian"]),
    ...mapGetters("classification", { transportCls: "transports" }),
    title() {
      return this.isIntra
        ? this.$t("graph.titleIntra")
        : this.$t("graph.titleExtra")
    },
    scenarioFields() {
      return this.isItalian ? this.scenarioFieldsIt : this.scenarioFieldsEn
    },
    graphDensity() {
      return this.metrics ? this.metrics.density.toFixed(2) : 0
    }
  },

  props: {
    isIntra: {
      type: Boolean,
      default: true
    },
    nodes: {
      type: Array,
      default: () => []
    },
    edges: {
      type: Array,
      default: () => []
    },
    metrics: {
      type: Object,
      default: () => null
    },
    displayTransport: {
      type: Boolean,
      default: true
    },
    transports: {
      type: Array,
      default: () => null
    },
    spinner: {
      type: Boolean,
      default: false
    }
  },
  methods: {
    handleUpdateTransports(trs) {
      this.localTransports = trs
    },
    handleScenarioTransports(trs) {
      this.scenarioTransports = trs
    },
    handleNodesTable(table) {
      this.selectedNodesTable = table
    },
    handleGraphSelect(selectedGraph) {
      if (selectedGraph.nodes.length > 0) {
        //user clicked a node
        this.nodeSelected = true
        this.handleNodeSelect(selectedGraph)
      } else {
        //user clicked an edge
        this.nodeSelected = false
        this.handleEdgeSelect(selectedGraph)
      }
    },
    handleNodeSelect(selectedGraph) {
      this.selectedEdges = []
      this.selectedNodesTable = []
      this.selectedNode = getNode(this.nodes, selectedGraph.nodes[0])

      //Compute total weight
      var totalImport = 0
      var totalExport = 0
      selectedGraph.edges.forEach((edgeId) => {
        const selectedEdge = getEdge(this.edges, edgeId)
        if (selectedEdge.from == this.selectedNode.id) {
          //export
          totalExport += selectedEdge.weight
        } else {
          //import
          totalImport += selectedEdge.weight
        }
      })

      var percentage = 0
      selectedGraph.edges.forEach((edgeId) => {
        const selectedEdge = getEdge(this.edges, edgeId)
        const sourceNode = getNode(this.nodes, selectedEdge.from)
        const destinationNode = getNode(this.nodes, selectedEdge.to)

        this.selectedEdges.push(selectedEdge)
        if (sourceNode.id == this.selectedNode.id) {
          //export
          percentage = (selectedEdge.weight / totalExport) * 100
        } else {
          //import
          percentage = (selectedEdge.weight / totalImport) * 100
        }

        var weightFormatted = selectedEdge.weight

        this.selectedNodesTable.push({
          source: sourceNode.name,
          from: selectedEdge.from,
          destination: destinationNode.name,
          to: selectedEdge.to,
          total: weightFormatted.toLocaleString(this.$i18n.locale),
          percentage:
            Math.round((percentage + Number.EPSILON) * 100) / 100 + "%",
          flow: this.selectedNode.id == sourceNode.id ? "Export" : "Import",
          euro:
            selectedEdge.VALUE_IN_EUROS.toLocaleString(this.$i18n.locale) + "€"
        })
      })
      //Local copy of selected transports
      this.localTransports = []
      if (this.displayTransport) {
        this.localTransports = containsAllTransports(this.transports)
          ? [...this.transportCls.slice(1)]
          : [...this.transports]
      }
      this.scenarioModal = true
    },
    handleEdgeSelect(selectedGraph) {
      this.selectedEdges = []
      this.selectedNodesTable = []
      this.selectedNode = { id: -1, name: "" }
      //Compute total weight
      var sumOfSelectedEdge = 0
      selectedGraph.edges.forEach((edgeId) => {
        const selectedEdge = getEdge(this.edges, edgeId)
        sumOfSelectedEdge = sumOfSelectedEdge + selectedEdge.weight
      })

      selectedGraph.edges.forEach((edgeId) => {
        const selectedEdge = getEdge(this.edges, edgeId)
        const sourceNode = getNode(this.nodes, selectedEdge.from)
        const destinationNode = getNode(this.nodes, selectedEdge.to)

        this.selectedEdges.push(selectedEdge)

        var percentage = (selectedEdge.weight / sumOfSelectedEdge) * 100
        var weightFormatted = selectedEdge.weight

        this.selectedNodesTable.push({
          source: sourceNode.name,
          from: selectedEdge.from,
          destination: destinationNode.name,
          to: selectedEdge.to,
          total: weightFormatted.toLocaleString("en-US"),
          percentage:
            Math.round((percentage + Number.EPSILON) * 100) / 100 + "%",
          flow: "-",
          euro:
            selectedEdge.VALUE_IN_EUROS.toLocaleString(this.$i18n.locale) + "€"
        })
      })
      //Local copy of selected transports
      this.localTransports = []
      if (this.displayTransport) {
        this.localTransports = containsAllTransports(this.transports)
          ? [...this.transportCls.slice(1)]
          : [...this.transports]
      }
      this.scenarioModal = true
    },
    handleOverNode(event) {
      const nodeId = event.node
      this.nodeMetric = getCentrality(this.nodes, nodeId, this.metrics)
    },
    handleGraphFit() {
      this.$refs.graph.fit()
    },
    applyConstraints() {
      const constraints = []

      //New business logic here (only for nodes)!!!!
      var nodesDiff = []
      if (this.nodeSelected && !this.displayTransport) {
        //console.log("Node scenario, applying new business logic!")
        nodesDiff = this.selectedEdges.filter(
          (edge) => !containsEdge(edge, this.selectedNodesTable)
        )
      } else {
        //console.log("Edge scenario, doing nothing :)")
        nodesDiff = this.selectedEdges
      }

      //Local copy of selected transports
      this.localTransports = []
      if (this.displayTransport) {
        this.localTransports = containsAllTransports(this.transports)
          ? [...this.transportCls.slice(1)]
          : [...this.transports]
      }

      nodesDiff.forEach((edge) => {
        constraints.push({
          from: getNode(this.nodes, edge.from).label,
          to: getNode(this.nodes, edge.to).label,
          exclude: this.displayTransport
            ? getTransportDifference(
                this.localTransports,
                this.scenarioTransports
              )
            : "-99"
        })
      })
      this.$emit("applyConstraints", constraints)
      this.closeModal()
    },
    showInfo() {
      this.$emit("showinfo")
    },
    closeModal() {
      //Clear selected scenario transports
      this.scenarioTransports = []
      this.scenarioModal = false
    },
    getData(id) {
      var nodes = []
      var edges = []
      for (var edgeId in this.edges) {
        edges.push({
          from: this.edges[edgeId].from,
          to: this.edges[edgeId].to
        })
      }
      for (var nodeId in this.nodes) {
        nodes.push({
          id: this.nodes[nodeId].id,
          label: this.nodes[nodeId].label,
          x: this.nodes[nodeId].x,
          y: this.nodes[nodeId].y
        })
      }
      let jsonData = JSON.stringify({ nodes, edges })
      return [jsonData, id]
    }
  }
}
</script>
<style scoped>
.network {
  text-align: center;
  height: 100%;
  margin: 0 0;
}

.graph-info {
  margin-top: 0.6em;
  font-size: small;
  min-height: 30px;
  padding-left: 0.8rem;
  margin-bottom: 0.6rem;
  font-weight: 400;
}
</style>
