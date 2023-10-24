<template>
  <div>
    <CDataTable
      id="metricsTable"
      ref="metricsTable"
      v-if="data"
      :items="data"
      :fields="fields"
      :sorterValue="sorterValue"
      column-filter
      :items-per-page="10"
      sorter
      hover
      pagination
      @filtered-items-change="bho()"
      @page-change="setPage()"
      :noItemsView="{
        noResults: this.$t('graph.table.no_filtering_results_available'),
        noItems: this.$t('graph.table.no_items_available')
      }">
      <template #name="{ item }">
        <td headers="head_1">
          {{ item.name }}
        </td>
      </template>
      <template #vulnerability="{ item }">
        <td headers="head_2">
          {{ item.vulnerability }}
        </td>
      </template>
      <template #hubness="{ item }">
        <td headers="head_3">
          {{ item.hubness }}
        </td>
      </template>
      <template #exportStrenght="{ item }">
        <td headers="head_4">
          {{ item.exportStrenght }}
        </td>
      </template>
    </CDataTable>
    <span class="no-visible">{{ page_number }}</span>
  </div>
</template>
<script>
export default {
  name: "GraphTable",
  data: () => ({ page_number: 0 }),
  props: {
    data: {
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
    }
  },
  methods: {
    fixSortingTable() {
      const table = this.$refs.metricsTable
      if (table.$el.children[0].children[0].children[0].children) {
        const thead = table.$el.children[0].children[0].children[0].children
        const tr_0 = thead[0].children
        const tr_1 = thead[1].children
        if (tr_0) {
          for (let i = 0; i <= 4; i++) {
            tr_0[i].children[1].ariaLabel =
              this.$t("graph.table.order_field") + tr_0[i].ariaLabel

            tr_0[i].children[1].role = "button"

            tr_1[i].children[0].ariaLabel =
              this.$t("graph.table.search_field") + tr_0[i].ariaLabel
            tr_1[i].children[0].title =
              this.$t("graph.table.search_field") + tr_0[i].ariaLabel
          }
        }
      }
    },
    fixBodyTable() {
      const table = this.$refs.metricsTable
      const tBody = table.$el.children[0].children[0].children[1]
      tBody.ariaLive = "polite"
      tBody.children[0].children[0].children[0].role = ""
      if (
        tBody.children[0].children[0].children[0].className ==
        "text-center my-5"
      ) {
        tBody.children[0].children[0].children[0].role = "alert"
        tBody.children[0].children[0].children[0].role
      }
      console.log(tBody.children[0].children[0].children[0].role)
    },
    fixNavTable() {
      const table = this.$refs.metricsTable
      if (table.$el.children[1]) {
        const nav = table.$el.children[1]
        nav.ariaLabel = this.$t("graph.table.pagination")
        let nav_buttons = nav.children[0].children
        const next_button = nav_buttons.length - 2
        const last_button = nav_buttons.length - 1

        nav_buttons[0].children[0].ariaLabel = this.$t(
          "graph.table.go_to_first_page"
        )
        nav_buttons[0].children[0].title = this.$t(
          "graph.table.go_to_first_page"
        )
        nav_buttons[1].children[0].ariaLabel = this.$t(
          "graph.table.go_to_previous_page"
        )
        nav_buttons[1].children[0].title = this.$t(
          "graph.table.go_to_previous_page"
        )

        nav_buttons[next_button].children[0].ariaLabel = this.$t(
          "graph.table.go_to_next_page"
        )
        nav_buttons[next_button].children[0].title = this.$t(
          "graph.table.go_to_next_page"
        )

        nav_buttons[last_button].children[0].ariaLabel = this.$t(
          "graph.table.go_to_last_page"
        )
        nav_buttons[last_button].children[0].title = this.$t(
          "graph.table.go_to_last_page"
        )

        for (let i = 2; i <= nav_buttons.length - 3; i++) {
          if (nav_buttons[i].className == "active page-item") {
            nav_buttons[i].children[0].ariaLabel =
              this.$t("graph.table.current_page") +
              nav_buttons[i].children[0].innerText
            nav_buttons[i].children[0].title =
              this.$t("graph.table.current_page") +
              nav_buttons[i].children[0].innerText
          } else {
            nav_buttons[i].children[0].ariaLabel =
              this.$t("graph.table.go_to_page") +
              nav_buttons[i].children[0].innerText
            nav_buttons[i].children[0].title =
              this.$t("graph.table.go_to_page") +
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
    bho() {
      this.setPage()
    }
  },
  mounted() {
    this.fixSortingTable()
    this.fixNavTable()
    this.fixBodyTable()
  },
  updated() {
    this.fixSortingTable()
    this.fixNavTable()
    this.fixBodyTable()
  }
}
</script>
<style>
.no-visible {
  display: none;
}
</style>
