<template>
  <div>
    <!--h1 class="sr-only">{{ modalTitle }}</h1-->
    <CModal
      :show="showModal"
      :closeOnBackdrop="false"
      @update:show="closeModal"
      size="lg">
      <template #header>
        <span class="scenario-title float-left" role="heading" aria-level="2">{{
          modalTitle
        }}</span>
        <span class="float-right">
          <exporter
            filename="terra_scenario"
            :data="getData(csvTable, 'table')"
            :options="['csv']"
            source="table"
            :header="csvHeader">
          </exporter>
        </span>
      </template>
      <CDataTable
        v-if="nodesTable"
        id="scenarioTable"
        ref="scenarioTable"
        :items="nodesTable"
        :fields="fields"
        :items-per-page="5"
        sorter
        hover
        pagination
        @page-change="setPage()">
        <!--CDataTable
        v-if="nodesTable"
        :items="nodesTable"
        :fields="fields"
        column-filter
        :column-filter-value.sync="columnFilterValue"
        :items-per-page="5"
        :sorterValue="sorterValue"
        sorter
        hover
        pagination-->
        <!--
            source: field.source,
            destination: field.destination,
            percentage: field.percentage,
            flow: field.flow
        -->
        <template #source="{ item }">
          <td headers="head_scenario_0">
            {{ item.source }}
          </td>
        </template>
        <template #destination="{ item }">
          <td headers="head_scenario_1">
            {{ item.destination }}
          </td>
        </template>
        <template #euro="{ item }">
          <td headers="head_scenario_2">
            {{ item.euro }}
          </td>
        </template>
        <template #percentage="{ item }">
          <td headers="head_scenario_3">
            {{ item.percentage }}
          </td>
        </template>
        <template #flow="{ item }">
          <td headers="head_scenario_4">
            {{ item.flow }}
          </td>
        </template>
        <template #show_delete="{ item }">
          <td>
            <span
              v-if="selectedNode.id > 0 && !displayTransport && showScenario"
              class="icon-link"
              @click="deleteRow(item)"
              :title="$t('common.delete')"
              ><close-icon alt="" />
            </span>
          </td>
        </template>
      </CDataTable>
      <div class="row">
        <div class="col-12">
          <label for="checkScenario" class="scenario-analysis">
            {{ scenarioTitle }}
            <span class="ml-4 ml-4">
              <CSwitch
                id="checkScenario"
                color="primary"
                size="sm"
                labelOn="✓"
                labelOff="X"
                :checked="showScenario"
                @update:checked="toggleScenario" />
            </span>
          </label>
        </div>
      </div>
      <!-- Drag'n drop -->
      <div v-if="showScenario && displayTransport">
        <div class="row constraint-container">
          <div class="col-left constraint-left">
            {{ $t("graph.scenario.transports_selected") }}
          </div>
          <div class="col-center">
            <!-- nothing -->
          </div>
          <div class="col-right constraint-right">
            {{ $t("graph.scenario.transports_scenario") }}
          </div>
        </div>
        <div class="row drag-container">
          <div
            class="col-left drop-zone"
            @drop="onDropTransports($event)"
            @dragenter.prevent
            @dragover.prevent>
            <div
              v-for="transport in transports"
              :key="transport.id"
              class="drag-el"
              draggable="true"
              @dragstart="startDrag($event, transport)">
              {{ transport.descr }}
            </div>
          </div>
          <div class="col-center">
            <!-- Nothing -->
          </div>
          <div
            class="col-right drop-zone"
            @drop="onDropScenario($event)"
            @dragenter.prevent
            @dragover.prevent>
            <div
              v-for="scenarioTransport in scenarioTransports"
              :key="scenarioTransport.id"
              class="drag-el"
              draggable="true"
              @dragstart="startDrag($event, scenarioTransport)">
              {{ scenarioTransport.descr }}
            </div>
          </div>
        </div>
      </div>
      <template #footer>
        <CButton
          v-if="showScenario"
          color="danger"
          shape="square"
          size="sm"
          @click="applyConstraints"
          :title="$t('common.apply')"
          >{{ $t("common.apply") }}</CButton
        >
        <CButton
          color="primary"
          shape="square"
          size="sm"
          @click="closeModal"
          :title="$t('common.close')">
          {{ $t("common.close") }}
        </CButton>
      </template>
    </CModal>
    <span class="no-visible">{{ page_number }}</span>
  </div>
