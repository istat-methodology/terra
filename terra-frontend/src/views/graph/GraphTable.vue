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
      @filtered-items-change="setPage()"
      @page-change="setPage()"
      :noItemsView="{
        noResults: this.$t('common.table.no_filtering_results_available'),
        noItems: this.$t('common.table.no_items_available')
      }">
      <template #label="{ item }">
        <td headers="head_0">
          {{ item.label }}
        </td>
      </template>
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
  data: () => ({
    page_number: 0
  }),
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
      if (this.$refs.metricsTable) {
        const table = this.$refs.metricsTable
        if (table.$el.children[0].children[0].children[0].children) {
          const thead = table.$el.children[0].children[0].children[0].children

          if (thead[0].children && thead[1].children) {
            const tr_0 = thead[0].children
            const tr_1 = thead[1].children
            //console.log(tr_0.length - 1)
            const tr_len = tr_0.length - 1
            if (tr_0) {
              for (let i = 0; i <= tr_len; i++) {
                if (tr_0[i].children[1]) {
                  tr_0[i].children[1].ariaLabel =
                    this.$t("common.table.order_field") + tr_0[i].innerText
                  tr_0[i].children[1].role = "button"
                }
                if (tr_0[i].children[0]) {
                  tr_1[i].children[0].ariaLabel =
                    this.$t("common.table.search_field") + tr_0[i].innerText
                  tr_1[i].children[0].title =
                    this.$t("common.table.search_field") + tr_0[i].innerText
                }
              }
            }
          }
        }
      }
    },
    fixBodyTable() {
      if (this.$refs.metricsTable) {
        const table = this.$refs.metricsTable
        const tBody = table.$el.children[0].children[0].children[1]
        tBody.ariaLive = "polite"
        if (tBody.children[0].children[0].children[0]) {
          if (
            tBody.children[0].children[0].children[0].className ==
            "text-center my-5"
          ) {
            tBody.children[0].children[0].children[0].role = "alert"
            //console.log(tBody.children[0].children[0].children[0].role)
          }
        }
      }
    },
    fixNavTable() {
      if (this.$refs.metricsTable) {
        const table = this.$refs.metricsTable
        if (table.$el.children[1]) {
          const nav = table.$el.children[1]
          nav.ariaLabel = this.$t("common.table.pagination")
          if (nav.children[0].children) {
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
              }
            }
          }
        }
      }
    },
    setPage() {
      if (this.page_number > 10) this.page_number = 0
      this.page_number = this.page_number + 1
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