</template>
<script>
import exporter from "@/components/Exporter"
export default {
  name: "GraphScenario",
  components: {
    exporter
  },
  data: () => ({
    showScenario: false,
    columnFilterValue: {},
    page_number: 0
  }),
  props: {
    showModal: {
      type: Boolean,
      default: false
    },
    displayTransport: {
      type: Boolean,
      default: false
    },
    selectedNodesTable: {
      type: Array,
      default: () => null
    },
    fields: {
      type: Array,
      default: () => []
    },
    sorterValue: {
      type: Object,
      default: () => ({ column: null, asc: true })
    },
    selectedNode: {
      type: Object,
      default: () => ({ id: -1, name: "" })
    },
    selectedTransports: {
      type: Array,
      default: () => null
    },
    selectedScenarioTransports: {
      type: Array,
      default: () => null
    }
  },
  computed: {
    nodesTable: {
      get() {
        return this.selectedNodesTable
      },
      set(value) {
        this.$emit("updateNodesTable", value)
      }
    },
    csvTable: {
      get() {
        return this.selectedNodesTable.map((field) => {
          return {
            source: field.source,
            destination: field.destination,
            euro: field.euro,
            percentage: field.percentage,
            flow: field.flow
          }
        })
      },
      set(value) {
        this.$emit("updateNodesTable", value)
      }
    },
    csvHeader: {
      get() {
        return this.fields.map((field) => field.label)
      },
      set(value) {
        this.$emit("fields", value)
      }
    },
    transports: {
      get() {
        return this.selectedTransports
      },
      set(value) {
        this.$emit("updateTransports", value)
      }
    },
    scenarioTransports: {
      get() {
        return this.selectedScenarioTransports
      },
      set(value) {
        this.$emit("updateScenarioTransports", value)
      }
    },
    modalTitle() {
      return this.selectedNode.id > 0
        ? this.$t("graph.scenario.main", { country: this.selectedNode.name })
        : this.$t("graph.scenario.mainEdge")
    },
    scenarioTitle() {
      return this.selectedNode.id > 0
        ? this.displayTransport
          ? this.$t("graph.scenario.title_extra_node")
          : this.$t("graph.scenario.title_world_node")
        : this.displayTransport
        ? this.$t("graph.scenario.title_extra_edge")
        : this.$t("graph.scenario.title_world_edge")
    }
  },
  methods: {
    toggleScenario() {
      this.showScenario = !this.showScenario
    },
    startDrag(event, item) {
      event.dataTransfer.dropEffect = "move"
      event.dataTransfer.effectAllowed = "move"
      event.dataTransfer.setData("itemId", item.id)
    },
    onDropTransports(event) {
      const itemId = event.dataTransfer.getData("ItemId")
      this.scenarioTransports = this.scenarioTransports.filter(
        (tr) => tr.id != itemId
      )
    },
    onDropScenario(event) {
      const itemId = event.dataTransfer.getData("ItemId")
      const transport = this.transports.find((tr) => tr.id == itemId)
      if (!this.scenarioTransports.find((tr) => tr.id == transport.id))
        this.scenarioTransports.push(transport)
    },
    deleteRow(row) {
      var updatedTable = this.nodesTable.filter((rw) => rw != row)
      //console.log(updatedTable.length)
      this.$emit("updateNodesTable", updatedTable)
    },
    closeModal() {
      this.$emit("closeModal")
      this.columnFilterValue = {}
      this.showScenario = false
    },
    applyConstraints() {
      this.showScenario = false
      this.$emit("applyConstraints")
    },
    getData(data, id) {
      if (data != null) {
        return [data, id]
      }
      return null
    },
    fixHeaderTableForAccessibility() {
      setTimeout(() => {
        var thead = document
          .getElementById("scenarioTable")
          .querySelector("thead > tr")
        thead.querySelectorAll("th").forEach((element, index) => {
          element.setAttribute("id", "head_scenario" + index)
          element.setAttribute("title", element.innerText)
          element.setAttribute("aria-label", element.innerText)
        })
      }, 300)
    },
    fixSortingTable() {
      const table = this.$refs.scenarioTable
      if (table.$el.children[0].children[0].children[0].children) {
        const thead = table.$el.children[0].children[0].children[0].children
        if (thead[0].children) {
          const tr_0 = thead[0].children

          if (tr_0) {
            for (let i = 0; i <= 4; i++) {
              if (tr_0[i].children[1]) {
                tr_0[i].children[1].ariaLabel =
                  this.$t("common.table.order_field") + tr_0[i].ariaLabel

                tr_0[i].children[1].role = "button"
              }
            }
          }
        }
      }
    },
    fixNavTable() {
      const table = this.$refs.scenarioTable
      if (table.$el.children[1]) {
        const nav = table.$el.children[1]
        nav.ariaLabel = this.$t("common.table.pagination")
        let nav_buttons = nav.children[0].children
        const next_button = nav_buttons.length - 2
        const last_button = nav_buttons.length - 1

        nav_buttons[0].children[0].ariaLabel = this.$t(
          "common.table.go_to_first_page"
        )
        nav_buttons[0].children[0].title = this.$t(
          "common.table.go_to_first_page"
        )
        nav_buttons[1].children[0].ariaLabel = this.$t(
          "common.table.go_to_previous_page"
        )
        nav_buttons[1].children[0].title = this.$t(
          "common.table.go_to_previous_page"
        )

        nav_buttons[next_button].children[0].ariaLabel = this.$t(
          "common.table.go_to_next_page"
        )
        nav_buttons[next_button].children[0].title = this.$t(
          "common.table.go_to_next_page"
        )

        nav_buttons[last_button].children[0].ariaLabel = this.$t(
          "common.table.go_to_last_page"
        )
        nav_buttons[last_button].children[0].title = this.$t(
          "common.table.go_to_last_page"
        )
        for (let i = 2; i <= nav_buttons.length - 3; i++) {
          if (nav_buttons[i].className == "active page-item") {
            nav_buttons[i].children[0].ariaLabel =
              this.$t("common.table.current_page") +
              nav_buttons[i].children[0].innerText
            nav_buttons[i].children[0].title =
              this.$t("common.table.current_page") +
              nav_buttons[i].children[0].innerText
          } else {
            nav_buttons[i].children[0].ariaLabel =
              this.$t("common.table.go_to_page") +
              nav_buttons[i].children[0].innerText
            nav_buttons[i].children[0].title =
              this.$t("common.table.go_to_page") +
              nav_buttons[i].children[0].innerText
            //
          }
        }
      }
    },
    setPage() {
      if (this.page_number > 10) this.page_number = 0
      this.page_number = this.page_number + 1
    },
    fixBodyTable() {
      const table = this.$refs.metricsTable
      if (table) {
        if (table.$el) {
          if (table.$el.children[0].children[0].children[1]) {
            const tBody = table.$el.children[0].children[0].children[1]
            tBody.ariaLive = "polite"
            //console.log(tBody)
          }
        }
      }
    }
  },
  mounted() {
    this.fixHeaderTableForAccessibility()
    this.fixSortingTable()
    this.fixNavTable()
    this.fixBodyTable()
  },
  updated() {
    this.fixHeaderTableForAccessibility()
    this.fixSortingTable()
    this.fixNavTable()
    this.fixBodyTable()
  }
}
</script>
<style scoped>
.scenario-title {
  padding-top: 0.5rem;
  padding-left: 0.5rem;
  font-size: 16px;
  font-weight: 600;
}
.scenario-analysis {
  font-weight: 500;
  font-size: 16px;
  padding: 1rem 0.4rem 0rem 0.4rem;
  color: #321fdb;
  border-top: 1px solid #d8dbe0;
}

.constraint-left {
  padding: 0.8rem 0rem 0.4rem 0.2rem;
  font-weight: 500;
  margin-top: 0.6rem;
}

.constraint-right {
  padding: 0.8rem 0rem 0.4rem 1.4rem;
  font-weight: 500;
  margin-top: 0.6rem;
}

.col-left {
  flex: 0 0 47%;
  max-width: 47%;
}

.col-right {
  flex: 0 0 47%;
  max-width: 47%;
}

.col-center {
  flex: 0 0 6%;
  max-width: 6%;
}

.drag-container {
  margin-right: 0;
  margin-left: 0;
}

.drop-zone {
  border: 1px solid #ebedef;
  border-radius: 0.2rem;
  padding: 10px;
  min-height: 120px;
}

.drag-el {
  border-radius: 0.2rem;
  background-color: #ebedef;
  border: 1px solid #9da5b1;
  color: #4f5d73;
  padding: 2px 10px;
  margin-bottom: 4px;
  cursor: grab;
  cursor: -moz-grab;
  cursor: -webkit-grab;
}

.drag-el:active {
  cursor: grabbing;
  cursor: -moz-grabbing;
  cursor: -webkit-grabbing;
}

.drag-el:nth-last-of-type(1) {
  margin-bottom: 0;
}
.no-visible {
  display: none;
}
</style>
